#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from contextlib import suppress
from datetime import datetime, timezone

from pefile import (
    DEBUG_TYPE,
    DIRECTORY_ENTRY,
    image_characteristics,
    MACHINE_TYPE,
    SUBSYSTEM_TYPE,
    PE,
)

from ....lib.dotnet.header import DotNetHeader
from ....lib.json import flattened
from ... import arg, Unit


class pemeta(Unit):
    """
    Extract metadata from PE files, including:

    - File version resource
    - Code signature information
    - Timestamps
    - If present, .NET header information
    """
    def __init__(
        self, all : arg('-c', '--custom',
            help='Unless enabled, everything will be extracted.') = True,
        debug      : arg('-D', help='Parse the PDB path from the debug directory.') = False,
        dotnet     : arg('-N', help='Parse the .NET header.') = False,
        signatures : arg('-S', help='Parse digital signatures.') = False,
        timestamps : arg('-T', help='Extract time stamps.') = False,
        version    : arg('-V', help='Parse the VERSION resource.') = False,
        header     : arg('-H', help='Parse data from the PE header.') = False,
        tabular    : arg('-t', help='Print information in a table rather than as JSON') = False,
        timeraw    : arg('-r', help='Extract time stamps as numbers instead of human-readable format.') = False,
    ):
        super().__init__(
            debug=all or debug,
            dotnet=all or dotnet,
            signatures=all or signatures,
            timestamps=all or timestamps,
            version=all or version,
            header=all or header,
            timeraw=timeraw,
            tabular=tabular,
        )

    @classmethod
    def _ensure_string(cls, x):
        if not isinstance(x, str):
            x = repr(x) if not isinstance(x, bytes) else x.decode(cls.codec, 'backslashreplace')
        return x

    @classmethod
    def _parse_pedict(cls, bin):
        return dict((
            cls._ensure_string(key),
            cls._ensure_string(val)
        ) for key, val in bin.items() if val)

    @classmethod
    def parse_signature(cls, data: bytearray) -> dict:
        """
        Extracts a JSON-serializable and human readable dictionary with information about
        time stamp and code signing certificates that are attached to the input PE file.
        """
        from refinery.units.formats.pkcs7 import pkcs7
        from refinery.units.formats.pe.pesig import pesig

        try:
            signature = json.loads(data | pesig | pkcs7)
        except Exception as E:
            raise ValueError(F'PKCS7 parser failed with error: {E!s}')

        info = {}

        def find_timestamps(entry):
            if isinstance(entry, dict):
                if set(entry.keys()) == {'type', 'value'}:
                    if entry['type'] == 'signing_time':
                        return {'Timestamp': entry['value']}
                for value in entry.values():
                    result = find_timestamps(value)
                    if result is None:
                        continue
                    with suppress(KeyError):
                        result.setdefault('Timestamp Issuer', entry['sid']['issuer']['common_name'])
                    return result
            elif isinstance(entry, list):
                for value in entry:
                    result = find_timestamps(value)
                    if result is None:
                        continue
                    return result

        timestamp_info = find_timestamps(signature)
        if timestamp_info is not None:
            info.update(timestamp_info)

        try:
            certificates = signature['content']['certificates']
        except KeyError:
            return info

        for certificate in certificates:
            with suppress(Exception):
                tbs = certificate['tbs_certificate']
                primary_signature = False
                for extension in tbs['extensions']:
                    if extension['extn_id'] == 'extended_key_usage' and 'code_signing' in extension['extn_value']:
                        primary_signature = True
                    if extension['extn_id'] == 'key_usage' and 'key_cert_sign' in extension['extn_value']:
                        primary_signature = False
                        break
                if not primary_signature:
                    continue
                serial = int(tbs['serial_number'], 0)
                serial = F'{serial:x}'
                if len(serial) % 2:
                    serial = '0' + serial
                info.update(
                    Issuer=tbs['issuer']['common_name'],
                    Subject=tbs['subject']['common_name'],
                    Serial=serial,
                )
                return info
        return info

    @classmethod
    def parse_version(cls, pe: PE, data) -> dict:
        """
        Extracts a JSON-serializable and human readable dictionary with information about
        the version resource of an input PE file, if available.
        """
        try:
            pe.parse_data_directories(directories=[DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE']])
            FileInfoList = pe.FileInfo
        except AttributeError:
            return None
        for FileInfo in FileInfoList:
            for FileInfoEntry in FileInfo:
                with suppress(AttributeError):
                    for StringTableEntry in FileInfoEntry.StringTable:
                        StringTableEntryParsed = cls._parse_pedict(StringTableEntry.entries)
                        with suppress(AttributeError):
                            LangID = StringTableEntry.entries.get('LangID', None) or StringTableEntry.LangID
                            LangID = int(LangID, 0x10) if not isinstance(LangID, int) else LangID
                            LangHi = LangID >> 0x10
                            LangLo = LangID & 0xFFFF
                            Language = cls._LCID.get(LangHi, 'Language Neutral')
                            Charset = cls._CHARSET.get(LangLo, 'Unknown Charset')
                            StringTableEntryParsed.update(
                                LangID=F'{LangID:08X}',
                                Charset=Charset,
                                Language=Language
                            )
                        return StringTableEntryParsed

    @classmethod
    def parse_header(cls, pe: PE, data) -> dict:
        def format_macro_name(name: str, prefix, convert=True):
            name = name.split('_')[prefix:]
            if convert:
                for k, part in enumerate(name):
                    name[k] = part.upper() if len(part) <= 3 else part.capitalize()
            return ' '.join(name)

        characteristics = [
            name for name, mask in image_characteristics
            if pe.FILE_HEADER.Characteristics & mask
        ]
        header_information = {
            'Machine': format_macro_name(MACHINE_TYPE[pe.FILE_HEADER.Machine], 3, False),
            'Subsystem': format_macro_name(SUBSYSTEM_TYPE[pe.OPTIONAL_HEADER.Subsystem], 2),
        }
        for typespec, flag in {
            'EXE': 'IMAGE_FILE_EXECUTABLE_IMAGE',
            'DLL': 'IMAGE_FILE_DLL',
            'SYS': 'IMAGE_FILE_SYSTEM'
        }.items():
            if flag in characteristics:
                header_information['Type'] = typespec
        address_width = None
        if 'IMAGE_FILE_16BIT_MACHINE' in characteristics:
            address_width = 4
        elif pe.FILE_HEADER.Machine == MACHINE_TYPE['IMAGE_FILE_MACHINE_I386']:
            address_width = 8
        elif pe.FILE_HEADER.Machine == MACHINE_TYPE['IMAGE_FILE_MACHINE_AMD64']:
            address_width = 16
        if address_width:
            header_information['Bits'] = 4 * address_width
        else:
            address_width = 16
        header_information['ImageBase'] = F'0x{pe.OPTIONAL_HEADER.ImageBase:0{address_width}}'
        return header_information

    @classmethod
    def parse_time_stamps(cls, pe: PE, raw_time_stamps: bool) -> dict:
        """
        Extracts time stamps from the PE header (link time), as well as from the imports,
        exports, debug, and resource directory. The resource time stamp is also parsed as
        a DOS time stamp and returned as the "Delphi" time stamp.
        """
        if raw_time_stamps:
            def dt(ts): return ts
        else:
            def dt(ts):
                # parse as UTC but then forget time zone information
                return datetime.fromtimestamp(
                    ts,
                    tz=timezone.utc
                ).replace(tzinfo=None)

        pe.parse_data_directories(directories=[
            DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
            DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT'],
            DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_DEBUG'],
            DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE']
        ])

        info = {}

        with suppress(AttributeError):
            info.update(Linker=dt(pe.FILE_HEADER.TimeDateStamp))

        with suppress(AttributeError):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                info.update(Import=dt(entry.TimeDateStamp()))

        with suppress(AttributeError):
            for entry in pe.DIRECTORY_ENTRY_DEBUG:
                info.update(DbgDir=dt(entry.struct.TimeDateStamp))

        with suppress(AttributeError):
            Export = pe.DIRECTORY_ENTRY_EXPORT.struct.TimeDateStamp
            if Export: info.update(Export=dt(Export))

        with suppress(AttributeError):
            res_timestamp = pe.DIRECTORY_ENTRY_RESOURCE.struct.TimeDateStamp
            if res_timestamp:
                with suppress(ValueError):
                    from ...misc.datefix import datefix
                    dos = datefix.dostime(res_timestamp)
                    info.update(Delphi=dos)
                    info.update(RsrcTS=dt(res_timestamp))

        def norm(value):
            if isinstance(value, int):
                return value
            return str(value)

        return {key: norm(value) for key, value in info.items()}

    @classmethod
    def parse_dotnet(cls, pe: PE, data):
        """
        Extracts a JSON-serializable and human readable dictionary with information about
        the .NET metadata of an input PE file.
        """
        header = DotNetHeader(data, pe=pe)
        tables = header.meta.Streams.Tables
        info = dict(
            RuntimeVersion=F'{header.head.MajorRuntimeVersion}.{header.head.MinorRuntimeVersion}',
            Version=F'{header.meta.MajorVersion}.{header.meta.MinorVersion}',
            VersionString=header.meta.VersionString
        )

        info['Flags'] = [name for name, check in header.head.KnownFlags.items() if check]

        if len(tables.Assembly) == 1:
            assembly = tables.Assembly[0]
            info.update(
                AssemblyName=assembly.Name,
                Release='{}.{}.{}.{}'.format(
                    assembly.MajorVersion,
                    assembly.MinorVersion,
                    assembly.BuildNumber,
                    assembly.RevisionNumber
                )
            )

        try:
            entry = header.head.EntryPointToken + pe.OPTIONAL_HEADER.ImageBase
            info.update(EntryPoint=F'0x{entry:08X}')
        except AttributeError:
            pass

        if len(tables.Module) == 1:
            module = tables.Module[0]
            info.update(ModuleName=module.Name)

        return info

    @classmethod
    def parse_debug(cls, pe: PE, data):
        result = {}
        pe.parse_data_directories(directories=[
            DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_DEBUG']])
        for dbg in pe.DIRECTORY_ENTRY_DEBUG:
            if DEBUG_TYPE.get(dbg.struct.Type, None) != 'IMAGE_DEBUG_TYPE_CODEVIEW':
                continue
            with suppress(Exception):
                pdb = dbg.entry.PdbFileName
                if 0 in pdb:
                    pdb = pdb[:pdb.index(0)]
                result.update(
                    PdbPath=pdb.decode(cls.codec),
                    PdbAge=dbg.entry.Age
                )
        return result

    def process(self, data):
        result = {}
        pe = PE(data=data, fast_load=True)

        for switch, resolver, name in [
            (self.args.debug,   self.parse_debug,    'Debug'),    # noqa
            (self.args.dotnet,  self.parse_dotnet,   'DotNet'),   # noqa
            (self.args.header,  self.parse_header,   'Header'),   # noqa
            (self.args.version, self.parse_version,  'Version'),  # noqa
        ]:
            if not switch:
                continue
            try:
                info = resolver(pe, data)
            except Exception as E:
                self.log_info(F'failed to obtain {name}: {E!s}')
                continue
            if info:
                result[name] = info

        signature = {}

        if self.args.timestamps or self.args.signatures:
            with suppress(Exception):
                signature = self.parse_signature(data)

        if self.args.timestamps:
            ts = self.parse_time_stamps(pe, self.args.timeraw)
            with suppress(KeyError):
                ts.update(Signed=signature['Timestamp'])
            result.update(TimeStamp=ts)

        if signature and self.args.signatures:
            result['Signature'] = signature

        if self.args.tabular:
            table = list(flattened(result, 'PE'))
            width = max(len(key) for key, _ in table)
            for key, value in table:
                yield F'{key:<{width}} : {value!s}'.encode(self.codec)
        else:
            yield json.dumps(result, indent=4, ensure_ascii=False).encode(self.codec)

    _LCID = {
        0x0436: 'Afrikaans-South Africa',
        0x041c: 'Albanian-Albania',
        0x045e: 'Amharic-Ethiopia',
        0x0401: 'Arabic (Saudi Arabia)',
        0x1401: 'Arabic (Algeria)',
        0x3c01: 'Arabic (Bahrain)',
        0x0c01: 'Arabic (Egypt)',
        0x0801: 'Arabic (Iraq)',
        0x2c01: 'Arabic (Jordan)',
        0x3401: 'Arabic (Kuwait)',
        0x3001: 'Arabic (Lebanon)',
        0x1001: 'Arabic (Libya)',
        0x1801: 'Arabic (Morocco)',
        0x2001: 'Arabic (Oman)',
        0x4001: 'Arabic (Qatar)',
        0x2801: 'Arabic (Syria)',
        0x1c01: 'Arabic (Tunisia)',
        0x3801: 'Arabic (U.A.E.)',
        0x2401: 'Arabic (Yemen)',
        0x042b: 'Armenian-Armenia',
        0x044d: 'Assamese',
        0x082c: 'Azeri (Cyrillic)',
        0x042c: 'Azeri (Latin)',
        0x042d: 'Basque',
        0x0423: 'Belarusian',
        0x0445: 'Bengali (India)',
        0x0845: 'Bengali (Bangladesh)',
        0x141A: 'Bosnian (Bosnia/Herzegovina)',
        0x0402: 'Bulgarian',
        0x0455: 'Burmese',
        0x0403: 'Catalan',
        0x045c: 'Cherokee-United States',
        0x0804: 'Chinese (People\'s Republic of China)',
        0x1004: 'Chinese (Singapore)',
        0x0404: 'Chinese (Taiwan)',
        0x0c04: 'Chinese (Hong Kong SAR)',
        0x1404: 'Chinese (Macao SAR)',
        0x041a: 'Croatian',
        0x101a: 'Croatian (Bosnia/Herzegovina)',
        0x0405: 'Czech',
        0x0406: 'Danish',
        0x0465: 'Divehi',
        0x0413: 'Dutch-Netherlands',
        0x0813: 'Dutch-Belgium',
        0x0466: 'Edo',
        0x0409: 'English (United States)',
        0x0809: 'English (United Kingdom)',
        0x0c09: 'English (Australia)',
        0x2809: 'English (Belize)',
        0x1009: 'English (Canada)',
        0x2409: 'English (Caribbean)',
        0x3c09: 'English (Hong Kong SAR)',
        0x4009: 'English (India)',
        0x3809: 'English (Indonesia)',
        0x1809: 'English (Ireland)',
        0x2009: 'English (Jamaica)',
        0x4409: 'English (Malaysia)',
        0x1409: 'English (New Zealand)',
        0x3409: 'English (Philippines)',
        0x4809: 'English (Singapore)',
        0x1c09: 'English (South Africa)',
        0x2c09: 'English (Trinidad)',
        0x3009: 'English (Zimbabwe)',
        0x0425: 'Estonian',
        0x0438: 'Faroese',
        0x0429: 'Farsi',
        0x0464: 'Filipino',
        0x040b: 'Finnish',
        0x040c: 'French (France)',
        0x080c: 'French (Belgium)',
        0x2c0c: 'French (Cameroon)',
        0x0c0c: 'French (Canada)',
        0x240c: 'French (Democratic Rep. of Congo)',
        0x300c: 'French (Cote d\'Ivoire)',
        0x3c0c: 'French (Haiti)',
        0x140c: 'French (Luxembourg)',
        0x340c: 'French (Mali)',
        0x180c: 'French (Monaco)',
        0x380c: 'French (Morocco)',
        0xe40c: 'French (North Africa)',
        0x200c: 'French (Reunion)',
        0x280c: 'French (Senegal)',
        0x100c: 'French (Switzerland)',
        0x1c0c: 'French (West Indies)',
        0x0462: 'Frisian-Netherlands',
        0x0467: 'Fulfulde-Nigeria',
        0x042f: 'FYRO Macedonian',
        0x083c: 'Gaelic (Ireland)',
        0x043c: 'Gaelic (Scotland)',
        0x0456: 'Galician',
        0x0437: 'Georgian',
        0x0407: 'German (Germany)',
        0x0c07: 'German (Austria)',
        0x1407: 'German (Liechtenstein)',
        0x1007: 'German (Luxembourg)',
        0x0807: 'German (Switzerland)',
        0x0408: 'Greek',
        0x0474: 'Guarani-Paraguay',
        0x0447: 'Gujarati',
        0x0468: 'Hausa-Nigeria',
        0x0475: 'Hawaiian (United States)',
        0x040d: 'Hebrew',
        0x0439: 'Hindi',
        0x040e: 'Hungarian',
        0x0469: 'Ibibio-Nigeria',
        0x040f: 'Icelandic',
        0x0470: 'Igbo-Nigeria',
        0x0421: 'Indonesian',
        0x045d: 'Inuktitut',
        0x0410: 'Italian (Italy)',
        0x0810: 'Italian (Switzerland)',
        0x0411: 'Japanese',
        0x044b: 'Kannada',
        0x0471: 'Kanuri-Nigeria',
        0x0860: 'Kashmiri',
        0x0460: 'Kashmiri (Arabic)',
        0x043f: 'Kazakh',
        0x0453: 'Khmer',
        0x0457: 'Konkani',
        0x0412: 'Korean',
        0x0440: 'Kyrgyz (Cyrillic)',
        0x0454: 'Lao',
        0x0476: 'Latin',
        0x0426: 'Latvian',
        0x0427: 'Lithuanian',
        0x043e: 'Malay-Malaysia',
        0x083e: 'Malay-Brunei Darussalam',
        0x044c: 'Malayalam',
        0x043a: 'Maltese',
        0x0458: 'Manipuri',
        0x0481: 'Maori-New Zealand',
        0x044e: 'Marathi',
        0x0450: 'Mongolian (Cyrillic)',
        0x0850: 'Mongolian (Mongolian)',
        0x0461: 'Nepali',
        0x0861: 'Nepali-India',
        0x0414: 'Norwegian (Bokmål)',
        0x0814: 'Norwegian (Nynorsk)',
        0x0448: 'Oriya',
        0x0472: 'Oromo',
        0x0479: 'Papiamentu',
        0x0463: 'Pashto',
        0x0415: 'Polish',
        0x0416: 'Portuguese-Brazil',
        0x0816: 'Portuguese-Portugal',
        0x0446: 'Punjabi',
        0x0846: 'Punjabi (Pakistan)',
        0x046B: 'Quecha (Bolivia)',
        0x086B: 'Quecha (Ecuador)',
        0x0C6B: 'Quecha (Peru)',
        0x0417: 'Rhaeto-Romanic',
        0x0418: 'Romanian',
        0x0818: 'Romanian (Moldava)',
        0x0419: 'Russian',
        0x0819: 'Russian (Moldava)',
        0x043b: 'Sami (Lappish)',
        0x044f: 'Sanskrit',
        0x046c: 'Sepedi',
        0x0c1a: 'Serbian (Cyrillic)',
        0x081a: 'Serbian (Latin)',
        0x0459: 'Sindhi (India)',
        0x0859: 'Sindhi (Pakistan)',
        0x045b: 'Sinhalese-Sri Lanka',
        0x041b: 'Slovak',
        0x0424: 'Slovenian',
        0x0477: 'Somali',
        0x042e: 'Sorbian',
        0x0c0a: 'Spanish (Modern Sort)',
        0x040a: 'Spanish (Traditional Sort)',
        0x2c0a: 'Spanish (Argentina)',
        0x400a: 'Spanish (Bolivia)',
        0x340a: 'Spanish (Chile)',
        0x240a: 'Spanish (Colombia)',
        0x140a: 'Spanish (Costa Rica)',
        0x1c0a: 'Spanish (Dominican Republic)',
        0x300a: 'Spanish (Ecuador)',
        0x440a: 'Spanish (El Salvador)',
        0x100a: 'Spanish (Guatemala)',
        0x480a: 'Spanish (Honduras)',
        0x580a: 'Spanish (Latin America)',
        0x080a: 'Spanish (Mexico)',
        0x4c0a: 'Spanish (Nicaragua)',
        0x180a: 'Spanish (Panama)',
        0x3c0a: 'Spanish (Paraguay)',
        0x280a: 'Spanish (Peru)',
        0x500a: 'Spanish (Puerto Rico)',
        0x540a: 'Spanish (United States)',
        0x380a: 'Spanish (Uruguay)',
        0x200a: 'Spanish (Venezuela)',
        0x0430: 'Sutu',
        0x0441: 'Swahili',
        0x041d: 'Swedish',
        0x081d: 'Swedish-Finland',
        0x045a: 'Syriac',
        0x0428: 'Tajik',
        0x045f: 'Tamazight (Arabic)',
        0x085f: 'Tamazight (Latin)',
        0x0449: 'Tamil',
        0x0444: 'Tatar',
        0x044a: 'Telugu',
        0x041e: 'Thai',
        0x0851: 'Tibetan (Bhutan)',
        0x0451: 'Tibetan (People\'s Republic of China)',
        0x0873: 'Tigrigna (Eritrea)',
        0x0473: 'Tigrigna (Ethiopia)',
        0x0431: 'Tsonga',
        0x0432: 'Tswana',
        0x041f: 'Turkish',
        0x0442: 'Turkmen',
        0x0480: 'Uighur-China',
        0x0422: 'Ukrainian',
        0x0420: 'Urdu',
        0x0820: 'Urdu-India',
        0x0843: 'Uzbek (Cyrillic)',
        0x0443: 'Uzbek (Latin)',
        0x0433: 'Venda',
        0x042a: 'Vietnamese',
        0x0452: 'Welsh',
        0x0434: 'Xhosa',
        0x0478: 'Yi',
        0x043d: 'Yiddish',
        0x046a: 'Yoruba',
        0x0435: 'Zulu',
        0x04ff: 'HID (Human Interface Device)'
    }

    _CHARSET = {
        0x0000: '7-bit ASCII',
        0x03A4: 'Japan (Shift ? JIS X-0208)',
        0x03B5: 'Korea (Shift ? KSC 5601)',
        0x03B6: 'Taiwan (Big5)',
        0x04B0: 'Unicode',
        0x04E2: 'Latin-2 (Eastern European)',
        0x04E3: 'Cyrillic',
        0x04E4: 'Multilingual',
        0x04E5: 'Greek',
        0x04E6: 'Turkish',
        0x04E7: 'Hebrew',
        0x04E8: 'Arabic',
    }

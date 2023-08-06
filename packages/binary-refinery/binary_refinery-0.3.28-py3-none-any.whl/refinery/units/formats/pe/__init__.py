#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A package containing Portable Executable (PE) file related units.
"""
from pefile import PE, DIRECTORY_ENTRY
from typing import Union, ByteString
from .. import arg, Unit

IMAGE_DIRECTORY_ENTRY_SECURITY = DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_SECURITY']


def get_pe_size(pe: Union[PE, ByteString], overlay=True, sections=True, directories=True, certificate=True, memdump=False) -> int:
    """
    This fuction determines the size of a PE file, optionally taking into account the
    pefile module overlay computation, section information, data directory information,
    and certificate entries.
    """
    if not isinstance(pe, PE):
        pe = PE(data=pe, fast_load=True)

    overlay_value = overlay and pe.get_overlay_data_start_offset() or 0

    sections_value = sections and max(
        s.PointerToRawData + s.SizeOfRawData
        for s in pe.sections
    ) or 0

    memdump_value = memdump and max(
        s.VirtualAddress + s.Misc_VirtualSize
        for s in pe.sections
    ) or 0

    directories_value = directories and max(
        pe.get_offset_from_rva(d.VirtualAddress) + d.Size
        for d in pe.OPTIONAL_HEADER.DATA_DIRECTORY
    ) or 0

    if certificate:
        # The certificate overlay is given as a file offset
        # rather than a virtual address.
        cert_entry = pe.OPTIONAL_HEADER.DATA_DIRECTORY[IMAGE_DIRECTORY_ENTRY_SECURITY]
        cert_value = cert_entry.VirtualAddress + cert_entry.Size
    else:
        cert_value = 0

    return max(
        overlay_value,
        sections_value,
        directories_value,
        cert_value,
        memdump_value
    )


class OverlayUnit(Unit, abstract=True):
    def __init__(self, conservative: arg.switch('-c', help='Consider only section size to determine overlay.') = False):
        super().__init__(conservative=conservative)

    def _get_size(self, data):
        return get_pe_size(
            data,
            directories=not self.args.conservative,
            certificate=not self.args.conservative,
        )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .. import arg, Unit
from ...lib.meta import LazyMetaOracleFactory


class cm(Unit):
    """
    The Common Meta variables unit populates the set of meta variables of the current chunk with commonly
    used metadata. The unit has no effect outside a frame. If no option is given, the unit populates all
    available variables.
    """
    def __init__(
        self,
        invert  : arg.switch('-x', help='populate only options that have not been specified') = False,
        size    : arg.switch('-S', help='size of the chunk') = False,
        index   : arg.switch('-I', help='index of the chunk in the current frame') = False,
        ext     : arg.switch('-F', help='guess file extension') = False,
        entropy : arg.switch('-E', help='compute data entropy') = False,
        sha1    : arg.switch('-1', help='compute hash: SHA-1') = False,
        sha256  : arg.switch('-2', help='compute hash: SHA-256') = False,
        crc32   : arg.switch('-3', help='compute hash: CRC32') = False,
        md5     : arg.switch('-5', help='compute hash: MD5') = False,
        hashes  : arg.switch('-H', help='compute all common hashes') = False,

    ):
        args = {
            'size'    : size,
            'index'   : index,
            'ext'     : ext,
            'entropy' : entropy,
            'crc32'   : crc32 or hashes,
            'sha1'    : sha1 or hashes,
            'sha256'  : sha256 or hashes,
            'md5'     : md5 or hashes,
        }
        if not any(args.values()):
            if invert:
                raise ValueError('the --invert option can only be specified with another option.')
            for key in args:
                args[key] = True
        elif invert:
            for key in args:
                args[key] = not args[key]
        super().__init__(**args)

    def process(self, data):
        return data

    def filter(self, chunks):
        for index, chunk in enumerate(chunks):
            if not chunk.visible:
                continue
            oracle = LazyMetaOracleFactory(chunk)(index=index)
            for option in (
                'size',
                'index',
                'ext',
                'entropy',
                'crc32',
                'sha1',
                'sha256',
                'md5',
            ):
                if self.args[option]:
                    chunk[option] = oracle[option]
            yield chunk

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contains all units that can work on blocks a fixed length. Note that block cipher
algorithms can be found in `refinery.units.crypto.cipher`.
"""
import abc

from .. import arg, Unit
from ...lib.argformats import numseq
from ...lib import chunks
from ...lib.tools import infinitize


class NoNumpy(Exception):
    pass


class BlockTransformationBase(Unit, abstract=True):

    def __init__(
        self,
        bigendian: arg.switch('-E', help='Read chunks in big endian.') = False,
        blocksize: arg.number('-B', help='The size of each block in bytes, default is 1.') = 1,
        **keywords
    ):
        if blocksize < 1:
            raise ValueError('Block size can not be less than 1.')
        super().__init__(bigendian=bigendian, blocksize=blocksize, **keywords)

    @property
    def bytestream(self):
        """
        Indicates whether or not the block size is equal to 1, i.e. whether the unit is operating
        on a stream of bytes. In this case, many operations can be simplified.
        """
        return self.args.blocksize == 1

    @property
    def fbits(self):
        return 8 * self.args.blocksize

    @property
    def fmask(self):
        return (1 << self.fbits) - 1

    def rest(self, data):
        if self.bytestream:
            return B''
        end = self.args.blocksize * (len(data) // self.args.blocksize)
        return data[end:]

    def chunk(self, data, raw=False):
        if not raw:
            return chunks.unpack(data, self.args.blocksize, self.args.bigendian)

        def chunkraw(data):
            stop = len(data)
            stop = stop - stop % self.args.blocksize
            for k in range(0, stop, self.args.blocksize):
                yield data[k : k + self.args.blocksize]

        return chunkraw(data)

    def unchunk(self, data, raw=False):
        if not raw:
            return chunks.pack(data, self.args.blocksize, self.args.bigendian)

        def bytefilter(it):
            for item in it:
                if isinstance(item, (bytes, bytearray)):
                    yield item
                else:
                    yield bytes(item)

        return B''.join(bytefilter(data))


class BlockTransformation(BlockTransformationBase, abstract=True):

    def process(self, data):
        return self.unchunk(
            self.process_block(b) for b in self.chunk(data)
        ) + self.rest(data)

    @abc.abstractmethod
    def process_block(self, block):
        """
        A blockwise operation implements this routine to process each block, which
        is given as an integer. The return value is also expected to be an integer.
        """
        raise NotImplementedError


class ArithmeticUnit(BlockTransformation, abstract=True):

    def __init__(self, *argument: arg(type=numseq, help=(
        'A single numeric expression which provides the right argument to the operation, '
        'where the left argument is each block in the input data. This argument can also '
        'contain a sequence of bytes which is then split into blocks of the same size as '
        'the input data and used cyclically.')),
        bigendian=False, blocksize=1, **kw
    ):
        super().__init__(bigendian=bigendian, blocksize=blocksize, argument=argument, **kw)

    def _normalize_argument(self, it):
        for block in infinitize(it):
            yield block & self.fmask

    @abc.abstractmethod
    def operate(self, block, *args) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def inplace(self, block, *args) -> None:
        tmp = self.operate(block, *args)
        if tmp.dtype != block.dtype:
            tmp = tmp.astype(block.dtype)
        block[:] = tmp

    def process_ecb_fast(self, data):
        """
        Attempts to perform the operation more quickly by using numpy arrays.
        """
        try:
            import numpy
        except ModuleNotFoundError:
            raise NoNumpy

        order = '<>'[self.args.bigendian]
        dtype = numpy.dtype(F'{order}u{self.args.blocksize}')
        blocks = len(data) // self.args.blocksize

        def nparg(buffer):
            if hasattr(buffer, '__len__') and len(buffer) == 1:
                buffer = buffer[0]
            if isinstance(buffer, int):
                self.log_info('detected numeric argument')
                return buffer & self.fmask
            return numpy.fromiter(self._normalize_argument(buffer), dtype, blocks)

        rest = data[blocks * self.args.blocksize:]
        data = numpy.frombuffer(memoryview(data), dtype, blocks)
        args = [nparg(a) for a in self.args.argument]
        self.inplace(data, *args)
        return data.tobytes() + rest

    def process(self, data):
        try:
            result = self.process_ecb_fast(data)
        except NoNumpy:
            pass
        except Exception as error:
            self.log_warn(F'falling back to default method after numpy failed with error: {error}')
        else:
            self.log_debug('successfully used numpy to process data in ecb mode')
            return result
        self._arg = [self._normalize_argument(a) for a in self.args.argument]
        return super().process(data)

    def process_block(self, block):
        return self.operate(block, *(next(a) for a in self._arg)) & self.fmask


class UnaryOperation(ArithmeticUnit, abstract=True):
    def __init__(self, bigendian=False, blocksize=1):
        super().__init__(
            bigendian=bigendian, blocksize=blocksize)

    def inplace(self, block) -> None:
        super().inplace(block)


class BinaryOperation(ArithmeticUnit, abstract=True):
    def __init__(self, argument: arg(nargs=arg.delete), bigendian=False, blocksize=1):
        super().__init__(argument,
            bigendian=bigendian, blocksize=blocksize)

    def inplace(self, block, argument) -> None:
        super().inplace(block, argument)

import typing

import System
import System.Buffers.Binary


class BinaryPrimitives(System.Object):
    """Reads bytes as primitives with specific endianness"""

    @staticmethod
    @typing.overload
    def ReverseEndianness(value: int) -> int:
        """
        This is a no-op and added only for consistency.
        This allows the caller to read a struct of numeric primitives and reverse each field
        rather than having to skip sbyte fields.
        """
        ...

    @staticmethod
    @typing.overload
    def ReverseEndianness(value: int) -> int:
        """Reverses a primitive value - performs an endianness swap"""
        ...

    @staticmethod
    @typing.overload
    def ReverseEndianness(value: int) -> int:
        """Reverses a primitive value - performs an endianness swap"""
        ...

    @staticmethod
    @typing.overload
    def ReverseEndianness(value: int) -> int:
        """Reverses a primitive value - performs an endianness swap"""
        ...

    @staticmethod
    @typing.overload
    def ReverseEndianness(value: int) -> int:
        """
        This is a no-op and added only for consistency.
        This allows the caller to read a struct of numeric primitives and reverse each field
        rather than having to skip byte fields.
        """
        ...

    @staticmethod
    @typing.overload
    def ReverseEndianness(value: int) -> int:
        """Reverses a primitive value - performs an endianness swap"""
        ...

    @staticmethod
    @typing.overload
    def ReverseEndianness(value: int) -> int:
        """Reverses a primitive value - performs an endianness swap"""
        ...

    @staticmethod
    @typing.overload
    def ReverseEndianness(value: int) -> int:
        """Reverses a primitive value - performs an endianness swap"""
        ...

    @staticmethod
    def ReadDoubleLittleEndian(source: System.ReadOnlySpan[int]) -> float:
        """
        Reads a double from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadHalfLittleEndian(source: System.ReadOnlySpan[int]) -> System.Half:
        """
        Reads a Half from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadInt16LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads an Int16 out of a read-only span of bytes as little endian."""
        ...

    @staticmethod
    def ReadInt32LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads an Int32 out of a read-only span of bytes as little endian."""
        ...

    @staticmethod
    def ReadInt64LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads an Int64 out of a read-only span of bytes as little endian."""
        ...

    @staticmethod
    def ReadSingleLittleEndian(source: System.ReadOnlySpan[int]) -> float:
        """
        Reads a float from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadUInt16LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads a UInt16 out of a read-only span of bytes as little endian."""
        ...

    @staticmethod
    def ReadUInt32LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads a UInt32 out of a read-only span of bytes as little endian."""
        ...

    @staticmethod
    def ReadUInt64LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads a UInt64 out of a read-only span of bytes as little endian."""
        ...

    @staticmethod
    def TryReadDoubleLittleEndian(source: System.ReadOnlySpan[int], value: float) -> bool:
        """
        Reads a double from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a double; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadHalfLittleEndian(source: System.ReadOnlySpan[int], value: System.Half) -> bool:
        """
        Reads a Half from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a Half; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadInt16LittleEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads an Int16 out of a read-only span of bytes as little endian.
        
        :returns: If the span is too small to contain an Int16, return false.
        """
        ...

    @staticmethod
    def TryReadInt32LittleEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads an Int32 out of a read-only span of bytes as little endian.
        
        :returns: If the span is too small to contain an Int32, return false.
        """
        ...

    @staticmethod
    def TryReadInt64LittleEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads an Int64 out of a read-only span of bytes as little endian.
        
        :returns: If the span is too small to contain an Int64, return false.
        """
        ...

    @staticmethod
    def TryReadSingleLittleEndian(source: System.ReadOnlySpan[int], value: float) -> bool:
        """
        Reads a float from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a float; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadUInt16LittleEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads a UInt16 out of a read-only span of bytes as little endian.
        
        :returns: If the span is too small to contain a UInt16, return false.
        """
        ...

    @staticmethod
    def TryReadUInt32LittleEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads a UInt32 out of a read-only span of bytes as little endian.
        
        :returns: If the span is too small to contain a UInt32, return false.
        """
        ...

    @staticmethod
    def TryReadUInt64LittleEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads a UInt64 out of a read-only span of bytes as little endian.
        
        :returns: If the span is too small to contain a UInt64, return false.
        """
        ...

    @staticmethod
    def WriteDoubleLittleEndian(destination: System.Span[int], value: float) -> None:
        """
        Writes a double into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteHalfLittleEndian(destination: System.Span[int], value: System.Half) -> None:
        """
        Writes a Half into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteInt16LittleEndian(destination: System.Span[int], value: int) -> None:
        """Writes an Int16 into a span of bytes as little endian."""
        ...

    @staticmethod
    def WriteInt32LittleEndian(destination: System.Span[int], value: int) -> None:
        """Writes an Int32 into a span of bytes as little endian."""
        ...

    @staticmethod
    def WriteInt64LittleEndian(destination: System.Span[int], value: int) -> None:
        """Writes an Int64 into a span of bytes as little endian."""
        ...

    @staticmethod
    def WriteSingleLittleEndian(destination: System.Span[int], value: float) -> None:
        """
        Writes a float into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUInt16LittleEndian(destination: System.Span[int], value: int) -> None:
        """Write a UInt16 into a span of bytes as little endian."""
        ...

    @staticmethod
    def WriteUInt32LittleEndian(destination: System.Span[int], value: int) -> None:
        """Write a UInt32 into a span of bytes as little endian."""
        ...

    @staticmethod
    def WriteUInt64LittleEndian(destination: System.Span[int], value: int) -> None:
        """Write a UInt64 into a span of bytes as little endian."""
        ...

    @staticmethod
    def TryWriteDoubleLittleEndian(destination: System.Span[int], value: float) -> bool:
        """
        Writes a double into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a double; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteHalfLittleEndian(destination: System.Span[int], value: System.Half) -> bool:
        """
        Writes a Half into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a Half; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteInt16LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes an Int16 into a span of bytes as little endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...

    @staticmethod
    def TryWriteInt32LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes an Int32 into a span of bytes as little endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...

    @staticmethod
    def TryWriteInt64LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes an Int64 into a span of bytes as little endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...

    @staticmethod
    def TryWriteSingleLittleEndian(destination: System.Span[int], value: float) -> bool:
        """
        Writes a float into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a float; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUInt16LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a UInt16 into a span of bytes as little endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...

    @staticmethod
    def TryWriteUInt32LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a UInt32 into a span of bytes as little endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...

    @staticmethod
    def TryWriteUInt64LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a UInt64 into a span of bytes as little endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...

    @staticmethod
    def ReadDoubleBigEndian(source: System.ReadOnlySpan[int]) -> float:
        """
        Reads a double from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadHalfBigEndian(source: System.ReadOnlySpan[int]) -> System.Half:
        """
        Reads a Half from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadInt16BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads an Int16 out of a read-only span of bytes as big endian."""
        ...

    @staticmethod
    def ReadInt32BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads an Int32 out of a read-only span of bytes as big endian."""
        ...

    @staticmethod
    def ReadInt64BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads an Int64 out of a read-only span of bytes as big endian."""
        ...

    @staticmethod
    def ReadSingleBigEndian(source: System.ReadOnlySpan[int]) -> float:
        """
        Reads a float from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadUInt16BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads a UInt16 out of a read-only span of bytes as big endian."""
        ...

    @staticmethod
    def ReadUInt32BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads a UInt32 out of a read-only span of bytes as big endian."""
        ...

    @staticmethod
    def ReadUInt64BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """Reads a UInt64 out of a read-only span of bytes as big endian."""
        ...

    @staticmethod
    def TryReadDoubleBigEndian(source: System.ReadOnlySpan[int], value: float) -> bool:
        """
        Reads a double from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a double; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadHalfBigEndian(source: System.ReadOnlySpan[int], value: System.Half) -> bool:
        """
        Reads a Half from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a Half; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadInt16BigEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads an Int16 out of a read-only span of bytes as big endian.
        
        :returns: If the span is too small to contain an Int16, return false.
        """
        ...

    @staticmethod
    def TryReadInt32BigEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads an Int32 out of a read-only span of bytes as big endian.
        
        :returns: If the span is too small to contain an Int32, return false.
        """
        ...

    @staticmethod
    def TryReadInt64BigEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads an Int64 out of a read-only span of bytes as big endian.
        
        :returns: If the span is too small to contain an Int64, return false.
        """
        ...

    @staticmethod
    def TryReadSingleBigEndian(source: System.ReadOnlySpan[int], value: float) -> bool:
        """
        Reads a float from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a float; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadUInt16BigEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads a UInt16 out of a read-only span of bytes as big endian.
        
        :returns: If the span is too small to contain a UInt16, return false.
        """
        ...

    @staticmethod
    def TryReadUInt32BigEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads a UInt32 out of a read-only span of bytes as big endian.
        
        :returns: If the span is too small to contain a UInt32, return false.
        """
        ...

    @staticmethod
    def TryReadUInt64BigEndian(source: System.ReadOnlySpan[int], value: int) -> bool:
        """
        Reads a UInt64 out of a read-only span of bytes as big endian.
        
        :returns: If the span is too small to contain a UInt64, return false.
        """
        ...

    @staticmethod
    def WriteDoubleBigEndian(destination: System.Span[int], value: float) -> None:
        """
        Writes a double into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteHalfBigEndian(destination: System.Span[int], value: System.Half) -> None:
        """
        Writes a Half into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteInt16BigEndian(destination: System.Span[int], value: int) -> None:
        """Writes an Int16 into a span of bytes as big endian."""
        ...

    @staticmethod
    def WriteInt32BigEndian(destination: System.Span[int], value: int) -> None:
        """Writes an Int32 into a span of bytes as big endian."""
        ...

    @staticmethod
    def WriteInt64BigEndian(destination: System.Span[int], value: int) -> None:
        """Writes an Int64 into a span of bytes as big endian."""
        ...

    @staticmethod
    def WriteSingleBigEndian(destination: System.Span[int], value: float) -> None:
        """
        Writes a float into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUInt16BigEndian(destination: System.Span[int], value: int) -> None:
        """Write a UInt16 into a span of bytes as big endian."""
        ...

    @staticmethod
    def WriteUInt32BigEndian(destination: System.Span[int], value: int) -> None:
        """Write a UInt32 into a span of bytes as big endian."""
        ...

    @staticmethod
    def WriteUInt64BigEndian(destination: System.Span[int], value: int) -> None:
        """Write a UInt64 into a span of bytes as big endian."""
        ...

    @staticmethod
    def TryWriteDoubleBigEndian(destination: System.Span[int], value: float) -> bool:
        """
        Writes a double into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a double; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteHalfBigEndian(destination: System.Span[int], value: System.Half) -> bool:
        """
        Writes a Half into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a Half; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteInt16BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes an Int16 into a span of bytes as big endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...

    @staticmethod
    def TryWriteInt32BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes an Int32 into a span of bytes as big endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...

    @staticmethod
    def TryWriteInt64BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes an Int64 into a span of bytes as big endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...

    @staticmethod
    def TryWriteSingleBigEndian(destination: System.Span[int], value: float) -> bool:
        """
        Writes a float into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a float; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUInt16BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a UInt16 into a span of bytes as big endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...

    @staticmethod
    def TryWriteUInt32BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a UInt32 into a span of bytes as big endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...

    @staticmethod
    def TryWriteUInt64BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a UInt64 into a span of bytes as big endian.
        
        :returns: If the span is too small to contain the value, return false.
        """
        ...



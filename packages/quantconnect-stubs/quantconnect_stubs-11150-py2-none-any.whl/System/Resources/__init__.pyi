import abc
import typing

import System
import System.Collections
import System.Collections.Generic
import System.Globalization
import System.IO
import System.Reflection
import System.Resources
import System.Runtime.Serialization


class UltimateResourceFallbackLocation(System.Enum):
    """This class has no documentation."""

    MainAssembly = 0

    Satellite = 1


class IResourceReader(System.Collections.IEnumerable, System.IDisposable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Close(self) -> None:
        ...

    def GetEnumerator(self) -> System.Collections.IDictionaryEnumerator:
        ...


class ResourceSet(System.Object, System.IDisposable, System.Collections.IEnumerable):
    """This class has no documentation."""

    @property
    def Reader(self) -> System.Resources.IResourceReader:
        """This field is protected."""
        ...

    @Reader.setter
    def Reader(self, value: System.Resources.IResourceReader):
        """This field is protected."""
        ...

    @typing.overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, fileName: str) -> None:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream) -> None:
        ...

    @typing.overload
    def __init__(self, reader: System.Resources.IResourceReader) -> None:
        ...

    def Close(self) -> None:
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def Dispose(self) -> None:
        ...

    def GetDefaultReader(self) -> typing.Type:
        ...

    def GetDefaultWriter(self) -> typing.Type:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IDictionaryEnumerator:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    @typing.overload
    def GetString(self, name: str) -> str:
        ...

    @typing.overload
    def GetString(self, name: str, ignoreCase: bool) -> str:
        ...

    @typing.overload
    def GetObject(self, name: str) -> System.Object:
        ...

    @typing.overload
    def GetObject(self, name: str, ignoreCase: bool) -> System.Object:
        ...

    def ReadResources(self) -> None:
        """This method is protected."""
        ...


class ResourceManager(System.Object):
    """This class has no documentation."""

    @property
    def BaseNameField(self) -> str:
        """This field is protected."""
        ...

    @BaseNameField.setter
    def BaseNameField(self, value: str):
        """This field is protected."""
        ...

    @property
    def MainAssembly(self) -> System.Reflection.Assembly:
        """This field is protected."""
        ...

    @MainAssembly.setter
    def MainAssembly(self, value: System.Reflection.Assembly):
        """This field is protected."""
        ...

    MagicNumber: int = ...

    HeaderVersionNumber: int = 1

    ResReaderTypeName: str = "System.Resources.ResourceReader"

    ResSetTypeName: str = "System.Resources.RuntimeResourceSet"

    ResFileExtension: str = ".resources"

    ResFileExtensionLength: int = 10

    @property
    def BaseName(self) -> str:
        ...

    @property
    def IgnoreCase(self) -> bool:
        ...

    @IgnoreCase.setter
    def IgnoreCase(self, value: bool):
        ...

    @property
    def ResourceSetType(self) -> typing.Type:
        ...

    @property
    def FallbackLocation(self) -> int:
        """
        This property contains the int value of a member of the System.Resources.UltimateResourceFallbackLocation enum.
        
        This property is protected.
        """
        ...

    @FallbackLocation.setter
    def FallbackLocation(self, value: int):
        """
        This property contains the int value of a member of the System.Resources.UltimateResourceFallbackLocation enum.
        
        This property is protected.
        """
        ...

    @typing.overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, baseName: str, assembly: System.Reflection.Assembly) -> None:
        ...

    @typing.overload
    def __init__(self, baseName: str, assembly: System.Reflection.Assembly, usingResourceSet: typing.Type) -> None:
        ...

    @typing.overload
    def __init__(self, resourceSource: typing.Type) -> None:
        ...

    def ReleaseAllResources(self) -> None:
        ...

    @staticmethod
    def CreateFileBasedResourceManager(baseName: str, resourceDir: str, usingResourceSet: typing.Type) -> System.Resources.ResourceManager:
        ...

    def GetResourceFileName(self, culture: System.Globalization.CultureInfo) -> str:
        """This method is protected."""
        ...

    def GetResourceSet(self, culture: System.Globalization.CultureInfo, createIfNotExists: bool, tryParents: bool) -> System.Resources.ResourceSet:
        ...

    def InternalGetResourceSet(self, culture: System.Globalization.CultureInfo, createIfNotExists: bool, tryParents: bool) -> System.Resources.ResourceSet:
        """This method is protected."""
        ...

    @staticmethod
    def GetSatelliteContractVersion(a: System.Reflection.Assembly) -> System.Version:
        """This method is protected."""
        ...

    @staticmethod
    def GetNeutralResourcesLanguage(a: System.Reflection.Assembly) -> System.Globalization.CultureInfo:
        """This method is protected."""
        ...

    @typing.overload
    def GetString(self, name: str) -> str:
        ...

    @typing.overload
    def GetString(self, name: str, culture: System.Globalization.CultureInfo) -> str:
        ...

    @typing.overload
    def GetObject(self, name: str) -> System.Object:
        ...

    @typing.overload
    def GetObject(self, name: str, culture: System.Globalization.CultureInfo) -> System.Object:
        ...

    @typing.overload
    def GetStream(self, name: str) -> System.IO.UnmanagedMemoryStream:
        ...

    @typing.overload
    def GetStream(self, name: str, culture: System.Globalization.CultureInfo) -> System.IO.UnmanagedMemoryStream:
        ...


class MissingSatelliteAssemblyException(System.SystemException):
    """This class has no documentation."""

    @property
    def CultureName(self) -> str:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, cultureName: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class SatelliteContractVersionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Version(self) -> str:
        ...

    def __init__(self, version: str) -> None:
        ...


class ResourceReader(System.Object, System.Resources.IResourceReader):
    """This class has no documentation."""

    @property
    def _resCache(self) -> System.Collections.Generic.Dictionary[str, System.Resources.ResourceLocator]:
        ...

    @_resCache.setter
    def _resCache(self, value: System.Collections.Generic.Dictionary[str, System.Resources.ResourceLocator]):
        ...

    AllowCustomResourceTypes: bool

    @typing.overload
    def __init__(self, fileName: str) -> None:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream) -> None:
        ...

    def Close(self) -> None:
        ...

    def Dispose(self) -> None:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IDictionaryEnumerator:
        ...

    def GetResourceData(self, resourceName: str, resourceType: str, resourceData: typing.List[int]) -> None:
        ...


class NeutralResourcesLanguageAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def CultureName(self) -> str:
        ...

    @property
    def Location(self) -> int:
        """This property contains the int value of a member of the System.Resources.UltimateResourceFallbackLocation enum."""
        ...

    @typing.overload
    def __init__(self, cultureName: str) -> None:
        ...

    @typing.overload
    def __init__(self, cultureName: str, location: System.Resources.UltimateResourceFallbackLocation) -> None:
        ...


class MissingManifestResourceException(System.SystemException):
    """This class has no documentation."""

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...



import typing

import QuantConnect.Interfaces
import QuantConnect.Packets
import QuantConnect.Storage
import System
import System.Collections
import System.Collections.Generic
import System.Text

System_EventHandler = typing.Any

QuantConnect_Storage_ObjectStore_ReadJson_T = typing.TypeVar("QuantConnect_Storage_ObjectStore_ReadJson_T")
QuantConnect_Storage_ObjectStore_ReadXml_T = typing.TypeVar("QuantConnect_Storage_ObjectStore_ReadXml_T")
QuantConnect_Storage_ObjectStore_SaveJson_T = typing.TypeVar("QuantConnect_Storage_ObjectStore_SaveJson_T")
QuantConnect_Storage_ObjectStore_SaveXml_T = typing.TypeVar("QuantConnect_Storage_ObjectStore_SaveXml_T")


class ObjectStore(System.Object, QuantConnect.Interfaces.IObjectStore, typing.Iterable[System.Collections.Generic.KeyValuePair[str, typing.List[int]]]):
    """Helper class for easier access to IObjectStore methods"""

    @property
    def ErrorRaised(self) -> typing.List[System_EventHandler]:
        """Event raised each time there's an error"""
        ...

    @ErrorRaised.setter
    def ErrorRaised(self, value: typing.List[System_EventHandler]):
        """Event raised each time there's an error"""
        ...

    def __init__(self, store: QuantConnect.Interfaces.IObjectStore) -> None:
        """
        Initializes a new instance of the ObjectStore class
        
        :param store: The IObjectStore instance to wrap
        """
        ...

    def Initialize(self, algorithmName: str, userId: int, projectId: int, userToken: str, controls: QuantConnect.Packets.Controls) -> None:
        """
        Initializes the object store
        
        :param algorithmName: The algorithm name
        :param userId: The user id
        :param projectId: The project id
        :param userToken: The user token
        :param controls: The job controls instance
        """
        ...

    def ContainsKey(self, key: str) -> bool:
        """
        Determines whether the store contains data for the specified key
        
        :param key: The object key
        :returns: True if the key was found.
        """
        ...

    def ReadBytes(self, key: str) -> typing.List[int]:
        """
        Returns the object data for the specified key
        
        :param key: The object key
        :returns: A byte array containing the data.
        """
        ...

    def SaveBytes(self, key: str, contents: typing.List[int]) -> bool:
        """
        Saves the object data for the specified key
        
        :param key: The object key
        :param contents: The object data
        :returns: True if the save operation was successful.
        """
        ...

    def Delete(self, key: str) -> bool:
        """
        Deletes the object data for the specified key
        
        :param key: The object key
        :returns: True if the delete operation was successful.
        """
        ...

    def GetFilePath(self, key: str) -> str:
        """
        Returns the file path for the specified key
        
        :param key: The object key
        :returns: The path for the file.
        """
        ...

    def Read(self, key: str, encoding: System.Text.Encoding = None) -> str:
        """
        Returns the string object data for the specified key
        
        :param key: The object key
        :param encoding: The string encoding used
        :returns: A string containing the data.
        """
        ...

    def ReadString(self, key: str, encoding: System.Text.Encoding = None) -> str:
        """
        Returns the string object data for the specified key
        
        :param key: The object key
        :param encoding: The string encoding used
        :returns: A string containing the data.
        """
        ...

    def ReadJson(self, key: str, encoding: System.Text.Encoding = None, settings: typing.Any = None) -> QuantConnect_Storage_ObjectStore_ReadJson_T:
        """
        Returns the JSON deserialized object data for the specified key
        
        :param key: The object key
        :param encoding: The string encoding used
        :param settings: The settings used by the JSON deserializer
        :returns: An object containing the data.
        """
        ...

    def ReadXml(self, key: str, encoding: System.Text.Encoding = None) -> QuantConnect_Storage_ObjectStore_ReadXml_T:
        """
        Returns the XML deserialized object data for the specified key
        
        :param key: The object key
        :param encoding: The string encoding used
        :returns: An object containing the data.
        """
        ...

    def Save(self, key: str, text: str, encoding: System.Text.Encoding = None) -> bool:
        """
        Saves the object data in text format for the specified key
        
        :param key: The object key
        :param text: The string object to be saved
        :param encoding: The string encoding used
        :returns: True if the object was saved successfully.
        """
        ...

    def SaveString(self, key: str, text: str, encoding: System.Text.Encoding = None) -> bool:
        """
        Saves the object data in text format for the specified key
        
        :param key: The object key
        :param text: The string object to be saved
        :param encoding: The string encoding used
        :returns: True if the object was saved successfully.
        """
        ...

    def SaveJson(self, key: str, obj: QuantConnect_Storage_ObjectStore_SaveJson_T, encoding: System.Text.Encoding = None, settings: typing.Any = None) -> bool:
        """
        Saves the object data in JSON format for the specified key
        
        :param key: The object key
        :param obj: The object to be saved
        :param encoding: The string encoding used
        :param settings: The settings used by the JSON serializer
        :returns: True if the object was saved successfully.
        """
        ...

    def SaveXml(self, key: str, obj: QuantConnect_Storage_ObjectStore_SaveXml_T, encoding: System.Text.Encoding = None) -> bool:
        """
        Saves the object data in XML format for the specified key
        
        :param key: The object key
        :param obj: The object to be saved
        :param encoding: The string encoding used
        :returns: True if the object was saved successfully.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System.Collections.Generic.KeyValuePair[str, typing.List[int]]]:
        """
        Returns an enumerator that iterates through the collection.
        
        :returns: A System.Collections.Generic.IEnumerator`1 that can be used to iterate through the collection.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """
        Returns an enumerator that iterates through a collection.
        
        :returns: An System.Collections.IEnumerator object that can be used to iterate through the collection.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...



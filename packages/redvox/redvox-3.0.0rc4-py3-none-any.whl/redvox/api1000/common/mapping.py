"""
This module provides functions and wrappers for working protobuf Map fields.
"""

from typing import Dict, Generic, Type, TypeVar

from redvox.api1000.common.typing import check_type


# pylint: disable=C0103
T = TypeVar("T")


class Mapping(Generic[T]):
    """
    This class encapsulates the API M map fields providing high-level methods for manipulating the underlying
    mapping.
    """

    def __init__(self, metadata_proto, t: Type) -> None:
        """
        Instantiates this wrapper.
        :param metadata_proto: The protobuf field backing this metadata.
        """
        self.__t: Type = t
        self._metadata_proto = metadata_proto

    def get_proto(self):
        """
        Returns the protobuf definition associated with this mapping.
        :return: The protobuf definition associated with this mapping.
        """
        return self._metadata_proto

    def get_metadata_count(self) -> int:
        """
        Returns the number of key-pair values stored in this metadata.
        :return: The number of key-pair values stored in this metadata.
        """
        return len(self._metadata_proto)

    def get_metadata(self) -> Dict[str, T]:
        """
        Returns the metadata as a dictionary.
        :return: The metadata as a dictionary.
        """
        metadata_dict: Dict[str, T] = dict()
        for key, value in self._metadata_proto.items():
            metadata_dict[key] = value
        return metadata_dict

    def set_metadata(self, metadata: Dict[str, T]) -> "Mapping":
        """
        Sets the metadata to passed in dictionary.
        :param metadata: Sets the metadata to this.
        :return: This instance of Metadata.
        """
        for key, value in metadata.items():
            check_type(key, [str])
            check_type(value, [self.__t])

        self._metadata_proto.clear()
        for key, value in metadata.items():
            self._metadata_proto[key] = value

        return self

    def append_metadata(self, key: str, value: T) -> "Mapping":
        """
        Appends a key-value pair to the metadata mapping.
        :param key: Key to append.
        :param value: Value to append.
        :return: This instance of Metadata.
        """
        check_type(key, [str])
        check_type(value, [self.__t])

        self._metadata_proto[key] = value
        return self

    def clear_metadata(self) -> "Mapping":
        """
        Clears all metadata.
        :return: This instance of metadata
        """
        self._metadata_proto.clear()
        return self

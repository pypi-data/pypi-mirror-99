# coding: utf-8

from enum import Enum
from six import string_types, iteritems
from bitmovin_api_sdk.common.poscheck import poscheck_model
import pprint
import six


class DomainList(object):
    @poscheck_model
    def __init__(self,
                 domains=None):
        # type: (list[Domain]) -> None

        self._domains = list()
        self.discriminator = None

        if domains is not None:
            self.domains = domains

    @property
    def openapi_types(self):
        types = {
            'domains': 'list[Domain]'
        }

        return types

    @property
    def attribute_map(self):
        attributes = {
            'domains': 'domains'
        }
        return attributes

    @property
    def domains(self):
        # type: () -> list[Domain]
        """Gets the domains of this DomainList.


        :return: The domains of this DomainList.
        :rtype: list[Domain]
        """
        return self._domains

    @domains.setter
    def domains(self, domains):
        # type: (list) -> None
        """Sets the domains of this DomainList.


        :param domains: The domains of this DomainList.
        :type: list[Domain]
        """

        if domains is not None:
            if not isinstance(domains, list):
                raise TypeError("Invalid type for `domains`, type has to be `list[Domain]`")

        self._domains = domains

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if value is None:
                continue
            if isinstance(value, list):
                if len(value) == 0:
                    continue
                result[self.attribute_map.get(attr)] = [y.value if isinstance(y, Enum) else y for y in [x.to_dict() if hasattr(x, "to_dict") else x for x in value]]
            elif hasattr(value, "to_dict"):
                result[self.attribute_map.get(attr)] = value.to_dict()
            elif isinstance(value, Enum):
                result[self.attribute_map.get(attr)] = value.value
            elif isinstance(value, dict):
                result[self.attribute_map.get(attr)] = {k: (v.to_dict() if hasattr(v, "to_dict") else v) for (k, v) in value.items()}
            else:
                result[self.attribute_map.get(attr)] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DomainList):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

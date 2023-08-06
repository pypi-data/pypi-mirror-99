# coding: utf-8

from enum import Enum
from six import string_types, iteritems
from bitmovin_api_sdk.common.poscheck import poscheck_model
import pprint
import six


class BillableEncodingFeatureMinutes(object):
    @poscheck_model
    def __init__(self,
                 feature_type=None,
                 encoded_minutes=None,
                 feature_multiplier=None,
                 billable_minutes=None):
        # type: (string_types, float, float, float) -> None

        self._feature_type = None
        self._encoded_minutes = None
        self._feature_multiplier = None
        self._billable_minutes = None
        self.discriminator = None

        if feature_type is not None:
            self.feature_type = feature_type
        if encoded_minutes is not None:
            self.encoded_minutes = encoded_minutes
        if feature_multiplier is not None:
            self.feature_multiplier = feature_multiplier
        if billable_minutes is not None:
            self.billable_minutes = billable_minutes

    @property
    def openapi_types(self):
        types = {
            'feature_type': 'string_types',
            'encoded_minutes': 'float',
            'feature_multiplier': 'float',
            'billable_minutes': 'float'
        }

        return types

    @property
    def attribute_map(self):
        attributes = {
            'feature_type': 'featureType',
            'encoded_minutes': 'encodedMinutes',
            'feature_multiplier': 'featureMultiplier',
            'billable_minutes': 'billableMinutes'
        }
        return attributes

    @property
    def feature_type(self):
        # type: () -> string_types
        """Gets the feature_type of this BillableEncodingFeatureMinutes.

        The name of the feature.

        :return: The feature_type of this BillableEncodingFeatureMinutes.
        :rtype: string_types
        """
        return self._feature_type

    @feature_type.setter
    def feature_type(self, feature_type):
        # type: (string_types) -> None
        """Sets the feature_type of this BillableEncodingFeatureMinutes.

        The name of the feature.

        :param feature_type: The feature_type of this BillableEncodingFeatureMinutes.
        :type: string_types
        """

        if feature_type is not None:
            if not isinstance(feature_type, string_types):
                raise TypeError("Invalid type for `feature_type`, type has to be `string_types`")

        self._feature_type = feature_type

    @property
    def encoded_minutes(self):
        # type: () -> float
        """Gets the encoded_minutes of this BillableEncodingFeatureMinutes.

        Encoded minutes related to this feature.

        :return: The encoded_minutes of this BillableEncodingFeatureMinutes.
        :rtype: float
        """
        return self._encoded_minutes

    @encoded_minutes.setter
    def encoded_minutes(self, encoded_minutes):
        # type: (float) -> None
        """Sets the encoded_minutes of this BillableEncodingFeatureMinutes.

        Encoded minutes related to this feature.

        :param encoded_minutes: The encoded_minutes of this BillableEncodingFeatureMinutes.
        :type: float
        """

        if encoded_minutes is not None:
            if not isinstance(encoded_minutes, (float, int)):
                raise TypeError("Invalid type for `encoded_minutes`, type has to be `float`")

        self._encoded_minutes = encoded_minutes

    @property
    def feature_multiplier(self):
        # type: () -> float
        """Gets the feature_multiplier of this BillableEncodingFeatureMinutes.

        The multiplier used for this feature.

        :return: The feature_multiplier of this BillableEncodingFeatureMinutes.
        :rtype: float
        """
        return self._feature_multiplier

    @feature_multiplier.setter
    def feature_multiplier(self, feature_multiplier):
        # type: (float) -> None
        """Sets the feature_multiplier of this BillableEncodingFeatureMinutes.

        The multiplier used for this feature.

        :param feature_multiplier: The feature_multiplier of this BillableEncodingFeatureMinutes.
        :type: float
        """

        if feature_multiplier is not None:
            if not isinstance(feature_multiplier, (float, int)):
                raise TypeError("Invalid type for `feature_multiplier`, type has to be `float`")

        self._feature_multiplier = feature_multiplier

    @property
    def billable_minutes(self):
        # type: () -> float
        """Gets the billable_minutes of this BillableEncodingFeatureMinutes.

        The billable minutes related to this feature.

        :return: The billable_minutes of this BillableEncodingFeatureMinutes.
        :rtype: float
        """
        return self._billable_minutes

    @billable_minutes.setter
    def billable_minutes(self, billable_minutes):
        # type: (float) -> None
        """Sets the billable_minutes of this BillableEncodingFeatureMinutes.

        The billable minutes related to this feature.

        :param billable_minutes: The billable_minutes of this BillableEncodingFeatureMinutes.
        :type: float
        """

        if billable_minutes is not None:
            if not isinstance(billable_minutes, (float, int)):
                raise TypeError("Invalid type for `billable_minutes`, type has to be `float`")

        self._billable_minutes = billable_minutes

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
        if not isinstance(other, BillableEncodingFeatureMinutes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

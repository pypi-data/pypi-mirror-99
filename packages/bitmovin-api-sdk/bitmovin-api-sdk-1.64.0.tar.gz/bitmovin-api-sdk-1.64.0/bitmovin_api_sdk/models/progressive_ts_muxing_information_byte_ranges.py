# coding: utf-8

from enum import Enum
from six import string_types, iteritems
from bitmovin_api_sdk.common.poscheck import poscheck_model
import pprint
import six


class ProgressiveTsMuxingInformationByteRanges(object):
    @poscheck_model
    def __init__(self,
                 segment_number=None,
                 start_bytes=None,
                 end_bytes=None,
                 duration=None):
        # type: (int, int, int, float) -> None

        self._segment_number = None
        self._start_bytes = None
        self._end_bytes = None
        self._duration = None
        self.discriminator = None

        if segment_number is not None:
            self.segment_number = segment_number
        if start_bytes is not None:
            self.start_bytes = start_bytes
        if end_bytes is not None:
            self.end_bytes = end_bytes
        if duration is not None:
            self.duration = duration

    @property
    def openapi_types(self):
        types = {
            'segment_number': 'int',
            'start_bytes': 'int',
            'end_bytes': 'int',
            'duration': 'float'
        }

        return types

    @property
    def attribute_map(self):
        attributes = {
            'segment_number': 'segmentNumber',
            'start_bytes': 'startBytes',
            'end_bytes': 'endBytes',
            'duration': 'duration'
        }
        return attributes

    @property
    def segment_number(self):
        # type: () -> int
        """Gets the segment_number of this ProgressiveTsMuxingInformationByteRanges.

        Number of the segment (starting at 0) (required)

        :return: The segment_number of this ProgressiveTsMuxingInformationByteRanges.
        :rtype: int
        """
        return self._segment_number

    @segment_number.setter
    def segment_number(self, segment_number):
        # type: (int) -> None
        """Sets the segment_number of this ProgressiveTsMuxingInformationByteRanges.

        Number of the segment (starting at 0) (required)

        :param segment_number: The segment_number of this ProgressiveTsMuxingInformationByteRanges.
        :type: int
        """

        if segment_number is not None:
            if not isinstance(segment_number, int):
                raise TypeError("Invalid type for `segment_number`, type has to be `int`")

        self._segment_number = segment_number

    @property
    def start_bytes(self):
        # type: () -> int
        """Gets the start_bytes of this ProgressiveTsMuxingInformationByteRanges.

        The position of the first byte of the segment

        :return: The start_bytes of this ProgressiveTsMuxingInformationByteRanges.
        :rtype: int
        """
        return self._start_bytes

    @start_bytes.setter
    def start_bytes(self, start_bytes):
        # type: (int) -> None
        """Sets the start_bytes of this ProgressiveTsMuxingInformationByteRanges.

        The position of the first byte of the segment

        :param start_bytes: The start_bytes of this ProgressiveTsMuxingInformationByteRanges.
        :type: int
        """

        if start_bytes is not None:
            if not isinstance(start_bytes, int):
                raise TypeError("Invalid type for `start_bytes`, type has to be `int`")

        self._start_bytes = start_bytes

    @property
    def end_bytes(self):
        # type: () -> int
        """Gets the end_bytes of this ProgressiveTsMuxingInformationByteRanges.

        The position of the last byte of the segment

        :return: The end_bytes of this ProgressiveTsMuxingInformationByteRanges.
        :rtype: int
        """
        return self._end_bytes

    @end_bytes.setter
    def end_bytes(self, end_bytes):
        # type: (int) -> None
        """Sets the end_bytes of this ProgressiveTsMuxingInformationByteRanges.

        The position of the last byte of the segment

        :param end_bytes: The end_bytes of this ProgressiveTsMuxingInformationByteRanges.
        :type: int
        """

        if end_bytes is not None:
            if not isinstance(end_bytes, int):
                raise TypeError("Invalid type for `end_bytes`, type has to be `int`")

        self._end_bytes = end_bytes

    @property
    def duration(self):
        # type: () -> float
        """Gets the duration of this ProgressiveTsMuxingInformationByteRanges.

        The duration of the segment in seconds

        :return: The duration of this ProgressiveTsMuxingInformationByteRanges.
        :rtype: float
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        # type: (float) -> None
        """Sets the duration of this ProgressiveTsMuxingInformationByteRanges.

        The duration of the segment in seconds

        :param duration: The duration of this ProgressiveTsMuxingInformationByteRanges.
        :type: float
        """

        if duration is not None:
            if not isinstance(duration, (float, int)):
                raise TypeError("Invalid type for `duration`, type has to be `float`")

        self._duration = duration

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
        if not isinstance(other, ProgressiveTsMuxingInformationByteRanges):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

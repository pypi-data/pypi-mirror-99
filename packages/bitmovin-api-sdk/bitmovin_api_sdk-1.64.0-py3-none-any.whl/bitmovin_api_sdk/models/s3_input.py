# coding: utf-8

from enum import Enum
from six import string_types, iteritems
from bitmovin_api_sdk.common.poscheck import poscheck_model
from bitmovin_api_sdk.models.aws_cloud_region import AwsCloudRegion
from bitmovin_api_sdk.models.input import Input
import pprint
import six


class S3Input(Input):
    @poscheck_model
    def __init__(self,
                 name=None,
                 description=None,
                 created_at=None,
                 modified_at=None,
                 custom_data=None,
                 id_=None,
                 cloud_region=None,
                 bucket_name=None,
                 access_key=None,
                 secret_key=None):
        # type: (string_types, string_types, datetime, datetime, dict, string_types, AwsCloudRegion, string_types, string_types, string_types) -> None
        super(S3Input, self).__init__(name=name, description=description, created_at=created_at, modified_at=modified_at, custom_data=custom_data, id_=id_)

        self._cloud_region = None
        self._bucket_name = None
        self._access_key = None
        self._secret_key = None
        self.discriminator = None

        if cloud_region is not None:
            self.cloud_region = cloud_region
        if bucket_name is not None:
            self.bucket_name = bucket_name
        if access_key is not None:
            self.access_key = access_key
        if secret_key is not None:
            self.secret_key = secret_key

    @property
    def openapi_types(self):
        types = {}

        if hasattr(super(S3Input, self), 'openapi_types'):
            types = getattr(super(S3Input, self), 'openapi_types')

        types.update({
            'cloud_region': 'AwsCloudRegion',
            'bucket_name': 'string_types',
            'access_key': 'string_types',
            'secret_key': 'string_types'
        })

        return types

    @property
    def attribute_map(self):
        attributes = {}

        if hasattr(super(S3Input, self), 'attribute_map'):
            attributes = getattr(super(S3Input, self), 'attribute_map')

        attributes.update({
            'cloud_region': 'cloudRegion',
            'bucket_name': 'bucketName',
            'access_key': 'accessKey',
            'secret_key': 'secretKey'
        })
        return attributes

    @property
    def cloud_region(self):
        # type: () -> AwsCloudRegion
        """Gets the cloud_region of this S3Input.

        The cloud region in which the bucket is located. Is used to determine the ideal location for your encodings automatically.

        :return: The cloud_region of this S3Input.
        :rtype: AwsCloudRegion
        """
        return self._cloud_region

    @cloud_region.setter
    def cloud_region(self, cloud_region):
        # type: (AwsCloudRegion) -> None
        """Sets the cloud_region of this S3Input.

        The cloud region in which the bucket is located. Is used to determine the ideal location for your encodings automatically.

        :param cloud_region: The cloud_region of this S3Input.
        :type: AwsCloudRegion
        """

        if cloud_region is not None:
            if not isinstance(cloud_region, AwsCloudRegion):
                raise TypeError("Invalid type for `cloud_region`, type has to be `AwsCloudRegion`")

        self._cloud_region = cloud_region

    @property
    def bucket_name(self):
        # type: () -> string_types
        """Gets the bucket_name of this S3Input.

        Name of the bucket (required)

        :return: The bucket_name of this S3Input.
        :rtype: string_types
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        # type: (string_types) -> None
        """Sets the bucket_name of this S3Input.

        Name of the bucket (required)

        :param bucket_name: The bucket_name of this S3Input.
        :type: string_types
        """

        if bucket_name is not None:
            if not isinstance(bucket_name, string_types):
                raise TypeError("Invalid type for `bucket_name`, type has to be `string_types`")

        self._bucket_name = bucket_name

    @property
    def access_key(self):
        # type: () -> string_types
        """Gets the access_key of this S3Input.

        Amazon access key (required)

        :return: The access_key of this S3Input.
        :rtype: string_types
        """
        return self._access_key

    @access_key.setter
    def access_key(self, access_key):
        # type: (string_types) -> None
        """Sets the access_key of this S3Input.

        Amazon access key (required)

        :param access_key: The access_key of this S3Input.
        :type: string_types
        """

        if access_key is not None:
            if not isinstance(access_key, string_types):
                raise TypeError("Invalid type for `access_key`, type has to be `string_types`")

        self._access_key = access_key

    @property
    def secret_key(self):
        # type: () -> string_types
        """Gets the secret_key of this S3Input.

        Amazon secret key (required)

        :return: The secret_key of this S3Input.
        :rtype: string_types
        """
        return self._secret_key

    @secret_key.setter
    def secret_key(self, secret_key):
        # type: (string_types) -> None
        """Sets the secret_key of this S3Input.

        Amazon secret key (required)

        :param secret_key: The secret_key of this S3Input.
        :type: string_types
        """

        if secret_key is not None:
            if not isinstance(secret_key, string_types):
                raise TypeError("Invalid type for `secret_key`, type has to be `string_types`")

        self._secret_key = secret_key

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        if hasattr(super(S3Input, self), "to_dict"):
            result = super(S3Input, self).to_dict()
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
        if not isinstance(other, S3Input):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

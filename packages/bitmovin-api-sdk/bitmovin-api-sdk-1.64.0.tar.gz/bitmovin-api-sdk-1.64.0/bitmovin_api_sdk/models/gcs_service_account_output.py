# coding: utf-8

from enum import Enum
from six import string_types, iteritems
from bitmovin_api_sdk.common.poscheck import poscheck_model
from bitmovin_api_sdk.models.google_cloud_region import GoogleCloudRegion
from bitmovin_api_sdk.models.output import Output
import pprint
import six


class GcsServiceAccountOutput(Output):
    @poscheck_model
    def __init__(self,
                 name=None,
                 description=None,
                 created_at=None,
                 modified_at=None,
                 custom_data=None,
                 id_=None,
                 acl=None,
                 service_account_credentials=None,
                 bucket_name=None,
                 cloud_region=None):
        # type: (string_types, string_types, datetime, datetime, dict, string_types, list[AclEntry], string_types, string_types, GoogleCloudRegion) -> None
        super(GcsServiceAccountOutput, self).__init__(name=name, description=description, created_at=created_at, modified_at=modified_at, custom_data=custom_data, id_=id_, acl=acl)

        self._service_account_credentials = None
        self._bucket_name = None
        self._cloud_region = None
        self.discriminator = None

        if service_account_credentials is not None:
            self.service_account_credentials = service_account_credentials
        if bucket_name is not None:
            self.bucket_name = bucket_name
        if cloud_region is not None:
            self.cloud_region = cloud_region

    @property
    def openapi_types(self):
        types = {}

        if hasattr(super(GcsServiceAccountOutput, self), 'openapi_types'):
            types = getattr(super(GcsServiceAccountOutput, self), 'openapi_types')

        types.update({
            'service_account_credentials': 'string_types',
            'bucket_name': 'string_types',
            'cloud_region': 'GoogleCloudRegion'
        })

        return types

    @property
    def attribute_map(self):
        attributes = {}

        if hasattr(super(GcsServiceAccountOutput, self), 'attribute_map'):
            attributes = getattr(super(GcsServiceAccountOutput, self), 'attribute_map')

        attributes.update({
            'service_account_credentials': 'serviceAccountCredentials',
            'bucket_name': 'bucketName',
            'cloud_region': 'cloudRegion'
        })
        return attributes

    @property
    def service_account_credentials(self):
        # type: () -> string_types
        """Gets the service_account_credentials of this GcsServiceAccountOutput.

        GCS projectId (required)

        :return: The service_account_credentials of this GcsServiceAccountOutput.
        :rtype: string_types
        """
        return self._service_account_credentials

    @service_account_credentials.setter
    def service_account_credentials(self, service_account_credentials):
        # type: (string_types) -> None
        """Sets the service_account_credentials of this GcsServiceAccountOutput.

        GCS projectId (required)

        :param service_account_credentials: The service_account_credentials of this GcsServiceAccountOutput.
        :type: string_types
        """

        if service_account_credentials is not None:
            if not isinstance(service_account_credentials, string_types):
                raise TypeError("Invalid type for `service_account_credentials`, type has to be `string_types`")

        self._service_account_credentials = service_account_credentials

    @property
    def bucket_name(self):
        # type: () -> string_types
        """Gets the bucket_name of this GcsServiceAccountOutput.

        Name of the bucket (required)

        :return: The bucket_name of this GcsServiceAccountOutput.
        :rtype: string_types
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        # type: (string_types) -> None
        """Sets the bucket_name of this GcsServiceAccountOutput.

        Name of the bucket (required)

        :param bucket_name: The bucket_name of this GcsServiceAccountOutput.
        :type: string_types
        """

        if bucket_name is not None:
            if not isinstance(bucket_name, string_types):
                raise TypeError("Invalid type for `bucket_name`, type has to be `string_types`")

        self._bucket_name = bucket_name

    @property
    def cloud_region(self):
        # type: () -> GoogleCloudRegion
        """Gets the cloud_region of this GcsServiceAccountOutput.


        :return: The cloud_region of this GcsServiceAccountOutput.
        :rtype: GoogleCloudRegion
        """
        return self._cloud_region

    @cloud_region.setter
    def cloud_region(self, cloud_region):
        # type: (GoogleCloudRegion) -> None
        """Sets the cloud_region of this GcsServiceAccountOutput.


        :param cloud_region: The cloud_region of this GcsServiceAccountOutput.
        :type: GoogleCloudRegion
        """

        if cloud_region is not None:
            if not isinstance(cloud_region, GoogleCloudRegion):
                raise TypeError("Invalid type for `cloud_region`, type has to be `GoogleCloudRegion`")

        self._cloud_region = cloud_region

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        if hasattr(super(GcsServiceAccountOutput, self), "to_dict"):
            result = super(GcsServiceAccountOutput, self).to_dict()
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
        if not isinstance(other, GcsServiceAccountOutput):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

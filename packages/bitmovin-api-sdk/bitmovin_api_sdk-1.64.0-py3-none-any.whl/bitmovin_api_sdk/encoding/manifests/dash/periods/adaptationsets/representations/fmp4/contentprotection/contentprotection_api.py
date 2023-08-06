# coding: utf-8

from __future__ import absolute_import

from bitmovin_api_sdk.common import BaseApi, BitmovinApiLoggerBase
from bitmovin_api_sdk.common.poscheck import poscheck_except
from bitmovin_api_sdk.models.bitmovin_response import BitmovinResponse
from bitmovin_api_sdk.models.content_protection import ContentProtection
from bitmovin_api_sdk.models.response_envelope import ResponseEnvelope
from bitmovin_api_sdk.models.response_error import ResponseError
from bitmovin_api_sdk.encoding.manifests.dash.periods.adaptationsets.representations.fmp4.contentprotection.content_protection_list_query_params import ContentProtectionListQueryParams


class ContentprotectionApi(BaseApi):
    @poscheck_except(2)
    def __init__(self, api_key, tenant_org_id=None, base_url=None, logger=None):
        # type: (str, str, str, BitmovinApiLoggerBase) -> None

        super(ContentprotectionApi, self).__init__(
            api_key=api_key,
            tenant_org_id=tenant_org_id,
            base_url=base_url,
            logger=logger
        )

    def create(self, manifest_id, period_id, adaptationset_id, representation_id, content_protection, **kwargs):
        # type: (string_types, string_types, string_types, string_types, ContentProtection, dict) -> ContentProtection
        """Add Content Protection to fMP4 Representation

        :param manifest_id: Id of the manifest
        :type manifest_id: string_types, required
        :param period_id: Id of the period
        :type period_id: string_types, required
        :param adaptationset_id: Id of the adaptation set
        :type adaptationset_id: string_types, required
        :param representation_id: Id of the representation
        :type representation_id: string_types, required
        :param content_protection: The content protection to be added to the fMP4 representation
        :type content_protection: ContentProtection, required
        :return: Id of the DRM Fmp4 representation
        :rtype: ContentProtection
        """

        return self.api_client.post(
            '/encoding/manifests/dash/{manifest_id}/periods/{period_id}/adaptationsets/{adaptationset_id}/representations/fmp4/{representation_id}/contentprotection',
            content_protection,
            path_params={'manifest_id': manifest_id, 'period_id': period_id, 'adaptationset_id': adaptationset_id, 'representation_id': representation_id},
            type=ContentProtection,
            **kwargs
        )

    def delete(self, manifest_id, period_id, adaptationset_id, representation_id, contentprotection_id, **kwargs):
        # type: (string_types, string_types, string_types, string_types, string_types, dict) -> BitmovinResponse
        """Delete fMP4 Representation Content Protection

        :param manifest_id: Id of the manifest
        :type manifest_id: string_types, required
        :param period_id: Id of the period
        :type period_id: string_types, required
        :param adaptationset_id: Id of the adaptation set
        :type adaptationset_id: string_types, required
        :param representation_id: Id of the representation
        :type representation_id: string_types, required
        :param contentprotection_id: Id of the DRM fMP4 content protection to be deleted
        :type contentprotection_id: string_types, required
        :return: Id of the fMP4 Representation Content Protection
        :rtype: BitmovinResponse
        """

        return self.api_client.delete(
            '/encoding/manifests/dash/{manifest_id}/periods/{period_id}/adaptationsets/{adaptationset_id}/representations/fmp4/{representation_id}/contentprotection/{contentprotection_id}',
            path_params={'manifest_id': manifest_id, 'period_id': period_id, 'adaptationset_id': adaptationset_id, 'representation_id': representation_id, 'contentprotection_id': contentprotection_id},
            type=BitmovinResponse,
            **kwargs
        )

    def get(self, manifest_id, period_id, adaptationset_id, representation_id, contentprotection_id, **kwargs):
        # type: (string_types, string_types, string_types, string_types, string_types, dict) -> ContentProtection
        """fMP4 Representation Content Protection Details

        :param manifest_id: Id of the manifest
        :type manifest_id: string_types, required
        :param period_id: Id of the period
        :type period_id: string_types, required
        :param adaptationset_id: Id of the adaptation set
        :type adaptationset_id: string_types, required
        :param representation_id: Id of the representation
        :type representation_id: string_types, required
        :param contentprotection_id: Id of the DRM fMP4 content protection
        :type contentprotection_id: string_types, required
        :return: fMP4 Representation Content Protection details
        :rtype: ContentProtection
        """

        return self.api_client.get(
            '/encoding/manifests/dash/{manifest_id}/periods/{period_id}/adaptationsets/{adaptationset_id}/representations/fmp4/{representation_id}/contentprotection/{contentprotection_id}',
            path_params={'manifest_id': manifest_id, 'period_id': period_id, 'adaptationset_id': adaptationset_id, 'representation_id': representation_id, 'contentprotection_id': contentprotection_id},
            type=ContentProtection,
            **kwargs
        )

    def list(self, manifest_id, period_id, adaptationset_id, representation_id, query_params=None, **kwargs):
        # type: (string_types, string_types, string_types, string_types, ContentProtectionListQueryParams, dict) -> ContentProtection
        """List all fMP4 Representation Content Protections

        :param manifest_id: Id of the manifest
        :type manifest_id: string_types, required
        :param period_id: Id of the period
        :type period_id: string_types, required
        :param adaptationset_id: Id of the adaptation set
        :type adaptationset_id: string_types, required
        :param representation_id: Id of the representation
        :type representation_id: string_types, required
        :param query_params: Query parameters
        :type query_params: ContentProtectionListQueryParams
        :return: List of fMP4 Representation Content Protections
        :rtype: ContentProtection
        """

        return self.api_client.get(
            '/encoding/manifests/dash/{manifest_id}/periods/{period_id}/adaptationsets/{adaptationset_id}/representations/fmp4/{representation_id}/contentprotection',
            path_params={'manifest_id': manifest_id, 'period_id': period_id, 'adaptationset_id': adaptationset_id, 'representation_id': representation_id},
            query_params=query_params,
            pagination_response=True,
            type=ContentProtection,
            **kwargs
        )

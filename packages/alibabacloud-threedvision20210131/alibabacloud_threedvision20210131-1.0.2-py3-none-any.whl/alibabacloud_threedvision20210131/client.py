# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_threedvision20210131 import models as threedvision_20210131_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_rpc import models as rpc_models
from alibabacloud_openplatform20191219.client import Client as OpenPlatformClient
from alibabacloud_openplatform20191219 import models as open_platform_models
from alibabacloud_oss_sdk import models as oss_models
from alibabacloud_tea_fileform import models as file_form_models
from alibabacloud_oss_util import models as ossutil_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from alibabacloud_oss_sdk.client import Client as OSSClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = ''
        self.check_config(config)
        self._endpoint = self.get_endpoint('threedvision', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def reconstruct_body_by_single_image_with_options(
        self,
        request: threedvision_20210131_models.ReconstructBodyBySingleImageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> threedvision_20210131_models.ReconstructBodyBySingleImageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return threedvision_20210131_models.ReconstructBodyBySingleImageResponse().from_map(
            self.do_rpcrequest('ReconstructBodyBySingleImage', '2021-01-31', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def reconstruct_body_by_single_image_with_options_async(
        self,
        request: threedvision_20210131_models.ReconstructBodyBySingleImageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> threedvision_20210131_models.ReconstructBodyBySingleImageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return threedvision_20210131_models.ReconstructBodyBySingleImageResponse().from_map(
            await self.do_rpcrequest_async('ReconstructBodyBySingleImage', '2021-01-31', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def reconstruct_body_by_single_image(
        self,
        request: threedvision_20210131_models.ReconstructBodyBySingleImageRequest,
    ) -> threedvision_20210131_models.ReconstructBodyBySingleImageResponse:
        runtime = util_models.RuntimeOptions()
        return self.reconstruct_body_by_single_image_with_options(request, runtime)

    async def reconstruct_body_by_single_image_async(
        self,
        request: threedvision_20210131_models.ReconstructBodyBySingleImageRequest,
    ) -> threedvision_20210131_models.ReconstructBodyBySingleImageResponse:
        runtime = util_models.RuntimeOptions()
        return await self.reconstruct_body_by_single_image_with_options_async(request, runtime)

    def reconstruct_body_by_single_image_advance(
        self,
        request: threedvision_20210131_models.ReconstructBodyBySingleImageAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> threedvision_20210131_models.ReconstructBodyBySingleImageResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='threedvision',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        reconstruct_body_by_single_image_req = threedvision_20210131_models.ReconstructBodyBySingleImageRequest()
        OpenApiUtilClient.convert(request, reconstruct_body_by_single_image_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        reconstruct_body_by_single_image_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        reconstruct_body_by_single_image_resp = self.reconstruct_body_by_single_image_with_options(reconstruct_body_by_single_image_req, runtime)
        return reconstruct_body_by_single_image_resp

    async def reconstruct_body_by_single_image_advance_async(
        self,
        request: threedvision_20210131_models.ReconstructBodyBySingleImageAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> threedvision_20210131_models.ReconstructBodyBySingleImageResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='threedvision',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        reconstruct_body_by_single_image_req = threedvision_20210131_models.ReconstructBodyBySingleImageRequest()
        OpenApiUtilClient.convert(request, reconstruct_body_by_single_image_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        reconstruct_body_by_single_image_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        reconstruct_body_by_single_image_resp = await self.reconstruct_body_by_single_image_with_options_async(reconstruct_body_by_single_image_req, runtime)
        return reconstruct_body_by_single_image_resp

    def estimate_monocular_image_depth_with_options(
        self,
        request: threedvision_20210131_models.EstimateMonocularImageDepthRequest,
        runtime: util_models.RuntimeOptions,
    ) -> threedvision_20210131_models.EstimateMonocularImageDepthResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return threedvision_20210131_models.EstimateMonocularImageDepthResponse().from_map(
            self.do_rpcrequest('EstimateMonocularImageDepth', '2021-01-31', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def estimate_monocular_image_depth_with_options_async(
        self,
        request: threedvision_20210131_models.EstimateMonocularImageDepthRequest,
        runtime: util_models.RuntimeOptions,
    ) -> threedvision_20210131_models.EstimateMonocularImageDepthResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return threedvision_20210131_models.EstimateMonocularImageDepthResponse().from_map(
            await self.do_rpcrequest_async('EstimateMonocularImageDepth', '2021-01-31', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def estimate_monocular_image_depth(
        self,
        request: threedvision_20210131_models.EstimateMonocularImageDepthRequest,
    ) -> threedvision_20210131_models.EstimateMonocularImageDepthResponse:
        runtime = util_models.RuntimeOptions()
        return self.estimate_monocular_image_depth_with_options(request, runtime)

    async def estimate_monocular_image_depth_async(
        self,
        request: threedvision_20210131_models.EstimateMonocularImageDepthRequest,
    ) -> threedvision_20210131_models.EstimateMonocularImageDepthResponse:
        runtime = util_models.RuntimeOptions()
        return await self.estimate_monocular_image_depth_with_options_async(request, runtime)

    def estimate_monocular_image_depth_advance(
        self,
        request: threedvision_20210131_models.EstimateMonocularImageDepthAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> threedvision_20210131_models.EstimateMonocularImageDepthResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='threedvision',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        estimate_monocular_image_depth_req = threedvision_20210131_models.EstimateMonocularImageDepthRequest()
        OpenApiUtilClient.convert(request, estimate_monocular_image_depth_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        estimate_monocular_image_depth_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        estimate_monocular_image_depth_resp = self.estimate_monocular_image_depth_with_options(estimate_monocular_image_depth_req, runtime)
        return estimate_monocular_image_depth_resp

    async def estimate_monocular_image_depth_advance_async(
        self,
        request: threedvision_20210131_models.EstimateMonocularImageDepthAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> threedvision_20210131_models.EstimateMonocularImageDepthResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='threedvision',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        estimate_monocular_image_depth_req = threedvision_20210131_models.EstimateMonocularImageDepthRequest()
        OpenApiUtilClient.convert(request, estimate_monocular_image_depth_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        estimate_monocular_image_depth_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        estimate_monocular_image_depth_resp = await self.estimate_monocular_image_depth_with_options_async(estimate_monocular_image_depth_req, runtime)
        return estimate_monocular_image_depth_resp

    def estimate_stereo_image_depth_with_options(
        self,
        request: threedvision_20210131_models.EstimateStereoImageDepthRequest,
        runtime: util_models.RuntimeOptions,
    ) -> threedvision_20210131_models.EstimateStereoImageDepthResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return threedvision_20210131_models.EstimateStereoImageDepthResponse().from_map(
            self.do_rpcrequest('EstimateStereoImageDepth', '2021-01-31', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def estimate_stereo_image_depth_with_options_async(
        self,
        request: threedvision_20210131_models.EstimateStereoImageDepthRequest,
        runtime: util_models.RuntimeOptions,
    ) -> threedvision_20210131_models.EstimateStereoImageDepthResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return threedvision_20210131_models.EstimateStereoImageDepthResponse().from_map(
            await self.do_rpcrequest_async('EstimateStereoImageDepth', '2021-01-31', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def estimate_stereo_image_depth(
        self,
        request: threedvision_20210131_models.EstimateStereoImageDepthRequest,
    ) -> threedvision_20210131_models.EstimateStereoImageDepthResponse:
        runtime = util_models.RuntimeOptions()
        return self.estimate_stereo_image_depth_with_options(request, runtime)

    async def estimate_stereo_image_depth_async(
        self,
        request: threedvision_20210131_models.EstimateStereoImageDepthRequest,
    ) -> threedvision_20210131_models.EstimateStereoImageDepthResponse:
        runtime = util_models.RuntimeOptions()
        return await self.estimate_stereo_image_depth_with_options_async(request, runtime)

# coding: utf-8

from __future__ import absolute_import

import datetime
import re
import importlib

import six

from huaweicloudsdkcore.client import Client, ClientBuilder
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.utils import http_utils
from huaweicloudsdkcore.sdk_stream_request import SdkStreamRequest


class LiveAsyncClient(Client):
    """
    :param configuration: .Configuration object for this client
    :param pool_threads: The number of threads to use for async requests
        to the API. More threads means more concurrent API requests.
    """

    PRIMITIVE_TYPES = (float, bool, bytes, six.text_type) + six.integer_types
    NATIVE_TYPES_MAPPING = {
        'int': int,
        'long': int if six.PY3 else long,
        'float': float,
        'str': str,
        'bool': bool,
        'date': datetime.date,
        'datetime': datetime.datetime,
        'object': object,
    }

    def __init__(self):
        super(LiveAsyncClient, self).__init__()
        self.model_package = importlib.import_module("huaweicloudsdklive.v1.model")
        self.preset_headers = {'User-Agent': 'HuaweiCloud-SDK-Python'}

    @classmethod
    def new_builder(cls, clazz=None):
        if clazz is None:
            return ClientBuilder(cls)

        if clazz.__name__ != "LiveClient":
            raise TypeError("client type error, support client type is LiveClient")

        return ClientBuilder(clazz)

    def create_domain_async(self, request):
        """创建直播域名

        可单独创建直播播放域名或推流域名，每个租户最多可配置64条域名记录。 

        :param CreateDomainRequest request
        :return: CreateDomainResponse
        """
        return self.create_domain_with_http_info(request)

    def create_domain_with_http_info(self, request):
        """创建直播域名

        可单独创建直播播放域名或推流域名，每个租户最多可配置64条域名记录。 

        :param CreateDomainRequest request
        :return: CreateDomainResponse
        """

        all_params = ['create_domain_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json; charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/domain',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateDomainResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_domain_mapping_async(self, request):
        """域名映射

        将用户已创建的播放域名和推流域名建立域名映射关系

        :param CreateDomainMappingRequest request
        :return: CreateDomainMappingResponse
        """
        return self.create_domain_mapping_with_http_info(request)

    def create_domain_mapping_with_http_info(self, request):
        """域名映射

        将用户已创建的播放域名和推流域名建立域名映射关系

        :param CreateDomainMappingRequest request
        :return: CreateDomainMappingResponse
        """

        all_params = ['create_domain_mapping_request_body', 'specify_project']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'specify_project' in local_var_params:
            query_params.append(('specify_project', local_var_params['specify_project']))

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json; charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/domains_mapping',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateDomainMappingResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_record_config_async(self, request):
        """创建录制配置

        创建录制配置接口

        :param CreateRecordConfigRequest request
        :return: CreateRecordConfigResponse
        """
        return self.create_record_config_with_http_info(request)

    def create_record_config_with_http_info(self, request):
        """创建录制配置

        创建录制配置接口

        :param CreateRecordConfigRequest request
        :return: CreateRecordConfigResponse
        """

        all_params = ['create_record_config_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json; charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/record/config',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateRecordConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_stream_forbidden_async(self, request):
        """禁止直播推流

        禁止直播推流

        :param CreateStreamForbiddenRequest request
        :return: CreateStreamForbiddenResponse
        """
        return self.create_stream_forbidden_with_http_info(request)

    def create_stream_forbidden_with_http_info(self, request):
        """禁止直播推流

        禁止直播推流

        :param CreateStreamForbiddenRequest request
        :return: CreateStreamForbiddenResponse
        """

        all_params = ['create_stream_forbidden_request_body', 'specify_project']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'specify_project' in local_var_params:
            query_params.append(('specify_project', local_var_params['specify_project']))

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json; charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/stream/blocks',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateStreamForbiddenResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_transcodings_template_async(self, request):
        """创建直播转码模板

        创建直播转码模板

        :param CreateTranscodingsTemplateRequest request
        :return: CreateTranscodingsTemplateResponse
        """
        return self.create_transcodings_template_with_http_info(request)

    def create_transcodings_template_with_http_info(self, request):
        """创建直播转码模板

        创建直播转码模板

        :param CreateTranscodingsTemplateRequest request
        :return: CreateTranscodingsTemplateResponse
        """

        all_params = ['create_transcodings_template_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json; charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/template/transcodings',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateTranscodingsTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_domain_async(self, request):
        """删除直播域名

        删除域名。只有在域名停用（off）状态时才能删除。

        :param DeleteDomainRequest request
        :return: DeleteDomainResponse
        """
        return self.delete_domain_with_http_info(request)

    def delete_domain_with_http_info(self, request):
        """删除直播域名

        删除域名。只有在域名停用（off）状态时才能删除。

        :param DeleteDomainRequest request
        :return: DeleteDomainResponse
        """

        all_params = ['domain']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'domain' in local_var_params:
            query_params.append(('domain', local_var_params['domain']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/domain',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteDomainResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_domain_mapping_async(self, request):
        """删除直播域名映射关系

        将播放域名和推流域名的域名映射关系删除

        :param DeleteDomainMappingRequest request
        :return: DeleteDomainMappingResponse
        """
        return self.delete_domain_mapping_with_http_info(request)

    def delete_domain_mapping_with_http_info(self, request):
        """删除直播域名映射关系

        将播放域名和推流域名的域名映射关系删除

        :param DeleteDomainMappingRequest request
        :return: DeleteDomainMappingResponse
        """

        all_params = ['pull_domain', 'push_domain', 'specify_project']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'specify_project' in local_var_params:
            query_params.append(('specify_project', local_var_params['specify_project']))
        if 'pull_domain' in local_var_params:
            query_params.append(('pull_domain', local_var_params['pull_domain']))
        if 'push_domain' in local_var_params:
            query_params.append(('push_domain', local_var_params['push_domain']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/domains_mapping',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteDomainMappingResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_record_config_async(self, request):
        """删除录制配置

        删除录制配置接口

        :param DeleteRecordConfigRequest request
        :return: DeleteRecordConfigResponse
        """
        return self.delete_record_config_with_http_info(request)

    def delete_record_config_with_http_info(self, request):
        """删除录制配置

        删除录制配置接口

        :param DeleteRecordConfigRequest request
        :return: DeleteRecordConfigResponse
        """

        all_params = ['domain', 'app_name']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'domain' in local_var_params:
            query_params.append(('domain', local_var_params['domain']))
        if 'app_name' in local_var_params:
            query_params.append(('app_name', local_var_params['app_name']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/record/config',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteRecordConfigResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_stream_forbidden_async(self, request):
        """禁推恢复

        恢复直播推流接口

        :param DeleteStreamForbiddenRequest request
        :return: DeleteStreamForbiddenResponse
        """
        return self.delete_stream_forbidden_with_http_info(request)

    def delete_stream_forbidden_with_http_info(self, request):
        """禁推恢复

        恢复直播推流接口

        :param DeleteStreamForbiddenRequest request
        :return: DeleteStreamForbiddenResponse
        """

        all_params = ['domain', 'app_name', 'stream_name', 'specify_project']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'specify_project' in local_var_params:
            query_params.append(('specify_project', local_var_params['specify_project']))
        if 'domain' in local_var_params:
            query_params.append(('domain', local_var_params['domain']))
        if 'app_name' in local_var_params:
            query_params.append(('app_name', local_var_params['app_name']))
        if 'stream_name' in local_var_params:
            query_params.append(('stream_name', local_var_params['stream_name']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/stream/blocks',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteStreamForbiddenResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_transcodings_template_async(self, request):
        """删除直播转码模板

        删除直播转码模板

        :param DeleteTranscodingsTemplateRequest request
        :return: DeleteTranscodingsTemplateResponse
        """
        return self.delete_transcodings_template_with_http_info(request)

    def delete_transcodings_template_with_http_info(self, request):
        """删除直播转码模板

        删除直播转码模板

        :param DeleteTranscodingsTemplateRequest request
        :return: DeleteTranscodingsTemplateResponse
        """

        all_params = ['domain', 'app_name']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'domain' in local_var_params:
            query_params.append(('domain', local_var_params['domain']))
        if 'app_name' in local_var_params:
            query_params.append(('app_name', local_var_params['app_name']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/template/transcodings',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteTranscodingsTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_live_sample_logs_async(self, request):
        """获取直播播放日志

        获取直播播放日志，基于域名以5分钟粒度进行打包，日志内容以 \"|\" 进行分隔。 

        :param ListLiveSampleLogsRequest request
        :return: ListLiveSampleLogsResponse
        """
        return self.list_live_sample_logs_with_http_info(request)

    def list_live_sample_logs_with_http_info(self, request):
        """获取直播播放日志

        获取直播播放日志，基于域名以5分钟粒度进行打包，日志内容以 \"|\" 进行分隔。 

        :param ListLiveSampleLogsRequest request
        :return: ListLiveSampleLogsResponse
        """

        all_params = ['play_domain', 'start_time', 'end_time']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'play_domain' in local_var_params:
            query_params.append(('play_domain', local_var_params['play_domain']))
        if 'start_time' in local_var_params:
            query_params.append(('start_time', local_var_params['start_time']))
        if 'end_time' in local_var_params:
            query_params.append(('end_time', local_var_params['end_time']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/logs',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListLiveSampleLogsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_live_streams_online_async(self, request):
        """查询直播中的流信息

        查询直播中的流信息

        :param ListLiveStreamsOnlineRequest request
        :return: ListLiveStreamsOnlineResponse
        """
        return self.list_live_streams_online_with_http_info(request)

    def list_live_streams_online_with_http_info(self, request):
        """查询直播中的流信息

        查询直播中的流信息

        :param ListLiveStreamsOnlineRequest request
        :return: ListLiveStreamsOnlineResponse
        """

        all_params = ['publish_domain', 'app', 'offset', 'limit', 'stream']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'publish_domain' in local_var_params:
            query_params.append(('publish_domain', local_var_params['publish_domain']))
        if 'app' in local_var_params:
            query_params.append(('app', local_var_params['app']))
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'stream' in local_var_params:
            query_params.append(('stream', local_var_params['stream']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/realtime/streams',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListLiveStreamsOnlineResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_record_configs_async(self, request):
        """查询录制配置

        查询录制配置接口

        :param ListRecordConfigsRequest request
        :return: ListRecordConfigsResponse
        """
        return self.list_record_configs_with_http_info(request)

    def list_record_configs_with_http_info(self, request):
        """查询录制配置

        查询录制配置接口

        :param ListRecordConfigsRequest request
        :return: ListRecordConfigsResponse
        """

        all_params = ['domain', 'app_name', 'stream_name', 'page', 'size', 'record_type']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'domain' in local_var_params:
            query_params.append(('domain', local_var_params['domain']))
        if 'app_name' in local_var_params:
            query_params.append(('app_name', local_var_params['app_name']))
        if 'stream_name' in local_var_params:
            query_params.append(('stream_name', local_var_params['stream_name']))
        if 'page' in local_var_params:
            query_params.append(('page', local_var_params['page']))
        if 'size' in local_var_params:
            query_params.append(('size', local_var_params['size']))
        if 'record_type' in local_var_params:
            query_params.append(('record_type', local_var_params['record_type']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/record/config',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListRecordConfigsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_stream_forbidden_async(self, request):
        """查询禁止直播推流列表

        查询禁播黑名单列表

        :param ListStreamForbiddenRequest request
        :return: ListStreamForbiddenResponse
        """
        return self.list_stream_forbidden_with_http_info(request)

    def list_stream_forbidden_with_http_info(self, request):
        """查询禁止直播推流列表

        查询禁播黑名单列表

        :param ListStreamForbiddenRequest request
        :return: ListStreamForbiddenResponse
        """

        all_params = ['domain', 'specify_project', 'app_name', 'stream_name', 'page', 'size']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'specify_project' in local_var_params:
            query_params.append(('specify_project', local_var_params['specify_project']))
        if 'domain' in local_var_params:
            query_params.append(('domain', local_var_params['domain']))
        if 'app_name' in local_var_params:
            query_params.append(('app_name', local_var_params['app_name']))
        if 'stream_name' in local_var_params:
            query_params.append(('stream_name', local_var_params['stream_name']))
        if 'page' in local_var_params:
            query_params.append(('page', local_var_params['page']))
        if 'size' in local_var_params:
            query_params.append(('size', local_var_params['size']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/stream/blocks',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListStreamForbiddenResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_bandwidth_async(self, request):
        """查询直播加速的带宽数据

        查询直播加速的播流域名网络带宽监控数据

        :param ShowBandwidthRequest request
        :return: ShowBandwidthResponse
        """
        return self.show_bandwidth_with_http_info(request)

    def show_bandwidth_with_http_info(self, request):
        """查询直播加速的带宽数据

        查询直播加速的播流域名网络带宽监控数据

        :param ShowBandwidthRequest request
        :return: ShowBandwidthResponse
        """

        all_params = ['domain', 'start_time', 'end_time', 'step']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'domain' in local_var_params:
            query_params.append(('domain', local_var_params['domain']))
        if 'start_time' in local_var_params:
            query_params.append(('start_time', local_var_params['start_time']))
        if 'end_time' in local_var_params:
            query_params.append(('end_time', local_var_params['end_time']))
        if 'step' in local_var_params:
            query_params.append(('step', local_var_params['step']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/stream/bandwidth',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowBandwidthResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_domain_async(self, request):
        """查询直播域名

        查询直播域名

        :param ShowDomainRequest request
        :return: ShowDomainResponse
        """
        return self.show_domain_with_http_info(request)

    def show_domain_with_http_info(self, request):
        """查询直播域名

        查询直播域名

        :param ShowDomainRequest request
        :return: ShowDomainResponse
        """

        all_params = ['domain']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'domain' in local_var_params:
            query_params.append(('domain', local_var_params['domain']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/domain',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowDomainResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_online_users_async(self, request):
        """查询直播播放在线人数

        查询加速的直播播放在线人数

        :param ShowOnlineUsersRequest request
        :return: ShowOnlineUsersResponse
        """
        return self.show_online_users_with_http_info(request)

    def show_online_users_with_http_info(self, request):
        """查询直播播放在线人数

        查询加速的直播播放在线人数

        :param ShowOnlineUsersRequest request
        :return: ShowOnlineUsersResponse
        """

        all_params = ['domain', 'app_name', 'stream_name', 'start_time', 'end_time', 'step']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'domain' in local_var_params:
            query_params.append(('domain', local_var_params['domain']))
        if 'app_name' in local_var_params:
            query_params.append(('app_name', local_var_params['app_name']))
        if 'stream_name' in local_var_params:
            query_params.append(('stream_name', local_var_params['stream_name']))
        if 'start_time' in local_var_params:
            query_params.append(('start_time', local_var_params['start_time']))
        if 'end_time' in local_var_params:
            query_params.append(('end_time', local_var_params['end_time']))
        if 'step' in local_var_params:
            query_params.append(('step', local_var_params['step']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/stream/users',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowOnlineUsersResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_traffic_async(self, request):
        """查询直播加速的流量数据

        查询直播加速的播流域名网络流量监控数据

        :param ShowTrafficRequest request
        :return: ShowTrafficResponse
        """
        return self.show_traffic_with_http_info(request)

    def show_traffic_with_http_info(self, request):
        """查询直播加速的流量数据

        查询直播加速的播流域名网络流量监控数据

        :param ShowTrafficRequest request
        :return: ShowTrafficResponse
        """

        all_params = ['domain', 'start_time', 'end_time', 'step']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'domain' in local_var_params:
            query_params.append(('domain', local_var_params['domain']))
        if 'start_time' in local_var_params:
            query_params.append(('start_time', local_var_params['start_time']))
        if 'end_time' in local_var_params:
            query_params.append(('end_time', local_var_params['end_time']))
        if 'step' in local_var_params:
            query_params.append(('step', local_var_params['step']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/stream/traffic',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowTrafficResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_transcodings_template_async(self, request):
        """查询直播转码模板

        查询直播转码模板

        :param ShowTranscodingsTemplateRequest request
        :return: ShowTranscodingsTemplateResponse
        """
        return self.show_transcodings_template_with_http_info(request)

    def show_transcodings_template_with_http_info(self, request):
        """查询直播转码模板

        查询直播转码模板

        :param ShowTranscodingsTemplateRequest request
        :return: ShowTranscodingsTemplateResponse
        """

        all_params = ['domain', 'app_name', 'page', 'size']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'domain' in local_var_params:
            query_params.append(('domain', local_var_params['domain']))
        if 'app_name' in local_var_params:
            query_params.append(('app_name', local_var_params['app_name']))
        if 'page' in local_var_params:
            query_params.append(('page', local_var_params['page']))
        if 'size' in local_var_params:
            query_params.append(('size', local_var_params['size']))

        header_params = {}

        form_params = {}

        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/template/transcodings',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowTranscodingsTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_domain_async(self, request):
        """修改直播域名

        修改直播播放、RTMP推流加速域名相关信息

        :param UpdateDomainRequest request
        :return: UpdateDomainResponse
        """
        return self.update_domain_with_http_info(request)

    def update_domain_with_http_info(self, request):
        """修改直播域名

        修改直播播放、RTMP推流加速域名相关信息

        :param UpdateDomainRequest request
        :return: UpdateDomainResponse
        """

        all_params = ['update_domain_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json; charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/domain',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateDomainResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_stream_forbidden_async(self, request):
        """修改禁推属性

        修改禁推属性

        :param UpdateStreamForbiddenRequest request
        :return: UpdateStreamForbiddenResponse
        """
        return self.update_stream_forbidden_with_http_info(request)

    def update_stream_forbidden_with_http_info(self, request):
        """修改禁推属性

        修改禁推属性

        :param UpdateStreamForbiddenRequest request
        :return: UpdateStreamForbiddenResponse
        """

        all_params = ['update_stream_forbidden_request_body', 'specify_project']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'specify_project' in local_var_params:
            query_params.append(('specify_project', local_var_params['specify_project']))

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json; charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/stream/blocks',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateStreamForbiddenResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_transcodings_template_async(self, request):
        """配置直播转码模板

        修改直播转码模板

        :param UpdateTranscodingsTemplateRequest request
        :return: UpdateTranscodingsTemplateResponse
        """
        return self.update_transcodings_template_with_http_info(request)

    def update_transcodings_template_with_http_info(self, request):
        """配置直播转码模板

        修改直播转码模板

        :param UpdateTranscodingsTemplateRequest request
        :return: UpdateTranscodingsTemplateResponse
        """

        all_params = ['update_transcodings_template_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json; charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/template/transcodings',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateTranscodingsTemplateResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def call_api(self, resource_path, method, path_params=None, query_params=None, header_params=None, body=None,
                 post_params=None, response_type=None, response_headers=None, auth_settings=None,
                 collection_formats=None, request_type=None):
        """Makes the HTTP request and returns deserialized data.

        :param resource_path: Path to method endpoint.
        :param method: Method to call.
        :param path_params: Path parameters in the url.
        :param query_params: Query parameters in the url.
        :param header_params: Header parameters to be
            placed in the request header.
        :param body: Request body.
        :param post_params dict: Request post form parameters,
            for `application/x-www-form-urlencoded`, `multipart/form-data`.
        :param auth_settings list: Auth Settings names for the request.
        :param response_type: Response data type.
        :param response_headers: Header should be added to response data.
        :param collection_formats: dict of collection formats for path, query,
            header, and post parameters.
        :param request_type: Request data type.
        :return:
            Return the response directly.
        """
        return self.do_http_request(
            method=method,
            resource_path=resource_path,
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
            post_params=post_params,
            response_type=response_type,
            response_headers=response_headers,
            collection_formats=collection_formats,
            request_type=request_type,
	    async_request=True)

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


class BmsAsyncClient(Client):
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
        super(BmsAsyncClient, self).__init__()
        self.model_package = importlib.import_module("huaweicloudsdkbms.v1.model")
        self.preset_headers = {'User-Agent': 'HuaweiCloud-SDK-Python'}

    @classmethod
    def new_builder(cls, clazz=None):
        if clazz is None:
            return ClientBuilder(cls)

        if clazz.__name__ != "BmsClient":
            raise TypeError("client type error, support client type is BmsClient")

        return ClientBuilder(clazz)

    def attach_baremetal_server_volume_async(self, request):
        """裸金属服务器挂载云硬盘

        裸金属服务器创建成功后，如果发现磁盘不够用或者当前磁盘不满足要求，可以将已有云硬盘挂载给裸金属服务器，作为数据盘使用

        :param AttachBaremetalServerVolumeRequest request
        :return: AttachBaremetalServerVolumeResponse
        """
        return self.attach_baremetal_server_volume_with_http_info(request)

    def attach_baremetal_server_volume_with_http_info(self, request):
        """裸金属服务器挂载云硬盘

        裸金属服务器创建成功后，如果发现磁盘不够用或者当前磁盘不满足要求，可以将已有云硬盘挂载给裸金属服务器，作为数据盘使用

        :param AttachBaremetalServerVolumeRequest request
        :return: AttachBaremetalServerVolumeResponse
        """

        all_params = ['server_id', 'attach_volume']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

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
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/baremetalservers/{server_id}/attachvolume',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='AttachBaremetalServerVolumeResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def batch_reboot_baremetal_servers_async(self, request):
        """重启裸金属服务器

        根据给定的裸金属服务器ID列表，批量重启裸金属服务器

        :param BatchRebootBaremetalServersRequest request
        :return: BatchRebootBaremetalServersResponse
        """
        return self.batch_reboot_baremetal_servers_with_http_info(request)

    def batch_reboot_baremetal_servers_with_http_info(self, request):
        """重启裸金属服务器

        根据给定的裸金属服务器ID列表，批量重启裸金属服务器

        :param BatchRebootBaremetalServersRequest request
        :return: BatchRebootBaremetalServersResponse
        """

        all_params = ['reboot_body']
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
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/baremetalservers/action',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='BatchRebootBaremetalServersResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def batch_start_baremetal_servers_async(self, request):
        """启动裸金属服务器

        根据给定的裸金属服务器ID列表，批量启动裸金属服务器

        :param BatchStartBaremetalServersRequest request
        :return: BatchStartBaremetalServersResponse
        """
        return self.batch_start_baremetal_servers_with_http_info(request)

    def batch_start_baremetal_servers_with_http_info(self, request):
        """启动裸金属服务器

        根据给定的裸金属服务器ID列表，批量启动裸金属服务器

        :param BatchStartBaremetalServersRequest request
        :return: BatchStartBaremetalServersResponse
        """

        all_params = ['os_start_body']
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
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/baremetalservers/action',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='BatchStartBaremetalServersResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def batch_stop_baremetal_servers_async(self, request):
        """关闭裸金属服务器

        根据给定的裸金属服务器ID列表，批量关闭裸金属服务器

        :param BatchStopBaremetalServersRequest request
        :return: BatchStopBaremetalServersResponse
        """
        return self.batch_stop_baremetal_servers_with_http_info(request)

    def batch_stop_baremetal_servers_with_http_info(self, request):
        """关闭裸金属服务器

        根据给定的裸金属服务器ID列表，批量关闭裸金属服务器

        :param BatchStopBaremetalServersRequest request
        :return: BatchStopBaremetalServersResponse
        """

        all_params = ['os_stop_body']
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
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/baremetalservers/action',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='BatchStopBaremetalServersResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def change_baremetal_server_name_async(self, request):
        """修改裸金属服务器名称

        修改裸金属服务器名称

        :param ChangeBaremetalServerNameRequest request
        :return: ChangeBaremetalServerNameResponse
        """
        return self.change_baremetal_server_name_with_http_info(request)

    def change_baremetal_server_name_with_http_info(self, request):
        """修改裸金属服务器名称

        修改裸金属服务器名称

        :param ChangeBaremetalServerNameRequest request
        :return: ChangeBaremetalServerNameResponse
        """

        all_params = ['server_id', 'change_baremetal_name_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

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
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/baremetalservers/{server_id}',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ChangeBaremetalServerNameResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def create_bare_metal_servers_async(self, request):
        """创建裸金属服务器

        创建一台或多台裸金属服务器,裸金属服务器的登录鉴权方式包括两种：密钥对、密码。为安全起见，推荐使用密钥对方式

        :param CreateBareMetalServersRequest request
        :return: CreateBareMetalServersResponse
        """
        return self.create_bare_metal_servers_with_http_info(request)

    def create_bare_metal_servers_with_http_info(self, request):
        """创建裸金属服务器

        创建一台或多台裸金属服务器,裸金属服务器的登录鉴权方式包括两种：密钥对、密码。为安全起见，推荐使用密钥对方式

        :param CreateBareMetalServersRequest request
        :return: CreateBareMetalServersResponse
        """

        all_params = ['create_baremetal_servers_body']
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
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/baremetalservers',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='CreateBareMetalServersResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def delete_windows_bare_metal_server_password_async(self, request):
        """Windows裸金属服务器清除密码

        清除Windows裸金属服务器初始安装时系统生成的密码记录。清除密码后，不影响裸金属服务器密码登录功能，但不能再使用获取密码功能来查询该裸金属服务器密码。如果裸金属服务器是通过私有镜像创建的，请确保已安装Cloudbase-init。公共镜像默认已安装该软件

        :param DeleteWindowsBareMetalServerPasswordRequest request
        :return: DeleteWindowsBareMetalServerPasswordResponse
        """
        return self.delete_windows_bare_metal_server_password_with_http_info(request)

    def delete_windows_bare_metal_server_password_with_http_info(self, request):
        """Windows裸金属服务器清除密码

        清除Windows裸金属服务器初始安装时系统生成的密码记录。清除密码后，不影响裸金属服务器密码登录功能，但不能再使用获取密码功能来查询该裸金属服务器密码。如果裸金属服务器是通过私有镜像创建的，请确保已安装Cloudbase-init。公共镜像默认已安装该软件

        :param DeleteWindowsBareMetalServerPasswordRequest request
        :return: DeleteWindowsBareMetalServerPasswordResponse
        """

        all_params = ['server_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

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
            resource_path='/v1/{project_id}/baremetalservers/{server_id}/os-server-password',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DeleteWindowsBareMetalServerPasswordResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def detach_baremetal_server_volume_async(self, request):
        """裸金属服务器卸载云磁盘

        将挂载至裸金属服务器中的磁盘卸载；对于挂载在系统盘盘位（也就是“/dev/sda”挂载点）上的磁盘，不允许执行卸载操作；对于挂载在数据盘盘位（非“/dev/sda”挂载点）上的磁盘，支持离线卸载和在线卸载（裸金属服务器处于“运行中”状态）磁盘

        :param DetachBaremetalServerVolumeRequest request
        :return: DetachBaremetalServerVolumeResponse
        """
        return self.detach_baremetal_server_volume_with_http_info(request)

    def detach_baremetal_server_volume_with_http_info(self, request):
        """裸金属服务器卸载云磁盘

        将挂载至裸金属服务器中的磁盘卸载；对于挂载在系统盘盘位（也就是“/dev/sda”挂载点）上的磁盘，不允许执行卸载操作；对于挂载在数据盘盘位（非“/dev/sda”挂载点）上的磁盘，支持离线卸载和在线卸载（裸金属服务器处于“运行中”状态）磁盘

        :param DetachBaremetalServerVolumeRequest request
        :return: DetachBaremetalServerVolumeResponse
        """

        all_params = ['server_id', 'attachment_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']
        if 'attachment_id' in local_var_params:
            path_params['attachment_id'] = local_var_params['attachment_id']

        query_params = []

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
            resource_path='/v1/{project_id}/baremetalservers/{server_id}/detachvolume/{attachment_id}',
            method='DELETE',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='DetachBaremetalServerVolumeResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_bare_metal_server_details_async(self, request):
        """查询裸金属服务器详情

        获取裸金属服务器详细信息，该接口支持查询裸金属服务器的计费方式，以及是否被冻结

        :param ListBareMetalServerDetailsRequest request
        :return: ListBareMetalServerDetailsResponse
        """
        return self.list_bare_metal_server_details_with_http_info(request)

    def list_bare_metal_server_details_with_http_info(self, request):
        """查询裸金属服务器详情

        获取裸金属服务器详细信息，该接口支持查询裸金属服务器的计费方式，以及是否被冻结

        :param ListBareMetalServerDetailsRequest request
        :return: ListBareMetalServerDetailsResponse
        """

        all_params = ['server_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

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
            resource_path='/v1/{project_id}/baremetalservers/{server_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListBareMetalServerDetailsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_bare_metal_servers_async(self, request):
        """查询裸金属服务器详情列表

        用户根据设置的请求条件筛选裸金属服务器，并获取裸金属服务器的详细信息。该接口支持查询裸金属服务器计费方式，以及是否被冻结。

        :param ListBareMetalServersRequest request
        :return: ListBareMetalServersResponse
        """
        return self.list_bare_metal_servers_with_http_info(request)

    def list_bare_metal_servers_with_http_info(self, request):
        """查询裸金属服务器详情列表

        用户根据设置的请求条件筛选裸金属服务器，并获取裸金属服务器的详细信息。该接口支持查询裸金属服务器计费方式，以及是否被冻结。

        :param ListBareMetalServersRequest request
        :return: ListBareMetalServersResponse
        """

        all_params = ['flavor', 'name', 'status', 'limit', 'offset', 'tags', 'reservation_id', 'detail', 'enterprise_project_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'flavor' in local_var_params:
            query_params.append(('flavor', local_var_params['flavor']))
        if 'name' in local_var_params:
            query_params.append(('name', local_var_params['name']))
        if 'status' in local_var_params:
            query_params.append(('status', local_var_params['status']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))
        if 'tags' in local_var_params:
            query_params.append(('tags', local_var_params['tags']))
        if 'reservation_id' in local_var_params:
            query_params.append(('reservation_id', local_var_params['reservation_id']))
        if 'detail' in local_var_params:
            query_params.append(('detail', local_var_params['detail']))
        if 'enterprise_project_id' in local_var_params:
            query_params.append(('enterprise_project_id', local_var_params['enterprise_project_id']))

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
            resource_path='/v1/{project_id}/baremetalservers/detail',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListBareMetalServersResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def list_baremetal_flavor_detail_extends_async(self, request):
        """查询规格详情和规格扩展信息列表

        查询裸金属服务器的规格详情和规格的扩展信息。您可以调用此接口查询“baremetal:extBootType”参数取值，以确认某个规格是否支持快速发放

        :param ListBaremetalFlavorDetailExtendsRequest request
        :return: ListBaremetalFlavorDetailExtendsResponse
        """
        return self.list_baremetal_flavor_detail_extends_with_http_info(request)

    def list_baremetal_flavor_detail_extends_with_http_info(self, request):
        """查询规格详情和规格扩展信息列表

        查询裸金属服务器的规格详情和规格的扩展信息。您可以调用此接口查询“baremetal:extBootType”参数取值，以确认某个规格是否支持快速发放

        :param ListBaremetalFlavorDetailExtendsRequest request
        :return: ListBaremetalFlavorDetailExtendsResponse
        """

        all_params = ['availability_zone']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'availability_zone' in local_var_params:
            query_params.append(('availability_zone', local_var_params['availability_zone']))

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
            resource_path='/v1/{project_id}/baremetalservers/flavors',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ListBaremetalFlavorDetailExtendsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def reinstall_baremetal_server_os_async(self, request):
        """重装裸金属服务器操作系统

        重装裸金属服务器的操作系统。快速发放裸金属服务器支持裸金属服务器数据盘不变的情况下，使用原镜像重装系统盘。重装操作系统支持密码或者密钥注入

        :param ReinstallBaremetalServerOsRequest request
        :return: ReinstallBaremetalServerOsResponse
        """
        return self.reinstall_baremetal_server_os_with_http_info(request)

    def reinstall_baremetal_server_os_with_http_info(self, request):
        """重装裸金属服务器操作系统

        重装裸金属服务器的操作系统。快速发放裸金属服务器支持裸金属服务器数据盘不变的情况下，使用原镜像重装系统盘。重装操作系统支持密码或者密钥注入

        :param ReinstallBaremetalServerOsRequest request
        :return: ReinstallBaremetalServerOsResponse
        """

        all_params = ['server_id', 'os_reinstall_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

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
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/baremetalservers/{server_id}/reinstallos',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ReinstallBaremetalServerOsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def reset_pwd_one_click_async(self, request):
        """一键重置裸金属服务器密码

        在裸金属服务器支持一键重置密码功能的前提下，重置裸金属服务器管理帐号（root用户或Administrator用户）的密码。可以通过6.10.1-查询是否支持一键重置密码API查询是否支持一键重置密码。

        :param ResetPwdOneClickRequest request
        :return: ResetPwdOneClickResponse
        """
        return self.reset_pwd_one_click_with_http_info(request)

    def reset_pwd_one_click_with_http_info(self, request):
        """一键重置裸金属服务器密码

        在裸金属服务器支持一键重置密码功能的前提下，重置裸金属服务器管理帐号（root用户或Administrator用户）的密码。可以通过6.10.1-查询是否支持一键重置密码API查询是否支持一键重置密码。

        :param ResetPwdOneClickRequest request
        :return: ResetPwdOneClickResponse
        """

        all_params = ['server_id', 'reset_password_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

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
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/baremetalservers/{server_id}/os-reset-password',
            method='PUT',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ResetPwdOneClickResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_baremetal_server_interface_attachments_async(self, request):
        """查询裸金属服务器网卡信息

        查询裸金属服务器的网卡信息，比如网卡的IP地址、MAC地址

        :param ShowBaremetalServerInterfaceAttachmentsRequest request
        :return: ShowBaremetalServerInterfaceAttachmentsResponse
        """
        return self.show_baremetal_server_interface_attachments_with_http_info(request)

    def show_baremetal_server_interface_attachments_with_http_info(self, request):
        """查询裸金属服务器网卡信息

        查询裸金属服务器的网卡信息，比如网卡的IP地址、MAC地址

        :param ShowBaremetalServerInterfaceAttachmentsRequest request
        :return: ShowBaremetalServerInterfaceAttachmentsResponse
        """

        all_params = ['server_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

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
            resource_path='/v1/{project_id}/baremetalservers/{server_id}/os-interface',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowBaremetalServerInterfaceAttachmentsResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_baremetal_server_volume_info_async(self, request):
        """查询裸金属服务器挂载的云硬盘信息

        查询裸金属服务器挂载的磁盘信息

        :param ShowBaremetalServerVolumeInfoRequest request
        :return: ShowBaremetalServerVolumeInfoResponse
        """
        return self.show_baremetal_server_volume_info_with_http_info(request)

    def show_baremetal_server_volume_info_with_http_info(self, request):
        """查询裸金属服务器挂载的云硬盘信息

        查询裸金属服务器挂载的磁盘信息

        :param ShowBaremetalServerVolumeInfoRequest request
        :return: ShowBaremetalServerVolumeInfoResponse
        """

        all_params = ['server_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

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
            resource_path='/v1/{project_id}/baremetalservers/{server_id}/os-volume_attachments',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowBaremetalServerVolumeInfoResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_reset_pwd_async(self, request):
        """查询是否支持一键重置密码

        查询是否支持一键重置密码

        :param ShowResetPwdRequest request
        :return: ShowResetPwdResponse
        """
        return self.show_reset_pwd_with_http_info(request)

    def show_reset_pwd_with_http_info(self, request):
        """查询是否支持一键重置密码

        查询是否支持一键重置密码

        :param ShowResetPwdRequest request
        :return: ShowResetPwdResponse
        """

        all_params = ['server_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

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
            resource_path='/v1/{project_id}/baremetalservers/{server_id}/os-resetpwd-flag',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowResetPwdResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_tenant_quota_async(self, request):
        """查询租户配额

        查询该租户下，所有资源的配额信息，包括已使用配额

        :param ShowTenantQuotaRequest request
        :return: ShowTenantQuotaResponse
        """
        return self.show_tenant_quota_with_http_info(request)

    def show_tenant_quota_with_http_info(self, request):
        """查询租户配额

        查询该租户下，所有资源的配额信息，包括已使用配额

        :param ShowTenantQuotaRequest request
        :return: ShowTenantQuotaResponse
        """

        all_params = []
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
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/baremetalservers/limits',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowTenantQuotaResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_windows_baremetal_server_pwd_async(self, request):
        """Windows裸金属服务器获取密码

        获取Windows裸金属服务器初始安装时系统生成的管理员帐户（Administrator帐户或Cloudbase-init设置的帐户）随机密码。如果裸金属服务器是通过私有镜像创建的，请确保已安装Cloudbase-init。公共镜像默认已安装该软件

        :param ShowWindowsBaremetalServerPwdRequest request
        :return: ShowWindowsBaremetalServerPwdResponse
        """
        return self.show_windows_baremetal_server_pwd_with_http_info(request)

    def show_windows_baremetal_server_pwd_with_http_info(self, request):
        """Windows裸金属服务器获取密码

        获取Windows裸金属服务器初始安装时系统生成的管理员帐户（Administrator帐户或Cloudbase-init设置的帐户）随机密码。如果裸金属服务器是通过私有镜像创建的，请确保已安装Cloudbase-init。公共镜像默认已安装该软件

        :param ShowWindowsBaremetalServerPwdRequest request
        :return: ShowWindowsBaremetalServerPwdResponse
        """

        all_params = ['server_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

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
            resource_path='/v1/{project_id}/baremetalservers/{server_id}/os-server-password',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowWindowsBaremetalServerPwdResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def update_baremetal_server_metadata_async(self, request):
        """更新裸金属服务器元数据

        更新裸金属服务器元数据。如果元数据中没有待更新字段，则自动添加该字段。如果元数据中已存在待更新字段，则直接更新字段值；如果元数据中的字段不再请求参数中，则保持不变

        :param UpdateBaremetalServerMetadataRequest request
        :return: UpdateBaremetalServerMetadataResponse
        """
        return self.update_baremetal_server_metadata_with_http_info(request)

    def update_baremetal_server_metadata_with_http_info(self, request):
        """更新裸金属服务器元数据

        更新裸金属服务器元数据。如果元数据中没有待更新字段，则自动添加该字段。如果元数据中已存在待更新字段，则直接更新字段值；如果元数据中的字段不再请求参数中，则保持不变

        :param UpdateBaremetalServerMetadataRequest request
        :return: UpdateBaremetalServerMetadataResponse
        """

        all_params = ['server_id', 'meta_data']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

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
            ['application/json;charset=UTF-8'])

        auth_settings = []

        return self.call_api(
            resource_path='/v1/{project_id}/baremetalservers/{server_id}/metadata',
            method='POST',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='UpdateBaremetalServerMetadataResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_specified_version_async(self, request):
        """查询指定API版本信息

        查询裸金属服务指定接口版本的信息

        :param ShowSpecifiedVersionRequest request
        :return: ShowSpecifiedVersionResponse
        """
        return self.show_specified_version_with_http_info(request)

    def show_specified_version_with_http_info(self, request):
        """查询指定API版本信息

        查询裸金属服务指定接口版本的信息

        :param ShowSpecifiedVersionRequest request
        :return: ShowSpecifiedVersionResponse
        """

        all_params = ['api_version']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'api_version' in local_var_params:
            path_params['api_version'] = local_var_params['api_version']

        query_params = []

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
            resource_path='/{api_version}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowSpecifiedVersionResponse',
            response_headers=response_headers,
            auth_settings=auth_settings,
            collection_formats=collection_formats,
            request_type=request.__class__.__name__)


    def show_job_infos_async(self, request):
        """查询Job状态

        查询Job的执行状态。对于创建裸金属服务器物理机、挂卸卷等异步API，命令下发后，会返回job_id，通过job_id可以查询任务的执行状态

        :param ShowJobInfosRequest request
        :return: ShowJobInfosResponse
        """
        return self.show_job_infos_with_http_info(request)

    def show_job_infos_with_http_info(self, request):
        """查询Job状态

        查询Job的执行状态。对于创建裸金属服务器物理机、挂卸卷等异步API，命令下发后，会返回job_id，通过job_id可以查询任务的执行状态

        :param ShowJobInfosRequest request
        :return: ShowJobInfosResponse
        """

        all_params = ['job_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)

        collection_formats = {}

        path_params = {}
        if 'job_id' in local_var_params:
            path_params['job_id'] = local_var_params['job_id']

        query_params = []

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
            resource_path='/v1/{project_id}/jobs/{job_id}',
            method='GET',
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body_params,
            post_params=form_params,
            response_type='ShowJobInfosResponse',
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

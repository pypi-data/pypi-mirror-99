# -*- coding: utf8 -*-
# Copyright (c) 2017-2018 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.gaap.v20180529 import models


class GaapClient(AbstractClient):
    _apiVersion = '2018-05-29'
    _endpoint = 'gaap.tencentcloudapi.com'
    _service = 'gaap'


    def AddRealServers(self, request):
        """This API is used to add the information of the origin server (server), which supports IP or the domain name.

        :param request: Request instance for AddRealServers.
        :type request: :class:`tencentcloud.gaap.v20180529.models.AddRealServersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.AddRealServersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddRealServers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddRealServersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def BindListenerRealServers(self, request):
        """This API (BindListenerRealServers) is used for the TCP/UDP listener to bind/unbind the origin server.
        Note: This API unbinds the previously bound origin servers, and binds the origin servers selected for this call. For example, the previously bound origin servers are A, B and C, and the origin servers selected for this call are C, D and E, then the origin servers bound after this call will be C, D and E.

        :param request: Request instance for BindListenerRealServers.
        :type request: :class:`tencentcloud.gaap.v20180529.models.BindListenerRealServersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.BindListenerRealServersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("BindListenerRealServers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.BindListenerRealServersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def BindRuleRealServers(self, request):
        """This API is used to bind an origin server to the forwarding rules of layer-7 listeners. Note: This API unbinds all previously bound origin servers before binding those selected.

        :param request: Request instance for BindRuleRealServers.
        :type request: :class:`tencentcloud.gaap.v20180529.models.BindRuleRealServersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.BindRuleRealServersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("BindRuleRealServers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.BindRuleRealServersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckProxyCreate(self, request):
        """This API (CheckProxyCreate) is used to query whether an acceleration connection with the specified configuration can be created.

        :param request: Request instance for CheckProxyCreate.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CheckProxyCreateRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CheckProxyCreateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CheckProxyCreate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckProxyCreateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CloseProxies(self, request):
        """This API (CloseProxies) is used to disable connections. If disabled, no traffic will be generated, but the basic configuration fee will still be incurred.

        :param request: Request instance for CloseProxies.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CloseProxiesRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CloseProxiesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CloseProxies", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CloseProxiesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CloseProxyGroup(self, request):
        """This API is used to disable a connection group. Once disabled, the connection group will no longer generate traffic, but the basic connection configuration fees will still be incurred every day.

        :param request: Request instance for CloseProxyGroup.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CloseProxyGroupRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CloseProxyGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CloseProxyGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CloseProxyGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CloseSecurityPolicy(self, request):
        """This API is used to disable security policies.

        :param request: Request instance for CloseSecurityPolicy.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CloseSecurityPolicyRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CloseSecurityPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CloseSecurityPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CloseSecurityPolicyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateCertificate(self, request):
        """This API (CreateCertificate) is used to create the GAAP certificates and configuration files, including basic authentication configuration files, client CA certificates, server SSL certificates, GAAP SSL certificates, and origin server CA certificates.

        :param request: Request instance for CreateCertificate.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateCertificateRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateCertificateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateCertificate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateCertificateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDomain(self, request):
        """This API (CreateDomain) is used to create the access domain name for the HTTP/HTTPS listener. Clients request the backend data by accessing this domain.
        This API only supports connections of version 3.0.

        :param request: Request instance for CreateDomain.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateDomainRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateDomainResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateDomain", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateDomainResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDomainErrorPageInfo(self, request):
        """This API is used to customize the error code of an error response to the specified domain name.

        :param request: Request instance for CreateDomainErrorPageInfo.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateDomainErrorPageInfoRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateDomainErrorPageInfoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateDomainErrorPageInfo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateDomainErrorPageInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateHTTPListener(self, request):
        """This API (CreateHTTPListener) is used to create an HTTP listener in the connection instance.

        :param request: Request instance for CreateHTTPListener.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateHTTPListenerRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateHTTPListenerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateHTTPListener", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateHTTPListenerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateHTTPSListener(self, request):
        """This API (CreateHTTPListener) is used to create an HTTPS listener in the connection instance.

        :param request: Request instance for CreateHTTPSListener.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateHTTPSListenerRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateHTTPSListenerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateHTTPSListener", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateHTTPSListenerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateProxy(self, request):
        """This API (CreateProxy) is used to create an acceleration connection with specified configuration.

        :param request: Request instance for CreateProxy.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateProxyRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateProxyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateProxy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateProxyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateProxyGroup(self, request):
        """This API (CreateProxyGroup) is used to create a connection group.

        :param request: Request instance for CreateProxyGroup.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateProxyGroupRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateProxyGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateProxyGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateProxyGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateProxyGroupDomain(self, request):
        """This API (CreateProxyGroupDomain) is used to create the connection group domain name, and enable the domain name resolution.

        :param request: Request instance for CreateProxyGroupDomain.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateProxyGroupDomainRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateProxyGroupDomainResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateProxyGroupDomain", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateProxyGroupDomainResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateRule(self, request):
        """This API (CreateRule) is used to create the forwarding rules of HTTP/HTTPS listeners.

        :param request: Request instance for CreateRule.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateRuleRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateRuleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateRule", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateRuleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateSecurityPolicy(self, request):
        """This API is used to create security policies.

        :param request: Request instance for CreateSecurityPolicy.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateSecurityPolicyRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateSecurityPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateSecurityPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateSecurityPolicyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateSecurityRules(self, request):
        """This API is used to add security policy rules.

        :param request: Request instance for CreateSecurityRules.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateSecurityRulesRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateSecurityRulesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateSecurityRules", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateSecurityRulesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateTCPListeners(self, request):
        """This API (CreateTCPListeners) is used to batch create TCP listeners of single connections or connection groups.

        :param request: Request instance for CreateTCPListeners.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateTCPListenersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateTCPListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateTCPListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTCPListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateUDPListeners(self, request):
        """This API (CreateTCPListeners) is used to batch create UDP listeners of single connections or connection groups.

        :param request: Request instance for CreateUDPListeners.
        :type request: :class:`tencentcloud.gaap.v20180529.models.CreateUDPListenersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.CreateUDPListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateUDPListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateUDPListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteCertificate(self, request):
        """This API (DeleteCertificate) is used to delete certificates.

        :param request: Request instance for DeleteCertificate.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DeleteCertificateRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DeleteCertificateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteCertificate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteCertificateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteDomain(self, request):
        """This API (DeleteDomain) is only applicable to layer-7 listeners. It is used to delete the domain names of this listener, and all the rules under the domain name. All rules bound to the origin server are unbound automatically.

        :param request: Request instance for DeleteDomain.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DeleteDomainRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DeleteDomainResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteDomain", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteDomainResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteDomainErrorPageInfo(self, request):
        """This API is used to delete a custom error code for a domain name.

        :param request: Request instance for DeleteDomainErrorPageInfo.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DeleteDomainErrorPageInfoRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DeleteDomainErrorPageInfoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteDomainErrorPageInfo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteDomainErrorPageInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteListeners(self, request):
        """This API (DeleteListeners) is used to batch delete the listeners of a connection or connection group, including layer-4/7 listeners.

        :param request: Request instance for DeleteListeners.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DeleteListenersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DeleteListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteProxyGroup(self, request):
        """This API (DeleteProxyGroup) is used to delete a connection group.

        :param request: Request instance for DeleteProxyGroup.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DeleteProxyGroupRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DeleteProxyGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteProxyGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteProxyGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteRule(self, request):
        """This API (DeleteRule) is used to delete the forwarding rules of HTTP/HTTPS listeners.

        :param request: Request instance for DeleteRule.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DeleteRuleRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DeleteRuleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteRule", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteRuleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteSecurityPolicy(self, request):
        """This API is used to delete security policies.

        :param request: Request instance for DeleteSecurityPolicy.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DeleteSecurityPolicyRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DeleteSecurityPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteSecurityPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteSecurityPolicyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteSecurityRules(self, request):
        """This API is used to delete security policy rules.

        :param request: Request instance for DeleteSecurityRules.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DeleteSecurityRulesRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DeleteSecurityRulesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteSecurityRules", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteSecurityRulesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAccessRegions(self, request):
        """This API (DescribeAccessRegions) is used to query acceleration region (client access region).

        :param request: Request instance for DescribeAccessRegions.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeAccessRegionsRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeAccessRegionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAccessRegions", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAccessRegionsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAccessRegionsByDestRegion(self, request):
        """This API (DescribeAccessRegionsByDestRegion) is used to query the list of the available acceleration regions based on the origin server region.

        :param request: Request instance for DescribeAccessRegionsByDestRegion.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeAccessRegionsByDestRegionRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeAccessRegionsByDestRegionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAccessRegionsByDestRegion", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAccessRegionsByDestRegionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCertificateDetail(self, request):
        """This API (DescribeCertificateDetail) is used to query certificate details, including the certificate ID, name, type, content, key, and other information.

        :param request: Request instance for DescribeCertificateDetail.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeCertificateDetailRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeCertificateDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCertificateDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCertificateDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCertificates(self, request):
        """This API (DescribeCertificates) is used to query the list of available certificates.

        :param request: Request instance for DescribeCertificates.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeCertificatesRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeCertificatesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCertificates", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCertificatesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCountryAreaMapping(self, request):
        """This API (DescribeCountryAreaMapping) is used to obtain the country/region code mapping table.

        :param request: Request instance for DescribeCountryAreaMapping.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeCountryAreaMappingRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeCountryAreaMappingResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCountryAreaMapping", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCountryAreaMappingResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDestRegions(self, request):
        """This API (DescribeDestRegions) is used to query an origin server region (i.e., the region in which the origin server locates).

        :param request: Request instance for DescribeDestRegions.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeDestRegionsRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeDestRegionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDestRegions", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDestRegionsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDomainErrorPageInfo(self, request):
        """This API is used to query the custom error response to a domain name.

        :param request: Request instance for DescribeDomainErrorPageInfo.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeDomainErrorPageInfoRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeDomainErrorPageInfoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDomainErrorPageInfo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDomainErrorPageInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDomainErrorPageInfoByIds(self, request):
        """This API is used to query the corresponding error response by a custom error ID.

        :param request: Request instance for DescribeDomainErrorPageInfoByIds.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeDomainErrorPageInfoByIdsRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeDomainErrorPageInfoByIdsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDomainErrorPageInfoByIds", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDomainErrorPageInfoByIdsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeGroupAndStatisticsProxy(self, request):
        """This is an internal API. It is used to query the information of connections and connection groups from which the statistics can be derived.

        :param request: Request instance for DescribeGroupAndStatisticsProxy.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeGroupAndStatisticsProxyRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeGroupAndStatisticsProxyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeGroupAndStatisticsProxy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeGroupAndStatisticsProxyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeGroupDomainConfig(self, request):
        """This API (DescribeGroupDomainConfig) is used to obtain the domain name resolution configuration details of a connection group.

        :param request: Request instance for DescribeGroupDomainConfig.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeGroupDomainConfigRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeGroupDomainConfigResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeGroupDomainConfig", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeGroupDomainConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeHTTPListeners(self, request):
        """This API (DescribeHTTPListeners) is used to query HTTP listener information.

        :param request: Request instance for DescribeHTTPListeners.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeHTTPListenersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeHTTPListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeHTTPListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeHTTPListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeHTTPSListeners(self, request):
        """This API (DescribeHTTPSListeners) is used to query HTTPS listener information.

        :param request: Request instance for DescribeHTTPSListeners.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeHTTPSListenersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeHTTPSListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeHTTPSListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeHTTPSListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeListenerRealServers(self, request):
        """This API (DescribeListenerRealServers) is used to query the origin server list of TCP/UDP listeners, including the list of bound origin servers and origin servers that can be bound.

        :param request: Request instance for DescribeListenerRealServers.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeListenerRealServersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeListenerRealServersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeListenerRealServers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeListenerRealServersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeListenerStatistics(self, request):
        """This API is used to query listener statistics, including inbound/outbound bandwidth, inbound/outbound packets, and concurrence data. It supports granularities of 300, 3,600, and 86,400. Default value is the highest within the granularity range.

        :param request: Request instance for DescribeListenerStatistics.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeListenerStatisticsRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeListenerStatisticsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeListenerStatistics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeListenerStatisticsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeProxies(self, request):
        """This API (DescribeProxies) is used to query the connection instance list.

        :param request: Request instance for DescribeProxies.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeProxiesRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeProxiesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeProxies", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeProxiesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeProxiesStatus(self, request):
        """This API (DescribeProxiesStatus) is used to query the connection status list.

        :param request: Request instance for DescribeProxiesStatus.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeProxiesStatusRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeProxiesStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeProxiesStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeProxiesStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeProxyAndStatisticsListeners(self, request):
        """This is an internal API. It is used to query the information of connections and listeners from which the statistics can be derived.

        :param request: Request instance for DescribeProxyAndStatisticsListeners.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyAndStatisticsListenersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyAndStatisticsListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeProxyAndStatisticsListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeProxyAndStatisticsListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeProxyDetail(self, request):
        """This API (DescribeProxyDetail) is used to query connection details.

        :param request: Request instance for DescribeProxyDetail.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyDetailRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeProxyDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeProxyDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeProxyGroupDetails(self, request):
        """This API (DescribeProxyGroupDetails) is used to query connection group details.

        :param request: Request instance for DescribeProxyGroupDetails.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyGroupDetailsRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyGroupDetailsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeProxyGroupDetails", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeProxyGroupDetailsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeProxyGroupList(self, request):
        """This API (DescribeProxyGroupList) is used to pull the list of connection groups and the basic information of each connection group.

        :param request: Request instance for DescribeProxyGroupList.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyGroupListRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyGroupListResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeProxyGroupList", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeProxyGroupListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeProxyGroupStatistics(self, request):
        """This API is used to query listener statistics, including inbound/outbound bandwidth, inbound/outbound packets, and concurrence data. It supports granularities of 300, 3,600, and 86,400. Default value is the highest within the granularity range.

        :param request: Request instance for DescribeProxyGroupStatistics.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyGroupStatisticsRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyGroupStatisticsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeProxyGroupStatistics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeProxyGroupStatisticsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeProxyStatistics(self, request):
        """This API is used to query listener statistics, including inbound/outbound bandwidth, inbound/outbound packets, concurrence, packet loss, and latency data. It supports granularities of 300, 3,600, and 86,400. Default value is the highest within the granularity range.

        :param request: Request instance for DescribeProxyStatistics.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyStatisticsRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeProxyStatisticsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeProxyStatistics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeProxyStatisticsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRealServerStatistics(self, request):
        """This API is used to query the statistics of an origin server's health check results. Origin server status is displayed as 1 (normal) or 0 (exceptional). The queried origin server must be bound to a listener or rule, and the ID of the bound listener or rule must be specified for the query. This API supports displaying origin server status statistics at a 1-minute granularity.

        :param request: Request instance for DescribeRealServerStatistics.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeRealServerStatisticsRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeRealServerStatisticsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRealServerStatistics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRealServerStatisticsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRealServers(self, request):
        """This API is used to query origin server information. It can query all origin servers under the specified project name, and supports fuzzy query by specified IPs or domain names.

        :param request: Request instance for DescribeRealServers.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeRealServersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeRealServersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRealServers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRealServersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRealServersStatus(self, request):
        """This API (DescribeRealServersStatus) is used to query whether an origin server has been bound to a rule or listener.

        :param request: Request instance for DescribeRealServersStatus.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeRealServersStatusRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeRealServersStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRealServersStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRealServersStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRegionAndPrice(self, request):
        """This API (DescribeRegionAndPrice) is used to obtain the origin server regions and the bandwidth price gradient.

        :param request: Request instance for DescribeRegionAndPrice.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeRegionAndPriceRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeRegionAndPriceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRegionAndPrice", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRegionAndPriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeResourcesByTag(self, request):
        """This API (DescribeResourcesByTag) is used to query corresponding resource information by tags, including connection, connection group, and origin server.

        :param request: Request instance for DescribeResourcesByTag.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeResourcesByTagRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeResourcesByTagResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeResourcesByTag", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeResourcesByTagResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRuleRealServers(self, request):
        """This API (DescribeRuleRealServers) is used to query forwarding rules-related origin server information, including information of origin servers that can be bound and have been bound.

        :param request: Request instance for DescribeRuleRealServers.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeRuleRealServersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeRuleRealServersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRuleRealServers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRuleRealServersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRules(self, request):
        """This API (DescribeRules) is used to query all rule information of a listener, including the domain names, paths, and list of bound origin servers. For version 3.0 connections, this API returns the advanced authentication configuration information of the domain name.

        :param request: Request instance for DescribeRules.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeRulesRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeRulesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRules", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRulesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRulesByRuleIds(self, request):
        """This API is used to pull the list of rules based on rule ID. It supports pulling 1 to 10 rules at a time.

        :param request: Request instance for DescribeRulesByRuleIds.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeRulesByRuleIdsRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeRulesByRuleIdsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRulesByRuleIds", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRulesByRuleIdsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSecurityPolicyDetail(self, request):
        """This API is used to obtain security policy details.

        :param request: Request instance for DescribeSecurityPolicyDetail.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeSecurityPolicyDetailRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeSecurityPolicyDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSecurityPolicyDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSecurityPolicyDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSecurityRules(self, request):
        """This API is used to query the list of security rules based on security rule ID. It supports querying 1 to 20 security rules at a time.

        :param request: Request instance for DescribeSecurityRules.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeSecurityRulesRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeSecurityRulesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSecurityRules", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSecurityRulesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTCPListeners(self, request):
        """This API (DescribeTCPListeners) is used to query the TCP listener information of a single connection or connection group.

        :param request: Request instance for DescribeTCPListeners.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeTCPListenersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeTCPListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTCPListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTCPListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeUDPListeners(self, request):
        """This API (DescribeUDPListeners) is used to query the UDP listener information of a single connection or connection group.

        :param request: Request instance for DescribeUDPListeners.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DescribeUDPListenersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DescribeUDPListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUDPListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUDPListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DestroyProxies(self, request):
        """This API (DestroyProxies) is used to terminate a connection. If terminated, no fees will be incurred.

        :param request: Request instance for DestroyProxies.
        :type request: :class:`tencentcloud.gaap.v20180529.models.DestroyProxiesRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.DestroyProxiesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DestroyProxies", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DestroyProxiesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InquiryPriceCreateProxy(self, request):
        """This API (InquiryPriceCreateProxy) is used to create the price inquiries of acceleration connections.

        :param request: Request instance for InquiryPriceCreateProxy.
        :type request: :class:`tencentcloud.gaap.v20180529.models.InquiryPriceCreateProxyRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.InquiryPriceCreateProxyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceCreateProxy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceCreateProxyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyCertificate(self, request):
        """This API (ModifyCertificate) is used to modify a domain name certificate of a listener. domain name certificate. This API is only applicable to connections of version 3.0.

        :param request: Request instance for ModifyCertificate.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyCertificateRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyCertificateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyCertificate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyCertificateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyCertificateAttributes(self, request):
        """This API is used to modify certificate name and content.

        :param request: Request instance for ModifyCertificateAttributes.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyCertificateAttributesRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyCertificateAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyCertificateAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyCertificateAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyDomain(self, request):
        """This API (ModifyDomain) is used to modify domain names of listeners. For connections of version 3.0, it supports modifying certificates of the domain names.

        :param request: Request instance for ModifyDomain.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyDomainRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyDomainResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDomain", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDomainResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyGroupDomainConfig(self, request):
        """This API (ModifyGroupDomainConfig) is used to configure the nearest access domain name of a connection group.

        :param request: Request instance for ModifyGroupDomainConfig.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyGroupDomainConfigRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyGroupDomainConfigResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyGroupDomainConfig", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyGroupDomainConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyHTTPListenerAttribute(self, request):
        """This API (ModifyHTTPListenerAttribute) is used to modify the HTTP listener configuration information of a connection. Currently only supports modifying listener name.
        Note: Grouped connections currently do not support HTTP/HTTPS listeners.

        :param request: Request instance for ModifyHTTPListenerAttribute.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyHTTPListenerAttributeRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyHTTPListenerAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyHTTPListenerAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyHTTPListenerAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyHTTPSListenerAttribute(self, request):
        """This API (ModifyHTTPSListenerAttribute) is used to modify HTTPS listener configurations. It currently do not support connection groups and connections of version 1.0.

        :param request: Request instance for ModifyHTTPSListenerAttribute.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyHTTPSListenerAttributeRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyHTTPSListenerAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyHTTPSListenerAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyHTTPSListenerAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyProxiesAttribute(self, request):
        """This API (ModifyProxiesAttribute) is used to modify instance attributes (currently only supports modifying connection name).

        :param request: Request instance for ModifyProxiesAttribute.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyProxiesAttributeRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyProxiesAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyProxiesAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyProxiesAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyProxiesProject(self, request):
        """This API (ModifyProxiesProject) is used to modify the project to which a connection belongs.

        :param request: Request instance for ModifyProxiesProject.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyProxiesProjectRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyProxiesProjectResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyProxiesProject", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyProxiesProjectResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyProxyConfiguration(self, request):
        """This API (ModifyProxyConfiguration) is used to modify connection configurations. You can expand or reduce the capacity based on current business requirements. It only supports connections with a Scalarable of 1. Scalarable can be obtained via DescribeProxies API.

        :param request: Request instance for ModifyProxyConfiguration.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyProxyConfigurationRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyProxyConfigurationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyProxyConfiguration", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyProxyConfigurationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyProxyGroupAttribute(self, request):
        """This API (ModifyProxyGroupAttribute) is used to modify connection group attributes. It currently only supports modifying connection group name.

        :param request: Request instance for ModifyProxyGroupAttribute.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyProxyGroupAttributeRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyProxyGroupAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyProxyGroupAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyProxyGroupAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyRealServerName(self, request):
        """This API (ModifyRealServerName) is used to modify origin server names.

        :param request: Request instance for ModifyRealServerName.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyRealServerNameRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyRealServerNameResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRealServerName", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRealServerNameResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyRuleAttribute(self, request):
        """This API (ModifyRuleAttribute) is used to modify forwarding rule information, including health check configuration and forwarding policies.

        :param request: Request instance for ModifyRuleAttribute.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyRuleAttributeRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyRuleAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRuleAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRuleAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifySecurityRule(self, request):
        """This API is used to modify security policy rule names.

        :param request: Request instance for ModifySecurityRule.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifySecurityRuleRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifySecurityRuleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifySecurityRule", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifySecurityRuleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyTCPListenerAttribute(self, request):
        """This API (ModifyTCPListenerAttribute) is used to modify the TCP listener configuration of a connection instance, including health check configuration and scheduling policies.

        :param request: Request instance for ModifyTCPListenerAttribute.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyTCPListenerAttributeRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyTCPListenerAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyTCPListenerAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTCPListenerAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyUDPListenerAttribute(self, request):
        """This API (ModifyUDPListenerAttribute) is used to modify the UDP listener configuration of a connection instance, including modification of listener names and scheduling policies.

        :param request: Request instance for ModifyUDPListenerAttribute.
        :type request: :class:`tencentcloud.gaap.v20180529.models.ModifyUDPListenerAttributeRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.ModifyUDPListenerAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyUDPListenerAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyUDPListenerAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def OpenProxies(self, request):
        """This API (OpenProxies) is used to enable one or more connections.

        :param request: Request instance for OpenProxies.
        :type request: :class:`tencentcloud.gaap.v20180529.models.OpenProxiesRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.OpenProxiesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("OpenProxies", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.OpenProxiesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def OpenProxyGroup(self, request):
        """This API is used to enable all connections in a connection group.

        :param request: Request instance for OpenProxyGroup.
        :type request: :class:`tencentcloud.gaap.v20180529.models.OpenProxyGroupRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.OpenProxyGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("OpenProxyGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.OpenProxyGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def OpenSecurityPolicy(self, request):
        """This API is used to enable security policies.

        :param request: Request instance for OpenSecurityPolicy.
        :type request: :class:`tencentcloud.gaap.v20180529.models.OpenSecurityPolicyRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.OpenSecurityPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("OpenSecurityPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.OpenSecurityPolicyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RemoveRealServers(self, request):
        """This API is used to delete the added origin server (server) IP or domain name.

        :param request: Request instance for RemoveRealServers.
        :type request: :class:`tencentcloud.gaap.v20180529.models.RemoveRealServersRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.RemoveRealServersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RemoveRealServers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RemoveRealServersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SetAuthentication(self, request):
        """This API (SetAuthentication) is used for the advanced authentication configuration of connections, including authentication methods and their certificates. If only supports connections of version 3.0.

        :param request: Request instance for SetAuthentication.
        :type request: :class:`tencentcloud.gaap.v20180529.models.SetAuthenticationRequest`
        :rtype: :class:`tencentcloud.gaap.v20180529.models.SetAuthenticationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SetAuthentication", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SetAuthenticationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)
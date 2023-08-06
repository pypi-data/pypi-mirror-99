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

from tencentcloud.common.abstract_model import AbstractModel


class AccessConfiguration(AbstractModel):
    """List of acceleration regions in a connection group, including acceleration regions and their bandwidth and concurrence configuration.

    """

    def __init__(self):
        """
        :param AccessRegion: Acceleration region.
        :type AccessRegion: str
        :param Bandwidth: Connection bandwidth upper limit in Mbps.
        :type Bandwidth: int
        :param Concurrent: Concurrent connection upper limit in 10,000 connections, which indicates the allowed number of concurrently online connections.
        :type Concurrent: int
        """
        self.AccessRegion = None
        self.Bandwidth = None
        self.Concurrent = None


    def _deserialize(self, params):
        self.AccessRegion = params.get("AccessRegion")
        self.Bandwidth = params.get("Bandwidth")
        self.Concurrent = params.get("Concurrent")


class AccessRegionDetial(AbstractModel):
    """Query the available acceleration region information, the corresponding bandwidth options, and the concurrence based on origin servers.

    """

    def __init__(self):
        """
        :param RegionId: Region ID
        :type RegionId: str
        :param RegionName: Region name in Chinese or English
        :type RegionName: str
        :param ConcurrentList: Value array of the available concurrence
        :type ConcurrentList: list of int
        :param BandwidthList: Value array of the available bandwidth
        :type BandwidthList: list of int
        """
        self.RegionId = None
        self.RegionName = None
        self.ConcurrentList = None
        self.BandwidthList = None


    def _deserialize(self, params):
        self.RegionId = params.get("RegionId")
        self.RegionName = params.get("RegionName")
        self.ConcurrentList = params.get("ConcurrentList")
        self.BandwidthList = params.get("BandwidthList")


class AccessRegionDomainConf(AbstractModel):
    """Domain name nearest access configuration

    """

    def __init__(self):
        """
        :param RegionId: Region ID.
        :type RegionId: str
        :param NationCountryInnerList: Region/country code for the nearest access, which can be obtained via the DescribeCountryAreaMapping API.
        :type NationCountryInnerList: list of str
        """
        self.RegionId = None
        self.NationCountryInnerList = None


    def _deserialize(self, params):
        self.RegionId = params.get("RegionId")
        self.NationCountryInnerList = params.get("NationCountryInnerList")


class AddRealServersRequest(AbstractModel):
    """AddRealServers request structure.

    """

    def __init__(self):
        """
        :param ProjectId: Project ID corresponding to origin server
        :type ProjectId: int
        :param RealServerIP: IP or domain name corresponding to origin server
        :type RealServerIP: list of str
        :param RealServerName: Origin server name
        :type RealServerName: str
        :param TagSet: Tag list
        :type TagSet: list of TagPair
        """
        self.ProjectId = None
        self.RealServerIP = None
        self.RealServerName = None
        self.TagSet = None


    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.RealServerIP = params.get("RealServerIP")
        self.RealServerName = params.get("RealServerName")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = TagPair()
                obj._deserialize(item)
                self.TagSet.append(obj)


class AddRealServersResponse(AbstractModel):
    """AddRealServers response structure.

    """

    def __init__(self):
        """
        :param RealServerSet: Origin server information list
        :type RealServerSet: list of NewRealServer
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RealServerSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("RealServerSet") is not None:
            self.RealServerSet = []
            for item in params.get("RealServerSet"):
                obj = NewRealServer()
                obj._deserialize(item)
                self.RealServerSet.append(obj)
        self.RequestId = params.get("RequestId")


class BandwidthPriceGradient(AbstractModel):
    """Bandwidth price gradient

    """

    def __init__(self):
        """
        :param BandwidthRange: Bandwidth range.
        :type BandwidthRange: list of int
        :param BandwidthUnitPrice: Bandwidth unit price within the bandwidth range. Unit: CNY/Mbps/day.
        :type BandwidthUnitPrice: float
        :param DiscountBandwidthUnitPrice: Discounted bandwidth price in CNY/Mbps/day.
        :type DiscountBandwidthUnitPrice: float
        """
        self.BandwidthRange = None
        self.BandwidthUnitPrice = None
        self.DiscountBandwidthUnitPrice = None


    def _deserialize(self, params):
        self.BandwidthRange = params.get("BandwidthRange")
        self.BandwidthUnitPrice = params.get("BandwidthUnitPrice")
        self.DiscountBandwidthUnitPrice = params.get("DiscountBandwidthUnitPrice")


class BindListenerRealServersRequest(AbstractModel):
    """BindListenerRealServers request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param RealServerBindSet: List of origin servers to be bound. If the origin server scheduling policy type of this listener is weighted round robin, you need to enter the `RealServerWeight`, i.e., the origin server weight. If this field is left empty or for other scheduling types, the default origin server weight is 1.
        :type RealServerBindSet: list of RealServerBindSetReq
        """
        self.ListenerId = None
        self.RealServerBindSet = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        if params.get("RealServerBindSet") is not None:
            self.RealServerBindSet = []
            for item in params.get("RealServerBindSet"):
                obj = RealServerBindSetReq()
                obj._deserialize(item)
                self.RealServerBindSet.append(obj)


class BindListenerRealServersResponse(AbstractModel):
    """BindListenerRealServers response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class BindRealServer(AbstractModel):
    """Bound origin server information

    """

    def __init__(self):
        """
        :param RealServerId: Origin server ID
        :type RealServerId: str
        :param RealServerIP: Origin server IP or domain name
        :type RealServerIP: str
        :param RealServerWeight: Origin server weight
        :type RealServerWeight: int
        :param RealServerStatus: Origin server health check status. Valid values:
0: normal;
1: exceptional.
If health check is not enabled, this status will always be normal.
Note: this field may return null, indicating that no valid values can be obtained.
        :type RealServerStatus: int
        :param RealServerPort: Origin server port number
Note: This field may return null, indicating that no valid values can be obtained.
        :type RealServerPort: int
        :param DownIPList: If the origin server is a domain name, the domain name will be resolved to one or multiple IPs. This field indicates the exceptional IP list.
        :type DownIPList: list of str
        """
        self.RealServerId = None
        self.RealServerIP = None
        self.RealServerWeight = None
        self.RealServerStatus = None
        self.RealServerPort = None
        self.DownIPList = None


    def _deserialize(self, params):
        self.RealServerId = params.get("RealServerId")
        self.RealServerIP = params.get("RealServerIP")
        self.RealServerWeight = params.get("RealServerWeight")
        self.RealServerStatus = params.get("RealServerStatus")
        self.RealServerPort = params.get("RealServerPort")
        self.DownIPList = params.get("DownIPList")


class BindRealServerInfo(AbstractModel):
    """The returned value of the added origin server information

    """

    def __init__(self):
        """
        :param RealServerIP: Origin server IP or domain name
        :type RealServerIP: str
        :param RealServerId: Origin server ID
        :type RealServerId: str
        :param RealServerName: Origin server name
        :type RealServerName: str
        :param ProjectId: Project ID
        :type ProjectId: int
        :param TagSet: Tag list
Note: This field may return null, indicating that no valid values can be obtained.
        :type TagSet: list of TagPair
        """
        self.RealServerIP = None
        self.RealServerId = None
        self.RealServerName = None
        self.ProjectId = None
        self.TagSet = None


    def _deserialize(self, params):
        self.RealServerIP = params.get("RealServerIP")
        self.RealServerId = params.get("RealServerId")
        self.RealServerName = params.get("RealServerName")
        self.ProjectId = params.get("ProjectId")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = TagPair()
                obj._deserialize(item)
                self.TagSet.append(obj)


class BindRuleRealServersRequest(AbstractModel):
    """BindRuleRealServers request structure.

    """

    def __init__(self):
        """
        :param RuleId: Forwarding rule ID
        :type RuleId: str
        :param RealServerBindSet: An information list of the origin servers to bind.
If there are origin servers bound already, they will be replaced by this new origin server list.
If this field is empty, it indicates unbinding all origin servers of this rule.
If the origin server scheduling policy type of this rule is weighted round robin, you need to enter `RealServerWeight`, i.e., the origin server weight. If this field is left empty or for other scheduling types, the default origin server weight is 1.
        :type RealServerBindSet: list of RealServerBindSetReq
        """
        self.RuleId = None
        self.RealServerBindSet = None


    def _deserialize(self, params):
        self.RuleId = params.get("RuleId")
        if params.get("RealServerBindSet") is not None:
            self.RealServerBindSet = []
            for item in params.get("RealServerBindSet"):
                obj = RealServerBindSetReq()
                obj._deserialize(item)
                self.RealServerBindSet.append(obj)


class BindRuleRealServersResponse(AbstractModel):
    """BindRuleRealServers response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Certificate(AbstractModel):
    """Server Certificate

    """

    def __init__(self):
        """
        :param CertificateId: Certificate ID
        :type CertificateId: str
        :param CertificateName: Certificate name; It's an old parameter, please switch to CertificateAlias.
        :type CertificateName: str
        :param CertificateType: Certificate type.
        :type CertificateType: int
        :param CertificateAlias: Certificate name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type CertificateAlias: str
        :param CreateTime: Certificate creation time in the format of UNIX timestamp, indicating the number of seconds that have elapsed since January 1, 1970 (midnight in UTC/GMT).
        :type CreateTime: int
        :param BeginTime: Certificate effective time in the format of UNIX timestamp, indicating the number of seconds that have elapsed since January 1, 1970 (midnight in UTC/GMT).
Note: This field may return null, indicating that no valid values can be obtained.
        :type BeginTime: int
        :param EndTime: Certificate expiration time in the format of UNIX timestamp, indicating the number of seconds that have elapsed since January 1, 1970 (midnight in UTC/GMT).
Note: This field may return null, indicating that no valid values can be obtained.
        :type EndTime: int
        :param IssuerCN: Common name of the certificate issuer.
Note: This field may return null, indicating that no valid values can be obtained.
        :type IssuerCN: str
        :param SubjectCN: Common name of the certificate subject.
Note: This field may return null, indicating that no valid values can be obtained.
        :type SubjectCN: str
        """
        self.CertificateId = None
        self.CertificateName = None
        self.CertificateType = None
        self.CertificateAlias = None
        self.CreateTime = None
        self.BeginTime = None
        self.EndTime = None
        self.IssuerCN = None
        self.SubjectCN = None


    def _deserialize(self, params):
        self.CertificateId = params.get("CertificateId")
        self.CertificateName = params.get("CertificateName")
        self.CertificateType = params.get("CertificateType")
        self.CertificateAlias = params.get("CertificateAlias")
        self.CreateTime = params.get("CreateTime")
        self.BeginTime = params.get("BeginTime")
        self.EndTime = params.get("EndTime")
        self.IssuerCN = params.get("IssuerCN")
        self.SubjectCN = params.get("SubjectCN")


class CertificateAliasInfo(AbstractModel):
    """Certificate alias information.

    """

    def __init__(self):
        """
        :param CertificateId: Certificate ID.
        :type CertificateId: str
        :param CertificateAlias: Certificate alias.
        :type CertificateAlias: str
        """
        self.CertificateId = None
        self.CertificateAlias = None


    def _deserialize(self, params):
        self.CertificateId = params.get("CertificateId")
        self.CertificateAlias = params.get("CertificateAlias")


class CertificateDetail(AbstractModel):
    """Certificate details, including the certificate ID, name, type, content, and key content.

    """

    def __init__(self):
        """
        :param CertificateId: Certificate ID.
        :type CertificateId: str
        :param CertificateType: Certificate type.
        :type CertificateType: int
        :param CertificateAlias: Certificate name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type CertificateAlias: str
        :param CertificateContent: Certificate content.
        :type CertificateContent: str
        :param CertificateKey: Key content. This field will be returned if the certificate type is the SSL certificate.
Note: This field may return null, indicating that no valid values can be obtained.
        :type CertificateKey: str
        :param CreateTime: Creation time in the format of UNIX timestamp, indicating the number of seconds that have elapsed since January 1, 1970 (midnight in UTC/GMT).
Note: This field may return null, indicating that no valid values can be obtained.
        :type CreateTime: int
        :param BeginTime: Certificate effective time in the format of UNIX timestamp, indicating the number of seconds that have elapsed since January 1, 1970 (midnight in UTC/GMT).
Note: This field may return null, indicating that no valid values can be obtained.
        :type BeginTime: int
        :param EndTime: Certificate expiration time in the format of UNIX timestamp, indicating the number of seconds that have elapsed since January 1, 1970 (midnight in UTC/GMT).
Note: This field may return null, indicating that no valid values can be obtained.
        :type EndTime: int
        :param IssuerCN: Common name of the certificate's issuer.
Note: This field may return null, indicating that no valid values can be obtained.
        :type IssuerCN: str
        :param SubjectCN: Common name of the certificate subject.
Note: This field may return null, indicating that no valid values can be obtained.
        :type SubjectCN: str
        """
        self.CertificateId = None
        self.CertificateType = None
        self.CertificateAlias = None
        self.CertificateContent = None
        self.CertificateKey = None
        self.CreateTime = None
        self.BeginTime = None
        self.EndTime = None
        self.IssuerCN = None
        self.SubjectCN = None


    def _deserialize(self, params):
        self.CertificateId = params.get("CertificateId")
        self.CertificateType = params.get("CertificateType")
        self.CertificateAlias = params.get("CertificateAlias")
        self.CertificateContent = params.get("CertificateContent")
        self.CertificateKey = params.get("CertificateKey")
        self.CreateTime = params.get("CreateTime")
        self.BeginTime = params.get("BeginTime")
        self.EndTime = params.get("EndTime")
        self.IssuerCN = params.get("IssuerCN")
        self.SubjectCN = params.get("SubjectCN")


class CheckProxyCreateRequest(AbstractModel):
    """CheckProxyCreate request structure.

    """

    def __init__(self):
        """
        :param AccessRegion: Access (acceleration) region of the connection. The value can be obtained via the DescribeAccessRegionsByDestRegion API.
        :type AccessRegion: str
        :param RealServerRegion: Origin server region of the connection. The value can be obtained via the DescribeDestRegions API.
        :type RealServerRegion: str
        :param Bandwidth: Connection bandwidth cap. Unit: Mbps.
        :type Bandwidth: int
        :param Concurrent: Connection concurrence cap, which indicates the maximum number of simultaneous online connections. Unit: 10,000 connections.
        :type Concurrent: int
        :param GroupId: Connection group ID that needs to be entered when a connection is created in a connection group
        :type GroupId: str
        """
        self.AccessRegion = None
        self.RealServerRegion = None
        self.Bandwidth = None
        self.Concurrent = None
        self.GroupId = None


    def _deserialize(self, params):
        self.AccessRegion = params.get("AccessRegion")
        self.RealServerRegion = params.get("RealServerRegion")
        self.Bandwidth = params.get("Bandwidth")
        self.Concurrent = params.get("Concurrent")
        self.GroupId = params.get("GroupId")


class CheckProxyCreateResponse(AbstractModel):
    """CheckProxyCreate response structure.

    """

    def __init__(self):
        """
        :param CheckFlag: Queries whether a connection with the specified configuration can be created. 1: yes; 0: no.
        :type CheckFlag: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.CheckFlag = None
        self.RequestId = None


    def _deserialize(self, params):
        self.CheckFlag = params.get("CheckFlag")
        self.RequestId = params.get("RequestId")


class CloseProxiesRequest(AbstractModel):
    """CloseProxies request structure.

    """

    def __init__(self):
        """
        :param InstanceIds: Connection instance ID; It's an old parameter, please switch to ProxyIds.
        :type InstanceIds: list of str
        :param ClientToken: A string used to ensure the idempotency of the request, which is generated by the user and must be unique to each request. The maximum length is 64 ASCII characters. If this parameter is not specified, the idempotency of the request cannot be guaranteed.
For more information, please see How to Ensure Idempotence.
        :type ClientToken: str
        :param ProxyIds: Connection instance ID; It's a new parameter.
        :type ProxyIds: list of str
        """
        self.InstanceIds = None
        self.ClientToken = None
        self.ProxyIds = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.ClientToken = params.get("ClientToken")
        self.ProxyIds = params.get("ProxyIds")


class CloseProxiesResponse(AbstractModel):
    """CloseProxies response structure.

    """

    def __init__(self):
        """
        :param InvalidStatusInstanceSet: Only the running connection instance ID lists can be enabled.
        :type InvalidStatusInstanceSet: list of str
        :param OperationFailedInstanceSet: ID list of connection instances failed to be enabled.
        :type OperationFailedInstanceSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InvalidStatusInstanceSet = None
        self.OperationFailedInstanceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InvalidStatusInstanceSet = params.get("InvalidStatusInstanceSet")
        self.OperationFailedInstanceSet = params.get("OperationFailedInstanceSet")
        self.RequestId = params.get("RequestId")


class CloseProxyGroupRequest(AbstractModel):
    """CloseProxyGroup request structure.

    """

    def __init__(self):
        """
        :param GroupId: Connection group instance ID.
        :type GroupId: str
        """
        self.GroupId = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")


class CloseProxyGroupResponse(AbstractModel):
    """CloseProxyGroup response structure.

    """

    def __init__(self):
        """
        :param InvalidStatusInstanceSet: List of IDs of the connection instances that are not running, which cannot be enabled.
        :type InvalidStatusInstanceSet: list of str
        :param OperationFailedInstanceSet: List of IDs of the connection instances failed to be enabled.
        :type OperationFailedInstanceSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InvalidStatusInstanceSet = None
        self.OperationFailedInstanceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InvalidStatusInstanceSet = params.get("InvalidStatusInstanceSet")
        self.OperationFailedInstanceSet = params.get("OperationFailedInstanceSet")
        self.RequestId = params.get("RequestId")


class CloseSecurityPolicyRequest(AbstractModel):
    """CloseSecurityPolicy request structure.

    """

    def __init__(self):
        """
        :param ProxyId: Connection ID
        :type ProxyId: str
        :param PolicyId: Security group policy ID
        :type PolicyId: str
        """
        self.ProxyId = None
        self.PolicyId = None


    def _deserialize(self, params):
        self.ProxyId = params.get("ProxyId")
        self.PolicyId = params.get("PolicyId")


class CloseSecurityPolicyResponse(AbstractModel):
    """CloseSecurityPolicy response structure.

    """

    def __init__(self):
        """
        :param TaskId: Async Process ID. Using DescribeAsyncTaskStatus to query process and status.
        :type TaskId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class CountryAreaMap(AbstractModel):
    """Country/region code mapping (name and code)

    """

    def __init__(self):
        """
        :param NationCountryName: Country name.
        :type NationCountryName: str
        :param NationCountryInnerCode: Country code.
        :type NationCountryInnerCode: str
        :param GeographicalZoneName: Region name.
        :type GeographicalZoneName: str
        :param GeographicalZoneInnerCode: Region code.
        :type GeographicalZoneInnerCode: str
        :param ContinentName: Continent name.
        :type ContinentName: str
        :param ContinentInnerCode: Continent code.
        :type ContinentInnerCode: str
        """
        self.NationCountryName = None
        self.NationCountryInnerCode = None
        self.GeographicalZoneName = None
        self.GeographicalZoneInnerCode = None
        self.ContinentName = None
        self.ContinentInnerCode = None


    def _deserialize(self, params):
        self.NationCountryName = params.get("NationCountryName")
        self.NationCountryInnerCode = params.get("NationCountryInnerCode")
        self.GeographicalZoneName = params.get("GeographicalZoneName")
        self.GeographicalZoneInnerCode = params.get("GeographicalZoneInnerCode")
        self.ContinentName = params.get("ContinentName")
        self.ContinentInnerCode = params.get("ContinentInnerCode")


class CreateCertificateRequest(AbstractModel):
    """CreateCertificate request structure.

    """

    def __init__(self):
        """
        :param CertificateType: Certificate type. Where:
0: basic authentication configuration;
1: indicates client CA certificate;
2: server SSL certificate;
3: origin server CA certificate;
4: connection SSL certificate.
        :type CertificateType: int
        :param CertificateContent: Certificate content. URL encoding. Where:
If the certificate type is basic authentication, enter username/password pair for this parameter. Format: 'username:password', for example, root:FSGdT. The password is `htpasswd` or `openssl`, for example, openssl passwd -crypt 123456.
When the certificate type is CA/SSL certificate, enter the certificate content for this parameter in the format of `pem`.
        :type CertificateContent: str
        :param CertificateAlias: Certificate name
        :type CertificateAlias: str
        :param CertificateKey: Key content. URL encoding. This parameter is required only when the certificate type is SSL certificate. The format is `pem`.
        :type CertificateKey: str
        """
        self.CertificateType = None
        self.CertificateContent = None
        self.CertificateAlias = None
        self.CertificateKey = None


    def _deserialize(self, params):
        self.CertificateType = params.get("CertificateType")
        self.CertificateContent = params.get("CertificateContent")
        self.CertificateAlias = params.get("CertificateAlias")
        self.CertificateKey = params.get("CertificateKey")


class CreateCertificateResponse(AbstractModel):
    """CreateCertificate response structure.

    """

    def __init__(self):
        """
        :param CertificateId: Certificate ID
        :type CertificateId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.CertificateId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.CertificateId = params.get("CertificateId")
        self.RequestId = params.get("RequestId")


class CreateDomainErrorPageInfoRequest(AbstractModel):
    """CreateDomainErrorPageInfo request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param Domain: Domain name
        :type Domain: str
        :param ErrorNos: Original error code
        :type ErrorNos: list of int
        :param Body: New response packet
        :type Body: str
        :param NewErrorNo: New error code
        :type NewErrorNo: int
        :param ClearHeaders: Response header to be deleted
        :type ClearHeaders: list of str
        :param SetHeaders: Response header to be set
        :type SetHeaders: list of HttpHeaderParam
        """
        self.ListenerId = None
        self.Domain = None
        self.ErrorNos = None
        self.Body = None
        self.NewErrorNo = None
        self.ClearHeaders = None
        self.SetHeaders = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.Domain = params.get("Domain")
        self.ErrorNos = params.get("ErrorNos")
        self.Body = params.get("Body")
        self.NewErrorNo = params.get("NewErrorNo")
        self.ClearHeaders = params.get("ClearHeaders")
        if params.get("SetHeaders") is not None:
            self.SetHeaders = []
            for item in params.get("SetHeaders"):
                obj = HttpHeaderParam()
                obj._deserialize(item)
                self.SetHeaders.append(obj)


class CreateDomainErrorPageInfoResponse(AbstractModel):
    """CreateDomainErrorPageInfo response structure.

    """

    def __init__(self):
        """
        :param ErrorPageId: Configuration ID of a custom error response
        :type ErrorPageId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ErrorPageId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ErrorPageId = params.get("ErrorPageId")
        self.RequestId = params.get("RequestId")


class CreateDomainRequest(AbstractModel):
    """CreateDomain request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID.
        :type ListenerId: str
        :param Domain: Domain name to be created. Each listener supports up to 100 domain names.
        :type Domain: str
        :param CertificateId: Server certificate, which is used for the HTTPS interaction between client and GAAP.
        :type CertificateId: str
        :param ClientCertificateId: Client CA certificate, which is used for the HTTPS interaction between client and GAAP.
This field is required only when the mutual authentication method is adopted.
        :type ClientCertificateId: str
        :param PolyClientCertificateIds: Client CA certificate, which is used for the HTTPS interaction between the client and GAAP.
This field or the `ClientCertificateId` field is required for mutual authentication only.
        :type PolyClientCertificateIds: list of str
        """
        self.ListenerId = None
        self.Domain = None
        self.CertificateId = None
        self.ClientCertificateId = None
        self.PolyClientCertificateIds = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.Domain = params.get("Domain")
        self.CertificateId = params.get("CertificateId")
        self.ClientCertificateId = params.get("ClientCertificateId")
        self.PolyClientCertificateIds = params.get("PolyClientCertificateIds")


class CreateDomainResponse(AbstractModel):
    """CreateDomain response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateHTTPListenerRequest(AbstractModel):
    """CreateHTTPListener request structure.

    """

    def __init__(self):
        """
        :param ListenerName: Listener name
        :type ListenerName: str
        :param Port: Listener port, which is based on the listeners of same transport layer protocol (TCP or UDP). The port must be unique.
        :type Port: int
        :param ProxyId: Connection ID, which cannot be set together with `GroupId` at the same time. A listener will be created for the corresponding connection.
        :type ProxyId: str
        :param GroupId: Connection group ID, which cannot be set together with `ProxyId` at the same time. A listener will be created for the corresponding connection group.
        :type GroupId: str
        """
        self.ListenerName = None
        self.Port = None
        self.ProxyId = None
        self.GroupId = None


    def _deserialize(self, params):
        self.ListenerName = params.get("ListenerName")
        self.Port = params.get("Port")
        self.ProxyId = params.get("ProxyId")
        self.GroupId = params.get("GroupId")


class CreateHTTPListenerResponse(AbstractModel):
    """CreateHTTPListener response structure.

    """

    def __init__(self):
        """
        :param ListenerId: Created listener ID
        :type ListenerId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ListenerId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.RequestId = params.get("RequestId")


class CreateHTTPSListenerRequest(AbstractModel):
    """CreateHTTPSListener request structure.

    """

    def __init__(self):
        """
        :param ListenerName: Listener name
        :type ListenerName: str
        :param Port: Listener port, which is based on the listeners of same transport layer protocol (TCP or UDP). The port must be unique.
        :type Port: int
        :param CertificateId: Server certificate ID
        :type CertificateId: str
        :param ForwardProtocol: Protocol types of the forwarding from acceleration connection to origin server: HTTP | HTTPS
        :type ForwardProtocol: str
        :param ProxyId: Connection ID, which cannot be set together with `GroupId` at the same time. A listener will be created for the corresponding connection.
        :type ProxyId: str
        :param AuthType: Authentication type, where:
0: one-way authentication;
1: mutual authentication.
The one-way authentication is used by default.
        :type AuthType: int
        :param ClientCertificateId: Client CA certificate ID, which is required only when the mutual authentication is adopted.
        :type ClientCertificateId: str
        :param PolyClientCertificateIds: IDs of multiple new client CA certificates. This field or the `ClientCertificateId` field is required for mutual authentication only.
        :type PolyClientCertificateIds: list of str
        :param GroupId: Connection group ID, which cannot be set together with `ProxyId` at the same time. A listener will be created for the corresponding connection group.
        :type GroupId: str
        """
        self.ListenerName = None
        self.Port = None
        self.CertificateId = None
        self.ForwardProtocol = None
        self.ProxyId = None
        self.AuthType = None
        self.ClientCertificateId = None
        self.PolyClientCertificateIds = None
        self.GroupId = None


    def _deserialize(self, params):
        self.ListenerName = params.get("ListenerName")
        self.Port = params.get("Port")
        self.CertificateId = params.get("CertificateId")
        self.ForwardProtocol = params.get("ForwardProtocol")
        self.ProxyId = params.get("ProxyId")
        self.AuthType = params.get("AuthType")
        self.ClientCertificateId = params.get("ClientCertificateId")
        self.PolyClientCertificateIds = params.get("PolyClientCertificateIds")
        self.GroupId = params.get("GroupId")


class CreateHTTPSListenerResponse(AbstractModel):
    """CreateHTTPSListener response structure.

    """

    def __init__(self):
        """
        :param ListenerId: Created listener ID
        :type ListenerId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ListenerId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.RequestId = params.get("RequestId")


class CreateProxyGroupDomainRequest(AbstractModel):
    """CreateProxyGroupDomain request structure.

    """

    def __init__(self):
        """
        :param GroupId: Connection group ID of the domain name to be enabled.
        :type GroupId: str
        """
        self.GroupId = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")


class CreateProxyGroupDomainResponse(AbstractModel):
    """CreateProxyGroupDomain response structure.

    """

    def __init__(self):
        """
        :param GroupId: Connection group ID.
        :type GroupId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.GroupId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")
        self.RequestId = params.get("RequestId")


class CreateProxyGroupRequest(AbstractModel):
    """CreateProxyGroup request structure.

    """

    def __init__(self):
        """
        :param ProjectId: Project ID of connection group
        :type ProjectId: int
        :param GroupName: Alias of connection group
        :type GroupName: str
        :param RealServerRegion: Origin server region; Reference API: DescribeDestRegions; It returnes the `RegionId` of the parameter `RegionDetail`.
        :type RealServerRegion: str
        :param TagSet: Tag list
        :type TagSet: list of TagPair
        :param AccessRegionSet: List of acceleration regions, including their names, bandwidth, and concurrence configuration.
        :type AccessRegionSet: list of AccessConfiguration
        """
        self.ProjectId = None
        self.GroupName = None
        self.RealServerRegion = None
        self.TagSet = None
        self.AccessRegionSet = None


    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.GroupName = params.get("GroupName")
        self.RealServerRegion = params.get("RealServerRegion")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = TagPair()
                obj._deserialize(item)
                self.TagSet.append(obj)
        if params.get("AccessRegionSet") is not None:
            self.AccessRegionSet = []
            for item in params.get("AccessRegionSet"):
                obj = AccessConfiguration()
                obj._deserialize(item)
                self.AccessRegionSet.append(obj)


class CreateProxyGroupResponse(AbstractModel):
    """CreateProxyGroup response structure.

    """

    def __init__(self):
        """
        :param GroupId: Connection Group ID
        :type GroupId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.GroupId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")
        self.RequestId = params.get("RequestId")


class CreateProxyRequest(AbstractModel):
    """CreateProxy request structure.

    """

    def __init__(self):
        """
        :param ProjectId: Project ID of connection.
        :type ProjectId: int
        :param ProxyName: Connection name.
        :type ProxyName: str
        :param AccessRegion: Access region.
        :type AccessRegion: str
        :param Bandwidth: Connection bandwidth cap. Unit: Mbps.
        :type Bandwidth: int
        :param Concurrent: Connection concurrence cap, which indicates the maximum number of simultaneous online connections. Unit: 10,000 connections.
        :type Concurrent: int
        :param RealServerRegion: Origin server region. If GroupId exists, the origin server region is the one of connection group, and this field is not required. If GroupId does not exist, this field is reuqired.
        :type RealServerRegion: str
        :param ClientToken: A string used to ensure the idempotency of the request, which is generated by the user and must be unique to each request. The maximum length is 64 ASCII characters. If this parameter is not specified, the idempotency of the request cannot be guaranteed.
For more information, please see How to Ensure Idempotence.
        :type ClientToken: str
        :param GroupId: Connection group ID. This parameter is required when the connection is created in the connection group. Otherwise, this field is ignored.
        :type GroupId: str
        :param TagSet: List of tags to be added for connection.
        :type TagSet: list of TagPair
        :param ClonedProxyId: ID of the replicated connection. Only a running connection can be replicated.
The connection is to be replicated if this parameter is set.
        :type ClonedProxyId: str
        :param BillingType: Billing mode (0: bill-by-bandwidth, 1: bill-by-traffic. Default value: bill-by-bandwidth)
        :type BillingType: int
        """
        self.ProjectId = None
        self.ProxyName = None
        self.AccessRegion = None
        self.Bandwidth = None
        self.Concurrent = None
        self.RealServerRegion = None
        self.ClientToken = None
        self.GroupId = None
        self.TagSet = None
        self.ClonedProxyId = None
        self.BillingType = None


    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.ProxyName = params.get("ProxyName")
        self.AccessRegion = params.get("AccessRegion")
        self.Bandwidth = params.get("Bandwidth")
        self.Concurrent = params.get("Concurrent")
        self.RealServerRegion = params.get("RealServerRegion")
        self.ClientToken = params.get("ClientToken")
        self.GroupId = params.get("GroupId")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = TagPair()
                obj._deserialize(item)
                self.TagSet.append(obj)
        self.ClonedProxyId = params.get("ClonedProxyId")
        self.BillingType = params.get("BillingType")


class CreateProxyResponse(AbstractModel):
    """CreateProxy response structure.

    """

    def __init__(self):
        """
        :param InstanceId: Instance ID of connection.
        :type InstanceId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class CreateRuleRequest(AbstractModel):
    """CreateRule request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Layer-7 listener ID
        :type ListenerId: str
        :param Domain: Domain name of the forwarding rule
        :type Domain: str
        :param Path: Path of the forwarding rule
        :type Path: str
        :param RealServerType: The origin server type of the forwarding rule, which supports IP and DOMAIN types.
        :type RealServerType: str
        :param Scheduler: Forwarding rules of origin server, which supports round robin (rr), weighted round robin (wrr), and least connections (lc).
        :type Scheduler: str
        :param HealthCheck: Whether the health check is enabled for rules. 1: enabled; 0: disabled.
        :type HealthCheck: int
        :param CheckParams: Parameters related to origin server health check
        :type CheckParams: :class:`tencentcloud.gaap.v20180529.models.RuleCheckParams`
        :param ForwardProtocol: Protocol types of the forwarding from acceleration connection to origin server, which supports HTTP or HTTPS.
If this field is not passed in, it indicates that the ForwardProtocol of the corresponding listener will be used.
        :type ForwardProtocol: str
        :param ForwardHost: Remote host to which the acceleration connection forwards. If this parameter is not specified, the default host will be used, i.e., the host with which the client initiates HTTP requests.
        :type ForwardHost: str
        """
        self.ListenerId = None
        self.Domain = None
        self.Path = None
        self.RealServerType = None
        self.Scheduler = None
        self.HealthCheck = None
        self.CheckParams = None
        self.ForwardProtocol = None
        self.ForwardHost = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.Domain = params.get("Domain")
        self.Path = params.get("Path")
        self.RealServerType = params.get("RealServerType")
        self.Scheduler = params.get("Scheduler")
        self.HealthCheck = params.get("HealthCheck")
        if params.get("CheckParams") is not None:
            self.CheckParams = RuleCheckParams()
            self.CheckParams._deserialize(params.get("CheckParams"))
        self.ForwardProtocol = params.get("ForwardProtocol")
        self.ForwardHost = params.get("ForwardHost")


class CreateRuleResponse(AbstractModel):
    """CreateRule response structure.

    """

    def __init__(self):
        """
        :param RuleId: The ID of the successfully created forwarding rule
        :type RuleId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RuleId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.RuleId = params.get("RuleId")
        self.RequestId = params.get("RequestId")


class CreateSecurityPolicyRequest(AbstractModel):
    """CreateSecurityPolicy request structure.

    """

    def __init__(self):
        """
        :param DefaultAction: Default policy: ACCEPT or DROP
        :type DefaultAction: str
        :param ProxyId: Acceleration connection ID
        :type ProxyId: str
        :param GroupId: Connection group ID
        :type GroupId: str
        """
        self.DefaultAction = None
        self.ProxyId = None
        self.GroupId = None


    def _deserialize(self, params):
        self.DefaultAction = params.get("DefaultAction")
        self.ProxyId = params.get("ProxyId")
        self.GroupId = params.get("GroupId")


class CreateSecurityPolicyResponse(AbstractModel):
    """CreateSecurityPolicy response structure.

    """

    def __init__(self):
        """
        :param PolicyId: Security policy ID
        :type PolicyId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.PolicyId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.PolicyId = params.get("PolicyId")
        self.RequestId = params.get("RequestId")


class CreateSecurityRulesRequest(AbstractModel):
    """CreateSecurityRules request structure.

    """

    def __init__(self):
        """
        :param PolicyId: Security policy ID
        :type PolicyId: str
        :param RuleList: List of access rules
        :type RuleList: list of SecurityPolicyRuleIn
        """
        self.PolicyId = None
        self.RuleList = None


    def _deserialize(self, params):
        self.PolicyId = params.get("PolicyId")
        if params.get("RuleList") is not None:
            self.RuleList = []
            for item in params.get("RuleList"):
                obj = SecurityPolicyRuleIn()
                obj._deserialize(item)
                self.RuleList.append(obj)


class CreateSecurityRulesResponse(AbstractModel):
    """CreateSecurityRules response structure.

    """

    def __init__(self):
        """
        :param RuleIdList: List of rule IDs
        :type RuleIdList: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RuleIdList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.RuleIdList = params.get("RuleIdList")
        self.RequestId = params.get("RequestId")


class CreateTCPListenersRequest(AbstractModel):
    """CreateTCPListeners request structure.

    """

    def __init__(self):
        """
        :param ListenerName: Listener name.
        :type ListenerName: str
        :param Ports: List of listener ports.
        :type Ports: list of int non-negative
        :param Scheduler: Origin server scheduling policy of listeners, which supports round robin (rr), weighted round robin (wrr), and least connections (lc).
        :type Scheduler: str
        :param HealthCheck: Whether origin server has the health check enabled. 1: enabled; 0: disabled. UDP listeners do not support health check.
        :type HealthCheck: int
        :param RealServerType: The origin server type of listeners, supporting IP or DOMAIN type. The DOMAIN origin servers do not support the weighted round robin.
        :type RealServerType: str
        :param ProxyId: Connection ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type ProxyId: str
        :param GroupId: Connection group ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type GroupId: str
        :param DelayLoop: Time interval of origin server health check (unit: seconds). Value range: [5, 300].
        :type DelayLoop: int
        :param ConnectTimeout: Response timeout of origin server health check (unit: seconds). Value range: [2, 60]. The timeout value shall be less than the time interval for health check DelayLoop.
        :type ConnectTimeout: int
        :param RealServerPorts: List of origin server ports, which only supports the listeners of version 1.0 and connection group.
        :type RealServerPorts: list of int non-negative
        :param ClientIPMethod: Listener methods of getting client IPs. 0: TOA; 1: Proxy Protocol.
        :type ClientIPMethod: int
        """
        self.ListenerName = None
        self.Ports = None
        self.Scheduler = None
        self.HealthCheck = None
        self.RealServerType = None
        self.ProxyId = None
        self.GroupId = None
        self.DelayLoop = None
        self.ConnectTimeout = None
        self.RealServerPorts = None
        self.ClientIPMethod = None


    def _deserialize(self, params):
        self.ListenerName = params.get("ListenerName")
        self.Ports = params.get("Ports")
        self.Scheduler = params.get("Scheduler")
        self.HealthCheck = params.get("HealthCheck")
        self.RealServerType = params.get("RealServerType")
        self.ProxyId = params.get("ProxyId")
        self.GroupId = params.get("GroupId")
        self.DelayLoop = params.get("DelayLoop")
        self.ConnectTimeout = params.get("ConnectTimeout")
        self.RealServerPorts = params.get("RealServerPorts")
        self.ClientIPMethod = params.get("ClientIPMethod")


class CreateTCPListenersResponse(AbstractModel):
    """CreateTCPListeners response structure.

    """

    def __init__(self):
        """
        :param ListenerIds: Returns the listener ID
        :type ListenerIds: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ListenerIds = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ListenerIds = params.get("ListenerIds")
        self.RequestId = params.get("RequestId")


class CreateUDPListenersRequest(AbstractModel):
    """CreateUDPListeners request structure.

    """

    def __init__(self):
        """
        :param ListenerName: Listener name
        :type ListenerName: str
        :param Ports: List of listener ports
        :type Ports: list of int non-negative
        :param Scheduler: Origin server scheduling policy of listeners, which supports round robin (rr), weighted round robin (wrr), and least connections (lc).
        :type Scheduler: str
        :param RealServerType: Origin server type of listeners, which supports IP or DOMAIN type.
        :type RealServerType: str
        :param ProxyId: Connection ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type ProxyId: str
        :param GroupId: Connection group ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type GroupId: str
        :param RealServerPorts: List of origin server ports, which only supports the listeners of version 1.0 and connection group.
        :type RealServerPorts: list of int non-negative
        """
        self.ListenerName = None
        self.Ports = None
        self.Scheduler = None
        self.RealServerType = None
        self.ProxyId = None
        self.GroupId = None
        self.RealServerPorts = None


    def _deserialize(self, params):
        self.ListenerName = params.get("ListenerName")
        self.Ports = params.get("Ports")
        self.Scheduler = params.get("Scheduler")
        self.RealServerType = params.get("RealServerType")
        self.ProxyId = params.get("ProxyId")
        self.GroupId = params.get("GroupId")
        self.RealServerPorts = params.get("RealServerPorts")


class CreateUDPListenersResponse(AbstractModel):
    """CreateUDPListeners response structure.

    """

    def __init__(self):
        """
        :param ListenerIds: Returns the listener ID
        :type ListenerIds: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ListenerIds = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ListenerIds = params.get("ListenerIds")
        self.RequestId = params.get("RequestId")


class DeleteCertificateRequest(AbstractModel):
    """DeleteCertificate request structure.

    """

    def __init__(self):
        """
        :param CertificateId: ID of the certificate to be deleted.
        :type CertificateId: str
        """
        self.CertificateId = None


    def _deserialize(self, params):
        self.CertificateId = params.get("CertificateId")


class DeleteCertificateResponse(AbstractModel):
    """DeleteCertificate response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteDomainErrorPageInfoRequest(AbstractModel):
    """DeleteDomainErrorPageInfo request structure.

    """

    def __init__(self):
        """
        :param ErrorPageId: Unique ID of a custom error page. For more information, please see the response to CreateDomainErrorPageInfo.
        :type ErrorPageId: str
        """
        self.ErrorPageId = None


    def _deserialize(self, params):
        self.ErrorPageId = params.get("ErrorPageId")


class DeleteDomainErrorPageInfoResponse(AbstractModel):
    """DeleteDomainErrorPageInfo response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteDomainRequest(AbstractModel):
    """DeleteDomain request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param Domain: Domain name to be deleted
        :type Domain: str
        :param Force: Whether to make a forced deletion of forwarding rules that have been bound to origin servers. 0: no; 1: yes.
When not making a forced deletion, if there are rules bound to origin servers, they will not be deleted.
        :type Force: int
        """
        self.ListenerId = None
        self.Domain = None
        self.Force = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.Domain = params.get("Domain")
        self.Force = params.get("Force")


class DeleteDomainResponse(AbstractModel):
    """DeleteDomain response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteListenersRequest(AbstractModel):
    """DeleteListeners request structure.

    """

    def __init__(self):
        """
        :param ListenerIds: ID list of listeners to be deleted
        :type ListenerIds: list of str
        :param Force: Whether to allow a forced deletion of listeners that have been bound to origin servers. 1: allowed; 0: not allow.
        :type Force: int
        :param GroupId: Connection group ID; Either this parameter or `GroupId` must be set, but you cannot set both.
        :type GroupId: str
        :param ProxyId: Connection ID; Either this parameter or `GroupId` must be set, but you cannot set both.
        :type ProxyId: str
        """
        self.ListenerIds = None
        self.Force = None
        self.GroupId = None
        self.ProxyId = None


    def _deserialize(self, params):
        self.ListenerIds = params.get("ListenerIds")
        self.Force = params.get("Force")
        self.GroupId = params.get("GroupId")
        self.ProxyId = params.get("ProxyId")


class DeleteListenersResponse(AbstractModel):
    """DeleteListeners response structure.

    """

    def __init__(self):
        """
        :param OperationFailedListenerSet: ID list of listeners failed to be deleted
        :type OperationFailedListenerSet: list of str
        :param OperationSucceedListenerSet: ID list of listeners deleted successfully
        :type OperationSucceedListenerSet: list of str
        :param InvalidStatusListenerSet: ID list of invalid listeners. For example: the listener does not exist, or the instance corresponding to the listener does not match.
        :type InvalidStatusListenerSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.OperationFailedListenerSet = None
        self.OperationSucceedListenerSet = None
        self.InvalidStatusListenerSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.OperationFailedListenerSet = params.get("OperationFailedListenerSet")
        self.OperationSucceedListenerSet = params.get("OperationSucceedListenerSet")
        self.InvalidStatusListenerSet = params.get("InvalidStatusListenerSet")
        self.RequestId = params.get("RequestId")


class DeleteProxyGroupRequest(AbstractModel):
    """DeleteProxyGroup request structure.

    """

    def __init__(self):
        """
        :param GroupId: ID of the connection group to be deleted.
        :type GroupId: str
        :param Force: Whether to enable forced deletion. Valid values:
0: no;
1: yes.
Default value: 0. If there is a connection or listener/rule bound to an origin server in the connection group and `Force` is 0, the operation will return a failure.
        :type Force: int
        """
        self.GroupId = None
        self.Force = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")
        self.Force = params.get("Force")


class DeleteProxyGroupResponse(AbstractModel):
    """DeleteProxyGroup response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteRuleRequest(AbstractModel):
    """DeleteRule request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Layer-7 listener ID
        :type ListenerId: str
        :param RuleId: Forwarding rule ID
        :type RuleId: str
        :param Force: Whether to make a forced deletion of forwarding rules that have been bound to origin servers. 0: no; 1: yes.
        :type Force: int
        """
        self.ListenerId = None
        self.RuleId = None
        self.Force = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.RuleId = params.get("RuleId")
        self.Force = params.get("Force")


class DeleteRuleResponse(AbstractModel):
    """DeleteRule response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSecurityPolicyRequest(AbstractModel):
    """DeleteSecurityPolicy request structure.

    """

    def __init__(self):
        """
        :param PolicyId: Policy ID
        :type PolicyId: str
        """
        self.PolicyId = None


    def _deserialize(self, params):
        self.PolicyId = params.get("PolicyId")


class DeleteSecurityPolicyResponse(AbstractModel):
    """DeleteSecurityPolicy response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSecurityRulesRequest(AbstractModel):
    """DeleteSecurityRules request structure.

    """

    def __init__(self):
        """
        :param PolicyId: Security policy ID
        :type PolicyId: str
        :param RuleIdList: List of access rule IDs
        :type RuleIdList: list of str
        """
        self.PolicyId = None
        self.RuleIdList = None


    def _deserialize(self, params):
        self.PolicyId = params.get("PolicyId")
        self.RuleIdList = params.get("RuleIdList")


class DeleteSecurityRulesResponse(AbstractModel):
    """DeleteSecurityRules response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAccessRegionsByDestRegionRequest(AbstractModel):
    """DescribeAccessRegionsByDestRegion request structure.

    """

    def __init__(self):
        """
        :param DestRegion: Origin server region: the DescribeDestRegions API returns the value of `RegionId` field of `DestRegionSet`.
        :type DestRegion: str
        """
        self.DestRegion = None


    def _deserialize(self, params):
        self.DestRegion = params.get("DestRegion")


class DescribeAccessRegionsByDestRegionResponse(AbstractModel):
    """DescribeAccessRegionsByDestRegion response structure.

    """

    def __init__(self):
        """
        :param TotalCount: The number of available acceleration regions
        :type TotalCount: int
        :param AccessRegionSet: List of available acceleration region information
        :type AccessRegionSet: list of AccessRegionDetial
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.AccessRegionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("AccessRegionSet") is not None:
            self.AccessRegionSet = []
            for item in params.get("AccessRegionSet"):
                obj = AccessRegionDetial()
                obj._deserialize(item)
                self.AccessRegionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAccessRegionsRequest(AbstractModel):
    """DescribeAccessRegions request structure.

    """


class DescribeAccessRegionsResponse(AbstractModel):
    """DescribeAccessRegions response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Total quantity of acceleration regions
        :type TotalCount: int
        :param AccessRegionSet: Acceleration region details list
        :type AccessRegionSet: list of RegionDetail
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.AccessRegionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("AccessRegionSet") is not None:
            self.AccessRegionSet = []
            for item in params.get("AccessRegionSet"):
                obj = RegionDetail()
                obj._deserialize(item)
                self.AccessRegionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCertificateDetailRequest(AbstractModel):
    """DescribeCertificateDetail request structure.

    """

    def __init__(self):
        """
        :param CertificateId: Certificate ID.
        :type CertificateId: str
        """
        self.CertificateId = None


    def _deserialize(self, params):
        self.CertificateId = params.get("CertificateId")


class DescribeCertificateDetailResponse(AbstractModel):
    """DescribeCertificateDetail response structure.

    """

    def __init__(self):
        """
        :param CertificateDetail: Certificate Details.
        :type CertificateDetail: :class:`tencentcloud.gaap.v20180529.models.CertificateDetail`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.CertificateDetail = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("CertificateDetail") is not None:
            self.CertificateDetail = CertificateDetail()
            self.CertificateDetail._deserialize(params.get("CertificateDetail"))
        self.RequestId = params.get("RequestId")


class DescribeCertificatesRequest(AbstractModel):
    """DescribeCertificates request structure.

    """

    def __init__(self):
        """
        :param CertificateType: Certificate type. Where:
0: basic authentication configuration;
1: client CA certificate;
2: server SSL certificate;
3: origin server CA certificate;
4: connection SSL certificate.
-1: all types.
The default value is -1.
        :type CertificateType: int
        :param Offset: Offset. The default value is 0.
        :type Offset: int
        :param Limit: Quantity limit. The default value is 20.
        :type Limit: int
        """
        self.CertificateType = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.CertificateType = params.get("CertificateType")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeCertificatesResponse(AbstractModel):
    """DescribeCertificates response structure.

    """

    def __init__(self):
        """
        :param CertificateSet: Server certificate list, which includes certificate ID and certificate name.
        :type CertificateSet: list of Certificate
        :param TotalCount: Total quantity of server certificates that match the query conditions.
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.CertificateSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("CertificateSet") is not None:
            self.CertificateSet = []
            for item in params.get("CertificateSet"):
                obj = Certificate()
                obj._deserialize(item)
                self.CertificateSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeCountryAreaMappingRequest(AbstractModel):
    """DescribeCountryAreaMapping request structure.

    """


class DescribeCountryAreaMappingResponse(AbstractModel):
    """DescribeCountryAreaMapping response structure.

    """

    def __init__(self):
        """
        :param CountryAreaMappingList: Country/region code mapping table
        :type CountryAreaMappingList: list of CountryAreaMap
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.CountryAreaMappingList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("CountryAreaMappingList") is not None:
            self.CountryAreaMappingList = []
            for item in params.get("CountryAreaMappingList"):
                obj = CountryAreaMap()
                obj._deserialize(item)
                self.CountryAreaMappingList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDestRegionsRequest(AbstractModel):
    """DescribeDestRegions request structure.

    """


class DescribeDestRegionsResponse(AbstractModel):
    """DescribeDestRegions response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Total number of origin server regions
        :type TotalCount: int
        :param DestRegionSet: List of origin server region details
        :type DestRegionSet: list of RegionDetail
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.DestRegionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DestRegionSet") is not None:
            self.DestRegionSet = []
            for item in params.get("DestRegionSet"):
                obj = RegionDetail()
                obj._deserialize(item)
                self.DestRegionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDomainErrorPageInfoByIdsRequest(AbstractModel):
    """DescribeDomainErrorPageInfoByIds request structure.

    """

    def __init__(self):
        """
        :param ErrorPageIds: List of custom error IDs. Up to 10 IDs are supported
        :type ErrorPageIds: list of str
        """
        self.ErrorPageIds = None


    def _deserialize(self, params):
        self.ErrorPageIds = params.get("ErrorPageIds")


class DescribeDomainErrorPageInfoByIdsResponse(AbstractModel):
    """DescribeDomainErrorPageInfoByIds response structure.

    """

    def __init__(self):
        """
        :param ErrorPageSet: Configuration set of custom error responses
Note: this field may return null, indicating that no valid values can be obtained.
        :type ErrorPageSet: list of DomainErrorPageInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ErrorPageSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ErrorPageSet") is not None:
            self.ErrorPageSet = []
            for item in params.get("ErrorPageSet"):
                obj = DomainErrorPageInfo()
                obj._deserialize(item)
                self.ErrorPageSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDomainErrorPageInfoRequest(AbstractModel):
    """DescribeDomainErrorPageInfo request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param Domain: Domain name
        :type Domain: str
        """
        self.ListenerId = None
        self.Domain = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.Domain = params.get("Domain")


class DescribeDomainErrorPageInfoResponse(AbstractModel):
    """DescribeDomainErrorPageInfo response structure.

    """

    def __init__(self):
        """
        :param ErrorPageSet: Configuration set of a custom error response
Note: This field may return null, indicating that no valid values can be obtained.
        :type ErrorPageSet: list of DomainErrorPageInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ErrorPageSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ErrorPageSet") is not None:
            self.ErrorPageSet = []
            for item in params.get("ErrorPageSet"):
                obj = DomainErrorPageInfo()
                obj._deserialize(item)
                self.ErrorPageSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeGroupAndStatisticsProxyRequest(AbstractModel):
    """DescribeGroupAndStatisticsProxy request structure.

    """

    def __init__(self):
        """
        :param ProjectId: Project ID
        :type ProjectId: int
        """
        self.ProjectId = None


    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")


class DescribeGroupAndStatisticsProxyResponse(AbstractModel):
    """DescribeGroupAndStatisticsProxy response structure.

    """

    def __init__(self):
        """
        :param GroupSet: Information of connection groups that the statistics can be derived from
        :type GroupSet: list of GroupStatisticsInfo
        :param TotalCount: Connection group quantity
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.GroupSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("GroupSet") is not None:
            self.GroupSet = []
            for item in params.get("GroupSet"):
                obj = GroupStatisticsInfo()
                obj._deserialize(item)
                self.GroupSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeGroupDomainConfigRequest(AbstractModel):
    """DescribeGroupDomainConfig request structure.

    """

    def __init__(self):
        """
        :param GroupId: Connection group ID.
        :type GroupId: str
        """
        self.GroupId = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")


class DescribeGroupDomainConfigResponse(AbstractModel):
    """DescribeGroupDomainConfig response structure.

    """

    def __init__(self):
        """
        :param AccessRegionList: Nearest access configuration list of domain name resolution.
        :type AccessRegionList: list of DomainAccessRegionDict
        :param DefaultDnsIp: Default accesses Ip.
        :type DefaultDnsIp: str
        :param GroupId: Connection group ID.
        :type GroupId: str
        :param AccessRegionCount: Total number of configuration of access regions.
        :type AccessRegionCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AccessRegionList = None
        self.DefaultDnsIp = None
        self.GroupId = None
        self.AccessRegionCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AccessRegionList") is not None:
            self.AccessRegionList = []
            for item in params.get("AccessRegionList"):
                obj = DomainAccessRegionDict()
                obj._deserialize(item)
                self.AccessRegionList.append(obj)
        self.DefaultDnsIp = params.get("DefaultDnsIp")
        self.GroupId = params.get("GroupId")
        self.AccessRegionCount = params.get("AccessRegionCount")
        self.RequestId = params.get("RequestId")


class DescribeHTTPListenersRequest(AbstractModel):
    """DescribeHTTPListeners request structure.

    """

    def __init__(self):
        """
        :param ProxyId: Connection ID
        :type ProxyId: str
        :param ListenerId: Filter condition. Exact query by listener IDs.
        :type ListenerId: str
        :param ListenerName: Filter condition. Exact query by listener names.
        :type ListenerName: str
        :param Port: Filter condition. Exact query by listener ports.
        :type Port: int
        :param Offset: Offset. The default value is 0.
        :type Offset: int
        :param Limit: Quantity limit. The default value is 20.
        :type Limit: int
        :param SearchValue: Filter condition. It supports fuzzy query by ports or listener names. This parameter cannot be used with `ListenerName` or `Port`.
        :type SearchValue: str
        :param GroupId: Connection group ID
        :type GroupId: str
        """
        self.ProxyId = None
        self.ListenerId = None
        self.ListenerName = None
        self.Port = None
        self.Offset = None
        self.Limit = None
        self.SearchValue = None
        self.GroupId = None


    def _deserialize(self, params):
        self.ProxyId = params.get("ProxyId")
        self.ListenerId = params.get("ListenerId")
        self.ListenerName = params.get("ListenerName")
        self.Port = params.get("Port")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.SearchValue = params.get("SearchValue")
        self.GroupId = params.get("GroupId")


class DescribeHTTPListenersResponse(AbstractModel):
    """DescribeHTTPListeners response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Quantity of listeners
        :type TotalCount: int
        :param ListenerSet: HTTP listener list
        :type ListenerSet: list of HTTPListener
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ListenerSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ListenerSet") is not None:
            self.ListenerSet = []
            for item in params.get("ListenerSet"):
                obj = HTTPListener()
                obj._deserialize(item)
                self.ListenerSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeHTTPSListenersRequest(AbstractModel):
    """DescribeHTTPSListeners request structure.

    """

    def __init__(self):
        """
        :param ProxyId: Filter condition. Connection ID.
        :type ProxyId: str
        :param ListenerId: Filter condition. Exact query by listener IDs.
        :type ListenerId: str
        :param ListenerName: Filter condition. Exact query by listener names.
        :type ListenerName: str
        :param Port: Filter condition. Exact query by listener ports.
        :type Port: int
        :param Offset: Offset. The default value is 0
        :type Offset: int
        :param Limit: Quantity limit. The default value is 20.
        :type Limit: int
        :param SearchValue: Filter condition. It supports fuzzy query by ports or listener names.
        :type SearchValue: str
        :param GroupId: Connection group ID as a filter
        :type GroupId: str
        """
        self.ProxyId = None
        self.ListenerId = None
        self.ListenerName = None
        self.Port = None
        self.Offset = None
        self.Limit = None
        self.SearchValue = None
        self.GroupId = None


    def _deserialize(self, params):
        self.ProxyId = params.get("ProxyId")
        self.ListenerId = params.get("ListenerId")
        self.ListenerName = params.get("ListenerName")
        self.Port = params.get("Port")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.SearchValue = params.get("SearchValue")
        self.GroupId = params.get("GroupId")


class DescribeHTTPSListenersResponse(AbstractModel):
    """DescribeHTTPSListeners response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Quantity of listeners
        :type TotalCount: int
        :param ListenerSet: HTTPS listener list
        :type ListenerSet: list of HTTPSListener
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ListenerSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ListenerSet") is not None:
            self.ListenerSet = []
            for item in params.get("ListenerSet"):
                obj = HTTPSListener()
                obj._deserialize(item)
                self.ListenerSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListenerRealServersRequest(AbstractModel):
    """DescribeListenerRealServers request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        """
        self.ListenerId = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")


class DescribeListenerRealServersResponse(AbstractModel):
    """DescribeListenerRealServers response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Number of origin servers that can be bound
        :type TotalCount: int
        :param RealServerSet: An information list of origin servers
        :type RealServerSet: list of RealServer
        :param BindRealServerTotalCount: Number of bound origin servers
        :type BindRealServerTotalCount: int
        :param BindRealServerSet: Information list of bound origin servers
        :type BindRealServerSet: list of BindRealServer
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.RealServerSet = None
        self.BindRealServerTotalCount = None
        self.BindRealServerSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RealServerSet") is not None:
            self.RealServerSet = []
            for item in params.get("RealServerSet"):
                obj = RealServer()
                obj._deserialize(item)
                self.RealServerSet.append(obj)
        self.BindRealServerTotalCount = params.get("BindRealServerTotalCount")
        if params.get("BindRealServerSet") is not None:
            self.BindRealServerSet = []
            for item in params.get("BindRealServerSet"):
                obj = BindRealServer()
                obj._deserialize(item)
                self.BindRealServerSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListenerStatisticsRequest(AbstractModel):
    """DescribeListenerStatistics request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param StartTime: Start time
        :type StartTime: str
        :param EndTime: End time
        :type EndTime: str
        :param MetricNames: Statistical metric name list. It supports:["InBandwidth", "OutBandwidth", "Concurrent", "InPackets", "OutPackets"]
        :type MetricNames: list of str
        :param Granularity: Monitoring granularity. It currently supports: 300, 3,600, and 86,400. Unit: seconds.
Time range: <= 1 day, supported minimum granularity: 300 seconds;
Time range: <= 7 days, supported minimum granularity:3,600 seconds;
Time range: > 7 days, supported minimum granularity:86,400 seconds;
        :type Granularity: int
        """
        self.ListenerId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricNames = None
        self.Granularity = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricNames = params.get("MetricNames")
        self.Granularity = params.get("Granularity")


class DescribeListenerStatisticsResponse(AbstractModel):
    """DescribeListenerStatistics response structure.

    """

    def __init__(self):
        """
        :param StatisticsData: Connection group statistics
        :type StatisticsData: list of MetricStatisticsInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.StatisticsData = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("StatisticsData") is not None:
            self.StatisticsData = []
            for item in params.get("StatisticsData"):
                obj = MetricStatisticsInfo()
                obj._deserialize(item)
                self.StatisticsData.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeProxiesRequest(AbstractModel):
    """DescribeProxies request structure.

    """

    def __init__(self):
        """
        :param InstanceIds: Queries by one or multiple instance IDs. The upper limit on the number of instances for each request is 100. This parameter does not support specifying InstanceIds and Filters at the same time. It's an old parameter, please switch to ProxyIds.
        :type InstanceIds: list of str
        :param Offset: Offset. The default value is 0.
        :type Offset: int
        :param Limit: Number of results to be returned. The default value is 20, and the maximum value is 100.
        :type Limit: int
        :param Filters: Filter conditions.   
The upper limit on Filters for each request is 10, and the upper limit on Filter.Values is 5. This parameter does not support specifying InstanceIds and Filters at the same time. 
ProjectId - String - Required: No - Filter by a project ID.    
AccessRegion - String - Required: No - Filter by an access region.    
RealServerRegion - String - Required: No - Filter by an origin server region.
GroupId - String - Required: No - Filter by a connection group ID.
        :type Filters: list of Filter
        :param ProxyIds: Queries by one or multiple instance IDs. The upper limit on the number of instances for each request is 100. This parameter does not support specifying InstanceIds and Filters at the same time. It's a new parameter, and replaces InstanceIds.
        :type ProxyIds: list of str
        :param TagSet: Tag list. If this field exists, the list of the resources with the tag will be pulled.
It supports up to 5 tags. If there are two or more tags, the connections tagged any of them will be pulled.
        :type TagSet: list of TagPair
        :param Independent: When this field is 1, only not-grouped connections are pulled.
When this field is 0, only grouped connections are pulled.
When this field does not exist, all connections are pulled, including both not-grouped and grouped connections.
        :type Independent: int
        """
        self.InstanceIds = None
        self.Offset = None
        self.Limit = None
        self.Filters = None
        self.ProxyIds = None
        self.TagSet = None
        self.Independent = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.ProxyIds = params.get("ProxyIds")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = TagPair()
                obj._deserialize(item)
                self.TagSet.append(obj)
        self.Independent = params.get("Independent")


class DescribeProxiesResponse(AbstractModel):
    """DescribeProxies response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Number of connections.
        :type TotalCount: int
        :param InstanceSet: Connection instance information list; It's an old parameter, please switch to ProxySet.
        :type InstanceSet: list of ProxyInfo
        :param ProxySet: Connection instance information list; It's a new parameter.
        :type ProxySet: list of ProxyInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.InstanceSet = None
        self.ProxySet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("InstanceSet") is not None:
            self.InstanceSet = []
            for item in params.get("InstanceSet"):
                obj = ProxyInfo()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        if params.get("ProxySet") is not None:
            self.ProxySet = []
            for item in params.get("ProxySet"):
                obj = ProxyInfo()
                obj._deserialize(item)
                self.ProxySet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeProxiesStatusRequest(AbstractModel):
    """DescribeProxiesStatus request structure.

    """

    def __init__(self):
        """
        :param InstanceIds: Connection ID list; It's an old parameter, please switch to ProxyIds.
        :type InstanceIds: list of str
        :param ProxyIds: Connection ID list; It's a new parameter.
        :type ProxyIds: list of str
        """
        self.InstanceIds = None
        self.ProxyIds = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.ProxyIds = params.get("ProxyIds")


class DescribeProxiesStatusResponse(AbstractModel):
    """DescribeProxiesStatus response structure.

    """

    def __init__(self):
        """
        :param InstanceStatusSet: Connection status list.
        :type InstanceStatusSet: list of ProxyStatus
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceStatusSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("InstanceStatusSet") is not None:
            self.InstanceStatusSet = []
            for item in params.get("InstanceStatusSet"):
                obj = ProxyStatus()
                obj._deserialize(item)
                self.InstanceStatusSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeProxyAndStatisticsListenersRequest(AbstractModel):
    """DescribeProxyAndStatisticsListeners request structure.

    """

    def __init__(self):
        """
        :param ProjectId: Project ID
        :type ProjectId: int
        """
        self.ProjectId = None


    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")


class DescribeProxyAndStatisticsListenersResponse(AbstractModel):
    """DescribeProxyAndStatisticsListeners response structure.

    """

    def __init__(self):
        """
        :param ProxySet: Information of connections that the statistics can be derived from
        :type ProxySet: list of ProxySimpleInfo
        :param TotalCount: Quantity of connections
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ProxySet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ProxySet") is not None:
            self.ProxySet = []
            for item in params.get("ProxySet"):
                obj = ProxySimpleInfo()
                obj._deserialize(item)
                self.ProxySet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeProxyDetailRequest(AbstractModel):
    """DescribeProxyDetail request structure.

    """

    def __init__(self):
        """
        :param ProxyId: Connection ID to be queried.
        :type ProxyId: str
        """
        self.ProxyId = None


    def _deserialize(self, params):
        self.ProxyId = params.get("ProxyId")


class DescribeProxyDetailResponse(AbstractModel):
    """DescribeProxyDetail response structure.

    """

    def __init__(self):
        """
        :param ProxyDetail: Connection details
        :type ProxyDetail: :class:`tencentcloud.gaap.v20180529.models.ProxyInfo`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ProxyDetail = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ProxyDetail") is not None:
            self.ProxyDetail = ProxyInfo()
            self.ProxyDetail._deserialize(params.get("ProxyDetail"))
        self.RequestId = params.get("RequestId")


class DescribeProxyGroupDetailsRequest(AbstractModel):
    """DescribeProxyGroupDetails request structure.

    """

    def __init__(self):
        """
        :param GroupId: Connection group ID.
        :type GroupId: str
        """
        self.GroupId = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")


class DescribeProxyGroupDetailsResponse(AbstractModel):
    """DescribeProxyGroupDetails response structure.

    """

    def __init__(self):
        """
        :param ProxyGroupDetail: Connection group details
        :type ProxyGroupDetail: :class:`tencentcloud.gaap.v20180529.models.ProxyGroupDetail`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ProxyGroupDetail = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ProxyGroupDetail") is not None:
            self.ProxyGroupDetail = ProxyGroupDetail()
            self.ProxyGroupDetail._deserialize(params.get("ProxyGroupDetail"))
        self.RequestId = params.get("RequestId")


class DescribeProxyGroupListRequest(AbstractModel):
    """DescribeProxyGroupList request structure.

    """

    def __init__(self):
        """
        :param Offset: Offset. The default value is 0.
        :type Offset: int
        :param Limit: Number of returned results. The default value is 20. The maximum value is 100.
        :type Limit: int
        :param ProjectId: Project ID. Value range:
-1: all projects of this user
0: default project
Other values: specified project
        :type ProjectId: int
        :param TagSet: Tag list. If this field exists, the list of the resources with the tag will be pulled.
It supports up to 5 tags. If there are two or more tags, the connection groups tagged any of them will be pulled.
        :type TagSet: list of TagPair
        :param Filters: Filter conditions.   
The limit on Filter.Values of each request is 5.
RealServerRegion - String - Required: No - Filter by origin server region; Refer to the RegionId in the results returned by DescribeDestRegions API.
        :type Filters: list of Filter
        """
        self.Offset = None
        self.Limit = None
        self.ProjectId = None
        self.TagSet = None
        self.Filters = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.ProjectId = params.get("ProjectId")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = TagPair()
                obj._deserialize(item)
                self.TagSet.append(obj)
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeProxyGroupListResponse(AbstractModel):
    """DescribeProxyGroupList response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Total number of connection groups.
        :type TotalCount: int
        :param ProxyGroupList: List of connection groups.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProxyGroupList: list of ProxyGroupInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ProxyGroupList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ProxyGroupList") is not None:
            self.ProxyGroupList = []
            for item in params.get("ProxyGroupList"):
                obj = ProxyGroupInfo()
                obj._deserialize(item)
                self.ProxyGroupList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeProxyGroupStatisticsRequest(AbstractModel):
    """DescribeProxyGroupStatistics request structure.

    """

    def __init__(self):
        """
        :param GroupId: Connection group ID
        :type GroupId: str
        :param StartTime: Start time
        :type StartTime: str
        :param EndTime: End time
        :type EndTime: str
        :param MetricNames: Statistical metric name list. Values: InBandwidth (inbound bandwidth); OutBandwidth (outbound bandwidth); Concurrent (concurrence); InPackets (inbound packets); OutPackets (outbound packets).
        :type MetricNames: list of str
        :param Granularity: Monitoring granularity. It currently supports: 60, 300, 3,600, 86,400. Unit: seconds.
Time range: <= 1 day, supported minimum granularity: 60 seconds;
Time range: <= 7 days, supported minimum granularity: 3,600 seconds;
Time range: <= 30 days, supported minimum granularity: 86,400 seconds;
        :type Granularity: int
        """
        self.GroupId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricNames = None
        self.Granularity = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricNames = params.get("MetricNames")
        self.Granularity = params.get("Granularity")


class DescribeProxyGroupStatisticsResponse(AbstractModel):
    """DescribeProxyGroupStatistics response structure.

    """

    def __init__(self):
        """
        :param StatisticsData: Connection group statistics
        :type StatisticsData: list of MetricStatisticsInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.StatisticsData = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("StatisticsData") is not None:
            self.StatisticsData = []
            for item in params.get("StatisticsData"):
                obj = MetricStatisticsInfo()
                obj._deserialize(item)
                self.StatisticsData.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeProxyStatisticsRequest(AbstractModel):
    """DescribeProxyStatistics request structure.

    """

    def __init__(self):
        """
        :param ProxyId: Connection ID
        :type ProxyId: str
        :param StartTime: Start time (2019-03-25 12:00:00)
        :type StartTime: str
        :param EndTime: End time (2019-03-25 12:00:00)
        :type EndTime: str
        :param MetricNames: Statistical metric name list. Valid values: `InBandwidth` (inbound bandwidth); `OutBandwidth` (outbound bandwidth); Concurrent (concurrence); `InPackets` (inbound packets); `OutPackets` (outbound packets); `PacketLoss` (packet loss rate); `Latency` (latency); `HttpQPS` (the number of HTTP requests); `HttpsQPS` (the number of HTTPS requests).
        :type MetricNames: list of str
        :param Granularity: Monitoring granularity. It currently supports: 60, 300, 3,600, and 86,400. Unit: seconds.
Time range: <= 1 day, supported minimum granularity: 60 seconds;
Time range: <= 7 days, supported minimum granularity: 3,600 seconds;
Time range: <= 30 days, supported minimum granularity: 86,400 seconds;
        :type Granularity: int
        """
        self.ProxyId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricNames = None
        self.Granularity = None


    def _deserialize(self, params):
        self.ProxyId = params.get("ProxyId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricNames = params.get("MetricNames")
        self.Granularity = params.get("Granularity")


class DescribeProxyStatisticsResponse(AbstractModel):
    """DescribeProxyStatistics response structure.

    """

    def __init__(self):
        """
        :param StatisticsData: Connection statistics
        :type StatisticsData: list of MetricStatisticsInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.StatisticsData = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("StatisticsData") is not None:
            self.StatisticsData = []
            for item in params.get("StatisticsData"):
                obj = MetricStatisticsInfo()
                obj._deserialize(item)
                self.StatisticsData.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRealServerStatisticsRequest(AbstractModel):
    """DescribeRealServerStatistics request structure.

    """

    def __init__(self):
        """
        :param RealServerId: Origin server ID
        :type RealServerId: str
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param RuleId: Layer-7 rule ID
        :type RuleId: str
        :param WithinTime: Statistics duration. Unit: hours. It only supports querying statistics for the past 1, 3, 6, 12, and 24 hours.
        :type WithinTime: int
        :param StartTime: Statistics start time, such as `2020-08-19 00:00:00`
        :type StartTime: str
        :param EndTime: Statistics end time, such as `2020-08-19 23:59:59`
        :type EndTime: str
        :param Granularity: Statistics granularity in seconds. Only 1-minute (60-second) and 5-minute (300-second) granularities are supported.
        :type Granularity: int
        """
        self.RealServerId = None
        self.ListenerId = None
        self.RuleId = None
        self.WithinTime = None
        self.StartTime = None
        self.EndTime = None
        self.Granularity = None


    def _deserialize(self, params):
        self.RealServerId = params.get("RealServerId")
        self.ListenerId = params.get("ListenerId")
        self.RuleId = params.get("RuleId")
        self.WithinTime = params.get("WithinTime")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Granularity = params.get("Granularity")


class DescribeRealServerStatisticsResponse(AbstractModel):
    """DescribeRealServerStatistics response structure.

    """

    def __init__(self):
        """
        :param StatisticsData: Origin server status statistics of specified listener
        :type StatisticsData: list of StatisticsDataInfo
        :param RsStatisticsData: Status statistics of multiple origin servers
        :type RsStatisticsData: list of MetricStatisticsInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.StatisticsData = None
        self.RsStatisticsData = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("StatisticsData") is not None:
            self.StatisticsData = []
            for item in params.get("StatisticsData"):
                obj = StatisticsDataInfo()
                obj._deserialize(item)
                self.StatisticsData.append(obj)
        if params.get("RsStatisticsData") is not None:
            self.RsStatisticsData = []
            for item in params.get("RsStatisticsData"):
                obj = MetricStatisticsInfo()
                obj._deserialize(item)
                self.RsStatisticsData.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRealServersRequest(AbstractModel):
    """DescribeRealServers request structure.

    """

    def __init__(self):
        """
        :param ProjectId: Queries the project ID to which the origin server belongs. -1: all projects.
        :type ProjectId: int
        :param SearchValue: Origin server IP or domain name to be queried. The fuzzy match is supported.
        :type SearchValue: str
        :param Offset: Offset, which is 0 by default.
        :type Offset: int
        :param Limit: Quantity of values to return. The default value is 20 and the maximum value is 50.
        :type Limit: int
        :param TagSet: Tag list. If this field exists, the list of the resources with the tag will be pulled.
It supports up to 5 tags. If there are two or more tags, the origin servers tagged any of them will be pulled.
        :type TagSet: list of TagPair
        :param Filters: Filter conditions. The value of the `name` of the `filter` (RealServerName, RealServerIP)
        :type Filters: list of Filter
        """
        self.ProjectId = None
        self.SearchValue = None
        self.Offset = None
        self.Limit = None
        self.TagSet = None
        self.Filters = None


    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.SearchValue = params.get("SearchValue")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = TagPair()
                obj._deserialize(item)
                self.TagSet.append(obj)
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeRealServersResponse(AbstractModel):
    """DescribeRealServers response structure.

    """

    def __init__(self):
        """
        :param RealServerSet: An information list of origin server
        :type RealServerSet: list of BindRealServerInfo
        :param TotalCount: The quantity of origin servers
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RealServerSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("RealServerSet") is not None:
            self.RealServerSet = []
            for item in params.get("RealServerSet"):
                obj = BindRealServerInfo()
                obj._deserialize(item)
                self.RealServerSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeRealServersStatusRequest(AbstractModel):
    """DescribeRealServersStatus request structure.

    """

    def __init__(self):
        """
        :param RealServerIds: List of origin server IDs
        :type RealServerIds: list of str
        """
        self.RealServerIds = None


    def _deserialize(self, params):
        self.RealServerIds = params.get("RealServerIds")


class DescribeRealServersStatusResponse(AbstractModel):
    """DescribeRealServersStatus response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Quantity of origin server query results returned
        :type TotalCount: int
        :param RealServerStatusSet: Binding status list of origin servers
        :type RealServerStatusSet: list of RealServerStatus
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.RealServerStatusSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RealServerStatusSet") is not None:
            self.RealServerStatusSet = []
            for item in params.get("RealServerStatusSet"):
                obj = RealServerStatus()
                obj._deserialize(item)
                self.RealServerStatusSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRegionAndPriceRequest(AbstractModel):
    """DescribeRegionAndPrice request structure.

    """


class DescribeRegionAndPriceResponse(AbstractModel):
    """DescribeRegionAndPrice response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Total number of origin server regions
        :type TotalCount: int
        :param DestRegionSet: List of origin server region details
        :type DestRegionSet: list of RegionDetail
        :param BandwidthUnitPrice: Connection bandwidth price gradient
        :type BandwidthUnitPrice: list of BandwidthPriceGradient
        :param Currency: Currency type of bandwidth price:
CNY (Chinese Yuan)
USD (United States Dollar)
        :type Currency: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.DestRegionSet = None
        self.BandwidthUnitPrice = None
        self.Currency = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DestRegionSet") is not None:
            self.DestRegionSet = []
            for item in params.get("DestRegionSet"):
                obj = RegionDetail()
                obj._deserialize(item)
                self.DestRegionSet.append(obj)
        if params.get("BandwidthUnitPrice") is not None:
            self.BandwidthUnitPrice = []
            for item in params.get("BandwidthUnitPrice"):
                obj = BandwidthPriceGradient()
                obj._deserialize(item)
                self.BandwidthUnitPrice.append(obj)
        self.Currency = params.get("Currency")
        self.RequestId = params.get("RequestId")


class DescribeResourcesByTagRequest(AbstractModel):
    """DescribeResourcesByTag request structure.

    """

    def __init__(self):
        """
        :param TagKey: Tag key.
        :type TagKey: str
        :param TagValue: Tag value.
        :type TagValue: str
        :param ResourceType: Resource type, including:
Proxy (connection);
ProxyGroup (connection group);
RealServer (origin server).
If this field is not specified, all resources with the tag will be queried.
        :type ResourceType: str
        """
        self.TagKey = None
        self.TagValue = None
        self.ResourceType = None


    def _deserialize(self, params):
        self.TagKey = params.get("TagKey")
        self.TagValue = params.get("TagValue")
        self.ResourceType = params.get("ResourceType")


class DescribeResourcesByTagResponse(AbstractModel):
    """DescribeResourcesByTag response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Total resources
        :type TotalCount: int
        :param ResourceSet: Resource list corresponding to the tag
        :type ResourceSet: list of TagResourceInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ResourceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ResourceSet") is not None:
            self.ResourceSet = []
            for item in params.get("ResourceSet"):
                obj = TagResourceInfo()
                obj._deserialize(item)
                self.ResourceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRuleRealServersRequest(AbstractModel):
    """DescribeRuleRealServers request structure.

    """

    def __init__(self):
        """
        :param RuleId: Forwarding rule ID
        :type RuleId: str
        :param Offset: Offset. Default value: 0.
        :type Offset: int
        :param Limit: Number of values to be returned. The default value is 20. Maximum is 1000.
        :type Limit: int
        """
        self.RuleId = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.RuleId = params.get("RuleId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeRuleRealServersResponse(AbstractModel):
    """DescribeRuleRealServers response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Quantity of origin servers that can be bound
        :type TotalCount: int
        :param RealServerSet: Information list of origin servers that can be bound
        :type RealServerSet: list of RealServer
        :param BindRealServerTotalCount: Quantity of bound origin servers
        :type BindRealServerTotalCount: int
        :param BindRealServerSet: Bound origin server information list
        :type BindRealServerSet: list of BindRealServer
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.RealServerSet = None
        self.BindRealServerTotalCount = None
        self.BindRealServerSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RealServerSet") is not None:
            self.RealServerSet = []
            for item in params.get("RealServerSet"):
                obj = RealServer()
                obj._deserialize(item)
                self.RealServerSet.append(obj)
        self.BindRealServerTotalCount = params.get("BindRealServerTotalCount")
        if params.get("BindRealServerSet") is not None:
            self.BindRealServerSet = []
            for item in params.get("BindRealServerSet"):
                obj = BindRealServer()
                obj._deserialize(item)
                self.BindRealServerSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRulesByRuleIdsRequest(AbstractModel):
    """DescribeRulesByRuleIds request structure.

    """

    def __init__(self):
        """
        :param RuleIds: List of rule IDs. Up to 10 rules are supported.
        :type RuleIds: list of str
        """
        self.RuleIds = None


    def _deserialize(self, params):
        self.RuleIds = params.get("RuleIds")


class DescribeRulesByRuleIdsResponse(AbstractModel):
    """DescribeRulesByRuleIds response structure.

    """

    def __init__(self):
        """
        :param TotalCount: The number of returned rules.
        :type TotalCount: int
        :param RuleSet: List of returned rules.
        :type RuleSet: list of RuleInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.RuleSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RuleSet") is not None:
            self.RuleSet = []
            for item in params.get("RuleSet"):
                obj = RuleInfo()
                obj._deserialize(item)
                self.RuleSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRulesRequest(AbstractModel):
    """DescribeRules request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Layer-7 listener ID.
        :type ListenerId: str
        """
        self.ListenerId = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")


class DescribeRulesResponse(AbstractModel):
    """DescribeRules response structure.

    """

    def __init__(self):
        """
        :param DomainRuleSet: Rule information list classified by domain name type
        :type DomainRuleSet: list of DomainRuleSet
        :param TotalCount: Total quantity of domain names under this listener
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DomainRuleSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DomainRuleSet") is not None:
            self.DomainRuleSet = []
            for item in params.get("DomainRuleSet"):
                obj = DomainRuleSet()
                obj._deserialize(item)
                self.DomainRuleSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSecurityPolicyDetailRequest(AbstractModel):
    """DescribeSecurityPolicyDetail request structure.

    """

    def __init__(self):
        """
        :param PolicyId: Security policy ID
        :type PolicyId: str
        """
        self.PolicyId = None


    def _deserialize(self, params):
        self.PolicyId = params.get("PolicyId")


class DescribeSecurityPolicyDetailResponse(AbstractModel):
    """DescribeSecurityPolicyDetail response structure.

    """

    def __init__(self):
        """
        :param ProxyId: Connection ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type ProxyId: str
        :param Status: Security policy status:
BOUND (security policies enabled)
UNBIND (security policies disabled)
BINDING (enabling security policies)
UNBINDING (disabling security policies)
        :type Status: str
        :param DefaultAction: Default policy: ACCEPT or DROP.
        :type DefaultAction: str
        :param PolicyId: Policy ID
        :type PolicyId: str
        :param RuleList: List of rules
        :type RuleList: list of SecurityPolicyRuleOut
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ProxyId = None
        self.Status = None
        self.DefaultAction = None
        self.PolicyId = None
        self.RuleList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ProxyId = params.get("ProxyId")
        self.Status = params.get("Status")
        self.DefaultAction = params.get("DefaultAction")
        self.PolicyId = params.get("PolicyId")
        if params.get("RuleList") is not None:
            self.RuleList = []
            for item in params.get("RuleList"):
                obj = SecurityPolicyRuleOut()
                obj._deserialize(item)
                self.RuleList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSecurityRulesRequest(AbstractModel):
    """DescribeSecurityRules request structure.

    """

    def __init__(self):
        """
        :param SecurityRuleIds: List of security rule IDs. Up to 20 security rules are supported.
        :type SecurityRuleIds: list of str
        """
        self.SecurityRuleIds = None


    def _deserialize(self, params):
        self.SecurityRuleIds = params.get("SecurityRuleIds")


class DescribeSecurityRulesResponse(AbstractModel):
    """DescribeSecurityRules response structure.

    """

    def __init__(self):
        """
        :param TotalCount: The number of returned security rules.
        :type TotalCount: int
        :param SecurityRuleSet: List of returned security rules.
        :type SecurityRuleSet: list of SecurityPolicyRuleOut
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.SecurityRuleSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("SecurityRuleSet") is not None:
            self.SecurityRuleSet = []
            for item in params.get("SecurityRuleSet"):
                obj = SecurityPolicyRuleOut()
                obj._deserialize(item)
                self.SecurityRuleSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTCPListenersRequest(AbstractModel):
    """DescribeTCPListeners request structure.

    """

    def __init__(self):
        """
        :param ProxyId: Connection ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type ProxyId: str
        :param ListenerId: Filter condition. Exact query by listener IDs.
        :type ListenerId: str
        :param ListenerName: Filter condition. Exact query by listener names.
        :type ListenerName: str
        :param Port: Filter condition. Exact query by listener ports.
        :type Port: int
        :param Offset: Offset. The default value is 0.
        :type Offset: int
        :param Limit: Quantity limit. The default value is 20.
        :type Limit: int
        :param GroupId: Connection group ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type GroupId: str
        :param SearchValue: Filter condition. It supports fuzzy query by ports or listener names. This parameter cannot be used with `ListenerName` or `Port`.
        :type SearchValue: str
        """
        self.ProxyId = None
        self.ListenerId = None
        self.ListenerName = None
        self.Port = None
        self.Offset = None
        self.Limit = None
        self.GroupId = None
        self.SearchValue = None


    def _deserialize(self, params):
        self.ProxyId = params.get("ProxyId")
        self.ListenerId = params.get("ListenerId")
        self.ListenerName = params.get("ListenerName")
        self.Port = params.get("Port")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.GroupId = params.get("GroupId")
        self.SearchValue = params.get("SearchValue")


class DescribeTCPListenersResponse(AbstractModel):
    """DescribeTCPListeners response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Total quantity of listeners that matches the conditions
        :type TotalCount: int
        :param ListenerSet: TCP listener list
        :type ListenerSet: list of TCPListener
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ListenerSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ListenerSet") is not None:
            self.ListenerSet = []
            for item in params.get("ListenerSet"):
                obj = TCPListener()
                obj._deserialize(item)
                self.ListenerSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeUDPListenersRequest(AbstractModel):
    """DescribeUDPListeners request structure.

    """

    def __init__(self):
        """
        :param ProxyId: Connection ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type ProxyId: str
        :param ListenerId: Filter condition. Exact query by listener IDs.
        :type ListenerId: str
        :param ListenerName: Filter condition. Exact query by listener names.
        :type ListenerName: str
        :param Port: Filter condition. Exact query by listener ports.
        :type Port: int
        :param Offset: Offset. The default value is 0.
        :type Offset: int
        :param Limit: Quantity limit. The default value is 20.
        :type Limit: int
        :param GroupId: Connection group ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type GroupId: str
        :param SearchValue: Filter condition. It supports fuzzy query by ports or listener names. This parameter cannot be used with `ListenerName` or `Port`.
        :type SearchValue: str
        """
        self.ProxyId = None
        self.ListenerId = None
        self.ListenerName = None
        self.Port = None
        self.Offset = None
        self.Limit = None
        self.GroupId = None
        self.SearchValue = None


    def _deserialize(self, params):
        self.ProxyId = params.get("ProxyId")
        self.ListenerId = params.get("ListenerId")
        self.ListenerName = params.get("ListenerName")
        self.Port = params.get("Port")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.GroupId = params.get("GroupId")
        self.SearchValue = params.get("SearchValue")


class DescribeUDPListenersResponse(AbstractModel):
    """DescribeUDPListeners response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Quantity of listeners
        :type TotalCount: int
        :param ListenerSet: UDP listener list
        :type ListenerSet: list of UDPListener
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ListenerSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ListenerSet") is not None:
            self.ListenerSet = []
            for item in params.get("ListenerSet"):
                obj = UDPListener()
                obj._deserialize(item)
                self.ListenerSet.append(obj)
        self.RequestId = params.get("RequestId")


class DestroyProxiesRequest(AbstractModel):
    """DestroyProxies request structure.

    """

    def __init__(self):
        """
        :param Force: The identifier for forced deletion
1: this connection list is deleted forcibly regardless of whether the origin server has been bound.
0: this connection list cannot be deleted if the origin server has been bound.
If this identifier is 0, the deletion can be performed only when all the connections have not been bound to any origin servers.
        :type Force: int
        :param InstanceIds: List of connection instance IDs; It's an old parameter, please switch to ProxyIds.
        :type InstanceIds: list of str
        :param ClientToken: A string used to ensure the idempotency of the request, which is generated by the user and must be unique to each request. The maximum length is 64 ASCII characters. If this parameter is not specified, the idempotency of the request cannot be guaranteed.
For more information, please see How to Ensure Idempotence.
        :type ClientToken: str
        :param ProxyIds: List of connection instance IDs; It's a new parameter.
        :type ProxyIds: list of str
        """
        self.Force = None
        self.InstanceIds = None
        self.ClientToken = None
        self.ProxyIds = None


    def _deserialize(self, params):
        self.Force = params.get("Force")
        self.InstanceIds = params.get("InstanceIds")
        self.ClientToken = params.get("ClientToken")
        self.ProxyIds = params.get("ProxyIds")


class DestroyProxiesResponse(AbstractModel):
    """DestroyProxies response structure.

    """

    def __init__(self):
        """
        :param InvalidStatusInstanceSet: ID list of connection instances that cannot be terminated.
        :type InvalidStatusInstanceSet: list of str
        :param OperationFailedInstanceSet: ID list of connection instances that failed to be terminated.
        :type OperationFailedInstanceSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InvalidStatusInstanceSet = None
        self.OperationFailedInstanceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InvalidStatusInstanceSet = params.get("InvalidStatusInstanceSet")
        self.OperationFailedInstanceSet = params.get("OperationFailedInstanceSet")
        self.RequestId = params.get("RequestId")


class DomainAccessRegionDict(AbstractModel):
    """Nearest access configuration details of domain name resolution

    """

    def __init__(self):
        """
        :param NationCountryInnerList: Nearest access region
        :type NationCountryInnerList: list of NationCountryInnerInfo
        :param ProxyList: Acceleration region connection list
        :type ProxyList: list of ProxyIdDict
        :param RegionId: Acceleration region ID
        :type RegionId: str
        :param GeographicalZoneInnerCode: Acceleration region internal code
        :type GeographicalZoneInnerCode: str
        :param ContinentInnerCode: Internal code of the continent to which the acceleration region belongs
        :type ContinentInnerCode: str
        :param RegionName: Acceleration region alias
        :type RegionName: str
        """
        self.NationCountryInnerList = None
        self.ProxyList = None
        self.RegionId = None
        self.GeographicalZoneInnerCode = None
        self.ContinentInnerCode = None
        self.RegionName = None


    def _deserialize(self, params):
        if params.get("NationCountryInnerList") is not None:
            self.NationCountryInnerList = []
            for item in params.get("NationCountryInnerList"):
                obj = NationCountryInnerInfo()
                obj._deserialize(item)
                self.NationCountryInnerList.append(obj)
        if params.get("ProxyList") is not None:
            self.ProxyList = []
            for item in params.get("ProxyList"):
                obj = ProxyIdDict()
                obj._deserialize(item)
                self.ProxyList.append(obj)
        self.RegionId = params.get("RegionId")
        self.GeographicalZoneInnerCode = params.get("GeographicalZoneInnerCode")
        self.ContinentInnerCode = params.get("ContinentInnerCode")
        self.RegionName = params.get("RegionName")


class DomainErrorPageInfo(AbstractModel):
    """Custom error response configuration of a domain name

    """

    def __init__(self):
        """
        :param ErrorPageId: Configuration ID of a custom error response
        :type ErrorPageId: str
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param Domain: Domain name
        :type Domain: str
        :param ErrorNos: Original error code
        :type ErrorNos: list of int
        :param NewErrorNo: New error code
Note: This field may return null, indicating that no valid values can be obtained.
        :type NewErrorNo: int
        :param ClearHeaders: Response header to be cleared
Note: This field may return null, indicating that no valid values can be obtained.
        :type ClearHeaders: list of str
        :param SetHeaders: Response header to be set
Note: This field may return null, indicating that no valid values can be obtained.
        :type SetHeaders: list of HttpHeaderParam
        :param Body: Configured response body (excluding HTTP header)
Note: This field may return null, indicating that no valid values can be obtained.
        :type Body: str
        :param Status: Rule status. 0: success
Note: this field may return null, indicating that no valid value is obtained.
        :type Status: int
        """
        self.ErrorPageId = None
        self.ListenerId = None
        self.Domain = None
        self.ErrorNos = None
        self.NewErrorNo = None
        self.ClearHeaders = None
        self.SetHeaders = None
        self.Body = None
        self.Status = None


    def _deserialize(self, params):
        self.ErrorPageId = params.get("ErrorPageId")
        self.ListenerId = params.get("ListenerId")
        self.Domain = params.get("Domain")
        self.ErrorNos = params.get("ErrorNos")
        self.NewErrorNo = params.get("NewErrorNo")
        self.ClearHeaders = params.get("ClearHeaders")
        if params.get("SetHeaders") is not None:
            self.SetHeaders = []
            for item in params.get("SetHeaders"):
                obj = HttpHeaderParam()
                obj._deserialize(item)
                self.SetHeaders.append(obj)
        self.Body = params.get("Body")
        self.Status = params.get("Status")


class DomainRuleSet(AbstractModel):
    """Forwarding rule information of Layer-7 listeners classified by domain name

    """

    def __init__(self):
        """
        :param Domain: Forwarding rule domain name.
        :type Domain: str
        :param RuleSet: Forwarding rule list of the domain name.
        :type RuleSet: list of RuleInfo
        :param CertificateId: Server certificate ID of the domain. When it is `default`, it indicates that the default certificate will be used (i.e., the certificate configured for the listener).
Note: This field may return null, indicating that no valid values can be obtained.
        :type CertificateId: str
        :param CertificateAlias: Server certificate name of the domain name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type CertificateAlias: str
        :param ClientCertificateId: Client certificate ID of the domain. When it is `default`, it indicates that the default certificate will be used (i.e., the certificate configured for the listener).
Note: This field may return null, indicating that no valid values can be obtained.
        :type ClientCertificateId: str
        :param ClientCertificateAlias: Client certificate name of the domain name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ClientCertificateAlias: str
        :param BasicAuthConfId: Basic authentication configuration ID of the domain name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type BasicAuthConfId: str
        :param BasicAuth: Basic authentication status:
0: disabled;
1: enabled.
Note: This field may return null, indicating that no valid values can be obtained.
        :type BasicAuth: int
        :param BasicAuthConfAlias: Basic authentication configuration name of the domain name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type BasicAuthConfAlias: str
        :param RealServerCertificateId: Origin server authentication certificate ID of the domain name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type RealServerCertificateId: str
        :param RealServerAuth: Origin server authentication status:
0: disabled;
1: enabled.
Note: This field may return null, indicating that no valid values can be obtained.
        :type RealServerAuth: int
        :param RealServerCertificateAlias: Origin server authentication certificate name of the domain name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type RealServerCertificateAlias: str
        :param GaapCertificateId: Connection authentication certificate ID of the domain name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type GaapCertificateId: str
        :param GaapAuth: Connection authentication status:
0: disabled;
1: enabled.
Note: This field may return null, indicating that no valid values can be obtained.
        :type GaapAuth: int
        :param GaapCertificateAlias: Connection authentication certificate name of the domain name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type GaapCertificateAlias: str
        :param RealServerCertificateDomain: Origin server authentication domain name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type RealServerCertificateDomain: str
        :param PolyClientCertificateAliasInfo: Returns IDs and aliases of multiple certificates when there are multiple client certificates.
Note: This field may return null, indicating that no valid values can be obtained.
        :type PolyClientCertificateAliasInfo: list of CertificateAliasInfo
        :param PolyRealServerCertificateAliasInfo: Returns IDs and aliases of multiple certificates when there are multiple origin certificates.
Note: This field may return null, indicating that no valid values can be obtained.
        :type PolyRealServerCertificateAliasInfo: list of CertificateAliasInfo
        :param DomainStatus: Domain name status.
0: running;
1: changing;
2: deleting.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DomainStatus: int
        """
        self.Domain = None
        self.RuleSet = None
        self.CertificateId = None
        self.CertificateAlias = None
        self.ClientCertificateId = None
        self.ClientCertificateAlias = None
        self.BasicAuthConfId = None
        self.BasicAuth = None
        self.BasicAuthConfAlias = None
        self.RealServerCertificateId = None
        self.RealServerAuth = None
        self.RealServerCertificateAlias = None
        self.GaapCertificateId = None
        self.GaapAuth = None
        self.GaapCertificateAlias = None
        self.RealServerCertificateDomain = None
        self.PolyClientCertificateAliasInfo = None
        self.PolyRealServerCertificateAliasInfo = None
        self.DomainStatus = None


    def _deserialize(self, params):
        self.Domain = params.get("Domain")
        if params.get("RuleSet") is not None:
            self.RuleSet = []
            for item in params.get("RuleSet"):
                obj = RuleInfo()
                obj._deserialize(item)
                self.RuleSet.append(obj)
        self.CertificateId = params.get("CertificateId")
        self.CertificateAlias = params.get("CertificateAlias")
        self.ClientCertificateId = params.get("ClientCertificateId")
        self.ClientCertificateAlias = params.get("ClientCertificateAlias")
        self.BasicAuthConfId = params.get("BasicAuthConfId")
        self.BasicAuth = params.get("BasicAuth")
        self.BasicAuthConfAlias = params.get("BasicAuthConfAlias")
        self.RealServerCertificateId = params.get("RealServerCertificateId")
        self.RealServerAuth = params.get("RealServerAuth")
        self.RealServerCertificateAlias = params.get("RealServerCertificateAlias")
        self.GaapCertificateId = params.get("GaapCertificateId")
        self.GaapAuth = params.get("GaapAuth")
        self.GaapCertificateAlias = params.get("GaapCertificateAlias")
        self.RealServerCertificateDomain = params.get("RealServerCertificateDomain")
        if params.get("PolyClientCertificateAliasInfo") is not None:
            self.PolyClientCertificateAliasInfo = []
            for item in params.get("PolyClientCertificateAliasInfo"):
                obj = CertificateAliasInfo()
                obj._deserialize(item)
                self.PolyClientCertificateAliasInfo.append(obj)
        if params.get("PolyRealServerCertificateAliasInfo") is not None:
            self.PolyRealServerCertificateAliasInfo = []
            for item in params.get("PolyRealServerCertificateAliasInfo"):
                obj = CertificateAliasInfo()
                obj._deserialize(item)
                self.PolyRealServerCertificateAliasInfo.append(obj)
        self.DomainStatus = params.get("DomainStatus")


class Filter(AbstractModel):
    """Filter conditions

    """

    def __init__(self):
        """
        :param Name: Filter conditions
        :type Name: str
        :param Values: Filter values
        :type Values: list of str
        """
        self.Name = None
        self.Values = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")


class GroupStatisticsInfo(AbstractModel):
    """The connection groups from which the statistics can be derived, and the connection information.

    """

    def __init__(self):
        """
        :param GroupId: Connection group ID
        :type GroupId: str
        :param GroupName: Connection group name
        :type GroupName: str
        :param ProxySet: List of connections of a connection group
        :type ProxySet: list of ProxySimpleInfo
        """
        self.GroupId = None
        self.GroupName = None
        self.ProxySet = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")
        self.GroupName = params.get("GroupName")
        if params.get("ProxySet") is not None:
            self.ProxySet = []
            for item in params.get("ProxySet"):
                obj = ProxySimpleInfo()
                obj._deserialize(item)
                self.ProxySet.append(obj)


class HTTPListener(AbstractModel):
    """HTTP listener information

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param ListenerName: Listener name
        :type ListenerName: str
        :param Port: Listener port
        :type Port: int
        :param CreateTime: Listener creation time; using UNIX timestamp.
        :type CreateTime: int
        :param Protocol: Listener protocol. Valid values: HTTP, HTTPS. The value `HTTP` is used for this structure
        :type Protocol: str
        :param ListenerStatus: Listener status:
0: running;
1: creating;
2: terminating;
3: adjusting origin server;
4: modifying configuration.
        :type ListenerStatus: int
        """
        self.ListenerId = None
        self.ListenerName = None
        self.Port = None
        self.CreateTime = None
        self.Protocol = None
        self.ListenerStatus = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.ListenerName = params.get("ListenerName")
        self.Port = params.get("Port")
        self.CreateTime = params.get("CreateTime")
        self.Protocol = params.get("Protocol")
        self.ListenerStatus = params.get("ListenerStatus")


class HTTPSListener(AbstractModel):
    """HTTPS listener information

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param ListenerName: Listener name
        :type ListenerName: str
        :param Port: Listener port
        :type Port: int
        :param Protocol: Listener protocol. Valid values: HTTP, HTTPS. The value `HTTPS` is used for this structure
        :type Protocol: str
        :param ListenerStatus: Listener status:
0: running;
1: creating;
2: terminating;
3: adjusting origin server;
4: modifying configuration.
        :type ListenerStatus: int
        :param CertificateId: Server SSL certificate ID of the listener
        :type CertificateId: str
        :param ForwardProtocol: Protocol used in the forwarding from connections to origin servers
        :type ForwardProtocol: str
        :param CreateTime: Listener creation time; using UNIX timestamp.
        :type CreateTime: int
        :param CertificateAlias: Server SSL certificate alias
Note: This field may return null, indicating that no valid values can be obtained.
        :type CertificateAlias: str
        :param ClientCertificateId: Client CA certificate ID of the listener
Note: This field may return null, indicating that no valid values can be obtained.
        :type ClientCertificateId: str
        :param AuthType: Listener authentication mode. Valid values:
0: one-way authentication;
1: mutual authentication.
Note: this field may return null, indicating that no valid values can be obtained.
        :type AuthType: int
        :param ClientCertificateAlias: Client CA certificate alias
Note: This field may return null, indicating that no valid values can be obtained.
        :type ClientCertificateAlias: str
        :param PolyClientCertificateAliasInfo: Alias information of multiple client CA certificates.
Note: This field may return null, indicating that no valid values can be obtained.
        :type PolyClientCertificateAliasInfo: list of CertificateAliasInfo
        """
        self.ListenerId = None
        self.ListenerName = None
        self.Port = None
        self.Protocol = None
        self.ListenerStatus = None
        self.CertificateId = None
        self.ForwardProtocol = None
        self.CreateTime = None
        self.CertificateAlias = None
        self.ClientCertificateId = None
        self.AuthType = None
        self.ClientCertificateAlias = None
        self.PolyClientCertificateAliasInfo = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.ListenerName = params.get("ListenerName")
        self.Port = params.get("Port")
        self.Protocol = params.get("Protocol")
        self.ListenerStatus = params.get("ListenerStatus")
        self.CertificateId = params.get("CertificateId")
        self.ForwardProtocol = params.get("ForwardProtocol")
        self.CreateTime = params.get("CreateTime")
        self.CertificateAlias = params.get("CertificateAlias")
        self.ClientCertificateId = params.get("ClientCertificateId")
        self.AuthType = params.get("AuthType")
        self.ClientCertificateAlias = params.get("ClientCertificateAlias")
        if params.get("PolyClientCertificateAliasInfo") is not None:
            self.PolyClientCertificateAliasInfo = []
            for item in params.get("PolyClientCertificateAliasInfo"):
                obj = CertificateAliasInfo()
                obj._deserialize(item)
                self.PolyClientCertificateAliasInfo.append(obj)


class HttpHeaderParam(AbstractModel):
    """Parameter describing an HTTP packet header

    """

    def __init__(self):
        """
        :param HeaderName: HTTP header name
        :type HeaderName: str
        :param HeaderValue: HTTP header value
        :type HeaderValue: str
        """
        self.HeaderName = None
        self.HeaderValue = None


    def _deserialize(self, params):
        self.HeaderName = params.get("HeaderName")
        self.HeaderValue = params.get("HeaderValue")


class InquiryPriceCreateProxyRequest(AbstractModel):
    """InquiryPriceCreateProxy request structure.

    """

    def __init__(self):
        """
        :param AccessRegion: Acceleration region name.
        :type AccessRegion: str
        :param Bandwidth: Connection bandwidth cap. Unit: Mbps.
        :type Bandwidth: int
        :param DestRegion: Origin server region name. It's an old parameter, please switch to RealServerRegion.
        :type DestRegion: str
        :param Concurrency: Upper limit of connection concurrence, which indicates a number of simultaneous online connections. Unit: 10,000 connections. It's an old parameter, please switch to Concurrent.
        :type Concurrency: int
        :param RealServerRegion: Origin server region name; It's a new parameter.
        :type RealServerRegion: str
        :param Concurrent: Upper limit of connection concurrence, which indicates a number of simultaneous online connections. Unit: 10,000 connections. It's a new parameter.
        :type Concurrent: int
        :param BillingType: Billing mode. Valid values: 0: bill-by-bandwidth (default value); 1: bill-by-traffic.
        :type BillingType: int
        """
        self.AccessRegion = None
        self.Bandwidth = None
        self.DestRegion = None
        self.Concurrency = None
        self.RealServerRegion = None
        self.Concurrent = None
        self.BillingType = None


    def _deserialize(self, params):
        self.AccessRegion = params.get("AccessRegion")
        self.Bandwidth = params.get("Bandwidth")
        self.DestRegion = params.get("DestRegion")
        self.Concurrency = params.get("Concurrency")
        self.RealServerRegion = params.get("RealServerRegion")
        self.Concurrent = params.get("Concurrent")
        self.BillingType = params.get("BillingType")


class InquiryPriceCreateProxyResponse(AbstractModel):
    """InquiryPriceCreateProxy response structure.

    """

    def __init__(self):
        """
        :param ProxyDailyPrice: Basic price of connection in USD/day.
        :type ProxyDailyPrice: float
        :param BandwidthUnitPrice: Tiered price of connection bandwidth.
Note: this field may return null, indicating that no valid values can be obtained.
        :type BandwidthUnitPrice: list of BandwidthPriceGradient
        :param DiscountProxyDailyPrice: Discounted basic price of connection in USD/day.
        :type DiscountProxyDailyPrice: float
        :param Currency: Currency, which supports CNY, USD, etc.
        :type Currency: str
        :param FlowUnitPrice: Connection traffic price in USD/GB.
Note: this field may return null, indicating that no valid values can be obtained.
        :type FlowUnitPrice: float
        :param DiscountFlowUnitPrice: Discounted connection traffic price in USD/GB.
Note: this field may return null, indicating that no valid values can be obtained.
        :type DiscountFlowUnitPrice: float
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ProxyDailyPrice = None
        self.BandwidthUnitPrice = None
        self.DiscountProxyDailyPrice = None
        self.Currency = None
        self.FlowUnitPrice = None
        self.DiscountFlowUnitPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ProxyDailyPrice = params.get("ProxyDailyPrice")
        if params.get("BandwidthUnitPrice") is not None:
            self.BandwidthUnitPrice = []
            for item in params.get("BandwidthUnitPrice"):
                obj = BandwidthPriceGradient()
                obj._deserialize(item)
                self.BandwidthUnitPrice.append(obj)
        self.DiscountProxyDailyPrice = params.get("DiscountProxyDailyPrice")
        self.Currency = params.get("Currency")
        self.FlowUnitPrice = params.get("FlowUnitPrice")
        self.DiscountFlowUnitPrice = params.get("DiscountFlowUnitPrice")
        self.RequestId = params.get("RequestId")


class ListenerInfo(AbstractModel):
    """Used by internal APIs. It returns the information of listeners whose statistics can be queried.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param ListenerName: Listener name
        :type ListenerName: str
        :param Port: Listening port
        :type Port: int
        :param Protocol: Listener protocol type
        :type Protocol: str
        """
        self.ListenerId = None
        self.ListenerName = None
        self.Port = None
        self.Protocol = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.ListenerName = params.get("ListenerName")
        self.Port = params.get("Port")
        self.Protocol = params.get("Protocol")


class MetricStatisticsInfo(AbstractModel):
    """One-metric statistics

    """

    def __init__(self):
        """
        :param MetricName: Metric name
        :type MetricName: str
        :param MetricData: Metric statistics
        :type MetricData: list of StatisticsDataInfo
        """
        self.MetricName = None
        self.MetricData = None


    def _deserialize(self, params):
        self.MetricName = params.get("MetricName")
        if params.get("MetricData") is not None:
            self.MetricData = []
            for item in params.get("MetricData"):
                obj = StatisticsDataInfo()
                obj._deserialize(item)
                self.MetricData.append(obj)


class ModifyCertificateAttributesRequest(AbstractModel):
    """ModifyCertificateAttributes request structure.

    """

    def __init__(self):
        """
        :param CertificateId: Certificate ID.
        :type CertificateId: str
        :param CertificateAlias: Certificate name. Up to 50 characters.
        :type CertificateAlias: str
        """
        self.CertificateId = None
        self.CertificateAlias = None


    def _deserialize(self, params):
        self.CertificateId = params.get("CertificateId")
        self.CertificateAlias = params.get("CertificateAlias")


class ModifyCertificateAttributesResponse(AbstractModel):
    """ModifyCertificateAttributes response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyCertificateRequest(AbstractModel):
    """ModifyCertificate request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener instance ID
        :type ListenerId: str
        :param Domain: Domain name whose certificate needs to be modified
        :type Domain: str
        :param CertificateId: New server certificate ID:
If CertificateId=default, using the listener certificate.
        :type CertificateId: str
        :param ClientCertificateId: New client certificate ID:
If ClientCertificateId=default, using the listener certificate.
This parameter is required only when the mutual authentication is adopted.
        :type ClientCertificateId: str
        :param PolyClientCertificateIds: List of new IDs of multiple client certificates, where:
This parameter or the `ClientCertificateId` parameter is required for mutual authentication only.
        :type PolyClientCertificateIds: list of str
        """
        self.ListenerId = None
        self.Domain = None
        self.CertificateId = None
        self.ClientCertificateId = None
        self.PolyClientCertificateIds = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.Domain = params.get("Domain")
        self.CertificateId = params.get("CertificateId")
        self.ClientCertificateId = params.get("ClientCertificateId")
        self.PolyClientCertificateIds = params.get("PolyClientCertificateIds")


class ModifyCertificateResponse(AbstractModel):
    """ModifyCertificate response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDomainRequest(AbstractModel):
    """ModifyDomain request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Layer-7 listener ID
        :type ListenerId: str
        :param OldDomain: Original domain name information
        :type OldDomain: str
        :param NewDomain: New domain name information
        :type NewDomain: str
        :param CertificateId: Server SSL certificate ID. It's only applicable to the connections of version 3.0:
If this field is not passed in, the original certificate will be used;
If this field is passed in, and CertificateId=default, the listener certificate will be used;
For other cases, the certificate specified by CertificateId will be used.
        :type CertificateId: str
        :param ClientCertificateId: Client CA certificate ID. It's only applicable to the connections of version 3.0:
If this field is not passed in, the original certificate will be used;
If this field is passed in, and ClientCertificateId=default, the listener certificate will be used;
For other cases, the certificate specified by ClientCertificateId will be used.
        :type ClientCertificateId: str
        :param PolyClientCertificateIds: Client CA certificate ID. It is only applicable to connections on version 3.0, where:
If this field and `ClientCertificateId` are not included, the original certificate will be used;
If this field is included, and ClientCertificateId=default, then the listener certificate will be used;
In other cases, the certificate specified by `ClientCertificateId` or `PolyClientCertificateIds` will be used.
        :type PolyClientCertificateIds: list of str
        """
        self.ListenerId = None
        self.OldDomain = None
        self.NewDomain = None
        self.CertificateId = None
        self.ClientCertificateId = None
        self.PolyClientCertificateIds = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.OldDomain = params.get("OldDomain")
        self.NewDomain = params.get("NewDomain")
        self.CertificateId = params.get("CertificateId")
        self.ClientCertificateId = params.get("ClientCertificateId")
        self.PolyClientCertificateIds = params.get("PolyClientCertificateIds")


class ModifyDomainResponse(AbstractModel):
    """ModifyDomain response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyGroupDomainConfigRequest(AbstractModel):
    """ModifyGroupDomainConfig request structure.

    """

    def __init__(self):
        """
        :param GroupId: Connection group ID.
        :type GroupId: str
        :param DefaultDnsIp: Default access IP or domain name of domain name resolution
        :type DefaultDnsIp: str
        :param AccessRegionList: Nearest access region configuration.
        :type AccessRegionList: list of AccessRegionDomainConf
        """
        self.GroupId = None
        self.DefaultDnsIp = None
        self.AccessRegionList = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")
        self.DefaultDnsIp = params.get("DefaultDnsIp")
        if params.get("AccessRegionList") is not None:
            self.AccessRegionList = []
            for item in params.get("AccessRegionList"):
                obj = AccessRegionDomainConf()
                obj._deserialize(item)
                self.AccessRegionList.append(obj)


class ModifyGroupDomainConfigResponse(AbstractModel):
    """ModifyGroupDomainConfig response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyHTTPListenerAttributeRequest(AbstractModel):
    """ModifyHTTPListenerAttribute request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID to be modified
        :type ListenerId: str
        :param ListenerName: New listener name
        :type ListenerName: str
        :param ProxyId: Connection ID
        :type ProxyId: str
        """
        self.ListenerId = None
        self.ListenerName = None
        self.ProxyId = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.ListenerName = params.get("ListenerName")
        self.ProxyId = params.get("ProxyId")


class ModifyHTTPListenerAttributeResponse(AbstractModel):
    """ModifyHTTPListenerAttribute response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyHTTPSListenerAttributeRequest(AbstractModel):
    """ModifyHTTPSListenerAttribute request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param ProxyId: Connection ID. This field is required if using a single connection listener.
        :type ProxyId: str
        :param ListenerName: New listener name
        :type ListenerName: str
        :param ForwardProtocol: Type of the protocol used in the forwarding from connections to origin servers
        :type ForwardProtocol: str
        :param CertificateId: New listener server certificate ID
        :type CertificateId: str
        :param ClientCertificateId: New listener client certificate ID
        :type ClientCertificateId: str
        :param PolyClientCertificateIds: Client certificate ID of the listener after modification, which is a new field.
        :type PolyClientCertificateIds: list of str
        """
        self.ListenerId = None
        self.ProxyId = None
        self.ListenerName = None
        self.ForwardProtocol = None
        self.CertificateId = None
        self.ClientCertificateId = None
        self.PolyClientCertificateIds = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.ProxyId = params.get("ProxyId")
        self.ListenerName = params.get("ListenerName")
        self.ForwardProtocol = params.get("ForwardProtocol")
        self.CertificateId = params.get("CertificateId")
        self.ClientCertificateId = params.get("ClientCertificateId")
        self.PolyClientCertificateIds = params.get("PolyClientCertificateIds")


class ModifyHTTPSListenerAttributeResponse(AbstractModel):
    """ModifyHTTPSListenerAttribute response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyProxiesAttributeRequest(AbstractModel):
    """ModifyProxiesAttribute request structure.

    """

    def __init__(self):
        """
        :param InstanceIds: ID of one or multiple connections to be operated; It's an old parameter, please switch to ProxyIds.
        :type InstanceIds: list of str
        :param ProxyName: Connection name. Up to 30 characters.
        :type ProxyName: str
        :param ClientToken: A string used to ensure the idempotency of the request, which is generated by the user and must be unique to each request. The maximum length is 64 ASCII characters. If this parameter is not specified, the idempotency of the request cannot be guaranteed.
For more information, please see How to Ensure Idempotence.
        :type ClientToken: str
        :param ProxyIds: ID of one or multiple connections to be operated; It's a new parameter.
        :type ProxyIds: list of str
        """
        self.InstanceIds = None
        self.ProxyName = None
        self.ClientToken = None
        self.ProxyIds = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.ProxyName = params.get("ProxyName")
        self.ClientToken = params.get("ClientToken")
        self.ProxyIds = params.get("ProxyIds")


class ModifyProxiesAttributeResponse(AbstractModel):
    """ModifyProxiesAttribute response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyProxiesProjectRequest(AbstractModel):
    """ModifyProxiesProject request structure.

    """

    def __init__(self):
        """
        :param ProjectId: The target project ID.
        :type ProjectId: int
        :param InstanceIds: ID of one or multiple connections to be operated; It's an old parameter, please switch to ProxyIds.
        :type InstanceIds: list of str
        :param ClientToken: A string used to ensure the idempotency of the request, which is generated by the user and must be unique to each request. The maximum length is 64 ASCII characters. If this parameter is not specified, the idempotency of the request cannot be guaranteed.
For more information, please see How to Ensure Idempotence.
        :type ClientToken: str
        :param ProxyIds: ID of one or multiple connections to be operated; It's a new parameter.
        :type ProxyIds: list of str
        """
        self.ProjectId = None
        self.InstanceIds = None
        self.ClientToken = None
        self.ProxyIds = None


    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.InstanceIds = params.get("InstanceIds")
        self.ClientToken = params.get("ClientToken")
        self.ProxyIds = params.get("ProxyIds")


class ModifyProxiesProjectResponse(AbstractModel):
    """ModifyProxiesProject response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyProxyConfigurationRequest(AbstractModel):
    """ModifyProxyConfiguration request structure.

    """

    def __init__(self):
        """
        :param InstanceId: Connection instance ID; It's an old parameter, please switch to ProxyId.
        :type InstanceId: str
        :param Bandwidth: Target bandwidth. Unit: Mbps.
Bandwidth or Concurrent must be set. Use the DescribeAccessRegionsByDestRegion API to obtain the value range.
        :type Bandwidth: int
        :param Concurrent: Target concurrence value. Unit: 10,000 connections.
Bandwidth or Concurrent must be set. Use the DescribeAccessRegionsByDestRegion API to obtain the value range.
        :type Concurrent: int
        :param ClientToken: A string used to ensure the idempotency of the request, which is generated by the user and must be unique to each request. The maximum length is 64 ASCII characters. If this parameter is not specified, the idempotency of the request cannot be guaranteed.
For more information, please see How to Ensure Idempotence.
        :type ClientToken: str
        :param ProxyId: Connection instance ID; It's a new parameter.
        :type ProxyId: str
        :param BillingType: Billing mode (0: bill-by-bandwidth, 1: bill-by-traffic. Default value: bill-by-bandwidth)
        :type BillingType: int
        """
        self.InstanceId = None
        self.Bandwidth = None
        self.Concurrent = None
        self.ClientToken = None
        self.ProxyId = None
        self.BillingType = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Bandwidth = params.get("Bandwidth")
        self.Concurrent = params.get("Concurrent")
        self.ClientToken = params.get("ClientToken")
        self.ProxyId = params.get("ProxyId")
        self.BillingType = params.get("BillingType")


class ModifyProxyConfigurationResponse(AbstractModel):
    """ModifyProxyConfiguration response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyProxyGroupAttributeRequest(AbstractModel):
    """ModifyProxyGroupAttribute request structure.

    """

    def __init__(self):
        """
        :param GroupId: ID of the connection group to be modified.
        :type GroupId: str
        :param GroupName: New connection group name. Up to 30 characters. The extra characters will be truncated.
        :type GroupName: str
        :param ProjectId: Project ID
        :type ProjectId: int
        """
        self.GroupId = None
        self.GroupName = None
        self.ProjectId = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")
        self.GroupName = params.get("GroupName")
        self.ProjectId = params.get("ProjectId")


class ModifyProxyGroupAttributeResponse(AbstractModel):
    """ModifyProxyGroupAttribute response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyRealServerNameRequest(AbstractModel):
    """ModifyRealServerName request structure.

    """

    def __init__(self):
        """
        :param RealServerName: Origin server name
        :type RealServerName: str
        :param RealServerId: Origin server ID
        :type RealServerId: str
        """
        self.RealServerName = None
        self.RealServerId = None


    def _deserialize(self, params):
        self.RealServerName = params.get("RealServerName")
        self.RealServerId = params.get("RealServerId")


class ModifyRealServerNameResponse(AbstractModel):
    """ModifyRealServerName response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyRuleAttributeRequest(AbstractModel):
    """ModifyRuleAttribute request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param RuleId: Forwarding rule ID
        :type RuleId: str
        :param Scheduler: Scheduling policy:
rr: round robin;
wrr: weighted round robin;
lc: least connections.
        :type Scheduler: str
        :param HealthCheck: Whether to enable the origin server health check:
1: enable;
0: disable.
        :type HealthCheck: int
        :param CheckParams: Health check configuration parameters
        :type CheckParams: :class:`tencentcloud.gaap.v20180529.models.RuleCheckParams`
        :param Path: Forwarding rule path
        :type Path: str
        :param ForwardProtocol: Protocol types of the forwarding from acceleration connection to origin server, which supports default, HTTP and HTTPS.
If `ForwardProtocol=default`, the `ForwardProtocol` of the listener will be used.
        :type ForwardProtocol: str
        :param ForwardHost: The `host` carried in the request forwarded from the acceleration connection to the origin server.
If `ForwardHost=default`, the domain name of rule will be used. For other cases, the value set in this field will be used.
        :type ForwardHost: str
        """
        self.ListenerId = None
        self.RuleId = None
        self.Scheduler = None
        self.HealthCheck = None
        self.CheckParams = None
        self.Path = None
        self.ForwardProtocol = None
        self.ForwardHost = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.RuleId = params.get("RuleId")
        self.Scheduler = params.get("Scheduler")
        self.HealthCheck = params.get("HealthCheck")
        if params.get("CheckParams") is not None:
            self.CheckParams = RuleCheckParams()
            self.CheckParams._deserialize(params.get("CheckParams"))
        self.Path = params.get("Path")
        self.ForwardProtocol = params.get("ForwardProtocol")
        self.ForwardHost = params.get("ForwardHost")


class ModifyRuleAttributeResponse(AbstractModel):
    """ModifyRuleAttribute response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySecurityRuleRequest(AbstractModel):
    """ModifySecurityRule request structure.

    """

    def __init__(self):
        """
        :param RuleId: Rule ID
        :type RuleId: str
        :param AliasName: Rule name: up to 30 characters. The extra characters will be truncated.
        :type AliasName: str
        :param PolicyId: Security policy ID
        :type PolicyId: str
        :param RuleAction: Security rule action
        :type RuleAction: str
        :param SourceCidr: A CIDR IP address associated with the rule
        :type SourceCidr: str
        :param Protocol: Protocol type
        :type Protocol: str
        :param DestPortRange: Port range. Valid values:
A single port: 80
Multiple ports: 80 and 443
Consecutive ports: 3306-20000
All ports: ALL
        :type DestPortRange: str
        """
        self.RuleId = None
        self.AliasName = None
        self.PolicyId = None
        self.RuleAction = None
        self.SourceCidr = None
        self.Protocol = None
        self.DestPortRange = None


    def _deserialize(self, params):
        self.RuleId = params.get("RuleId")
        self.AliasName = params.get("AliasName")
        self.PolicyId = params.get("PolicyId")
        self.RuleAction = params.get("RuleAction")
        self.SourceCidr = params.get("SourceCidr")
        self.Protocol = params.get("Protocol")
        self.DestPortRange = params.get("DestPortRange")


class ModifySecurityRuleResponse(AbstractModel):
    """ModifySecurityRule response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyTCPListenerAttributeRequest(AbstractModel):
    """ModifyTCPListenerAttribute request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param GroupId: Connection group ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type GroupId: str
        :param ProxyId: Connection ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type ProxyId: str
        :param ListenerName: Listener name
        :type ListenerName: str
        :param Scheduler: Origin server scheduling policy of listeners, which supports round robin (rr), weighted round robin (wrr), and least connections (lc).
        :type Scheduler: str
        :param DelayLoop: Time interval of origin server health check (unit: seconds). Value range: [5, 300].
        :type DelayLoop: int
        :param ConnectTimeout: Response timeout of origin server health check (unit: seconds). Value range: [2, 60]. The timeout value shall be less than the time interval for health check DelayLoop.
        :type ConnectTimeout: int
        :param HealthCheck: Whether to enable health check. 1: enable; 0: disable.
        :type HealthCheck: int
        """
        self.ListenerId = None
        self.GroupId = None
        self.ProxyId = None
        self.ListenerName = None
        self.Scheduler = None
        self.DelayLoop = None
        self.ConnectTimeout = None
        self.HealthCheck = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.GroupId = params.get("GroupId")
        self.ProxyId = params.get("ProxyId")
        self.ListenerName = params.get("ListenerName")
        self.Scheduler = params.get("Scheduler")
        self.DelayLoop = params.get("DelayLoop")
        self.ConnectTimeout = params.get("ConnectTimeout")
        self.HealthCheck = params.get("HealthCheck")


class ModifyTCPListenerAttributeResponse(AbstractModel):
    """ModifyTCPListenerAttribute response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyUDPListenerAttributeRequest(AbstractModel):
    """ModifyUDPListenerAttribute request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param GroupId: Connection group ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type GroupId: str
        :param ProxyId: Connection ID; Either `ProxyId` or `GroupId` must be set, but you cannot set both.
        :type ProxyId: str
        :param ListenerName: Listener name
        :type ListenerName: str
        :param Scheduler: Origin server scheduling policy of listeners
        :type Scheduler: str
        """
        self.ListenerId = None
        self.GroupId = None
        self.ProxyId = None
        self.ListenerName = None
        self.Scheduler = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.GroupId = params.get("GroupId")
        self.ProxyId = params.get("ProxyId")
        self.ListenerName = params.get("ListenerName")
        self.Scheduler = params.get("Scheduler")


class ModifyUDPListenerAttributeResponse(AbstractModel):
    """ModifyUDPListenerAttribute response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class NationCountryInnerInfo(AbstractModel):
    """Nearest access country/region details

    """

    def __init__(self):
        """
        :param NationCountryName: Country name
        :type NationCountryName: str
        :param NationCountryInnerCode: Country internal code
        :type NationCountryInnerCode: str
        """
        self.NationCountryName = None
        self.NationCountryInnerCode = None


    def _deserialize(self, params):
        self.NationCountryName = params.get("NationCountryName")
        self.NationCountryInnerCode = params.get("NationCountryInnerCode")


class NewRealServer(AbstractModel):
    """Add new origin server information

    """

    def __init__(self):
        """
        :param RealServerId: Origin server ID
        :type RealServerId: str
        :param RealServerIP: Origin server IP or domain name
        :type RealServerIP: str
        """
        self.RealServerId = None
        self.RealServerIP = None


    def _deserialize(self, params):
        self.RealServerId = params.get("RealServerId")
        self.RealServerIP = params.get("RealServerIP")


class OpenProxiesRequest(AbstractModel):
    """OpenProxies request structure.

    """

    def __init__(self):
        """
        :param InstanceIds: List of connection instance IDs; It's an old parameter, please switch to ProxyIds.
        :type InstanceIds: list of str
        :param ClientToken: A string used to ensure the idempotency of the request, which is generated by the user and must be unique to each request. The maximum length is 64 ASCII characters. If this parameter is not specified, the idempotency of the request cannot be guaranteed.
For more information, please see How to Ensure Idempotence.
        :type ClientToken: str
        :param ProxyIds: List of connection instance IDs; It's a new parameter.
        :type ProxyIds: list of str
        """
        self.InstanceIds = None
        self.ClientToken = None
        self.ProxyIds = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.ClientToken = params.get("ClientToken")
        self.ProxyIds = params.get("ProxyIds")


class OpenProxiesResponse(AbstractModel):
    """OpenProxies response structure.

    """

    def __init__(self):
        """
        :param InvalidStatusInstanceSet: The connection instance ID list cannot be enabled if it's not disabled.
        :type InvalidStatusInstanceSet: list of str
        :param OperationFailedInstanceSet: ID list of connection instances failed to be enabled.
        :type OperationFailedInstanceSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InvalidStatusInstanceSet = None
        self.OperationFailedInstanceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InvalidStatusInstanceSet = params.get("InvalidStatusInstanceSet")
        self.OperationFailedInstanceSet = params.get("OperationFailedInstanceSet")
        self.RequestId = params.get("RequestId")


class OpenProxyGroupRequest(AbstractModel):
    """OpenProxyGroup request structure.

    """

    def __init__(self):
        """
        :param GroupId: Connection group instance ID
        :type GroupId: str
        """
        self.GroupId = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")


class OpenProxyGroupResponse(AbstractModel):
    """OpenProxyGroup response structure.

    """

    def __init__(self):
        """
        :param InvalidStatusInstanceSet: List of IDs of the connection instances that are not disabled, which cannot be enabled.
        :type InvalidStatusInstanceSet: list of str
        :param OperationFailedInstanceSet: List of IDs of the connection instances failed to be enabled.
        :type OperationFailedInstanceSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InvalidStatusInstanceSet = None
        self.OperationFailedInstanceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InvalidStatusInstanceSet = params.get("InvalidStatusInstanceSet")
        self.OperationFailedInstanceSet = params.get("OperationFailedInstanceSet")
        self.RequestId = params.get("RequestId")


class OpenSecurityPolicyRequest(AbstractModel):
    """OpenSecurityPolicy request structure.

    """

    def __init__(self):
        """
        :param ProxyId: ID of the connections requiring enabled security policies.
        :type ProxyId: str
        :param PolicyId: Security policy ID
        :type PolicyId: str
        """
        self.ProxyId = None
        self.PolicyId = None


    def _deserialize(self, params):
        self.ProxyId = params.get("ProxyId")
        self.PolicyId = params.get("PolicyId")


class OpenSecurityPolicyResponse(AbstractModel):
    """OpenSecurityPolicy response structure.

    """

    def __init__(self):
        """
        :param TaskId: Async Process ID. Using DescribeAsyncTaskStatus to query process and status.
        :type TaskId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class ProxyGroupDetail(AbstractModel):
    """Connection group details

    """

    def __init__(self):
        """
        :param CreateTime: Creation time
        :type CreateTime: int
        :param ProjectId: Project ID
        :type ProjectId: int
        :param ProxyNum: Number of connections in connection group
        :type ProxyNum: int
        :param Status: Connection group status:
0: running normally;
1: creating;
4: terminating;
11: migrating;
        :type Status: int
        :param OwnerUin: Owner UIN
        :type OwnerUin: str
        :param CreateUin: Creation UIN
        :type CreateUin: str
        :param GroupName: Connection name
        :type GroupName: str
        :param DnsDefaultIp: Default IP of domain name resolution for connection groups
        :type DnsDefaultIp: str
        :param Domain: Connection group domain name
Note: This field may return null, indicating that no valid values can be obtained.
        :type Domain: str
        :param RealServerRegionInfo: Target region
        :type RealServerRegionInfo: :class:`tencentcloud.gaap.v20180529.models.RegionDetail`
        :param IsOldGroup: Whether it is an old connection group, i.e., those created before August 3, 2018.
        :type IsOldGroup: bool
        :param GroupId: Connection group ID
        :type GroupId: str
        :param TagSet: Tag list
Note: This field may return null, indicating that no valid values can be obtained.
        :type TagSet: list of TagPair
        :param PolicyId: Security policy ID. This field exists if security policies are set.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type PolicyId: str
        :param Version: Connection group version
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Version: str
        :param ClientIPMethod: Describes how the connection obtains client IPs. 0: TOA; 1: Proxy Protocol.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ClientIPMethod: list of int
        """
        self.CreateTime = None
        self.ProjectId = None
        self.ProxyNum = None
        self.Status = None
        self.OwnerUin = None
        self.CreateUin = None
        self.GroupName = None
        self.DnsDefaultIp = None
        self.Domain = None
        self.RealServerRegionInfo = None
        self.IsOldGroup = None
        self.GroupId = None
        self.TagSet = None
        self.PolicyId = None
        self.Version = None
        self.ClientIPMethod = None


    def _deserialize(self, params):
        self.CreateTime = params.get("CreateTime")
        self.ProjectId = params.get("ProjectId")
        self.ProxyNum = params.get("ProxyNum")
        self.Status = params.get("Status")
        self.OwnerUin = params.get("OwnerUin")
        self.CreateUin = params.get("CreateUin")
        self.GroupName = params.get("GroupName")
        self.DnsDefaultIp = params.get("DnsDefaultIp")
        self.Domain = params.get("Domain")
        if params.get("RealServerRegionInfo") is not None:
            self.RealServerRegionInfo = RegionDetail()
            self.RealServerRegionInfo._deserialize(params.get("RealServerRegionInfo"))
        self.IsOldGroup = params.get("IsOldGroup")
        self.GroupId = params.get("GroupId")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = TagPair()
                obj._deserialize(item)
                self.TagSet.append(obj)
        self.PolicyId = params.get("PolicyId")
        self.Version = params.get("Version")
        self.ClientIPMethod = params.get("ClientIPMethod")


class ProxyGroupInfo(AbstractModel):
    """Connection group details list

    """

    def __init__(self):
        """
        :param GroupId: Connection group ID
        :type GroupId: str
        :param Domain: Connection group domain name
Note: This field may return null, indicating that no valid values can be obtained.
        :type Domain: str
        :param GroupName: Connection group name
Note: This field may return null, indicating that no valid values can be obtained.
        :type GroupName: str
        :param ProjectId: Project ID
        :type ProjectId: int
        :param RealServerRegionInfo: Target region
        :type RealServerRegionInfo: :class:`tencentcloud.gaap.v20180529.models.RegionDetail`
        :param Status: Connection group status.
Where:
0: running;
1: creating;
4: terminating;
11: connection migrating.
        :type Status: str
        :param TagSet: Tag list.
        :type TagSet: list of TagPair
        :param Version: Connection group version
Note: this field may return null, indicating that no valid values can be obtained.
        :type Version: str
        :param CreateTime: Creation time
Note: this field may return null, indicating that no valid values can be obtained.
        :type CreateTime: int
        :param ProxyType: Whether the connection group contains a Microsoft connection
Note: this field may return null, indicating that no valid values can be obtained.
        :type ProxyType: int
        """
        self.GroupId = None
        self.Domain = None
        self.GroupName = None
        self.ProjectId = None
        self.RealServerRegionInfo = None
        self.Status = None
        self.TagSet = None
        self.Version = None
        self.CreateTime = None
        self.ProxyType = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")
        self.Domain = params.get("Domain")
        self.GroupName = params.get("GroupName")
        self.ProjectId = params.get("ProjectId")
        if params.get("RealServerRegionInfo") is not None:
            self.RealServerRegionInfo = RegionDetail()
            self.RealServerRegionInfo._deserialize(params.get("RealServerRegionInfo"))
        self.Status = params.get("Status")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = TagPair()
                obj._deserialize(item)
                self.TagSet.append(obj)
        self.Version = params.get("Version")
        self.CreateTime = params.get("CreateTime")
        self.ProxyType = params.get("ProxyType")


class ProxyIdDict(AbstractModel):
    """Connection ID

    """

    def __init__(self):
        """
        :param ProxyId: Connection ID
        :type ProxyId: str
        """
        self.ProxyId = None


    def _deserialize(self, params):
        self.ProxyId = params.get("ProxyId")


class ProxyInfo(AbstractModel):
    """Connection information

    """

    def __init__(self):
        """
        :param InstanceId: Connection instance ID; It's an old parameter, please switch to ProxyId.
Note: This field may return null, indicating that no valid values can be obtained.
        :type InstanceId: str
        :param CreateTime: Creation time in the format of UNIX timestamp, indicating the number of seconds that have elapsed since January 1, 1970 (midnight in UTC/GMT).
        :type CreateTime: int
        :param ProjectId: Project ID.
        :type ProjectId: int
        :param ProxyName: Connection name.
        :type ProxyName: str
        :param AccessRegion: Access region.
        :type AccessRegion: str
        :param RealServerRegion: Origin server region.
        :type RealServerRegion: str
        :param Bandwidth: Bandwidth. Unit: Mbps.
        :type Bandwidth: int
        :param Concurrent: Concurrence. Unit: requests/second.
        :type Concurrent: int
        :param Status: Connection status:
RUNNING: running;
CREATING: creating;
DESTROYING: terminating;
OPENING: enabling;
CLOSING: disabling;
CLOSED: disabled;
ADJUSTING: adjusting configuration
ISOLATING: isolating (it's triggered when the account is in arrears);
ISOLATED: isolated (it's triggered when the account is in arrears);
UNKNOWN: unknown status.
        :type Status: str
        :param Domain: Accessed domain name.
        :type Domain: str
        :param IP: Accessed IP.
        :type IP: str
        :param Version: Connection versions: 1.0, 2.0, 3.0.
        :type Version: str
        :param ProxyId: Connection instance ID; It's a new parameter.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProxyId: str
        :param Scalarable: 1: this connection is expandable; 0: this connection is not expandable.
        :type Scalarable: int
        :param SupportProtocols: Supported protocol types.
        :type SupportProtocols: list of str
        :param GroupId: Connection group ID. This field exists if a connection belongs to a connection group.
Note: This field may return null, indicating that no valid values can be obtained.
        :type GroupId: str
        :param PolicyId: Security policy ID. This field exists if security policies are configured.
Note: This field may return null, indicating that no valid values can be obtained.
        :type PolicyId: str
        :param AccessRegionInfo: Access region details, including region ID and region name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type AccessRegionInfo: :class:`tencentcloud.gaap.v20180529.models.RegionDetail`
        :param RealServerRegionInfo: Origin server region details, including region ID and region name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type RealServerRegionInfo: :class:`tencentcloud.gaap.v20180529.models.RegionDetail`
        :param ForwardIP: Forwarding IP of the connection
        :type ForwardIP: str
        :param TagSet: Tag list. This field is an empty list if no tags exist.
Note: This field may return null, indicating that no valid values can be obtained.
        :type TagSet: list of TagPair
        :param SupportSecurity: Whether security groups are supported.
Note: This field may return null, indicating that no valid values can be obtained.
        :type SupportSecurity: int
        :param BillingType: Billing mode. 0: bill-by-bandwidth; 1: bill-by-traffic.
Note: this field may return null, indicating that no valid values can be obtained.
        :type BillingType: int
        :param RelatedGlobalDomains: List of domain names associated with resolution record
Note: this field may return null, indicating that no valid values can be obtained.
        :type RelatedGlobalDomains: list of str
        :param ModifyConfigTime: Configuration change time
Note: this field may return null, indicating that no valid values can be obtained.
        :type ModifyConfigTime: int
        :param ProxyType: Connection type. 104: SILVER connection.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ProxyType: int
        :param ClientIPMethod: Describes how the connection obtains client IPs. 0: TOA; 1: Proxy Protocol.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ClientIPMethod: list of int
        """
        self.InstanceId = None
        self.CreateTime = None
        self.ProjectId = None
        self.ProxyName = None
        self.AccessRegion = None
        self.RealServerRegion = None
        self.Bandwidth = None
        self.Concurrent = None
        self.Status = None
        self.Domain = None
        self.IP = None
        self.Version = None
        self.ProxyId = None
        self.Scalarable = None
        self.SupportProtocols = None
        self.GroupId = None
        self.PolicyId = None
        self.AccessRegionInfo = None
        self.RealServerRegionInfo = None
        self.ForwardIP = None
        self.TagSet = None
        self.SupportSecurity = None
        self.BillingType = None
        self.RelatedGlobalDomains = None
        self.ModifyConfigTime = None
        self.ProxyType = None
        self.ClientIPMethod = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.CreateTime = params.get("CreateTime")
        self.ProjectId = params.get("ProjectId")
        self.ProxyName = params.get("ProxyName")
        self.AccessRegion = params.get("AccessRegion")
        self.RealServerRegion = params.get("RealServerRegion")
        self.Bandwidth = params.get("Bandwidth")
        self.Concurrent = params.get("Concurrent")
        self.Status = params.get("Status")
        self.Domain = params.get("Domain")
        self.IP = params.get("IP")
        self.Version = params.get("Version")
        self.ProxyId = params.get("ProxyId")
        self.Scalarable = params.get("Scalarable")
        self.SupportProtocols = params.get("SupportProtocols")
        self.GroupId = params.get("GroupId")
        self.PolicyId = params.get("PolicyId")
        if params.get("AccessRegionInfo") is not None:
            self.AccessRegionInfo = RegionDetail()
            self.AccessRegionInfo._deserialize(params.get("AccessRegionInfo"))
        if params.get("RealServerRegionInfo") is not None:
            self.RealServerRegionInfo = RegionDetail()
            self.RealServerRegionInfo._deserialize(params.get("RealServerRegionInfo"))
        self.ForwardIP = params.get("ForwardIP")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = TagPair()
                obj._deserialize(item)
                self.TagSet.append(obj)
        self.SupportSecurity = params.get("SupportSecurity")
        self.BillingType = params.get("BillingType")
        self.RelatedGlobalDomains = params.get("RelatedGlobalDomains")
        self.ModifyConfigTime = params.get("ModifyConfigTime")
        self.ProxyType = params.get("ProxyType")
        self.ClientIPMethod = params.get("ClientIPMethod")


class ProxySimpleInfo(AbstractModel):
    """Used by internal APIs. It returns connections from which the statistics can be derived, and the listener information.

    """

    def __init__(self):
        """
        :param ProxyId: Connection ID
        :type ProxyId: str
        :param ProxyName: Connection name
        :type ProxyName: str
        :param ListenerList: Listener list
        :type ListenerList: list of ListenerInfo
        """
        self.ProxyId = None
        self.ProxyName = None
        self.ListenerList = None


    def _deserialize(self, params):
        self.ProxyId = params.get("ProxyId")
        self.ProxyName = params.get("ProxyName")
        if params.get("ListenerList") is not None:
            self.ListenerList = []
            for item in params.get("ListenerList"):
                obj = ListenerInfo()
                obj._deserialize(item)
                self.ListenerList.append(obj)


class ProxyStatus(AbstractModel):
    """Connection status information

    """

    def __init__(self):
        """
        :param InstanceId: Connection instance ID.
        :type InstanceId: str
        :param Status: Connection status.
Valid values:
RUNNING: running;
CREATING: creating;
DESTROYING: terminating;
OPENING: enabling;
CLOSING: disabling;
CLOSED: disabled;
ADJUSTING: adjusting configuration;
ISOLATING: isolating;
ISOLATED: isolated;
UNKNOWN: unknown status.
        :type Status: str
        """
        self.InstanceId = None
        self.Status = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Status = params.get("Status")


class RealServer(AbstractModel):
    """Query listeners or rules-related origin server information, excluding `tag` information.

    """

    def __init__(self):
        """
        :param RealServerIP: Origin server IP or domain name
        :type RealServerIP: str
        :param RealServerId: Origin server ID
        :type RealServerId: str
        :param RealServerName: Origin server name
        :type RealServerName: str
        :param ProjectId: Project ID
        :type ProjectId: int
        """
        self.RealServerIP = None
        self.RealServerId = None
        self.RealServerName = None
        self.ProjectId = None


    def _deserialize(self, params):
        self.RealServerIP = params.get("RealServerIP")
        self.RealServerId = params.get("RealServerId")
        self.RealServerName = params.get("RealServerName")
        self.ProjectId = params.get("ProjectId")


class RealServerBindSetReq(AbstractModel):
    """RealServerBindSetReq

    """

    def __init__(self):
        """
        :param RealServerId: Origin server ID
        :type RealServerId: str
        :param RealServerPort: Origin server port
        :type RealServerPort: int
        :param RealServerIP: Origin server IP
        :type RealServerIP: str
        :param RealServerWeight: Origin server weight
        :type RealServerWeight: int
        """
        self.RealServerId = None
        self.RealServerPort = None
        self.RealServerIP = None
        self.RealServerWeight = None


    def _deserialize(self, params):
        self.RealServerId = params.get("RealServerId")
        self.RealServerPort = params.get("RealServerPort")
        self.RealServerIP = params.get("RealServerIP")
        self.RealServerWeight = params.get("RealServerWeight")


class RealServerStatus(AbstractModel):
    """Query the binding status of origin servers. BindStatus: 0 (not bound), 1(bound to rules or listeners).

    """

    def __init__(self):
        """
        :param RealServerId: Origin server ID.
        :type RealServerId: str
        :param BindStatus: 0: not bound, 1: bound to rule or listener.
        :type BindStatus: int
        :param ProxyId: ID of the connection bound to this origin server. This string is empty if they are not bound.
        :type ProxyId: str
        """
        self.RealServerId = None
        self.BindStatus = None
        self.ProxyId = None


    def _deserialize(self, params):
        self.RealServerId = params.get("RealServerId")
        self.BindStatus = params.get("BindStatus")
        self.ProxyId = params.get("ProxyId")


class RegionDetail(AbstractModel):
    """Region details

    """

    def __init__(self):
        """
        :param RegionId: Region ID
        :type RegionId: str
        :param RegionName: Region name in Chinese or English
        :type RegionName: str
        """
        self.RegionId = None
        self.RegionName = None


    def _deserialize(self, params):
        self.RegionId = params.get("RegionId")
        self.RegionName = params.get("RegionName")


class RemoveRealServersRequest(AbstractModel):
    """RemoveRealServers request structure.

    """

    def __init__(self):
        """
        :param RealServerIds: List of origin server IDs
        :type RealServerIds: list of str
        """
        self.RealServerIds = None


    def _deserialize(self, params):
        self.RealServerIds = params.get("RealServerIds")


class RemoveRealServersResponse(AbstractModel):
    """RemoveRealServers response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RuleCheckParams(AbstractModel):
    """Health check parameters of the layer-7 listeners' forwarding rules

    """

    def __init__(self):
        """
        :param DelayLoop: Time interval of health check
        :type DelayLoop: int
        :param ConnectTimeout: Response timeout of health check
        :type ConnectTimeout: int
        :param Path: Check path of health check
        :type Path: str
        :param Method: Health check method: GET/HEAD
        :type Method: str
        :param StatusCode: Return code indicting normal origin servers. Value range: [100, 200, 300, 400, 500]
        :type StatusCode: list of int non-negative
        :param Domain: Domain name to be performed health check
You cannot modify this parameter when calling ModifyRuleAttribute API.
        :type Domain: str
        :param FailedCountInter: Origin server failure check frequency
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type FailedCountInter: int
        :param FailedThreshold: Origin server health check threshold. All requests to the origin server will be blocked once the threshold is exceeded.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type FailedThreshold: int
        :param BlockInter: Duration to block requests targeting the origin server after a failed health check
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type BlockInter: int
        """
        self.DelayLoop = None
        self.ConnectTimeout = None
        self.Path = None
        self.Method = None
        self.StatusCode = None
        self.Domain = None
        self.FailedCountInter = None
        self.FailedThreshold = None
        self.BlockInter = None


    def _deserialize(self, params):
        self.DelayLoop = params.get("DelayLoop")
        self.ConnectTimeout = params.get("ConnectTimeout")
        self.Path = params.get("Path")
        self.Method = params.get("Method")
        self.StatusCode = params.get("StatusCode")
        self.Domain = params.get("Domain")
        self.FailedCountInter = params.get("FailedCountInter")
        self.FailedThreshold = params.get("FailedThreshold")
        self.BlockInter = params.get("BlockInter")


class RuleInfo(AbstractModel):
    """Forwarding rule of layer-7 listeners

    """

    def __init__(self):
        """
        :param RuleId: Rule information
        :type RuleId: str
        :param ListenerId: Listener information
        :type ListenerId: str
        :param Domain: Rule domain name
        :type Domain: str
        :param Path: Rule path
        :type Path: str
        :param RealServerType: Origin server type
        :type RealServerType: str
        :param Scheduler: Forwarding policy of the origin server
        :type Scheduler: str
        :param HealthCheck: Whether health check is enabled. 1: enabled, 0: disabled
        :type HealthCheck: int
        :param RuleStatus: Rule status. 0: running, 1: creating, 2: terminating, 3: binding/unbinding origin server, 4: updating configuration
        :type RuleStatus: int
        :param CheckParams: Health check parameters
        :type CheckParams: :class:`tencentcloud.gaap.v20180529.models.RuleCheckParams`
        :param RealServerSet: Bound origin server information
        :type RealServerSet: list of BindRealServer
        :param BindStatus: Origin server service status. 0: exceptional, 1: normal
If health check is not enabled, this status will always be normal.
As long as one origin server is exceptional, this status will be exceptional. Please view `RealServerSet` for the status of specific origin servers.
        :type BindStatus: int
        :param ForwardHost: The `host` carried in the request forwarded from the connection to the origin server. `default` indicates directly forwarding the received 'host'.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ForwardHost: str
        """
        self.RuleId = None
        self.ListenerId = None
        self.Domain = None
        self.Path = None
        self.RealServerType = None
        self.Scheduler = None
        self.HealthCheck = None
        self.RuleStatus = None
        self.CheckParams = None
        self.RealServerSet = None
        self.BindStatus = None
        self.ForwardHost = None


    def _deserialize(self, params):
        self.RuleId = params.get("RuleId")
        self.ListenerId = params.get("ListenerId")
        self.Domain = params.get("Domain")
        self.Path = params.get("Path")
        self.RealServerType = params.get("RealServerType")
        self.Scheduler = params.get("Scheduler")
        self.HealthCheck = params.get("HealthCheck")
        self.RuleStatus = params.get("RuleStatus")
        if params.get("CheckParams") is not None:
            self.CheckParams = RuleCheckParams()
            self.CheckParams._deserialize(params.get("CheckParams"))
        if params.get("RealServerSet") is not None:
            self.RealServerSet = []
            for item in params.get("RealServerSet"):
                obj = BindRealServer()
                obj._deserialize(item)
                self.RealServerSet.append(obj)
        self.BindStatus = params.get("BindStatus")
        self.ForwardHost = params.get("ForwardHost")


class SecurityPolicyRuleIn(AbstractModel):
    """Security policy rule (input parameter)

    """

    def __init__(self):
        """
        :param SourceCidr: Source IP or IP range of the request.
        :type SourceCidr: str
        :param Action: Policy: Allow (ACCEPT) or reject (DROP).
        :type Action: str
        :param AliasName: Rule alias
        :type AliasName: str
        :param Protocol: Protocol: TCP or UDP. ALL indicates all protocols.
        :type Protocol: str
        :param DestPortRange: Target port. Formatting examples:
Single port: 80
Multiple ports: 80, 443
Consecutive ports: 3306-20000
All ports: ALL
        :type DestPortRange: str
        """
        self.SourceCidr = None
        self.Action = None
        self.AliasName = None
        self.Protocol = None
        self.DestPortRange = None


    def _deserialize(self, params):
        self.SourceCidr = params.get("SourceCidr")
        self.Action = params.get("Action")
        self.AliasName = params.get("AliasName")
        self.Protocol = params.get("Protocol")
        self.DestPortRange = params.get("DestPortRange")


class SecurityPolicyRuleOut(AbstractModel):
    """Security policy rule (output parameter)

    """

    def __init__(self):
        """
        :param Action: Policy: Allow (ACCEPT) or reject (DROP).
        :type Action: str
        :param SourceCidr: Source IP or IP range of the request.
        :type SourceCidr: str
        :param AliasName: Rule alias
        :type AliasName: str
        :param DestPortRange: Target port range
Note: This field may return null, indicating that no valid values can be obtained.
        :type DestPortRange: str
        :param RuleId: Rule ID
        :type RuleId: str
        :param Protocol: Protocol type to be matched (TCP/UDP)
Note: This field may return null, indicating that no valid values can be obtained.
        :type Protocol: str
        :param PolicyId: Security policy ID
        :type PolicyId: str
        """
        self.Action = None
        self.SourceCidr = None
        self.AliasName = None
        self.DestPortRange = None
        self.RuleId = None
        self.Protocol = None
        self.PolicyId = None


    def _deserialize(self, params):
        self.Action = params.get("Action")
        self.SourceCidr = params.get("SourceCidr")
        self.AliasName = params.get("AliasName")
        self.DestPortRange = params.get("DestPortRange")
        self.RuleId = params.get("RuleId")
        self.Protocol = params.get("Protocol")
        self.PolicyId = params.get("PolicyId")


class SetAuthenticationRequest(AbstractModel):
    """SetAuthentication request structure.

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID.
        :type ListenerId: str
        :param Domain: The domain name requiring advanced configuration, i.e., the domain name of the listener's forwarding rules.
        :type Domain: str
        :param BasicAuth: Whether to enable the basic authentication:
0: disable basic authentication;
1: enable basic authentication.
The default value is 0.
        :type BasicAuth: int
        :param GaapAuth: Whether to enable the connection authentication, which is for the origin server to authenticate GAAP.
0: disable;
1: enable.
The default value is 0.
        :type GaapAuth: int
        :param RealServerAuth: Whether to enable the origin server authentication, which is for GAAP to authenticate the server.
0: disable;
1: enable.
The default value is 0.
        :type RealServerAuth: int
        :param BasicAuthConfId: Basic authentication configuration ID, which is obtained from the certificate management page.
        :type BasicAuthConfId: str
        :param GaapCertificateId: Connection SSL certificate ID, which is obtained from the certificate management page.
        :type GaapCertificateId: str
        :param RealServerCertificateId: CA certificate ID of the origin server, which is obtained from the certificate management page. When authenticating the origin server, enter this parameter or the `RealServerCertificateIds` parameter.
        :type RealServerCertificateId: str
        :param RealServerCertificateDomain: Domain name of the origin server certificate.
        :type RealServerCertificateDomain: str
        :param PolyRealServerCertificateIds: CA certificate IDs of multiple origin servers, which are obtained from the certificate management page. When authenticating the origin servers, enter this parameter or the `RealServerCertificateId` parameter.
        :type PolyRealServerCertificateIds: list of str
        """
        self.ListenerId = None
        self.Domain = None
        self.BasicAuth = None
        self.GaapAuth = None
        self.RealServerAuth = None
        self.BasicAuthConfId = None
        self.GaapCertificateId = None
        self.RealServerCertificateId = None
        self.RealServerCertificateDomain = None
        self.PolyRealServerCertificateIds = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.Domain = params.get("Domain")
        self.BasicAuth = params.get("BasicAuth")
        self.GaapAuth = params.get("GaapAuth")
        self.RealServerAuth = params.get("RealServerAuth")
        self.BasicAuthConfId = params.get("BasicAuthConfId")
        self.GaapCertificateId = params.get("GaapCertificateId")
        self.RealServerCertificateId = params.get("RealServerCertificateId")
        self.RealServerCertificateDomain = params.get("RealServerCertificateDomain")
        self.PolyRealServerCertificateIds = params.get("PolyRealServerCertificateIds")


class SetAuthenticationResponse(AbstractModel):
    """SetAuthentication response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class StatisticsDataInfo(AbstractModel):
    """Statistics information

    """

    def __init__(self):
        """
        :param Time: Corresponding time point
        :type Time: int
        :param Data: Statistics value
Note: This field may return null, indicating that no valid values can be obtained.
        :type Data: float
        """
        self.Time = None
        self.Data = None


    def _deserialize(self, params):
        self.Time = params.get("Time")
        self.Data = params.get("Data")


class TCPListener(AbstractModel):
    """TCP listener information

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param ListenerName: Listener name
        :type ListenerName: str
        :param Port: Listener port
        :type Port: int
        :param RealServerPort: Origin server port, which is only valid for the connections of version 1.0.
Note: This field may return null, indicating that no valid values can be obtained.
        :type RealServerPort: int
        :param RealServerType: Type of the origin server bound to listeners
        :type RealServerType: str
        :param Protocol: Listener protocol: TCP.
        :type Protocol: str
        :param ListenerStatus: Listener status. Valid values:
0: running;
1: creating;
2: terminating;
3: adjusting origin server;
4: adjusting configuration.
        :type ListenerStatus: int
        :param Scheduler: Origin server access policy of listener. Valid values:
rr: round robin;
wrr: weighted round robin;
lc: least connection.
        :type Scheduler: str
        :param ConnectTimeout: Response timeout of origin server health check (unit: seconds).
        :type ConnectTimeout: int
        :param DelayLoop: Time interval of origin server health check (unit: seconds).
        :type DelayLoop: int
        :param HealthCheck: Whether health check is enabled for listener. Valid values:
0: disabled;
1: enabled
        :type HealthCheck: int
        :param BindStatus: Status of origin server bound to listener. Valid values:
0: exceptional;
1: normal.
        :type BindStatus: int
        :param RealServerSet: Information of the origin server bound to listeners
Note: This field may return null, indicating that no valid values can be obtained.
        :type RealServerSet: list of BindRealServer
        :param CreateTime: Listener creation time; using UNIX timestamp.
        :type CreateTime: int
        :param ClientIPMethod: Describes how the listener obtains client IPs. 0: TOA; 1: Proxy Protocol.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ClientIPMethod: int
        """
        self.ListenerId = None
        self.ListenerName = None
        self.Port = None
        self.RealServerPort = None
        self.RealServerType = None
        self.Protocol = None
        self.ListenerStatus = None
        self.Scheduler = None
        self.ConnectTimeout = None
        self.DelayLoop = None
        self.HealthCheck = None
        self.BindStatus = None
        self.RealServerSet = None
        self.CreateTime = None
        self.ClientIPMethod = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.ListenerName = params.get("ListenerName")
        self.Port = params.get("Port")
        self.RealServerPort = params.get("RealServerPort")
        self.RealServerType = params.get("RealServerType")
        self.Protocol = params.get("Protocol")
        self.ListenerStatus = params.get("ListenerStatus")
        self.Scheduler = params.get("Scheduler")
        self.ConnectTimeout = params.get("ConnectTimeout")
        self.DelayLoop = params.get("DelayLoop")
        self.HealthCheck = params.get("HealthCheck")
        self.BindStatus = params.get("BindStatus")
        if params.get("RealServerSet") is not None:
            self.RealServerSet = []
            for item in params.get("RealServerSet"):
                obj = BindRealServer()
                obj._deserialize(item)
                self.RealServerSet.append(obj)
        self.CreateTime = params.get("CreateTime")
        self.ClientIPMethod = params.get("ClientIPMethod")


class TagPair(AbstractModel):
    """Tag key-value pair

    """

    def __init__(self):
        """
        :param TagKey: Tag key
        :type TagKey: str
        :param TagValue: Tag value
        :type TagValue: str
        """
        self.TagKey = None
        self.TagValue = None


    def _deserialize(self, params):
        self.TagKey = params.get("TagKey")
        self.TagValue = params.get("TagValue")


class TagResourceInfo(AbstractModel):
    """Resource information of the tag

    """

    def __init__(self):
        """
        :param ResourceType: Resource types:
`Proxy`: connections;
`ProxyGroup`: connection groups;
`RealServer`: origin servers.
        :type ResourceType: str
        :param ResourceId: Resource ID
        :type ResourceId: str
        """
        self.ResourceType = None
        self.ResourceId = None


    def _deserialize(self, params):
        self.ResourceType = params.get("ResourceType")
        self.ResourceId = params.get("ResourceId")


class UDPListener(AbstractModel):
    """UDP listener information

    """

    def __init__(self):
        """
        :param ListenerId: Listener ID
        :type ListenerId: str
        :param ListenerName: Listener name
        :type ListenerName: str
        :param Port: Listener port
        :type Port: int
        :param RealServerPort: Origin server port, which is only valid for the connections or connection groups of version 1.0.
Note: This field may return null, indicating that no valid values can be obtained.
        :type RealServerPort: int
        :param RealServerType: Type of the origin server bound to listeners
        :type RealServerType: str
        :param Protocol: Listener protocol: UDP.
        :type Protocol: str
        :param ListenerStatus: Listener status. Valid values:
0: running;
1: creating;
2: terminating;
3: adjusting origin server;
4: adjusting configuration.
        :type ListenerStatus: int
        :param Scheduler: Origin server access policy of listeners
        :type Scheduler: str
        :param BindStatus: Status of origin server bound to listener. 0: normal, 1: exceptional IP, 2: exceptional domain name resolution
        :type BindStatus: int
        :param RealServerSet: Information of the origin server bound to listeners
        :type RealServerSet: list of BindRealServer
        :param CreateTime: Listener creation time; using UNIX timestamp.
        :type CreateTime: int
        """
        self.ListenerId = None
        self.ListenerName = None
        self.Port = None
        self.RealServerPort = None
        self.RealServerType = None
        self.Protocol = None
        self.ListenerStatus = None
        self.Scheduler = None
        self.BindStatus = None
        self.RealServerSet = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.ListenerId = params.get("ListenerId")
        self.ListenerName = params.get("ListenerName")
        self.Port = params.get("Port")
        self.RealServerPort = params.get("RealServerPort")
        self.RealServerType = params.get("RealServerType")
        self.Protocol = params.get("Protocol")
        self.ListenerStatus = params.get("ListenerStatus")
        self.Scheduler = params.get("Scheduler")
        self.BindStatus = params.get("BindStatus")
        if params.get("RealServerSet") is not None:
            self.RealServerSet = []
            for item in params.get("RealServerSet"):
                obj = BindRealServer()
                obj._deserialize(item)
                self.RealServerSet.append(obj)
        self.CreateTime = params.get("CreateTime")
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


class AddUserContactRequest(AbstractModel):
    """AddUserContact request structure.

    """

    def __init__(self):
        """
        :param Name: Contact name, which needs to be unique and can contain 2-60 characters, supporting uppercase and lowercase letters, numbers, and underline “_”. It cannot start with “_”.
        :type Name: str
        :param ContactInfo: Email address, which can contain uppercase and lowercase letters, numbers, and underline “_”, and cannot start with “_”.
        :type ContactInfo: str
        :param Product: Service type, which is fixed to “mysql”.
        :type Product: str
        """
        self.Name = None
        self.ContactInfo = None
        self.Product = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.ContactInfo = params.get("ContactInfo")
        self.Product = params.get("Product")


class AddUserContactResponse(AbstractModel):
    """AddUserContact response structure.

    """

    def __init__(self):
        """
        :param Id: The successfully added contact ID
        :type Id: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Id = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.RequestId = params.get("RequestId")


class ContactItem(AbstractModel):
    """Contact description.

    """

    def __init__(self):
        """
        :param Id: Contact ID.
        :type Id: int
        :param Name: Contact name.
        :type Name: str
        :param Mail: The email address of the contact.
        :type Mail: str
        """
        self.Id = None
        self.Name = None
        self.Mail = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.Mail = params.get("Mail")


class CreateDBDiagReportTaskRequest(AbstractModel):
    """CreateDBDiagReportTask request structure.

    """

    def __init__(self):
        """
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param StartTime: Start time, such as `2020-11-08T14:00:00+08:00`.
        :type StartTime: str
        :param EndTime: End time, such as `2020-11-09T14:00:00+08:00`.
        :type EndTime: str
        :param SendMailFlag: Whether to send an email. Valid values: 0 - Yes, 1 - No.
        :type SendMailFlag: int
        :param ContactPerson: An array of contact IDs to receive the email.
        :type ContactPerson: list of int
        :param ContactGroup: An array of contact group IDs to receive the email.
        :type ContactGroup: list of int
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TencentDB for CynosDB (compatible with MySQL)). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.SendMailFlag = None
        self.ContactPerson = None
        self.ContactGroup = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.SendMailFlag = params.get("SendMailFlag")
        self.ContactPerson = params.get("ContactPerson")
        self.ContactGroup = params.get("ContactGroup")
        self.Product = params.get("Product")


class CreateDBDiagReportTaskResponse(AbstractModel):
    """CreateDBDiagReportTask response structure.

    """

    def __init__(self):
        """
        :param AsyncRequestId: ID of an async task request, which can be used to query the execution result of an async task.
Note: this field may return `null`, indicating that no valid value is obtained.
        :type AsyncRequestId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AsyncRequestId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AsyncRequestId = params.get("AsyncRequestId")
        self.RequestId = params.get("RequestId")


class CreateMailProfileRequest(AbstractModel):
    """CreateMailProfile request structure.

    """

    def __init__(self):
        """
        :param ProfileInfo: Email configurations
        :type ProfileInfo: :class:`tencentcloud.dbbrain.v20191016.models.ProfileInfo`
        :param ProfileLevel: Configuration level. Valid values: "User" (user-level), "Instance" (instance-level). For database inspection report, it should be `User`; and for scheduled task reports, it should be `Instance`.
        :type ProfileLevel: str
        :param ProfileName: Configuration name, which needs to be unique. For database inspection reports, this name can be customize as needed. For scheduled task reports, the name should be in the format of "scheduler_" + {instanceId}, such as "schduler_cdb-test".
        :type ProfileName: str
        :param ProfileType: Configuration type. Valid values: "dbScan_mail_configuration" (email configuration of database inspection report), "scheduler_mail_configuration" (email configuration of scheduled task report).
        :type ProfileType: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TencentDB for CynosDB (compatible with MySQL)).
        :type Product: str
        :param BindInstanceIds: Instance ID bound to the configuration, which is set when the configuration level is "Instance". Only one instance can be bound at a time.
        :type BindInstanceIds: list of str
        """
        self.ProfileInfo = None
        self.ProfileLevel = None
        self.ProfileName = None
        self.ProfileType = None
        self.Product = None
        self.BindInstanceIds = None


    def _deserialize(self, params):
        if params.get("ProfileInfo") is not None:
            self.ProfileInfo = ProfileInfo()
            self.ProfileInfo._deserialize(params.get("ProfileInfo"))
        self.ProfileLevel = params.get("ProfileLevel")
        self.ProfileName = params.get("ProfileName")
        self.ProfileType = params.get("ProfileType")
        self.Product = params.get("Product")
        self.BindInstanceIds = params.get("BindInstanceIds")


class CreateMailProfileResponse(AbstractModel):
    """CreateMailProfile response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateSchedulerMailProfileRequest(AbstractModel):
    """CreateSchedulerMailProfile request structure.

    """

    def __init__(self):
        """
        :param WeekConfiguration: Value range: 1-7, representing Monday to Sunday respectively.
        :type WeekConfiguration: list of int
        :param ProfileInfo: Email configurations
        :type ProfileInfo: :class:`tencentcloud.dbbrain.v20191016.models.ProfileInfo`
        :param ProfileName: Configuration name, which needs to be unique. For scheduled task reports, the name should be in the format of "scheduler_" + {instanceId}, such as "schduler_cdb-test".
        :type ProfileName: str
        :param BindInstanceId: Configure the instance ID that you need to generate the health report.
        :type BindInstanceId: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.WeekConfiguration = None
        self.ProfileInfo = None
        self.ProfileName = None
        self.BindInstanceId = None
        self.Product = None


    def _deserialize(self, params):
        self.WeekConfiguration = params.get("WeekConfiguration")
        if params.get("ProfileInfo") is not None:
            self.ProfileInfo = ProfileInfo()
            self.ProfileInfo._deserialize(params.get("ProfileInfo"))
        self.ProfileName = params.get("ProfileName")
        self.BindInstanceId = params.get("BindInstanceId")
        self.Product = params.get("Product")


class CreateSchedulerMailProfileResponse(AbstractModel):
    """CreateSchedulerMailProfile response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAllUserContactRequest(AbstractModel):
    """DescribeAllUserContact request structure.

    """

    def __init__(self):
        """
        :param Product: Service type, which is fixed to “mysql”.
        :type Product: str
        :param Names: An array of contact name. Fuzzy search is supported.
        :type Names: list of str
        """
        self.Product = None
        self.Names = None


    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.Names = params.get("Names")


class DescribeAllUserContactResponse(AbstractModel):
    """DescribeAllUserContact response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Total number of contacts.
        :type TotalCount: int
        :param Contacts: Contact information.
Note: this field may return `null`, indicating that no valid value is obtained.
        :type Contacts: list of ContactItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Contacts = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Contacts") is not None:
            self.Contacts = []
            for item in params.get("Contacts"):
                obj = ContactItem()
                obj._deserialize(item)
                self.Contacts.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAllUserGroupRequest(AbstractModel):
    """DescribeAllUserGroup request structure.

    """

    def __init__(self):
        """
        :param Product: Service type, which is fixed to “mysql”.
        :type Product: str
        :param Names: An array of contact group name. Fuzzy search is supported.
        :type Names: list of str
        """
        self.Product = None
        self.Names = None


    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.Names = params.get("Names")


class DescribeAllUserGroupResponse(AbstractModel):
    """DescribeAllUserGroup response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Total number of contact groups.
        :type TotalCount: int
        :param Groups: Contact group information.
Note: this field may return `null`, indicating that no valid value is obtained.
        :type Groups: list of GroupItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Groups = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Groups") is not None:
            self.Groups = []
            for item in params.get("Groups"):
                obj = GroupItem()
                obj._deserialize(item)
                self.Groups.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBDiagEventRequest(AbstractModel):
    """DescribeDBDiagEvent request structure.

    """

    def __init__(self):
        """
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param EventId: Event ID, which can be obtained through the `DescribeDBDiagHistory` API.
        :type EventId: int
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TencentDB for CynosDB (compatible with MySQL)). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.EventId = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.EventId = params.get("EventId")
        self.Product = params.get("Product")


class DescribeDBDiagEventResponse(AbstractModel):
    """DescribeDBDiagEvent response structure.

    """

    def __init__(self):
        """
        :param DiagItem: Diagnosis item.
        :type DiagItem: str
        :param DiagType: Diagnosis type.
        :type DiagType: str
        :param EventId: Event ID.
        :type EventId: int
        :param Explanation: Event details.
        :type Explanation: str
        :param Outline: Summary.
        :type Outline: str
        :param Problem: Problem found.
        :type Problem: str
        :param Severity: Severity, which can be divided into 5 levels: 1: fatal, 2: severe, 3: warning, 4: notice, 5: healthy.
        :type Severity: int
        :param StartTime: Start time
        :type StartTime: str
        :param Suggestions: Suggestion.
        :type Suggestions: str
        :param Metric: Reserved field.
Note: this field may return null, indicating that no valid values can be obtained.
        :type Metric: str
        :param EndTime: End time.
        :type EndTime: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DiagItem = None
        self.DiagType = None
        self.EventId = None
        self.Explanation = None
        self.Outline = None
        self.Problem = None
        self.Severity = None
        self.StartTime = None
        self.Suggestions = None
        self.Metric = None
        self.EndTime = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DiagItem = params.get("DiagItem")
        self.DiagType = params.get("DiagType")
        self.EventId = params.get("EventId")
        self.Explanation = params.get("Explanation")
        self.Outline = params.get("Outline")
        self.Problem = params.get("Problem")
        self.Severity = params.get("Severity")
        self.StartTime = params.get("StartTime")
        self.Suggestions = params.get("Suggestions")
        self.Metric = params.get("Metric")
        self.EndTime = params.get("EndTime")
        self.RequestId = params.get("RequestId")


class DescribeDBDiagHistoryRequest(AbstractModel):
    """DescribeDBDiagHistory request structure.

    """

    def __init__(self):
        """
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param StartTime: Start time, such as "2019-09-10 12:13:14".
        :type StartTime: str
        :param EndTime: End time, such as "2019-09-11 12:13:14". The interval between the end time and the start time can be up to 2 days.
        :type EndTime: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TencentDB for CynosDB (compatible with MySQL)). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Product = params.get("Product")


class DescribeDBDiagHistoryResponse(AbstractModel):
    """DescribeDBDiagHistory response structure.

    """

    def __init__(self):
        """
        :param Events: Event description.
        :type Events: list of DiagHistoryEventItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Events = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Events") is not None:
            self.Events = []
            for item in params.get("Events"):
                obj = DiagHistoryEventItem()
                obj._deserialize(item)
                self.Events.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBSpaceStatusRequest(AbstractModel):
    """DescribeDBSpaceStatus request structure.

    """

    def __init__(self):
        """
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param RangeDays: Query period in days. The end date is the current date and the query period is 7 days by default.
        :type RangeDays: int
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TencentDB for CynosDB (compatible with MySQL)). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.RangeDays = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RangeDays = params.get("RangeDays")
        self.Product = params.get("Product")


class DescribeDBSpaceStatusResponse(AbstractModel):
    """DescribeDBSpaceStatus response structure.

    """

    def __init__(self):
        """
        :param Growth: Disk usage growth in MB.
        :type Growth: int
        :param Remain: Available disk space in MB.
        :type Remain: int
        :param Total: Total disk space in MB.
        :type Total: int
        :param AvailableDays: Estimated number of available days.
        :type AvailableDays: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Growth = None
        self.Remain = None
        self.Total = None
        self.AvailableDays = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Growth = params.get("Growth")
        self.Remain = params.get("Remain")
        self.Total = params.get("Total")
        self.AvailableDays = params.get("AvailableDays")
        self.RequestId = params.get("RequestId")


class DescribeDiagDBInstancesRequest(AbstractModel):
    """DescribeDiagDBInstances request structure.

    """

    def __init__(self):
        """
        :param IsSupported: Whether it is an instance supported by DBbrain. It is fixed to “true”.
        :type IsSupported: bool
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        :param Offset: Pagination parameter indicating the offset.
        :type Offset: int
        :param Limit: Pagination parameter indicating the number of entries for each page.
        :type Limit: int
        :param InstanceNames: Query by instance name.
        :type InstanceNames: list of str
        :param InstanceIds: Query by instance ID.
        :type InstanceIds: list of str
        :param Regions: Query by region.
        :type Regions: list of str
        """
        self.IsSupported = None
        self.Product = None
        self.Offset = None
        self.Limit = None
        self.InstanceNames = None
        self.InstanceIds = None
        self.Regions = None


    def _deserialize(self, params):
        self.IsSupported = params.get("IsSupported")
        self.Product = params.get("Product")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.InstanceNames = params.get("InstanceNames")
        self.InstanceIds = params.get("InstanceIds")
        self.Regions = params.get("Regions")


class DescribeDiagDBInstancesResponse(AbstractModel):
    """DescribeDiagDBInstances response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Total Number of Instances
        :type TotalCount: int
        :param DbScanStatus: Status of all instance inspection. 0: all instance inspection enabled, 1: all instance inspection disabled
        :type DbScanStatus: int
        :param Items: Instance related information
        :type Items: list of InstanceInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.DbScanStatus = None
        self.Items = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        self.DbScanStatus = params.get("DbScanStatus")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = InstanceInfo()
                obj._deserialize(item)
                self.Items.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeHealthScoreRequest(AbstractModel):
    """DescribeHealthScore request structure.

    """

    def __init__(self):
        """
        :param InstanceId: The instance ID that needs to obtain the health score
        :type InstanceId: str
        :param Time: Time to obtain the health score
        :type Time: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL (compatible with MySQL)). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.Time = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Time = params.get("Time")
        self.Product = params.get("Product")


class DescribeHealthScoreResponse(AbstractModel):
    """DescribeHealthScore response structure.

    """

    def __init__(self):
        """
        :param Data: Health score and deduction for exceptions
        :type Data: :class:`tencentcloud.dbbrain.v20191016.models.HealthScoreInfo`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = HealthScoreInfo()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeMailProfileRequest(AbstractModel):
    """DescribeMailProfile request structure.

    """

    def __init__(self):
        """
        :param ProfileType: Configuration type. Valid values: "dbScan_mail_configuration" (email configuration of database inspection report), "scheduler_mail_configuration" (email configuration of scheduled task report).
        :type ProfileType: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        :param Offset: Pagination offset
        :type Offset: int
        :param Limit: The number of results per page in paginated queries. Maximum value: 50
        :type Limit: int
        :param ProfileName: Query by the name of email configuration. The name of the regularly sent email configuration should be in the format of "scheduler_"+{instanceId}.
        :type ProfileName: str
        """
        self.ProfileType = None
        self.Product = None
        self.Offset = None
        self.Limit = None
        self.ProfileName = None


    def _deserialize(self, params):
        self.ProfileType = params.get("ProfileType")
        self.Product = params.get("Product")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.ProfileName = params.get("ProfileName")


class DescribeMailProfileResponse(AbstractModel):
    """DescribeMailProfile response structure.

    """

    def __init__(self):
        """
        :param ProfileList: Email configuration details
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ProfileList: list of UserProfile
        :param TotalCount: Total number of email templates
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ProfileList = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ProfileList") is not None:
            self.ProfileList = []
            for item in params.get("ProfileList"):
                obj = UserProfile()
                obj._deserialize(item)
                self.ProfileList.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSlowLogTimeSeriesStatsRequest(AbstractModel):
    """DescribeSlowLogTimeSeriesStats request structure.

    """

    def __init__(self):
        """
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param StartTime: Start time, such as "2019-09-10 12:13:14".
        :type StartTime: str
        :param EndTime: End time, such as "2019-09-10 12:13:14". The interval between the end time and the start time can be up to 7 days.
        :type EndTime: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TencentDB for CynosDB (compatible with MySQL)). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Product = params.get("Product")


class DescribeSlowLogTimeSeriesStatsResponse(AbstractModel):
    """DescribeSlowLogTimeSeriesStats response structure.

    """

    def __init__(self):
        """
        :param Period: Time range in seconds in histogram.
        :type Period: int
        :param TimeSeries: Number of slow logs in specified time range.
        :type TimeSeries: list of TimeSlice
        :param SeriesData: Instance CPU utilization monitoring data in specified time range.
        :type SeriesData: :class:`tencentcloud.dbbrain.v20191016.models.MonitorMetricSeriesData`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Period = None
        self.TimeSeries = None
        self.SeriesData = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Period = params.get("Period")
        if params.get("TimeSeries") is not None:
            self.TimeSeries = []
            for item in params.get("TimeSeries"):
                obj = TimeSlice()
                obj._deserialize(item)
                self.TimeSeries.append(obj)
        if params.get("SeriesData") is not None:
            self.SeriesData = MonitorMetricSeriesData()
            self.SeriesData._deserialize(params.get("SeriesData"))
        self.RequestId = params.get("RequestId")


class DescribeSlowLogTopSqlsRequest(AbstractModel):
    """DescribeSlowLogTopSqls request structure.

    """

    def __init__(self):
        """
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param StartTime: Start time, such as "2019-09-10 12:13:14".
        :type StartTime: str
        :param EndTime: End time, such as "2019-09-10 12:13:14". The interval between the end time and the start time can be up to 7 days.
        :type EndTime: str
        :param SortBy: Sorting key. Valid values: QueryTime, ExecTimes, RowsSent, LockTime, RowsExamined.
        :type SortBy: str
        :param OrderBy: Sorting order. Valid values: ASC (ascending), DESC (descending).
        :type OrderBy: str
        :param Limit: Number of results to be returned. Default value: 20. Maximum value: 100.
        :type Limit: int
        :param Offset: Offset. Default value: 0.
        :type Offset: int
        :param SchemaList: Database name array.
        :type SchemaList: list of SchemaItem
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TencentDB for CynosDB (compatible with MySQL)). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.SortBy = None
        self.OrderBy = None
        self.Limit = None
        self.Offset = None
        self.SchemaList = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.SortBy = params.get("SortBy")
        self.OrderBy = params.get("OrderBy")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        if params.get("SchemaList") is not None:
            self.SchemaList = []
            for item in params.get("SchemaList"):
                obj = SchemaItem()
                obj._deserialize(item)
                self.SchemaList.append(obj)
        self.Product = params.get("Product")


class DescribeSlowLogTopSqlsResponse(AbstractModel):
    """DescribeSlowLogTopSqls response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Number of eligible entries.
        :type TotalCount: int
        :param Rows: List of top slow SQL statements
        :type Rows: list of SlowLogTopSqlItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Rows = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Rows") is not None:
            self.Rows = []
            for item in params.get("Rows"):
                obj = SlowLogTopSqlItem()
                obj._deserialize(item)
                self.Rows.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTopSpaceTableTimeSeriesRequest(AbstractModel):
    """DescribeTopSpaceTableTimeSeries request structure.

    """

    def __init__(self):
        """
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param Limit: Number of returned top tables. Default value: 20. Maximum value: 20.
        :type Limit: int
        :param SortBy: Field used to sort top tables. Valid values: DataLength, IndexLength, TotalLength, DataFree, FragRatio, TableRows, PhysicalFileSize. Default value: PhysicalFileSize.
        :type SortBy: str
        :param StartDate: Start date. It can be as early as 29 days before the current date, and defaults to 6 days before the end date.
        :type StartDate: str
        :param EndDate: End date. It can be as early as 29 days before the current date, and defaults to the current date.
        :type EndDate: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TencentDB for CynosDB (compatible with MySQL)). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.Limit = None
        self.SortBy = None
        self.StartDate = None
        self.EndDate = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Limit = params.get("Limit")
        self.SortBy = params.get("SortBy")
        self.StartDate = params.get("StartDate")
        self.EndDate = params.get("EndDate")
        self.Product = params.get("Product")


class DescribeTopSpaceTableTimeSeriesResponse(AbstractModel):
    """DescribeTopSpaceTableTimeSeries response structure.

    """

    def __init__(self):
        """
        :param TopSpaceTableTimeSeries: Time series list of the returned space statistics of top tables.
        :type TopSpaceTableTimeSeries: list of TableSpaceTimeSeries
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TopSpaceTableTimeSeries = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TopSpaceTableTimeSeries") is not None:
            self.TopSpaceTableTimeSeries = []
            for item in params.get("TopSpaceTableTimeSeries"):
                obj = TableSpaceTimeSeries()
                obj._deserialize(item)
                self.TopSpaceTableTimeSeries.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTopSpaceTablesRequest(AbstractModel):
    """DescribeTopSpaceTables request structure.

    """

    def __init__(self):
        """
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param Limit: Number of returned top tables. Default value: 20. Maximum value: 20.
        :type Limit: int
        :param SortBy: Field used to sort top tables. Valid values: DataLength, IndexLength, TotalLength, DataFree, FragRatio, TableRows, PhysicalFileSize. Default value: PhysicalFileSize.
        :type SortBy: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TencentDB for CynosDB (compatible with MySQL)). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.Limit = None
        self.SortBy = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Limit = params.get("Limit")
        self.SortBy = params.get("SortBy")
        self.Product = params.get("Product")


class DescribeTopSpaceTablesResponse(AbstractModel):
    """DescribeTopSpaceTables response structure.

    """

    def __init__(self):
        """
        :param TopSpaceTables: List of the returned space statistics of top tables.
        :type TopSpaceTables: list of TableSpaceData
        :param Timestamp: Timestamp (in seconds) of tablespace data collect points
        :type Timestamp: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TopSpaceTables = None
        self.Timestamp = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TopSpaceTables") is not None:
            self.TopSpaceTables = []
            for item in params.get("TopSpaceTables"):
                obj = TableSpaceData()
                obj._deserialize(item)
                self.TopSpaceTables.append(obj)
        self.Timestamp = params.get("Timestamp")
        self.RequestId = params.get("RequestId")


class DiagHistoryEventItem(AbstractModel):
    """Instance diagnosis event

    """

    def __init__(self):
        """
        :param DiagType: Diagnosis type.
        :type DiagType: str
        :param EndTime: End time.
        :type EndTime: str
        :param StartTime: Start time.
        :type StartTime: str
        :param EventId: Event ID.
        :type EventId: int
        :param Severity: Severity, which can be divided into 5 levels: 1: fatal, 2: severe, 3: warning, 4: notice, 5: healthy.
        :type Severity: int
        :param Outline: Summary.
        :type Outline: str
        :param DiagItem: Diagnosis item.
        :type DiagItem: str
        :param InstanceId: Instance ID.
Note: this field may return null, indicating that no valid values can be obtained.
        :type InstanceId: str
        :param Metric: Reserved field
Note: this field may return null, indicating that no valid values can be obtained.
        :type Metric: str
        :param Region: Region
Note: this field may return null, indicating that no valid values can be obtained.
        :type Region: str
        """
        self.DiagType = None
        self.EndTime = None
        self.StartTime = None
        self.EventId = None
        self.Severity = None
        self.Outline = None
        self.DiagItem = None
        self.InstanceId = None
        self.Metric = None
        self.Region = None


    def _deserialize(self, params):
        self.DiagType = params.get("DiagType")
        self.EndTime = params.get("EndTime")
        self.StartTime = params.get("StartTime")
        self.EventId = params.get("EventId")
        self.Severity = params.get("Severity")
        self.Outline = params.get("Outline")
        self.DiagItem = params.get("DiagItem")
        self.InstanceId = params.get("InstanceId")
        self.Metric = params.get("Metric")
        self.Region = params.get("Region")


class EventInfo(AbstractModel):
    """Exception information

    """

    def __init__(self):
        """
        :param EventId: Event ID
        :type EventId: int
        :param DiagType: Diagnosis type
        :type DiagType: str
        :param StartTime: Start time
        :type StartTime: str
        :param EndTime: End time
        :type EndTime: str
        :param Outline: Summary
        :type Outline: str
        :param Severity: Severity, which can be divided into 5 levels: 1: fatal, 2: severe, 3: warning, 4: notice, 5: healthy.
        :type Severity: int
        :param ScoreLost: Deduction
        :type ScoreLost: int
        :param Metric: Reserved field
        :type Metric: str
        :param Count: The number of alarms
        :type Count: int
        """
        self.EventId = None
        self.DiagType = None
        self.StartTime = None
        self.EndTime = None
        self.Outline = None
        self.Severity = None
        self.ScoreLost = None
        self.Metric = None
        self.Count = None


    def _deserialize(self, params):
        self.EventId = params.get("EventId")
        self.DiagType = params.get("DiagType")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Outline = params.get("Outline")
        self.Severity = params.get("Severity")
        self.ScoreLost = params.get("ScoreLost")
        self.Metric = params.get("Metric")
        self.Count = params.get("Count")


class GroupItem(AbstractModel):
    """Describe the group information.

    """

    def __init__(self):
        """
        :param Id: Group ID.
        :type Id: int
        :param Name: Group name.
        :type Name: str
        :param MemberCount: Number of group members.
        :type MemberCount: int
        """
        self.Id = None
        self.Name = None
        self.MemberCount = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.MemberCount = params.get("MemberCount")


class HealthScoreInfo(AbstractModel):
    """Obtain the details of the health score and deduction.

    """

    def __init__(self):
        """
        :param IssueTypes: Exception details
        :type IssueTypes: list of IssueTypeInfo
        :param EventsTotalCount: Total number of the exceptions
        :type EventsTotalCount: int
        :param HealthScore: Health score
        :type HealthScore: int
        :param HealthLevel: Health level, such as "HEALTH", "SUB_HEALTH", "RISK", "HIGH_RISK".
        :type HealthLevel: str
        """
        self.IssueTypes = None
        self.EventsTotalCount = None
        self.HealthScore = None
        self.HealthLevel = None


    def _deserialize(self, params):
        if params.get("IssueTypes") is not None:
            self.IssueTypes = []
            for item in params.get("IssueTypes"):
                obj = IssueTypeInfo()
                obj._deserialize(item)
                self.IssueTypes.append(obj)
        self.EventsTotalCount = params.get("EventsTotalCount")
        self.HealthScore = params.get("HealthScore")
        self.HealthLevel = params.get("HealthLevel")


class InstanceConfs(AbstractModel):
    """Instance configuration.

    """

    def __init__(self):
        """
        :param DailyInspection: Whether to enable database inspection. Valid values: Yes/No.
        :type DailyInspection: str
        :param OverviewDisplay: Whether to enable instance overview. Valid values: Yes/No.
        :type OverviewDisplay: str
        """
        self.DailyInspection = None
        self.OverviewDisplay = None


    def _deserialize(self, params):
        self.DailyInspection = params.get("DailyInspection")
        self.OverviewDisplay = params.get("OverviewDisplay")


class InstanceInfo(AbstractModel):
    """Query the list of instances and return information about the instances.

    """

    def __init__(self):
        """
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param InstanceName: Instance name
        :type InstanceName: str
        :param Region: The region where the instance belongs
        :type Region: str
        :param HealthScore: Health score
        :type HealthScore: int
        :param Product: Service
        :type Product: str
        :param EventCount: Number of exceptions
        :type EventCount: int
        :param InstanceType: Instance type. Valid values: 1: MASTER, 2: DR, 3: RO, 4: SDR
        :type InstanceType: int
        :param Cpu: Number of cores
        :type Cpu: int
        :param Memory: Memory in MB
        :type Memory: int
        :param Volume: Disk storage in GB
        :type Volume: int
        :param EngineVersion: Database version
        :type EngineVersion: str
        :param Vip: Private network address
        :type Vip: str
        :param Vport: Private network port
        :type Vport: int
        :param Source: Access source
        :type Source: str
        :param GroupId: Group ID
        :type GroupId: str
        :param GroupName: Group name
        :type GroupName: str
        :param Status: Instance status. Valid values: 0: Delivering, 1: Running, 4: Terminating, 5: Isolated
        :type Status: int
        :param UniqSubnetId: Subnet unified ID
        :type UniqSubnetId: str
        :param DeployMode: cdb (TencentDB instance) type
        :type DeployMode: str
        :param InitFlag: cdb (TencentDB instance) initialization flag. Valid values: 0: not initialized, 1: initialized
        :type InitFlag: int
        :param TaskStatus: Task status
        :type TaskStatus: int
        :param UniqVpcId: Unified VPC ID
        :type UniqVpcId: str
        :param InstanceConf: Instance inspection/overview status
        :type InstanceConf: :class:`tencentcloud.dbbrain.v20191016.models.InstanceConfs`
        :param DeadlineTime: Resource expiration time
        :type DeadlineTime: str
        :param IsSupported: Whether it is an instance supported by DBbrain.
        :type IsSupported: bool
        :param SecAuditStatus: The status of instance security audit log. ON: enabled, OFF: disabled.
        :type SecAuditStatus: str
        :param AuditPolicyStatus: The status of instance audit log. ALL_AUDIT: full audit is enabled, RULE_AUDIT: rule audit is enabled, UNBOUND: audit is disabled.
        :type AuditPolicyStatus: str
        :param AuditRunningStatus: The running status of instance audit log. normal: running, paused: suspension due to arrears
        :type AuditRunningStatus: str
        """
        self.InstanceId = None
        self.InstanceName = None
        self.Region = None
        self.HealthScore = None
        self.Product = None
        self.EventCount = None
        self.InstanceType = None
        self.Cpu = None
        self.Memory = None
        self.Volume = None
        self.EngineVersion = None
        self.Vip = None
        self.Vport = None
        self.Source = None
        self.GroupId = None
        self.GroupName = None
        self.Status = None
        self.UniqSubnetId = None
        self.DeployMode = None
        self.InitFlag = None
        self.TaskStatus = None
        self.UniqVpcId = None
        self.InstanceConf = None
        self.DeadlineTime = None
        self.IsSupported = None
        self.SecAuditStatus = None
        self.AuditPolicyStatus = None
        self.AuditRunningStatus = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.Region = params.get("Region")
        self.HealthScore = params.get("HealthScore")
        self.Product = params.get("Product")
        self.EventCount = params.get("EventCount")
        self.InstanceType = params.get("InstanceType")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.Volume = params.get("Volume")
        self.EngineVersion = params.get("EngineVersion")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.Source = params.get("Source")
        self.GroupId = params.get("GroupId")
        self.GroupName = params.get("GroupName")
        self.Status = params.get("Status")
        self.UniqSubnetId = params.get("UniqSubnetId")
        self.DeployMode = params.get("DeployMode")
        self.InitFlag = params.get("InitFlag")
        self.TaskStatus = params.get("TaskStatus")
        self.UniqVpcId = params.get("UniqVpcId")
        if params.get("InstanceConf") is not None:
            self.InstanceConf = InstanceConfs()
            self.InstanceConf._deserialize(params.get("InstanceConf"))
        self.DeadlineTime = params.get("DeadlineTime")
        self.IsSupported = params.get("IsSupported")
        self.SecAuditStatus = params.get("SecAuditStatus")
        self.AuditPolicyStatus = params.get("AuditPolicyStatus")
        self.AuditRunningStatus = params.get("AuditRunningStatus")


class IssueTypeInfo(AbstractModel):
    """Metric information

    """

    def __init__(self):
        """
        :param IssueType: Metric categories: AVAILABILITY, MAINTAINABILITY, PERFORMANCE, and RELIABILITY
        :type IssueType: str
        :param Events: Exception
        :type Events: list of EventInfo
        :param TotalCount: Total number of the exceptions
        :type TotalCount: int
        """
        self.IssueType = None
        self.Events = None
        self.TotalCount = None


    def _deserialize(self, params):
        self.IssueType = params.get("IssueType")
        if params.get("Events") is not None:
            self.Events = []
            for item in params.get("Events"):
                obj = EventInfo()
                obj._deserialize(item)
                self.Events.append(obj)
        self.TotalCount = params.get("TotalCount")


class MailConfiguration(AbstractModel):
    """Email sending configuration.

    """

    def __init__(self):
        """
        :param SendMail: Whether to enable email sending. Valid values: 0 (No), 1 (Yes).
        :type SendMail: int
        :param Region: Region configuration, such as "ap-guangzhou", "ap-shanghai". For the inspection email sending template, configure the region where you need to send the inspection email. For the subscription email sending template, configure the region to which the current subscribed instance belongs.
        :type Region: list of str
        :param HealthStatus: Sending a report with the specified health level, such as "HEALTH", "SUB_HEALTH", "RISK", "HIGH_RISK".
        :type HealthStatus: list of str
        :param ContactPerson: Contact ID. Either `ContactGroup` or `ContactID` should be passed in.
        :type ContactPerson: list of int
        :param ContactGroup: Contact group ID. Either `ContactGroup` or `ContactID` should be passed in.
        :type ContactGroup: list of int
        """
        self.SendMail = None
        self.Region = None
        self.HealthStatus = None
        self.ContactPerson = None
        self.ContactGroup = None


    def _deserialize(self, params):
        self.SendMail = params.get("SendMail")
        self.Region = params.get("Region")
        self.HealthStatus = params.get("HealthStatus")
        self.ContactPerson = params.get("ContactPerson")
        self.ContactGroup = params.get("ContactGroup")


class ModifyDiagDBInstanceConfRequest(AbstractModel):
    """ModifyDiagDBInstanceConf request structure.

    """

    def __init__(self):
        """
        :param InstanceConfs: Whether to enable inspection
        :type InstanceConfs: :class:`tencentcloud.dbbrain.v20191016.models.InstanceConfs`
        :param Regions: Target regions of the request. If the value is `All`, it is applied to all regions.
        :type Regions: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TencentDB for CynosDB (compatible with MySQL)).
        :type Product: str
        :param InstanceIds: ID of the instance to modify.
        :type InstanceIds: list of str
        """
        self.InstanceConfs = None
        self.Regions = None
        self.Product = None
        self.InstanceIds = None


    def _deserialize(self, params):
        if params.get("InstanceConfs") is not None:
            self.InstanceConfs = InstanceConfs()
            self.InstanceConfs._deserialize(params.get("InstanceConfs"))
        self.Regions = params.get("Regions")
        self.Product = params.get("Product")
        self.InstanceIds = params.get("InstanceIds")


class ModifyDiagDBInstanceConfResponse(AbstractModel):
    """ModifyDiagDBInstanceConf response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class MonitorFloatMetric(AbstractModel):
    """Monitoring data in float type

    """

    def __init__(self):
        """
        :param Metric: Metric name.
        :type Metric: str
        :param Unit: Metric unit.
        :type Unit: str
        :param Values: Metric value.
Note: this field may return null, indicating that no valid values can be obtained.
        :type Values: list of float
        """
        self.Metric = None
        self.Unit = None
        self.Values = None


    def _deserialize(self, params):
        self.Metric = params.get("Metric")
        self.Unit = params.get("Unit")
        self.Values = params.get("Values")


class MonitorFloatMetricSeriesData(AbstractModel):
    """Monitoring metric value in float type in a unit of time interval

    """

    def __init__(self):
        """
        :param Series: Monitoring metric.
        :type Series: list of MonitorFloatMetric
        :param Timestamp: Timestamp corresponding to monitoring metric.
        :type Timestamp: list of int
        """
        self.Series = None
        self.Timestamp = None


    def _deserialize(self, params):
        if params.get("Series") is not None:
            self.Series = []
            for item in params.get("Series"):
                obj = MonitorFloatMetric()
                obj._deserialize(item)
                self.Series.append(obj)
        self.Timestamp = params.get("Timestamp")


class MonitorMetric(AbstractModel):
    """Monitoring data

    """

    def __init__(self):
        """
        :param Metric: Metric name.
        :type Metric: str
        :param Unit: Metric unit.
        :type Unit: str
        :param Values: Metric value.
Note: this field may return null, indicating that no valid values can be obtained.
        :type Values: list of int
        """
        self.Metric = None
        self.Unit = None
        self.Values = None


    def _deserialize(self, params):
        self.Metric = params.get("Metric")
        self.Unit = params.get("Unit")
        self.Values = params.get("Values")


class MonitorMetricSeriesData(AbstractModel):
    """Monitoring metric data in specified time range

    """

    def __init__(self):
        """
        :param Series: Monitoring metric.
        :type Series: list of MonitorMetric
        :param Timestamp: Timestamp corresponding to monitoring metric.
        :type Timestamp: list of int
        """
        self.Series = None
        self.Timestamp = None


    def _deserialize(self, params):
        if params.get("Series") is not None:
            self.Series = []
            for item in params.get("Series"):
                obj = MonitorMetric()
                obj._deserialize(item)
                self.Series.append(obj)
        self.Timestamp = params.get("Timestamp")


class ProfileInfo(AbstractModel):
    """Information configured by user.

    """

    def __init__(self):
        """
        :param Language: Language of the email, such as `en`.
        :type Language: str
        :param MailConfiguration: The content of email template.
        :type MailConfiguration: :class:`tencentcloud.dbbrain.v20191016.models.MailConfiguration`
        """
        self.Language = None
        self.MailConfiguration = None


    def _deserialize(self, params):
        self.Language = params.get("Language")
        if params.get("MailConfiguration") is not None:
            self.MailConfiguration = MailConfiguration()
            self.MailConfiguration._deserialize(params.get("MailConfiguration"))


class SchemaItem(AbstractModel):
    """`SchemaItem` array

    """

    def __init__(self):
        """
        :param Schema: Database name
        :type Schema: str
        """
        self.Schema = None


    def _deserialize(self, params):
        self.Schema = params.get("Schema")


class SlowLogTopSqlItem(AbstractModel):
    """Top slow SQL statements

    """

    def __init__(self):
        """
        :param LockTime: Total SQL lock wait time
        :type LockTime: float
        :param LockTimeMax: Maximum lock wait time
        :type LockTimeMax: float
        :param LockTimeMin: Minimum lock wait time
        :type LockTimeMin: float
        :param RowsExamined: Total number of scanned rows
        :type RowsExamined: int
        :param RowsExaminedMax: Maximum number of scanned rows
        :type RowsExaminedMax: int
        :param RowsExaminedMin: Minimum number of scanned rows
        :type RowsExaminedMin: int
        :param QueryTime: Total duration
        :type QueryTime: float
        :param QueryTimeMax: Maximum execution time
        :type QueryTimeMax: float
        :param QueryTimeMin: Minimum execution time
        :type QueryTimeMin: float
        :param RowsSent: Total number of returned rows
        :type RowsSent: int
        :param RowsSentMax: Maximum number of returned rows
        :type RowsSentMax: int
        :param RowsSentMin: Minimum number of returned rows
        :type RowsSentMin: int
        :param ExecTimes: Number of executions
        :type ExecTimes: int
        :param SqlTemplate: SQL template
        :type SqlTemplate: str
        :param SqlText: SQL with parameter (random)
        :type SqlText: str
        :param Schema: Database name
        :type Schema: str
        :param QueryTimeRatio: Ratio of total duration
        :type QueryTimeRatio: float
        :param LockTimeRatio: Ratio of total SQL lock wait time
        :type LockTimeRatio: float
        :param RowsExaminedRatio: Ratio of total number of scanned rows
        :type RowsExaminedRatio: float
        :param RowsSentRatio: Ratio of total number of returned rows
        :type RowsSentRatio: float
        """
        self.LockTime = None
        self.LockTimeMax = None
        self.LockTimeMin = None
        self.RowsExamined = None
        self.RowsExaminedMax = None
        self.RowsExaminedMin = None
        self.QueryTime = None
        self.QueryTimeMax = None
        self.QueryTimeMin = None
        self.RowsSent = None
        self.RowsSentMax = None
        self.RowsSentMin = None
        self.ExecTimes = None
        self.SqlTemplate = None
        self.SqlText = None
        self.Schema = None
        self.QueryTimeRatio = None
        self.LockTimeRatio = None
        self.RowsExaminedRatio = None
        self.RowsSentRatio = None


    def _deserialize(self, params):
        self.LockTime = params.get("LockTime")
        self.LockTimeMax = params.get("LockTimeMax")
        self.LockTimeMin = params.get("LockTimeMin")
        self.RowsExamined = params.get("RowsExamined")
        self.RowsExaminedMax = params.get("RowsExaminedMax")
        self.RowsExaminedMin = params.get("RowsExaminedMin")
        self.QueryTime = params.get("QueryTime")
        self.QueryTimeMax = params.get("QueryTimeMax")
        self.QueryTimeMin = params.get("QueryTimeMin")
        self.RowsSent = params.get("RowsSent")
        self.RowsSentMax = params.get("RowsSentMax")
        self.RowsSentMin = params.get("RowsSentMin")
        self.ExecTimes = params.get("ExecTimes")
        self.SqlTemplate = params.get("SqlTemplate")
        self.SqlText = params.get("SqlText")
        self.Schema = params.get("Schema")
        self.QueryTimeRatio = params.get("QueryTimeRatio")
        self.LockTimeRatio = params.get("LockTimeRatio")
        self.RowsExaminedRatio = params.get("RowsExaminedRatio")
        self.RowsSentRatio = params.get("RowsSentRatio")


class TableSpaceData(AbstractModel):
    """Database table space statistics.

    """

    def __init__(self):
        """
        :param TableName: Table name.
        :type TableName: str
        :param TableSchema: Database name.
        :type TableSchema: str
        :param Engine: Database table storage engine.
        :type Engine: str
        :param DataLength: Data space in MB.
        :type DataLength: float
        :param IndexLength: Index space in MB.
        :type IndexLength: float
        :param DataFree: Fragmented space in MB.
        :type DataFree: float
        :param TotalLength: Total space usage in MB.
        :type TotalLength: float
        :param FragRatio: Fragmented rate (%).
        :type FragRatio: float
        :param TableRows: Number of rows.
        :type TableRows: int
        :param PhysicalFileSize: Size in MB of the physical file exclusive to a table.
        :type PhysicalFileSize: float
        """
        self.TableName = None
        self.TableSchema = None
        self.Engine = None
        self.DataLength = None
        self.IndexLength = None
        self.DataFree = None
        self.TotalLength = None
        self.FragRatio = None
        self.TableRows = None
        self.PhysicalFileSize = None


    def _deserialize(self, params):
        self.TableName = params.get("TableName")
        self.TableSchema = params.get("TableSchema")
        self.Engine = params.get("Engine")
        self.DataLength = params.get("DataLength")
        self.IndexLength = params.get("IndexLength")
        self.DataFree = params.get("DataFree")
        self.TotalLength = params.get("TotalLength")
        self.FragRatio = params.get("FragRatio")
        self.TableRows = params.get("TableRows")
        self.PhysicalFileSize = params.get("PhysicalFileSize")


class TableSpaceTimeSeries(AbstractModel):
    """Time series of database table space data

    """

    def __init__(self):
        """
        :param TableName: Table name.
        :type TableName: str
        :param TableSchema: Database name.
        :type TableSchema: str
        :param Engine: Database table storage engine.
        :type Engine: str
        :param SeriesData: Monitoring metric data in a unit of time interval.
        :type SeriesData: :class:`tencentcloud.dbbrain.v20191016.models.MonitorFloatMetricSeriesData`
        """
        self.TableName = None
        self.TableSchema = None
        self.Engine = None
        self.SeriesData = None


    def _deserialize(self, params):
        self.TableName = params.get("TableName")
        self.TableSchema = params.get("TableSchema")
        self.Engine = params.get("Engine")
        if params.get("SeriesData") is not None:
            self.SeriesData = MonitorFloatMetricSeriesData()
            self.SeriesData._deserialize(params.get("SeriesData"))


class TimeSlice(AbstractModel):
    """Slow log statistics in specified time range

    """

    def __init__(self):
        """
        :param Count: Total number
        :type Count: int
        :param Timestamp: Statistics start time
        :type Timestamp: int
        """
        self.Count = None
        self.Timestamp = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.Timestamp = params.get("Timestamp")


class UserProfile(AbstractModel):
    """Information configured by user, including email configuration.

    """

    def __init__(self):
        """
        :param ProfileId: Configured ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ProfileId: str
        :param ProfileType: Configuration type
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ProfileType: str
        :param ProfileLevel: Configuration level. Valid values: “User” or “Instance”
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ProfileLevel: str
        :param ProfileName: Configuration name
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ProfileName: str
        :param ProfileInfo: Configuration details
        :type ProfileInfo: :class:`tencentcloud.dbbrain.v20191016.models.ProfileInfo`
        """
        self.ProfileId = None
        self.ProfileType = None
        self.ProfileLevel = None
        self.ProfileName = None
        self.ProfileInfo = None


    def _deserialize(self, params):
        self.ProfileId = params.get("ProfileId")
        self.ProfileType = params.get("ProfileType")
        self.ProfileLevel = params.get("ProfileLevel")
        self.ProfileName = params.get("ProfileName")
        if params.get("ProfileInfo") is not None:
            self.ProfileInfo = ProfileInfo()
            self.ProfileInfo._deserialize(params.get("ProfileInfo"))
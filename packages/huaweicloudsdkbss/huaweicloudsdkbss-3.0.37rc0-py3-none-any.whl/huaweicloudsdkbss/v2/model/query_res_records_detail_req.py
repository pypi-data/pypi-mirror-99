# coding: utf-8

import pprint
import re

import six





class QueryResRecordsDetailReq:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'cycle': 'str',
        'cloud_service_type': 'str',
        'resource_type': 'str',
        'region': 'str',
        'res_instance_id': 'str',
        'charge_mode': 'int',
        'bill_type': 'int',
        'enterprise_project_id': 'str',
        'include_zero_record': 'bool',
        'offset': 'int',
        'limit': 'int',
        'method': 'str',
        'sub_customer_id': 'str'
    }

    attribute_map = {
        'cycle': 'cycle',
        'cloud_service_type': 'cloud_service_type',
        'resource_type': 'resource_type',
        'region': 'region',
        'res_instance_id': 'res_instance_id',
        'charge_mode': 'charge_mode',
        'bill_type': 'bill_type',
        'enterprise_project_id': 'enterprise_project_id',
        'include_zero_record': 'include_zero_record',
        'offset': 'offset',
        'limit': 'limit',
        'method': 'method',
        'sub_customer_id': 'sub_customer_id'
    }

    def __init__(self, cycle=None, cloud_service_type=None, resource_type=None, region=None, res_instance_id=None, charge_mode=None, bill_type=None, enterprise_project_id=None, include_zero_record=None, offset=None, limit=None, method=None, sub_customer_id=None):
        """QueryResRecordsDetailReq - a model defined in huaweicloud sdk"""
        
        

        self._cycle = None
        self._cloud_service_type = None
        self._resource_type = None
        self._region = None
        self._res_instance_id = None
        self._charge_mode = None
        self._bill_type = None
        self._enterprise_project_id = None
        self._include_zero_record = None
        self._offset = None
        self._limit = None
        self._method = None
        self._sub_customer_id = None
        self.discriminator = None

        self.cycle = cycle
        if cloud_service_type is not None:
            self.cloud_service_type = cloud_service_type
        if resource_type is not None:
            self.resource_type = resource_type
        if region is not None:
            self.region = region
        if res_instance_id is not None:
            self.res_instance_id = res_instance_id
        if charge_mode is not None:
            self.charge_mode = charge_mode
        if bill_type is not None:
            self.bill_type = bill_type
        if enterprise_project_id is not None:
            self.enterprise_project_id = enterprise_project_id
        if include_zero_record is not None:
            self.include_zero_record = include_zero_record
        if offset is not None:
            self.offset = offset
        if limit is not None:
            self.limit = limit
        if method is not None:
            self.method = method
        if sub_customer_id is not None:
            self.sub_customer_id = sub_customer_id

    @property
    def cycle(self):
        """Gets the cycle of this QueryResRecordsDetailReq.

        查询的资源详单所在账期，格式为YYYY-MM。 示例：2019-01。  说明： 不支持2019年1月份之前的资源详单。

        :return: The cycle of this QueryResRecordsDetailReq.
        :rtype: str
        """
        return self._cycle

    @cycle.setter
    def cycle(self, cycle):
        """Sets the cycle of this QueryResRecordsDetailReq.

        查询的资源详单所在账期，格式为YYYY-MM。 示例：2019-01。  说明： 不支持2019年1月份之前的资源详单。

        :param cycle: The cycle of this QueryResRecordsDetailReq.
        :type: str
        """
        self._cycle = cycle

    @property
    def cloud_service_type(self):
        """Gets the cloud_service_type of this QueryResRecordsDetailReq.

        云服务类型编码，例如ECS的云服务类型编码为“hws.service.type.ec2”。您可以调用查询云服务类型列表接口获取。

        :return: The cloud_service_type of this QueryResRecordsDetailReq.
        :rtype: str
        """
        return self._cloud_service_type

    @cloud_service_type.setter
    def cloud_service_type(self, cloud_service_type):
        """Sets the cloud_service_type of this QueryResRecordsDetailReq.

        云服务类型编码，例如ECS的云服务类型编码为“hws.service.type.ec2”。您可以调用查询云服务类型列表接口获取。

        :param cloud_service_type: The cloud_service_type of this QueryResRecordsDetailReq.
        :type: str
        """
        self._cloud_service_type = cloud_service_type

    @property
    def resource_type(self):
        """Gets the resource_type of this QueryResRecordsDetailReq.

        资源类型编码，例如ECS的VM为“hws.resource.type.vm”。您可以调用查询资源类型列表接口获取。

        :return: The resource_type of this QueryResRecordsDetailReq.
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this QueryResRecordsDetailReq.

        资源类型编码，例如ECS的VM为“hws.resource.type.vm”。您可以调用查询资源类型列表接口获取。

        :param resource_type: The resource_type of this QueryResRecordsDetailReq.
        :type: str
        """
        self._resource_type = resource_type

    @property
    def region(self):
        """Gets the region of this QueryResRecordsDetailReq.

        云服务区编码，例如：“cn-north-1”。具体请参见地区和终端节点对应云服务的“区域”列的值。

        :return: The region of this QueryResRecordsDetailReq.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this QueryResRecordsDetailReq.

        云服务区编码，例如：“cn-north-1”。具体请参见地区和终端节点对应云服务的“区域”列的值。

        :param region: The region of this QueryResRecordsDetailReq.
        :type: str
        """
        self._region = region

    @property
    def res_instance_id(self):
        """Gets the res_instance_id of this QueryResRecordsDetailReq.

        资源实例ID。

        :return: The res_instance_id of this QueryResRecordsDetailReq.
        :rtype: str
        """
        return self._res_instance_id

    @res_instance_id.setter
    def res_instance_id(self, res_instance_id):
        """Sets the res_instance_id of this QueryResRecordsDetailReq.

        资源实例ID。

        :param res_instance_id: The res_instance_id of this QueryResRecordsDetailReq.
        :type: str
        """
        self._res_instance_id = res_instance_id

    @property
    def charge_mode(self):
        """Gets the charge_mode of this QueryResRecordsDetailReq.

        计费模式： 1 : 包年/包月3：按需10：预留实例

        :return: The charge_mode of this QueryResRecordsDetailReq.
        :rtype: int
        """
        return self._charge_mode

    @charge_mode.setter
    def charge_mode(self, charge_mode):
        """Sets the charge_mode of this QueryResRecordsDetailReq.

        计费模式： 1 : 包年/包月3：按需10：预留实例

        :param charge_mode: The charge_mode of this QueryResRecordsDetailReq.
        :type: int
        """
        self._charge_mode = charge_mode

    @property
    def bill_type(self):
        """Gets the bill_type of this QueryResRecordsDetailReq.

        账单类型： 1：消费-新购2：消费-续订3：消费-变更4：退款-退订5：消费-使用8：消费-自动续订9：调账-补偿14：消费-服务支持计划月末扣费16：调账-扣费

        :return: The bill_type of this QueryResRecordsDetailReq.
        :rtype: int
        """
        return self._bill_type

    @bill_type.setter
    def bill_type(self, bill_type):
        """Sets the bill_type of this QueryResRecordsDetailReq.

        账单类型： 1：消费-新购2：消费-续订3：消费-变更4：退款-退订5：消费-使用8：消费-自动续订9：调账-补偿14：消费-服务支持计划月末扣费16：调账-扣费

        :param bill_type: The bill_type of this QueryResRecordsDetailReq.
        :type: int
        """
        self._bill_type = bill_type

    @property
    def enterprise_project_id(self):
        """Gets the enterprise_project_id of this QueryResRecordsDetailReq.

        企业项目标识（企业项目ID）。 default项目对应ID：0未归集（表示该云服务不支持企业项目管理能力）项目对应ID：-1其余项目对应ID获取方法请参见如何获取企业项目ID。

        :return: The enterprise_project_id of this QueryResRecordsDetailReq.
        :rtype: str
        """
        return self._enterprise_project_id

    @enterprise_project_id.setter
    def enterprise_project_id(self, enterprise_project_id):
        """Sets the enterprise_project_id of this QueryResRecordsDetailReq.

        企业项目标识（企业项目ID）。 default项目对应ID：0未归集（表示该云服务不支持企业项目管理能力）项目对应ID：-1其余项目对应ID获取方法请参见如何获取企业项目ID。

        :param enterprise_project_id: The enterprise_project_id of this QueryResRecordsDetailReq.
        :type: str
        """
        self._enterprise_project_id = enterprise_project_id

    @property
    def include_zero_record(self):
        """Gets the include_zero_record of this QueryResRecordsDetailReq.

        返回是否包含应付金额为0的记录。 true: 包含false: 不包含

        :return: The include_zero_record of this QueryResRecordsDetailReq.
        :rtype: bool
        """
        return self._include_zero_record

    @include_zero_record.setter
    def include_zero_record(self, include_zero_record):
        """Sets the include_zero_record of this QueryResRecordsDetailReq.

        返回是否包含应付金额为0的记录。 true: 包含false: 不包含

        :param include_zero_record: The include_zero_record of this QueryResRecordsDetailReq.
        :type: bool
        """
        self._include_zero_record = include_zero_record

    @property
    def offset(self):
        """Gets the offset of this QueryResRecordsDetailReq.

        偏移量，从0开始。默认值为0。

        :return: The offset of this QueryResRecordsDetailReq.
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this QueryResRecordsDetailReq.

        偏移量，从0开始。默认值为0。

        :param offset: The offset of this QueryResRecordsDetailReq.
        :type: int
        """
        self._offset = offset

    @property
    def limit(self):
        """Gets the limit of this QueryResRecordsDetailReq.

        页面大小。默认值为10。

        :return: The limit of this QueryResRecordsDetailReq.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this QueryResRecordsDetailReq.

        页面大小。默认值为10。

        :param limit: The limit of this QueryResRecordsDetailReq.
        :type: int
        """
        self._limit = limit

    @property
    def method(self):
        """Gets the method of this QueryResRecordsDetailReq.

        查询方式。 oneself：客户自己sub_customer：企业子客户all：客户自己和企业子客户 默认为all，如果没有企业子客户，all的时候也是查询客户自己的数据。

        :return: The method of this QueryResRecordsDetailReq.
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method):
        """Sets the method of this QueryResRecordsDetailReq.

        查询方式。 oneself：客户自己sub_customer：企业子客户all：客户自己和企业子客户 默认为all，如果没有企业子客户，all的时候也是查询客户自己的数据。

        :param method: The method of this QueryResRecordsDetailReq.
        :type: str
        """
        self._method = method

    @property
    def sub_customer_id(self):
        """Gets the sub_customer_id of this QueryResRecordsDetailReq.

        企业子账号ID。  说明： 如果method取值不为sub_customer，则该参数无效。如果method取值为sub_customer，则该参数不能为空。

        :return: The sub_customer_id of this QueryResRecordsDetailReq.
        :rtype: str
        """
        return self._sub_customer_id

    @sub_customer_id.setter
    def sub_customer_id(self, sub_customer_id):
        """Sets the sub_customer_id of this QueryResRecordsDetailReq.

        企业子账号ID。  说明： 如果method取值不为sub_customer，则该参数无效。如果method取值为sub_customer，则该参数不能为空。

        :param sub_customer_id: The sub_customer_id of this QueryResRecordsDetailReq.
        :type: str
        """
        self._sub_customer_id = sub_customer_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, QueryResRecordsDetailReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

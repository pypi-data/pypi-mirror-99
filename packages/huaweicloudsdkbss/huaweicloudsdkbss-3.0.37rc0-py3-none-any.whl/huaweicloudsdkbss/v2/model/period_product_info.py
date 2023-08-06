# coding: utf-8

import pprint
import re

import six





class PeriodProductInfo:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'id': 'str',
        'cloud_service_type': 'str',
        'resource_type': 'str',
        'resource_spec': 'str',
        'region': 'str',
        'available_zone': 'str',
        'resource_size': 'int',
        'size_measure_id': 'int',
        'period_type': 'int',
        'period_num': 'int',
        'subscription_num': 'int'
    }

    attribute_map = {
        'id': 'id',
        'cloud_service_type': 'cloud_service_type',
        'resource_type': 'resource_type',
        'resource_spec': 'resource_spec',
        'region': 'region',
        'available_zone': 'available_zone',
        'resource_size': 'resource_size',
        'size_measure_id': 'size_measure_id',
        'period_type': 'period_type',
        'period_num': 'period_num',
        'subscription_num': 'subscription_num'
    }

    def __init__(self, id=None, cloud_service_type=None, resource_type=None, resource_spec=None, region=None, available_zone=None, resource_size=None, size_measure_id=None, period_type=None, period_num=None, subscription_num=None):
        """PeriodProductInfo - a model defined in huaweicloud sdk"""
        
        

        self._id = None
        self._cloud_service_type = None
        self._resource_type = None
        self._resource_spec = None
        self._region = None
        self._available_zone = None
        self._resource_size = None
        self._size_measure_id = None
        self._period_type = None
        self._period_num = None
        self._subscription_num = None
        self.discriminator = None

        self.id = id
        self.cloud_service_type = cloud_service_type
        self.resource_type = resource_type
        self.resource_spec = resource_spec
        self.region = region
        if available_zone is not None:
            self.available_zone = available_zone
        if resource_size is not None:
            self.resource_size = resource_size
        if size_measure_id is not None:
            self.size_measure_id = size_measure_id
        self.period_type = period_type
        self.period_num = period_num
        self.subscription_num = subscription_num

    @property
    def id(self):
        """Gets the id of this PeriodProductInfo.

        ID标识，同一次询价中不能重复，用于标识返回询价结果和请求的映射关系。

        :return: The id of this PeriodProductInfo.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PeriodProductInfo.

        ID标识，同一次询价中不能重复，用于标识返回询价结果和请求的映射关系。

        :param id: The id of this PeriodProductInfo.
        :type: str
        """
        self._id = id

    @property
    def cloud_service_type(self):
        """Gets the cloud_service_type of this PeriodProductInfo.

        云服务类型编码，例如ECS的云服务类型编码为“hws.service.type.ec2”。您可以调用查询云服务类型列表接口获取。

        :return: The cloud_service_type of this PeriodProductInfo.
        :rtype: str
        """
        return self._cloud_service_type

    @cloud_service_type.setter
    def cloud_service_type(self, cloud_service_type):
        """Sets the cloud_service_type of this PeriodProductInfo.

        云服务类型编码，例如ECS的云服务类型编码为“hws.service.type.ec2”。您可以调用查询云服务类型列表接口获取。

        :param cloud_service_type: The cloud_service_type of this PeriodProductInfo.
        :type: str
        """
        self._cloud_service_type = cloud_service_type

    @property
    def resource_type(self):
        """Gets the resource_type of this PeriodProductInfo.

        资源类型编码，例如ECS的VM为“hws.resource.type.vm”。您可以调用查询资源类型列表接口获取。 ResourceType是CloudServiceType中的一种资源，CloudServiceType由多种ResourceType组合提供。

        :return: The resource_type of this PeriodProductInfo.
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this PeriodProductInfo.

        资源类型编码，例如ECS的VM为“hws.resource.type.vm”。您可以调用查询资源类型列表接口获取。 ResourceType是CloudServiceType中的一种资源，CloudServiceType由多种ResourceType组合提供。

        :param resource_type: The resource_type of this PeriodProductInfo.
        :type: str
        """
        self._resource_type = resource_type

    @property
    def resource_spec(self):
        """Gets the resource_spec of this PeriodProductInfo.

        云服务产品的资源规格。如果是VM的资源规格，则需要在规格后面添加“.win”或“.linux”，例如“s2.small.1.linux”。具体请参见对应云服务的相关介绍。

        :return: The resource_spec of this PeriodProductInfo.
        :rtype: str
        """
        return self._resource_spec

    @resource_spec.setter
    def resource_spec(self, resource_spec):
        """Sets the resource_spec of this PeriodProductInfo.

        云服务产品的资源规格。如果是VM的资源规格，则需要在规格后面添加“.win”或“.linux”，例如“s2.small.1.linux”。具体请参见对应云服务的相关介绍。

        :param resource_spec: The resource_spec of this PeriodProductInfo.
        :type: str
        """
        self._resource_spec = resource_spec

    @property
    def region(self):
        """Gets the region of this PeriodProductInfo.

        云服务区编码，例如：“cn-north-1”。具体请参见地区和终端节点对应云服务的“区域”列的值。

        :return: The region of this PeriodProductInfo.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this PeriodProductInfo.

        云服务区编码，例如：“cn-north-1”。具体请参见地区和终端节点对应云服务的“区域”列的值。

        :param region: The region of this PeriodProductInfo.
        :type: str
        """
        self._region = region

    @property
    def available_zone(self):
        """Gets the available_zone of this PeriodProductInfo.

        可用区标识。

        :return: The available_zone of this PeriodProductInfo.
        :rtype: str
        """
        return self._available_zone

    @available_zone.setter
    def available_zone(self, available_zone):
        """Sets the available_zone of this PeriodProductInfo.

        可用区标识。

        :param available_zone: The available_zone of this PeriodProductInfo.
        :type: str
        """
        self._available_zone = available_zone

    @property
    def resource_size(self):
        """Gets the resource_size of this PeriodProductInfo.

        资源容量大小，例如购买的卷大小或带宽大小。 线性产品时该参数不能为空。

        :return: The resource_size of this PeriodProductInfo.
        :rtype: int
        """
        return self._resource_size

    @resource_size.setter
    def resource_size(self, resource_size):
        """Sets the resource_size of this PeriodProductInfo.

        资源容量大小，例如购买的卷大小或带宽大小。 线性产品时该参数不能为空。

        :param resource_size: The resource_size of this PeriodProductInfo.
        :type: int
        """
        self._resource_size = resource_size

    @property
    def size_measure_id(self):
        """Gets the size_measure_id of this PeriodProductInfo.

        资源容量度量标识。 15：Mbps（购买带宽时使用）17：GB（购买云硬盘时使用）14：个 线性产品时该参数不能为空。

        :return: The size_measure_id of this PeriodProductInfo.
        :rtype: int
        """
        return self._size_measure_id

    @size_measure_id.setter
    def size_measure_id(self, size_measure_id):
        """Sets the size_measure_id of this PeriodProductInfo.

        资源容量度量标识。 15：Mbps（购买带宽时使用）17：GB（购买云硬盘时使用）14：个 线性产品时该参数不能为空。

        :param size_measure_id: The size_measure_id of this PeriodProductInfo.
        :type: int
        """
        self._size_measure_id = size_measure_id

    @property
    def period_type(self):
        """Gets the period_type of this PeriodProductInfo.

        订购包年/包月产品的周期类型。 0：天2：月3：年4：小时

        :return: The period_type of this PeriodProductInfo.
        :rtype: int
        """
        return self._period_type

    @period_type.setter
    def period_type(self, period_type):
        """Sets the period_type of this PeriodProductInfo.

        订购包年/包月产品的周期类型。 0：天2：月3：年4：小时

        :param period_type: The period_type of this PeriodProductInfo.
        :type: int
        """
        self._period_type = period_type

    @property
    def period_num(self):
        """Gets the period_num of this PeriodProductInfo.

        订购包年/包月产品的周期数。

        :return: The period_num of this PeriodProductInfo.
        :rtype: int
        """
        return self._period_num

    @period_num.setter
    def period_num(self, period_num):
        """Sets the period_num of this PeriodProductInfo.

        订购包年/包月产品的周期数。

        :param period_num: The period_num of this PeriodProductInfo.
        :type: int
        """
        self._period_num = period_num

    @property
    def subscription_num(self):
        """Gets the subscription_num of this PeriodProductInfo.

        订购包年/包月产品的数量。

        :return: The subscription_num of this PeriodProductInfo.
        :rtype: int
        """
        return self._subscription_num

    @subscription_num.setter
    def subscription_num(self, subscription_num):
        """Sets the subscription_num of this PeriodProductInfo.

        订购包年/包月产品的数量。

        :param subscription_num: The subscription_num of this PeriodProductInfo.
        :type: int
        """
        self._subscription_num = subscription_num

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
        if not isinstance(other, PeriodProductInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

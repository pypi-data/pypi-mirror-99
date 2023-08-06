# coding: utf-8

import pprint
import re

import six





class AdjustRecordV2:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'customer_id': 'str',
        'customer_name': 'str',
        'operation_type': 'str',
        'amount': 'float',
        'currency': 'str',
        'apply_scene': 'str',
        'operation_time': 'str',
        'measure_id': 'int',
        'trans_id': 'str'
    }

    attribute_map = {
        'customer_id': 'customer_id',
        'customer_name': 'customer_name',
        'operation_type': 'operation_type',
        'amount': 'amount',
        'currency': 'currency',
        'apply_scene': 'apply_scene',
        'operation_time': 'operation_time',
        'measure_id': 'measure_id',
        'trans_id': 'trans_id'
    }

    def __init__(self, customer_id=None, customer_name=None, operation_type=None, amount=None, currency=None, apply_scene=None, operation_time=None, measure_id=None, trans_id=None):
        """AdjustRecordV2 - a model defined in huaweicloud sdk"""
        
        

        self._customer_id = None
        self._customer_name = None
        self._operation_type = None
        self._amount = None
        self._currency = None
        self._apply_scene = None
        self._operation_time = None
        self._measure_id = None
        self._trans_id = None
        self.discriminator = None

        if customer_id is not None:
            self.customer_id = customer_id
        if customer_name is not None:
            self.customer_name = customer_name
        if operation_type is not None:
            self.operation_type = operation_type
        if amount is not None:
            self.amount = amount
        if currency is not None:
            self.currency = currency
        if apply_scene is not None:
            self.apply_scene = apply_scene
        if operation_time is not None:
            self.operation_time = operation_time
        if measure_id is not None:
            self.measure_id = measure_id
        if trans_id is not None:
            self.trans_id = trans_id

    @property
    def customer_id(self):
        """Gets the customer_id of this AdjustRecordV2.

        客户账号ID。

        :return: The customer_id of this AdjustRecordV2.
        :rtype: str
        """
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        """Sets the customer_id of this AdjustRecordV2.

        客户账号ID。

        :param customer_id: The customer_id of this AdjustRecordV2.
        :type: str
        """
        self._customer_id = customer_id

    @property
    def customer_name(self):
        """Gets the customer_name of this AdjustRecordV2.

        客户名称。

        :return: The customer_name of this AdjustRecordV2.
        :rtype: str
        """
        return self._customer_name

    @customer_name.setter
    def customer_name(self, customer_name):
        """Sets the customer_name of this AdjustRecordV2.

        客户名称。

        :param customer_name: The customer_name of this AdjustRecordV2.
        :type: str
        """
        self._customer_name = customer_name

    @property
    def operation_type(self):
        """Gets the operation_type of this AdjustRecordV2.

        调账类型。 SOURCE_OPERATION_BEADJUST：拨款SOURCE_OPERATION_BERETRIEVE：回收SOURCE_OPERATION_BEUNBIND：解绑回收

        :return: The operation_type of this AdjustRecordV2.
        :rtype: str
        """
        return self._operation_type

    @operation_type.setter
    def operation_type(self, operation_type):
        """Sets the operation_type of this AdjustRecordV2.

        调账类型。 SOURCE_OPERATION_BEADJUST：拨款SOURCE_OPERATION_BERETRIEVE：回收SOURCE_OPERATION_BEUNBIND：解绑回收

        :param operation_type: The operation_type of this AdjustRecordV2.
        :type: str
        """
        self._operation_type = operation_type

    @property
    def amount(self):
        """Gets the amount of this AdjustRecordV2.

        调账的总金额。

        :return: The amount of this AdjustRecordV2.
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this AdjustRecordV2.

        调账的总金额。

        :param amount: The amount of this AdjustRecordV2.
        :type: float
        """
        self._amount = amount

    @property
    def currency(self):
        """Gets the currency of this AdjustRecordV2.

        币种。 CNY：人民币

        :return: The currency of this AdjustRecordV2.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this AdjustRecordV2.

        币种。 CNY：人民币

        :param currency: The currency of this AdjustRecordV2.
        :type: str
        """
        self._currency = currency

    @property
    def apply_scene(self):
        """Gets the apply_scene of this AdjustRecordV2.

        使用场景。

        :return: The apply_scene of this AdjustRecordV2.
        :rtype: str
        """
        return self._apply_scene

    @apply_scene.setter
    def apply_scene(self, apply_scene):
        """Sets the apply_scene of this AdjustRecordV2.

        使用场景。

        :param apply_scene: The apply_scene of this AdjustRecordV2.
        :type: str
        """
        self._apply_scene = apply_scene

    @property
    def operation_time(self):
        """Gets the operation_time of this AdjustRecordV2.

        调账操作的时间。 UTC时间，格式为：2016-03-28T14:45:38Z

        :return: The operation_time of this AdjustRecordV2.
        :rtype: str
        """
        return self._operation_time

    @operation_time.setter
    def operation_time(self, operation_time):
        """Sets the operation_time of this AdjustRecordV2.

        调账操作的时间。 UTC时间，格式为：2016-03-28T14:45:38Z

        :param operation_time: The operation_time of this AdjustRecordV2.
        :type: str
        """
        self._operation_time = operation_time

    @property
    def measure_id(self):
        """Gets the measure_id of this AdjustRecordV2.

        调账单位。 1：元

        :return: The measure_id of this AdjustRecordV2.
        :rtype: int
        """
        return self._measure_id

    @measure_id.setter
    def measure_id(self, measure_id):
        """Sets the measure_id of this AdjustRecordV2.

        调账单位。 1：元

        :param measure_id: The measure_id of this AdjustRecordV2.
        :type: int
        """
        self._measure_id = measure_id

    @property
    def trans_id(self):
        """Gets the trans_id of this AdjustRecordV2.

        事务ID。

        :return: The trans_id of this AdjustRecordV2.
        :rtype: str
        """
        return self._trans_id

    @trans_id.setter
    def trans_id(self, trans_id):
        """Sets the trans_id of this AdjustRecordV2.

        事务ID。

        :param trans_id: The trans_id of this AdjustRecordV2.
        :type: str
        """
        self._trans_id = trans_id

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
        if not isinstance(other, AdjustRecordV2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

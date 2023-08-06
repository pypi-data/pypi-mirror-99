# coding: utf-8

import pprint
import re

import six





class ReclaimToPartnerAccountBalancesReq:


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
        'amount': 'float',
        'indirect_partner_id': 'str'
    }

    attribute_map = {
        'customer_id': 'customer_id',
        'amount': 'amount',
        'indirect_partner_id': 'indirect_partner_id'
    }

    def __init__(self, customer_id=None, amount=None, indirect_partner_id=None):
        """ReclaimToPartnerAccountBalancesReq - a model defined in huaweicloud sdk"""
        
        

        self._customer_id = None
        self._amount = None
        self._indirect_partner_id = None
        self.discriminator = None

        self.customer_id = customer_id
        self.amount = amount
        if indirect_partner_id is not None:
            self.indirect_partner_id = indirect_partner_id

    @property
    def customer_id(self):
        """Gets the customer_id of this ReclaimToPartnerAccountBalancesReq.

        客户账号ID。您可以调用查询客户列表接口获取customer_id。

        :return: The customer_id of this ReclaimToPartnerAccountBalancesReq.
        :rtype: str
        """
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        """Sets the customer_id of this ReclaimToPartnerAccountBalancesReq.

        客户账号ID。您可以调用查询客户列表接口获取customer_id。

        :param customer_id: The customer_id of this ReclaimToPartnerAccountBalancesReq.
        :type: str
        """
        self._customer_id = customer_id

    @property
    def amount(self):
        """Gets the amount of this ReclaimToPartnerAccountBalancesReq.

        回收的金额。 单位：元。取值大于0且精确到小数点后2位。

        :return: The amount of this ReclaimToPartnerAccountBalancesReq.
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this ReclaimToPartnerAccountBalancesReq.

        回收的金额。 单位：元。取值大于0且精确到小数点后2位。

        :param amount: The amount of this ReclaimToPartnerAccountBalancesReq.
        :type: float
        """
        self._amount = amount

    @property
    def indirect_partner_id(self):
        """Gets the indirect_partner_id of this ReclaimToPartnerAccountBalancesReq.

        精英服务商ID。 华为云伙伴能力中心（一级经销商）回收精英服务商（二级经销商）的子客户账户余额时，需携带此参数；否则只能回收自己的子客户账户余额。

        :return: The indirect_partner_id of this ReclaimToPartnerAccountBalancesReq.
        :rtype: str
        """
        return self._indirect_partner_id

    @indirect_partner_id.setter
    def indirect_partner_id(self, indirect_partner_id):
        """Sets the indirect_partner_id of this ReclaimToPartnerAccountBalancesReq.

        精英服务商ID。 华为云伙伴能力中心（一级经销商）回收精英服务商（二级经销商）的子客户账户余额时，需携带此参数；否则只能回收自己的子客户账户余额。

        :param indirect_partner_id: The indirect_partner_id of this ReclaimToPartnerAccountBalancesReq.
        :type: str
        """
        self._indirect_partner_id = indirect_partner_id

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
        if not isinstance(other, ReclaimToPartnerAccountBalancesReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

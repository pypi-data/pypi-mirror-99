# coding: utf-8

import pprint
import re

import six





class ReclaimIndirectPartnerAccountReq:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'indirect_partner_id': 'str',
        'amount': 'float'
    }

    attribute_map = {
        'indirect_partner_id': 'indirect_partner_id',
        'amount': 'amount'
    }

    def __init__(self, indirect_partner_id=None, amount=None):
        """ReclaimIndirectPartnerAccountReq - a model defined in huaweicloud sdk"""
        
        

        self._indirect_partner_id = None
        self._amount = None
        self.discriminator = None

        self.indirect_partner_id = indirect_partner_id
        self.amount = amount

    @property
    def indirect_partner_id(self):
        """Gets the indirect_partner_id of this ReclaimIndirectPartnerAccountReq.

        精英服务商ID。

        :return: The indirect_partner_id of this ReclaimIndirectPartnerAccountReq.
        :rtype: str
        """
        return self._indirect_partner_id

    @indirect_partner_id.setter
    def indirect_partner_id(self, indirect_partner_id):
        """Sets the indirect_partner_id of this ReclaimIndirectPartnerAccountReq.

        精英服务商ID。

        :param indirect_partner_id: The indirect_partner_id of this ReclaimIndirectPartnerAccountReq.
        :type: str
        """
        self._indirect_partner_id = indirect_partner_id

    @property
    def amount(self):
        """Gets the amount of this ReclaimIndirectPartnerAccountReq.

        回收金额。 华为云伙伴能力中心回收的精英服务商的账户金额。 说明： 回收金额不能大于精英服务商的账户余额。 单位：元。取值大于0且精确到小数点后2位。

        :return: The amount of this ReclaimIndirectPartnerAccountReq.
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this ReclaimIndirectPartnerAccountReq.

        回收金额。 华为云伙伴能力中心回收的精英服务商的账户金额。 说明： 回收金额不能大于精英服务商的账户余额。 单位：元。取值大于0且精确到小数点后2位。

        :param amount: The amount of this ReclaimIndirectPartnerAccountReq.
        :type: float
        """
        self._amount = amount

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
        if not isinstance(other, ReclaimIndirectPartnerAccountReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

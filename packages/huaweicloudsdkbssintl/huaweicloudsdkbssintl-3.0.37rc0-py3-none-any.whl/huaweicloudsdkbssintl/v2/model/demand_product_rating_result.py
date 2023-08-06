# coding: utf-8

import pprint
import re

import six





class DemandProductRatingResult:


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
        'product_id': 'str',
        'amount': 'float',
        'discount_amount': 'float',
        'official_website_amount': 'float',
        'measure_id': 'int',
        'discount_rating_results': 'list[DemandDiscountRatingResult]'
    }

    attribute_map = {
        'id': 'id',
        'product_id': 'product_id',
        'amount': 'amount',
        'discount_amount': 'discount_amount',
        'official_website_amount': 'official_website_amount',
        'measure_id': 'measure_id',
        'discount_rating_results': 'discount_rating_results'
    }

    def __init__(self, id=None, product_id=None, amount=None, discount_amount=None, official_website_amount=None, measure_id=None, discount_rating_results=None):
        """DemandProductRatingResult - a model defined in huaweicloud sdk"""
        
        

        self._id = None
        self._product_id = None
        self._amount = None
        self._discount_amount = None
        self._official_website_amount = None
        self._measure_id = None
        self._discount_rating_results = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if product_id is not None:
            self.product_id = product_id
        if amount is not None:
            self.amount = amount
        if discount_amount is not None:
            self.discount_amount = discount_amount
        if official_website_amount is not None:
            self.official_website_amount = official_website_amount
        if measure_id is not None:
            self.measure_id = measure_id
        if discount_rating_results is not None:
            self.discount_rating_results = discount_rating_results

    @property
    def id(self):
        """Gets the id of this DemandProductRatingResult.

        |参数名称：ID标识| |参数约束及描述：同一次询价中不能重复，用于标识返回询价结果和请求的映射关系|

        :return: The id of this DemandProductRatingResult.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DemandProductRatingResult.

        |参数名称：ID标识| |参数约束及描述：同一次询价中不能重复，用于标识返回询价结果和请求的映射关系|

        :param id: The id of this DemandProductRatingResult.
        :type: str
        """
        self._id = id

    @property
    def product_id(self):
        """Gets the product_id of this DemandProductRatingResult.

        |参数名称：寻到的产品ID| |参数约束及描述：寻到的产品ID|

        :return: The product_id of this DemandProductRatingResult.
        :rtype: str
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        """Sets the product_id of this DemandProductRatingResult.

        |参数名称：寻到的产品ID| |参数约束及描述：寻到的产品ID|

        :param product_id: The product_id of this DemandProductRatingResult.
        :type: str
        """
        self._product_id = product_id

    @property
    def amount(self):
        """Gets the amount of this DemandProductRatingResult.

        |参数名称：总额| |参数约束及描述：即最终优惠的金额|

        :return: The amount of this DemandProductRatingResult.
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this DemandProductRatingResult.

        |参数名称：总额| |参数约束及描述：即最终优惠的金额|

        :param amount: The amount of this DemandProductRatingResult.
        :type: float
        """
        self._amount = amount

    @property
    def discount_amount(self):
        """Gets the discount_amount of this DemandProductRatingResult.

        |参数名称：优惠额（官网价和总价的差）| |参数约束及描述：优惠额（官网价和总价的差）|

        :return: The discount_amount of this DemandProductRatingResult.
        :rtype: float
        """
        return self._discount_amount

    @discount_amount.setter
    def discount_amount(self, discount_amount):
        """Sets the discount_amount of this DemandProductRatingResult.

        |参数名称：优惠额（官网价和总价的差）| |参数约束及描述：优惠额（官网价和总价的差）|

        :param discount_amount: The discount_amount of this DemandProductRatingResult.
        :type: float
        """
        self._discount_amount = discount_amount

    @property
    def official_website_amount(self):
        """Gets the official_website_amount of this DemandProductRatingResult.

        |参数名称：官网价| |参数约束及描述：官网价|

        :return: The official_website_amount of this DemandProductRatingResult.
        :rtype: float
        """
        return self._official_website_amount

    @official_website_amount.setter
    def official_website_amount(self, official_website_amount):
        """Sets the official_website_amount of this DemandProductRatingResult.

        |参数名称：官网价| |参数约束及描述：官网价|

        :param official_website_amount: The official_website_amount of this DemandProductRatingResult.
        :type: float
        """
        self._official_website_amount = official_website_amount

    @property
    def measure_id(self):
        """Gets the measure_id of this DemandProductRatingResult.

        |参数名称：度量单位标识| |参数约束及描述：1：元|

        :return: The measure_id of this DemandProductRatingResult.
        :rtype: int
        """
        return self._measure_id

    @measure_id.setter
    def measure_id(self, measure_id):
        """Sets the measure_id of this DemandProductRatingResult.

        |参数名称：度量单位标识| |参数约束及描述：1：元|

        :param measure_id: The measure_id of this DemandProductRatingResult.
        :type: int
        """
        self._measure_id = measure_id

    @property
    def discount_rating_results(self):
        """Gets the discount_rating_results of this DemandProductRatingResult.

        |参数名称：折扣优惠明细| |参数的约束及描述：包含产品本身的促销信息，同时包含商务或者伙伴折扣的优惠信息|

        :return: The discount_rating_results of this DemandProductRatingResult.
        :rtype: list[DemandDiscountRatingResult]
        """
        return self._discount_rating_results

    @discount_rating_results.setter
    def discount_rating_results(self, discount_rating_results):
        """Sets the discount_rating_results of this DemandProductRatingResult.

        |参数名称：折扣优惠明细| |参数的约束及描述：包含产品本身的促销信息，同时包含商务或者伙伴折扣的优惠信息|

        :param discount_rating_results: The discount_rating_results of this DemandProductRatingResult.
        :type: list[DemandDiscountRatingResult]
        """
        self._discount_rating_results = discount_rating_results

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
        if not isinstance(other, DemandProductRatingResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

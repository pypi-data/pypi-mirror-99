# coding: utf-8

"""
    MateCat API

    We developed a set of Rest API to let you integrate Matecat in your translation management system or in any other application. Use our API to create projects and check their status.  # noqa: E501

    OpenAPI spec version: 2.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class OutsourceConfirmation(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'create_timestamp': 'datetime',
        'delivery_timestamp': 'int',
        'quote_review_link': 'object'
    }

    attribute_map = {
        'create_timestamp': 'create_timestamp',
        'delivery_timestamp': 'delivery_timestamp',
        'quote_review_link': 'quote_review_link'
    }

    def __init__(self, create_timestamp=None, delivery_timestamp=None, quote_review_link=None):  # noqa: E501
        """OutsourceConfirmation - a model defined in Swagger"""  # noqa: E501
        self._create_timestamp = None
        self._delivery_timestamp = None
        self._quote_review_link = None
        self.discriminator = None
        if create_timestamp is not None:
            self.create_timestamp = create_timestamp
        if delivery_timestamp is not None:
            self.delivery_timestamp = delivery_timestamp
        if quote_review_link is not None:
            self.quote_review_link = quote_review_link

    @property
    def create_timestamp(self):
        """Gets the create_timestamp of this OutsourceConfirmation.  # noqa: E501


        :return: The create_timestamp of this OutsourceConfirmation.  # noqa: E501
        :rtype: datetime
        """
        return self._create_timestamp

    @create_timestamp.setter
    def create_timestamp(self, create_timestamp):
        """Sets the create_timestamp of this OutsourceConfirmation.


        :param create_timestamp: The create_timestamp of this OutsourceConfirmation.  # noqa: E501
        :type: datetime
        """

        self._create_timestamp = create_timestamp

    @property
    def delivery_timestamp(self):
        """Gets the delivery_timestamp of this OutsourceConfirmation.  # noqa: E501


        :return: The delivery_timestamp of this OutsourceConfirmation.  # noqa: E501
        :rtype: int
        """
        return self._delivery_timestamp

    @delivery_timestamp.setter
    def delivery_timestamp(self, delivery_timestamp):
        """Sets the delivery_timestamp of this OutsourceConfirmation.


        :param delivery_timestamp: The delivery_timestamp of this OutsourceConfirmation.  # noqa: E501
        :type: int
        """

        self._delivery_timestamp = delivery_timestamp

    @property
    def quote_review_link(self):
        """Gets the quote_review_link of this OutsourceConfirmation.  # noqa: E501


        :return: The quote_review_link of this OutsourceConfirmation.  # noqa: E501
        :rtype: object
        """
        return self._quote_review_link

    @quote_review_link.setter
    def quote_review_link(self, quote_review_link):
        """Sets the quote_review_link of this OutsourceConfirmation.


        :param quote_review_link: The quote_review_link of this OutsourceConfirmation.  # noqa: E501
        :type: object
        """

        self._quote_review_link = quote_review_link

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
                result[attr] = value
        if issubclass(OutsourceConfirmation, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OutsourceConfirmation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

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

class Body5(object):
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
        'email': 'str',
        'delivery_date': 'int',
        'timezone': 'str'
    }

    attribute_map = {
        'email': 'email',
        'delivery_date': 'delivery_date',
        'timezone': 'timezone'
    }

    def __init__(self, email=None, delivery_date=None, timezone=None):  # noqa: E501
        """Body5 - a model defined in Swagger"""  # noqa: E501
        self._email = None
        self._delivery_date = None
        self._timezone = None
        self.discriminator = None
        self.email = email
        self.delivery_date = delivery_date
        self.timezone = timezone

    @property
    def email(self):
        """Gets the email of this Body5.  # noqa: E501

        email of the translator to assign the job  # noqa: E501

        :return: The email of this Body5.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this Body5.

        email of the translator to assign the job  # noqa: E501

        :param email: The email of this Body5.  # noqa: E501
        :type: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def delivery_date(self):
        """Gets the delivery_date of this Body5.  # noqa: E501

        deliery date for the assignment, expressed as timestamp  # noqa: E501

        :return: The delivery_date of this Body5.  # noqa: E501
        :rtype: int
        """
        return self._delivery_date

    @delivery_date.setter
    def delivery_date(self, delivery_date):
        """Sets the delivery_date of this Body5.

        deliery date for the assignment, expressed as timestamp  # noqa: E501

        :param delivery_date: The delivery_date of this Body5.  # noqa: E501
        :type: int
        """
        if delivery_date is None:
            raise ValueError("Invalid value for `delivery_date`, must not be `None`")  # noqa: E501

        self._delivery_date = delivery_date

    @property
    def timezone(self):
        """Gets the timezone of this Body5.  # noqa: E501

        time zone to convert the delivery_date param expressed as offset based on UTC. Example 1.0, -7.0 etc.  # noqa: E501

        :return: The timezone of this Body5.  # noqa: E501
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """Sets the timezone of this Body5.

        time zone to convert the delivery_date param expressed as offset based on UTC. Example 1.0, -7.0 etc.  # noqa: E501

        :param timezone: The timezone of this Body5.  # noqa: E501
        :type: str
        """
        if timezone is None:
            raise ValueError("Invalid value for `timezone`, must not be `None`")  # noqa: E501

        self._timezone = timezone

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
        if issubclass(Body5, dict):
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
        if not isinstance(other, Body5):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

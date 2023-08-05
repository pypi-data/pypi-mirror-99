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

class TeamMember(object):
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
        'id': 'int',
        'id_team': 'int',
        'user': 'User'
    }

    attribute_map = {
        'id': 'id',
        'id_team': 'id_team',
        'user': 'user'
    }

    def __init__(self, id=None, id_team=None, user=None):  # noqa: E501
        """TeamMember - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._id_team = None
        self._user = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if id_team is not None:
            self.id_team = id_team
        if user is not None:
            self.user = user

    @property
    def id(self):
        """Gets the id of this TeamMember.  # noqa: E501


        :return: The id of this TeamMember.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this TeamMember.


        :param id: The id of this TeamMember.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def id_team(self):
        """Gets the id_team of this TeamMember.  # noqa: E501


        :return: The id_team of this TeamMember.  # noqa: E501
        :rtype: int
        """
        return self._id_team

    @id_team.setter
    def id_team(self, id_team):
        """Sets the id_team of this TeamMember.


        :param id_team: The id_team of this TeamMember.  # noqa: E501
        :type: int
        """

        self._id_team = id_team

    @property
    def user(self):
        """Gets the user of this TeamMember.  # noqa: E501


        :return: The user of this TeamMember.  # noqa: E501
        :rtype: User
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this TeamMember.


        :param user: The user of this TeamMember.  # noqa: E501
        :type: User
        """

        self._user = user

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
        if issubclass(TeamMember, dict):
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
        if not isinstance(other, TeamMember):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

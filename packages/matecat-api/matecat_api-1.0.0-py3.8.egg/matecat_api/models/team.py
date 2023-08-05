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

class Team(object):
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
        'name': 'str',
        'type': 'str',
        'created_at': 'datetime',
        'created_by': 'int',
        'pending_invitations': 'list[object]'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'type': 'type',
        'created_at': 'created_at',
        'created_by': 'created_by',
        'pending_invitations': 'pending_invitations'
    }

    def __init__(self, id=None, name=None, type=None, created_at=None, created_by=None, pending_invitations=None):  # noqa: E501
        """Team - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._type = None
        self._created_at = None
        self._created_by = None
        self._pending_invitations = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if type is not None:
            self.type = type
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if pending_invitations is not None:
            self.pending_invitations = pending_invitations

    @property
    def id(self):
        """Gets the id of this Team.  # noqa: E501


        :return: The id of this Team.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Team.


        :param id: The id of this Team.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Team.  # noqa: E501


        :return: The name of this Team.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Team.


        :param name: The name of this Team.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def type(self):
        """Gets the type of this Team.  # noqa: E501


        :return: The type of this Team.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Team.


        :param type: The type of this Team.  # noqa: E501
        :type: str
        """
        allowed_values = ["general", "personal"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def created_at(self):
        """Gets the created_at of this Team.  # noqa: E501


        :return: The created_at of this Team.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Team.


        :param created_at: The created_at of this Team.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this Team.  # noqa: E501


        :return: The created_by of this Team.  # noqa: E501
        :rtype: int
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this Team.


        :param created_by: The created_by of this Team.  # noqa: E501
        :type: int
        """

        self._created_by = created_by

    @property
    def pending_invitations(self):
        """Gets the pending_invitations of this Team.  # noqa: E501


        :return: The pending_invitations of this Team.  # noqa: E501
        :rtype: list[object]
        """
        return self._pending_invitations

    @pending_invitations.setter
    def pending_invitations(self, pending_invitations):
        """Sets the pending_invitations of this Team.


        :param pending_invitations: The pending_invitations of this Team.  # noqa: E501
        :type: list[object]
        """

        self._pending_invitations = pending_invitations

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
        if issubclass(Team, dict):
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
        if not isinstance(other, Team):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

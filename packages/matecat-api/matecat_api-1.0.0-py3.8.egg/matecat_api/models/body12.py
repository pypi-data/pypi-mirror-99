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

class Body12(object):
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
        'comment': 'str',
        'id_qa_entry': 'str',
        'source_page': 'str',
        'uid': 'str'
    }

    attribute_map = {
        'comment': 'comment',
        'id_qa_entry': 'id_qa_entry',
        'source_page': 'source_page',
        'uid': 'uid'
    }

    def __init__(self, comment=None, id_qa_entry=None, source_page=None, uid=None):  # noqa: E501
        """Body12 - a model defined in Swagger"""  # noqa: E501
        self._comment = None
        self._id_qa_entry = None
        self._source_page = None
        self._uid = None
        self.discriminator = None
        self.comment = comment
        self.id_qa_entry = id_qa_entry
        self.source_page = source_page
        self.uid = uid

    @property
    def comment(self):
        """Gets the comment of this Body12.  # noqa: E501


        :return: The comment of this Body12.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this Body12.


        :param comment: The comment of this Body12.  # noqa: E501
        :type: str
        """
        if comment is None:
            raise ValueError("Invalid value for `comment`, must not be `None`")  # noqa: E501

        self._comment = comment

    @property
    def id_qa_entry(self):
        """Gets the id_qa_entry of this Body12.  # noqa: E501


        :return: The id_qa_entry of this Body12.  # noqa: E501
        :rtype: str
        """
        return self._id_qa_entry

    @id_qa_entry.setter
    def id_qa_entry(self, id_qa_entry):
        """Sets the id_qa_entry of this Body12.


        :param id_qa_entry: The id_qa_entry of this Body12.  # noqa: E501
        :type: str
        """
        if id_qa_entry is None:
            raise ValueError("Invalid value for `id_qa_entry`, must not be `None`")  # noqa: E501

        self._id_qa_entry = id_qa_entry

    @property
    def source_page(self):
        """Gets the source_page of this Body12.  # noqa: E501


        :return: The source_page of this Body12.  # noqa: E501
        :rtype: str
        """
        return self._source_page

    @source_page.setter
    def source_page(self, source_page):
        """Sets the source_page of this Body12.


        :param source_page: The source_page of this Body12.  # noqa: E501
        :type: str
        """
        if source_page is None:
            raise ValueError("Invalid value for `source_page`, must not be `None`")  # noqa: E501

        self._source_page = source_page

    @property
    def uid(self):
        """Gets the uid of this Body12.  # noqa: E501


        :return: The uid of this Body12.  # noqa: E501
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this Body12.


        :param uid: The uid of this Body12.  # noqa: E501
        :type: str
        """
        if uid is None:
            raise ValueError("Invalid value for `uid`, must not be `None`")  # noqa: E501

        self._uid = uid

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
        if issubclass(Body12, dict):
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
        if not isinstance(other, Body12):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

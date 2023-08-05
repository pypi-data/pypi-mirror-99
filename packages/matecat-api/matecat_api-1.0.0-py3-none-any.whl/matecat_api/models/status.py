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

class Status(object):
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
        'errors': 'list[object]',
        'data': 'DataStatus',
        'status': 'str',
        'analyze': 'str',
        'jobs': 'JobsStatus'
    }

    attribute_map = {
        'errors': 'errors',
        'data': 'data',
        'status': 'status',
        'analyze': 'analyze',
        'jobs': 'jobs'
    }

    def __init__(self, errors=None, data=None, status=None, analyze=None, jobs=None):  # noqa: E501
        """Status - a model defined in Swagger"""  # noqa: E501
        self._errors = None
        self._data = None
        self._status = None
        self._analyze = None
        self._jobs = None
        self.discriminator = None
        if errors is not None:
            self.errors = errors
        if data is not None:
            self.data = data
        if status is not None:
            self.status = status
        if analyze is not None:
            self.analyze = analyze
        if jobs is not None:
            self.jobs = jobs

    @property
    def errors(self):
        """Gets the errors of this Status.  # noqa: E501

        A list of objects containing error message at system wide level. Every error has a negative numeric code and a textual message ( currently the only error reported is the wrong version number in config.inc.php file and happens only after Matecat updates, so you should never see it ).  # noqa: E501

        :return: The errors of this Status.  # noqa: E501
        :rtype: list[object]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this Status.

        A list of objects containing error message at system wide level. Every error has a negative numeric code and a textual message ( currently the only error reported is the wrong version number in config.inc.php file and happens only after Matecat updates, so you should never see it ).  # noqa: E501

        :param errors: The errors of this Status.  # noqa: E501
        :type: list[object]
        """

        self._errors = errors

    @property
    def data(self):
        """Gets the data of this Status.  # noqa: E501


        :return: The data of this Status.  # noqa: E501
        :rtype: DataStatus
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this Status.


        :param data: The data of this Status.  # noqa: E501
        :type: DataStatus
        """

        self._data = data

    @property
    def status(self):
        """Gets the status of this Status.  # noqa: E501

        The analysis status of the project. ANALYZING - analysis/creation still in progress; NO_SEGMENTS_FOUND - the project has no segments to analyze (have you uploaded a file containing only images?); ANALYSIS_NOT_ENABLED - no analysis will be performed because of Matecat configuration; DONE - the analysis/creation is completed; FAIL - the analysis/creation is failed.  # noqa: E501

        :return: The status of this Status.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Status.

        The analysis status of the project. ANALYZING - analysis/creation still in progress; NO_SEGMENTS_FOUND - the project has no segments to analyze (have you uploaded a file containing only images?); ANALYSIS_NOT_ENABLED - no analysis will be performed because of Matecat configuration; DONE - the analysis/creation is completed; FAIL - the analysis/creation is failed.  # noqa: E501

        :param status: The status of this Status.  # noqa: E501
        :type: str
        """
        allowed_values = ["ANALYZING", "NO_SEGMENTS_FOUND", "ANALYSIS_NOT_ENABLED", "DONE", "FAIL"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def analyze(self):
        """Gets the analyze of this Status.  # noqa: E501

        A link to the analyze page; it's a human readable version of this API output  # noqa: E501

        :return: The analyze of this Status.  # noqa: E501
        :rtype: str
        """
        return self._analyze

    @analyze.setter
    def analyze(self, analyze):
        """Sets the analyze of this Status.

        A link to the analyze page; it's a human readable version of this API output  # noqa: E501

        :param analyze: The analyze of this Status.  # noqa: E501
        :type: str
        """

        self._analyze = analyze

    @property
    def jobs(self):
        """Gets the jobs of this Status.  # noqa: E501


        :return: The jobs of this Status.  # noqa: E501
        :rtype: JobsStatus
        """
        return self._jobs

    @jobs.setter
    def jobs(self, jobs):
        """Sets the jobs of this Status.


        :param jobs: The jobs of this Status.  # noqa: E501
        :type: JobsStatus
        """

        self._jobs = jobs

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
        if issubclass(Status, dict):
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
        if not isinstance(other, Status):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

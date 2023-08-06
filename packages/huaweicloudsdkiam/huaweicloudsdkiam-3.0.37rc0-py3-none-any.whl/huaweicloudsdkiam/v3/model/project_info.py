# coding: utf-8

import pprint
import re

import six





class ProjectInfo:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'domain': 'DomainInfo',
        'id': 'str',
        'name': 'str'
    }

    attribute_map = {
        'domain': 'domain',
        'id': 'id',
        'name': 'name'
    }

    def __init__(self, domain=None, id=None, name=None):
        """ProjectInfo - a model defined in huaweicloud sdk"""
        
        

        self._domain = None
        self._id = None
        self._name = None
        self.discriminator = None

        if domain is not None:
            self.domain = domain
        if id is not None:
            self.id = id
        self.name = name

    @property
    def domain(self):
        """Gets the domain of this ProjectInfo.


        :return: The domain of this ProjectInfo.
        :rtype: DomainInfo
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this ProjectInfo.


        :param domain: The domain of this ProjectInfo.
        :type: DomainInfo
        """
        self._domain = domain

    @property
    def id(self):
        """Gets the id of this ProjectInfo.

        project id

        :return: The id of this ProjectInfo.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ProjectInfo.

        project id

        :param id: The id of this ProjectInfo.
        :type: str
        """
        self._id = id

    @property
    def name(self):
        """Gets the name of this ProjectInfo.

        project name

        :return: The name of this ProjectInfo.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ProjectInfo.

        project name

        :param name: The name of this ProjectInfo.
        :type: str
        """
        self._name = name

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
        if not isinstance(other, ProjectInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

# coding: utf-8

import pprint
import re

import six





class CopyImageCrossRegionRequestBody:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'agency_name': 'str',
        'description': 'str',
        'name': 'str',
        'project_name': 'str',
        'region': 'str'
    }

    attribute_map = {
        'agency_name': 'agency_name',
        'description': 'description',
        'name': 'name',
        'project_name': 'project_name',
        'region': 'region'
    }

    def __init__(self, agency_name=None, description=None, name=None, project_name=None, region=None):
        """CopyImageCrossRegionRequestBody - a model defined in huaweicloud sdk"""
        
        

        self._agency_name = None
        self._description = None
        self._name = None
        self._project_name = None
        self._region = None
        self.discriminator = None

        self.agency_name = agency_name
        if description is not None:
            self.description = description
        self.name = name
        self.project_name = project_name
        self.region = region

    @property
    def agency_name(self):
        """Gets the agency_name of this CopyImageCrossRegionRequestBody.

        IMS服务委托名称。

        :return: The agency_name of this CopyImageCrossRegionRequestBody.
        :rtype: str
        """
        return self._agency_name

    @agency_name.setter
    def agency_name(self, agency_name):
        """Sets the agency_name of this CopyImageCrossRegionRequestBody.

        IMS服务委托名称。

        :param agency_name: The agency_name of this CopyImageCrossRegionRequestBody.
        :type: str
        """
        self._agency_name = agency_name

    @property
    def description(self):
        """Gets the description of this CopyImageCrossRegionRequestBody.

        镜像描述信息。支持字母、数字、中文等，不支持回车、<、 >，长度不能超过1024个字符。默认为空。

        :return: The description of this CopyImageCrossRegionRequestBody.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CopyImageCrossRegionRequestBody.

        镜像描述信息。支持字母、数字、中文等，不支持回车、<、 >，长度不能超过1024个字符。默认为空。

        :param description: The description of this CopyImageCrossRegionRequestBody.
        :type: str
        """
        self._description = description

    @property
    def name(self):
        """Gets the name of this CopyImageCrossRegionRequestBody.

        镜像名称

        :return: The name of this CopyImageCrossRegionRequestBody.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CopyImageCrossRegionRequestBody.

        镜像名称

        :param name: The name of this CopyImageCrossRegionRequestBody.
        :type: str
        """
        self._name = name

    @property
    def project_name(self):
        """Gets the project_name of this CopyImageCrossRegionRequestBody.

        目的区域的项目名称。

        :return: The project_name of this CopyImageCrossRegionRequestBody.
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this CopyImageCrossRegionRequestBody.

        目的区域的项目名称。

        :param project_name: The project_name of this CopyImageCrossRegionRequestBody.
        :type: str
        """
        self._project_name = project_name

    @property
    def region(self):
        """Gets the region of this CopyImageCrossRegionRequestBody.

        目的区域的Region ID。

        :return: The region of this CopyImageCrossRegionRequestBody.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this CopyImageCrossRegionRequestBody.

        目的区域的Region ID。

        :param region: The region of this CopyImageCrossRegionRequestBody.
        :type: str
        """
        self._region = region

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
        if not isinstance(other, CopyImageCrossRegionRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

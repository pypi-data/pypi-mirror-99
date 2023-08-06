# coding: utf-8

import pprint
import re

import six





class UpdateRepoRequestBody:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'is_public': 'bool',
        'category': 'str',
        'description': 'str'
    }

    attribute_map = {
        'is_public': 'is_public',
        'category': 'category',
        'description': 'description'
    }

    def __init__(self, is_public=None, category=None, description=None):
        """UpdateRepoRequestBody - a model defined in huaweicloud sdk"""
        
        

        self._is_public = None
        self._category = None
        self._description = None
        self.discriminator = None

        self.is_public = is_public
        if category is not None:
            self.category = category
        if description is not None:
            self.description = description

    @property
    def is_public(self):
        """Gets the is_public of this UpdateRepoRequestBody.

        是否为公共仓库，可选值为true或false。

        :return: The is_public of this UpdateRepoRequestBody.
        :rtype: bool
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """Sets the is_public of this UpdateRepoRequestBody.

        是否为公共仓库，可选值为true或false。

        :param is_public: The is_public of this UpdateRepoRequestBody.
        :type: bool
        """
        self._is_public = is_public

    @property
    def category(self):
        """Gets the category of this UpdateRepoRequestBody.

        仓库类型，可设置为app_server, linux, framework_app, database, lang, other, windows, arm。

        :return: The category of this UpdateRepoRequestBody.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this UpdateRepoRequestBody.

        仓库类型，可设置为app_server, linux, framework_app, database, lang, other, windows, arm。

        :param category: The category of this UpdateRepoRequestBody.
        :type: str
        """
        self._category = category

    @property
    def description(self):
        """Gets the description of this UpdateRepoRequestBody.

        镜像仓库的描述信息。

        :return: The description of this UpdateRepoRequestBody.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdateRepoRequestBody.

        镜像仓库的描述信息。

        :param description: The description of this UpdateRepoRequestBody.
        :type: str
        """
        self._description = description

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
        if not isinstance(other, UpdateRepoRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

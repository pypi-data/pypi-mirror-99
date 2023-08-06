# coding: utf-8

import pprint
import re

import six





class CreateManualImageSyncRepoRequestBody:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'image_tag': 'list[str]',
        'override': 'bool',
        'remote_namespace': 'str',
        'remote_region_id': 'str'
    }

    attribute_map = {
        'image_tag': 'imageTag',
        'override': 'override',
        'remote_namespace': 'remoteNamespace',
        'remote_region_id': 'remoteRegionId'
    }

    def __init__(self, image_tag=None, override=None, remote_namespace=None, remote_region_id=None):
        """CreateManualImageSyncRepoRequestBody - a model defined in huaweicloud sdk"""
        
        

        self._image_tag = None
        self._override = None
        self._remote_namespace = None
        self._remote_region_id = None
        self.discriminator = None

        self.image_tag = image_tag
        if override is not None:
            self.override = override
        self.remote_namespace = remote_namespace
        self.remote_region_id = remote_region_id

    @property
    def image_tag(self):
        """Gets the image_tag of this CreateManualImageSyncRepoRequestBody.

        版本列表

        :return: The image_tag of this CreateManualImageSyncRepoRequestBody.
        :rtype: list[str]
        """
        return self._image_tag

    @image_tag.setter
    def image_tag(self, image_tag):
        """Sets the image_tag of this CreateManualImageSyncRepoRequestBody.

        版本列表

        :param image_tag: The image_tag of this CreateManualImageSyncRepoRequestBody.
        :type: list[str]
        """
        self._image_tag = image_tag

    @property
    def override(self):
        """Gets the override of this CreateManualImageSyncRepoRequestBody.

        是否覆盖，默认为false

        :return: The override of this CreateManualImageSyncRepoRequestBody.
        :rtype: bool
        """
        return self._override

    @override.setter
    def override(self, override):
        """Sets the override of this CreateManualImageSyncRepoRequestBody.

        是否覆盖，默认为false

        :param override: The override of this CreateManualImageSyncRepoRequestBody.
        :type: bool
        """
        self._override = override

    @property
    def remote_namespace(self):
        """Gets the remote_namespace of this CreateManualImageSyncRepoRequestBody.

        目标组织

        :return: The remote_namespace of this CreateManualImageSyncRepoRequestBody.
        :rtype: str
        """
        return self._remote_namespace

    @remote_namespace.setter
    def remote_namespace(self, remote_namespace):
        """Sets the remote_namespace of this CreateManualImageSyncRepoRequestBody.

        目标组织

        :param remote_namespace: The remote_namespace of this CreateManualImageSyncRepoRequestBody.
        :type: str
        """
        self._remote_namespace = remote_namespace

    @property
    def remote_region_id(self):
        """Gets the remote_region_id of this CreateManualImageSyncRepoRequestBody.

        目标region ID。

        :return: The remote_region_id of this CreateManualImageSyncRepoRequestBody.
        :rtype: str
        """
        return self._remote_region_id

    @remote_region_id.setter
    def remote_region_id(self, remote_region_id):
        """Sets the remote_region_id of this CreateManualImageSyncRepoRequestBody.

        目标region ID。

        :param remote_region_id: The remote_region_id of this CreateManualImageSyncRepoRequestBody.
        :type: str
        """
        self._remote_region_id = remote_region_id

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
        if not isinstance(other, CreateManualImageSyncRepoRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

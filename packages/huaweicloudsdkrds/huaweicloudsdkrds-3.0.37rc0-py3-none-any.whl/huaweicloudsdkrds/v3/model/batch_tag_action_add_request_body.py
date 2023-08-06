# coding: utf-8

import pprint
import re

import six





class BatchTagActionAddRequestBody:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'action': 'str',
        'tags': 'list[TagWithKeyValue]'
    }

    attribute_map = {
        'action': 'action',
        'tags': 'tags'
    }

    def __init__(self, action=None, tags=None):
        """BatchTagActionAddRequestBody - a model defined in huaweicloud sdk"""
        
        

        self._action = None
        self._tags = None
        self.discriminator = None

        self.action = action
        self.tags = tags

    @property
    def action(self):
        """Gets the action of this BatchTagActionAddRequestBody.

        操作标识（区分大小写）：创建时为“create”。

        :return: The action of this BatchTagActionAddRequestBody.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this BatchTagActionAddRequestBody.

        操作标识（区分大小写）：创建时为“create”。

        :param action: The action of this BatchTagActionAddRequestBody.
        :type: str
        """
        self._action = action

    @property
    def tags(self):
        """Gets the tags of this BatchTagActionAddRequestBody.

        标签列表。单个实例总标签数上限10个。

        :return: The tags of this BatchTagActionAddRequestBody.
        :rtype: list[TagWithKeyValue]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this BatchTagActionAddRequestBody.

        标签列表。单个实例总标签数上限10个。

        :param tags: The tags of this BatchTagActionAddRequestBody.
        :type: list[TagWithKeyValue]
        """
        self._tags = tags

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
        if not isinstance(other, BatchTagActionAddRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

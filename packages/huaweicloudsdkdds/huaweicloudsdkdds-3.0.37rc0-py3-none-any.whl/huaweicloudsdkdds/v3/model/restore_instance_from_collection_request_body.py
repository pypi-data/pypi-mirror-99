# coding: utf-8

import pprint
import re

import six





class RestoreInstanceFromCollectionRequestBody:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'restore_collections': 'list[RestoreInstanceFromCollectionRequestBodyRestoreCollections]'
    }

    attribute_map = {
        'restore_collections': 'restore_collections'
    }

    def __init__(self, restore_collections=None):
        """RestoreInstanceFromCollectionRequestBody - a model defined in huaweicloud sdk"""
        
        

        self._restore_collections = None
        self.discriminator = None

        self.restore_collections = restore_collections

    @property
    def restore_collections(self):
        """Gets the restore_collections of this RestoreInstanceFromCollectionRequestBody.

        数据库信息。

        :return: The restore_collections of this RestoreInstanceFromCollectionRequestBody.
        :rtype: list[RestoreInstanceFromCollectionRequestBodyRestoreCollections]
        """
        return self._restore_collections

    @restore_collections.setter
    def restore_collections(self, restore_collections):
        """Sets the restore_collections of this RestoreInstanceFromCollectionRequestBody.

        数据库信息。

        :param restore_collections: The restore_collections of this RestoreInstanceFromCollectionRequestBody.
        :type: list[RestoreInstanceFromCollectionRequestBodyRestoreCollections]
        """
        self._restore_collections = restore_collections

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
        if not isinstance(other, RestoreInstanceFromCollectionRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

# coding: utf-8

import pprint
import re

import six





class SourceObject:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'kind': 'SourceKind',
        'spec': 'SourceOrArtifact'
    }

    attribute_map = {
        'kind': 'kind',
        'spec': 'spec'
    }

    def __init__(self, kind=None, spec=None):
        """SourceObject - a model defined in huaweicloud sdk"""
        
        

        self._kind = None
        self._spec = None
        self.discriminator = None

        if kind is not None:
            self.kind = kind
        if spec is not None:
            self.spec = spec

    @property
    def kind(self):
        """Gets the kind of this SourceObject.


        :return: The kind of this SourceObject.
        :rtype: SourceKind
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this SourceObject.


        :param kind: The kind of this SourceObject.
        :type: SourceKind
        """
        self._kind = kind

    @property
    def spec(self):
        """Gets the spec of this SourceObject.


        :return: The spec of this SourceObject.
        :rtype: SourceOrArtifact
        """
        return self._spec

    @spec.setter
    def spec(self, spec):
        """Sets the spec of this SourceObject.


        :param spec: The spec of this SourceObject.
        :type: SourceOrArtifact
        """
        self._spec = spec

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
        if not isinstance(other, SourceObject):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

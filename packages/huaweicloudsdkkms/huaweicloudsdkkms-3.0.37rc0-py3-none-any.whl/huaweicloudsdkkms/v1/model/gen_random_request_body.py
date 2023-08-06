# coding: utf-8

import pprint
import re

import six





class GenRandomRequestBody:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'random_data_length': 'str',
        'sequence': 'str'
    }

    attribute_map = {
        'random_data_length': 'random_data_length',
        'sequence': 'sequence'
    }

    def __init__(self, random_data_length=None, sequence=None):
        """GenRandomRequestBody - a model defined in huaweicloud sdk"""
        
        

        self._random_data_length = None
        self._sequence = None
        self.discriminator = None

        if random_data_length is not None:
            self.random_data_length = random_data_length
        if sequence is not None:
            self.sequence = sequence

    @property
    def random_data_length(self):
        """Gets the random_data_length of this GenRandomRequestBody.

        随机数的bit位长度。 取值为8的倍数，取值范围为8~8192。 随机数的bit位长度，取值为“512”。

        :return: The random_data_length of this GenRandomRequestBody.
        :rtype: str
        """
        return self._random_data_length

    @random_data_length.setter
    def random_data_length(self, random_data_length):
        """Sets the random_data_length of this GenRandomRequestBody.

        随机数的bit位长度。 取值为8的倍数，取值范围为8~8192。 随机数的bit位长度，取值为“512”。

        :param random_data_length: The random_data_length of this GenRandomRequestBody.
        :type: str
        """
        self._random_data_length = random_data_length

    @property
    def sequence(self):
        """Gets the sequence of this GenRandomRequestBody.

        请求消息序列号，36字节序列号。 例如：919c82d4-8046-4722-9094-35c3c6524cff

        :return: The sequence of this GenRandomRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this GenRandomRequestBody.

        请求消息序列号，36字节序列号。 例如：919c82d4-8046-4722-9094-35c3c6524cff

        :param sequence: The sequence of this GenRandomRequestBody.
        :type: str
        """
        self._sequence = sequence

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
        if not isinstance(other, GenRandomRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

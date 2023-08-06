# coding: utf-8

import pprint
import re

import six





class CreateDatakeyRequestBody:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'key_id': 'str',
        'encryption_context': 'object',
        'key_spec': 'str',
        'datakey_length': 'str',
        'sequence': 'str'
    }

    attribute_map = {
        'key_id': 'key_id',
        'encryption_context': 'encryption_context',
        'key_spec': 'key_spec',
        'datakey_length': 'datakey_length',
        'sequence': 'sequence'
    }

    def __init__(self, key_id=None, encryption_context=None, key_spec=None, datakey_length=None, sequence=None):
        """CreateDatakeyRequestBody - a model defined in huaweicloud sdk"""
        
        

        self._key_id = None
        self._encryption_context = None
        self._key_spec = None
        self._datakey_length = None
        self._sequence = None
        self.discriminator = None

        if key_id is not None:
            self.key_id = key_id
        if encryption_context is not None:
            self.encryption_context = encryption_context
        if key_spec is not None:
            self.key_spec = key_spec
        if datakey_length is not None:
            self.datakey_length = datakey_length
        if sequence is not None:
            self.sequence = sequence

    @property
    def key_id(self):
        """Gets the key_id of this CreateDatakeyRequestBody.

        密钥ID，36字节，满足正则匹配“^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$”。 例如：0d0466b0-e727-4d9c-b35d-f84bb474a37f。

        :return: The key_id of this CreateDatakeyRequestBody.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """Sets the key_id of this CreateDatakeyRequestBody.

        密钥ID，36字节，满足正则匹配“^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$”。 例如：0d0466b0-e727-4d9c-b35d-f84bb474a37f。

        :param key_id: The key_id of this CreateDatakeyRequestBody.
        :type: str
        """
        self._key_id = key_id

    @property
    def encryption_context(self):
        """Gets the encryption_context of this CreateDatakeyRequestBody.

        一系列key-value键值对，用于记录资源上下文信息，用于保护数据的完整性，不应包含敏感信息，最大长度为8192。 当在加密时指定了该参数时，解密密文时，需要传入相同的参数，才能正确的解密。 例如：{\"Key1\":\"Value1\",\"Key2\":\"Value2\"}

        :return: The encryption_context of this CreateDatakeyRequestBody.
        :rtype: object
        """
        return self._encryption_context

    @encryption_context.setter
    def encryption_context(self, encryption_context):
        """Sets the encryption_context of this CreateDatakeyRequestBody.

        一系列key-value键值对，用于记录资源上下文信息，用于保护数据的完整性，不应包含敏感信息，最大长度为8192。 当在加密时指定了该参数时，解密密文时，需要传入相同的参数，才能正确的解密。 例如：{\"Key1\":\"Value1\",\"Key2\":\"Value2\"}

        :param encryption_context: The encryption_context of this CreateDatakeyRequestBody.
        :type: object
        """
        self._encryption_context = encryption_context

    @property
    def key_spec(self):
        """Gets the key_spec of this CreateDatakeyRequestBody.

        指定生成的密钥bit位长度。有效值：AES_256、AES_128。  - AES_256：表示256比特的对称密钥。  - AES_128：表示128比特的对称密钥。 说明：  datakey_length和key_spec二选一。   - 若datakey_length和key_spec都为空，默认生成256bit的密钥。   - 若datakey_length和key_spec都指定了值，仅datakey_length生效。

        :return: The key_spec of this CreateDatakeyRequestBody.
        :rtype: str
        """
        return self._key_spec

    @key_spec.setter
    def key_spec(self, key_spec):
        """Sets the key_spec of this CreateDatakeyRequestBody.

        指定生成的密钥bit位长度。有效值：AES_256、AES_128。  - AES_256：表示256比特的对称密钥。  - AES_128：表示128比特的对称密钥。 说明：  datakey_length和key_spec二选一。   - 若datakey_length和key_spec都为空，默认生成256bit的密钥。   - 若datakey_length和key_spec都指定了值，仅datakey_length生效。

        :param key_spec: The key_spec of this CreateDatakeyRequestBody.
        :type: str
        """
        self._key_spec = key_spec

    @property
    def datakey_length(self):
        """Gets the datakey_length of this CreateDatakeyRequestBody.

        密钥bit位长度。取值为8的倍数，取值范围为8~8192。 说明：  datakey_length和key_spec二选一。   - 若datakey_length和key_spec都为空，默认生成256bit的密钥。   - 若datakey_length和key_spec都指定了值，仅datakey_length生效。

        :return: The datakey_length of this CreateDatakeyRequestBody.
        :rtype: str
        """
        return self._datakey_length

    @datakey_length.setter
    def datakey_length(self, datakey_length):
        """Sets the datakey_length of this CreateDatakeyRequestBody.

        密钥bit位长度。取值为8的倍数，取值范围为8~8192。 说明：  datakey_length和key_spec二选一。   - 若datakey_length和key_spec都为空，默认生成256bit的密钥。   - 若datakey_length和key_spec都指定了值，仅datakey_length生效。

        :param datakey_length: The datakey_length of this CreateDatakeyRequestBody.
        :type: str
        """
        self._datakey_length = datakey_length

    @property
    def sequence(self):
        """Gets the sequence of this CreateDatakeyRequestBody.

        请求消息序列号，36字节序列号。 例如：919c82d4-8046-4722-9094-35c3c6524cff

        :return: The sequence of this CreateDatakeyRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this CreateDatakeyRequestBody.

        请求消息序列号，36字节序列号。 例如：919c82d4-8046-4722-9094-35c3c6524cff

        :param sequence: The sequence of this CreateDatakeyRequestBody.
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
        if not isinstance(other, CreateDatakeyRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

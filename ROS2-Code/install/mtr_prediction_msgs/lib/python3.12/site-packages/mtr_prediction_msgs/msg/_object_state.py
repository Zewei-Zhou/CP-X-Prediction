# generated from rosidl_generator_py/resource/_idl.py.em
# with input from mtr_prediction_msgs:msg/ObjectState.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'sensor_id'
# Member 'continuous_state'
# Member 'discrete_state'
# Member 'continuous_state_covariance'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ObjectState(type):
    """Metaclass of message 'ObjectState'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('mtr_prediction_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'mtr_prediction_msgs.msg.ObjectState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__object_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__object_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__object_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__object_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__object_state

            from mtr_prediction_msgs.msg import ObjectClassification
            if ObjectClassification.__class__._TYPE_SUPPORT is None:
                ObjectClassification.__class__.__import_type_support__()

            from mtr_prediction_msgs.msg import ObjectReferencePoint
            if ObjectReferencePoint.__class__._TYPE_SUPPORT is None:
                ObjectReferencePoint.__class__.__import_type_support__()

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ObjectState(metaclass=Metaclass_ObjectState):
    """Message class 'ObjectState'."""

    __slots__ = [
        '_header',
        '_model_id',
        '_sensor_id',
        '_continuous_state',
        '_discrete_state',
        '_continuous_state_covariance',
        '_classifications',
        '_reference_point',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'model_id': 'uint8',
        'sensor_id': 'sequence<uint64>',
        'continuous_state': 'sequence<double>',
        'discrete_state': 'sequence<int64>',
        'continuous_state_covariance': 'sequence<double>',
        'classifications': 'sequence<mtr_prediction_msgs/ObjectClassification>',
        'reference_point': 'mtr_prediction_msgs/ObjectReferencePoint',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint64')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('int64')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['mtr_prediction_msgs', 'msg'], 'ObjectClassification')),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['mtr_prediction_msgs', 'msg'], 'ObjectReferencePoint'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.model_id = kwargs.get('model_id', int())
        self.sensor_id = array.array('Q', kwargs.get('sensor_id', []))
        self.continuous_state = array.array('d', kwargs.get('continuous_state', []))
        self.discrete_state = array.array('q', kwargs.get('discrete_state', []))
        self.continuous_state_covariance = array.array('d', kwargs.get('continuous_state_covariance', []))
        self.classifications = kwargs.get('classifications', [])
        from mtr_prediction_msgs.msg import ObjectReferencePoint
        self.reference_point = kwargs.get('reference_point', ObjectReferencePoint())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.model_id != other.model_id:
            return False
        if self.sensor_id != other.sensor_id:
            return False
        if self.continuous_state != other.continuous_state:
            return False
        if self.discrete_state != other.discrete_state:
            return False
        if self.continuous_state_covariance != other.continuous_state_covariance:
            return False
        if self.classifications != other.classifications:
            return False
        if self.reference_point != other.reference_point:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def model_id(self):
        """Message field 'model_id'."""
        return self._model_id

    @model_id.setter
    def model_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'model_id' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'model_id' field must be an unsigned integer in [0, 255]"
        self._model_id = value

    @builtins.property
    def sensor_id(self):
        """Message field 'sensor_id'."""
        return self._sensor_id

    @sensor_id.setter
    def sensor_id(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'Q', \
                "The 'sensor_id' array.array() must have the type code of 'Q'"
            self._sensor_id = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 18446744073709551616 for val in value)), \
                "The 'sensor_id' field must be a set or sequence and each value of type 'int' and each unsigned integer in [0, 18446744073709551615]"
        self._sensor_id = array.array('Q', value)

    @builtins.property
    def continuous_state(self):
        """Message field 'continuous_state'."""
        return self._continuous_state

    @continuous_state.setter
    def continuous_state(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'continuous_state' array.array() must have the type code of 'd'"
            self._continuous_state = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'continuous_state' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._continuous_state = array.array('d', value)

    @builtins.property
    def discrete_state(self):
        """Message field 'discrete_state'."""
        return self._discrete_state

    @discrete_state.setter
    def discrete_state(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'q', \
                "The 'discrete_state' array.array() must have the type code of 'q'"
            self._discrete_state = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= -9223372036854775808 and val < 9223372036854775808 for val in value)), \
                "The 'discrete_state' field must be a set or sequence and each value of type 'int' and each integer in [-9223372036854775808, 9223372036854775807]"
        self._discrete_state = array.array('q', value)

    @builtins.property
    def continuous_state_covariance(self):
        """Message field 'continuous_state_covariance'."""
        return self._continuous_state_covariance

    @continuous_state_covariance.setter
    def continuous_state_covariance(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'continuous_state_covariance' array.array() must have the type code of 'd'"
            self._continuous_state_covariance = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'continuous_state_covariance' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._continuous_state_covariance = array.array('d', value)

    @builtins.property
    def classifications(self):
        """Message field 'classifications'."""
        return self._classifications

    @classifications.setter
    def classifications(self, value):
        if __debug__:
            from mtr_prediction_msgs.msg import ObjectClassification
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, ObjectClassification) for v in value) and
                 True), \
                "The 'classifications' field must be a set or sequence and each value of type 'ObjectClassification'"
        self._classifications = value

    @builtins.property
    def reference_point(self):
        """Message field 'reference_point'."""
        return self._reference_point

    @reference_point.setter
    def reference_point(self, value):
        if __debug__:
            from mtr_prediction_msgs.msg import ObjectReferencePoint
            assert \
                isinstance(value, ObjectReferencePoint), \
                "The 'reference_point' field must be a sub message of type 'ObjectReferencePoint'"
        self._reference_point = value

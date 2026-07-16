# generated from rosidl_generator_py/resource/_idl.py.em
# with input from mtr_prediction_msgs:msg/Object.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Object(type):
    """Metaclass of message 'Object'."""

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
                'mtr_prediction_msgs.msg.Object')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__object
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__object
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__object
            cls._TYPE_SUPPORT = module.type_support_msg__msg__object
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__object

            from mtr_prediction_msgs.msg import ObjectState
            if ObjectState.__class__._TYPE_SUPPORT is None:
                ObjectState.__class__.__import_type_support__()

            from mtr_prediction_msgs.msg import ObjectStatePrediction
            if ObjectStatePrediction.__class__._TYPE_SUPPORT is None:
                ObjectStatePrediction.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Object(metaclass=Metaclass_Object):
    """Message class 'Object'."""

    __slots__ = [
        '_id',
        '_existence_probability',
        '_state',
        '_state_history',
        '_state_predictions',
    ]

    _fields_and_field_types = {
        'id': 'uint64',
        'existence_probability': 'double',
        'state': 'mtr_prediction_msgs/ObjectState',
        'state_history': 'sequence<mtr_prediction_msgs/ObjectState>',
        'state_predictions': 'sequence<mtr_prediction_msgs/ObjectStatePrediction>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['mtr_prediction_msgs', 'msg'], 'ObjectState'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['mtr_prediction_msgs', 'msg'], 'ObjectState')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['mtr_prediction_msgs', 'msg'], 'ObjectStatePrediction')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.id = kwargs.get('id', int())
        self.existence_probability = kwargs.get('existence_probability', float())
        from mtr_prediction_msgs.msg import ObjectState
        self.state = kwargs.get('state', ObjectState())
        self.state_history = kwargs.get('state_history', [])
        self.state_predictions = kwargs.get('state_predictions', [])

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
        if self.id != other.id:
            return False
        if self.existence_probability != other.existence_probability:
            return False
        if self.state != other.state:
            return False
        if self.state_history != other.state_history:
            return False
        if self.state_predictions != other.state_predictions:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property  # noqa: A003
    def id(self):  # noqa: A003
        """Message field 'id'."""
        return self._id

    @id.setter  # noqa: A003
    def id(self, value):  # noqa: A003
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'id' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'id' field must be an unsigned integer in [0, 18446744073709551615]"
        self._id = value

    @builtins.property
    def existence_probability(self):
        """Message field 'existence_probability'."""
        return self._existence_probability

    @existence_probability.setter
    def existence_probability(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'existence_probability' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'existence_probability' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._existence_probability = value

    @builtins.property
    def state(self):
        """Message field 'state'."""
        return self._state

    @state.setter
    def state(self, value):
        if __debug__:
            from mtr_prediction_msgs.msg import ObjectState
            assert \
                isinstance(value, ObjectState), \
                "The 'state' field must be a sub message of type 'ObjectState'"
        self._state = value

    @builtins.property
    def state_history(self):
        """Message field 'state_history'."""
        return self._state_history

    @state_history.setter
    def state_history(self, value):
        if __debug__:
            from mtr_prediction_msgs.msg import ObjectState
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
                 all(isinstance(v, ObjectState) for v in value) and
                 True), \
                "The 'state_history' field must be a set or sequence and each value of type 'ObjectState'"
        self._state_history = value

    @builtins.property
    def state_predictions(self):
        """Message field 'state_predictions'."""
        return self._state_predictions

    @state_predictions.setter
    def state_predictions(self, value):
        if __debug__:
            from mtr_prediction_msgs.msg import ObjectStatePrediction
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
                 all(isinstance(v, ObjectStatePrediction) for v in value) and
                 True), \
                "The 'state_predictions' field must be a set or sequence and each value of type 'ObjectStatePrediction'"
        self._state_predictions = value

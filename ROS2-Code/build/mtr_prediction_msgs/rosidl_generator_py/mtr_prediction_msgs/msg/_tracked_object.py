# generated from rosidl_generator_py/resource/_idl.py.em
# with input from mtr_prediction_msgs:msg/TrackedObject.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_TrackedObject(type):
    """Metaclass of message 'TrackedObject'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'OBJECT_TYPE_UNKNOWN': 0,
        'OBJECT_TYPE_VEHICLE': 1,
        'OBJECT_TYPE_PEDESTRIAN': 2,
        'OBJECT_TYPE_CYCLIST': 3,
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
                'mtr_prediction_msgs.msg.TrackedObject')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__tracked_object
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__tracked_object
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__tracked_object
            cls._TYPE_SUPPORT = module.type_support_msg__msg__tracked_object
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__tracked_object

            from geometry_msgs.msg import Pose
            if Pose.__class__._TYPE_SUPPORT is None:
                Pose.__class__.__import_type_support__()

            from geometry_msgs.msg import Twist
            if Twist.__class__._TYPE_SUPPORT is None:
                Twist.__class__.__import_type_support__()

            from geometry_msgs.msg import Vector3
            if Vector3.__class__._TYPE_SUPPORT is None:
                Vector3.__class__.__import_type_support__()

            from mtr_prediction_msgs.msg import ObjectState
            if ObjectState.__class__._TYPE_SUPPORT is None:
                ObjectState.__class__.__import_type_support__()

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'OBJECT_TYPE_UNKNOWN': cls.__constants['OBJECT_TYPE_UNKNOWN'],
            'OBJECT_TYPE_VEHICLE': cls.__constants['OBJECT_TYPE_VEHICLE'],
            'OBJECT_TYPE_PEDESTRIAN': cls.__constants['OBJECT_TYPE_PEDESTRIAN'],
            'OBJECT_TYPE_CYCLIST': cls.__constants['OBJECT_TYPE_CYCLIST'],
        }

    @property
    def OBJECT_TYPE_UNKNOWN(self):
        """Message constant 'OBJECT_TYPE_UNKNOWN'."""
        return Metaclass_TrackedObject.__constants['OBJECT_TYPE_UNKNOWN']

    @property
    def OBJECT_TYPE_VEHICLE(self):
        """Message constant 'OBJECT_TYPE_VEHICLE'."""
        return Metaclass_TrackedObject.__constants['OBJECT_TYPE_VEHICLE']

    @property
    def OBJECT_TYPE_PEDESTRIAN(self):
        """Message constant 'OBJECT_TYPE_PEDESTRIAN'."""
        return Metaclass_TrackedObject.__constants['OBJECT_TYPE_PEDESTRIAN']

    @property
    def OBJECT_TYPE_CYCLIST(self):
        """Message constant 'OBJECT_TYPE_CYCLIST'."""
        return Metaclass_TrackedObject.__constants['OBJECT_TYPE_CYCLIST']


class TrackedObject(metaclass=Metaclass_TrackedObject):
    """
    Message class 'TrackedObject'.

    Constants:
      OBJECT_TYPE_UNKNOWN
      OBJECT_TYPE_VEHICLE
      OBJECT_TYPE_PEDESTRIAN
      OBJECT_TYPE_CYCLIST
    """

    __slots__ = [
        '_header',
        '_object_id',
        '_model_id',
        '_pose',
        '_velocity',
        '_size',
        '_object_type',
        '_track_history',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'object_id': 'uint64',
        'model_id': 'uint8',
        'pose': 'geometry_msgs/Pose',
        'velocity': 'geometry_msgs/Twist',
        'size': 'geometry_msgs/Vector3',
        'object_type': 'uint8',
        'track_history': 'sequence<mtr_prediction_msgs/ObjectState>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Twist'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Vector3'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['mtr_prediction_msgs', 'msg'], 'ObjectState')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.object_id = kwargs.get('object_id', int())
        self.model_id = kwargs.get('model_id', int())
        from geometry_msgs.msg import Pose
        self.pose = kwargs.get('pose', Pose())
        from geometry_msgs.msg import Twist
        self.velocity = kwargs.get('velocity', Twist())
        from geometry_msgs.msg import Vector3
        self.size = kwargs.get('size', Vector3())
        self.object_type = kwargs.get('object_type', int())
        self.track_history = kwargs.get('track_history', [])

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
        if self.object_id != other.object_id:
            return False
        if self.model_id != other.model_id:
            return False
        if self.pose != other.pose:
            return False
        if self.velocity != other.velocity:
            return False
        if self.size != other.size:
            return False
        if self.object_type != other.object_type:
            return False
        if self.track_history != other.track_history:
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
    def object_id(self):
        """Message field 'object_id'."""
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'object_id' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'object_id' field must be an unsigned integer in [0, 18446744073709551615]"
        self._object_id = value

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
    def pose(self):
        """Message field 'pose'."""
        return self._pose

    @pose.setter
    def pose(self, value):
        if __debug__:
            from geometry_msgs.msg import Pose
            assert \
                isinstance(value, Pose), \
                "The 'pose' field must be a sub message of type 'Pose'"
        self._pose = value

    @builtins.property
    def velocity(self):
        """Message field 'velocity'."""
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if __debug__:
            from geometry_msgs.msg import Twist
            assert \
                isinstance(value, Twist), \
                "The 'velocity' field must be a sub message of type 'Twist'"
        self._velocity = value

    @builtins.property
    def size(self):
        """Message field 'size'."""
        return self._size

    @size.setter
    def size(self, value):
        if __debug__:
            from geometry_msgs.msg import Vector3
            assert \
                isinstance(value, Vector3), \
                "The 'size' field must be a sub message of type 'Vector3'"
        self._size = value

    @builtins.property
    def object_type(self):
        """Message field 'object_type'."""
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'object_type' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'object_type' field must be an unsigned integer in [0, 255]"
        self._object_type = value

    @builtins.property
    def track_history(self):
        """Message field 'track_history'."""
        return self._track_history

    @track_history.setter
    def track_history(self, value):
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
                "The 'track_history' field must be a set or sequence and each value of type 'ObjectState'"
        self._track_history = value

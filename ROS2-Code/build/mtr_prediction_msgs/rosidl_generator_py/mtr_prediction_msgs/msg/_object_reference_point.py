# generated from rosidl_generator_py/resource/_idl.py.em
# with input from mtr_prediction_msgs:msg/ObjectReferencePoint.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ObjectReferencePoint(type):
    """Metaclass of message 'ObjectReferencePoint'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'GEOMETRIC_CENTER': 0,
        'BACK': 1,
        'BACK_LEFT': 2,
        'LEFT': 3,
        'FRONT_LEFT': 4,
        'FRONT': 5,
        'FRONT_RIGHT': 6,
        'RIGHT': 7,
        'BACK_RIGHT': 8,
        'GRAVITY_CENTER': 10,
        'REAR_AXLE_GROUND': 11,
        'UNKNOWN': 100,
        'UNKNOWN_EDGE': 101,
        'UNKNOWN_CORNER': 102,
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
                'mtr_prediction_msgs.msg.ObjectReferencePoint')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__object_reference_point
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__object_reference_point
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__object_reference_point
            cls._TYPE_SUPPORT = module.type_support_msg__msg__object_reference_point
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__object_reference_point

            from geometry_msgs.msg import Vector3
            if Vector3.__class__._TYPE_SUPPORT is None:
                Vector3.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'GEOMETRIC_CENTER': cls.__constants['GEOMETRIC_CENTER'],
            'BACK': cls.__constants['BACK'],
            'BACK_LEFT': cls.__constants['BACK_LEFT'],
            'LEFT': cls.__constants['LEFT'],
            'FRONT_LEFT': cls.__constants['FRONT_LEFT'],
            'FRONT': cls.__constants['FRONT'],
            'FRONT_RIGHT': cls.__constants['FRONT_RIGHT'],
            'RIGHT': cls.__constants['RIGHT'],
            'BACK_RIGHT': cls.__constants['BACK_RIGHT'],
            'GRAVITY_CENTER': cls.__constants['GRAVITY_CENTER'],
            'REAR_AXLE_GROUND': cls.__constants['REAR_AXLE_GROUND'],
            'UNKNOWN': cls.__constants['UNKNOWN'],
            'UNKNOWN_EDGE': cls.__constants['UNKNOWN_EDGE'],
            'UNKNOWN_CORNER': cls.__constants['UNKNOWN_CORNER'],
        }

    @property
    def GEOMETRIC_CENTER(self):
        """Message constant 'GEOMETRIC_CENTER'."""
        return Metaclass_ObjectReferencePoint.__constants['GEOMETRIC_CENTER']

    @property
    def BACK(self):
        """Message constant 'BACK'."""
        return Metaclass_ObjectReferencePoint.__constants['BACK']

    @property
    def BACK_LEFT(self):
        """Message constant 'BACK_LEFT'."""
        return Metaclass_ObjectReferencePoint.__constants['BACK_LEFT']

    @property
    def LEFT(self):
        """Message constant 'LEFT'."""
        return Metaclass_ObjectReferencePoint.__constants['LEFT']

    @property
    def FRONT_LEFT(self):
        """Message constant 'FRONT_LEFT'."""
        return Metaclass_ObjectReferencePoint.__constants['FRONT_LEFT']

    @property
    def FRONT(self):
        """Message constant 'FRONT'."""
        return Metaclass_ObjectReferencePoint.__constants['FRONT']

    @property
    def FRONT_RIGHT(self):
        """Message constant 'FRONT_RIGHT'."""
        return Metaclass_ObjectReferencePoint.__constants['FRONT_RIGHT']

    @property
    def RIGHT(self):
        """Message constant 'RIGHT'."""
        return Metaclass_ObjectReferencePoint.__constants['RIGHT']

    @property
    def BACK_RIGHT(self):
        """Message constant 'BACK_RIGHT'."""
        return Metaclass_ObjectReferencePoint.__constants['BACK_RIGHT']

    @property
    def GRAVITY_CENTER(self):
        """Message constant 'GRAVITY_CENTER'."""
        return Metaclass_ObjectReferencePoint.__constants['GRAVITY_CENTER']

    @property
    def REAR_AXLE_GROUND(self):
        """Message constant 'REAR_AXLE_GROUND'."""
        return Metaclass_ObjectReferencePoint.__constants['REAR_AXLE_GROUND']

    @property
    def UNKNOWN(self):
        """Message constant 'UNKNOWN'."""
        return Metaclass_ObjectReferencePoint.__constants['UNKNOWN']

    @property
    def UNKNOWN_EDGE(self):
        """Message constant 'UNKNOWN_EDGE'."""
        return Metaclass_ObjectReferencePoint.__constants['UNKNOWN_EDGE']

    @property
    def UNKNOWN_CORNER(self):
        """Message constant 'UNKNOWN_CORNER'."""
        return Metaclass_ObjectReferencePoint.__constants['UNKNOWN_CORNER']


class ObjectReferencePoint(metaclass=Metaclass_ObjectReferencePoint):
    """
    Message class 'ObjectReferencePoint'.

    Constants:
      GEOMETRIC_CENTER
      BACK
      BACK_LEFT
      LEFT
      FRONT_LEFT
      FRONT
      FRONT_RIGHT
      RIGHT
      BACK_RIGHT
      GRAVITY_CENTER
      REAR_AXLE_GROUND
      UNKNOWN
      UNKNOWN_EDGE
      UNKNOWN_CORNER
    """

    __slots__ = [
        '_value',
        '_translation_to_geometric_center',
    ]

    _fields_and_field_types = {
        'value': 'uint8',
        'translation_to_geometric_center': 'geometry_msgs/Vector3',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Vector3'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.value = kwargs.get('value', int())
        from geometry_msgs.msg import Vector3
        self.translation_to_geometric_center = kwargs.get('translation_to_geometric_center', Vector3())

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
        if self.value != other.value:
            return False
        if self.translation_to_geometric_center != other.translation_to_geometric_center:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def value(self):
        """Message field 'value'."""
        return self._value

    @value.setter
    def value(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'value' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'value' field must be an unsigned integer in [0, 255]"
        self._value = value

    @builtins.property
    def translation_to_geometric_center(self):
        """Message field 'translation_to_geometric_center'."""
        return self._translation_to_geometric_center

    @translation_to_geometric_center.setter
    def translation_to_geometric_center(self, value):
        if __debug__:
            from geometry_msgs.msg import Vector3
            assert \
                isinstance(value, Vector3), \
                "The 'translation_to_geometric_center' field must be a sub message of type 'Vector3'"
        self._translation_to_geometric_center = value

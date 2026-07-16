# generated from rosidl_generator_py/resource/_idl.py.em
# with input from mtr_prediction_msgs:msg/ObjectClassification.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ObjectClassification(type):
    """Metaclass of message 'ObjectClassification'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'UNCLASSIFIED': 0,
        'PEDESTRIAN': 1,
        'BICYCLE': 2,
        'MOTORBIKE': 3,
        'MOTORCYCLE': 3,
        'CAR': 4,
        'TRUCK': 5,
        'UTILITY': 5,
        'VAN': 6,
        'BUS': 7,
        'ANIMAL': 8,
        'ROAD_OBSTACLE': 9,
        'TRAIN': 10,
        'TRAILER': 11,
        'VRU': 12,
        'MICRO': 13,
        'CAR_UNION': 50,
        'TRUCK_UNION': 51,
        'BIKE_UNION': 52,
        'UNKNOWN': 100,
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
                'mtr_prediction_msgs.msg.ObjectClassification')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__object_classification
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__object_classification
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__object_classification
            cls._TYPE_SUPPORT = module.type_support_msg__msg__object_classification
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__object_classification

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'UNCLASSIFIED': cls.__constants['UNCLASSIFIED'],
            'PEDESTRIAN': cls.__constants['PEDESTRIAN'],
            'BICYCLE': cls.__constants['BICYCLE'],
            'MOTORBIKE': cls.__constants['MOTORBIKE'],
            'MOTORCYCLE': cls.__constants['MOTORCYCLE'],
            'CAR': cls.__constants['CAR'],
            'TRUCK': cls.__constants['TRUCK'],
            'UTILITY': cls.__constants['UTILITY'],
            'VAN': cls.__constants['VAN'],
            'BUS': cls.__constants['BUS'],
            'ANIMAL': cls.__constants['ANIMAL'],
            'ROAD_OBSTACLE': cls.__constants['ROAD_OBSTACLE'],
            'TRAIN': cls.__constants['TRAIN'],
            'TRAILER': cls.__constants['TRAILER'],
            'VRU': cls.__constants['VRU'],
            'MICRO': cls.__constants['MICRO'],
            'CAR_UNION': cls.__constants['CAR_UNION'],
            'TRUCK_UNION': cls.__constants['TRUCK_UNION'],
            'BIKE_UNION': cls.__constants['BIKE_UNION'],
            'UNKNOWN': cls.__constants['UNKNOWN'],
        }

    @property
    def UNCLASSIFIED(self):
        """Message constant 'UNCLASSIFIED'."""
        return Metaclass_ObjectClassification.__constants['UNCLASSIFIED']

    @property
    def PEDESTRIAN(self):
        """Message constant 'PEDESTRIAN'."""
        return Metaclass_ObjectClassification.__constants['PEDESTRIAN']

    @property
    def BICYCLE(self):
        """Message constant 'BICYCLE'."""
        return Metaclass_ObjectClassification.__constants['BICYCLE']

    @property
    def MOTORBIKE(self):
        """Message constant 'MOTORBIKE'."""
        return Metaclass_ObjectClassification.__constants['MOTORBIKE']

    @property
    def MOTORCYCLE(self):
        """Message constant 'MOTORCYCLE'."""
        return Metaclass_ObjectClassification.__constants['MOTORCYCLE']

    @property
    def CAR(self):
        """Message constant 'CAR'."""
        return Metaclass_ObjectClassification.__constants['CAR']

    @property
    def TRUCK(self):
        """Message constant 'TRUCK'."""
        return Metaclass_ObjectClassification.__constants['TRUCK']

    @property
    def UTILITY(self):
        """Message constant 'UTILITY'."""
        return Metaclass_ObjectClassification.__constants['UTILITY']

    @property
    def VAN(self):
        """Message constant 'VAN'."""
        return Metaclass_ObjectClassification.__constants['VAN']

    @property
    def BUS(self):
        """Message constant 'BUS'."""
        return Metaclass_ObjectClassification.__constants['BUS']

    @property
    def ANIMAL(self):
        """Message constant 'ANIMAL'."""
        return Metaclass_ObjectClassification.__constants['ANIMAL']

    @property
    def ROAD_OBSTACLE(self):
        """Message constant 'ROAD_OBSTACLE'."""
        return Metaclass_ObjectClassification.__constants['ROAD_OBSTACLE']

    @property
    def TRAIN(self):
        """Message constant 'TRAIN'."""
        return Metaclass_ObjectClassification.__constants['TRAIN']

    @property
    def TRAILER(self):
        """Message constant 'TRAILER'."""
        return Metaclass_ObjectClassification.__constants['TRAILER']

    @property
    def VRU(self):
        """Message constant 'VRU'."""
        return Metaclass_ObjectClassification.__constants['VRU']

    @property
    def MICRO(self):
        """Message constant 'MICRO'."""
        return Metaclass_ObjectClassification.__constants['MICRO']

    @property
    def CAR_UNION(self):
        """Message constant 'CAR_UNION'."""
        return Metaclass_ObjectClassification.__constants['CAR_UNION']

    @property
    def TRUCK_UNION(self):
        """Message constant 'TRUCK_UNION'."""
        return Metaclass_ObjectClassification.__constants['TRUCK_UNION']

    @property
    def BIKE_UNION(self):
        """Message constant 'BIKE_UNION'."""
        return Metaclass_ObjectClassification.__constants['BIKE_UNION']

    @property
    def UNKNOWN(self):
        """Message constant 'UNKNOWN'."""
        return Metaclass_ObjectClassification.__constants['UNKNOWN']


class ObjectClassification(metaclass=Metaclass_ObjectClassification):
    """
    Message class 'ObjectClassification'.

    Constants:
      UNCLASSIFIED
      PEDESTRIAN
      BICYCLE
      MOTORBIKE
      MOTORCYCLE
      CAR
      TRUCK
      UTILITY
      VAN
      BUS
      ANIMAL
      ROAD_OBSTACLE
      TRAIN
      TRAILER
      VRU
      MICRO
      CAR_UNION
      TRUCK_UNION
      BIKE_UNION
      UNKNOWN
    """

    __slots__ = [
        '_type',
        '_probability',
    ]

    _fields_and_field_types = {
        'type': 'uint8',
        'probability': 'double',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.type = kwargs.get('type', int())
        self.probability = kwargs.get('probability', float())

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
        if self.type != other.type:
            return False
        if self.probability != other.probability:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property  # noqa: A003
    def type(self):  # noqa: A003
        """Message field 'type'."""
        return self._type

    @type.setter  # noqa: A003
    def type(self, value):  # noqa: A003
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'type' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'type' field must be an unsigned integer in [0, 255]"
        self._type = value

    @builtins.property
    def probability(self):
        """Message field 'probability'."""
        return self._probability

    @probability.setter
    def probability(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'probability' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'probability' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._probability = value

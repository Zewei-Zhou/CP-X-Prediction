// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/ObjectReferencePoint.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'GEOMETRIC_CENTER'.
/**
  * possible reference points
  * As default the GEOMETRIC_CENTER is used
  * This is the geometric center center center point
 */
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__GEOMETRIC_CENTER = 0
};

/// Constant 'BACK'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__BACK = 1
};

/// Constant 'BACK_LEFT'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__BACK_LEFT = 2
};

/// Constant 'LEFT'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__LEFT = 3
};

/// Constant 'FRONT_LEFT'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__FRONT_LEFT = 4
};

/// Constant 'FRONT'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__FRONT = 5
};

/// Constant 'FRONT_RIGHT'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__FRONT_RIGHT = 6
};

/// Constant 'RIGHT'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__RIGHT = 7
};

/// Constant 'BACK_RIGHT'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__BACK_RIGHT = 8
};

/// Constant 'GRAVITY_CENTER'.
/**
  * additional reference points for vehicles
 */
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__GRAVITY_CENTER = 10
};

/// Constant 'REAR_AXLE_GROUND'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__REAR_AXLE_GROUND = 11
};

/// Constant 'UNKNOWN'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__UNKNOWN = 100
};

/// Constant 'UNKNOWN_EDGE'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__UNKNOWN_EDGE = 101
};

/// Constant 'UNKNOWN_CORNER'.
enum
{
  mtr_prediction_msgs__msg__ObjectReferencePoint__UNKNOWN_CORNER = 102
};

// Include directives for member types
// Member 'translation_to_geometric_center'
#include "geometry_msgs/msg/detail/vector3__struct.h"

/// Struct defined in msg/ObjectReferencePoint in the package mtr_prediction_msgs.
/**
  * Message for the reference point of an objects position
 */
typedef struct mtr_prediction_msgs__msg__ObjectReferencePoint
{
  /// the actual value
  uint8_t value;
  /// translation from given reference point to geometric center
  /// This vector is given relative to a Cartesian coordinate system which is located in the given reference point.
  /// The x-axis is parallel to the longitudinal axis of the vehicle!
  geometry_msgs__msg__Vector3 translation_to_geometric_center;
} mtr_prediction_msgs__msg__ObjectReferencePoint;

// Struct for a sequence of mtr_prediction_msgs__msg__ObjectReferencePoint.
typedef struct mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence
{
  mtr_prediction_msgs__msg__ObjectReferencePoint * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__STRUCT_H_

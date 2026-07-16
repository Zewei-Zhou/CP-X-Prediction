// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'OBJECT_TYPE_UNKNOWN'.
enum
{
  mtr_prediction_msgs__msg__TrackedObject__OBJECT_TYPE_UNKNOWN = 0
};

/// Constant 'OBJECT_TYPE_VEHICLE'.
enum
{
  mtr_prediction_msgs__msg__TrackedObject__OBJECT_TYPE_VEHICLE = 1
};

/// Constant 'OBJECT_TYPE_PEDESTRIAN'.
enum
{
  mtr_prediction_msgs__msg__TrackedObject__OBJECT_TYPE_PEDESTRIAN = 2
};

/// Constant 'OBJECT_TYPE_CYCLIST'.
enum
{
  mtr_prediction_msgs__msg__TrackedObject__OBJECT_TYPE_CYCLIST = 3
};

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'velocity'
#include "geometry_msgs/msg/detail/twist__struct.h"
// Member 'size'
#include "geometry_msgs/msg/detail/vector3__struct.h"
// Member 'track_history'
#include "mtr_prediction_msgs/msg/detail/object_state__struct.h"

/// Struct defined in msg/TrackedObject in the package mtr_prediction_msgs.
/**
  * Single tracked object for motion prediction input
 */
typedef struct mtr_prediction_msgs__msg__TrackedObject
{
  std_msgs__msg__Header header;
  /// Object identification
  uint64_t object_id;
  /// Same as ObjectState (1=ego, 16=vehicle, etc.)
  uint8_t model_id;
  /// Current state
  /// x, y, z, orientation
  geometry_msgs__msg__Pose pose;
  /// linear and angular velocity
  geometry_msgs__msg__Twist velocity;
  /// length, width, height
  geometry_msgs__msg__Vector3 size;
  /// Object classification
  uint8_t object_type;
  /// Historical trajectory (10 past states at 10Hz = 1 second history)
  mtr_prediction_msgs__msg__ObjectState__Sequence track_history;
} mtr_prediction_msgs__msg__TrackedObject;

// Struct for a sequence of mtr_prediction_msgs__msg__TrackedObject.
typedef struct mtr_prediction_msgs__msg__TrackedObject__Sequence
{
  mtr_prediction_msgs__msg__TrackedObject * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__TrackedObject__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__STRUCT_H_

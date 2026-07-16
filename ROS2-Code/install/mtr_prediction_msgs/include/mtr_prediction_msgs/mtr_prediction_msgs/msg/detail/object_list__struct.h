// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/ObjectList.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_LIST__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_LIST__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'objects'
#include "mtr_prediction_msgs/msg/detail/object__struct.h"

/// Struct defined in msg/ObjectList in the package mtr_prediction_msgs.
/**
  * Message for a list of objects
 */
typedef struct mtr_prediction_msgs__msg__ObjectList
{
  /// header
  /// frame_id of the reference frame (common: "base_link", "map",...), and timestamp
  /// The frame is where the position and orientation is published.
  /// Probably this will be in vehicle or global coordinates and there should be a transform in between
  /// The timestamp is the time of the newest sample
  std_msgs__msg__Header header;
  /// List of objects
  mtr_prediction_msgs__msg__Object__Sequence objects;
} mtr_prediction_msgs__msg__ObjectList;

// Struct for a sequence of mtr_prediction_msgs__msg__ObjectList.
typedef struct mtr_prediction_msgs__msg__ObjectList__Sequence
{
  mtr_prediction_msgs__msg__ObjectList * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__ObjectList__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_LIST__STRUCT_H_

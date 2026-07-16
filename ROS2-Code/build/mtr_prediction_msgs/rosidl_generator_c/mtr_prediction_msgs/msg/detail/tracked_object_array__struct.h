// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__STRUCT_H_

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
#include "mtr_prediction_msgs/msg/detail/tracked_object__struct.h"

/// Struct defined in msg/TrackedObjectArray in the package mtr_prediction_msgs.
/**
  * Array of tracked objects
 */
typedef struct mtr_prediction_msgs__msg__TrackedObjectArray
{
  std_msgs__msg__Header header;
  mtr_prediction_msgs__msg__TrackedObject__Sequence objects;
} mtr_prediction_msgs__msg__TrackedObjectArray;

// Struct for a sequence of mtr_prediction_msgs__msg__TrackedObjectArray.
typedef struct mtr_prediction_msgs__msg__TrackedObjectArray__Sequence
{
  mtr_prediction_msgs__msg__TrackedObjectArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__TrackedObjectArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__STRUCT_H_

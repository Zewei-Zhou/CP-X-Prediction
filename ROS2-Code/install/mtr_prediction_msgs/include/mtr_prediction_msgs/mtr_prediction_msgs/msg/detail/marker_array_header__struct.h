// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/MarkerArrayHeader.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__MARKER_ARRAY_HEADER__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__MARKER_ARRAY_HEADER__STRUCT_H_

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
// Member 'markers'
#include "visualization_msgs/msg/detail/marker__struct.h"

/// Struct defined in msg/MarkerArrayHeader in the package mtr_prediction_msgs.
typedef struct mtr_prediction_msgs__msg__MarkerArrayHeader
{
  /// header for time/frame information
  std_msgs__msg__Header header;
  /// markers from visualization_msgs::markers
  visualization_msgs__msg__Marker__Sequence markers;
} mtr_prediction_msgs__msg__MarkerArrayHeader;

// Struct for a sequence of mtr_prediction_msgs__msg__MarkerArrayHeader.
typedef struct mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence
{
  mtr_prediction_msgs__msg__MarkerArrayHeader * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__MARKER_ARRAY_HEADER__STRUCT_H_

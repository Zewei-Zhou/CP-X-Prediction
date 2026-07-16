// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/ObjectStatePrediction.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'states'
#include "mtr_prediction_msgs/msg/detail/object_state__struct.h"

/// Struct defined in msg/ObjectStatePrediction in the package mtr_prediction_msgs.
/**
  * Message for the predicted states of an object
 */
typedef struct mtr_prediction_msgs__msg__ObjectStatePrediction
{
  /// probability of this prediction to occur
  double probability;
  /// Predicted states of the object
  ///   Sorted ascending by time
  mtr_prediction_msgs__msg__ObjectState__Sequence states;
} mtr_prediction_msgs__msg__ObjectStatePrediction;

// Struct for a sequence of mtr_prediction_msgs__msg__ObjectStatePrediction.
typedef struct mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence
{
  mtr_prediction_msgs__msg__ObjectStatePrediction * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__STRUCT_H_

// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/Object.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'state'
// Member 'state_history'
#include "mtr_prediction_msgs/msg/detail/object_state__struct.h"
// Member 'state_predictions'
#include "mtr_prediction_msgs/msg/detail/object_state_prediction__struct.h"

/// Struct defined in msg/Object in the package mtr_prediction_msgs.
/**
  * Message for the state of an object
 */
typedef struct mtr_prediction_msgs__msg__Object
{
  /// Lifetime ID of the object
  uint64_t id;
  /// Existence probability of the object [0,1]
  double existence_probability;
  /// Motion state estimate of the object
  mtr_prediction_msgs__msg__ObjectState state;
  /// History of the object's states
  mtr_prediction_msgs__msg__ObjectState__Sequence state_history;
  /// Prediction of the object state
  mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence state_predictions;
} mtr_prediction_msgs__msg__Object;

// Struct for a sequence of mtr_prediction_msgs__msg__Object.
typedef struct mtr_prediction_msgs__msg__Object__Sequence
{
  mtr_prediction_msgs__msg__Object * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__Object__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT__STRUCT_H_

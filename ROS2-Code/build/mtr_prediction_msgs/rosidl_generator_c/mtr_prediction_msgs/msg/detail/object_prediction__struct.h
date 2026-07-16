// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/ObjectPrediction.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_PREDICTION__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_PREDICTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'trajectories'
#include "mtr_prediction_msgs/msg/detail/predicted_trajectory__struct.h"

/// Struct defined in msg/ObjectPrediction in the package mtr_prediction_msgs.
/**
  * Prediction for a single object
 */
typedef struct mtr_prediction_msgs__msg__ObjectPrediction
{
  uint64_t object_id;
  uint8_t object_type;
  /// Multiple trajectory modes (MTR outputs 6 modes)
  mtr_prediction_msgs__msg__PredictedTrajectory__Sequence trajectories;
} mtr_prediction_msgs__msg__ObjectPrediction;

// Struct for a sequence of mtr_prediction_msgs__msg__ObjectPrediction.
typedef struct mtr_prediction_msgs__msg__ObjectPrediction__Sequence
{
  mtr_prediction_msgs__msg__ObjectPrediction * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__ObjectPrediction__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_PREDICTION__STRUCT_H_

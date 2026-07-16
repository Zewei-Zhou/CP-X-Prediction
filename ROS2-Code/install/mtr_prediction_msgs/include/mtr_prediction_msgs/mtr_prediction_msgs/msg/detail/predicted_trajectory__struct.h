// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/PredictedTrajectory.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORY__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'waypoints'
#include "geometry_msgs/msg/detail/pose_stamped__struct.h"
// Member 'velocities'
#include "geometry_msgs/msg/detail/twist_stamped__struct.h"

/// Struct defined in msg/PredictedTrajectory in the package mtr_prediction_msgs.
/**
  * Single predicted trajectory mode
 */
typedef struct mtr_prediction_msgs__msg__PredictedTrajectory
{
  /// Probability of this mode (0.0 to 1.0)
  float confidence;
  /// Predicted waypoints (80 future timesteps at 10Hz = 8 seconds)
  /// Each has pose + timestamp
  geometry_msgs__msg__PoseStamped__Sequence waypoints;
  /// Optional: predicted velocities
  geometry_msgs__msg__TwistStamped__Sequence velocities;
} mtr_prediction_msgs__msg__PredictedTrajectory;

// Struct for a sequence of mtr_prediction_msgs__msg__PredictedTrajectory.
typedef struct mtr_prediction_msgs__msg__PredictedTrajectory__Sequence
{
  mtr_prediction_msgs__msg__PredictedTrajectory * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__PredictedTrajectory__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORY__STRUCT_H_

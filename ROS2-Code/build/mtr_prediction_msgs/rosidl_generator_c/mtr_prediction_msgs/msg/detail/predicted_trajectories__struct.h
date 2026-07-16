// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/PredictedTrajectories.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__STRUCT_H_

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
// Member 'predictions'
#include "mtr_prediction_msgs/msg/detail/object_prediction__struct.h"
// Member 'map_polylines'
#include "sensor_msgs/msg/detail/point_cloud2__struct.h"

/// Struct defined in msg/PredictedTrajectories in the package mtr_prediction_msgs.
/**
  * Predictions for all objects
 */
typedef struct mtr_prediction_msgs__msg__PredictedTrajectories
{
  std_msgs__msg__Header header;
  /// Array of predictions (one per tracked object)
  mtr_prediction_msgs__msg__ObjectPrediction__Sequence predictions;
  /// Optional: Map information used for prediction
  sensor_msgs__msg__PointCloud2 map_polylines;
} mtr_prediction_msgs__msg__PredictedTrajectories;

// Struct for a sequence of mtr_prediction_msgs__msg__PredictedTrajectories.
typedef struct mtr_prediction_msgs__msg__PredictedTrajectories__Sequence
{
  mtr_prediction_msgs__msg__PredictedTrajectories * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__PredictedTrajectories__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__STRUCT_H_

// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/ObjectState.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__STRUCT_H_

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
// Member 'sensor_id'
// Member 'continuous_state'
// Member 'discrete_state'
// Member 'continuous_state_covariance'
#include "rosidl_runtime_c/primitives_sequence.h"
// Member 'classifications'
#include "mtr_prediction_msgs/msg/detail/object_classification__struct.h"
// Member 'reference_point'
#include "mtr_prediction_msgs/msg/detail/object_reference_point__struct.h"

/// Struct defined in msg/ObjectState in the package mtr_prediction_msgs.
typedef struct mtr_prediction_msgs__msg__ObjectState
{
  std_msgs__msg__Header header;
  /// to ensure that the model_id is unique, all existing models an their corresponding IDs are listed here:
  ///   EGO:           1
  ///   EGORWS:        2
  ///   ISCACTR:       16
  ///   HEXAMOTION:    17
  ///   TRAFFICLIGHT:  20
  uint8_t model_id;
  /// IDs of the sensors having measured this state
  /// In case of a fused object, this vector will have multiple entries
  rosidl_runtime_c__uint64__Sequence sensor_id;
  /// continuous state vector (N)
  rosidl_runtime_c__double__Sequence continuous_state;
  /// discrete state vector (M) for discrete int/bool/string quantitites
  rosidl_runtime_c__int64__Sequence discrete_state;
  /// continuous state covariance matrix (N*N flattened)
  /// CONTINUOUS_STATE_COVARIANCE_INVALID (-1): state value is invalid / not set
  /// CONTINUOUS_STATE_COVARIANCE_UNKNOWN (max): state value is set, but covariance is unknown
  rosidl_runtime_c__double__Sequence continuous_state_covariance;
  /// classification incl. probabilities
  mtr_prediction_msgs__msg__ObjectClassification__Sequence classifications;
  /// reference point for object position
  mtr_prediction_msgs__msg__ObjectReferencePoint reference_point;
} mtr_prediction_msgs__msg__ObjectState;

// Struct for a sequence of mtr_prediction_msgs__msg__ObjectState.
typedef struct mtr_prediction_msgs__msg__ObjectState__Sequence
{
  mtr_prediction_msgs__msg__ObjectState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__ObjectState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__STRUCT_H_

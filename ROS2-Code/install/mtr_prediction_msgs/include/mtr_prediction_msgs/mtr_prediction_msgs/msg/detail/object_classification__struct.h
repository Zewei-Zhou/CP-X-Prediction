// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mtr_prediction_msgs:msg/ObjectClassification.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_CLASSIFICATION__STRUCT_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_CLASSIFICATION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'UNCLASSIFIED'.
/**
  * unknown classification
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__UNCLASSIFIED = 0
};

/// Constant 'PEDESTRIAN'.
/**
  * persons on foot (walking, standing, running, sitting, lying) without a dedicated mobility device such as a wheelchair or stroller
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__PEDESTRIAN = 1
};

/// Constant 'BICYCLE'.
/**
  * bicycles and their riders
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__BICYCLE = 2
};

/// Constant 'MOTORBIKE'.
/**
  * --- DEPRECATED; USE MOTORCYCLE
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__MOTORBIKE = 3
};

/// Constant 'MOTORCYCLE'.
/**
  * motorized two-wheel vehicles and their riders
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__MOTORCYCLE = 3
};

/// Constant 'CAR'.
/**
  * standard passenger cars for personal transport
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__CAR = 4
};

/// Constant 'TRUCK'.
/**
  * --- DEPRECATED; USE UTILITY
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__TRUCK = 5
};

/// Constant 'UTILITY'.
/**
  * commercial & utility vehicles like trucks, trailers, construction vehicles, agricultural/utility vehicles, and other large road vehicles
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__UTILITY = 5
};

/// Constant 'VAN'.
/**
  * --- DEPRECATED; USE CAR
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__VAN = 6
};

/// Constant 'BUS'.
/**
  * vehicles designed to carry many passengers such as urban buses, articulated buses, and bus trailers
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__BUS = 7
};

/// Constant 'ANIMAL'.
/**
  * animals that may influence traffic
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__ANIMAL = 8
};

/// Constant 'ROAD_OBSTACLE'.
/**
  * --- DEPRECATED
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__ROAD_OBSTACLE = 9
};

/// Constant 'TRAIN'.
/**
  * --- DEPRECATED; USE UTILITY
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__TRAIN = 10
};

/// Constant 'TRAILER'.
/**
  * --- DEPRECATED; USE UTILITY
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__TRAILER = 11
};

/// Constant 'VRU'.
/**
  * vulnerable road users that typically move on sidewalks such as wheelchairs and strollers, except pedestrians
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__VRU = 12
};

/// Constant 'MICRO'.
/**
  * micro-mobility devices typically used on bike lanes or the road (e.g., kick-scooters, Segways, hoverboards) with their riders
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__MICRO = 13
};

/// Constant 'CAR_UNION'.
/**
  * --- DEPRECATED; USE CAR
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__CAR_UNION = 50
};

/// Constant 'TRUCK_UNION'.
/**
  * --- DEPRECATED; USE UTILITY
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__TRUCK_UNION = 51
};

/// Constant 'BIKE_UNION'.
/**
  * --- DEPRECATED; USE MULTIPLE PROBABILISTIC CLASSIFICATIONS
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__BIKE_UNION = 52
};

/// Constant 'UNKNOWN'.
/**
  * definitely none of the other defined classes
 */
enum
{
  mtr_prediction_msgs__msg__ObjectClassification__UNKNOWN = 100
};

/// Struct defined in msg/ObjectClassification in the package mtr_prediction_msgs.
typedef struct mtr_prediction_msgs__msg__ObjectClassification
{
  uint8_t type;
  double probability;
} mtr_prediction_msgs__msg__ObjectClassification;

// Struct for a sequence of mtr_prediction_msgs__msg__ObjectClassification.
typedef struct mtr_prediction_msgs__msg__ObjectClassification__Sequence
{
  mtr_prediction_msgs__msg__ObjectClassification * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mtr_prediction_msgs__msg__ObjectClassification__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_CLASSIFICATION__STRUCT_H_

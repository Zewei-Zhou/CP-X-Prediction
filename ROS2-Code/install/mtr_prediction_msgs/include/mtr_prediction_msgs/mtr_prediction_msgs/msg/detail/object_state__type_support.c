// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from mtr_prediction_msgs:msg/ObjectState.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "mtr_prediction_msgs/msg/detail/object_state__rosidl_typesupport_introspection_c.h"
#include "mtr_prediction_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "mtr_prediction_msgs/msg/detail/object_state__functions.h"
#include "mtr_prediction_msgs/msg/detail/object_state__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `sensor_id`
// Member `continuous_state`
// Member `discrete_state`
// Member `continuous_state_covariance`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `classifications`
#include "mtr_prediction_msgs/msg/object_classification.h"
// Member `classifications`
#include "mtr_prediction_msgs/msg/detail/object_classification__rosidl_typesupport_introspection_c.h"
// Member `reference_point`
#include "mtr_prediction_msgs/msg/object_reference_point.h"
// Member `reference_point`
#include "mtr_prediction_msgs/msg/detail/object_reference_point__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  mtr_prediction_msgs__msg__ObjectState__init(message_memory);
}

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_fini_function(void * message_memory)
{
  mtr_prediction_msgs__msg__ObjectState__fini(message_memory);
}

size_t mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__size_function__ObjectState__sensor_id(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint64__Sequence * member =
    (const rosidl_runtime_c__uint64__Sequence *)(untyped_member);
  return member->size;
}

const void * mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__sensor_id(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint64__Sequence * member =
    (const rosidl_runtime_c__uint64__Sequence *)(untyped_member);
  return &member->data[index];
}

void * mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__sensor_id(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint64__Sequence * member =
    (rosidl_runtime_c__uint64__Sequence *)(untyped_member);
  return &member->data[index];
}

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__fetch_function__ObjectState__sensor_id(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint64_t * item =
    ((const uint64_t *)
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__sensor_id(untyped_member, index));
  uint64_t * value =
    (uint64_t *)(untyped_value);
  *value = *item;
}

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__assign_function__ObjectState__sensor_id(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint64_t * item =
    ((uint64_t *)
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__sensor_id(untyped_member, index));
  const uint64_t * value =
    (const uint64_t *)(untyped_value);
  *item = *value;
}

bool mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__resize_function__ObjectState__sensor_id(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint64__Sequence * member =
    (rosidl_runtime_c__uint64__Sequence *)(untyped_member);
  rosidl_runtime_c__uint64__Sequence__fini(member);
  return rosidl_runtime_c__uint64__Sequence__init(member, size);
}

size_t mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__size_function__ObjectState__continuous_state(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__continuous_state(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__continuous_state(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__fetch_function__ObjectState__continuous_state(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__continuous_state(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__assign_function__ObjectState__continuous_state(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__continuous_state(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__resize_function__ObjectState__continuous_state(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__size_function__ObjectState__discrete_state(
  const void * untyped_member)
{
  const rosidl_runtime_c__int64__Sequence * member =
    (const rosidl_runtime_c__int64__Sequence *)(untyped_member);
  return member->size;
}

const void * mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__discrete_state(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int64__Sequence * member =
    (const rosidl_runtime_c__int64__Sequence *)(untyped_member);
  return &member->data[index];
}

void * mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__discrete_state(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int64__Sequence * member =
    (rosidl_runtime_c__int64__Sequence *)(untyped_member);
  return &member->data[index];
}

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__fetch_function__ObjectState__discrete_state(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int64_t * item =
    ((const int64_t *)
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__discrete_state(untyped_member, index));
  int64_t * value =
    (int64_t *)(untyped_value);
  *value = *item;
}

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__assign_function__ObjectState__discrete_state(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int64_t * item =
    ((int64_t *)
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__discrete_state(untyped_member, index));
  const int64_t * value =
    (const int64_t *)(untyped_value);
  *item = *value;
}

bool mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__resize_function__ObjectState__discrete_state(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int64__Sequence * member =
    (rosidl_runtime_c__int64__Sequence *)(untyped_member);
  rosidl_runtime_c__int64__Sequence__fini(member);
  return rosidl_runtime_c__int64__Sequence__init(member, size);
}

size_t mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__size_function__ObjectState__continuous_state_covariance(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__continuous_state_covariance(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__continuous_state_covariance(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__fetch_function__ObjectState__continuous_state_covariance(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__continuous_state_covariance(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__assign_function__ObjectState__continuous_state_covariance(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__continuous_state_covariance(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__resize_function__ObjectState__continuous_state_covariance(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__size_function__ObjectState__classifications(
  const void * untyped_member)
{
  const mtr_prediction_msgs__msg__ObjectClassification__Sequence * member =
    (const mtr_prediction_msgs__msg__ObjectClassification__Sequence *)(untyped_member);
  return member->size;
}

const void * mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__classifications(
  const void * untyped_member, size_t index)
{
  const mtr_prediction_msgs__msg__ObjectClassification__Sequence * member =
    (const mtr_prediction_msgs__msg__ObjectClassification__Sequence *)(untyped_member);
  return &member->data[index];
}

void * mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__classifications(
  void * untyped_member, size_t index)
{
  mtr_prediction_msgs__msg__ObjectClassification__Sequence * member =
    (mtr_prediction_msgs__msg__ObjectClassification__Sequence *)(untyped_member);
  return &member->data[index];
}

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__fetch_function__ObjectState__classifications(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const mtr_prediction_msgs__msg__ObjectClassification * item =
    ((const mtr_prediction_msgs__msg__ObjectClassification *)
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__classifications(untyped_member, index));
  mtr_prediction_msgs__msg__ObjectClassification * value =
    (mtr_prediction_msgs__msg__ObjectClassification *)(untyped_value);
  *value = *item;
}

void mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__assign_function__ObjectState__classifications(
  void * untyped_member, size_t index, const void * untyped_value)
{
  mtr_prediction_msgs__msg__ObjectClassification * item =
    ((mtr_prediction_msgs__msg__ObjectClassification *)
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__classifications(untyped_member, index));
  const mtr_prediction_msgs__msg__ObjectClassification * value =
    (const mtr_prediction_msgs__msg__ObjectClassification *)(untyped_value);
  *item = *value;
}

bool mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__resize_function__ObjectState__classifications(
  void * untyped_member, size_t size)
{
  mtr_prediction_msgs__msg__ObjectClassification__Sequence * member =
    (mtr_prediction_msgs__msg__ObjectClassification__Sequence *)(untyped_member);
  mtr_prediction_msgs__msg__ObjectClassification__Sequence__fini(member);
  return mtr_prediction_msgs__msg__ObjectClassification__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_message_member_array[8] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__ObjectState, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "model_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__ObjectState, model_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "sensor_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__ObjectState, sensor_id),  // bytes offset in struct
    NULL,  // default value
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__size_function__ObjectState__sensor_id,  // size() function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__sensor_id,  // get_const(index) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__sensor_id,  // get(index) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__fetch_function__ObjectState__sensor_id,  // fetch(index, &value) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__assign_function__ObjectState__sensor_id,  // assign(index, value) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__resize_function__ObjectState__sensor_id  // resize(index) function pointer
  },
  {
    "continuous_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__ObjectState, continuous_state),  // bytes offset in struct
    NULL,  // default value
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__size_function__ObjectState__continuous_state,  // size() function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__continuous_state,  // get_const(index) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__continuous_state,  // get(index) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__fetch_function__ObjectState__continuous_state,  // fetch(index, &value) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__assign_function__ObjectState__continuous_state,  // assign(index, value) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__resize_function__ObjectState__continuous_state  // resize(index) function pointer
  },
  {
    "discrete_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__ObjectState, discrete_state),  // bytes offset in struct
    NULL,  // default value
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__size_function__ObjectState__discrete_state,  // size() function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__discrete_state,  // get_const(index) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__discrete_state,  // get(index) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__fetch_function__ObjectState__discrete_state,  // fetch(index, &value) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__assign_function__ObjectState__discrete_state,  // assign(index, value) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__resize_function__ObjectState__discrete_state  // resize(index) function pointer
  },
  {
    "continuous_state_covariance",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__ObjectState, continuous_state_covariance),  // bytes offset in struct
    NULL,  // default value
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__size_function__ObjectState__continuous_state_covariance,  // size() function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__continuous_state_covariance,  // get_const(index) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__continuous_state_covariance,  // get(index) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__fetch_function__ObjectState__continuous_state_covariance,  // fetch(index, &value) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__assign_function__ObjectState__continuous_state_covariance,  // assign(index, value) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__resize_function__ObjectState__continuous_state_covariance  // resize(index) function pointer
  },
  {
    "classifications",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__ObjectState, classifications),  // bytes offset in struct
    NULL,  // default value
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__size_function__ObjectState__classifications,  // size() function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_const_function__ObjectState__classifications,  // get_const(index) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__get_function__ObjectState__classifications,  // get(index) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__fetch_function__ObjectState__classifications,  // fetch(index, &value) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__assign_function__ObjectState__classifications,  // assign(index, value) function pointer
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__resize_function__ObjectState__classifications  // resize(index) function pointer
  },
  {
    "reference_point",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__ObjectState, reference_point),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_message_members = {
  "mtr_prediction_msgs__msg",  // message namespace
  "ObjectState",  // message name
  8,  // number of fields
  sizeof(mtr_prediction_msgs__msg__ObjectState),
  mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_message_member_array,  // message members
  mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_init_function,  // function to initialize message memory (memory has to be allocated)
  mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_message_type_support_handle = {
  0,
  &mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_mtr_prediction_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mtr_prediction_msgs, msg, ObjectState)() {
  mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_message_member_array[6].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mtr_prediction_msgs, msg, ObjectClassification)();
  mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_message_member_array[7].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mtr_prediction_msgs, msg, ObjectReferencePoint)();
  if (!mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_message_type_support_handle.typesupport_identifier) {
    mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &mtr_prediction_msgs__msg__ObjectState__rosidl_typesupport_introspection_c__ObjectState_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from mtr_prediction_msgs:msg/ObjectStatePrediction.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "mtr_prediction_msgs/msg/detail/object_state_prediction__rosidl_typesupport_introspection_c.h"
#include "mtr_prediction_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "mtr_prediction_msgs/msg/detail/object_state_prediction__functions.h"
#include "mtr_prediction_msgs/msg/detail/object_state_prediction__struct.h"


// Include directives for member types
// Member `states`
#include "mtr_prediction_msgs/msg/object_state.h"
// Member `states`
#include "mtr_prediction_msgs/msg/detail/object_state__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  mtr_prediction_msgs__msg__ObjectStatePrediction__init(message_memory);
}

void mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_fini_function(void * message_memory)
{
  mtr_prediction_msgs__msg__ObjectStatePrediction__fini(message_memory);
}

size_t mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__size_function__ObjectStatePrediction__states(
  const void * untyped_member)
{
  const mtr_prediction_msgs__msg__ObjectState__Sequence * member =
    (const mtr_prediction_msgs__msg__ObjectState__Sequence *)(untyped_member);
  return member->size;
}

const void * mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__get_const_function__ObjectStatePrediction__states(
  const void * untyped_member, size_t index)
{
  const mtr_prediction_msgs__msg__ObjectState__Sequence * member =
    (const mtr_prediction_msgs__msg__ObjectState__Sequence *)(untyped_member);
  return &member->data[index];
}

void * mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__get_function__ObjectStatePrediction__states(
  void * untyped_member, size_t index)
{
  mtr_prediction_msgs__msg__ObjectState__Sequence * member =
    (mtr_prediction_msgs__msg__ObjectState__Sequence *)(untyped_member);
  return &member->data[index];
}

void mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__fetch_function__ObjectStatePrediction__states(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const mtr_prediction_msgs__msg__ObjectState * item =
    ((const mtr_prediction_msgs__msg__ObjectState *)
    mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__get_const_function__ObjectStatePrediction__states(untyped_member, index));
  mtr_prediction_msgs__msg__ObjectState * value =
    (mtr_prediction_msgs__msg__ObjectState *)(untyped_value);
  *value = *item;
}

void mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__assign_function__ObjectStatePrediction__states(
  void * untyped_member, size_t index, const void * untyped_value)
{
  mtr_prediction_msgs__msg__ObjectState * item =
    ((mtr_prediction_msgs__msg__ObjectState *)
    mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__get_function__ObjectStatePrediction__states(untyped_member, index));
  const mtr_prediction_msgs__msg__ObjectState * value =
    (const mtr_prediction_msgs__msg__ObjectState *)(untyped_value);
  *item = *value;
}

bool mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__resize_function__ObjectStatePrediction__states(
  void * untyped_member, size_t size)
{
  mtr_prediction_msgs__msg__ObjectState__Sequence * member =
    (mtr_prediction_msgs__msg__ObjectState__Sequence *)(untyped_member);
  mtr_prediction_msgs__msg__ObjectState__Sequence__fini(member);
  return mtr_prediction_msgs__msg__ObjectState__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_message_member_array[2] = {
  {
    "probability",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__ObjectStatePrediction, probability),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "states",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__ObjectStatePrediction, states),  // bytes offset in struct
    NULL,  // default value
    mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__size_function__ObjectStatePrediction__states,  // size() function pointer
    mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__get_const_function__ObjectStatePrediction__states,  // get_const(index) function pointer
    mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__get_function__ObjectStatePrediction__states,  // get(index) function pointer
    mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__fetch_function__ObjectStatePrediction__states,  // fetch(index, &value) function pointer
    mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__assign_function__ObjectStatePrediction__states,  // assign(index, value) function pointer
    mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__resize_function__ObjectStatePrediction__states  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_message_members = {
  "mtr_prediction_msgs__msg",  // message namespace
  "ObjectStatePrediction",  // message name
  2,  // number of fields
  sizeof(mtr_prediction_msgs__msg__ObjectStatePrediction),
  mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_message_member_array,  // message members
  mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_init_function,  // function to initialize message memory (memory has to be allocated)
  mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_message_type_support_handle = {
  0,
  &mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_mtr_prediction_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mtr_prediction_msgs, msg, ObjectStatePrediction)() {
  mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mtr_prediction_msgs, msg, ObjectState)();
  if (!mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_message_type_support_handle.typesupport_identifier) {
    mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &mtr_prediction_msgs__msg__ObjectStatePrediction__rosidl_typesupport_introspection_c__ObjectStatePrediction_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

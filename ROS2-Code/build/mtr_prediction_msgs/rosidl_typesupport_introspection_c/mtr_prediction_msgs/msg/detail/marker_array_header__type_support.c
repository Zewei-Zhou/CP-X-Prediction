// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from mtr_prediction_msgs:msg/MarkerArrayHeader.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "mtr_prediction_msgs/msg/detail/marker_array_header__rosidl_typesupport_introspection_c.h"
#include "mtr_prediction_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "mtr_prediction_msgs/msg/detail/marker_array_header__functions.h"
#include "mtr_prediction_msgs/msg/detail/marker_array_header__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `markers`
#include "visualization_msgs/msg/marker.h"
// Member `markers`
#include "visualization_msgs/msg/detail/marker__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  mtr_prediction_msgs__msg__MarkerArrayHeader__init(message_memory);
}

void mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_fini_function(void * message_memory)
{
  mtr_prediction_msgs__msg__MarkerArrayHeader__fini(message_memory);
}

size_t mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__size_function__MarkerArrayHeader__markers(
  const void * untyped_member)
{
  const visualization_msgs__msg__Marker__Sequence * member =
    (const visualization_msgs__msg__Marker__Sequence *)(untyped_member);
  return member->size;
}

const void * mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__get_const_function__MarkerArrayHeader__markers(
  const void * untyped_member, size_t index)
{
  const visualization_msgs__msg__Marker__Sequence * member =
    (const visualization_msgs__msg__Marker__Sequence *)(untyped_member);
  return &member->data[index];
}

void * mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__get_function__MarkerArrayHeader__markers(
  void * untyped_member, size_t index)
{
  visualization_msgs__msg__Marker__Sequence * member =
    (visualization_msgs__msg__Marker__Sequence *)(untyped_member);
  return &member->data[index];
}

void mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__fetch_function__MarkerArrayHeader__markers(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const visualization_msgs__msg__Marker * item =
    ((const visualization_msgs__msg__Marker *)
    mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__get_const_function__MarkerArrayHeader__markers(untyped_member, index));
  visualization_msgs__msg__Marker * value =
    (visualization_msgs__msg__Marker *)(untyped_value);
  *value = *item;
}

void mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__assign_function__MarkerArrayHeader__markers(
  void * untyped_member, size_t index, const void * untyped_value)
{
  visualization_msgs__msg__Marker * item =
    ((visualization_msgs__msg__Marker *)
    mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__get_function__MarkerArrayHeader__markers(untyped_member, index));
  const visualization_msgs__msg__Marker * value =
    (const visualization_msgs__msg__Marker *)(untyped_value);
  *item = *value;
}

bool mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__resize_function__MarkerArrayHeader__markers(
  void * untyped_member, size_t size)
{
  visualization_msgs__msg__Marker__Sequence * member =
    (visualization_msgs__msg__Marker__Sequence *)(untyped_member);
  visualization_msgs__msg__Marker__Sequence__fini(member);
  return visualization_msgs__msg__Marker__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__MarkerArrayHeader, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "markers",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__MarkerArrayHeader, markers),  // bytes offset in struct
    NULL,  // default value
    mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__size_function__MarkerArrayHeader__markers,  // size() function pointer
    mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__get_const_function__MarkerArrayHeader__markers,  // get_const(index) function pointer
    mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__get_function__MarkerArrayHeader__markers,  // get(index) function pointer
    mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__fetch_function__MarkerArrayHeader__markers,  // fetch(index, &value) function pointer
    mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__assign_function__MarkerArrayHeader__markers,  // assign(index, value) function pointer
    mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__resize_function__MarkerArrayHeader__markers  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_message_members = {
  "mtr_prediction_msgs__msg",  // message namespace
  "MarkerArrayHeader",  // message name
  2,  // number of fields
  sizeof(mtr_prediction_msgs__msg__MarkerArrayHeader),
  mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_message_member_array,  // message members
  mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_init_function,  // function to initialize message memory (memory has to be allocated)
  mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_message_type_support_handle = {
  0,
  &mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_mtr_prediction_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mtr_prediction_msgs, msg, MarkerArrayHeader)() {
  mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, visualization_msgs, msg, Marker)();
  if (!mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_message_type_support_handle.typesupport_identifier) {
    mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &mtr_prediction_msgs__msg__MarkerArrayHeader__rosidl_typesupport_introspection_c__MarkerArrayHeader_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

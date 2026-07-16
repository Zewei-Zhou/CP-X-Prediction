// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from mtr_prediction_msgs:msg/PredictedTrajectory.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "mtr_prediction_msgs/msg/detail/predicted_trajectory__rosidl_typesupport_introspection_c.h"
#include "mtr_prediction_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "mtr_prediction_msgs/msg/detail/predicted_trajectory__functions.h"
#include "mtr_prediction_msgs/msg/detail/predicted_trajectory__struct.h"


// Include directives for member types
// Member `waypoints`
#include "geometry_msgs/msg/pose_stamped.h"
// Member `waypoints`
#include "geometry_msgs/msg/detail/pose_stamped__rosidl_typesupport_introspection_c.h"
// Member `velocities`
#include "geometry_msgs/msg/twist_stamped.h"
// Member `velocities`
#include "geometry_msgs/msg/detail/twist_stamped__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  mtr_prediction_msgs__msg__PredictedTrajectory__init(message_memory);
}

void mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_fini_function(void * message_memory)
{
  mtr_prediction_msgs__msg__PredictedTrajectory__fini(message_memory);
}

size_t mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__size_function__PredictedTrajectory__waypoints(
  const void * untyped_member)
{
  const geometry_msgs__msg__PoseStamped__Sequence * member =
    (const geometry_msgs__msg__PoseStamped__Sequence *)(untyped_member);
  return member->size;
}

const void * mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_const_function__PredictedTrajectory__waypoints(
  const void * untyped_member, size_t index)
{
  const geometry_msgs__msg__PoseStamped__Sequence * member =
    (const geometry_msgs__msg__PoseStamped__Sequence *)(untyped_member);
  return &member->data[index];
}

void * mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_function__PredictedTrajectory__waypoints(
  void * untyped_member, size_t index)
{
  geometry_msgs__msg__PoseStamped__Sequence * member =
    (geometry_msgs__msg__PoseStamped__Sequence *)(untyped_member);
  return &member->data[index];
}

void mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__fetch_function__PredictedTrajectory__waypoints(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const geometry_msgs__msg__PoseStamped * item =
    ((const geometry_msgs__msg__PoseStamped *)
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_const_function__PredictedTrajectory__waypoints(untyped_member, index));
  geometry_msgs__msg__PoseStamped * value =
    (geometry_msgs__msg__PoseStamped *)(untyped_value);
  *value = *item;
}

void mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__assign_function__PredictedTrajectory__waypoints(
  void * untyped_member, size_t index, const void * untyped_value)
{
  geometry_msgs__msg__PoseStamped * item =
    ((geometry_msgs__msg__PoseStamped *)
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_function__PredictedTrajectory__waypoints(untyped_member, index));
  const geometry_msgs__msg__PoseStamped * value =
    (const geometry_msgs__msg__PoseStamped *)(untyped_value);
  *item = *value;
}

bool mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__resize_function__PredictedTrajectory__waypoints(
  void * untyped_member, size_t size)
{
  geometry_msgs__msg__PoseStamped__Sequence * member =
    (geometry_msgs__msg__PoseStamped__Sequence *)(untyped_member);
  geometry_msgs__msg__PoseStamped__Sequence__fini(member);
  return geometry_msgs__msg__PoseStamped__Sequence__init(member, size);
}

size_t mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__size_function__PredictedTrajectory__velocities(
  const void * untyped_member)
{
  const geometry_msgs__msg__TwistStamped__Sequence * member =
    (const geometry_msgs__msg__TwistStamped__Sequence *)(untyped_member);
  return member->size;
}

const void * mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_const_function__PredictedTrajectory__velocities(
  const void * untyped_member, size_t index)
{
  const geometry_msgs__msg__TwistStamped__Sequence * member =
    (const geometry_msgs__msg__TwistStamped__Sequence *)(untyped_member);
  return &member->data[index];
}

void * mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_function__PredictedTrajectory__velocities(
  void * untyped_member, size_t index)
{
  geometry_msgs__msg__TwistStamped__Sequence * member =
    (geometry_msgs__msg__TwistStamped__Sequence *)(untyped_member);
  return &member->data[index];
}

void mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__fetch_function__PredictedTrajectory__velocities(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const geometry_msgs__msg__TwistStamped * item =
    ((const geometry_msgs__msg__TwistStamped *)
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_const_function__PredictedTrajectory__velocities(untyped_member, index));
  geometry_msgs__msg__TwistStamped * value =
    (geometry_msgs__msg__TwistStamped *)(untyped_value);
  *value = *item;
}

void mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__assign_function__PredictedTrajectory__velocities(
  void * untyped_member, size_t index, const void * untyped_value)
{
  geometry_msgs__msg__TwistStamped * item =
    ((geometry_msgs__msg__TwistStamped *)
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_function__PredictedTrajectory__velocities(untyped_member, index));
  const geometry_msgs__msg__TwistStamped * value =
    (const geometry_msgs__msg__TwistStamped *)(untyped_value);
  *item = *value;
}

bool mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__resize_function__PredictedTrajectory__velocities(
  void * untyped_member, size_t size)
{
  geometry_msgs__msg__TwistStamped__Sequence * member =
    (geometry_msgs__msg__TwistStamped__Sequence *)(untyped_member);
  geometry_msgs__msg__TwistStamped__Sequence__fini(member);
  return geometry_msgs__msg__TwistStamped__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_message_member_array[3] = {
  {
    "confidence",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__PredictedTrajectory, confidence),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "waypoints",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__PredictedTrajectory, waypoints),  // bytes offset in struct
    NULL,  // default value
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__size_function__PredictedTrajectory__waypoints,  // size() function pointer
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_const_function__PredictedTrajectory__waypoints,  // get_const(index) function pointer
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_function__PredictedTrajectory__waypoints,  // get(index) function pointer
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__fetch_function__PredictedTrajectory__waypoints,  // fetch(index, &value) function pointer
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__assign_function__PredictedTrajectory__waypoints,  // assign(index, value) function pointer
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__resize_function__PredictedTrajectory__waypoints  // resize(index) function pointer
  },
  {
    "velocities",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs__msg__PredictedTrajectory, velocities),  // bytes offset in struct
    NULL,  // default value
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__size_function__PredictedTrajectory__velocities,  // size() function pointer
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_const_function__PredictedTrajectory__velocities,  // get_const(index) function pointer
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__get_function__PredictedTrajectory__velocities,  // get(index) function pointer
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__fetch_function__PredictedTrajectory__velocities,  // fetch(index, &value) function pointer
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__assign_function__PredictedTrajectory__velocities,  // assign(index, value) function pointer
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__resize_function__PredictedTrajectory__velocities  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_message_members = {
  "mtr_prediction_msgs__msg",  // message namespace
  "PredictedTrajectory",  // message name
  3,  // number of fields
  sizeof(mtr_prediction_msgs__msg__PredictedTrajectory),
  mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_message_member_array,  // message members
  mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_init_function,  // function to initialize message memory (memory has to be allocated)
  mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_message_type_support_handle = {
  0,
  &mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_mtr_prediction_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mtr_prediction_msgs, msg, PredictedTrajectory)() {
  mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, PoseStamped)();
  mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, TwistStamped)();
  if (!mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_message_type_support_handle.typesupport_identifier) {
    mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &mtr_prediction_msgs__msg__PredictedTrajectory__rosidl_typesupport_introspection_c__PredictedTrajectory_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

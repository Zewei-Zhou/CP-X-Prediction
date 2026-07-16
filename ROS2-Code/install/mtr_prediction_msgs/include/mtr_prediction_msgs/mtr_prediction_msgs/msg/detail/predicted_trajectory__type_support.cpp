// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from mtr_prediction_msgs:msg/PredictedTrajectory.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "mtr_prediction_msgs/msg/detail/predicted_trajectory__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace mtr_prediction_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void PredictedTrajectory_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) mtr_prediction_msgs::msg::PredictedTrajectory(_init);
}

void PredictedTrajectory_fini_function(void * message_memory)
{
  auto typed_message = static_cast<mtr_prediction_msgs::msg::PredictedTrajectory *>(message_memory);
  typed_message->~PredictedTrajectory();
}

size_t size_function__PredictedTrajectory__waypoints(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<geometry_msgs::msg::PoseStamped> *>(untyped_member);
  return member->size();
}

const void * get_const_function__PredictedTrajectory__waypoints(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<geometry_msgs::msg::PoseStamped> *>(untyped_member);
  return &member[index];
}

void * get_function__PredictedTrajectory__waypoints(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<geometry_msgs::msg::PoseStamped> *>(untyped_member);
  return &member[index];
}

void fetch_function__PredictedTrajectory__waypoints(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const geometry_msgs::msg::PoseStamped *>(
    get_const_function__PredictedTrajectory__waypoints(untyped_member, index));
  auto & value = *reinterpret_cast<geometry_msgs::msg::PoseStamped *>(untyped_value);
  value = item;
}

void assign_function__PredictedTrajectory__waypoints(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<geometry_msgs::msg::PoseStamped *>(
    get_function__PredictedTrajectory__waypoints(untyped_member, index));
  const auto & value = *reinterpret_cast<const geometry_msgs::msg::PoseStamped *>(untyped_value);
  item = value;
}

void resize_function__PredictedTrajectory__waypoints(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<geometry_msgs::msg::PoseStamped> *>(untyped_member);
  member->resize(size);
}

size_t size_function__PredictedTrajectory__velocities(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<geometry_msgs::msg::TwistStamped> *>(untyped_member);
  return member->size();
}

const void * get_const_function__PredictedTrajectory__velocities(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<geometry_msgs::msg::TwistStamped> *>(untyped_member);
  return &member[index];
}

void * get_function__PredictedTrajectory__velocities(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<geometry_msgs::msg::TwistStamped> *>(untyped_member);
  return &member[index];
}

void fetch_function__PredictedTrajectory__velocities(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const geometry_msgs::msg::TwistStamped *>(
    get_const_function__PredictedTrajectory__velocities(untyped_member, index));
  auto & value = *reinterpret_cast<geometry_msgs::msg::TwistStamped *>(untyped_value);
  value = item;
}

void assign_function__PredictedTrajectory__velocities(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<geometry_msgs::msg::TwistStamped *>(
    get_function__PredictedTrajectory__velocities(untyped_member, index));
  const auto & value = *reinterpret_cast<const geometry_msgs::msg::TwistStamped *>(untyped_value);
  item = value;
}

void resize_function__PredictedTrajectory__velocities(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<geometry_msgs::msg::TwistStamped> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PredictedTrajectory_message_member_array[3] = {
  {
    "confidence",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::PredictedTrajectory, confidence),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "waypoints",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::PoseStamped>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::PredictedTrajectory, waypoints),  // bytes offset in struct
    nullptr,  // default value
    size_function__PredictedTrajectory__waypoints,  // size() function pointer
    get_const_function__PredictedTrajectory__waypoints,  // get_const(index) function pointer
    get_function__PredictedTrajectory__waypoints,  // get(index) function pointer
    fetch_function__PredictedTrajectory__waypoints,  // fetch(index, &value) function pointer
    assign_function__PredictedTrajectory__waypoints,  // assign(index, value) function pointer
    resize_function__PredictedTrajectory__waypoints  // resize(index) function pointer
  },
  {
    "velocities",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::TwistStamped>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::PredictedTrajectory, velocities),  // bytes offset in struct
    nullptr,  // default value
    size_function__PredictedTrajectory__velocities,  // size() function pointer
    get_const_function__PredictedTrajectory__velocities,  // get_const(index) function pointer
    get_function__PredictedTrajectory__velocities,  // get(index) function pointer
    fetch_function__PredictedTrajectory__velocities,  // fetch(index, &value) function pointer
    assign_function__PredictedTrajectory__velocities,  // assign(index, value) function pointer
    resize_function__PredictedTrajectory__velocities  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PredictedTrajectory_message_members = {
  "mtr_prediction_msgs::msg",  // message namespace
  "PredictedTrajectory",  // message name
  3,  // number of fields
  sizeof(mtr_prediction_msgs::msg::PredictedTrajectory),
  PredictedTrajectory_message_member_array,  // message members
  PredictedTrajectory_init_function,  // function to initialize message memory (memory has to be allocated)
  PredictedTrajectory_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PredictedTrajectory_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PredictedTrajectory_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace mtr_prediction_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<mtr_prediction_msgs::msg::PredictedTrajectory>()
{
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::PredictedTrajectory_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, mtr_prediction_msgs, msg, PredictedTrajectory)() {
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::PredictedTrajectory_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

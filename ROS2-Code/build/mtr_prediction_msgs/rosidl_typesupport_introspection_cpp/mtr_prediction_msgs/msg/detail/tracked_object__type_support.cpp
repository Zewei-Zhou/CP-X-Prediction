// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from mtr_prediction_msgs:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "mtr_prediction_msgs/msg/detail/tracked_object__struct.hpp"
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

void TrackedObject_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) mtr_prediction_msgs::msg::TrackedObject(_init);
}

void TrackedObject_fini_function(void * message_memory)
{
  auto typed_message = static_cast<mtr_prediction_msgs::msg::TrackedObject *>(message_memory);
  typed_message->~TrackedObject();
}

size_t size_function__TrackedObject__track_history(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<mtr_prediction_msgs::msg::ObjectState> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrackedObject__track_history(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<mtr_prediction_msgs::msg::ObjectState> *>(untyped_member);
  return &member[index];
}

void * get_function__TrackedObject__track_history(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<mtr_prediction_msgs::msg::ObjectState> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrackedObject__track_history(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const mtr_prediction_msgs::msg::ObjectState *>(
    get_const_function__TrackedObject__track_history(untyped_member, index));
  auto & value = *reinterpret_cast<mtr_prediction_msgs::msg::ObjectState *>(untyped_value);
  value = item;
}

void assign_function__TrackedObject__track_history(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<mtr_prediction_msgs::msg::ObjectState *>(
    get_function__TrackedObject__track_history(untyped_member, index));
  const auto & value = *reinterpret_cast<const mtr_prediction_msgs::msg::ObjectState *>(untyped_value);
  item = value;
}

void resize_function__TrackedObject__track_history(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<mtr_prediction_msgs::msg::ObjectState> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember TrackedObject_message_member_array[8] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::TrackedObject, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "object_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::TrackedObject, object_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "model_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::TrackedObject, model_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "pose",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Pose>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::TrackedObject, pose),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "velocity",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Twist>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::TrackedObject, velocity),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "size",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Vector3>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::TrackedObject, size),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "object_type",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::TrackedObject, object_type),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "track_history",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<mtr_prediction_msgs::msg::ObjectState>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::TrackedObject, track_history),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrackedObject__track_history,  // size() function pointer
    get_const_function__TrackedObject__track_history,  // get_const(index) function pointer
    get_function__TrackedObject__track_history,  // get(index) function pointer
    fetch_function__TrackedObject__track_history,  // fetch(index, &value) function pointer
    assign_function__TrackedObject__track_history,  // assign(index, value) function pointer
    resize_function__TrackedObject__track_history  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers TrackedObject_message_members = {
  "mtr_prediction_msgs::msg",  // message namespace
  "TrackedObject",  // message name
  8,  // number of fields
  sizeof(mtr_prediction_msgs::msg::TrackedObject),
  TrackedObject_message_member_array,  // message members
  TrackedObject_init_function,  // function to initialize message memory (memory has to be allocated)
  TrackedObject_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t TrackedObject_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &TrackedObject_message_members,
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
get_message_type_support_handle<mtr_prediction_msgs::msg::TrackedObject>()
{
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::TrackedObject_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, mtr_prediction_msgs, msg, TrackedObject)() {
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::TrackedObject_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

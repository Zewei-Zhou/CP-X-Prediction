// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from mtr_prediction_msgs:msg/Object.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "mtr_prediction_msgs/msg/detail/object__struct.hpp"
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

void Object_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) mtr_prediction_msgs::msg::Object(_init);
}

void Object_fini_function(void * message_memory)
{
  auto typed_message = static_cast<mtr_prediction_msgs::msg::Object *>(message_memory);
  typed_message->~Object();
}

size_t size_function__Object__state_history(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<mtr_prediction_msgs::msg::ObjectState> *>(untyped_member);
  return member->size();
}

const void * get_const_function__Object__state_history(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<mtr_prediction_msgs::msg::ObjectState> *>(untyped_member);
  return &member[index];
}

void * get_function__Object__state_history(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<mtr_prediction_msgs::msg::ObjectState> *>(untyped_member);
  return &member[index];
}

void fetch_function__Object__state_history(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const mtr_prediction_msgs::msg::ObjectState *>(
    get_const_function__Object__state_history(untyped_member, index));
  auto & value = *reinterpret_cast<mtr_prediction_msgs::msg::ObjectState *>(untyped_value);
  value = item;
}

void assign_function__Object__state_history(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<mtr_prediction_msgs::msg::ObjectState *>(
    get_function__Object__state_history(untyped_member, index));
  const auto & value = *reinterpret_cast<const mtr_prediction_msgs::msg::ObjectState *>(untyped_value);
  item = value;
}

void resize_function__Object__state_history(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<mtr_prediction_msgs::msg::ObjectState> *>(untyped_member);
  member->resize(size);
}

size_t size_function__Object__state_predictions(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<mtr_prediction_msgs::msg::ObjectStatePrediction> *>(untyped_member);
  return member->size();
}

const void * get_const_function__Object__state_predictions(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<mtr_prediction_msgs::msg::ObjectStatePrediction> *>(untyped_member);
  return &member[index];
}

void * get_function__Object__state_predictions(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<mtr_prediction_msgs::msg::ObjectStatePrediction> *>(untyped_member);
  return &member[index];
}

void fetch_function__Object__state_predictions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const mtr_prediction_msgs::msg::ObjectStatePrediction *>(
    get_const_function__Object__state_predictions(untyped_member, index));
  auto & value = *reinterpret_cast<mtr_prediction_msgs::msg::ObjectStatePrediction *>(untyped_value);
  value = item;
}

void assign_function__Object__state_predictions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<mtr_prediction_msgs::msg::ObjectStatePrediction *>(
    get_function__Object__state_predictions(untyped_member, index));
  const auto & value = *reinterpret_cast<const mtr_prediction_msgs::msg::ObjectStatePrediction *>(untyped_value);
  item = value;
}

void resize_function__Object__state_predictions(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<mtr_prediction_msgs::msg::ObjectStatePrediction> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Object_message_member_array[5] = {
  {
    "id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::Object, id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "existence_probability",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::Object, existence_probability),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "state",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<mtr_prediction_msgs::msg::ObjectState>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::Object, state),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "state_history",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<mtr_prediction_msgs::msg::ObjectState>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::Object, state_history),  // bytes offset in struct
    nullptr,  // default value
    size_function__Object__state_history,  // size() function pointer
    get_const_function__Object__state_history,  // get_const(index) function pointer
    get_function__Object__state_history,  // get(index) function pointer
    fetch_function__Object__state_history,  // fetch(index, &value) function pointer
    assign_function__Object__state_history,  // assign(index, value) function pointer
    resize_function__Object__state_history  // resize(index) function pointer
  },
  {
    "state_predictions",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<mtr_prediction_msgs::msg::ObjectStatePrediction>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::Object, state_predictions),  // bytes offset in struct
    nullptr,  // default value
    size_function__Object__state_predictions,  // size() function pointer
    get_const_function__Object__state_predictions,  // get_const(index) function pointer
    get_function__Object__state_predictions,  // get(index) function pointer
    fetch_function__Object__state_predictions,  // fetch(index, &value) function pointer
    assign_function__Object__state_predictions,  // assign(index, value) function pointer
    resize_function__Object__state_predictions  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Object_message_members = {
  "mtr_prediction_msgs::msg",  // message namespace
  "Object",  // message name
  5,  // number of fields
  sizeof(mtr_prediction_msgs::msg::Object),
  Object_message_member_array,  // message members
  Object_init_function,  // function to initialize message memory (memory has to be allocated)
  Object_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Object_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Object_message_members,
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
get_message_type_support_handle<mtr_prediction_msgs::msg::Object>()
{
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::Object_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, mtr_prediction_msgs, msg, Object)() {
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::Object_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

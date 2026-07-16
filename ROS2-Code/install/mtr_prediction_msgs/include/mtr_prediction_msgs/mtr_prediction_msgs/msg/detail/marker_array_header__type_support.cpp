// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from mtr_prediction_msgs:msg/MarkerArrayHeader.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "mtr_prediction_msgs/msg/detail/marker_array_header__struct.hpp"
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

void MarkerArrayHeader_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) mtr_prediction_msgs::msg::MarkerArrayHeader(_init);
}

void MarkerArrayHeader_fini_function(void * message_memory)
{
  auto typed_message = static_cast<mtr_prediction_msgs::msg::MarkerArrayHeader *>(message_memory);
  typed_message->~MarkerArrayHeader();
}

size_t size_function__MarkerArrayHeader__markers(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<visualization_msgs::msg::Marker> *>(untyped_member);
  return member->size();
}

const void * get_const_function__MarkerArrayHeader__markers(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<visualization_msgs::msg::Marker> *>(untyped_member);
  return &member[index];
}

void * get_function__MarkerArrayHeader__markers(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<visualization_msgs::msg::Marker> *>(untyped_member);
  return &member[index];
}

void fetch_function__MarkerArrayHeader__markers(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const visualization_msgs::msg::Marker *>(
    get_const_function__MarkerArrayHeader__markers(untyped_member, index));
  auto & value = *reinterpret_cast<visualization_msgs::msg::Marker *>(untyped_value);
  value = item;
}

void assign_function__MarkerArrayHeader__markers(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<visualization_msgs::msg::Marker *>(
    get_function__MarkerArrayHeader__markers(untyped_member, index));
  const auto & value = *reinterpret_cast<const visualization_msgs::msg::Marker *>(untyped_value);
  item = value;
}

void resize_function__MarkerArrayHeader__markers(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<visualization_msgs::msg::Marker> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember MarkerArrayHeader_message_member_array[2] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::MarkerArrayHeader, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "markers",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<visualization_msgs::msg::Marker>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::MarkerArrayHeader, markers),  // bytes offset in struct
    nullptr,  // default value
    size_function__MarkerArrayHeader__markers,  // size() function pointer
    get_const_function__MarkerArrayHeader__markers,  // get_const(index) function pointer
    get_function__MarkerArrayHeader__markers,  // get(index) function pointer
    fetch_function__MarkerArrayHeader__markers,  // fetch(index, &value) function pointer
    assign_function__MarkerArrayHeader__markers,  // assign(index, value) function pointer
    resize_function__MarkerArrayHeader__markers  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers MarkerArrayHeader_message_members = {
  "mtr_prediction_msgs::msg",  // message namespace
  "MarkerArrayHeader",  // message name
  2,  // number of fields
  sizeof(mtr_prediction_msgs::msg::MarkerArrayHeader),
  MarkerArrayHeader_message_member_array,  // message members
  MarkerArrayHeader_init_function,  // function to initialize message memory (memory has to be allocated)
  MarkerArrayHeader_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t MarkerArrayHeader_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &MarkerArrayHeader_message_members,
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
get_message_type_support_handle<mtr_prediction_msgs::msg::MarkerArrayHeader>()
{
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::MarkerArrayHeader_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, mtr_prediction_msgs, msg, MarkerArrayHeader)() {
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::MarkerArrayHeader_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

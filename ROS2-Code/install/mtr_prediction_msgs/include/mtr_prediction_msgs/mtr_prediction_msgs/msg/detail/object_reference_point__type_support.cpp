// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from mtr_prediction_msgs:msg/ObjectReferencePoint.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "mtr_prediction_msgs/msg/detail/object_reference_point__struct.hpp"
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

void ObjectReferencePoint_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) mtr_prediction_msgs::msg::ObjectReferencePoint(_init);
}

void ObjectReferencePoint_fini_function(void * message_memory)
{
  auto typed_message = static_cast<mtr_prediction_msgs::msg::ObjectReferencePoint *>(message_memory);
  typed_message->~ObjectReferencePoint();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ObjectReferencePoint_message_member_array[2] = {
  {
    "value",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::ObjectReferencePoint, value),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "translation_to_geometric_center",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Vector3>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::ObjectReferencePoint, translation_to_geometric_center),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ObjectReferencePoint_message_members = {
  "mtr_prediction_msgs::msg",  // message namespace
  "ObjectReferencePoint",  // message name
  2,  // number of fields
  sizeof(mtr_prediction_msgs::msg::ObjectReferencePoint),
  ObjectReferencePoint_message_member_array,  // message members
  ObjectReferencePoint_init_function,  // function to initialize message memory (memory has to be allocated)
  ObjectReferencePoint_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ObjectReferencePoint_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ObjectReferencePoint_message_members,
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
get_message_type_support_handle<mtr_prediction_msgs::msg::ObjectReferencePoint>()
{
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::ObjectReferencePoint_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, mtr_prediction_msgs, msg, ObjectReferencePoint)() {
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::ObjectReferencePoint_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

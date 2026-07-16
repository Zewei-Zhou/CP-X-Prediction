// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from mtr_prediction_msgs:msg/ObjectState.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "mtr_prediction_msgs/msg/detail/object_state__struct.hpp"
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

void ObjectState_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) mtr_prediction_msgs::msg::ObjectState(_init);
}

void ObjectState_fini_function(void * message_memory)
{
  auto typed_message = static_cast<mtr_prediction_msgs::msg::ObjectState *>(message_memory);
  typed_message->~ObjectState();
}

size_t size_function__ObjectState__sensor_id(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<uint64_t> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ObjectState__sensor_id(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<uint64_t> *>(untyped_member);
  return &member[index];
}

void * get_function__ObjectState__sensor_id(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<uint64_t> *>(untyped_member);
  return &member[index];
}

void fetch_function__ObjectState__sensor_id(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const uint64_t *>(
    get_const_function__ObjectState__sensor_id(untyped_member, index));
  auto & value = *reinterpret_cast<uint64_t *>(untyped_value);
  value = item;
}

void assign_function__ObjectState__sensor_id(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<uint64_t *>(
    get_function__ObjectState__sensor_id(untyped_member, index));
  const auto & value = *reinterpret_cast<const uint64_t *>(untyped_value);
  item = value;
}

void resize_function__ObjectState__sensor_id(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<uint64_t> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ObjectState__continuous_state(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ObjectState__continuous_state(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__ObjectState__continuous_state(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__ObjectState__continuous_state(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__ObjectState__continuous_state(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__ObjectState__continuous_state(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__ObjectState__continuous_state(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__ObjectState__continuous_state(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ObjectState__discrete_state(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<int64_t> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ObjectState__discrete_state(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<int64_t> *>(untyped_member);
  return &member[index];
}

void * get_function__ObjectState__discrete_state(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<int64_t> *>(untyped_member);
  return &member[index];
}

void fetch_function__ObjectState__discrete_state(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const int64_t *>(
    get_const_function__ObjectState__discrete_state(untyped_member, index));
  auto & value = *reinterpret_cast<int64_t *>(untyped_value);
  value = item;
}

void assign_function__ObjectState__discrete_state(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<int64_t *>(
    get_function__ObjectState__discrete_state(untyped_member, index));
  const auto & value = *reinterpret_cast<const int64_t *>(untyped_value);
  item = value;
}

void resize_function__ObjectState__discrete_state(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<int64_t> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ObjectState__continuous_state_covariance(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ObjectState__continuous_state_covariance(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__ObjectState__continuous_state_covariance(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__ObjectState__continuous_state_covariance(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__ObjectState__continuous_state_covariance(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__ObjectState__continuous_state_covariance(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__ObjectState__continuous_state_covariance(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__ObjectState__continuous_state_covariance(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ObjectState__classifications(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<mtr_prediction_msgs::msg::ObjectClassification> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ObjectState__classifications(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<mtr_prediction_msgs::msg::ObjectClassification> *>(untyped_member);
  return &member[index];
}

void * get_function__ObjectState__classifications(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<mtr_prediction_msgs::msg::ObjectClassification> *>(untyped_member);
  return &member[index];
}

void fetch_function__ObjectState__classifications(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const mtr_prediction_msgs::msg::ObjectClassification *>(
    get_const_function__ObjectState__classifications(untyped_member, index));
  auto & value = *reinterpret_cast<mtr_prediction_msgs::msg::ObjectClassification *>(untyped_value);
  value = item;
}

void assign_function__ObjectState__classifications(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<mtr_prediction_msgs::msg::ObjectClassification *>(
    get_function__ObjectState__classifications(untyped_member, index));
  const auto & value = *reinterpret_cast<const mtr_prediction_msgs::msg::ObjectClassification *>(untyped_value);
  item = value;
}

void resize_function__ObjectState__classifications(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<mtr_prediction_msgs::msg::ObjectClassification> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ObjectState_message_member_array[8] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::ObjectState, header),  // bytes offset in struct
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
    offsetof(mtr_prediction_msgs::msg::ObjectState, model_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "sensor_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::ObjectState, sensor_id),  // bytes offset in struct
    nullptr,  // default value
    size_function__ObjectState__sensor_id,  // size() function pointer
    get_const_function__ObjectState__sensor_id,  // get_const(index) function pointer
    get_function__ObjectState__sensor_id,  // get(index) function pointer
    fetch_function__ObjectState__sensor_id,  // fetch(index, &value) function pointer
    assign_function__ObjectState__sensor_id,  // assign(index, value) function pointer
    resize_function__ObjectState__sensor_id  // resize(index) function pointer
  },
  {
    "continuous_state",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::ObjectState, continuous_state),  // bytes offset in struct
    nullptr,  // default value
    size_function__ObjectState__continuous_state,  // size() function pointer
    get_const_function__ObjectState__continuous_state,  // get_const(index) function pointer
    get_function__ObjectState__continuous_state,  // get(index) function pointer
    fetch_function__ObjectState__continuous_state,  // fetch(index, &value) function pointer
    assign_function__ObjectState__continuous_state,  // assign(index, value) function pointer
    resize_function__ObjectState__continuous_state  // resize(index) function pointer
  },
  {
    "discrete_state",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::ObjectState, discrete_state),  // bytes offset in struct
    nullptr,  // default value
    size_function__ObjectState__discrete_state,  // size() function pointer
    get_const_function__ObjectState__discrete_state,  // get_const(index) function pointer
    get_function__ObjectState__discrete_state,  // get(index) function pointer
    fetch_function__ObjectState__discrete_state,  // fetch(index, &value) function pointer
    assign_function__ObjectState__discrete_state,  // assign(index, value) function pointer
    resize_function__ObjectState__discrete_state  // resize(index) function pointer
  },
  {
    "continuous_state_covariance",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::ObjectState, continuous_state_covariance),  // bytes offset in struct
    nullptr,  // default value
    size_function__ObjectState__continuous_state_covariance,  // size() function pointer
    get_const_function__ObjectState__continuous_state_covariance,  // get_const(index) function pointer
    get_function__ObjectState__continuous_state_covariance,  // get(index) function pointer
    fetch_function__ObjectState__continuous_state_covariance,  // fetch(index, &value) function pointer
    assign_function__ObjectState__continuous_state_covariance,  // assign(index, value) function pointer
    resize_function__ObjectState__continuous_state_covariance  // resize(index) function pointer
  },
  {
    "classifications",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<mtr_prediction_msgs::msg::ObjectClassification>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::ObjectState, classifications),  // bytes offset in struct
    nullptr,  // default value
    size_function__ObjectState__classifications,  // size() function pointer
    get_const_function__ObjectState__classifications,  // get_const(index) function pointer
    get_function__ObjectState__classifications,  // get(index) function pointer
    fetch_function__ObjectState__classifications,  // fetch(index, &value) function pointer
    assign_function__ObjectState__classifications,  // assign(index, value) function pointer
    resize_function__ObjectState__classifications  // resize(index) function pointer
  },
  {
    "reference_point",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<mtr_prediction_msgs::msg::ObjectReferencePoint>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mtr_prediction_msgs::msg::ObjectState, reference_point),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ObjectState_message_members = {
  "mtr_prediction_msgs::msg",  // message namespace
  "ObjectState",  // message name
  8,  // number of fields
  sizeof(mtr_prediction_msgs::msg::ObjectState),
  ObjectState_message_member_array,  // message members
  ObjectState_init_function,  // function to initialize message memory (memory has to be allocated)
  ObjectState_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ObjectState_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ObjectState_message_members,
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
get_message_type_support_handle<mtr_prediction_msgs::msg::ObjectState>()
{
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::ObjectState_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, mtr_prediction_msgs, msg, ObjectState)() {
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_introspection_cpp::ObjectState_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

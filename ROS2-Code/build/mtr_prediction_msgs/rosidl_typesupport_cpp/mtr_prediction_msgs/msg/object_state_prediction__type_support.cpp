// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from mtr_prediction_msgs:msg/ObjectStatePrediction.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "mtr_prediction_msgs/msg/detail/object_state_prediction__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace mtr_prediction_msgs
{

namespace msg
{

namespace rosidl_typesupport_cpp
{

typedef struct _ObjectStatePrediction_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ObjectStatePrediction_type_support_ids_t;

static const _ObjectStatePrediction_type_support_ids_t _ObjectStatePrediction_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ObjectStatePrediction_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ObjectStatePrediction_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ObjectStatePrediction_type_support_symbol_names_t _ObjectStatePrediction_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, mtr_prediction_msgs, msg, ObjectStatePrediction)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, mtr_prediction_msgs, msg, ObjectStatePrediction)),
  }
};

typedef struct _ObjectStatePrediction_type_support_data_t
{
  void * data[2];
} _ObjectStatePrediction_type_support_data_t;

static _ObjectStatePrediction_type_support_data_t _ObjectStatePrediction_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ObjectStatePrediction_message_typesupport_map = {
  2,
  "mtr_prediction_msgs",
  &_ObjectStatePrediction_message_typesupport_ids.typesupport_identifier[0],
  &_ObjectStatePrediction_message_typesupport_symbol_names.symbol_name[0],
  &_ObjectStatePrediction_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ObjectStatePrediction_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ObjectStatePrediction_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace msg

}  // namespace mtr_prediction_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<mtr_prediction_msgs::msg::ObjectStatePrediction>()
{
  return &::mtr_prediction_msgs::msg::rosidl_typesupport_cpp::ObjectStatePrediction_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, mtr_prediction_msgs, msg, ObjectStatePrediction)() {
  return get_message_type_support_handle<mtr_prediction_msgs::msg::ObjectStatePrediction>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

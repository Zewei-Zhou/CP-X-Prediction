// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectReferencePoint.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__TRAITS_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "mtr_prediction_msgs/msg/detail/object_reference_point__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'translation_to_geometric_center'
#include "geometry_msgs/msg/detail/vector3__traits.hpp"

namespace mtr_prediction_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ObjectReferencePoint & msg,
  std::ostream & out)
{
  out << "{";
  // member: value
  {
    out << "value: ";
    rosidl_generator_traits::value_to_yaml(msg.value, out);
    out << ", ";
  }

  // member: translation_to_geometric_center
  {
    out << "translation_to_geometric_center: ";
    to_flow_style_yaml(msg.translation_to_geometric_center, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ObjectReferencePoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "value: ";
    rosidl_generator_traits::value_to_yaml(msg.value, out);
    out << "\n";
  }

  // member: translation_to_geometric_center
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "translation_to_geometric_center:\n";
    to_block_style_yaml(msg.translation_to_geometric_center, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ObjectReferencePoint & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace mtr_prediction_msgs

namespace rosidl_generator_traits
{

[[deprecated("use mtr_prediction_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const mtr_prediction_msgs::msg::ObjectReferencePoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  mtr_prediction_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use mtr_prediction_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const mtr_prediction_msgs::msg::ObjectReferencePoint & msg)
{
  return mtr_prediction_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<mtr_prediction_msgs::msg::ObjectReferencePoint>()
{
  return "mtr_prediction_msgs::msg::ObjectReferencePoint";
}

template<>
inline const char * name<mtr_prediction_msgs::msg::ObjectReferencePoint>()
{
  return "mtr_prediction_msgs/msg/ObjectReferencePoint";
}

template<>
struct has_fixed_size<mtr_prediction_msgs::msg::ObjectReferencePoint>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Vector3>::value> {};

template<>
struct has_bounded_size<mtr_prediction_msgs::msg::ObjectReferencePoint>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Vector3>::value> {};

template<>
struct is_message<mtr_prediction_msgs::msg::ObjectReferencePoint>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__TRAITS_HPP_

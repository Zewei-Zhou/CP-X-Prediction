// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectStatePrediction.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__TRAITS_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "mtr_prediction_msgs/msg/detail/object_state_prediction__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'states'
#include "mtr_prediction_msgs/msg/detail/object_state__traits.hpp"

namespace mtr_prediction_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ObjectStatePrediction & msg,
  std::ostream & out)
{
  out << "{";
  // member: probability
  {
    out << "probability: ";
    rosidl_generator_traits::value_to_yaml(msg.probability, out);
    out << ", ";
  }

  // member: states
  {
    if (msg.states.size() == 0) {
      out << "states: []";
    } else {
      out << "states: [";
      size_t pending_items = msg.states.size();
      for (auto item : msg.states) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ObjectStatePrediction & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: probability
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "probability: ";
    rosidl_generator_traits::value_to_yaml(msg.probability, out);
    out << "\n";
  }

  // member: states
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.states.size() == 0) {
      out << "states: []\n";
    } else {
      out << "states:\n";
      for (auto item : msg.states) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ObjectStatePrediction & msg, bool use_flow_style = false)
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
  const mtr_prediction_msgs::msg::ObjectStatePrediction & msg,
  std::ostream & out, size_t indentation = 0)
{
  mtr_prediction_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use mtr_prediction_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const mtr_prediction_msgs::msg::ObjectStatePrediction & msg)
{
  return mtr_prediction_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<mtr_prediction_msgs::msg::ObjectStatePrediction>()
{
  return "mtr_prediction_msgs::msg::ObjectStatePrediction";
}

template<>
inline const char * name<mtr_prediction_msgs::msg::ObjectStatePrediction>()
{
  return "mtr_prediction_msgs/msg/ObjectStatePrediction";
}

template<>
struct has_fixed_size<mtr_prediction_msgs::msg::ObjectStatePrediction>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<mtr_prediction_msgs::msg::ObjectStatePrediction>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<mtr_prediction_msgs::msg::ObjectStatePrediction>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__TRAITS_HPP_

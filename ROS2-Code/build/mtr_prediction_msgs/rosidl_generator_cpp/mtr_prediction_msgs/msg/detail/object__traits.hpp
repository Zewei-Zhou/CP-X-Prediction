// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from mtr_prediction_msgs:msg/Object.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT__TRAITS_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "mtr_prediction_msgs/msg/detail/object__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'state'
// Member 'state_history'
#include "mtr_prediction_msgs/msg/detail/object_state__traits.hpp"
// Member 'state_predictions'
#include "mtr_prediction_msgs/msg/detail/object_state_prediction__traits.hpp"

namespace mtr_prediction_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Object & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: existence_probability
  {
    out << "existence_probability: ";
    rosidl_generator_traits::value_to_yaml(msg.existence_probability, out);
    out << ", ";
  }

  // member: state
  {
    out << "state: ";
    to_flow_style_yaml(msg.state, out);
    out << ", ";
  }

  // member: state_history
  {
    if (msg.state_history.size() == 0) {
      out << "state_history: []";
    } else {
      out << "state_history: [";
      size_t pending_items = msg.state_history.size();
      for (auto item : msg.state_history) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: state_predictions
  {
    if (msg.state_predictions.size() == 0) {
      out << "state_predictions: []";
    } else {
      out << "state_predictions: [";
      size_t pending_items = msg.state_predictions.size();
      for (auto item : msg.state_predictions) {
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
  const Object & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: existence_probability
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "existence_probability: ";
    rosidl_generator_traits::value_to_yaml(msg.existence_probability, out);
    out << "\n";
  }

  // member: state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "state:\n";
    to_block_style_yaml(msg.state, out, indentation + 2);
  }

  // member: state_history
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.state_history.size() == 0) {
      out << "state_history: []\n";
    } else {
      out << "state_history:\n";
      for (auto item : msg.state_history) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: state_predictions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.state_predictions.size() == 0) {
      out << "state_predictions: []\n";
    } else {
      out << "state_predictions:\n";
      for (auto item : msg.state_predictions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Object & msg, bool use_flow_style = false)
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
  const mtr_prediction_msgs::msg::Object & msg,
  std::ostream & out, size_t indentation = 0)
{
  mtr_prediction_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use mtr_prediction_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const mtr_prediction_msgs::msg::Object & msg)
{
  return mtr_prediction_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<mtr_prediction_msgs::msg::Object>()
{
  return "mtr_prediction_msgs::msg::Object";
}

template<>
inline const char * name<mtr_prediction_msgs::msg::Object>()
{
  return "mtr_prediction_msgs/msg/Object";
}

template<>
struct has_fixed_size<mtr_prediction_msgs::msg::Object>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<mtr_prediction_msgs::msg::Object>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<mtr_prediction_msgs::msg::Object>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT__TRAITS_HPP_

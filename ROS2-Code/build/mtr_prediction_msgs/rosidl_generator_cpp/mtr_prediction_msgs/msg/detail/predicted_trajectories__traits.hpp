// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from mtr_prediction_msgs:msg/PredictedTrajectories.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__TRAITS_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "mtr_prediction_msgs/msg/detail/predicted_trajectories__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'predictions'
#include "mtr_prediction_msgs/msg/detail/object_prediction__traits.hpp"
// Member 'map_polylines'
#include "sensor_msgs/msg/detail/point_cloud2__traits.hpp"

namespace mtr_prediction_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const PredictedTrajectories & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: predictions
  {
    if (msg.predictions.size() == 0) {
      out << "predictions: []";
    } else {
      out << "predictions: [";
      size_t pending_items = msg.predictions.size();
      for (auto item : msg.predictions) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: map_polylines
  {
    out << "map_polylines: ";
    to_flow_style_yaml(msg.map_polylines, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PredictedTrajectories & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: predictions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.predictions.size() == 0) {
      out << "predictions: []\n";
    } else {
      out << "predictions:\n";
      for (auto item : msg.predictions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: map_polylines
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "map_polylines:\n";
    to_block_style_yaml(msg.map_polylines, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PredictedTrajectories & msg, bool use_flow_style = false)
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
  const mtr_prediction_msgs::msg::PredictedTrajectories & msg,
  std::ostream & out, size_t indentation = 0)
{
  mtr_prediction_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use mtr_prediction_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const mtr_prediction_msgs::msg::PredictedTrajectories & msg)
{
  return mtr_prediction_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<mtr_prediction_msgs::msg::PredictedTrajectories>()
{
  return "mtr_prediction_msgs::msg::PredictedTrajectories";
}

template<>
inline const char * name<mtr_prediction_msgs::msg::PredictedTrajectories>()
{
  return "mtr_prediction_msgs/msg/PredictedTrajectories";
}

template<>
struct has_fixed_size<mtr_prediction_msgs::msg::PredictedTrajectories>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<mtr_prediction_msgs::msg::PredictedTrajectories>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<mtr_prediction_msgs::msg::PredictedTrajectories>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__TRAITS_HPP_

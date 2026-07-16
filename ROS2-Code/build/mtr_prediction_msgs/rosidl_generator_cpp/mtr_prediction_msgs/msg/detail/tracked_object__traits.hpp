// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from mtr_prediction_msgs:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__TRAITS_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "mtr_prediction_msgs/msg/detail/tracked_object__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"
// Member 'velocity'
#include "geometry_msgs/msg/detail/twist__traits.hpp"
// Member 'size'
#include "geometry_msgs/msg/detail/vector3__traits.hpp"
// Member 'track_history'
#include "mtr_prediction_msgs/msg/detail/object_state__traits.hpp"

namespace mtr_prediction_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const TrackedObject & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: object_id
  {
    out << "object_id: ";
    rosidl_generator_traits::value_to_yaml(msg.object_id, out);
    out << ", ";
  }

  // member: model_id
  {
    out << "model_id: ";
    rosidl_generator_traits::value_to_yaml(msg.model_id, out);
    out << ", ";
  }

  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
    out << ", ";
  }

  // member: velocity
  {
    out << "velocity: ";
    to_flow_style_yaml(msg.velocity, out);
    out << ", ";
  }

  // member: size
  {
    out << "size: ";
    to_flow_style_yaml(msg.size, out);
    out << ", ";
  }

  // member: object_type
  {
    out << "object_type: ";
    rosidl_generator_traits::value_to_yaml(msg.object_type, out);
    out << ", ";
  }

  // member: track_history
  {
    if (msg.track_history.size() == 0) {
      out << "track_history: []";
    } else {
      out << "track_history: [";
      size_t pending_items = msg.track_history.size();
      for (auto item : msg.track_history) {
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
  const TrackedObject & msg,
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

  // member: object_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_id: ";
    rosidl_generator_traits::value_to_yaml(msg.object_id, out);
    out << "\n";
  }

  // member: model_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "model_id: ";
    rosidl_generator_traits::value_to_yaml(msg.model_id, out);
    out << "\n";
  }

  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }

  // member: velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "velocity:\n";
    to_block_style_yaml(msg.velocity, out, indentation + 2);
  }

  // member: size
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "size:\n";
    to_block_style_yaml(msg.size, out, indentation + 2);
  }

  // member: object_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_type: ";
    rosidl_generator_traits::value_to_yaml(msg.object_type, out);
    out << "\n";
  }

  // member: track_history
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.track_history.size() == 0) {
      out << "track_history: []\n";
    } else {
      out << "track_history:\n";
      for (auto item : msg.track_history) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TrackedObject & msg, bool use_flow_style = false)
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
  const mtr_prediction_msgs::msg::TrackedObject & msg,
  std::ostream & out, size_t indentation = 0)
{
  mtr_prediction_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use mtr_prediction_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const mtr_prediction_msgs::msg::TrackedObject & msg)
{
  return mtr_prediction_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<mtr_prediction_msgs::msg::TrackedObject>()
{
  return "mtr_prediction_msgs::msg::TrackedObject";
}

template<>
inline const char * name<mtr_prediction_msgs::msg::TrackedObject>()
{
  return "mtr_prediction_msgs/msg/TrackedObject";
}

template<>
struct has_fixed_size<mtr_prediction_msgs::msg::TrackedObject>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<mtr_prediction_msgs::msg::TrackedObject>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<mtr_prediction_msgs::msg::TrackedObject>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__TRAITS_HPP_

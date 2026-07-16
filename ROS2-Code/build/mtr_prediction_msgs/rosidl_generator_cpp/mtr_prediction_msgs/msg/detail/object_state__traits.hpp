// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectState.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__TRAITS_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "mtr_prediction_msgs/msg/detail/object_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'classifications'
#include "mtr_prediction_msgs/msg/detail/object_classification__traits.hpp"
// Member 'reference_point'
#include "mtr_prediction_msgs/msg/detail/object_reference_point__traits.hpp"

namespace mtr_prediction_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ObjectState & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: model_id
  {
    out << "model_id: ";
    rosidl_generator_traits::value_to_yaml(msg.model_id, out);
    out << ", ";
  }

  // member: sensor_id
  {
    if (msg.sensor_id.size() == 0) {
      out << "sensor_id: []";
    } else {
      out << "sensor_id: [";
      size_t pending_items = msg.sensor_id.size();
      for (auto item : msg.sensor_id) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: continuous_state
  {
    if (msg.continuous_state.size() == 0) {
      out << "continuous_state: []";
    } else {
      out << "continuous_state: [";
      size_t pending_items = msg.continuous_state.size();
      for (auto item : msg.continuous_state) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: discrete_state
  {
    if (msg.discrete_state.size() == 0) {
      out << "discrete_state: []";
    } else {
      out << "discrete_state: [";
      size_t pending_items = msg.discrete_state.size();
      for (auto item : msg.discrete_state) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: continuous_state_covariance
  {
    if (msg.continuous_state_covariance.size() == 0) {
      out << "continuous_state_covariance: []";
    } else {
      out << "continuous_state_covariance: [";
      size_t pending_items = msg.continuous_state_covariance.size();
      for (auto item : msg.continuous_state_covariance) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: classifications
  {
    if (msg.classifications.size() == 0) {
      out << "classifications: []";
    } else {
      out << "classifications: [";
      size_t pending_items = msg.classifications.size();
      for (auto item : msg.classifications) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: reference_point
  {
    out << "reference_point: ";
    to_flow_style_yaml(msg.reference_point, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ObjectState & msg,
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

  // member: model_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "model_id: ";
    rosidl_generator_traits::value_to_yaml(msg.model_id, out);
    out << "\n";
  }

  // member: sensor_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.sensor_id.size() == 0) {
      out << "sensor_id: []\n";
    } else {
      out << "sensor_id:\n";
      for (auto item : msg.sensor_id) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: continuous_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.continuous_state.size() == 0) {
      out << "continuous_state: []\n";
    } else {
      out << "continuous_state:\n";
      for (auto item : msg.continuous_state) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: discrete_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.discrete_state.size() == 0) {
      out << "discrete_state: []\n";
    } else {
      out << "discrete_state:\n";
      for (auto item : msg.discrete_state) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: continuous_state_covariance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.continuous_state_covariance.size() == 0) {
      out << "continuous_state_covariance: []\n";
    } else {
      out << "continuous_state_covariance:\n";
      for (auto item : msg.continuous_state_covariance) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: classifications
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.classifications.size() == 0) {
      out << "classifications: []\n";
    } else {
      out << "classifications:\n";
      for (auto item : msg.classifications) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: reference_point
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reference_point:\n";
    to_block_style_yaml(msg.reference_point, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ObjectState & msg, bool use_flow_style = false)
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
  const mtr_prediction_msgs::msg::ObjectState & msg,
  std::ostream & out, size_t indentation = 0)
{
  mtr_prediction_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use mtr_prediction_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const mtr_prediction_msgs::msg::ObjectState & msg)
{
  return mtr_prediction_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<mtr_prediction_msgs::msg::ObjectState>()
{
  return "mtr_prediction_msgs::msg::ObjectState";
}

template<>
inline const char * name<mtr_prediction_msgs::msg::ObjectState>()
{
  return "mtr_prediction_msgs/msg/ObjectState";
}

template<>
struct has_fixed_size<mtr_prediction_msgs::msg::ObjectState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<mtr_prediction_msgs::msg::ObjectState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<mtr_prediction_msgs::msg::ObjectState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__TRAITS_HPP_

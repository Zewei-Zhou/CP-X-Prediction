// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectState.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/object_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_ObjectState_reference_point
{
public:
  explicit Init_ObjectState_reference_point(::mtr_prediction_msgs::msg::ObjectState & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::ObjectState reference_point(::mtr_prediction_msgs::msg::ObjectState::_reference_point_type arg)
  {
    msg_.reference_point = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectState msg_;
};

class Init_ObjectState_classifications
{
public:
  explicit Init_ObjectState_classifications(::mtr_prediction_msgs::msg::ObjectState & msg)
  : msg_(msg)
  {}
  Init_ObjectState_reference_point classifications(::mtr_prediction_msgs::msg::ObjectState::_classifications_type arg)
  {
    msg_.classifications = std::move(arg);
    return Init_ObjectState_reference_point(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectState msg_;
};

class Init_ObjectState_continuous_state_covariance
{
public:
  explicit Init_ObjectState_continuous_state_covariance(::mtr_prediction_msgs::msg::ObjectState & msg)
  : msg_(msg)
  {}
  Init_ObjectState_classifications continuous_state_covariance(::mtr_prediction_msgs::msg::ObjectState::_continuous_state_covariance_type arg)
  {
    msg_.continuous_state_covariance = std::move(arg);
    return Init_ObjectState_classifications(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectState msg_;
};

class Init_ObjectState_discrete_state
{
public:
  explicit Init_ObjectState_discrete_state(::mtr_prediction_msgs::msg::ObjectState & msg)
  : msg_(msg)
  {}
  Init_ObjectState_continuous_state_covariance discrete_state(::mtr_prediction_msgs::msg::ObjectState::_discrete_state_type arg)
  {
    msg_.discrete_state = std::move(arg);
    return Init_ObjectState_continuous_state_covariance(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectState msg_;
};

class Init_ObjectState_continuous_state
{
public:
  explicit Init_ObjectState_continuous_state(::mtr_prediction_msgs::msg::ObjectState & msg)
  : msg_(msg)
  {}
  Init_ObjectState_discrete_state continuous_state(::mtr_prediction_msgs::msg::ObjectState::_continuous_state_type arg)
  {
    msg_.continuous_state = std::move(arg);
    return Init_ObjectState_discrete_state(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectState msg_;
};

class Init_ObjectState_sensor_id
{
public:
  explicit Init_ObjectState_sensor_id(::mtr_prediction_msgs::msg::ObjectState & msg)
  : msg_(msg)
  {}
  Init_ObjectState_continuous_state sensor_id(::mtr_prediction_msgs::msg::ObjectState::_sensor_id_type arg)
  {
    msg_.sensor_id = std::move(arg);
    return Init_ObjectState_continuous_state(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectState msg_;
};

class Init_ObjectState_model_id
{
public:
  explicit Init_ObjectState_model_id(::mtr_prediction_msgs::msg::ObjectState & msg)
  : msg_(msg)
  {}
  Init_ObjectState_sensor_id model_id(::mtr_prediction_msgs::msg::ObjectState::_model_id_type arg)
  {
    msg_.model_id = std::move(arg);
    return Init_ObjectState_sensor_id(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectState msg_;
};

class Init_ObjectState_header
{
public:
  Init_ObjectState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObjectState_model_id header(::mtr_prediction_msgs::msg::ObjectState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ObjectState_model_id(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::ObjectState>()
{
  return mtr_prediction_msgs::msg::builder::Init_ObjectState_header();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__BUILDER_HPP_

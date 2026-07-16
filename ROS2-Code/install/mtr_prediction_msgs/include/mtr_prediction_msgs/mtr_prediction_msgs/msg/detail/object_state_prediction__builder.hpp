// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectStatePrediction.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/object_state_prediction__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_ObjectStatePrediction_states
{
public:
  explicit Init_ObjectStatePrediction_states(::mtr_prediction_msgs::msg::ObjectStatePrediction & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::ObjectStatePrediction states(::mtr_prediction_msgs::msg::ObjectStatePrediction::_states_type arg)
  {
    msg_.states = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectStatePrediction msg_;
};

class Init_ObjectStatePrediction_probability
{
public:
  Init_ObjectStatePrediction_probability()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObjectStatePrediction_states probability(::mtr_prediction_msgs::msg::ObjectStatePrediction::_probability_type arg)
  {
    msg_.probability = std::move(arg);
    return Init_ObjectStatePrediction_states(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectStatePrediction msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::ObjectStatePrediction>()
{
  return mtr_prediction_msgs::msg::builder::Init_ObjectStatePrediction_probability();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__BUILDER_HPP_

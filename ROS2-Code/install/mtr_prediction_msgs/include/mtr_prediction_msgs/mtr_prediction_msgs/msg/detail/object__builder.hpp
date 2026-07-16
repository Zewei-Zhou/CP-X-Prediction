// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/Object.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/object__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_Object_state_predictions
{
public:
  explicit Init_Object_state_predictions(::mtr_prediction_msgs::msg::Object & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::Object state_predictions(::mtr_prediction_msgs::msg::Object::_state_predictions_type arg)
  {
    msg_.state_predictions = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::Object msg_;
};

class Init_Object_state_history
{
public:
  explicit Init_Object_state_history(::mtr_prediction_msgs::msg::Object & msg)
  : msg_(msg)
  {}
  Init_Object_state_predictions state_history(::mtr_prediction_msgs::msg::Object::_state_history_type arg)
  {
    msg_.state_history = std::move(arg);
    return Init_Object_state_predictions(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::Object msg_;
};

class Init_Object_state
{
public:
  explicit Init_Object_state(::mtr_prediction_msgs::msg::Object & msg)
  : msg_(msg)
  {}
  Init_Object_state_history state(::mtr_prediction_msgs::msg::Object::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_Object_state_history(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::Object msg_;
};

class Init_Object_existence_probability
{
public:
  explicit Init_Object_existence_probability(::mtr_prediction_msgs::msg::Object & msg)
  : msg_(msg)
  {}
  Init_Object_state existence_probability(::mtr_prediction_msgs::msg::Object::_existence_probability_type arg)
  {
    msg_.existence_probability = std::move(arg);
    return Init_Object_state(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::Object msg_;
};

class Init_Object_id
{
public:
  Init_Object_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Object_existence_probability id(::mtr_prediction_msgs::msg::Object::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_Object_existence_probability(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::Object msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::Object>()
{
  return mtr_prediction_msgs::msg::builder::Init_Object_id();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT__BUILDER_HPP_

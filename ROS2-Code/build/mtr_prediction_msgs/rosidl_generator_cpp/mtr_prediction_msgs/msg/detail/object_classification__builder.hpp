// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectClassification.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_CLASSIFICATION__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_CLASSIFICATION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/object_classification__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_ObjectClassification_probability
{
public:
  explicit Init_ObjectClassification_probability(::mtr_prediction_msgs::msg::ObjectClassification & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::ObjectClassification probability(::mtr_prediction_msgs::msg::ObjectClassification::_probability_type arg)
  {
    msg_.probability = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectClassification msg_;
};

class Init_ObjectClassification_type
{
public:
  Init_ObjectClassification_type()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObjectClassification_probability type(::mtr_prediction_msgs::msg::ObjectClassification::_type_type arg)
  {
    msg_.type = std::move(arg);
    return Init_ObjectClassification_probability(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectClassification msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::ObjectClassification>()
{
  return mtr_prediction_msgs::msg::builder::Init_ObjectClassification_type();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_CLASSIFICATION__BUILDER_HPP_

// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectPrediction.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_PREDICTION__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_PREDICTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/object_prediction__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_ObjectPrediction_trajectories
{
public:
  explicit Init_ObjectPrediction_trajectories(::mtr_prediction_msgs::msg::ObjectPrediction & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::ObjectPrediction trajectories(::mtr_prediction_msgs::msg::ObjectPrediction::_trajectories_type arg)
  {
    msg_.trajectories = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectPrediction msg_;
};

class Init_ObjectPrediction_object_type
{
public:
  explicit Init_ObjectPrediction_object_type(::mtr_prediction_msgs::msg::ObjectPrediction & msg)
  : msg_(msg)
  {}
  Init_ObjectPrediction_trajectories object_type(::mtr_prediction_msgs::msg::ObjectPrediction::_object_type_type arg)
  {
    msg_.object_type = std::move(arg);
    return Init_ObjectPrediction_trajectories(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectPrediction msg_;
};

class Init_ObjectPrediction_object_id
{
public:
  Init_ObjectPrediction_object_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObjectPrediction_object_type object_id(::mtr_prediction_msgs::msg::ObjectPrediction::_object_id_type arg)
  {
    msg_.object_id = std::move(arg);
    return Init_ObjectPrediction_object_type(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectPrediction msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::ObjectPrediction>()
{
  return mtr_prediction_msgs::msg::builder::Init_ObjectPrediction_object_id();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_PREDICTION__BUILDER_HPP_

// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectReferencePoint.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/object_reference_point__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_ObjectReferencePoint_translation_to_geometric_center
{
public:
  explicit Init_ObjectReferencePoint_translation_to_geometric_center(::mtr_prediction_msgs::msg::ObjectReferencePoint & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::ObjectReferencePoint translation_to_geometric_center(::mtr_prediction_msgs::msg::ObjectReferencePoint::_translation_to_geometric_center_type arg)
  {
    msg_.translation_to_geometric_center = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectReferencePoint msg_;
};

class Init_ObjectReferencePoint_value
{
public:
  Init_ObjectReferencePoint_value()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObjectReferencePoint_translation_to_geometric_center value(::mtr_prediction_msgs::msg::ObjectReferencePoint::_value_type arg)
  {
    msg_.value = std::move(arg);
    return Init_ObjectReferencePoint_translation_to_geometric_center(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectReferencePoint msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::ObjectReferencePoint>()
{
  return mtr_prediction_msgs::msg::builder::Init_ObjectReferencePoint_value();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__BUILDER_HPP_

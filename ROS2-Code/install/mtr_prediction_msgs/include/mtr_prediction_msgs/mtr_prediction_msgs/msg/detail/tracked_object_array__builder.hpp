// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/tracked_object_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_TrackedObjectArray_objects
{
public:
  explicit Init_TrackedObjectArray_objects(::mtr_prediction_msgs::msg::TrackedObjectArray & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::TrackedObjectArray objects(::mtr_prediction_msgs::msg::TrackedObjectArray::_objects_type arg)
  {
    msg_.objects = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::TrackedObjectArray msg_;
};

class Init_TrackedObjectArray_header
{
public:
  Init_TrackedObjectArray_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrackedObjectArray_objects header(::mtr_prediction_msgs::msg::TrackedObjectArray::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_TrackedObjectArray_objects(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::TrackedObjectArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::TrackedObjectArray>()
{
  return mtr_prediction_msgs::msg::builder::Init_TrackedObjectArray_header();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__BUILDER_HPP_

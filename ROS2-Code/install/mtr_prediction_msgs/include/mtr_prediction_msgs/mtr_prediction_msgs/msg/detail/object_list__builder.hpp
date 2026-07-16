// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectList.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_LIST__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_LIST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/object_list__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_ObjectList_objects
{
public:
  explicit Init_ObjectList_objects(::mtr_prediction_msgs::msg::ObjectList & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::ObjectList objects(::mtr_prediction_msgs::msg::ObjectList::_objects_type arg)
  {
    msg_.objects = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectList msg_;
};

class Init_ObjectList_header
{
public:
  Init_ObjectList_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObjectList_objects header(::mtr_prediction_msgs::msg::ObjectList::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ObjectList_objects(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::ObjectList msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::ObjectList>()
{
  return mtr_prediction_msgs::msg::builder::Init_ObjectList_header();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_LIST__BUILDER_HPP_

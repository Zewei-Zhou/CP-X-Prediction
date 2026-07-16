// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/MarkerArrayHeader.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__MARKER_ARRAY_HEADER__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__MARKER_ARRAY_HEADER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/marker_array_header__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_MarkerArrayHeader_markers
{
public:
  explicit Init_MarkerArrayHeader_markers(::mtr_prediction_msgs::msg::MarkerArrayHeader & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::MarkerArrayHeader markers(::mtr_prediction_msgs::msg::MarkerArrayHeader::_markers_type arg)
  {
    msg_.markers = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::MarkerArrayHeader msg_;
};

class Init_MarkerArrayHeader_header
{
public:
  Init_MarkerArrayHeader_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MarkerArrayHeader_markers header(::mtr_prediction_msgs::msg::MarkerArrayHeader::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_MarkerArrayHeader_markers(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::MarkerArrayHeader msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::MarkerArrayHeader>()
{
  return mtr_prediction_msgs::msg::builder::Init_MarkerArrayHeader_header();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__MARKER_ARRAY_HEADER__BUILDER_HPP_

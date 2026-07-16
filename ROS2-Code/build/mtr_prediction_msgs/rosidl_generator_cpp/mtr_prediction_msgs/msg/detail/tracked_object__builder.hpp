// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/tracked_object__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_TrackedObject_track_history
{
public:
  explicit Init_TrackedObject_track_history(::mtr_prediction_msgs::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::TrackedObject track_history(::mtr_prediction_msgs::msg::TrackedObject::_track_history_type arg)
  {
    msg_.track_history = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::TrackedObject msg_;
};

class Init_TrackedObject_object_type
{
public:
  explicit Init_TrackedObject_object_type(::mtr_prediction_msgs::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  Init_TrackedObject_track_history object_type(::mtr_prediction_msgs::msg::TrackedObject::_object_type_type arg)
  {
    msg_.object_type = std::move(arg);
    return Init_TrackedObject_track_history(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::TrackedObject msg_;
};

class Init_TrackedObject_size
{
public:
  explicit Init_TrackedObject_size(::mtr_prediction_msgs::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  Init_TrackedObject_object_type size(::mtr_prediction_msgs::msg::TrackedObject::_size_type arg)
  {
    msg_.size = std::move(arg);
    return Init_TrackedObject_object_type(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::TrackedObject msg_;
};

class Init_TrackedObject_velocity
{
public:
  explicit Init_TrackedObject_velocity(::mtr_prediction_msgs::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  Init_TrackedObject_size velocity(::mtr_prediction_msgs::msg::TrackedObject::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_TrackedObject_size(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::TrackedObject msg_;
};

class Init_TrackedObject_pose
{
public:
  explicit Init_TrackedObject_pose(::mtr_prediction_msgs::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  Init_TrackedObject_velocity pose(::mtr_prediction_msgs::msg::TrackedObject::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_TrackedObject_velocity(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::TrackedObject msg_;
};

class Init_TrackedObject_model_id
{
public:
  explicit Init_TrackedObject_model_id(::mtr_prediction_msgs::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  Init_TrackedObject_pose model_id(::mtr_prediction_msgs::msg::TrackedObject::_model_id_type arg)
  {
    msg_.model_id = std::move(arg);
    return Init_TrackedObject_pose(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::TrackedObject msg_;
};

class Init_TrackedObject_object_id
{
public:
  explicit Init_TrackedObject_object_id(::mtr_prediction_msgs::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  Init_TrackedObject_model_id object_id(::mtr_prediction_msgs::msg::TrackedObject::_object_id_type arg)
  {
    msg_.object_id = std::move(arg);
    return Init_TrackedObject_model_id(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::TrackedObject msg_;
};

class Init_TrackedObject_header
{
public:
  Init_TrackedObject_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrackedObject_object_id header(::mtr_prediction_msgs::msg::TrackedObject::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_TrackedObject_object_id(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::TrackedObject msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::TrackedObject>()
{
  return mtr_prediction_msgs::msg::builder::Init_TrackedObject_header();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__BUILDER_HPP_

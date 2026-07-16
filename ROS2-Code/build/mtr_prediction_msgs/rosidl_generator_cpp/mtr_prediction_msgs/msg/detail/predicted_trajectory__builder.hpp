// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/PredictedTrajectory.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORY__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/predicted_trajectory__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_PredictedTrajectory_velocities
{
public:
  explicit Init_PredictedTrajectory_velocities(::mtr_prediction_msgs::msg::PredictedTrajectory & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::PredictedTrajectory velocities(::mtr_prediction_msgs::msg::PredictedTrajectory::_velocities_type arg)
  {
    msg_.velocities = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::PredictedTrajectory msg_;
};

class Init_PredictedTrajectory_waypoints
{
public:
  explicit Init_PredictedTrajectory_waypoints(::mtr_prediction_msgs::msg::PredictedTrajectory & msg)
  : msg_(msg)
  {}
  Init_PredictedTrajectory_velocities waypoints(::mtr_prediction_msgs::msg::PredictedTrajectory::_waypoints_type arg)
  {
    msg_.waypoints = std::move(arg);
    return Init_PredictedTrajectory_velocities(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::PredictedTrajectory msg_;
};

class Init_PredictedTrajectory_confidence
{
public:
  Init_PredictedTrajectory_confidence()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PredictedTrajectory_waypoints confidence(::mtr_prediction_msgs::msg::PredictedTrajectory::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_PredictedTrajectory_waypoints(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::PredictedTrajectory msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::PredictedTrajectory>()
{
  return mtr_prediction_msgs::msg::builder::Init_PredictedTrajectory_confidence();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORY__BUILDER_HPP_

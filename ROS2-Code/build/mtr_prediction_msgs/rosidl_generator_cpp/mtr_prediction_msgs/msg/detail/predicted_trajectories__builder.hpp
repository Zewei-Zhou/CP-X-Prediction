// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mtr_prediction_msgs:msg/PredictedTrajectories.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__BUILDER_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mtr_prediction_msgs/msg/detail/predicted_trajectories__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mtr_prediction_msgs
{

namespace msg
{

namespace builder
{

class Init_PredictedTrajectories_map_polylines
{
public:
  explicit Init_PredictedTrajectories_map_polylines(::mtr_prediction_msgs::msg::PredictedTrajectories & msg)
  : msg_(msg)
  {}
  ::mtr_prediction_msgs::msg::PredictedTrajectories map_polylines(::mtr_prediction_msgs::msg::PredictedTrajectories::_map_polylines_type arg)
  {
    msg_.map_polylines = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::PredictedTrajectories msg_;
};

class Init_PredictedTrajectories_predictions
{
public:
  explicit Init_PredictedTrajectories_predictions(::mtr_prediction_msgs::msg::PredictedTrajectories & msg)
  : msg_(msg)
  {}
  Init_PredictedTrajectories_map_polylines predictions(::mtr_prediction_msgs::msg::PredictedTrajectories::_predictions_type arg)
  {
    msg_.predictions = std::move(arg);
    return Init_PredictedTrajectories_map_polylines(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::PredictedTrajectories msg_;
};

class Init_PredictedTrajectories_header
{
public:
  Init_PredictedTrajectories_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PredictedTrajectories_predictions header(::mtr_prediction_msgs::msg::PredictedTrajectories::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_PredictedTrajectories_predictions(msg_);
  }

private:
  ::mtr_prediction_msgs::msg::PredictedTrajectories msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mtr_prediction_msgs::msg::PredictedTrajectories>()
{
  return mtr_prediction_msgs::msg::builder::Init_PredictedTrajectories_header();
}

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__BUILDER_HPP_

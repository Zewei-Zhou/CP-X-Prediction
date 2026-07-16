// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mtr_prediction_msgs:msg/PredictedTrajectories.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__STRUCT_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'predictions'
#include "mtr_prediction_msgs/msg/detail/object_prediction__struct.hpp"
// Member 'map_polylines'
#include "sensor_msgs/msg/detail/point_cloud2__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__mtr_prediction_msgs__msg__PredictedTrajectories __attribute__((deprecated))
#else
# define DEPRECATED__mtr_prediction_msgs__msg__PredictedTrajectories __declspec(deprecated)
#endif

namespace mtr_prediction_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PredictedTrajectories_
{
  using Type = PredictedTrajectories_<ContainerAllocator>;

  explicit PredictedTrajectories_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    map_polylines(_init)
  {
    (void)_init;
  }

  explicit PredictedTrajectories_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    map_polylines(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _predictions_type =
    std::vector<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator>>>;
  _predictions_type predictions;
  using _map_polylines_type =
    sensor_msgs::msg::PointCloud2_<ContainerAllocator>;
  _map_polylines_type map_polylines;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__predictions(
    const std::vector<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator>>> & _arg)
  {
    this->predictions = _arg;
    return *this;
  }
  Type & set__map_polylines(
    const sensor_msgs::msg::PointCloud2_<ContainerAllocator> & _arg)
  {
    this->map_polylines = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator> *;
  using ConstRawPtr =
    const mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mtr_prediction_msgs__msg__PredictedTrajectories
    std::shared_ptr<mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mtr_prediction_msgs__msg__PredictedTrajectories
    std::shared_ptr<mtr_prediction_msgs::msg::PredictedTrajectories_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PredictedTrajectories_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->predictions != other.predictions) {
      return false;
    }
    if (this->map_polylines != other.map_polylines) {
      return false;
    }
    return true;
  }
  bool operator!=(const PredictedTrajectories_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PredictedTrajectories_

// alias to use template instance with default allocator
using PredictedTrajectories =
  mtr_prediction_msgs::msg::PredictedTrajectories_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__PREDICTED_TRAJECTORIES__STRUCT_HPP_

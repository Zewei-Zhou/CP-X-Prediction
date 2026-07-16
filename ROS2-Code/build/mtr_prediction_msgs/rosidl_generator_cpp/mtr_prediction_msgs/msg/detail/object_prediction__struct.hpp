// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectPrediction.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_PREDICTION__STRUCT_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_PREDICTION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'trajectories'
#include "mtr_prediction_msgs/msg/detail/predicted_trajectory__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__mtr_prediction_msgs__msg__ObjectPrediction __attribute__((deprecated))
#else
# define DEPRECATED__mtr_prediction_msgs__msg__ObjectPrediction __declspec(deprecated)
#endif

namespace mtr_prediction_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ObjectPrediction_
{
  using Type = ObjectPrediction_<ContainerAllocator>;

  explicit ObjectPrediction_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->object_id = 0ull;
      this->object_type = 0;
    }
  }

  explicit ObjectPrediction_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->object_id = 0ull;
      this->object_type = 0;
    }
  }

  // field types and members
  using _object_id_type =
    uint64_t;
  _object_id_type object_id;
  using _object_type_type =
    uint8_t;
  _object_type_type object_type;
  using _trajectories_type =
    std::vector<mtr_prediction_msgs::msg::PredictedTrajectory_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::PredictedTrajectory_<ContainerAllocator>>>;
  _trajectories_type trajectories;

  // setters for named parameter idiom
  Type & set__object_id(
    const uint64_t & _arg)
  {
    this->object_id = _arg;
    return *this;
  }
  Type & set__object_type(
    const uint8_t & _arg)
  {
    this->object_type = _arg;
    return *this;
  }
  Type & set__trajectories(
    const std::vector<mtr_prediction_msgs::msg::PredictedTrajectory_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::PredictedTrajectory_<ContainerAllocator>>> & _arg)
  {
    this->trajectories = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator> *;
  using ConstRawPtr =
    const mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mtr_prediction_msgs__msg__ObjectPrediction
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mtr_prediction_msgs__msg__ObjectPrediction
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectPrediction_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ObjectPrediction_ & other) const
  {
    if (this->object_id != other.object_id) {
      return false;
    }
    if (this->object_type != other.object_type) {
      return false;
    }
    if (this->trajectories != other.trajectories) {
      return false;
    }
    return true;
  }
  bool operator!=(const ObjectPrediction_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ObjectPrediction_

// alias to use template instance with default allocator
using ObjectPrediction =
  mtr_prediction_msgs::msg::ObjectPrediction_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_PREDICTION__STRUCT_HPP_

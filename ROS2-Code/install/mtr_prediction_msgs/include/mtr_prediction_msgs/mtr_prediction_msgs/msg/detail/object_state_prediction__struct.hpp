// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectStatePrediction.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__STRUCT_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'states'
#include "mtr_prediction_msgs/msg/detail/object_state__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__mtr_prediction_msgs__msg__ObjectStatePrediction __attribute__((deprecated))
#else
# define DEPRECATED__mtr_prediction_msgs__msg__ObjectStatePrediction __declspec(deprecated)
#endif

namespace mtr_prediction_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ObjectStatePrediction_
{
  using Type = ObjectStatePrediction_<ContainerAllocator>;

  explicit ObjectStatePrediction_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->probability = 0.0;
    }
  }

  explicit ObjectStatePrediction_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->probability = 0.0;
    }
  }

  // field types and members
  using _probability_type =
    double;
  _probability_type probability;
  using _states_type =
    std::vector<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>>>;
  _states_type states;

  // setters for named parameter idiom
  Type & set__probability(
    const double & _arg)
  {
    this->probability = _arg;
    return *this;
  }
  Type & set__states(
    const std::vector<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>>> & _arg)
  {
    this->states = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator> *;
  using ConstRawPtr =
    const mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mtr_prediction_msgs__msg__ObjectStatePrediction
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mtr_prediction_msgs__msg__ObjectStatePrediction
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectStatePrediction_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ObjectStatePrediction_ & other) const
  {
    if (this->probability != other.probability) {
      return false;
    }
    if (this->states != other.states) {
      return false;
    }
    return true;
  }
  bool operator!=(const ObjectStatePrediction_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ObjectStatePrediction_

// alias to use template instance with default allocator
using ObjectStatePrediction =
  mtr_prediction_msgs::msg::ObjectStatePrediction_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE_PREDICTION__STRUCT_HPP_

// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectState.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__STRUCT_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__STRUCT_HPP_

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
// Member 'classifications'
#include "mtr_prediction_msgs/msg/detail/object_classification__struct.hpp"
// Member 'reference_point'
#include "mtr_prediction_msgs/msg/detail/object_reference_point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__mtr_prediction_msgs__msg__ObjectState __attribute__((deprecated))
#else
# define DEPRECATED__mtr_prediction_msgs__msg__ObjectState __declspec(deprecated)
#endif

namespace mtr_prediction_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ObjectState_
{
  using Type = ObjectState_<ContainerAllocator>;

  explicit ObjectState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    reference_point(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->model_id = 0;
    }
  }

  explicit ObjectState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    reference_point(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->model_id = 0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _model_id_type =
    uint8_t;
  _model_id_type model_id;
  using _sensor_id_type =
    std::vector<uint64_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint64_t>>;
  _sensor_id_type sensor_id;
  using _continuous_state_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _continuous_state_type continuous_state;
  using _discrete_state_type =
    std::vector<int64_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int64_t>>;
  _discrete_state_type discrete_state;
  using _continuous_state_covariance_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _continuous_state_covariance_type continuous_state_covariance;
  using _classifications_type =
    std::vector<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator>>>;
  _classifications_type classifications;
  using _reference_point_type =
    mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator>;
  _reference_point_type reference_point;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__model_id(
    const uint8_t & _arg)
  {
    this->model_id = _arg;
    return *this;
  }
  Type & set__sensor_id(
    const std::vector<uint64_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint64_t>> & _arg)
  {
    this->sensor_id = _arg;
    return *this;
  }
  Type & set__continuous_state(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->continuous_state = _arg;
    return *this;
  }
  Type & set__discrete_state(
    const std::vector<int64_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int64_t>> & _arg)
  {
    this->discrete_state = _arg;
    return *this;
  }
  Type & set__continuous_state_covariance(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->continuous_state_covariance = _arg;
    return *this;
  }
  Type & set__classifications(
    const std::vector<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator>>> & _arg)
  {
    this->classifications = _arg;
    return *this;
  }
  Type & set__reference_point(
    const mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator> & _arg)
  {
    this->reference_point = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator> *;
  using ConstRawPtr =
    const mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mtr_prediction_msgs__msg__ObjectState
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mtr_prediction_msgs__msg__ObjectState
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ObjectState_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->model_id != other.model_id) {
      return false;
    }
    if (this->sensor_id != other.sensor_id) {
      return false;
    }
    if (this->continuous_state != other.continuous_state) {
      return false;
    }
    if (this->discrete_state != other.discrete_state) {
      return false;
    }
    if (this->continuous_state_covariance != other.continuous_state_covariance) {
      return false;
    }
    if (this->classifications != other.classifications) {
      return false;
    }
    if (this->reference_point != other.reference_point) {
      return false;
    }
    return true;
  }
  bool operator!=(const ObjectState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ObjectState_

// alias to use template instance with default allocator
using ObjectState =
  mtr_prediction_msgs::msg::ObjectState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_STATE__STRUCT_HPP_

// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mtr_prediction_msgs:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__STRUCT_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__STRUCT_HPP_

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
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"
// Member 'velocity'
#include "geometry_msgs/msg/detail/twist__struct.hpp"
// Member 'size'
#include "geometry_msgs/msg/detail/vector3__struct.hpp"
// Member 'track_history'
#include "mtr_prediction_msgs/msg/detail/object_state__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__mtr_prediction_msgs__msg__TrackedObject __attribute__((deprecated))
#else
# define DEPRECATED__mtr_prediction_msgs__msg__TrackedObject __declspec(deprecated)
#endif

namespace mtr_prediction_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TrackedObject_
{
  using Type = TrackedObject_<ContainerAllocator>;

  explicit TrackedObject_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    pose(_init),
    velocity(_init),
    size(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->object_id = 0ull;
      this->model_id = 0;
      this->object_type = 0;
    }
  }

  explicit TrackedObject_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    pose(_alloc, _init),
    velocity(_alloc, _init),
    size(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->object_id = 0ull;
      this->model_id = 0;
      this->object_type = 0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _object_id_type =
    uint64_t;
  _object_id_type object_id;
  using _model_id_type =
    uint8_t;
  _model_id_type model_id;
  using _pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _pose_type pose;
  using _velocity_type =
    geometry_msgs::msg::Twist_<ContainerAllocator>;
  _velocity_type velocity;
  using _size_type =
    geometry_msgs::msg::Vector3_<ContainerAllocator>;
  _size_type size;
  using _object_type_type =
    uint8_t;
  _object_type_type object_type;
  using _track_history_type =
    std::vector<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>>>;
  _track_history_type track_history;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__object_id(
    const uint64_t & _arg)
  {
    this->object_id = _arg;
    return *this;
  }
  Type & set__model_id(
    const uint8_t & _arg)
  {
    this->model_id = _arg;
    return *this;
  }
  Type & set__pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }
  Type & set__velocity(
    const geometry_msgs::msg::Twist_<ContainerAllocator> & _arg)
  {
    this->velocity = _arg;
    return *this;
  }
  Type & set__size(
    const geometry_msgs::msg::Vector3_<ContainerAllocator> & _arg)
  {
    this->size = _arg;
    return *this;
  }
  Type & set__object_type(
    const uint8_t & _arg)
  {
    this->object_type = _arg;
    return *this;
  }
  Type & set__track_history(
    const std::vector<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::ObjectState_<ContainerAllocator>>> & _arg)
  {
    this->track_history = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t OBJECT_TYPE_UNKNOWN =
    0u;
  static constexpr uint8_t OBJECT_TYPE_VEHICLE =
    1u;
  static constexpr uint8_t OBJECT_TYPE_PEDESTRIAN =
    2u;
  static constexpr uint8_t OBJECT_TYPE_CYCLIST =
    3u;

  // pointer types
  using RawPtr =
    mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator> *;
  using ConstRawPtr =
    const mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mtr_prediction_msgs__msg__TrackedObject
    std::shared_ptr<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mtr_prediction_msgs__msg__TrackedObject
    std::shared_ptr<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TrackedObject_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->object_id != other.object_id) {
      return false;
    }
    if (this->model_id != other.model_id) {
      return false;
    }
    if (this->pose != other.pose) {
      return false;
    }
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->size != other.size) {
      return false;
    }
    if (this->object_type != other.object_type) {
      return false;
    }
    if (this->track_history != other.track_history) {
      return false;
    }
    return true;
  }
  bool operator!=(const TrackedObject_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TrackedObject_

// alias to use template instance with default allocator
using TrackedObject =
  mtr_prediction_msgs::msg::TrackedObject_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t TrackedObject_<ContainerAllocator>::OBJECT_TYPE_UNKNOWN;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t TrackedObject_<ContainerAllocator>::OBJECT_TYPE_VEHICLE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t TrackedObject_<ContainerAllocator>::OBJECT_TYPE_PEDESTRIAN;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t TrackedObject_<ContainerAllocator>::OBJECT_TYPE_CYCLIST;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT__STRUCT_HPP_

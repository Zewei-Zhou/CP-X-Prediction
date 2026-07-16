// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectReferencePoint.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__STRUCT_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'translation_to_geometric_center'
#include "geometry_msgs/msg/detail/vector3__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__mtr_prediction_msgs__msg__ObjectReferencePoint __attribute__((deprecated))
#else
# define DEPRECATED__mtr_prediction_msgs__msg__ObjectReferencePoint __declspec(deprecated)
#endif

namespace mtr_prediction_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ObjectReferencePoint_
{
  using Type = ObjectReferencePoint_<ContainerAllocator>;

  explicit ObjectReferencePoint_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : translation_to_geometric_center(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->value = 0;
    }
  }

  explicit ObjectReferencePoint_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : translation_to_geometric_center(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->value = 0;
    }
  }

  // field types and members
  using _value_type =
    uint8_t;
  _value_type value;
  using _translation_to_geometric_center_type =
    geometry_msgs::msg::Vector3_<ContainerAllocator>;
  _translation_to_geometric_center_type translation_to_geometric_center;

  // setters for named parameter idiom
  Type & set__value(
    const uint8_t & _arg)
  {
    this->value = _arg;
    return *this;
  }
  Type & set__translation_to_geometric_center(
    const geometry_msgs::msg::Vector3_<ContainerAllocator> & _arg)
  {
    this->translation_to_geometric_center = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t GEOMETRIC_CENTER =
    0u;
  static constexpr uint8_t BACK =
    1u;
  static constexpr uint8_t BACK_LEFT =
    2u;
  static constexpr uint8_t LEFT =
    3u;
  static constexpr uint8_t FRONT_LEFT =
    4u;
  static constexpr uint8_t FRONT =
    5u;
  static constexpr uint8_t FRONT_RIGHT =
    6u;
  static constexpr uint8_t RIGHT =
    7u;
  static constexpr uint8_t BACK_RIGHT =
    8u;
  static constexpr uint8_t GRAVITY_CENTER =
    10u;
  static constexpr uint8_t REAR_AXLE_GROUND =
    11u;
  static constexpr uint8_t UNKNOWN =
    100u;
  static constexpr uint8_t UNKNOWN_EDGE =
    101u;
  static constexpr uint8_t UNKNOWN_CORNER =
    102u;

  // pointer types
  using RawPtr =
    mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator> *;
  using ConstRawPtr =
    const mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mtr_prediction_msgs__msg__ObjectReferencePoint
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mtr_prediction_msgs__msg__ObjectReferencePoint
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectReferencePoint_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ObjectReferencePoint_ & other) const
  {
    if (this->value != other.value) {
      return false;
    }
    if (this->translation_to_geometric_center != other.translation_to_geometric_center) {
      return false;
    }
    return true;
  }
  bool operator!=(const ObjectReferencePoint_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ObjectReferencePoint_

// alias to use template instance with default allocator
using ObjectReferencePoint =
  mtr_prediction_msgs::msg::ObjectReferencePoint_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::GEOMETRIC_CENTER;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::BACK;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::BACK_LEFT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::LEFT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::FRONT_LEFT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::FRONT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::FRONT_RIGHT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::RIGHT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::BACK_RIGHT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::GRAVITY_CENTER;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::REAR_AXLE_GROUND;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::UNKNOWN;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::UNKNOWN_EDGE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectReferencePoint_<ContainerAllocator>::UNKNOWN_CORNER;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_REFERENCE_POINT__STRUCT_HPP_

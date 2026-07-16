// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mtr_prediction_msgs:msg/ObjectClassification.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_CLASSIFICATION__STRUCT_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_CLASSIFICATION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__mtr_prediction_msgs__msg__ObjectClassification __attribute__((deprecated))
#else
# define DEPRECATED__mtr_prediction_msgs__msg__ObjectClassification __declspec(deprecated)
#endif

namespace mtr_prediction_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ObjectClassification_
{
  using Type = ObjectClassification_<ContainerAllocator>;

  explicit ObjectClassification_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->type = 0;
      this->probability = 0.0;
    }
  }

  explicit ObjectClassification_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->type = 0;
      this->probability = 0.0;
    }
  }

  // field types and members
  using _type_type =
    uint8_t;
  _type_type type;
  using _probability_type =
    double;
  _probability_type probability;

  // setters for named parameter idiom
  Type & set__type(
    const uint8_t & _arg)
  {
    this->type = _arg;
    return *this;
  }
  Type & set__probability(
    const double & _arg)
  {
    this->probability = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t UNCLASSIFIED =
    0u;
  static constexpr uint8_t PEDESTRIAN =
    1u;
  static constexpr uint8_t BICYCLE =
    2u;
  static constexpr uint8_t MOTORBIKE =
    3u;
  static constexpr uint8_t MOTORCYCLE =
    3u;
  static constexpr uint8_t CAR =
    4u;
  static constexpr uint8_t TRUCK =
    5u;
  static constexpr uint8_t UTILITY =
    5u;
  static constexpr uint8_t VAN =
    6u;
  static constexpr uint8_t BUS =
    7u;
  static constexpr uint8_t ANIMAL =
    8u;
  static constexpr uint8_t ROAD_OBSTACLE =
    9u;
  static constexpr uint8_t TRAIN =
    10u;
  static constexpr uint8_t TRAILER =
    11u;
  static constexpr uint8_t VRU =
    12u;
  static constexpr uint8_t MICRO =
    13u;
  static constexpr uint8_t CAR_UNION =
    50u;
  static constexpr uint8_t TRUCK_UNION =
    51u;
  static constexpr uint8_t BIKE_UNION =
    52u;
  static constexpr uint8_t UNKNOWN =
    100u;

  // pointer types
  using RawPtr =
    mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator> *;
  using ConstRawPtr =
    const mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mtr_prediction_msgs__msg__ObjectClassification
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mtr_prediction_msgs__msg__ObjectClassification
    std::shared_ptr<mtr_prediction_msgs::msg::ObjectClassification_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ObjectClassification_ & other) const
  {
    if (this->type != other.type) {
      return false;
    }
    if (this->probability != other.probability) {
      return false;
    }
    return true;
  }
  bool operator!=(const ObjectClassification_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ObjectClassification_

// alias to use template instance with default allocator
using ObjectClassification =
  mtr_prediction_msgs::msg::ObjectClassification_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::UNCLASSIFIED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::PEDESTRIAN;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::BICYCLE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::MOTORBIKE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::MOTORCYCLE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::CAR;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::TRUCK;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::UTILITY;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::VAN;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::BUS;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::ANIMAL;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::ROAD_OBSTACLE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::TRAIN;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::TRAILER;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::VRU;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::MICRO;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::CAR_UNION;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::TRUCK_UNION;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::BIKE_UNION;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObjectClassification_<ContainerAllocator>::UNKNOWN;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__OBJECT_CLASSIFICATION__STRUCT_HPP_

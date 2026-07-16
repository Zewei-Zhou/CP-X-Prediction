// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mtr_prediction_msgs:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__STRUCT_HPP_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__STRUCT_HPP_

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
// Member 'objects'
#include "mtr_prediction_msgs/msg/detail/tracked_object__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__mtr_prediction_msgs__msg__TrackedObjectArray __attribute__((deprecated))
#else
# define DEPRECATED__mtr_prediction_msgs__msg__TrackedObjectArray __declspec(deprecated)
#endif

namespace mtr_prediction_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TrackedObjectArray_
{
  using Type = TrackedObjectArray_<ContainerAllocator>;

  explicit TrackedObjectArray_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    (void)_init;
  }

  explicit TrackedObjectArray_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _objects_type =
    std::vector<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator>>>;
  _objects_type objects;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__objects(
    const std::vector<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<mtr_prediction_msgs::msg::TrackedObject_<ContainerAllocator>>> & _arg)
  {
    this->objects = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator> *;
  using ConstRawPtr =
    const mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mtr_prediction_msgs__msg__TrackedObjectArray
    std::shared_ptr<mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mtr_prediction_msgs__msg__TrackedObjectArray
    std::shared_ptr<mtr_prediction_msgs::msg::TrackedObjectArray_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TrackedObjectArray_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->objects != other.objects) {
      return false;
    }
    return true;
  }
  bool operator!=(const TrackedObjectArray_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TrackedObjectArray_

// alias to use template instance with default allocator
using TrackedObjectArray =
  mtr_prediction_msgs::msg::TrackedObjectArray_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace mtr_prediction_msgs

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__STRUCT_HPP_

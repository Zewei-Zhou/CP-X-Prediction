// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from mtr_prediction_msgs:msg/ObjectPrediction.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/object_prediction__rosidl_typesupport_fastrtps_cpp.hpp"
#include "mtr_prediction_msgs/msg/detail/object_prediction__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions
namespace mtr_prediction_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const mtr_prediction_msgs::msg::PredictedTrajectory &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  mtr_prediction_msgs::msg::PredictedTrajectory &);
size_t get_serialized_size(
  const mtr_prediction_msgs::msg::PredictedTrajectory &,
  size_t current_alignment);
size_t
max_serialized_size_PredictedTrajectory(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace mtr_prediction_msgs


namespace mtr_prediction_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mtr_prediction_msgs
cdr_serialize(
  const mtr_prediction_msgs::msg::ObjectPrediction & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: object_id
  cdr << ros_message.object_id;
  // Member: object_type
  cdr << ros_message.object_type;
  // Member: trajectories
  {
    size_t size = ros_message.trajectories.size();
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; i++) {
      mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
        ros_message.trajectories[i],
        cdr);
    }
  }
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mtr_prediction_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  mtr_prediction_msgs::msg::ObjectPrediction & ros_message)
{
  // Member: object_id
  cdr >> ros_message.object_id;

  // Member: object_type
  cdr >> ros_message.object_type;

  // Member: trajectories
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);

    // Check there are at least 'size' remaining bytes in the CDR stream before resizing
    auto old_state = cdr.getState();
    bool correct_size = cdr.jump(size);
    cdr.setState(old_state);
    if (!correct_size) {
      fprintf(stderr, "sequence size exceeds remaining buffer\n");
      return false;
    }

    ros_message.trajectories.resize(size);
    for (size_t i = 0; i < size; i++) {
      mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
        cdr, ros_message.trajectories[i]);
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mtr_prediction_msgs
get_serialized_size(
  const mtr_prediction_msgs::msg::ObjectPrediction & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: object_id
  {
    size_t item_size = sizeof(ros_message.object_id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: object_type
  {
    size_t item_size = sizeof(ros_message.object_type);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: trajectories
  {
    size_t array_size = ros_message.trajectories.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    for (size_t index = 0; index < array_size; ++index) {
      current_alignment +=
        mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
        ros_message.trajectories[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mtr_prediction_msgs
max_serialized_size_ObjectPrediction(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: object_id
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: object_type
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: trajectories
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_PredictedTrajectory(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = mtr_prediction_msgs::msg::ObjectPrediction;
    is_plain =
      (
      offsetof(DataType, trajectories) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _ObjectPrediction__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const mtr_prediction_msgs::msg::ObjectPrediction *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _ObjectPrediction__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<mtr_prediction_msgs::msg::ObjectPrediction *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _ObjectPrediction__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const mtr_prediction_msgs::msg::ObjectPrediction *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _ObjectPrediction__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_ObjectPrediction(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _ObjectPrediction__callbacks = {
  "mtr_prediction_msgs::msg",
  "ObjectPrediction",
  _ObjectPrediction__cdr_serialize,
  _ObjectPrediction__cdr_deserialize,
  _ObjectPrediction__get_serialized_size,
  _ObjectPrediction__max_serialized_size
};

static rosidl_message_type_support_t _ObjectPrediction__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_ObjectPrediction__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace mtr_prediction_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_mtr_prediction_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<mtr_prediction_msgs::msg::ObjectPrediction>()
{
  return &mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::_ObjectPrediction__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, mtr_prediction_msgs, msg, ObjectPrediction)() {
  return &mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::_ObjectPrediction__handle;
}

#ifdef __cplusplus
}
#endif

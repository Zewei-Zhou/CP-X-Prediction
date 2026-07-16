// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from mtr_prediction_msgs:msg/ObjectPrediction.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/object_prediction__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "mtr_prediction_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "mtr_prediction_msgs/msg/detail/object_prediction__struct.h"
#include "mtr_prediction_msgs/msg/detail/object_prediction__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "mtr_prediction_msgs/msg/detail/predicted_trajectory__functions.h"  // trajectories

// forward declare type support functions
size_t get_serialized_size_mtr_prediction_msgs__msg__PredictedTrajectory(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_mtr_prediction_msgs__msg__PredictedTrajectory(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, mtr_prediction_msgs, msg, PredictedTrajectory)();


using _ObjectPrediction__ros_msg_type = mtr_prediction_msgs__msg__ObjectPrediction;

static bool _ObjectPrediction__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ObjectPrediction__ros_msg_type * ros_message = static_cast<const _ObjectPrediction__ros_msg_type *>(untyped_ros_message);
  // Field name: object_id
  {
    cdr << ros_message->object_id;
  }

  // Field name: object_type
  {
    cdr << ros_message->object_type;
  }

  // Field name: trajectories
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, mtr_prediction_msgs, msg, PredictedTrajectory
      )()->data);
    size_t size = ros_message->trajectories.size;
    auto array_ptr = ros_message->trajectories.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      if (!callbacks->cdr_serialize(
          &array_ptr[i], cdr))
      {
        return false;
      }
    }
  }

  return true;
}

static bool _ObjectPrediction__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ObjectPrediction__ros_msg_type * ros_message = static_cast<_ObjectPrediction__ros_msg_type *>(untyped_ros_message);
  // Field name: object_id
  {
    cdr >> ros_message->object_id;
  }

  // Field name: object_type
  {
    cdr >> ros_message->object_type;
  }

  // Field name: trajectories
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, mtr_prediction_msgs, msg, PredictedTrajectory
      )()->data);
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

    if (ros_message->trajectories.data) {
      mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__fini(&ros_message->trajectories);
    }
    if (!mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__init(&ros_message->trajectories, size)) {
      fprintf(stderr, "failed to create array for field 'trajectories'");
      return false;
    }
    auto array_ptr = ros_message->trajectories.data;
    for (size_t i = 0; i < size; ++i) {
      if (!callbacks->cdr_deserialize(
          cdr, &array_ptr[i]))
      {
        return false;
      }
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_mtr_prediction_msgs
size_t get_serialized_size_mtr_prediction_msgs__msg__ObjectPrediction(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ObjectPrediction__ros_msg_type * ros_message = static_cast<const _ObjectPrediction__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name object_id
  {
    size_t item_size = sizeof(ros_message->object_id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name object_type
  {
    size_t item_size = sizeof(ros_message->object_type);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name trajectories
  {
    size_t array_size = ros_message->trajectories.size;
    auto array_ptr = ros_message->trajectories.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_mtr_prediction_msgs__msg__PredictedTrajectory(
        &array_ptr[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}

static uint32_t _ObjectPrediction__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_mtr_prediction_msgs__msg__ObjectPrediction(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_mtr_prediction_msgs
size_t max_serialized_size_mtr_prediction_msgs__msg__ObjectPrediction(
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

  // member: object_id
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: object_type
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: trajectories
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
      size_t inner_size;
      inner_size =
        max_serialized_size_mtr_prediction_msgs__msg__PredictedTrajectory(
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
    using DataType = mtr_prediction_msgs__msg__ObjectPrediction;
    is_plain =
      (
      offsetof(DataType, trajectories) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ObjectPrediction__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_mtr_prediction_msgs__msg__ObjectPrediction(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ObjectPrediction = {
  "mtr_prediction_msgs::msg",
  "ObjectPrediction",
  _ObjectPrediction__cdr_serialize,
  _ObjectPrediction__cdr_deserialize,
  _ObjectPrediction__get_serialized_size,
  _ObjectPrediction__max_serialized_size
};

static rosidl_message_type_support_t _ObjectPrediction__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ObjectPrediction,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, mtr_prediction_msgs, msg, ObjectPrediction)() {
  return &_ObjectPrediction__type_support;
}

#if defined(__cplusplus)
}
#endif

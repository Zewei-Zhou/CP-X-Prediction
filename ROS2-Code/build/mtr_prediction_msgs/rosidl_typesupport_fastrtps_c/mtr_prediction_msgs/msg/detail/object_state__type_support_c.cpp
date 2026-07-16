// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from mtr_prediction_msgs:msg/ObjectState.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/object_state__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "mtr_prediction_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "mtr_prediction_msgs/msg/detail/object_state__struct.h"
#include "mtr_prediction_msgs/msg/detail/object_state__functions.h"
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

#include "mtr_prediction_msgs/msg/detail/object_classification__functions.h"  // classifications
#include "mtr_prediction_msgs/msg/detail/object_reference_point__functions.h"  // reference_point
#include "rosidl_runtime_c/primitives_sequence.h"  // continuous_state, continuous_state_covariance, discrete_state, sensor_id
#include "rosidl_runtime_c/primitives_sequence_functions.h"  // continuous_state, continuous_state_covariance, discrete_state, sensor_id
#include "std_msgs/msg/detail/header__functions.h"  // header

// forward declare type support functions
size_t get_serialized_size_mtr_prediction_msgs__msg__ObjectClassification(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_mtr_prediction_msgs__msg__ObjectClassification(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, mtr_prediction_msgs, msg, ObjectClassification)();
size_t get_serialized_size_mtr_prediction_msgs__msg__ObjectReferencePoint(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_mtr_prediction_msgs__msg__ObjectReferencePoint(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, mtr_prediction_msgs, msg, ObjectReferencePoint)();
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_mtr_prediction_msgs
size_t get_serialized_size_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_mtr_prediction_msgs
size_t max_serialized_size_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_mtr_prediction_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, std_msgs, msg, Header)();


using _ObjectState__ros_msg_type = mtr_prediction_msgs__msg__ObjectState;

static bool _ObjectState__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ObjectState__ros_msg_type * ros_message = static_cast<const _ObjectState__ros_msg_type *>(untyped_ros_message);
  // Field name: header
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, std_msgs, msg, Header
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->header, cdr))
    {
      return false;
    }
  }

  // Field name: model_id
  {
    cdr << ros_message->model_id;
  }

  // Field name: sensor_id
  {
    size_t size = ros_message->sensor_id.size;
    auto array_ptr = ros_message->sensor_id.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: continuous_state
  {
    size_t size = ros_message->continuous_state.size;
    auto array_ptr = ros_message->continuous_state.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: discrete_state
  {
    size_t size = ros_message->discrete_state.size;
    auto array_ptr = ros_message->discrete_state.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: continuous_state_covariance
  {
    size_t size = ros_message->continuous_state_covariance.size;
    auto array_ptr = ros_message->continuous_state_covariance.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: classifications
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, mtr_prediction_msgs, msg, ObjectClassification
      )()->data);
    size_t size = ros_message->classifications.size;
    auto array_ptr = ros_message->classifications.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      if (!callbacks->cdr_serialize(
          &array_ptr[i], cdr))
      {
        return false;
      }
    }
  }

  // Field name: reference_point
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, mtr_prediction_msgs, msg, ObjectReferencePoint
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->reference_point, cdr))
    {
      return false;
    }
  }

  return true;
}

static bool _ObjectState__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ObjectState__ros_msg_type * ros_message = static_cast<_ObjectState__ros_msg_type *>(untyped_ros_message);
  // Field name: header
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, std_msgs, msg, Header
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->header))
    {
      return false;
    }
  }

  // Field name: model_id
  {
    cdr >> ros_message->model_id;
  }

  // Field name: sensor_id
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

    if (ros_message->sensor_id.data) {
      rosidl_runtime_c__uint64__Sequence__fini(&ros_message->sensor_id);
    }
    if (!rosidl_runtime_c__uint64__Sequence__init(&ros_message->sensor_id, size)) {
      fprintf(stderr, "failed to create array for field 'sensor_id'");
      return false;
    }
    auto array_ptr = ros_message->sensor_id.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: continuous_state
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

    if (ros_message->continuous_state.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->continuous_state);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->continuous_state, size)) {
      fprintf(stderr, "failed to create array for field 'continuous_state'");
      return false;
    }
    auto array_ptr = ros_message->continuous_state.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: discrete_state
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

    if (ros_message->discrete_state.data) {
      rosidl_runtime_c__int64__Sequence__fini(&ros_message->discrete_state);
    }
    if (!rosidl_runtime_c__int64__Sequence__init(&ros_message->discrete_state, size)) {
      fprintf(stderr, "failed to create array for field 'discrete_state'");
      return false;
    }
    auto array_ptr = ros_message->discrete_state.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: continuous_state_covariance
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

    if (ros_message->continuous_state_covariance.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->continuous_state_covariance);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->continuous_state_covariance, size)) {
      fprintf(stderr, "failed to create array for field 'continuous_state_covariance'");
      return false;
    }
    auto array_ptr = ros_message->continuous_state_covariance.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: classifications
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, mtr_prediction_msgs, msg, ObjectClassification
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

    if (ros_message->classifications.data) {
      mtr_prediction_msgs__msg__ObjectClassification__Sequence__fini(&ros_message->classifications);
    }
    if (!mtr_prediction_msgs__msg__ObjectClassification__Sequence__init(&ros_message->classifications, size)) {
      fprintf(stderr, "failed to create array for field 'classifications'");
      return false;
    }
    auto array_ptr = ros_message->classifications.data;
    for (size_t i = 0; i < size; ++i) {
      if (!callbacks->cdr_deserialize(
          cdr, &array_ptr[i]))
      {
        return false;
      }
    }
  }

  // Field name: reference_point
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, mtr_prediction_msgs, msg, ObjectReferencePoint
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->reference_point))
    {
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_mtr_prediction_msgs
size_t get_serialized_size_mtr_prediction_msgs__msg__ObjectState(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ObjectState__ros_msg_type * ros_message = static_cast<const _ObjectState__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name header

  current_alignment += get_serialized_size_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);
  // field.name model_id
  {
    size_t item_size = sizeof(ros_message->model_id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name sensor_id
  {
    size_t array_size = ros_message->sensor_id.size;
    auto array_ptr = ros_message->sensor_id.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name continuous_state
  {
    size_t array_size = ros_message->continuous_state.size;
    auto array_ptr = ros_message->continuous_state.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name discrete_state
  {
    size_t array_size = ros_message->discrete_state.size;
    auto array_ptr = ros_message->discrete_state.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name continuous_state_covariance
  {
    size_t array_size = ros_message->continuous_state_covariance.size;
    auto array_ptr = ros_message->continuous_state_covariance.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name classifications
  {
    size_t array_size = ros_message->classifications.size;
    auto array_ptr = ros_message->classifications.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_mtr_prediction_msgs__msg__ObjectClassification(
        &array_ptr[index], current_alignment);
    }
  }
  // field.name reference_point

  current_alignment += get_serialized_size_mtr_prediction_msgs__msg__ObjectReferencePoint(
    &(ros_message->reference_point), current_alignment);

  return current_alignment - initial_alignment;
}

static uint32_t _ObjectState__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_mtr_prediction_msgs__msg__ObjectState(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_mtr_prediction_msgs
size_t max_serialized_size_mtr_prediction_msgs__msg__ObjectState(
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

  // member: header
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_std_msgs__msg__Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: model_id
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: sensor_id
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: continuous_state
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: discrete_state
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: continuous_state_covariance
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: classifications
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
        max_serialized_size_mtr_prediction_msgs__msg__ObjectClassification(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: reference_point
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_mtr_prediction_msgs__msg__ObjectReferencePoint(
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
    using DataType = mtr_prediction_msgs__msg__ObjectState;
    is_plain =
      (
      offsetof(DataType, reference_point) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ObjectState__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_mtr_prediction_msgs__msg__ObjectState(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ObjectState = {
  "mtr_prediction_msgs::msg",
  "ObjectState",
  _ObjectState__cdr_serialize,
  _ObjectState__cdr_deserialize,
  _ObjectState__get_serialized_size,
  _ObjectState__max_serialized_size
};

static rosidl_message_type_support_t _ObjectState__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ObjectState,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, mtr_prediction_msgs, msg, ObjectState)() {
  return &_ObjectState__type_support;
}

#if defined(__cplusplus)
}
#endif

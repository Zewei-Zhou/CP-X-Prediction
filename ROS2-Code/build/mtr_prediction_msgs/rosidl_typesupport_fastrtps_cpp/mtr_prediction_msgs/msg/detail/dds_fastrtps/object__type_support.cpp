// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from mtr_prediction_msgs:msg/Object.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/object__rosidl_typesupport_fastrtps_cpp.hpp"
#include "mtr_prediction_msgs/msg/detail/object__struct.hpp"

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
  const mtr_prediction_msgs::msg::ObjectState &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  mtr_prediction_msgs::msg::ObjectState &);
size_t get_serialized_size(
  const mtr_prediction_msgs::msg::ObjectState &,
  size_t current_alignment);
size_t
max_serialized_size_ObjectState(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace mtr_prediction_msgs

// functions for mtr_prediction_msgs::msg::ObjectState already declared above

namespace mtr_prediction_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const mtr_prediction_msgs::msg::ObjectStatePrediction &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  mtr_prediction_msgs::msg::ObjectStatePrediction &);
size_t get_serialized_size(
  const mtr_prediction_msgs::msg::ObjectStatePrediction &,
  size_t current_alignment);
size_t
max_serialized_size_ObjectStatePrediction(
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
  const mtr_prediction_msgs::msg::Object & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: id
  cdr << ros_message.id;
  // Member: existence_probability
  cdr << ros_message.existence_probability;
  // Member: state
  mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.state,
    cdr);
  // Member: state_history
  {
    size_t size = ros_message.state_history.size();
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; i++) {
      mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
        ros_message.state_history[i],
        cdr);
    }
  }
  // Member: state_predictions
  {
    size_t size = ros_message.state_predictions.size();
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; i++) {
      mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
        ros_message.state_predictions[i],
        cdr);
    }
  }
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mtr_prediction_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  mtr_prediction_msgs::msg::Object & ros_message)
{
  // Member: id
  cdr >> ros_message.id;

  // Member: existence_probability
  cdr >> ros_message.existence_probability;

  // Member: state
  mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.state);

  // Member: state_history
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

    ros_message.state_history.resize(size);
    for (size_t i = 0; i < size; i++) {
      mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
        cdr, ros_message.state_history[i]);
    }
  }

  // Member: state_predictions
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

    ros_message.state_predictions.resize(size);
    for (size_t i = 0; i < size; i++) {
      mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
        cdr, ros_message.state_predictions[i]);
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mtr_prediction_msgs
get_serialized_size(
  const mtr_prediction_msgs::msg::Object & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: id
  {
    size_t item_size = sizeof(ros_message.id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: existence_probability
  {
    size_t item_size = sizeof(ros_message.existence_probability);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: state

  current_alignment +=
    mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.state, current_alignment);
  // Member: state_history
  {
    size_t array_size = ros_message.state_history.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    for (size_t index = 0; index < array_size; ++index) {
      current_alignment +=
        mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
        ros_message.state_history[index], current_alignment);
    }
  }
  // Member: state_predictions
  {
    size_t array_size = ros_message.state_predictions.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    for (size_t index = 0; index < array_size; ++index) {
      current_alignment +=
        mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
        ros_message.state_predictions[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mtr_prediction_msgs
max_serialized_size_Object(
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


  // Member: id
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: existence_probability
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: state
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_ObjectState(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: state_history
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
        mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_ObjectState(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: state_predictions
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
        mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_ObjectStatePrediction(
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
    using DataType = mtr_prediction_msgs::msg::Object;
    is_plain =
      (
      offsetof(DataType, state_predictions) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _Object__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const mtr_prediction_msgs::msg::Object *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Object__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<mtr_prediction_msgs::msg::Object *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Object__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const mtr_prediction_msgs::msg::Object *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Object__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_Object(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _Object__callbacks = {
  "mtr_prediction_msgs::msg",
  "Object",
  _Object__cdr_serialize,
  _Object__cdr_deserialize,
  _Object__get_serialized_size,
  _Object__max_serialized_size
};

static rosidl_message_type_support_t _Object__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Object__callbacks,
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
get_message_type_support_handle<mtr_prediction_msgs::msg::Object>()
{
  return &mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::_Object__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, mtr_prediction_msgs, msg, Object)() {
  return &mtr_prediction_msgs::msg::typesupport_fastrtps_cpp::_Object__handle;
}

#ifdef __cplusplus
}
#endif

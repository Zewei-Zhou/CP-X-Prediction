// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from mtr_prediction_msgs:msg/ObjectState.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/object_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `sensor_id`
// Member `continuous_state`
// Member `discrete_state`
// Member `continuous_state_covariance`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `classifications`
#include "mtr_prediction_msgs/msg/detail/object_classification__functions.h"
// Member `reference_point`
#include "mtr_prediction_msgs/msg/detail/object_reference_point__functions.h"

bool
mtr_prediction_msgs__msg__ObjectState__init(mtr_prediction_msgs__msg__ObjectState * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    mtr_prediction_msgs__msg__ObjectState__fini(msg);
    return false;
  }
  // model_id
  // sensor_id
  if (!rosidl_runtime_c__uint64__Sequence__init(&msg->sensor_id, 0)) {
    mtr_prediction_msgs__msg__ObjectState__fini(msg);
    return false;
  }
  // continuous_state
  if (!rosidl_runtime_c__double__Sequence__init(&msg->continuous_state, 0)) {
    mtr_prediction_msgs__msg__ObjectState__fini(msg);
    return false;
  }
  // discrete_state
  if (!rosidl_runtime_c__int64__Sequence__init(&msg->discrete_state, 0)) {
    mtr_prediction_msgs__msg__ObjectState__fini(msg);
    return false;
  }
  // continuous_state_covariance
  if (!rosidl_runtime_c__double__Sequence__init(&msg->continuous_state_covariance, 0)) {
    mtr_prediction_msgs__msg__ObjectState__fini(msg);
    return false;
  }
  // classifications
  if (!mtr_prediction_msgs__msg__ObjectClassification__Sequence__init(&msg->classifications, 0)) {
    mtr_prediction_msgs__msg__ObjectState__fini(msg);
    return false;
  }
  // reference_point
  if (!mtr_prediction_msgs__msg__ObjectReferencePoint__init(&msg->reference_point)) {
    mtr_prediction_msgs__msg__ObjectState__fini(msg);
    return false;
  }
  return true;
}

void
mtr_prediction_msgs__msg__ObjectState__fini(mtr_prediction_msgs__msg__ObjectState * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // model_id
  // sensor_id
  rosidl_runtime_c__uint64__Sequence__fini(&msg->sensor_id);
  // continuous_state
  rosidl_runtime_c__double__Sequence__fini(&msg->continuous_state);
  // discrete_state
  rosidl_runtime_c__int64__Sequence__fini(&msg->discrete_state);
  // continuous_state_covariance
  rosidl_runtime_c__double__Sequence__fini(&msg->continuous_state_covariance);
  // classifications
  mtr_prediction_msgs__msg__ObjectClassification__Sequence__fini(&msg->classifications);
  // reference_point
  mtr_prediction_msgs__msg__ObjectReferencePoint__fini(&msg->reference_point);
}

bool
mtr_prediction_msgs__msg__ObjectState__are_equal(const mtr_prediction_msgs__msg__ObjectState * lhs, const mtr_prediction_msgs__msg__ObjectState * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // model_id
  if (lhs->model_id != rhs->model_id) {
    return false;
  }
  // sensor_id
  if (!rosidl_runtime_c__uint64__Sequence__are_equal(
      &(lhs->sensor_id), &(rhs->sensor_id)))
  {
    return false;
  }
  // continuous_state
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->continuous_state), &(rhs->continuous_state)))
  {
    return false;
  }
  // discrete_state
  if (!rosidl_runtime_c__int64__Sequence__are_equal(
      &(lhs->discrete_state), &(rhs->discrete_state)))
  {
    return false;
  }
  // continuous_state_covariance
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->continuous_state_covariance), &(rhs->continuous_state_covariance)))
  {
    return false;
  }
  // classifications
  if (!mtr_prediction_msgs__msg__ObjectClassification__Sequence__are_equal(
      &(lhs->classifications), &(rhs->classifications)))
  {
    return false;
  }
  // reference_point
  if (!mtr_prediction_msgs__msg__ObjectReferencePoint__are_equal(
      &(lhs->reference_point), &(rhs->reference_point)))
  {
    return false;
  }
  return true;
}

bool
mtr_prediction_msgs__msg__ObjectState__copy(
  const mtr_prediction_msgs__msg__ObjectState * input,
  mtr_prediction_msgs__msg__ObjectState * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // model_id
  output->model_id = input->model_id;
  // sensor_id
  if (!rosidl_runtime_c__uint64__Sequence__copy(
      &(input->sensor_id), &(output->sensor_id)))
  {
    return false;
  }
  // continuous_state
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->continuous_state), &(output->continuous_state)))
  {
    return false;
  }
  // discrete_state
  if (!rosidl_runtime_c__int64__Sequence__copy(
      &(input->discrete_state), &(output->discrete_state)))
  {
    return false;
  }
  // continuous_state_covariance
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->continuous_state_covariance), &(output->continuous_state_covariance)))
  {
    return false;
  }
  // classifications
  if (!mtr_prediction_msgs__msg__ObjectClassification__Sequence__copy(
      &(input->classifications), &(output->classifications)))
  {
    return false;
  }
  // reference_point
  if (!mtr_prediction_msgs__msg__ObjectReferencePoint__copy(
      &(input->reference_point), &(output->reference_point)))
  {
    return false;
  }
  return true;
}

mtr_prediction_msgs__msg__ObjectState *
mtr_prediction_msgs__msg__ObjectState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectState * msg = (mtr_prediction_msgs__msg__ObjectState *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__ObjectState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(mtr_prediction_msgs__msg__ObjectState));
  bool success = mtr_prediction_msgs__msg__ObjectState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
mtr_prediction_msgs__msg__ObjectState__destroy(mtr_prediction_msgs__msg__ObjectState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    mtr_prediction_msgs__msg__ObjectState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
mtr_prediction_msgs__msg__ObjectState__Sequence__init(mtr_prediction_msgs__msg__ObjectState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectState * data = NULL;

  if (size) {
    data = (mtr_prediction_msgs__msg__ObjectState *)allocator.zero_allocate(size, sizeof(mtr_prediction_msgs__msg__ObjectState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = mtr_prediction_msgs__msg__ObjectState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        mtr_prediction_msgs__msg__ObjectState__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
mtr_prediction_msgs__msg__ObjectState__Sequence__fini(mtr_prediction_msgs__msg__ObjectState__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      mtr_prediction_msgs__msg__ObjectState__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

mtr_prediction_msgs__msg__ObjectState__Sequence *
mtr_prediction_msgs__msg__ObjectState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectState__Sequence * array = (mtr_prediction_msgs__msg__ObjectState__Sequence *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__ObjectState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = mtr_prediction_msgs__msg__ObjectState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
mtr_prediction_msgs__msg__ObjectState__Sequence__destroy(mtr_prediction_msgs__msg__ObjectState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    mtr_prediction_msgs__msg__ObjectState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
mtr_prediction_msgs__msg__ObjectState__Sequence__are_equal(const mtr_prediction_msgs__msg__ObjectState__Sequence * lhs, const mtr_prediction_msgs__msg__ObjectState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!mtr_prediction_msgs__msg__ObjectState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
mtr_prediction_msgs__msg__ObjectState__Sequence__copy(
  const mtr_prediction_msgs__msg__ObjectState__Sequence * input,
  mtr_prediction_msgs__msg__ObjectState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(mtr_prediction_msgs__msg__ObjectState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    mtr_prediction_msgs__msg__ObjectState * data =
      (mtr_prediction_msgs__msg__ObjectState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!mtr_prediction_msgs__msg__ObjectState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          mtr_prediction_msgs__msg__ObjectState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!mtr_prediction_msgs__msg__ObjectState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

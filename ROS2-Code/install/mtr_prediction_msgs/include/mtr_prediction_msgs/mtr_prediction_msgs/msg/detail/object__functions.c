// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from mtr_prediction_msgs:msg/Object.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/object__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `state`
// Member `state_history`
#include "mtr_prediction_msgs/msg/detail/object_state__functions.h"
// Member `state_predictions`
#include "mtr_prediction_msgs/msg/detail/object_state_prediction__functions.h"

bool
mtr_prediction_msgs__msg__Object__init(mtr_prediction_msgs__msg__Object * msg)
{
  if (!msg) {
    return false;
  }
  // id
  // existence_probability
  // state
  if (!mtr_prediction_msgs__msg__ObjectState__init(&msg->state)) {
    mtr_prediction_msgs__msg__Object__fini(msg);
    return false;
  }
  // state_history
  if (!mtr_prediction_msgs__msg__ObjectState__Sequence__init(&msg->state_history, 0)) {
    mtr_prediction_msgs__msg__Object__fini(msg);
    return false;
  }
  // state_predictions
  if (!mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__init(&msg->state_predictions, 0)) {
    mtr_prediction_msgs__msg__Object__fini(msg);
    return false;
  }
  return true;
}

void
mtr_prediction_msgs__msg__Object__fini(mtr_prediction_msgs__msg__Object * msg)
{
  if (!msg) {
    return;
  }
  // id
  // existence_probability
  // state
  mtr_prediction_msgs__msg__ObjectState__fini(&msg->state);
  // state_history
  mtr_prediction_msgs__msg__ObjectState__Sequence__fini(&msg->state_history);
  // state_predictions
  mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__fini(&msg->state_predictions);
}

bool
mtr_prediction_msgs__msg__Object__are_equal(const mtr_prediction_msgs__msg__Object * lhs, const mtr_prediction_msgs__msg__Object * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // existence_probability
  if (lhs->existence_probability != rhs->existence_probability) {
    return false;
  }
  // state
  if (!mtr_prediction_msgs__msg__ObjectState__are_equal(
      &(lhs->state), &(rhs->state)))
  {
    return false;
  }
  // state_history
  if (!mtr_prediction_msgs__msg__ObjectState__Sequence__are_equal(
      &(lhs->state_history), &(rhs->state_history)))
  {
    return false;
  }
  // state_predictions
  if (!mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__are_equal(
      &(lhs->state_predictions), &(rhs->state_predictions)))
  {
    return false;
  }
  return true;
}

bool
mtr_prediction_msgs__msg__Object__copy(
  const mtr_prediction_msgs__msg__Object * input,
  mtr_prediction_msgs__msg__Object * output)
{
  if (!input || !output) {
    return false;
  }
  // id
  output->id = input->id;
  // existence_probability
  output->existence_probability = input->existence_probability;
  // state
  if (!mtr_prediction_msgs__msg__ObjectState__copy(
      &(input->state), &(output->state)))
  {
    return false;
  }
  // state_history
  if (!mtr_prediction_msgs__msg__ObjectState__Sequence__copy(
      &(input->state_history), &(output->state_history)))
  {
    return false;
  }
  // state_predictions
  if (!mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__copy(
      &(input->state_predictions), &(output->state_predictions)))
  {
    return false;
  }
  return true;
}

mtr_prediction_msgs__msg__Object *
mtr_prediction_msgs__msg__Object__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__Object * msg = (mtr_prediction_msgs__msg__Object *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__Object), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(mtr_prediction_msgs__msg__Object));
  bool success = mtr_prediction_msgs__msg__Object__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
mtr_prediction_msgs__msg__Object__destroy(mtr_prediction_msgs__msg__Object * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    mtr_prediction_msgs__msg__Object__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
mtr_prediction_msgs__msg__Object__Sequence__init(mtr_prediction_msgs__msg__Object__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__Object * data = NULL;

  if (size) {
    data = (mtr_prediction_msgs__msg__Object *)allocator.zero_allocate(size, sizeof(mtr_prediction_msgs__msg__Object), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = mtr_prediction_msgs__msg__Object__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        mtr_prediction_msgs__msg__Object__fini(&data[i - 1]);
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
mtr_prediction_msgs__msg__Object__Sequence__fini(mtr_prediction_msgs__msg__Object__Sequence * array)
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
      mtr_prediction_msgs__msg__Object__fini(&array->data[i]);
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

mtr_prediction_msgs__msg__Object__Sequence *
mtr_prediction_msgs__msg__Object__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__Object__Sequence * array = (mtr_prediction_msgs__msg__Object__Sequence *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__Object__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = mtr_prediction_msgs__msg__Object__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
mtr_prediction_msgs__msg__Object__Sequence__destroy(mtr_prediction_msgs__msg__Object__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    mtr_prediction_msgs__msg__Object__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
mtr_prediction_msgs__msg__Object__Sequence__are_equal(const mtr_prediction_msgs__msg__Object__Sequence * lhs, const mtr_prediction_msgs__msg__Object__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!mtr_prediction_msgs__msg__Object__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
mtr_prediction_msgs__msg__Object__Sequence__copy(
  const mtr_prediction_msgs__msg__Object__Sequence * input,
  mtr_prediction_msgs__msg__Object__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(mtr_prediction_msgs__msg__Object);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    mtr_prediction_msgs__msg__Object * data =
      (mtr_prediction_msgs__msg__Object *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!mtr_prediction_msgs__msg__Object__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          mtr_prediction_msgs__msg__Object__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!mtr_prediction_msgs__msg__Object__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from mtr_prediction_msgs:msg/ObjectStatePrediction.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/object_state_prediction__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `states`
#include "mtr_prediction_msgs/msg/detail/object_state__functions.h"

bool
mtr_prediction_msgs__msg__ObjectStatePrediction__init(mtr_prediction_msgs__msg__ObjectStatePrediction * msg)
{
  if (!msg) {
    return false;
  }
  // probability
  // states
  if (!mtr_prediction_msgs__msg__ObjectState__Sequence__init(&msg->states, 0)) {
    mtr_prediction_msgs__msg__ObjectStatePrediction__fini(msg);
    return false;
  }
  return true;
}

void
mtr_prediction_msgs__msg__ObjectStatePrediction__fini(mtr_prediction_msgs__msg__ObjectStatePrediction * msg)
{
  if (!msg) {
    return;
  }
  // probability
  // states
  mtr_prediction_msgs__msg__ObjectState__Sequence__fini(&msg->states);
}

bool
mtr_prediction_msgs__msg__ObjectStatePrediction__are_equal(const mtr_prediction_msgs__msg__ObjectStatePrediction * lhs, const mtr_prediction_msgs__msg__ObjectStatePrediction * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // probability
  if (lhs->probability != rhs->probability) {
    return false;
  }
  // states
  if (!mtr_prediction_msgs__msg__ObjectState__Sequence__are_equal(
      &(lhs->states), &(rhs->states)))
  {
    return false;
  }
  return true;
}

bool
mtr_prediction_msgs__msg__ObjectStatePrediction__copy(
  const mtr_prediction_msgs__msg__ObjectStatePrediction * input,
  mtr_prediction_msgs__msg__ObjectStatePrediction * output)
{
  if (!input || !output) {
    return false;
  }
  // probability
  output->probability = input->probability;
  // states
  if (!mtr_prediction_msgs__msg__ObjectState__Sequence__copy(
      &(input->states), &(output->states)))
  {
    return false;
  }
  return true;
}

mtr_prediction_msgs__msg__ObjectStatePrediction *
mtr_prediction_msgs__msg__ObjectStatePrediction__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectStatePrediction * msg = (mtr_prediction_msgs__msg__ObjectStatePrediction *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__ObjectStatePrediction), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(mtr_prediction_msgs__msg__ObjectStatePrediction));
  bool success = mtr_prediction_msgs__msg__ObjectStatePrediction__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
mtr_prediction_msgs__msg__ObjectStatePrediction__destroy(mtr_prediction_msgs__msg__ObjectStatePrediction * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    mtr_prediction_msgs__msg__ObjectStatePrediction__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__init(mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectStatePrediction * data = NULL;

  if (size) {
    data = (mtr_prediction_msgs__msg__ObjectStatePrediction *)allocator.zero_allocate(size, sizeof(mtr_prediction_msgs__msg__ObjectStatePrediction), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = mtr_prediction_msgs__msg__ObjectStatePrediction__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        mtr_prediction_msgs__msg__ObjectStatePrediction__fini(&data[i - 1]);
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
mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__fini(mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence * array)
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
      mtr_prediction_msgs__msg__ObjectStatePrediction__fini(&array->data[i]);
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

mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence *
mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence * array = (mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__destroy(mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__are_equal(const mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence * lhs, const mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!mtr_prediction_msgs__msg__ObjectStatePrediction__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__copy(
  const mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence * input,
  mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(mtr_prediction_msgs__msg__ObjectStatePrediction);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    mtr_prediction_msgs__msg__ObjectStatePrediction * data =
      (mtr_prediction_msgs__msg__ObjectStatePrediction *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!mtr_prediction_msgs__msg__ObjectStatePrediction__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          mtr_prediction_msgs__msg__ObjectStatePrediction__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!mtr_prediction_msgs__msg__ObjectStatePrediction__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

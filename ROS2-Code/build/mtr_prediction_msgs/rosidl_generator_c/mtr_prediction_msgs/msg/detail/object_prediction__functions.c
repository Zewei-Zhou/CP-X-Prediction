// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from mtr_prediction_msgs:msg/ObjectPrediction.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/object_prediction__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `trajectories`
#include "mtr_prediction_msgs/msg/detail/predicted_trajectory__functions.h"

bool
mtr_prediction_msgs__msg__ObjectPrediction__init(mtr_prediction_msgs__msg__ObjectPrediction * msg)
{
  if (!msg) {
    return false;
  }
  // object_id
  // object_type
  // trajectories
  if (!mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__init(&msg->trajectories, 0)) {
    mtr_prediction_msgs__msg__ObjectPrediction__fini(msg);
    return false;
  }
  return true;
}

void
mtr_prediction_msgs__msg__ObjectPrediction__fini(mtr_prediction_msgs__msg__ObjectPrediction * msg)
{
  if (!msg) {
    return;
  }
  // object_id
  // object_type
  // trajectories
  mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__fini(&msg->trajectories);
}

bool
mtr_prediction_msgs__msg__ObjectPrediction__are_equal(const mtr_prediction_msgs__msg__ObjectPrediction * lhs, const mtr_prediction_msgs__msg__ObjectPrediction * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // object_id
  if (lhs->object_id != rhs->object_id) {
    return false;
  }
  // object_type
  if (lhs->object_type != rhs->object_type) {
    return false;
  }
  // trajectories
  if (!mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__are_equal(
      &(lhs->trajectories), &(rhs->trajectories)))
  {
    return false;
  }
  return true;
}

bool
mtr_prediction_msgs__msg__ObjectPrediction__copy(
  const mtr_prediction_msgs__msg__ObjectPrediction * input,
  mtr_prediction_msgs__msg__ObjectPrediction * output)
{
  if (!input || !output) {
    return false;
  }
  // object_id
  output->object_id = input->object_id;
  // object_type
  output->object_type = input->object_type;
  // trajectories
  if (!mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__copy(
      &(input->trajectories), &(output->trajectories)))
  {
    return false;
  }
  return true;
}

mtr_prediction_msgs__msg__ObjectPrediction *
mtr_prediction_msgs__msg__ObjectPrediction__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectPrediction * msg = (mtr_prediction_msgs__msg__ObjectPrediction *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__ObjectPrediction), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(mtr_prediction_msgs__msg__ObjectPrediction));
  bool success = mtr_prediction_msgs__msg__ObjectPrediction__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
mtr_prediction_msgs__msg__ObjectPrediction__destroy(mtr_prediction_msgs__msg__ObjectPrediction * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    mtr_prediction_msgs__msg__ObjectPrediction__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
mtr_prediction_msgs__msg__ObjectPrediction__Sequence__init(mtr_prediction_msgs__msg__ObjectPrediction__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectPrediction * data = NULL;

  if (size) {
    data = (mtr_prediction_msgs__msg__ObjectPrediction *)allocator.zero_allocate(size, sizeof(mtr_prediction_msgs__msg__ObjectPrediction), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = mtr_prediction_msgs__msg__ObjectPrediction__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        mtr_prediction_msgs__msg__ObjectPrediction__fini(&data[i - 1]);
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
mtr_prediction_msgs__msg__ObjectPrediction__Sequence__fini(mtr_prediction_msgs__msg__ObjectPrediction__Sequence * array)
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
      mtr_prediction_msgs__msg__ObjectPrediction__fini(&array->data[i]);
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

mtr_prediction_msgs__msg__ObjectPrediction__Sequence *
mtr_prediction_msgs__msg__ObjectPrediction__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectPrediction__Sequence * array = (mtr_prediction_msgs__msg__ObjectPrediction__Sequence *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__ObjectPrediction__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = mtr_prediction_msgs__msg__ObjectPrediction__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
mtr_prediction_msgs__msg__ObjectPrediction__Sequence__destroy(mtr_prediction_msgs__msg__ObjectPrediction__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    mtr_prediction_msgs__msg__ObjectPrediction__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
mtr_prediction_msgs__msg__ObjectPrediction__Sequence__are_equal(const mtr_prediction_msgs__msg__ObjectPrediction__Sequence * lhs, const mtr_prediction_msgs__msg__ObjectPrediction__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!mtr_prediction_msgs__msg__ObjectPrediction__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
mtr_prediction_msgs__msg__ObjectPrediction__Sequence__copy(
  const mtr_prediction_msgs__msg__ObjectPrediction__Sequence * input,
  mtr_prediction_msgs__msg__ObjectPrediction__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(mtr_prediction_msgs__msg__ObjectPrediction);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    mtr_prediction_msgs__msg__ObjectPrediction * data =
      (mtr_prediction_msgs__msg__ObjectPrediction *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!mtr_prediction_msgs__msg__ObjectPrediction__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          mtr_prediction_msgs__msg__ObjectPrediction__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!mtr_prediction_msgs__msg__ObjectPrediction__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

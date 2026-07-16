// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from mtr_prediction_msgs:msg/PredictedTrajectory.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/predicted_trajectory__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `waypoints`
#include "geometry_msgs/msg/detail/pose_stamped__functions.h"
// Member `velocities`
#include "geometry_msgs/msg/detail/twist_stamped__functions.h"

bool
mtr_prediction_msgs__msg__PredictedTrajectory__init(mtr_prediction_msgs__msg__PredictedTrajectory * msg)
{
  if (!msg) {
    return false;
  }
  // confidence
  // waypoints
  if (!geometry_msgs__msg__PoseStamped__Sequence__init(&msg->waypoints, 0)) {
    mtr_prediction_msgs__msg__PredictedTrajectory__fini(msg);
    return false;
  }
  // velocities
  if (!geometry_msgs__msg__TwistStamped__Sequence__init(&msg->velocities, 0)) {
    mtr_prediction_msgs__msg__PredictedTrajectory__fini(msg);
    return false;
  }
  return true;
}

void
mtr_prediction_msgs__msg__PredictedTrajectory__fini(mtr_prediction_msgs__msg__PredictedTrajectory * msg)
{
  if (!msg) {
    return;
  }
  // confidence
  // waypoints
  geometry_msgs__msg__PoseStamped__Sequence__fini(&msg->waypoints);
  // velocities
  geometry_msgs__msg__TwistStamped__Sequence__fini(&msg->velocities);
}

bool
mtr_prediction_msgs__msg__PredictedTrajectory__are_equal(const mtr_prediction_msgs__msg__PredictedTrajectory * lhs, const mtr_prediction_msgs__msg__PredictedTrajectory * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // waypoints
  if (!geometry_msgs__msg__PoseStamped__Sequence__are_equal(
      &(lhs->waypoints), &(rhs->waypoints)))
  {
    return false;
  }
  // velocities
  if (!geometry_msgs__msg__TwistStamped__Sequence__are_equal(
      &(lhs->velocities), &(rhs->velocities)))
  {
    return false;
  }
  return true;
}

bool
mtr_prediction_msgs__msg__PredictedTrajectory__copy(
  const mtr_prediction_msgs__msg__PredictedTrajectory * input,
  mtr_prediction_msgs__msg__PredictedTrajectory * output)
{
  if (!input || !output) {
    return false;
  }
  // confidence
  output->confidence = input->confidence;
  // waypoints
  if (!geometry_msgs__msg__PoseStamped__Sequence__copy(
      &(input->waypoints), &(output->waypoints)))
  {
    return false;
  }
  // velocities
  if (!geometry_msgs__msg__TwistStamped__Sequence__copy(
      &(input->velocities), &(output->velocities)))
  {
    return false;
  }
  return true;
}

mtr_prediction_msgs__msg__PredictedTrajectory *
mtr_prediction_msgs__msg__PredictedTrajectory__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__PredictedTrajectory * msg = (mtr_prediction_msgs__msg__PredictedTrajectory *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__PredictedTrajectory), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(mtr_prediction_msgs__msg__PredictedTrajectory));
  bool success = mtr_prediction_msgs__msg__PredictedTrajectory__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
mtr_prediction_msgs__msg__PredictedTrajectory__destroy(mtr_prediction_msgs__msg__PredictedTrajectory * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    mtr_prediction_msgs__msg__PredictedTrajectory__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__init(mtr_prediction_msgs__msg__PredictedTrajectory__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__PredictedTrajectory * data = NULL;

  if (size) {
    data = (mtr_prediction_msgs__msg__PredictedTrajectory *)allocator.zero_allocate(size, sizeof(mtr_prediction_msgs__msg__PredictedTrajectory), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = mtr_prediction_msgs__msg__PredictedTrajectory__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        mtr_prediction_msgs__msg__PredictedTrajectory__fini(&data[i - 1]);
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
mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__fini(mtr_prediction_msgs__msg__PredictedTrajectory__Sequence * array)
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
      mtr_prediction_msgs__msg__PredictedTrajectory__fini(&array->data[i]);
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

mtr_prediction_msgs__msg__PredictedTrajectory__Sequence *
mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__PredictedTrajectory__Sequence * array = (mtr_prediction_msgs__msg__PredictedTrajectory__Sequence *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__PredictedTrajectory__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__destroy(mtr_prediction_msgs__msg__PredictedTrajectory__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__are_equal(const mtr_prediction_msgs__msg__PredictedTrajectory__Sequence * lhs, const mtr_prediction_msgs__msg__PredictedTrajectory__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!mtr_prediction_msgs__msg__PredictedTrajectory__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__copy(
  const mtr_prediction_msgs__msg__PredictedTrajectory__Sequence * input,
  mtr_prediction_msgs__msg__PredictedTrajectory__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(mtr_prediction_msgs__msg__PredictedTrajectory);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    mtr_prediction_msgs__msg__PredictedTrajectory * data =
      (mtr_prediction_msgs__msg__PredictedTrajectory *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!mtr_prediction_msgs__msg__PredictedTrajectory__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          mtr_prediction_msgs__msg__PredictedTrajectory__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!mtr_prediction_msgs__msg__PredictedTrajectory__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from mtr_prediction_msgs:msg/TrackedObject.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/tracked_object__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `velocity`
#include "geometry_msgs/msg/detail/twist__functions.h"
// Member `size`
#include "geometry_msgs/msg/detail/vector3__functions.h"
// Member `track_history`
#include "mtr_prediction_msgs/msg/detail/object_state__functions.h"

bool
mtr_prediction_msgs__msg__TrackedObject__init(mtr_prediction_msgs__msg__TrackedObject * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    mtr_prediction_msgs__msg__TrackedObject__fini(msg);
    return false;
  }
  // object_id
  // model_id
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    mtr_prediction_msgs__msg__TrackedObject__fini(msg);
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Twist__init(&msg->velocity)) {
    mtr_prediction_msgs__msg__TrackedObject__fini(msg);
    return false;
  }
  // size
  if (!geometry_msgs__msg__Vector3__init(&msg->size)) {
    mtr_prediction_msgs__msg__TrackedObject__fini(msg);
    return false;
  }
  // object_type
  // track_history
  if (!mtr_prediction_msgs__msg__ObjectState__Sequence__init(&msg->track_history, 0)) {
    mtr_prediction_msgs__msg__TrackedObject__fini(msg);
    return false;
  }
  return true;
}

void
mtr_prediction_msgs__msg__TrackedObject__fini(mtr_prediction_msgs__msg__TrackedObject * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // object_id
  // model_id
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // velocity
  geometry_msgs__msg__Twist__fini(&msg->velocity);
  // size
  geometry_msgs__msg__Vector3__fini(&msg->size);
  // object_type
  // track_history
  mtr_prediction_msgs__msg__ObjectState__Sequence__fini(&msg->track_history);
}

bool
mtr_prediction_msgs__msg__TrackedObject__are_equal(const mtr_prediction_msgs__msg__TrackedObject * lhs, const mtr_prediction_msgs__msg__TrackedObject * rhs)
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
  // object_id
  if (lhs->object_id != rhs->object_id) {
    return false;
  }
  // model_id
  if (lhs->model_id != rhs->model_id) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Twist__are_equal(
      &(lhs->velocity), &(rhs->velocity)))
  {
    return false;
  }
  // size
  if (!geometry_msgs__msg__Vector3__are_equal(
      &(lhs->size), &(rhs->size)))
  {
    return false;
  }
  // object_type
  if (lhs->object_type != rhs->object_type) {
    return false;
  }
  // track_history
  if (!mtr_prediction_msgs__msg__ObjectState__Sequence__are_equal(
      &(lhs->track_history), &(rhs->track_history)))
  {
    return false;
  }
  return true;
}

bool
mtr_prediction_msgs__msg__TrackedObject__copy(
  const mtr_prediction_msgs__msg__TrackedObject * input,
  mtr_prediction_msgs__msg__TrackedObject * output)
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
  // object_id
  output->object_id = input->object_id;
  // model_id
  output->model_id = input->model_id;
  // pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Twist__copy(
      &(input->velocity), &(output->velocity)))
  {
    return false;
  }
  // size
  if (!geometry_msgs__msg__Vector3__copy(
      &(input->size), &(output->size)))
  {
    return false;
  }
  // object_type
  output->object_type = input->object_type;
  // track_history
  if (!mtr_prediction_msgs__msg__ObjectState__Sequence__copy(
      &(input->track_history), &(output->track_history)))
  {
    return false;
  }
  return true;
}

mtr_prediction_msgs__msg__TrackedObject *
mtr_prediction_msgs__msg__TrackedObject__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__TrackedObject * msg = (mtr_prediction_msgs__msg__TrackedObject *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__TrackedObject), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(mtr_prediction_msgs__msg__TrackedObject));
  bool success = mtr_prediction_msgs__msg__TrackedObject__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
mtr_prediction_msgs__msg__TrackedObject__destroy(mtr_prediction_msgs__msg__TrackedObject * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    mtr_prediction_msgs__msg__TrackedObject__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
mtr_prediction_msgs__msg__TrackedObject__Sequence__init(mtr_prediction_msgs__msg__TrackedObject__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__TrackedObject * data = NULL;

  if (size) {
    data = (mtr_prediction_msgs__msg__TrackedObject *)allocator.zero_allocate(size, sizeof(mtr_prediction_msgs__msg__TrackedObject), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = mtr_prediction_msgs__msg__TrackedObject__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        mtr_prediction_msgs__msg__TrackedObject__fini(&data[i - 1]);
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
mtr_prediction_msgs__msg__TrackedObject__Sequence__fini(mtr_prediction_msgs__msg__TrackedObject__Sequence * array)
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
      mtr_prediction_msgs__msg__TrackedObject__fini(&array->data[i]);
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

mtr_prediction_msgs__msg__TrackedObject__Sequence *
mtr_prediction_msgs__msg__TrackedObject__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__TrackedObject__Sequence * array = (mtr_prediction_msgs__msg__TrackedObject__Sequence *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__TrackedObject__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = mtr_prediction_msgs__msg__TrackedObject__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
mtr_prediction_msgs__msg__TrackedObject__Sequence__destroy(mtr_prediction_msgs__msg__TrackedObject__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    mtr_prediction_msgs__msg__TrackedObject__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
mtr_prediction_msgs__msg__TrackedObject__Sequence__are_equal(const mtr_prediction_msgs__msg__TrackedObject__Sequence * lhs, const mtr_prediction_msgs__msg__TrackedObject__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!mtr_prediction_msgs__msg__TrackedObject__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
mtr_prediction_msgs__msg__TrackedObject__Sequence__copy(
  const mtr_prediction_msgs__msg__TrackedObject__Sequence * input,
  mtr_prediction_msgs__msg__TrackedObject__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(mtr_prediction_msgs__msg__TrackedObject);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    mtr_prediction_msgs__msg__TrackedObject * data =
      (mtr_prediction_msgs__msg__TrackedObject *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!mtr_prediction_msgs__msg__TrackedObject__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          mtr_prediction_msgs__msg__TrackedObject__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!mtr_prediction_msgs__msg__TrackedObject__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

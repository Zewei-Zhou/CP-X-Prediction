// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from mtr_prediction_msgs:msg/MarkerArrayHeader.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/marker_array_header__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `markers`
#include "visualization_msgs/msg/detail/marker__functions.h"

bool
mtr_prediction_msgs__msg__MarkerArrayHeader__init(mtr_prediction_msgs__msg__MarkerArrayHeader * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    mtr_prediction_msgs__msg__MarkerArrayHeader__fini(msg);
    return false;
  }
  // markers
  if (!visualization_msgs__msg__Marker__Sequence__init(&msg->markers, 0)) {
    mtr_prediction_msgs__msg__MarkerArrayHeader__fini(msg);
    return false;
  }
  return true;
}

void
mtr_prediction_msgs__msg__MarkerArrayHeader__fini(mtr_prediction_msgs__msg__MarkerArrayHeader * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // markers
  visualization_msgs__msg__Marker__Sequence__fini(&msg->markers);
}

bool
mtr_prediction_msgs__msg__MarkerArrayHeader__are_equal(const mtr_prediction_msgs__msg__MarkerArrayHeader * lhs, const mtr_prediction_msgs__msg__MarkerArrayHeader * rhs)
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
  // markers
  if (!visualization_msgs__msg__Marker__Sequence__are_equal(
      &(lhs->markers), &(rhs->markers)))
  {
    return false;
  }
  return true;
}

bool
mtr_prediction_msgs__msg__MarkerArrayHeader__copy(
  const mtr_prediction_msgs__msg__MarkerArrayHeader * input,
  mtr_prediction_msgs__msg__MarkerArrayHeader * output)
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
  // markers
  if (!visualization_msgs__msg__Marker__Sequence__copy(
      &(input->markers), &(output->markers)))
  {
    return false;
  }
  return true;
}

mtr_prediction_msgs__msg__MarkerArrayHeader *
mtr_prediction_msgs__msg__MarkerArrayHeader__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__MarkerArrayHeader * msg = (mtr_prediction_msgs__msg__MarkerArrayHeader *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__MarkerArrayHeader), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(mtr_prediction_msgs__msg__MarkerArrayHeader));
  bool success = mtr_prediction_msgs__msg__MarkerArrayHeader__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
mtr_prediction_msgs__msg__MarkerArrayHeader__destroy(mtr_prediction_msgs__msg__MarkerArrayHeader * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    mtr_prediction_msgs__msg__MarkerArrayHeader__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__init(mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__MarkerArrayHeader * data = NULL;

  if (size) {
    data = (mtr_prediction_msgs__msg__MarkerArrayHeader *)allocator.zero_allocate(size, sizeof(mtr_prediction_msgs__msg__MarkerArrayHeader), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = mtr_prediction_msgs__msg__MarkerArrayHeader__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        mtr_prediction_msgs__msg__MarkerArrayHeader__fini(&data[i - 1]);
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
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__fini(mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * array)
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
      mtr_prediction_msgs__msg__MarkerArrayHeader__fini(&array->data[i]);
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

mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence *
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * array = (mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__destroy(mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__are_equal(const mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * lhs, const mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!mtr_prediction_msgs__msg__MarkerArrayHeader__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__copy(
  const mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * input,
  mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(mtr_prediction_msgs__msg__MarkerArrayHeader);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    mtr_prediction_msgs__msg__MarkerArrayHeader * data =
      (mtr_prediction_msgs__msg__MarkerArrayHeader *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!mtr_prediction_msgs__msg__MarkerArrayHeader__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          mtr_prediction_msgs__msg__MarkerArrayHeader__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!mtr_prediction_msgs__msg__MarkerArrayHeader__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

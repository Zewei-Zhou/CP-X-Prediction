// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from mtr_prediction_msgs:msg/ObjectReferencePoint.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/object_reference_point__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `translation_to_geometric_center`
#include "geometry_msgs/msg/detail/vector3__functions.h"

bool
mtr_prediction_msgs__msg__ObjectReferencePoint__init(mtr_prediction_msgs__msg__ObjectReferencePoint * msg)
{
  if (!msg) {
    return false;
  }
  // value
  // translation_to_geometric_center
  if (!geometry_msgs__msg__Vector3__init(&msg->translation_to_geometric_center)) {
    mtr_prediction_msgs__msg__ObjectReferencePoint__fini(msg);
    return false;
  }
  return true;
}

void
mtr_prediction_msgs__msg__ObjectReferencePoint__fini(mtr_prediction_msgs__msg__ObjectReferencePoint * msg)
{
  if (!msg) {
    return;
  }
  // value
  // translation_to_geometric_center
  geometry_msgs__msg__Vector3__fini(&msg->translation_to_geometric_center);
}

bool
mtr_prediction_msgs__msg__ObjectReferencePoint__are_equal(const mtr_prediction_msgs__msg__ObjectReferencePoint * lhs, const mtr_prediction_msgs__msg__ObjectReferencePoint * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // value
  if (lhs->value != rhs->value) {
    return false;
  }
  // translation_to_geometric_center
  if (!geometry_msgs__msg__Vector3__are_equal(
      &(lhs->translation_to_geometric_center), &(rhs->translation_to_geometric_center)))
  {
    return false;
  }
  return true;
}

bool
mtr_prediction_msgs__msg__ObjectReferencePoint__copy(
  const mtr_prediction_msgs__msg__ObjectReferencePoint * input,
  mtr_prediction_msgs__msg__ObjectReferencePoint * output)
{
  if (!input || !output) {
    return false;
  }
  // value
  output->value = input->value;
  // translation_to_geometric_center
  if (!geometry_msgs__msg__Vector3__copy(
      &(input->translation_to_geometric_center), &(output->translation_to_geometric_center)))
  {
    return false;
  }
  return true;
}

mtr_prediction_msgs__msg__ObjectReferencePoint *
mtr_prediction_msgs__msg__ObjectReferencePoint__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectReferencePoint * msg = (mtr_prediction_msgs__msg__ObjectReferencePoint *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__ObjectReferencePoint), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(mtr_prediction_msgs__msg__ObjectReferencePoint));
  bool success = mtr_prediction_msgs__msg__ObjectReferencePoint__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
mtr_prediction_msgs__msg__ObjectReferencePoint__destroy(mtr_prediction_msgs__msg__ObjectReferencePoint * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    mtr_prediction_msgs__msg__ObjectReferencePoint__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence__init(mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectReferencePoint * data = NULL;

  if (size) {
    data = (mtr_prediction_msgs__msg__ObjectReferencePoint *)allocator.zero_allocate(size, sizeof(mtr_prediction_msgs__msg__ObjectReferencePoint), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = mtr_prediction_msgs__msg__ObjectReferencePoint__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        mtr_prediction_msgs__msg__ObjectReferencePoint__fini(&data[i - 1]);
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
mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence__fini(mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence * array)
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
      mtr_prediction_msgs__msg__ObjectReferencePoint__fini(&array->data[i]);
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

mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence *
mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence * array = (mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence__destroy(mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence__are_equal(const mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence * lhs, const mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!mtr_prediction_msgs__msg__ObjectReferencePoint__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence__copy(
  const mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence * input,
  mtr_prediction_msgs__msg__ObjectReferencePoint__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(mtr_prediction_msgs__msg__ObjectReferencePoint);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    mtr_prediction_msgs__msg__ObjectReferencePoint * data =
      (mtr_prediction_msgs__msg__ObjectReferencePoint *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!mtr_prediction_msgs__msg__ObjectReferencePoint__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          mtr_prediction_msgs__msg__ObjectReferencePoint__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!mtr_prediction_msgs__msg__ObjectReferencePoint__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

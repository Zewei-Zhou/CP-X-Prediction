// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from mtr_prediction_msgs:msg/ObjectClassification.idl
// generated code does not contain a copyright notice
#include "mtr_prediction_msgs/msg/detail/object_classification__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
mtr_prediction_msgs__msg__ObjectClassification__init(mtr_prediction_msgs__msg__ObjectClassification * msg)
{
  if (!msg) {
    return false;
  }
  // type
  // probability
  return true;
}

void
mtr_prediction_msgs__msg__ObjectClassification__fini(mtr_prediction_msgs__msg__ObjectClassification * msg)
{
  if (!msg) {
    return;
  }
  // type
  // probability
}

bool
mtr_prediction_msgs__msg__ObjectClassification__are_equal(const mtr_prediction_msgs__msg__ObjectClassification * lhs, const mtr_prediction_msgs__msg__ObjectClassification * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // type
  if (lhs->type != rhs->type) {
    return false;
  }
  // probability
  if (lhs->probability != rhs->probability) {
    return false;
  }
  return true;
}

bool
mtr_prediction_msgs__msg__ObjectClassification__copy(
  const mtr_prediction_msgs__msg__ObjectClassification * input,
  mtr_prediction_msgs__msg__ObjectClassification * output)
{
  if (!input || !output) {
    return false;
  }
  // type
  output->type = input->type;
  // probability
  output->probability = input->probability;
  return true;
}

mtr_prediction_msgs__msg__ObjectClassification *
mtr_prediction_msgs__msg__ObjectClassification__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectClassification * msg = (mtr_prediction_msgs__msg__ObjectClassification *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__ObjectClassification), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(mtr_prediction_msgs__msg__ObjectClassification));
  bool success = mtr_prediction_msgs__msg__ObjectClassification__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
mtr_prediction_msgs__msg__ObjectClassification__destroy(mtr_prediction_msgs__msg__ObjectClassification * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    mtr_prediction_msgs__msg__ObjectClassification__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
mtr_prediction_msgs__msg__ObjectClassification__Sequence__init(mtr_prediction_msgs__msg__ObjectClassification__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectClassification * data = NULL;

  if (size) {
    data = (mtr_prediction_msgs__msg__ObjectClassification *)allocator.zero_allocate(size, sizeof(mtr_prediction_msgs__msg__ObjectClassification), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = mtr_prediction_msgs__msg__ObjectClassification__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        mtr_prediction_msgs__msg__ObjectClassification__fini(&data[i - 1]);
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
mtr_prediction_msgs__msg__ObjectClassification__Sequence__fini(mtr_prediction_msgs__msg__ObjectClassification__Sequence * array)
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
      mtr_prediction_msgs__msg__ObjectClassification__fini(&array->data[i]);
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

mtr_prediction_msgs__msg__ObjectClassification__Sequence *
mtr_prediction_msgs__msg__ObjectClassification__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mtr_prediction_msgs__msg__ObjectClassification__Sequence * array = (mtr_prediction_msgs__msg__ObjectClassification__Sequence *)allocator.allocate(sizeof(mtr_prediction_msgs__msg__ObjectClassification__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = mtr_prediction_msgs__msg__ObjectClassification__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
mtr_prediction_msgs__msg__ObjectClassification__Sequence__destroy(mtr_prediction_msgs__msg__ObjectClassification__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    mtr_prediction_msgs__msg__ObjectClassification__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
mtr_prediction_msgs__msg__ObjectClassification__Sequence__are_equal(const mtr_prediction_msgs__msg__ObjectClassification__Sequence * lhs, const mtr_prediction_msgs__msg__ObjectClassification__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!mtr_prediction_msgs__msg__ObjectClassification__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
mtr_prediction_msgs__msg__ObjectClassification__Sequence__copy(
  const mtr_prediction_msgs__msg__ObjectClassification__Sequence * input,
  mtr_prediction_msgs__msg__ObjectClassification__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(mtr_prediction_msgs__msg__ObjectClassification);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    mtr_prediction_msgs__msg__ObjectClassification * data =
      (mtr_prediction_msgs__msg__ObjectClassification *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!mtr_prediction_msgs__msg__ObjectClassification__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          mtr_prediction_msgs__msg__ObjectClassification__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!mtr_prediction_msgs__msg__ObjectClassification__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

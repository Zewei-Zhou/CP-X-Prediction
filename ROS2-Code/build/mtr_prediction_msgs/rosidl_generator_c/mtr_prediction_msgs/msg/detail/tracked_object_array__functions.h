// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from mtr_prediction_msgs:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__FUNCTIONS_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "mtr_prediction_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "mtr_prediction_msgs/msg/detail/tracked_object_array__struct.h"

/// Initialize msg/TrackedObjectArray message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * mtr_prediction_msgs__msg__TrackedObjectArray
 * )) before or use
 * mtr_prediction_msgs__msg__TrackedObjectArray__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
bool
mtr_prediction_msgs__msg__TrackedObjectArray__init(mtr_prediction_msgs__msg__TrackedObjectArray * msg);

/// Finalize msg/TrackedObjectArray message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
void
mtr_prediction_msgs__msg__TrackedObjectArray__fini(mtr_prediction_msgs__msg__TrackedObjectArray * msg);

/// Create msg/TrackedObjectArray message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * mtr_prediction_msgs__msg__TrackedObjectArray__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
mtr_prediction_msgs__msg__TrackedObjectArray *
mtr_prediction_msgs__msg__TrackedObjectArray__create();

/// Destroy msg/TrackedObjectArray message.
/**
 * It calls
 * mtr_prediction_msgs__msg__TrackedObjectArray__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
void
mtr_prediction_msgs__msg__TrackedObjectArray__destroy(mtr_prediction_msgs__msg__TrackedObjectArray * msg);

/// Check for msg/TrackedObjectArray message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
bool
mtr_prediction_msgs__msg__TrackedObjectArray__are_equal(const mtr_prediction_msgs__msg__TrackedObjectArray * lhs, const mtr_prediction_msgs__msg__TrackedObjectArray * rhs);

/// Copy a msg/TrackedObjectArray message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
bool
mtr_prediction_msgs__msg__TrackedObjectArray__copy(
  const mtr_prediction_msgs__msg__TrackedObjectArray * input,
  mtr_prediction_msgs__msg__TrackedObjectArray * output);

/// Initialize array of msg/TrackedObjectArray messages.
/**
 * It allocates the memory for the number of elements and calls
 * mtr_prediction_msgs__msg__TrackedObjectArray__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
bool
mtr_prediction_msgs__msg__TrackedObjectArray__Sequence__init(mtr_prediction_msgs__msg__TrackedObjectArray__Sequence * array, size_t size);

/// Finalize array of msg/TrackedObjectArray messages.
/**
 * It calls
 * mtr_prediction_msgs__msg__TrackedObjectArray__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
void
mtr_prediction_msgs__msg__TrackedObjectArray__Sequence__fini(mtr_prediction_msgs__msg__TrackedObjectArray__Sequence * array);

/// Create array of msg/TrackedObjectArray messages.
/**
 * It allocates the memory for the array and calls
 * mtr_prediction_msgs__msg__TrackedObjectArray__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
mtr_prediction_msgs__msg__TrackedObjectArray__Sequence *
mtr_prediction_msgs__msg__TrackedObjectArray__Sequence__create(size_t size);

/// Destroy array of msg/TrackedObjectArray messages.
/**
 * It calls
 * mtr_prediction_msgs__msg__TrackedObjectArray__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
void
mtr_prediction_msgs__msg__TrackedObjectArray__Sequence__destroy(mtr_prediction_msgs__msg__TrackedObjectArray__Sequence * array);

/// Check for msg/TrackedObjectArray message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
bool
mtr_prediction_msgs__msg__TrackedObjectArray__Sequence__are_equal(const mtr_prediction_msgs__msg__TrackedObjectArray__Sequence * lhs, const mtr_prediction_msgs__msg__TrackedObjectArray__Sequence * rhs);

/// Copy an array of msg/TrackedObjectArray messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
bool
mtr_prediction_msgs__msg__TrackedObjectArray__Sequence__copy(
  const mtr_prediction_msgs__msg__TrackedObjectArray__Sequence * input,
  mtr_prediction_msgs__msg__TrackedObjectArray__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_ARRAY__FUNCTIONS_H_

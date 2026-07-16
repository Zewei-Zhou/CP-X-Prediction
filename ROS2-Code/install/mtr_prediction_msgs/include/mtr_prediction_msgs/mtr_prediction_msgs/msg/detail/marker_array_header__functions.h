// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from mtr_prediction_msgs:msg/MarkerArrayHeader.idl
// generated code does not contain a copyright notice

#ifndef MTR_PREDICTION_MSGS__MSG__DETAIL__MARKER_ARRAY_HEADER__FUNCTIONS_H_
#define MTR_PREDICTION_MSGS__MSG__DETAIL__MARKER_ARRAY_HEADER__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "mtr_prediction_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "mtr_prediction_msgs/msg/detail/marker_array_header__struct.h"

/// Initialize msg/MarkerArrayHeader message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * mtr_prediction_msgs__msg__MarkerArrayHeader
 * )) before or use
 * mtr_prediction_msgs__msg__MarkerArrayHeader__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
bool
mtr_prediction_msgs__msg__MarkerArrayHeader__init(mtr_prediction_msgs__msg__MarkerArrayHeader * msg);

/// Finalize msg/MarkerArrayHeader message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
void
mtr_prediction_msgs__msg__MarkerArrayHeader__fini(mtr_prediction_msgs__msg__MarkerArrayHeader * msg);

/// Create msg/MarkerArrayHeader message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * mtr_prediction_msgs__msg__MarkerArrayHeader__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
mtr_prediction_msgs__msg__MarkerArrayHeader *
mtr_prediction_msgs__msg__MarkerArrayHeader__create();

/// Destroy msg/MarkerArrayHeader message.
/**
 * It calls
 * mtr_prediction_msgs__msg__MarkerArrayHeader__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
void
mtr_prediction_msgs__msg__MarkerArrayHeader__destroy(mtr_prediction_msgs__msg__MarkerArrayHeader * msg);

/// Check for msg/MarkerArrayHeader message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
bool
mtr_prediction_msgs__msg__MarkerArrayHeader__are_equal(const mtr_prediction_msgs__msg__MarkerArrayHeader * lhs, const mtr_prediction_msgs__msg__MarkerArrayHeader * rhs);

/// Copy a msg/MarkerArrayHeader message.
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
mtr_prediction_msgs__msg__MarkerArrayHeader__copy(
  const mtr_prediction_msgs__msg__MarkerArrayHeader * input,
  mtr_prediction_msgs__msg__MarkerArrayHeader * output);

/// Initialize array of msg/MarkerArrayHeader messages.
/**
 * It allocates the memory for the number of elements and calls
 * mtr_prediction_msgs__msg__MarkerArrayHeader__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
bool
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__init(mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * array, size_t size);

/// Finalize array of msg/MarkerArrayHeader messages.
/**
 * It calls
 * mtr_prediction_msgs__msg__MarkerArrayHeader__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
void
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__fini(mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * array);

/// Create array of msg/MarkerArrayHeader messages.
/**
 * It allocates the memory for the array and calls
 * mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence *
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__create(size_t size);

/// Destroy array of msg/MarkerArrayHeader messages.
/**
 * It calls
 * mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
void
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__destroy(mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * array);

/// Check for msg/MarkerArrayHeader message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_mtr_prediction_msgs
bool
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__are_equal(const mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * lhs, const mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * rhs);

/// Copy an array of msg/MarkerArrayHeader messages.
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
mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__copy(
  const mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * input,
  mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // MTR_PREDICTION_MSGS__MSG__DETAIL__MARKER_ARRAY_HEADER__FUNCTIONS_H_

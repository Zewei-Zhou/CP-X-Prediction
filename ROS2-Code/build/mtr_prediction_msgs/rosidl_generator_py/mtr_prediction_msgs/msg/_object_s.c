// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from mtr_prediction_msgs:msg/Object.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "mtr_prediction_msgs/msg/detail/object__struct.h"
#include "mtr_prediction_msgs/msg/detail/object__functions.h"

#include "rosidl_runtime_c/primitives_sequence.h"
#include "rosidl_runtime_c/primitives_sequence_functions.h"

// Nested array functions includes
#include "mtr_prediction_msgs/msg/detail/object_state__functions.h"
#include "mtr_prediction_msgs/msg/detail/object_state_prediction__functions.h"
// end nested array functions include
bool mtr_prediction_msgs__msg__object_state__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * mtr_prediction_msgs__msg__object_state__convert_to_py(void * raw_ros_message);
bool mtr_prediction_msgs__msg__object_state__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * mtr_prediction_msgs__msg__object_state__convert_to_py(void * raw_ros_message);
bool mtr_prediction_msgs__msg__object_state_prediction__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * mtr_prediction_msgs__msg__object_state_prediction__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool mtr_prediction_msgs__msg__object__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[39];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("mtr_prediction_msgs.msg._object.Object", full_classname_dest, 38) == 0);
  }
  mtr_prediction_msgs__msg__Object * ros_message = _ros_message;
  {  // id
    PyObject * field = PyObject_GetAttrString(_pymsg, "id");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->id = PyLong_AsUnsignedLongLong(field);
    Py_DECREF(field);
  }
  {  // existence_probability
    PyObject * field = PyObject_GetAttrString(_pymsg, "existence_probability");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->existence_probability = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // state
    PyObject * field = PyObject_GetAttrString(_pymsg, "state");
    if (!field) {
      return false;
    }
    if (!mtr_prediction_msgs__msg__object_state__convert_from_py(field, &ros_message->state)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // state_history
    PyObject * field = PyObject_GetAttrString(_pymsg, "state_history");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'state_history'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!mtr_prediction_msgs__msg__ObjectState__Sequence__init(&(ros_message->state_history), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create mtr_prediction_msgs__msg__ObjectState__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    mtr_prediction_msgs__msg__ObjectState * dest = ros_message->state_history.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!mtr_prediction_msgs__msg__object_state__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }
  {  // state_predictions
    PyObject * field = PyObject_GetAttrString(_pymsg, "state_predictions");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'state_predictions'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence__init(&(ros_message->state_predictions), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create mtr_prediction_msgs__msg__ObjectStatePrediction__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    mtr_prediction_msgs__msg__ObjectStatePrediction * dest = ros_message->state_predictions.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!mtr_prediction_msgs__msg__object_state_prediction__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * mtr_prediction_msgs__msg__object__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Object */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("mtr_prediction_msgs.msg._object");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Object");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  mtr_prediction_msgs__msg__Object * ros_message = (mtr_prediction_msgs__msg__Object *)raw_ros_message;
  {  // id
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLongLong(ros_message->id);
    {
      int rc = PyObject_SetAttrString(_pymessage, "id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // existence_probability
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->existence_probability);
    {
      int rc = PyObject_SetAttrString(_pymessage, "existence_probability", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // state
    PyObject * field = NULL;
    field = mtr_prediction_msgs__msg__object_state__convert_to_py(&ros_message->state);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // state_history
    PyObject * field = NULL;
    size_t size = ros_message->state_history.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    mtr_prediction_msgs__msg__ObjectState * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->state_history.data[i]);
      PyObject * pyitem = mtr_prediction_msgs__msg__object_state__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "state_history", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // state_predictions
    PyObject * field = NULL;
    size_t size = ros_message->state_predictions.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    mtr_prediction_msgs__msg__ObjectStatePrediction * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->state_predictions.data[i]);
      PyObject * pyitem = mtr_prediction_msgs__msg__object_state_prediction__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "state_predictions", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

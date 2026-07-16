#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "mtr_prediction_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__mtr_prediction_msgs__msg__MarkerArrayHeader() -> *const std::ffi::c_void;
}

#[link(name = "mtr_prediction_msgs__rosidl_generator_c")]
extern "C" {
    fn mtr_prediction_msgs__msg__MarkerArrayHeader__init(msg: *mut MarkerArrayHeader) -> bool;
    fn mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MarkerArrayHeader>, size: usize) -> bool;
    fn mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MarkerArrayHeader>);
    fn mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MarkerArrayHeader>, out_seq: *mut rosidl_runtime_rs::Sequence<MarkerArrayHeader>) -> bool;
}

// Corresponds to mtr_prediction_msgs__msg__MarkerArrayHeader
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MarkerArrayHeader {
    /// header for time/frame information
    pub header: std_msgs::msg::rmw::Header,

    /// markers from visualization_msgs::markers
    pub markers: rosidl_runtime_rs::Sequence<visualization_msgs::msg::rmw::Marker>,

}



impl Default for MarkerArrayHeader {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !mtr_prediction_msgs__msg__MarkerArrayHeader__init(&mut msg as *mut _) {
        panic!("Call to mtr_prediction_msgs__msg__MarkerArrayHeader__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MarkerArrayHeader {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mtr_prediction_msgs__msg__MarkerArrayHeader__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MarkerArrayHeader {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MarkerArrayHeader where Self: Sized {
  const TYPE_NAME: &'static str = "mtr_prediction_msgs/msg/MarkerArrayHeader";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__mtr_prediction_msgs__msg__MarkerArrayHeader() }
  }
}


#[link(name = "mtr_prediction_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__mtr_prediction_msgs__msg__PredictedTrajectory() -> *const std::ffi::c_void;
}

#[link(name = "mtr_prediction_msgs__rosidl_generator_c")]
extern "C" {
    fn mtr_prediction_msgs__msg__PredictedTrajectory__init(msg: *mut PredictedTrajectory) -> bool;
    fn mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PredictedTrajectory>, size: usize) -> bool;
    fn mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PredictedTrajectory>);
    fn mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PredictedTrajectory>, out_seq: *mut rosidl_runtime_rs::Sequence<PredictedTrajectory>) -> bool;
}

// Corresponds to mtr_prediction_msgs__msg__PredictedTrajectory
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Single predicted trajectory mode

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PredictedTrajectory {
    /// Probability of this mode (0.0 to 1.0)
    pub confidence: f32,

    /// Predicted waypoints (80 future timesteps at 10Hz = 8 seconds)
    /// Each has pose + timestamp
    pub waypoints: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::PoseStamped>,

    /// Optional: predicted velocities
    pub velocities: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::TwistStamped>,

}



impl Default for PredictedTrajectory {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !mtr_prediction_msgs__msg__PredictedTrajectory__init(&mut msg as *mut _) {
        panic!("Call to mtr_prediction_msgs__msg__PredictedTrajectory__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PredictedTrajectory {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mtr_prediction_msgs__msg__PredictedTrajectory__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PredictedTrajectory {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PredictedTrajectory where Self: Sized {
  const TYPE_NAME: &'static str = "mtr_prediction_msgs/msg/PredictedTrajectory";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__mtr_prediction_msgs__msg__PredictedTrajectory() }
  }
}


#[link(name = "mtr_prediction_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__mtr_prediction_msgs__msg__ObjectPrediction() -> *const std::ffi::c_void;
}

#[link(name = "mtr_prediction_msgs__rosidl_generator_c")]
extern "C" {
    fn mtr_prediction_msgs__msg__ObjectPrediction__init(msg: *mut ObjectPrediction) -> bool;
    fn mtr_prediction_msgs__msg__ObjectPrediction__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ObjectPrediction>, size: usize) -> bool;
    fn mtr_prediction_msgs__msg__ObjectPrediction__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ObjectPrediction>);
    fn mtr_prediction_msgs__msg__ObjectPrediction__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ObjectPrediction>, out_seq: *mut rosidl_runtime_rs::Sequence<ObjectPrediction>) -> bool;
}

// Corresponds to mtr_prediction_msgs__msg__ObjectPrediction
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Prediction for a single object

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObjectPrediction {

    // This member is not documented.
    #[allow(missing_docs)]
    pub object_id: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub object_type: u8,

    /// Multiple trajectory modes (MTR outputs 6 modes)
    pub trajectories: rosidl_runtime_rs::Sequence<super::super::msg::rmw::PredictedTrajectory>,

}



impl Default for ObjectPrediction {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !mtr_prediction_msgs__msg__ObjectPrediction__init(&mut msg as *mut _) {
        panic!("Call to mtr_prediction_msgs__msg__ObjectPrediction__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ObjectPrediction {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mtr_prediction_msgs__msg__ObjectPrediction__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mtr_prediction_msgs__msg__ObjectPrediction__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mtr_prediction_msgs__msg__ObjectPrediction__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ObjectPrediction {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ObjectPrediction where Self: Sized {
  const TYPE_NAME: &'static str = "mtr_prediction_msgs/msg/ObjectPrediction";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__mtr_prediction_msgs__msg__ObjectPrediction() }
  }
}



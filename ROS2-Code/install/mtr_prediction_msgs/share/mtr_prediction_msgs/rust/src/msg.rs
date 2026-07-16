#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to mtr_prediction_msgs__msg__MarkerArrayHeader

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MarkerArrayHeader {
    /// header for time/frame information
    pub header: std_msgs::msg::Header,

    /// markers from visualization_msgs::markers
    pub markers: Vec<visualization_msgs::msg::Marker>,

}



impl Default for MarkerArrayHeader {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::MarkerArrayHeader::default())
  }
}

impl rosidl_runtime_rs::Message for MarkerArrayHeader {
  type RmwMsg = super::msg::rmw::MarkerArrayHeader;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        markers: msg.markers
          .into_iter()
          .map(|elem| visualization_msgs::msg::Marker::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        markers: msg.markers
          .iter()
          .map(|elem| visualization_msgs::msg::Marker::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      markers: msg.markers
          .into_iter()
          .map(visualization_msgs::msg::Marker::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to mtr_prediction_msgs__msg__PredictedTrajectory
/// Single predicted trajectory mode

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PredictedTrajectory {
    /// Probability of this mode (0.0 to 1.0)
    pub confidence: f32,

    /// Predicted waypoints (80 future timesteps at 10Hz = 8 seconds)
    /// Each has pose + timestamp
    pub waypoints: Vec<geometry_msgs::msg::PoseStamped>,

    /// Optional: predicted velocities
    pub velocities: Vec<geometry_msgs::msg::TwistStamped>,

}



impl Default for PredictedTrajectory {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::PredictedTrajectory::default())
  }
}

impl rosidl_runtime_rs::Message for PredictedTrajectory {
  type RmwMsg = super::msg::rmw::PredictedTrajectory;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        confidence: msg.confidence,
        waypoints: msg.waypoints
          .into_iter()
          .map(|elem| geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        velocities: msg.velocities
          .into_iter()
          .map(|elem| geometry_msgs::msg::TwistStamped::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      confidence: msg.confidence,
        waypoints: msg.waypoints
          .iter()
          .map(|elem| geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        velocities: msg.velocities
          .iter()
          .map(|elem| geometry_msgs::msg::TwistStamped::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      confidence: msg.confidence,
      waypoints: msg.waypoints
          .into_iter()
          .map(geometry_msgs::msg::PoseStamped::from_rmw_message)
          .collect(),
      velocities: msg.velocities
          .into_iter()
          .map(geometry_msgs::msg::TwistStamped::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to mtr_prediction_msgs__msg__ObjectPrediction
/// Prediction for a single object

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObjectPrediction {

    // This member is not documented.
    #[allow(missing_docs)]
    pub object_id: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub object_type: u8,

    /// Multiple trajectory modes (MTR outputs 6 modes)
    pub trajectories: Vec<super::msg::PredictedTrajectory>,

}



impl Default for ObjectPrediction {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ObjectPrediction::default())
  }
}

impl rosidl_runtime_rs::Message for ObjectPrediction {
  type RmwMsg = super::msg::rmw::ObjectPrediction;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        object_id: msg.object_id,
        object_type: msg.object_type,
        trajectories: msg.trajectories
          .into_iter()
          .map(|elem| super::msg::PredictedTrajectory::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      object_id: msg.object_id,
      object_type: msg.object_type,
        trajectories: msg.trajectories
          .iter()
          .map(|elem| super::msg::PredictedTrajectory::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      object_id: msg.object_id,
      object_type: msg.object_type,
      trajectories: msg.trajectories
          .into_iter()
          .map(super::msg::PredictedTrajectory::from_rmw_message)
          .collect(),
    }
  }
}



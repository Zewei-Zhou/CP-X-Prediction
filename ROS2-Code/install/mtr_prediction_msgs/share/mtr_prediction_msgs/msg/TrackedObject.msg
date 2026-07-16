# Single tracked object for motion prediction input
std_msgs/Header header

# Object identification
uint64 object_id
uint8 model_id  # Same as ObjectState (1=ego, 16=vehicle, etc.)

# Current state
geometry_msgs/Pose pose  # x, y, z, orientation
geometry_msgs/Twist velocity  # linear and angular velocity
geometry_msgs/Vector3 size  # length, width, height

# Object classification
uint8 object_type
uint8 OBJECT_TYPE_UNKNOWN = 0
uint8 OBJECT_TYPE_VEHICLE = 1
uint8 OBJECT_TYPE_PEDESTRIAN = 2
uint8 OBJECT_TYPE_CYCLIST = 3

# Historical trajectory (10 past states at 10Hz = 1 second history)
ObjectState[] track_history
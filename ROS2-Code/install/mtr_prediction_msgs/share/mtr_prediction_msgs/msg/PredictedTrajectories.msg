# Predictions for all objects
std_msgs/Header header

# Array of predictions (one per tracked object)
ObjectPrediction[] predictions

# Optional: Map information used for prediction
sensor_msgs/PointCloud2 map_polylines
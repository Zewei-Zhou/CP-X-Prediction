import sys
import os
import math
import re
import rclpy
from rclpy.node import Node
import torch
import numpy as np
from collections import deque

from mtr_prediction_msgs.msg import MarkerArrayHeader, PredictedTrajectory,  ObjectPrediction
from geometry_msgs.msg import PoseStamped, TwistStamped
from mtr.models.model import MotionTransformer
from mtr.config import cfg, cfg_from_yaml_file
from mtr.datasets.waymo.waymo_dataset import WaymoDataset 

class MTRPredictionNode(Node):
    def __init__(self):
        super().__init__('mtr_prediction_node')
        
        # 1. Load MTR Configuration
        cfg_file = "/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Prediction/MTR/tools/cfgs/challenge/mtr-finetuning-V2XPNP.yaml"
        cfg_from_yaml_file(cfg_file, cfg)
        
        # 2. Initialize Model
        self.get_logger().info("Loading MTR Model into GPU...")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = MotionTransformer(config=cfg.MODEL).to(self.device)
        
        # 3. Load Weights
        weights_path = "/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Prediction/MTR/output/challenge/mtr-training-CPX-Prediction/good_ckpt/checkpoint_epoch_25.pth"
        self.model.load_params_with_optimizer(weights_path, to_cpu=False, logger=self.get_logger())
        self.model.eval() # CRITICAL: Put model in inference mode
        
        # Initialize an empty dummy dataset just to access its coordinate transformation tools
        self.dataset_tools = WaymoDataset(dataset_cfg=cfg.DATA_CONFIG, training=False, logger=self.get_logger())

        # ROS Setup
        # self.sub = self.create_subscription(TrackedObjectArray, '/tracking/car/transformed_objects_header_box_score_label', self.tracking_callback, 10)
        # self.sub_ego = self.create_subscription()
        self.sub_carxx = self.create_subscription(MarkerArrayHeader, '/tracking/carxx/transformed_objects_header_box_score_label', self.tracking_callback, 10)
        # self.sub_carzzl = self.create_subscription(MarkerArrayHeader, '/tracking/carzzl/transformed_objects_header_box_score_label', self.tracking_callback, 10)
        
        self.pub = self.create_publisher(ObjectPrediction, '/prediction/trajectories', 10)
        self.history_buffer = deque(maxlen=11)



    def extract_agent_features(self, marker_msg, timestamp):
        """
        Takes a single ROS visualization_msgs/Marker and returns a dictionary 
        of features ready for MTR history buffering.
        """
        # 1. Position and Dimensions
        x = marker_msg.pose.position.x
        y = marker_msg.pose.position.y
        z = marker_msg.pose.position.z
        length = marker_msg.scale.x
        width = marker_msg.scale.y
        height = marker_msg.scale.z
        
        # 2. Calculate Heading (Yaw) from Quaternion
        qx = marker_msg.pose.orientation.x
        qy = marker_msg.pose.orientation.y
        qz = marker_msg.pose.orientation.z
        qw = marker_msg.pose.orientation.w
        
        siny_cosp = 2 * (qw * qz + qx * qy)
        cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        
        # 3. Parse the text field: "0.41 m/s, <ID= 9>, <ds= ...>"
        text_data = marker_msg.text
        speed_match = re.search(r"([0-9.]+)\s*m/s", text_data)
        speed = float(speed_match.group(1)) if speed_match else 0.0
        agent_id = marker_msg.id
        
        # 4. Calculate Vector Velocities
        vx = speed * math.cos(yaw)
        vy = speed * math.sin(yaw)
        
        # 5. Determine type and map to Waymo formats
        agent_ns = marker_msg.ns.lower()
        if "car" in agent_ns:
            waymo_type = 'TYPE_VEHICLE'
        elif "pedestrian" in agent_ns:
            waymo_type = 'TYPE_PEDESTRIAN'
        elif "cyclist" in agent_ns:
            waymo_type = 'TYPE_CYCLIST'
        else:
            waymo_type = 'TYPE_VEHICLE' # Fallback
        
        return {
            "id": agent_id,
            "type": waymo_type,
            "state": [x, y, z, length, width, height, yaw, vx, vy],
            "timestamp": timestamp
        }
        
    def extract_ego_features(self, ego_msg):
        pass
    
    def update_history_buffer_ego_agent(self, msg):
        # find the history frame with the timestamp that matches the EGO vehicle
        pass


    def update_history_buffer(self, msg):
        """
        Update history buffer for every new incoming message.
        """
        # contains information for all agents
        frame_information = []
        
        # Extract Ego Vehicle from ROS MSG
        # get the EGO vehicle information for the given timestamp?
        ego_features = None
        # frame_information.append(ego_features)
    
        
        ts = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        for marker_msg in msg.markers:
            agent_features = self.extract_agent_features(marker_msg, ts)
            frame_information.append(agent_features)
        
        self.history_buffer.append(frame_information)
                
    def create_batch_dict(self):
        """
            batch_dict = {
                'batch_size': 1,
                'input_dict': {
                    # --- AGENT TENSORS ---
                    # The heavily processed ego-centric features [batch, num_agents, num_timesteps, 28]
                    'obj_trajs': torch.Tensor(...), 
                    # Which timesteps are valid for which agents [batch, num_agents, num_timesteps]
                    'obj_trajs_mask': torch.BoolTensor(...), 
                    # The index of the Ego vehicle in the num_agents list (usually [0])
                    'track_index_to_predict': torch.LongTensor([0]), 
                    
                    # --- EGO/CENTER STATE ---
                    # The global state of the Ego vehicle [batch, 10] -> [x, y, z, l, w, h, heading, vx, vy, valid]
                    'center_objects_world': torch.Tensor(...), 
                    'center_objects_type': np.array(['TYPE_VEHICLE']),
                    'center_objects_id': np.array([ego_id]),

                    # --- MAP TENSORS ---
                    # Processed polylines [batch, num_polylines, points_per_line, 9]
                    'map_polylines': torch.Tensor(...), 
                    'map_polylines_mask': torch.BoolTensor(...),
                    'map_polylines_center': torch.Tensor(...),

                    # --- DUMMY LABELS (Required to prevent KeyError during inference) ---
                    'center_gt_trajs_src': torch.zeros((1, 80, 10)), # 80 future steps, 10 features
                    'obj_trajs_future_state': torch.zeros((1, num_agents, 80, 4)),
                    'obj_trajs_future_mask': torch.zeros((1, num_agents, 80), dtype=torch.bool),
                }
            }
        """
        # ---------------------------------------------------------
        # STEP A: Find Unique Agents and Map Types
        # ---------------------------------------------------------
        unique_agent_ids = []
        id_to_type = {} 
        
        for frame in self.history_buffer:
            for agent in frame:
                if agent["id"] not in id_to_type:
                    unique_agent_ids.append(agent["id"])
                    id_to_type[agent["id"]] = agent["type"]
        
        num_agents = len(unique_agent_ids)
        id_to_index = {agent_id: idx for idx, agent_id in enumerate(unique_agent_ids)}

        # ---------------------------------------------------------
        # STEP B: Initialize Empty Arrays
        # ---------------------------------------------------------
        raw_global_trajectories = np.zeros((num_agents, 11, 10), dtype=np.float32)
        trajectory_masks = np.zeros((num_agents, 11), dtype=bool)
        obj_types = np.empty(num_agents, dtype=object)
        
        for agent_id, waymo_type in id_to_type.items():
            row_idx = id_to_index[agent_id]
            obj_types[row_idx] = waymo_type

        # ---------------------------------------------------------
        # STEP C: Fill the Arrays
        # ---------------------------------------------------------
        for t_idx, frame in enumerate(self.history_buffer):
            for agent in frame:
                row_idx = id_to_index[agent["id"]]
                raw_global_trajectories[row_idx, t_idx, :9] = agent["state"]
                raw_global_trajectories[row_idx, t_idx, 9] = 1.0 # Valid flag
                trajectory_masks[row_idx, t_idx] = True

        # ---------------------------------------------------------
        # STEP D: Transform Coordinates & Pack Batch Dict
        # ---------------------------------------------------------
        # 1. Dummy Ego State [x, y, z, length, width, height, heading, vx, vy, valid]
        dummy_ego_state = np.array([[0.0, 0.0, 0.0, 4.5, 2.0, 1.5, 0.0, 0.0, 0.0, 1.0]], dtype=np.float32)

        # 2. Past/future arrays (no batch dim — method adds it internally)
        timestamps = np.arange(11, dtype=np.float32) * 0.1
        obj_trajs_future_dummy = np.zeros((num_agents, 80, 10), dtype=np.float32)

        # 3. Coordinate Transformation (returns 4 arrays with leading num_center_objects dim)
        (
            obj_trajs_centered,
            obj_trajs_mask,
            obj_trajs_future_state,
            obj_trajs_future_mask,
        ) = self.dataset_tools.generate_centered_trajs_for_agents(
            center_objects=dummy_ego_state,
            obj_trajs_past=raw_global_trajectories,
            obj_types=obj_types,
            center_indices=np.array([0]),
            sdc_index=0,
            timestamps=timestamps,
            obj_trajs_future=obj_trajs_future_dummy,
        )

        # 4. Cast mask to bool and derive obj_trajs_pos / obj_trajs_last_pos
        obj_trajs_mask = obj_trajs_mask > 0
        obj_trajs_pos = obj_trajs_centered[:, :, :, 0:3]
        num_center, num_obj, num_t, _ = obj_trajs_pos.shape
        obj_trajs_last_pos = np.zeros((num_center, num_obj, 3), dtype=np.float32)
        for k in range(num_t):
            m = obj_trajs_mask[:, :, k]
            obj_trajs_last_pos[m] = obj_trajs_pos[:, :, k, :][m]

        # 4. Pack into the final input_dict
        input_dict = {
            # --- AGENT TENSORS ---
            'obj_trajs': torch.tensor(obj_trajs_centered),
            'obj_trajs_mask': torch.tensor(obj_trajs_mask),
            'obj_trajs_pos': torch.tensor(obj_trajs_pos),
            'obj_trajs_last_pos': torch.tensor(obj_trajs_last_pos),
            'obj_types': obj_types,
            'track_index_to_predict': torch.tensor([0], dtype=torch.long),
            
            # --- EGO/CENTER STATE ---
            'center_objects_world': torch.tensor(dummy_ego_state),
            'center_objects_type': np.array(['TYPE_VEHICLE']),
            'center_objects_id': np.array([0]),
            
            # --- DUMMY MAP TENSORS (To prevent crashes before map integration) ---
            'map_polylines': torch.zeros((1, 1, 20, 9)),
            'map_polylines_mask': torch.zeros((1, 1, 20), dtype=torch.bool),
            'map_polylines_center': torch.zeros((1, 1, 3)),

            # --- DUMMY LABELS (To prevent KeyErrors during inference) ---
            'center_gt_trajs_src': torch.zeros((1, 80, 10)),
            'obj_trajs_future_state': torch.zeros((1, num_agents, 80, 4)),
            'obj_trajs_future_mask': torch.zeros((1, num_agents, 80), dtype=torch.bool),
        }
        
        batch_dict = {
            'batch_size': 1,
            'input_dict': input_dict,
        }
        
        return batch_dict
    

    def tracking_callback(self, msg):
        self.update_history_buffer(msg)
        
        if len(self.history_buffer) < 11: 
            return

        batch_dict = self.create_batch_dict()
        
        for key, val in batch_dict['input_dict'].items():
            if isinstance(val, torch.Tensor):
                batch_dict['input_dict'][key] = val.to(self.device)
        
        with torch.no_grad():
            output_dict = self.model(batch_dict)
            
        # ---------------------------------------------------------
        # Extract Ego Outputs & Un-Rotate
        # ---------------------------------------------------------
        ego_pred_scores = output_dict['pred_scores'][0]
        ego_pred_trajs = output_dict['pred_trajs'][0]
        
        ego_state = batch_dict['input_dict']['center_objects_world'][0]
        ego_x = ego_state[0]
        ego_y = ego_state[1]
        ego_yaw = ego_state[6]

        cos_theta = torch.cos(ego_yaw)
        sin_theta = torch.sin(ego_yaw)

        x_local = ego_pred_trajs[..., 0]
        y_local = ego_pred_trajs[..., 1]

        x_global = ego_x + x_local * cos_theta - y_local * sin_theta
        y_global = ego_y + x_local * sin_theta + y_local * cos_theta

        # ---------------------------------------------------------
        # Format into Custom ROS Messages (Now with Twist!)
        # ---------------------------------------------------------
        obj_pred_msg = ObjectPrediction()
        obj_pred_msg.object_id = 0 
        obj_pred_msg.object_type = 0 # 0 = TYPE_VEHICLE
        
        dt = 0.1 # 10Hz prediction rate
        
        for mode_idx in range(6):
            traj_msg = PredictedTrajectory()
            traj_msg.confidence = ego_pred_scores[mode_idx].item()
            
            for t_idx in range(80):
                # 1. Pose Math
                waypoint_msg = PoseStamped()
                waypoint_msg.header = msg.header 
                
                curr_x = x_global[mode_idx, t_idx].item()
                curr_y = y_global[mode_idx, t_idx].item()
                
                waypoint_msg.pose.position.x = curr_x
                waypoint_msg.pose.position.y = curr_y
                waypoint_msg.pose.position.z = 0.0 
                waypoint_msg.pose.orientation.w = 1.0 
                
                traj_msg.waypoints.append(waypoint_msg)
                
                # 2. Velocity (Twist) Math
                twist_msg = TwistStamped()
                twist_msg.header = msg.header
                
                if t_idx == 0:
                    # For the very first step, look forward to get the velocity
                    next_x = x_global[mode_idx, 1].item()
                    next_y = y_global[mode_idx, 1].item()
                    dx = next_x - curr_x
                    dy = next_y - curr_y
                else:
                    # For all other steps, look backward
                    prev_x = x_global[mode_idx, t_idx - 1].item()
                    prev_y = y_global[mode_idx, t_idx - 1].item()
                    dx = curr_x - prev_x
                    dy = curr_y - prev_y
                    
                twist_msg.twist.linear.x = dx / dt
                twist_msg.twist.linear.y = dy / dt
                twist_msg.twist.linear.z = 0.0
                
                traj_msg.velocities.append(twist_msg)
            
            obj_pred_msg.trajectories.append(traj_msg)
            
        self.pub.publish(obj_pred_msg)

def main(args=None):
    rclpy.init(args=args)
    node = MTRPredictionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
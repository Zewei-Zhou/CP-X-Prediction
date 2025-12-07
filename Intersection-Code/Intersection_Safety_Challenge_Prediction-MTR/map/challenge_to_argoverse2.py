import pickle
import os
import numpy as np
import math
from map import *
from data_preprocess import create_infos_from_csv
from matplotlib import pyplot as plt
from av2.geometry.interpolate import interp_arc, compute_midpoint_line
import re
import torch

polygon_types = ['VEHICLE', 'BIKE', 'BUS', 'PEDESTRIAN']
polygon_is_intersections = [True, False, None]
out_intersection_id = ['2-1', '2--1', '16-2', '1--2',
                       '5-1', '5--1', '8--2', '81-2', '20-1',
                       '21--1', '64-2', '3-1', '4-2', '3--1',
                       '4--2', '0--1', '0-1', '2-2', '2--2',
                       '14--2', '4-1', '4--1', '1-1', '1--1']

point_types = ['DASH_SOLID_YELLOW', 'DASH_SOLID_WHITE', 'DASHED_WHITE', 'DASHED_YELLOW',
               'DOUBLE_SOLID_YELLOW', 'DOUBLE_SOLID_WHITE', 'DOUBLE_DASH_YELLOW', 'DOUBLE_DASH_WHITE',
               'SOLID_YELLOW', 'SOLID_WHITE', 'SOLID_DASH_WHITE', 'SOLID_DASH_YELLOW', 'SOLID_BLUE',
               'NONE', 'UNKNOWN', 'CROSSWALK', 'CENTERLINE']

point_sides = ['LEFT', 'RIGHT', 'CENTER']
polygon_to_polygon_types = ['NONE', 'PRED', 'SUCC', 'LEFT', 'RIGHT']

def get_scenario_segment_ids(vector_map):
    # get the segment ids set of Lanes and crosswalk
    lane_ids = {}
    crosswalk_ids = {}
    for index, feature in enumerate(vector_map.map_features):
        if isinstance(feature, Lane):
            lane_ids[str(feature.road_id) + '_' + str(feature.lane_id)] = index
        elif isinstance(feature, Crosswalk):
            crosswalk_id = str(feature.id)
            if crosswalk_id not in crosswalk_ids:
                crosswalk_ids[crosswalk_id] = []
            crosswalk_ids[crosswalk_id].append(index)

    return lane_ids, crosswalk_ids


def get_scenario_segments(vector_map, ids):
    # get the scenario segment set
    scenario_segments = []
    map_features = vector_map.map_features
    for id, map_indices in ids.items():
        if isinstance(map_indices, int):
            scenario_segments.append(map_features[map_indices])
        if isinstance(map_indices, list):
            # unique the content
            scenario_segment = []
            for index in map_indices:
                if not scenario_segment:
                    scenario_segment.append(map_features[index])
                elif not any(np.all(map_features[index].polygon == arr.polygon) for arr in scenario_segment):
                    scenario_segment.append(map_features[index])
            scenario_segments.append(scenario_segment)
    return scenario_segments


def map_preprocess(vector_map) -> None:
    for feature in vector_map.map_features:
        if hasattr(feature, 'boundary'):
            # hard coding downsample
            feature.boundary = np.array([[point.x, point.y] for point in feature.boundary[::5]])
        if hasattr(feature, 'polyline'):
            feature.polyline = np.array([[point.x, point.y] for point in feature.polyline])
        if hasattr(feature, 'polygon'):
            feature.polygon = np.array([[point.x, point.y] for point in feature.polygon])


def unique_crosswalk(cross_walk_ids):
    unique_cross_walk_ids = {}
    for id, index in cross_walk_ids.items():
        if id not in unique_cross_walk_ids:
            unique_cross_walk_ids[id] = []
        unique_cross_walk_ids[id].append(index)
    return unique_cross_walk_ids


def side_to_directed_lineseg(
        query_point: np.ndarray,
        start_point: np.ndarray,
        end_point: np.ndarray) -> str:
    cond = ((end_point[0] - start_point[0]) * (query_point[1] - start_point[1]) -
            (end_point[1] - start_point[1]) * (query_point[0] - start_point[0]))
    if cond > 0:
        return 'LEFT'
    elif cond < 0:
        return 'RIGHT'
    else:
        return 'CENTER'


def extract_values(input_str):
    pattern = r"\{(.*?)\}_\[(.*?)\]"

    match = re.match(pattern, input_str)

    if match:
        first_value = match.group(1) if match.group(1) else False
        second_value = match.group(2) if match.group(2) else False
        return f"{first_value}_{second_value}"
    else:
        return False
    

def compute_left_boundary(centerline_pts, right_ln_boundary, num_interp_pts):
    """
    Compute the left boundary of a lane given the centerline and the right boundary, with checks for stability.

    Args:
        centerline_pts (NDArrayFloat): Numpy array of shape (N, 2 or 3) representing the centerline.
        right_ln_boundary (NDArrayFloat): Numpy array of shape (N, 2 or 3) representing the right boundary.
        num_interp_pts (int): Desired number of interpolated points if initial points do not match.

    Returns:
        NDArrayFloat: Numpy array of shape (N, 2 or 3) representing the left boundary of the lane.

    Raises:
        ValueError: If the dimensions of the input arrays do not match or if they are not 2D or 3D.
    """
    # Ensure both arrays are 2D or 3D
    if centerline_pts.ndim != 2 or right_ln_boundary.ndim != 2:
        raise ValueError("Both centerline and right boundary points must be 2D arrays.")

    # Ensure both arrays have the same dimensionality
    if centerline_pts.shape[1] != right_ln_boundary.shape[1]:
        raise ValueError("Dimension mismatch: Centerline and right boundary must have the same number of columns.")

    # Ensure both arrays are either 2D or 3D
    if centerline_pts.shape[1] not in [2, 3]:
        raise ValueError("Both arrays must have either 2 or 3 dimensions per point.")

    # Adjust the number of points on both centerline and right boundary if they do not match
    if len(centerline_pts) != len(right_ln_boundary):
        centerline_pts = interp_arc(num_interp_pts, points=centerline_pts)
        right_ln_boundary = interp_arc(num_interp_pts, points=right_ln_boundary)

    # Calculate left boundary points by reflecting the right boundary across the centerline
    left_ln_boundary = 2 * centerline_pts - right_ln_boundary

    return left_ln_boundary


# --------------------------------------------------------------
# load vector map
with open("/home/cav/Zewei/Safety_challenge/Challenge_Prediction/map/vector_map.pkl", "rb") as f:
    vector_map = pickle.load(f)

map_preprocess(vector_map)

lane_segment_ids, cross_walk_ids = get_scenario_segment_ids(vector_map)
# cross_walk_ids = unique_crosswalk_id(cross_walk_ids)
polygon_ids = list(lane_segment_ids.keys()) + list(cross_walk_ids.keys())
num_polygons = len(lane_segment_ids) + len(cross_walk_ids) * 2

# initialization
dim = 3  # hard coding
polygon_position = np.zeros((num_polygons, dim), dtype=float)
polygon_orientation = np.zeros(num_polygons, dtype=float)
polygon_height = np.zeros(num_polygons, dtype=float)
polygon_type = np.zeros(num_polygons, dtype=np.uint8)
polygon_is_intersection = np.zeros(num_polygons, dtype=np.uint8)
point_position = [None] * num_polygons
point_orientation = [None] * num_polygons
point_magnitude = [None] * num_polygons
point_height = [None] * num_polygons
point_type = [None] * num_polygons
point_side = [None] * num_polygons

lane_segments = get_scenario_segments(vector_map, lane_segment_ids)
for lane_segment in lane_segments:
    lane_segment_idx = polygon_ids.index(str(lane_segment.road_id) + '_' + str(lane_segment.lane_id))
    centerline = lane_segment.polyline
    centerline = np.c_[centerline, np.zeros(centerline.shape[0])]
    polygon_position[lane_segment_idx] = centerline[0, :dim]  # hard coding 0 for height
    polygon_orientation[lane_segment_idx] = np.arctan2(centerline[1, 1] - centerline[0, 1],
                                                       centerline[1, 0] - centerline[0, 0])

    polygon_type[lane_segment_idx] = 1 if lane_segment.type == 0 else 3  # hard coding
    polygon_is_intersection[lane_segment_idx] = 0 \
        if polygon_ids[lane_segment_idx] in out_intersection_id else 1  # hard coding

    right_boundary = np.c_[lane_segment.boundary, np.zeros(lane_segment.boundary.shape[0])]
    left_boundary = compute_left_boundary(centerline, right_boundary, centerline.shape[0])

    point_position[lane_segment_idx] = np.concatenate([
        left_boundary[:-1, :dim],
        right_boundary[:-1, :dim],
        centerline[:-1, :dim]
    ], axis=0)

    left_vectors = left_boundary[1:] - left_boundary[:-1]
    right_vectors = right_boundary[1:] - right_boundary[:-1]
    center_vectors = centerline[1:] - centerline[:-1]

    point_orientation[lane_segment_idx] = np.concatenate([
        np.arctan2(left_vectors[:, 1], left_vectors[:, 0]),
        np.arctan2(right_vectors[:, 1], right_vectors[:, 0]),
        np.arctan2(center_vectors[:, 1], center_vectors[:, 0])
    ], axis=0)

    point_magnitude[lane_segment_idx] = np.linalg.norm(
        np.concatenate([
            left_vectors[:, :2],
            right_vectors[:, :2],
            center_vectors[:, :2]
        ], axis=0), ord=2, axis=-1
    )

    point_height[lane_segment_idx] = np.concatenate([
        left_vectors[:, 2],
        right_vectors[:, 2],
        center_vectors[:, 2]
    ], axis=0)

    left_type = point_types.index('DOUBLE_SOLID_WHITE')
    right_type = point_types.index('SOLID_WHITE')
    center_type = point_types.index('CENTERLINE')

    point_type[lane_segment_idx] = np.concatenate(
        [np.full((len(left_vectors),), left_type, dtype=np.uint8),
         np.full((len(right_vectors),), right_type, dtype=np.uint8),
         np.full((len(center_vectors),), center_type, dtype=np.uint8)], axis=0)

    point_side[lane_segment_idx] = np.concatenate(
        [np.full((len(left_vectors),), point_sides.index('LEFT'), dtype=np.uint8),
         np.full((len(right_vectors),), point_sides.index('RIGHT'), dtype=np.uint8),
         np.full((len(center_vectors),), point_sides.index('CENTER'), dtype=np.uint8)], axis=0)

crosswalk_segments = get_scenario_segments(vector_map, cross_walk_ids)
for crosswalk in crosswalk_segments:
    crosswalk = crosswalk[0]  # hard coding, only one exists in the crosswalk
    crosswalk_idx = polygon_ids.index(str(crosswalk.id))
    # capture the 2 edge (2 long edge)
    edge = crosswalk.polygon
    distance = np.sum((edge[1:, :] - edge[:-1, :]) ** 2, axis=1)
    top_two_index = np.argsort(distance)[-2:][::-1]

    edge1 = edge[[top_two_index[0], top_two_index[0] + 1], :]
    edge2 = edge[[top_two_index[1], top_two_index[1] + 1], :]
    edge1 = np.c_[edge1, np.zeros(edge1.shape[0])]
    edge2 = np.c_[edge2, np.zeros(edge2.shape[0])]

    start_position = (edge1[0] + edge2[0]) / 2
    end_position = (edge1[-1] + edge2[-1]) / 2
    polygon_position[crosswalk_idx] = start_position[:dim]
    polygon_position[crosswalk_idx + len(cross_walk_ids)] = end_position[:dim]
    polygon_orientation[crosswalk_idx] = np.arctan2((end_position - start_position)[1],
                                                    (end_position - start_position)[0])
    polygon_orientation[crosswalk_idx + len(cross_walk_ids)] = np.arctan2((start_position - end_position)[1],
                                                                          (start_position - end_position)[0])
    polygon_height[crosswalk_idx] = end_position[2] - start_position[2]
    polygon_height[crosswalk_idx + len(cross_walk_ids)] = start_position[2] - end_position[2]
    polygon_type[crosswalk_idx] = polygon_types.index('PEDESTRIAN')
    polygon_type[crosswalk_idx + len(cross_walk_ids)] = polygon_types.index('PEDESTRIAN')
    polygon_is_intersection[crosswalk_idx] = polygon_is_intersections.index(None)
    polygon_is_intersection[crosswalk_idx + len(cross_walk_ids)] = polygon_is_intersections.index(None)

    if side_to_directed_lineseg((edge1[0] + edge1[-1]) / 2, start_position, end_position) == 'LEFT':
        left_boundary = edge1
        right_boundary = edge2
    else:
        left_boundary = edge2
        right_boundary = edge1

    num_centerline_points = math.ceil(np.linalg.norm(end_position - start_position, ord=2) / 2.0) + 1
    centerline = compute_midpoint_line(left_ln_boundary=left_boundary,
                                       right_ln_boundary=right_boundary,
                                       num_interp_pts=int(num_centerline_points))[0].astype(np.float32)

    point_position[crosswalk_idx] = np.concatenate([left_boundary[:-1, :dim],
                                                    right_boundary[:-1, :dim],
                                                    centerline[:-1, :dim]], axis=0)
    point_position[crosswalk_idx + len(cross_walk_ids)] = np.concatenate(
        [np.flip(right_boundary, axis=0)[:-1, :dim],
         np.flip(left_boundary, axis=0)[:-1, :dim],
         np.flip(centerline, axis=0)[:-1, :dim]], axis=0)

    left_vectors = left_boundary[1:] - left_boundary[:-1]
    right_vectors = right_boundary[1:] - right_boundary[:-1]
    center_vectors = centerline[1:] - centerline[:-1]

    point_orientation[crosswalk_idx] = np.concatenate(
        [np.arctan2(left_vectors[:, 1], left_vectors[:, 0]),
         np.arctan2(right_vectors[:, 1], right_vectors[:, 0]),
         np.arctan2(center_vectors[:, 1], center_vectors[:, 0])], axis=0)
    point_orientation[crosswalk_idx + len(cross_walk_ids)] = np.concatenate(
        [np.arctan2(-np.flip(right_vectors, axis=0)[:, 1], -np.flip(right_vectors, axis=0)[:, 0]),
         np.arctan2(-np.flip(left_vectors, axis=0)[:, 1], -np.flip(left_vectors, axis=0)[:, 0]),
         np.arctan2(-np.flip(center_vectors, axis=0)[:, 1], -np.flip(center_vectors, axis=0)[:, 0])], axis=0)

    point_magnitude[crosswalk_idx] = np.linalg.norm(np.concatenate([left_vectors[:, :2],
                                                                    right_vectors[:, :2],
                                                                    center_vectors[:, :2]], axis=0), ord=2, axis=-1)
    point_magnitude[crosswalk_idx + len(cross_walk_ids)] = np.linalg.norm(
        np.concatenate([-np.flip(right_vectors, axis=0)[:, :2],
                        -np.flip(left_vectors, axis=0)[:, :2],
                        -np.flip(center_vectors, axis=0)[:, :2]], axis=0), ord=2, axis=-1)

    point_height[crosswalk_idx] = np.concatenate([left_vectors[:, 2], right_vectors[:, 2], center_vectors[:, 2]],
                                                 axis=0)
    point_height[crosswalk_idx + len(cross_walk_ids)] = np.concatenate(
        [-np.flip(right_vectors, axis=0)[:, 2],
         -np.flip(left_vectors, axis=0)[:, 2],
         -np.flip(center_vectors, axis=0)[:, 2]], axis=0)

    crosswalk_type = point_types.index('CROSSWALK')
    center_type = point_types.index('CENTERLINE')

    point_type[crosswalk_idx] = np.concatenate([
        np.full((len(left_vectors),), crosswalk_type, dtype=np.uint8),
        np.full((len(right_vectors),), crosswalk_type, dtype=np.uint8),
        np.full((len(center_vectors),), center_type, dtype=np.uint8)], axis=0)
    point_type[crosswalk_idx + len(cross_walk_ids)] = np.concatenate(
        [np.full((len(right_vectors),), crosswalk_type, dtype=np.uint8),
         np.full((len(left_vectors),), crosswalk_type, dtype=np.uint8),
         np.full((len(center_vectors),), center_type, dtype=np.uint8)], axis=0)

    point_side[crosswalk_idx] = np.concatenate(
        [np.full((len(left_vectors),), point_sides.index('LEFT'), dtype=np.uint8),
         np.full((len(right_vectors),), point_sides.index('RIGHT'), dtype=np.uint8),
         np.full((len(center_vectors),), point_sides.index('CENTER'), dtype=np.uint8)], axis=0)
    point_side[crosswalk_idx + len(cross_walk_ids)] = np.concatenate(
        [np.full((len(right_vectors),), point_sides.index('LEFT'), dtype=np.uint8),
         np.full((len(left_vectors),), point_sides.index('RIGHT'), dtype=np.uint8),
         np.full((len(center_vectors),), point_sides.index('CENTER'), dtype=np.uint8)], axis=0)

num_points = np.array([point.shape[0] for point in point_position], dtype=np.int64)
point_to_polygon_edge_index = np.stack(
    [np.arange(num_points.sum(), dtype=np.int64),
     np.repeat(np.arange(num_polygons, dtype=np.int64), num_points)], axis=0)

polygon_to_polygon_edge_index = []
polygon_to_polygon_type = []

for lane_segment in lane_segments:
    lane_segment_idx = polygon_ids.index(str(lane_segment.road_id) + '_' + str(lane_segment.lane_id))
    pred_inds = []
    for pred in lane_segment.entry_lanes:
        id = extract_values(pred)
        if id:
            pred_idx = polygon_ids.index(id)
            pred_inds.append(pred_idx)
    if len(pred_inds) != 0:
        polygon_to_polygon_edge_index.append(
            np.stack([np.array(pred_inds, dtype=np.int64),
                      np.full((len(pred_inds),), lane_segment_idx, dtype=np.int64)], axis=0))
        polygon_to_polygon_type.append(
            np.full((len(pred_inds),), polygon_to_polygon_types.index('PRED'), dtype=np.uint8))
    succ_inds = []
    for succ in lane_segment.exit_lanes:
        id = extract_values(succ)
        if id:
            succ_idx = polygon_ids.index(id)
            succ_inds.append(succ_idx)
    if len(succ_inds) != 0:
        polygon_to_polygon_edge_index.append(
            np.stack([np.array(succ_inds, dtype=np.int64),
                      np.full((len(succ_inds),), lane_segment_idx, dtype=np.int64)], axis=0))
        polygon_to_polygon_type.append(
            np.full((len(succ_inds),), polygon_to_polygon_types.index('SUCC'), dtype=np.uint8))
    # if lane_segment.left_neighbor_id is not None:
    #     left_idx = polygon_ids.index(lane_segment.left_neighbor_id)
    #     if left_idx is not None:
    #         polygon_to_polygon_edge_index.append(
    #             np.array([[left_idx], [lane_segment_idx]], dtype=np.int64))
    #         polygon_to_polygon_type.append(
    #             np.array([polygon_to_polygon_types.index('LEFT')], dtype=np.uint8))
    # if lane_segment.right_neighbor_id is not None:
    #     right_idx = polygon_ids.index(lane_segment.right_neighbor_id)
    #     if right_idx is not None:
    #         polygon_to_polygon_edge_index.append(
    #             np.array([[right_idx], [lane_segment_idx]], dtype=np.int64))
    #         polygon_to_polygon_type.append(
    #             np.array([polygon_to_polygon_types.index('RIGHT')], dtype=np.uint8))

if len(polygon_to_polygon_edge_index) != 0:
    polygon_to_polygon_edge_index = np.concatenate(polygon_to_polygon_edge_index, axis=1)
    polygon_to_polygon_type = np.concatenate(polygon_to_polygon_type, axis=0)
else:
    polygon_to_polygon_edge_index = np.array([[], []], dtype=np.int64)
    polygon_to_polygon_type = np.array([], dtype=np.uint8)

polygon_position = torch.tensor(polygon_position, dtype=torch.float32)
polygon_orientation = torch.tensor(polygon_orientation, dtype=torch.float32)
polygon_height = torch.tensor(polygon_height, dtype=torch.float32)
polygon_type = torch.tensor(polygon_type, dtype=torch.uint8)
polygon_is_intersection = torch.tensor(polygon_is_intersection, dtype=torch.uint8)

point_position = [torch.tensor(p, dtype=torch.float32) if p is not None else None for p in point_position]
point_orientation = [torch.tensor(p, dtype=torch.float32) if p is not None else None for p in point_orientation]
point_magnitude = [torch.tensor(p, dtype=torch.float32) if p is not None else None for p in point_magnitude]
point_height = [torch.tensor(p, dtype=torch.float32) if p is not None else None for p in point_height]
point_type = [torch.tensor(p, dtype=torch.uint8) if p is not None else None for p in point_type]
point_side = [torch.tensor(p, dtype=torch.float32) if p is not None else None for p in point_side]


map_data = {
    'map_polygon': {},
    'map_point': {},
    ('map_point', 'to', 'map_polygon'): {},
    ('map_polygon', 'to', 'map_polygon'): {},
}
map_data['map_polygon']['num_nodes'] = num_polygons
map_data['map_polygon']['position'] = polygon_position
map_data['map_polygon']['orientation'] = polygon_orientation
if dim == 3:
    map_data['map_polygon']['height'] = polygon_height
map_data['map_polygon']['type'] = polygon_type
map_data['map_polygon']['is_intersection'] = polygon_is_intersection
if len(num_points) == 0:
    map_data['map_point']['num_nodes'] = 0
    map_data['map_point']['position'] = torch.tensor([], dtype=torch.float)
    map_data['map_point']['orientation'] = torch.tensor([], dtype=torch.float)
    map_data['map_point']['magnitude'] = torch.tensor([], dtype=torch.float)
    if dim == 3:
        map_data['map_point']['height'] = torch.tensor([], dtype=torch.float)
    map_data['map_point']['type'] = torch.tensor([], dtype=torch.uint8)
    map_data['map_point']['side'] = torch.tensor([], dtype=torch.uint8)
else:
    map_data['map_point']['num_nodes'] = num_points.sum().item()
    map_data['map_point']['position'] = torch.cat(point_position, dim=0)
    map_data['map_point']['orientation'] = torch.cat(point_orientation, dim=0)
    map_data['map_point']['magnitude'] = torch.cat(point_magnitude, dim=0)
    if dim == 3:
        map_data['map_point']['height'] = torch.cat(point_height, dim=0)
    map_data['map_point']['type'] = torch.cat(point_type, dim=0)
    map_data['map_point']['side'] = torch.cat(point_side, dim=0)
map_data['map_point', 'to', 'map_polygon']['edge_index'] = point_to_polygon_edge_index
map_data['map_polygon', 'to', 'map_polygon']['edge_index'] = polygon_to_polygon_edge_index
map_data['map_polygon', 'to', 'map_polygon']['type'] = polygon_to_polygon_type
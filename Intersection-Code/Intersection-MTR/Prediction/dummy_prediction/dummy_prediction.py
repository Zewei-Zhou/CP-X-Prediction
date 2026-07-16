import pandas as pd
import numpy as np
import warnings
import os
import matplotlib.pyplot as plt
import math
from dummy_ttc_analysis_2 import detect_start_timestamp

def_collision_points = {4: [6.5, -10.0],
                        1: [20.0, -25.0],
                        3: [26, -16.1],
                        2: [14.0, -2.0]}


def dummy_path_prediction(prediction_scenario,
                          track_end_points,
                          track_start_points,
                          dummy_motion_phase):
    object_classes = prediction_scenario['object_type_class']
    trajs = prediction_scenario['trajs']
    current_time_index = prediction_scenario['current_time_index']

    # find the dummy
    dummy_index = object_classes.index('Dummy')
    dummy_his_traj = trajs[dummy_index, :current_time_index]

    start_point = dummy_his_traj[0, :]
    last_point = dummy_his_traj[-1, :]

    # static or dynamic, hard coding the threshold
    # assumption: the initial timestamp of the prediction run
    #             will not be assigned in the final static phase
    disp = math.sqrt((start_point[0] - last_point[0]) ** 2
                     + (start_point[1] - last_point[1]) ** 2)
    if disp < 0.75 and start_point[6] == 0:
        # use initial point position to determine
        min_dist = float('inf')
        nearest_start_position = None

        for position, directions in track_start_points.items():
            for direction, initial_points in directions.items():
                if initial_points:
                    for point in initial_points:
                        dist = math.sqrt((start_point[0] - point[0]) ** 2 +
                                         (start_point[1] - point[1]) ** 2)
                        if dist < min_dist:
                            min_dist = dist
                            nearest_start_position = [position, direction]

        path_end_point = \
            track_end_points[nearest_start_position[0]][nearest_start_position[1]]
        track_position = nearest_start_position[0]
        phase = dummy_motion_phase['initial_static']
    else:
        track_heading = {}
        dummy_path_heading = start_point[6]
        # dummy_path_heading = math.atan2(last_point[1] - start_point[1],
        #                              last_point[0] - start_point[0])

        min_heading_diff = float('inf')
        similar_track_position = None
        for position, directions in track_start_points.items():
            for direction, initial_points in directions.items():
                if initial_points:
                    # just select the first start point to calculate
                    initial_point = initial_points[0]
                    end_point = track_end_points[position][direction]
                    if position not in track_heading:
                        track_heading[position] = {}
                    track_heading[position].update(
                        {direction: math.atan2(end_point[1] - initial_point[1], end_point[0] - initial_point[0])})

                    heading_diff = math.fabs(track_heading[position][direction] - dummy_path_heading)
                    if heading_diff < min_heading_diff:
                        min_heading_diff = heading_diff
                        similar_track_position = [position, direction]
                        start_dist = math.sqrt((last_point[0] - initial_point[0]) ** 2 +
                                               (last_point[1] - initial_point[1]) ** 2)

        # hard coding to recheck the result
        if last_point[0] < 24 and last_point[1] > -20:
            if similar_track_position[0] in [1, 2]:
                similar_track_position[0] = 2

            if similar_track_position[0] in [3, 4]:
                similar_track_position[0] = 4

        path_end_point = \
            track_end_points[similar_track_position[0]][similar_track_position[1]]
        track_position = similar_track_position[0]

        # determine the static phase
        phase = None
        # end statics
        end_dist = math.sqrt((path_end_point[0] - last_point[0]) ** 2 +
                             (path_end_point[1] - last_point[1]) ** 2)
        if end_dist < 0.75:
            phase = dummy_motion_phase['end_static']
        elif disp < 0.75:
            # inital statics
            #todo: collision scenario
            phase = dummy_motion_phase['initial_static']

    return path_end_point, track_position, phase


def dummy_speed_prediction(prediction_scenario,
                           path_end_point,
                           track_position,
                           phase,
                           ttc_modes,
                           speed_mode_para):
    object_classes = prediction_scenario['object_type_class']
    trajs = prediction_scenario['trajs']

    current_time_index = prediction_scenario['current_time_index']
    pred_length = trajs.shape[1] - current_time_index - 1
    pred_dummy_traj = np.zeros((pred_length, 2))

    # find the dummy
    dummy_index = object_classes.index('Dummy')
    dummy_traj = trajs[dummy_index]
    dummy_his_traj = dummy_traj[:current_time_index + 1, :]
    dummy_fut_traj = dummy_traj[current_time_index + 1:, :2]
    dummy_subclass = prediction_scenario['object_type_subclass'][dummy_index]

    #todo: hard coding   transform the class
    if dummy_subclass == 'VRU_Adult_Using_Bicycle_Dummy':
        dummy_subclass = 'VRU_Adult_Using_Motorized_Bicycle_Dummy'

    speed_mode_para = speed_mode_para[dummy_subclass]
    ttc_modes = ttc_modes[dummy_subclass]

    # find the interaction vehicle based on the prior knowledge
    vehicle_index = [i for i, x in enumerate(object_classes) if x == 'Vehicle']
    if len(vehicle_index) > 1:
        if track_position == 3:
            vehicle_index = [
                index for index in vehicle_index
                if not ((trajs[index][trajs[index][:, -1] > 0][:, 1] < -25).any() or
                        (trajs[index][trajs[index][:, -1] > 0][:, 6] > 0.5).any())
            ]

        elif track_position == 4:
            vehicle_index = [
                index for index in vehicle_index
                if not ((trajs[index][trajs[index][:, -1] > 0][:, 1] > 0).any() or
                        (trajs[index][trajs[index][:, -1] > 0][:, 6] < -0.5).any())
            ]

    # if vehicle index still > 1 after filer, just select the first one
    vehicle_index = [i for i in vehicle_index if np.any(trajs[i][:current_time_index, -1] > 0)]  # remove nan traj

    # end static
    pred_dummy_trajs = []
    if phase == 4:
        pred_dummy_traj[:, :2] = dummy_traj[current_time_index, :2]
        pred_dummy_trajs += [pred_dummy_traj]

    if phase is None:
        # detect the start timestamp and end timestamp

        velocity = np.sqrt(dummy_his_traj[:, 7] ** 2 +
                           dummy_his_traj[:, 8] ** 2)
        start_timestamp = 0
        end_timestamp = len(velocity)

        if velocity[0] < 0.5:
            start_timestamp = detect_start_timestamp(velocity)
        else:
            index = np.where(velocity < 0.5)[0]
            if len(index) > 0:
                end_timestamp = index[0]

        if start_timestamp > 0:
            # acceleration trajectory
            # hard coding to filter the mode
            ref_velocity = None
            if start_timestamp < current_time_index - 25:
                ref_velocity = np.median(velocity[start_timestamp:])
            pred_dummy_trajs_temp = generate_whole_trajectory(speed_mode_para,
                                                              dummy_traj[start_timestamp, :2],
                                                              path_end_point,
                                                              ref_velocity,
                                                              current_time_index,
                                                              start_timestamp, pred_length)
            pred_dummy_trajs += pred_dummy_trajs_temp

        elif end_timestamp != len(velocity):
            # end static trajectory
            pred_dummy_traj[:, :2] = dummy_his_traj[end_timestamp, :2]
            pred_dummy_trajs += [pred_dummy_traj]
        else:
            med_v = np.median(velocity)
            fin_v = velocity[-1]

            # deceleration trajectory
            pred_dummy_trajs_temp = generate_seg_trajectory(speed_mode_para,
                                                            dummy_traj[current_time_index, :2],
                                                            path_end_point,
                                                            med_v,
                                                            current_time_index,
                                                            end_timestamp, pred_length)
            pred_dummy_trajs += pred_dummy_trajs_temp

        # todo: collision trajectory

    # initial static
    if phase == 0:
        if len(vehicle_index) == 0:
            pred_dummy_traj[:, :2] = dummy_traj[current_time_index, :2]
            pred_dummy_trajs += [pred_dummy_traj]
        else:
            # todo: to change the prediction source
            vehicle_traj = trajs[vehicle_index[0]]

            pred_vehicle_traj = vehicle_traj[current_time_index + 1:, :]

            # calculate the ttc
            # vehicle_velocity = np.sqrt(pred_vehicle_traj[:, 7] ** 2 +
            #                            pred_vehicle_traj[:, 8] ** 2)
            ttc_list = []
            for i in range(0, pred_length):
                ttc, disp = calculate_ttc(pred_vehicle_traj[i, :2],
                                          def_collision_points[track_position],
                                          pred_vehicle_traj[i, 7:9])
                ttc_list.append(ttc)
            # caclulate from the biggest ttc
            for j, ttc_mode in ttc_modes.items():
                start_timestamp = []
                for m, ttc in enumerate(ttc_list):
                    if ttc < 0 < ttc_mode:
                        continue
                    else:
                        if ttc < ttc_mode:
                            start_timestamp.append(m)

                if len(start_timestamp) == 0:
                    pred_dummy_traj[:, :2] = dummy_traj[current_time_index, :2]
                    pred_dummy_trajs += [pred_dummy_traj]
                    continue
                else:
                    # start_timestamp = - start_timestamp[0]
                    ref_velocity = None
                    pred_dummy_trajs_temp = generate_whole_trajectory(speed_mode_para,
                                                                      dummy_traj[current_time_index, :2],
                                                                      path_end_point,
                                                                      ref_velocity,
                                                                      current_time_index,
                                                                      - start_timestamp[0] - 1, pred_length)
                    pred_dummy_trajs += pred_dummy_trajs_temp

    return pred_dummy_trajs, dummy_fut_traj


def generate_whole_trajectory(speed_mode_para,
                              start_point, end_point,
                              ref_velocity,
                              current_time_index,
                              start_timestamp, pred_length):
    pred_trajs = []
    d_total = math.sqrt((start_point[0] - end_point[0]) ** 2 +
                        (start_point[1] - end_point[1]) ** 2)

    for mode in speed_mode_para.values():
        V_max, a, t_a = mode['V_max'], mode['a'], mode['t_a']

        d_acc = 0.5 * a * t_a ** 2
        d_cruise = d_total - 2 * d_acc

        # fliter the corner cases
        if d_cruise < 0:
            continue

        if ref_velocity is not None:
            if np.abs(ref_velocity - V_max) > 1:
                continue

        t_cruise = d_cruise / V_max
        total_timestamp = (2 * t_a + t_cruise) * 10
        timestamp_cruise = t_cruise * 10
        timestamp_a = t_a * 10
        timestamp = np.arange(0, total_timestamp)

        # Position and velocity calculation for each phase
        position = np.zeros_like(timestamp)

        accel_phase = timestamp <= timestamp_a
        position[accel_phase] = 0.5 * a * (timestamp[accel_phase] * 0.1) ** 2

        cruise_phase = (timestamp > timestamp_a) & (timestamp <= timestamp_a + timestamp_cruise)
        position[cruise_phase] = d_acc + V_max * (timestamp[cruise_phase] - timestamp_a) * 0.1

        decel_phase = timestamp > timestamp_a + timestamp_cruise
        decel_time = (timestamp[decel_phase] - (timestamp_a + timestamp_cruise)) * 0.1
        position[decel_phase] = d_acc + d_cruise + V_max * decel_time - 0.5 * a * decel_time ** 2

        # Normalize position to obtain the trajectory
        ratio = position / d_total
        x = start_point[0] + ratio * (end_point[0] - start_point[0])
        y = start_point[1] + ratio * (end_point[1] - start_point[1])

        trajectory = np.column_stack((x, y))

        # post process
        pred_traj = np.zeros((pred_length, 2))
        if start_timestamp >= 0:
            overlap_len = current_time_index - start_timestamp + 1
            cut_len = min(len(trajectory) - overlap_len, pred_length)
            temp = trajectory[overlap_len:overlap_len + cut_len, :]
            pred_traj[: cut_len, :] = \
                trajectory[overlap_len:overlap_len + cut_len, :]
            if cut_len < pred_length:
                last_point = trajectory[cut_len - 1, :]
                pred_traj[cut_len:pred_length, :] = last_point
        else:
            start_timestamp_abs = np.abs(start_timestamp + 1)
            extend_len = min(len(trajectory) + start_timestamp_abs, pred_length)
            pred_traj[start_timestamp_abs: extend_len, :] = trajectory[:extend_len - start_timestamp_abs, :]

            pred_traj[:start_timestamp_abs, :] = trajectory[0, :]
            if extend_len < pred_length:
                pred_traj[extend_len:, :] = trajectory[extend_len - start_timestamp_abs - 1, :]

        pred_trajs.append(pred_traj)

    return pred_trajs


def generate_seg_trajectory(speed_mode_para,
                            start_point, end_point,
                            med_v,
                            current_time_index,
                            start_timestamp, pred_length):
    pred_trajs = []
    d_total = math.sqrt((start_point[0] - end_point[0]) ** 2 +
                        (start_point[1] - end_point[1]) ** 2)

    for mode in speed_mode_para.values():
        V_max, a, t_a = mode['V_max'], mode['a'], mode['t_a']

        # hard coding to filter the mode
        if np.abs(med_v - V_max) > 1:
            continue

        d_dec = 0.5 * a * t_a ** 2
        if d_dec > d_total:
            t_dec = int(np.sqrt(2 * d_total / a))

            timestamp = np.arange(0, pred_length)
            position = np.zeros(pred_length)

            decel_phase = timestamp < t_dec * 10
            position[decel_phase] = \
                d_total - 0.5 * a * (t_dec - timestamp[decel_phase] * 0.1) ** 2

            position[t_dec * 10:] = position[t_dec * 10 - 1]
        else:
            d_cruise = d_total - d_dec
            if d_cruise > 0:
                t_cruise = d_cruise / V_max

                # t = np.linspace(0, t_cruise + t_a)
                timestamp = np.arange(0, pred_length)

                position = np.zeros_like(timestamp)

                cruise_phase = timestamp <= t_cruise * 10
                position[cruise_phase] = V_max * timestamp[cruise_phase] * 0.1

                decel_phase = timestamp > t_cruise * 10
                decel_time = timestamp[decel_phase] * 0.1 - t_cruise
                position[decel_phase] = d_cruise + V_max * decel_time - 0.5 * a * decel_time ** 2
            else:
                t_decel = np.sqrt(2 * d_total / a)
                timestamp = np.arange(0, t_decel)

                position = d_total - 0.5 * a * (t_decel - timestamp * 0.1) ** 2

        # Normalize position to obtain the trajectory
        ratio = position / d_total
        x = start_point[0] + ratio * (end_point[0] - start_point[0])
        y = start_point[1] + ratio * (end_point[1] - start_point[1])

        trajectory = np.column_stack((x, y))
        pred_trajs.append(trajectory)

    return pred_trajs


def calculate_ttc(traj1, conflict_point, v1):
    rel_pos1 = [conflict_point[0], conflict_point[1]] - traj1[:]
    rel_vel1 = v1
    norm_rel_vel_sq1 = np.linalg.norm(rel_vel1) ** 2

    ttc = np.dot(rel_pos1, rel_vel1) / (norm_rel_vel_sq1 + 1e-5)

    return ttc, np.linalg.norm(rel_pos1)

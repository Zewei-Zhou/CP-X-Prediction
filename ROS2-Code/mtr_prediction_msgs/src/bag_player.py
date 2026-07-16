"""Replay a ROS1 bag as ROS2 topics, remapping visualization_header_msgs/MarkerArrayHeader
to mtr_prediction_msgs/MarkerArrayHeader so node.py can subscribe with its native type."""
import sys
import time

import rclpy
from rclpy.node import Node
from rclpy.clock import Clock

from rosbags.highlevel import AnyReader
from pathlib import Path

from mtr_prediction_msgs.msg import MarkerArrayHeader
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import Header
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA
from builtin_interfaces.msg import Time, Duration


HEADER_TOPICS = {
    '/tracking/carxx/transformed_objects_header_box_score_label',
    '/tracking/carzzl/transformed_objects_header_box_score_label',
    '/tracking/nw/transformed_objects_header_box_score_label',
    '/tracking/se/transformed_objects_header_box_score_label',
}

MARKER_ARRAY_TOPICS_SUFFIXES = (
    '_det_box_score_label',
    '_objects_box_score_label',
)


def _to_time(sec_nsec):
    t = Time()
    t.sec = int(sec_nsec[0]) if isinstance(sec_nsec, tuple) else int(sec_nsec.sec)
    t.nanosec = int(sec_nsec[1]) if isinstance(sec_nsec, tuple) else int(sec_nsec.nanosec)
    return t


def _convert_header(src):
    h = Header()
    h.stamp.sec = int(src.stamp.sec)
    h.stamp.nanosec = int(src.stamp.nanosec)
    h.frame_id = src.frame_id
    return h


def _convert_marker(src):
    m = Marker()
    m.header = _convert_header(src.header)
    m.ns = src.ns
    m.id = int(src.id)
    m.type = int(src.type)
    m.action = int(src.action)
    m.pose.position.x = float(src.pose.position.x)
    m.pose.position.y = float(src.pose.position.y)
    m.pose.position.z = float(src.pose.position.z)
    m.pose.orientation.x = float(src.pose.orientation.x)
    m.pose.orientation.y = float(src.pose.orientation.y)
    m.pose.orientation.z = float(src.pose.orientation.z)
    m.pose.orientation.w = float(src.pose.orientation.w)
    m.scale.x = float(src.scale.x)
    m.scale.y = float(src.scale.y)
    m.scale.z = float(src.scale.z)
    m.color.r = float(src.color.r)
    m.color.g = float(src.color.g)
    m.color.b = float(src.color.b)
    m.color.a = float(src.color.a)
    m.lifetime.sec = int(src.lifetime.sec)
    m.lifetime.nanosec = int(src.lifetime.nanosec)
    m.frame_locked = bool(src.frame_locked)
    for p in src.points:
        pt = Point()
        pt.x = float(p.x); pt.y = float(p.y); pt.z = float(p.z)
        m.points.append(pt)
    for c in src.colors:
        col = ColorRGBA()
        col.r = float(c.r); col.g = float(c.g); col.b = float(c.b); col.a = float(c.a)
        m.colors.append(col)
    m.text = src.text
    m.mesh_resource = src.mesh_resource
    m.mesh_use_embedded_materials = bool(src.mesh_use_embedded_materials)
    return m


class BagPlayer(Node):
    def __init__(self, bag_path: str, rate: float = 1.0):
        super().__init__('bag_player')
        self.pubs = {}
        self.bag_path = Path(bag_path)
        self.rate = rate
        self.get_logger().info(f'Opening bag: {self.bag_path}')

    def _get_pub(self, topic: str, msg_type: str):
        if topic in self.pubs:
            return self.pubs[topic]
        if topic in HEADER_TOPICS:
            pub = self.create_publisher(MarkerArrayHeader, topic, 10)
        else:
            pub = self.create_publisher(MarkerArray, topic, 10)
        self.pubs[topic] = pub
        return pub

    def play(self):
        with AnyReader([self.bag_path]) as reader:
            connections = reader.connections
            self.get_logger().info(f'{len(connections)} topics in bag')
            for c in connections:
                self.get_logger().info(f'  {c.topic}  [{c.msgtype}]')
                # pre-create publisher
                self._get_pub(c.topic, c.msgtype)

            start_wall = time.time()
            start_bag = None

            for connection, timestamp, rawdata in reader.messages():
                if not rclpy.ok():
                    break
                msg = reader.deserialize(rawdata, connection.msgtype)
                topic = connection.topic

                if topic in HEADER_TOPICS:
                    out = MarkerArrayHeader()
                    out.header = _convert_header(msg.header)
                    out.markers = [_convert_marker(m) for m in msg.markers]
                elif connection.msgtype.endswith('MarkerArray'):
                    out = MarkerArray()
                    out.markers = [_convert_marker(m) for m in msg.markers]
                else:
                    continue

                # pace playback by bag timestamps
                if start_bag is None:
                    start_bag = timestamp
                elapsed_bag = (timestamp - start_bag) / 1e9 / self.rate
                elapsed_wall = time.time() - start_wall
                sleep = elapsed_bag - elapsed_wall
                if sleep > 0:
                    time.sleep(sleep)

                self.pubs[topic].publish(out)
            self.get_logger().info('Bag playback finished.')


def main():
    bag = sys.argv[1] if len(sys.argv) > 1 else '/data/robert/CP-X-Prediction/ROS2-Code/rosbag/output.bag'
    rate = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    rclpy.init()
    node = BagPlayer(bag, rate=rate)
    try:
        node.play()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

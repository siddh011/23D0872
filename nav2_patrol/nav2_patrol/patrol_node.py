
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped
from tf_transformations import quaternion_from_euler


class WaypointPatroller(Node):

    def __init__(self):
        super().__init__('waypoint_patroller')

        self.client = ActionClient(
            self,
            FollowWaypoints,
            '/follow_waypoints'
        )

        self.get_logger().info("Waiting for Nav2 action server...")
        self.client.wait_for_server()

        # Hardcoded waypoints (x, y, theta)
        self.waypoint_list = [
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (2.0, 2.0, 1.57)
        ]

        self.send_waypoints()

    def create_pose(self, x, y, theta):

        pose = PoseStamped()

        pose.header.frame_id = "map"
        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0

        q = quaternion_from_euler(0, 0, theta)

        pose.pose.orientation.x = q[0]
        pose.pose.orientation.y = q[1]
        pose.pose.orientation.z = q[2]
        pose.pose.orientation.w = q[3]

        return pose

    def send_waypoints(self):

        goal_msg = FollowWaypoints.Goal()

        for wp in self.waypoint_list:
            goal_msg.poses.append(
                self.create_pose(wp[0], wp[1], wp[2])
            )

        self.get_logger().info("Sending waypoints to Nav2...")

        self.send_goal_future = self.client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self.send_goal_future.add_done_callback(
            self.goal_response_callback
        )

    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected!")
            return

        self.get_logger().info("Goal accepted!")

        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(
            self.result_callback
        )

    def feedback_callback(self, feedback_msg):

        current_waypoint = feedback_msg.feedback.current_waypoint

        self.get_logger().info(
            f"Navigating to Waypoint {current_waypoint + 1}..."
        )

    def result_callback(self, future):

        result = future.result().result

        self.get_logger().info("All waypoints reached successfully!")
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    node = WaypointPatroller()
    rclpy.spin(node)


if __name__ == '__main__':
    main()


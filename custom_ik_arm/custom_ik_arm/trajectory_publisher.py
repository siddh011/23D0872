import rclpy
from rclpy.node import Node

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class TrajectoryPublisher(Node):

    def __init__(self):
        super().__init__('trajectory_publisher')

        self.publisher_ = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )

        self.timer = self.create_timer(2.0, self.publish_trajectory)

    def publish_trajectory(self):

        # Replace with your manually calculated IK angles (in radians)
        theta1 = 0.5
        theta2 = 0.8
        theta3 = -0.3

        traj = JointTrajectory()

        # Must match URDF joint names exactly
        traj.joint_names = [
            'joint1',
            'joint2',
            'joint3'
        ]

        point = JointTrajectoryPoint()
        point.positions = [theta1, theta2, theta3]
        point.velocities = [0.0, 0.0, 0.0]
        point.time_from_start = Duration(sec=3)

        traj.points.append(point)

        self.publisher_.publish(traj)

        self.get_logger().info(
            f'Published: {point.positions}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


class IKTrajectoryPublisher(Node):

    def __init__(self):
        super().__init__('ik_trajectory_publisher')

        self.publisher_ = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )

        self.timer = self.create_timer(2.0, self.publish_trajectory)

    def publish_trajectory(self):

        msg = JointTrajectory()

        msg.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_joint'
        ]

        point = JointTrajectoryPoint()

        point.positions = [
            0.54,
            -0.45,
            1.68,
            -1.23
        ]

        point.velocities = [0.0, 0.0, 0.0, 0.0]
        point.time_from_start.sec = 4

        msg.points.append(point)

        self.publisher_.publish(msg)

        self.get_logger().info("Publishing custom IK trajectory...")


def main(args=None):
    rclpy.init(args=args)
    node = IKTrajectoryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

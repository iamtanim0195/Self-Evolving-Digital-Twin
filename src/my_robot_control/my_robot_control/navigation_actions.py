import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class RobotActionController(Node):
    def __init__(self):
        super().__init__('robot_action_controller')
        # /cmd_vel টপিক পাবলিশ করার জন্য পাবলিশার তৈরি
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Robot Action Controller Node has been started!')

    def move_forward(self):
        msg = Twist()
        msg.linear.x = 0.5   # Positive velocity to move ahead
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Action: Moving Forward')

    def move_backward(self):
        msg = Twist()
        msg.linear.x = -0.5  # Negative velocity to reverse
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Action: Moving Backward')

    def turn_left(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 1.0  # Positive angular velocity rotates counter-clockwise
        self.publisher_.publish(msg)
        self.get_logger().info('Action: Turning Left')

    def turn_right(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = -1.0 # Negative angular velocity rotates clockwise
        self.publisher_.publish(msg)
        self.get_logger().info('Action: Turning Right')

    def stop_robot(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0  # Zero resets all motor speeds
        self.publisher_.publish(msg)
        self.get_logger().info('Action: Robot Stopped')

def main(args=None):
    rclpy.init(args=args)
    node = RobotActionController()
    
    try:
        # টেস্ট রান: গাড়িটি ৩ সেকেন্ড সামনে গিয়ে থেমে যাবে
        node.move_forward()
        time.sleep(3.0)
        node.stop_robot()
    except KeyboardInterrupt:
        node.stop_robot()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
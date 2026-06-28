import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class RobotActionController(Node):
    def __init__(self):
        super().__init__('robot_action_controller')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Robot Continuous Action Controller Node has been started!')

    def drive_robot(self, linear_x, angular_z, duration):
        """নির্দিষ্ট সময় ধরে লুপ আকারে অনবরত সিগন্যাল পাঠানোর মেথড"""
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        
        start_time = time.time()
        # নির্দিষ্ট duration শেষ না হওয়া পর্যন্ত প্রতি ০.১ সেকেন্ড পর পর সিগন্যাল পাঠাবে
        while (time.time() - start_time) < duration:
            self.publisher_.publish(msg)
            time.sleep(0.1)
            
        # সময় শেষ হলে গাড়ি থামিয়ে দেবে
        self.stop_robot()

    def stop_robot(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Action: Robot Stopped')

def main(args=None):
    rclpy.init(args=args)
    node = RobotActionController()
    
    try:
        # ৩ সেকেন্ডের জন্য ১.০ স্পিডে সামনে ড্রাইভ করবে (স্পিড একটু বাড়িয়ে দেওয়া হয়েছে)
        node.get_logger().info('Action: Moving Forward continuously for 3 seconds...')
        node.drive_robot(linear_x=1.0, angular_z=0.0, duration=3.0)
        
    except KeyboardInterrupt:
        node.stop_robot()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
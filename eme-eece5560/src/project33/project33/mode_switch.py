import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class ModeSwitch(Node):
    def __init__(self):
        super().__init__('mode_switch')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription_mode = self.create_subscription(
            String, 'mode', self.fsm_callback, 10)
        self.subscription_auto = self.create_subscription(
            Twist, 'control_input', self.auto_callback, 10)
        self.subscription_teleop = self.create_subscription(
            Twist, 'teleop', self.teleop_callback, 10)
        self.current_mode = 's'

    def stop(self):
        t = Twist()
        t.linear.x = 0.0
        t.linear.y = 0.0
        t.linear.z = 0.0
        t.angular.x = 0.0
        t.angular.y = 0.0
        t.angular.z = 0.0
        return t

    def auto_callback(self, msg):
        if self.current_mode == 'a':
            self.publisher_.publish(msg)

    def teleop_callback(self, msg):
        if self.current_mode == 't':
            self.publisher_.publish(msg)

# for this new project's fsm, we don't need latch or unlatch,
# so it would be pretty simple and straightforward, just three states
# switching to each other.
    def fsm_callback(self, msg):
        self.get_logger().info(f'Mode Requested:{msg.data}')
        mode_req = msg.data
        self.current_mode = mode_req
        if self.current_mode == 's':
            self.publisher_.publish(self.stop())
        self.get_logger().info(f'Selected mode: {self.current_mode}')


def main(args=None):
    rclpy.init()
    MSW = ModeSwitch()
    rclpy.spin(MSW)
    MSW.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

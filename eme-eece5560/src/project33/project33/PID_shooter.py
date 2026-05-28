import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist



class PID(Node):

    def __init__(self):
        super().__init__('pid_controller')
        #self.declare_parameter('fkp', '0.1')
        #self.declare_parameter('fki', '0')
        #self.declare_parameter('fkd', '0')
        #self.declare_parameter('tkp', '0.1')
        #self.declare_parameter('tki', '0')
        #self.declare_parameter('tkd', '0')
        self.subscription = self.create_subscription(
            Float32MultiArray, 'error', self.listener_callback, 10)
        
        self.publisher_ = self.create_publisher(Twist, 'control_input', 10)

        self.size_error_sum = 0
        self.size_error_last = 0
        self.fkp = 0.0025
        self.fki = 0
#.0001
        self.fkd = 0.0025


        self.angle_error_sum = 0
        self.angle_error_last = 0
        self.tkp = 0.0005
        self.tki = 0
        self.tkd = 0.0005
        # these params need to be tuned later

    def listener_callback(self, msg):
        size_error = msg.data[0]
        angle_error = msg.data[1]
        self.size_error_sum += size_error
        self.angle_error_sum += angle_error

        if self.size_error_sum > 100:
            # This step is crucial since we 're doing auto with teleop, it may go to integral windup.
            self.size_error_sum = 100
        elif self.size_error_sum < -100:
            self.size_error_sum = -100
        if self.angle_error_sum > 800:
            self.angle_error_sum = 800
        elif self.angle_error_sum < -800:
            self.angle_error_sum = -800

        size_error_diff = size_error-self.size_error_last
        angle_error_diff = angle_error-self.angle_error_last
        out = Twist()

        #fkp = float(self.get_parameter('fkp').get_parameter_value().string_value)
        #fki = float(self.get_parameter('fki').get_parameter_value().string_value)
        #fkd = float(self.get_parameter('fkd').get_parameter_value().string_value)
        #tkp = float(self.get_parameter('tkp').get_parameter_value().string_value)
        #tki = float(self.get_parameter('tki').get_parameter_value().value)
        #tkd = float(self.get_parameter('tkd').get_parameter_value().string_value)
        #self.get_logger().info(f'{type(fkp)}')
        out.linear.x = self.fkp * size_error + self.fki * \
            self.size_error_sum + self.fkd * size_error_diff
        out.angular.z = self.tkp * angle_error + self.tki * \
            self.angle_error_sum + self.tkd*angle_error_diff
#        if out.linear.x < -50
#            out.linear.x = 50
#        elif out.linear.x > 50
#            out.linear.x = 50
#        if out.angular.z < -10
#            out.angular.z = -10
#        elif out.angular.z > 10
#            out.angular.z = 10

        self.publisher_.publish(out)
        self.size_error_last = size_error
        self.angle_error_last = angle_error


def main(args=None):
    rclpy.init()
    PIDC = PID()
    rclpy.spin(PIDC)
    PIDC.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

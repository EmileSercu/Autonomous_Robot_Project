import rclpy
from rclpy.node import Node
import numpy as np
import cv2
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray, Bool
from cv_bridge import CvBridge


class TargetFinder(Node):
    def __init__(self):
        super().__init__('target_finder')

        self.target_publisher = self.create_publisher(
            Bool, 'target', 10)

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image, 'filtered', self.sub_callback, 10)

        # we can edit this value to make it shoot only when the robot is close enough
        self.ball_surface_area = 100.0

    def sub_callback(self, msg):
        cv_img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        img_gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(img_gray, 1, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        target = any(cv2.contourArea(contour) >=
                     self.ball_surface_area for contour in contours)

        msg = Bool()
        msg.data = target
        self.target_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    target_finder = TargetFinder()
    rclpy.spin(target_finder)
    target_finder.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

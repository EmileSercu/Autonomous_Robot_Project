import rclpy
from rclpy.node import Node
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class PingPongFilter(Node):
    def __init__(self):
        super().__init__('ping_pong_filter')
        self.publisher = self.create_publisher(Image,'filtered',10)
        self.declare_parameter('color', 'green')
        self.subscription = self.create_subscription(Image,'image_raw',self.filter_callback,10)
        self.bridge = CvBridge()

    def filter_callback(self, msg):
        color = self.get_parameter('color').get_parameter_value().string_value
        if color == 'blue':
            lower_bound = (97,235,110)
            upper_bound = (123,255,255)
        elif color == 'pink':
            lower_bound = [95,40,160]
            upper_bound = [180,230,255]
        elif color == 'yellow':
            lower_bound = [24,50,99]
            upper_bound = [50,255,255]
        elif color == 'green':
            lower_bound = [40,67,97]
            upper_bound = [80,255,255]
        
        
        cv_img = self.bridge.imgmsg_to_cv2(msg,'bgr8')
        img_hsv = cv2.cvtColor(cv_img,cv2.COLOR_BGR2HSV)
        lower = np.array(lower_bound, dtype=np.uint8)
        upper = np.array(upper_bound, dtype=np.uint8)
        img_filtered = cv2.inRange(img_hsv, lower, upper)
        erosion_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
        img_erode = cv2.erode(img_filtered,erosion_kernel)
        dilation_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
        img_dilate = cv2.dilate(img_erode,dilation_kernel)
        
        output = cv2.bitwise_and(cv_img,cv_img,mask=img_dilate)
        img_out = self.bridge.cv2_to_imgmsg(output,'bgr8')
        self.publisher.publish(img_out)

def main(args=None):
    rclpy.init(args=args)
    ping_pong_filter = PingPongFilter()
    rclpy.spin(ping_pong_filter)
    ping_pong_filter.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

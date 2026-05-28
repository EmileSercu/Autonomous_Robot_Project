import rclpy
from rclpy.node import Node
import numpy as np
import cv2
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge
from std_srvs.srv import SetBool

class ErrorFinder(Node):
    def __init__(self):
        super().__init__('error_finder')
        self.subscription = self.create_subscription(Image,'filtered',self.sub_callback,10)
        self.errorpublisher = self.create_publisher(Float32MultiArray, 'error',10)
        self.bridge = CvBridge()
        self.cli=self.create_client(SetBool, 'ready')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting')
        self.req = SetBool.Request()
        self.i = 0

    def sub_callback(self, msg):
        cv_img = self.bridge.imgmsg_to_cv2(msg,'bgr8')
        height, width, _ = cv_img.shape
        img_gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(img_gray, 1, 255, cv2.THRESH_BINARY)
        num, _, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity = 8, ltype = cv2.CV_32S)
        msg = Float32MultiArray()
        if num == 1: 
            self.get_logger().info('No detected images')
            msg.data = [0.0, 0.0]
            self.errorpublisher.publish(msg)
            return
        elif num == 2:
            hcenter = int(round(centroids[1, 0]))
            p_count = int(stats[1,2])
        elif num > 2:
            areas = stats[1:, 4]
            
            largest_id = 1 + np.argmax(areas)
            p_count = int(stats[largest_id, 2])
            hcenter = int(round(centroids[largest_id, 0]))

        # modified from lab 3.2 to get the error based on the size comparision of horizontal pixels to reference
        # and horizontal center of object to middle line
        size_error = 400 / 600 * height - p_count
        # modified to match the height, since the car might approach the 2d object at different angle
        angle_error =  hcenter - 0.5 * width
        if self.i < 200:
            if size_error < 50 and size_error > -50 and angle_error > -50 and angle_error < 50:
                self.i += 1
            else: 
                self.i = 0
        elif self.i == 200:
            self.req.data = True
        msg.data = [size_error,angle_error]
        self.errorpublisher.publish(msg)
        return self.cli.call_async(self.req)

            

def main(args=None):
    rclpy.init(args=args)
    error_finder = ErrorFinder()
    rclpy.spin(error_finder)
    error_finder.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

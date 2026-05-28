import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ModeInput(Node):
    def __init__(self):
        super().__init__('mode_console')
        self.pub = self.create_publisher(String, 'mode', 10)
        self.timer = self.create_timer(0.1, self.input_callback)

    def input_callback(self):
        cmd = input(
            "mode [s=Stop, a=Auto, t=Teleop, q=quit]: ").strip().lower()[:1]
        if cmd == 's':
            self.pub.publish(String(data='s'))
        elif cmd == 'a':
            self.pub.publish(String(data='a'))
        elif cmd == 't':
            self.pub.publish(String(data='t'))


def main():
    rclpy.init()
    minput = ModeInput()
    rclpy.spin(minput)
    minput.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

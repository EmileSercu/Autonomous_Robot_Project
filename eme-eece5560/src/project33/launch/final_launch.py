from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess


def generate_launch_description():

    return LaunchDescription([
        Node(
            package='project33',
            executable='center_finder_shooter',
            name='center_finder_shooter',
	        remappings=[
	            ('filtered','abot_06/camera_node/filtered')
            ]
        ),
        Node(
            package='project33',
            executable='mode_switch_shooter',
            name='mode_switch_shooter',
    	    remappings=[
		        ('cmd_vel','abot_06/abot/cmd_vel')
	        ]
        ),
        Node(
            package='project33',
            executable='PID_shooter',
            name='PID_shooter',
        ),
        Node(
            package='project33',
            executable='ping_pong_filter',
	    namespace='/abot_06/camera_node',
            name='ping_pong_filter',
        ),
        Node(
            package='camera_ros',
            executable='camera_node',
            namespace='abot_06',
            name='camera_node',
        ),
        Node(
            package='simple_abot_interface',
            executable='simple_abot_interface',
            namespace='abot_06',
            name='simple_abot_interface',
        ),
        # ExecuteProcess(
        #      cmd=[
        #         'ros2',
        #         'run',
        #         'teleop_twist_keyboard',
        #         'teleop_twist_keyboard',
        #         '--ros-args',
        #         '--remap',
        #         'cmd_vel:=teleop'
        #     ]
        # )
        
    ])

# ros2 run turtlesim turtle_teleop_key --ros-args -r /turtle1/cmd_vel:=drive
# change teleop key to not the one in the turtlesim package # teleop twist something
# ros2 run project33 mode_input

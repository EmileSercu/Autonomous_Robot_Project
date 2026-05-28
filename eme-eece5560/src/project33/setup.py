import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'project33'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        (os.path.join('share', package_name), ['package.xml']),
        # includes all launchfiles
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*_launch.py')),
        # open image
        ('share/' + package_name + '/images', ['images/image_blue_0.png']),
        ('share/' + package_name + '/images', ['images/image_pink_0.png']),
        ('share/' + package_name + '/images', ['images/apple.png']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='emile',
    maintainer_email='emile@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'center_finder = project33.center_finder:main',
            'center_finder_shooter = project33.center_finder_shooter:main',
            'mode_input = project33.mode_input:main',
            'mode_switch = project33.mode_switch:main',
            'mode_switch_shooter = project33.mode_switch_shooter:main',
            'PID = project33.PID:main',
            'PID_shooter = project33.PID_shooter:main',
            'target_finder = project33.target_finder:main',
            'ping_pong_filter = project33.ping_pong_filter:main'
        ],
    },
)

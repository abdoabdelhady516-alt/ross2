import os
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    xacro_file = os.path.expanduser('~/ros2_work/my_robot.urdf.xacro')

    # بنحوّل الـ xacro لـ URDF وبنبعته كنص عادي (str)
    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)

    return LaunchDescription([
        # بيقرا الـ URDF وينشر مكان كل جزء
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description}]),
        # نافذة الـ sliders بتاعة العجلات
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui'),
        # الـ RViz
        Node(package='rviz2', executable='rviz2'),
    ])

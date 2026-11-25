import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    xacro_file = os.path.expanduser('~/ros2_work/my_robot.urdf.xacro')
    bridge_file = os.path.expanduser('~/ros2_work/bridge.yaml')
    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)

    # 1) يفتح Gazebo بعالم فاضي (-r يعني شغّل الفيزياء على طول)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])
        ),
        launch_arguments={'gz_args': '-r -v 3 empty.sdf'}.items(),
    )

    # 2) ينشر الـ URDF على topic اسمه /robot_description
    rsp = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
    )

    # 3) يحط العربية جوه Gazebo (بنستنى 15 ثانية عشان Gazebo يكون فتح)
    spawn = TimerAction(period=15.0, actions=[
        Node(package='ros_gz_sim', executable='create',
             arguments=['-topic', 'robot_description', '-name', 'my_robot', '-z', '0.1'],
             output='screen'),
    ])

    # 4) الـ bridge: بيوصّل topics بين ROS وGazebo (الإعدادات في bridge.yaml)
    bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge',
        parameters=[{'config_file': bridge_file}],
        output='screen',
    )

    return LaunchDescription([gazebo, rsp, spawn, bridge])

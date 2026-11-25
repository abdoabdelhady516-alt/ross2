# ross2

A ROS 2 simulation workspace for a four-wheel skid-steer robot. It includes the robot model (URDF/xacro), a Gazebo launch setup with a ROS-Gazebo bridge, an RViz viewer, a saved occupancy map, and a small Nav2 script that sends the robot to a goal.

## Contents

| File | Purpose |
| --- | --- |
| `my_robot.urdf.xacro` | Main robot description. Dimensions and masses are xacro properties at the top of the file. |
| `my_robot_gazebo.xacro` | Gazebo settings: wheel friction and the DiffDrive plugin (`/cmd_vel` in, odometry and TF out). Included by the main xacro. |
| `my_robot.urdf` | Plain URDF version of the robot. |
| `gazebo_robot.launch.py` | Starts Gazebo, robot_state_publisher, spawns the robot and runs the ROS-Gazebo bridge. |
| `view_robot.launch.py` | Opens RViz with robot_state_publisher and the joint_state_publisher GUI (wheel sliders). |
| `bridge.yaml` | Topic bridge config between ROS 2 and Gazebo. |
| `my_map.pgm`, `my_map.yaml` | Saved map (112 x 103 px, 0.05 m/px) for Nav2. |
| `goal.py` | Sends a navigation goal to Nav2 and prints the remaining distance. |

## Robot

- Chassis: 0.40 x 0.20 x 0.05 m, 2.0 kg, with a top deck.
- Drive: four wheels (radius 0.05 m, width 0.04 m, 0.25 kg each), skid-steer, driven as a differential pair per side.
- Frames: `base_footprint` -> `base_link`, plus a `camera_optical_frame` with the orientation ROS expects for camera images.
- Modeled parts: RPLidar mast and lidar, camera, ToF sensor, IMU, battery, STM32 board, Orange Pi board, 4G antenna, GNSS antenna.

The sensor and board links are visual and inertial models only. The Gazebo file does not add simulated sensor plugins yet, so the bridge carries no lidar, camera or IMU topics.

## Bridged topics

| ROS topic | Type | Direction |
| --- | --- | --- |
| `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo to ROS |
| `/cmd_vel` | `geometry_msgs/msg/Twist` | ROS to Gazebo |
| `/odom` | `nav_msgs/msg/Odometry` | Gazebo to ROS |
| `/tf` | `tf2_msgs/msg/TFMessage` | Gazebo to ROS |

## Requirements

- ROS 2 with `xacro`, `robot_state_publisher`, `joint_state_publisher_gui`, `rviz2`
- Gazebo with `ros_gz_sim` and `ros_gz_bridge`
- Nav2 with `nav2_simple_commander` (only for `goal.py`)

## Setup

The launch files read the robot files from `~/ros2_work/`. Copy the repo contents there:

```bash
git clone https://github.com/abdoabdelhady516-alt/ross2.git ~/ros2_work
cd ~/ros2_work
source /opt/ros/<distro>/setup.bash
```

## Usage

View the robot in RViz:

```bash
ros2 launch ~/ros2_work/view_robot.launch.py
```

Run it in Gazebo (the robot spawns after about 15 seconds):

```bash
ros2 launch ~/ros2_work/gazebo_robot.launch.py
```

Drive it manually:

```bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2}, angular: {z: 0.0}}"
```

Send a navigation goal (Nav2 must already be running with `my_map.yaml`):

```bash
python3 goal.py 1.0 0.5          # go to x=1.0, y=0.5 in the map frame
python3 goal.py 1.0 0.5 --init   # also set the initial pose to (-2.0, -0.5) first
```

If no coordinates are given, the goal defaults to (1.0, 0.5).

## Notes

- Comments inside the launch and xacro files are written in Arabic.
- Change the robot size and weight in the properties at the top of `my_robot.urdf.xacro`.

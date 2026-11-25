import sys
import math
import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator


def make_pose(nav, x, y, yaw=0.0):
    p = PoseStamped()
    p.header.frame_id = 'map'
    p.header.stamp = nav.get_clock().now().to_msg()
    p.pose.position.x = x
    p.pose.position.y = y
    p.pose.orientation.z = math.sin(yaw / 2)
    p.pose.orientation.w = math.cos(yaw / 2)
    return p


args = [a for a in sys.argv[1:] if not a.startswith('--')]
x = float(args[0]) if len(args) > 0 else 1.0
y = float(args[1]) if len(args) > 1 else 0.5

rclpy.init()
nav = BasicNavigator()

if '--init' in sys.argv:
    nav.setInitialPose(make_pose(nav, -2.0, -0.5))

nav.waitUntilNav2Active()
nav.goToPose(make_pose(nav, x, y))

while not nav.isTaskComplete():
    fb = nav.getFeedback()
    if fb:
        print('remaining:', fb.distance_remaining)

print(nav.getResult())

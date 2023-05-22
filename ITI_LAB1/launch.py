from launch import LaunchDescription
from launch_ros.actions import Node
from geometry_msgs.msg import Twist

def generate_launch_description():
    ob = LaunchDescription()

    pub_node = Node(
        package='ITI_LAB1',
        executable='node1'
    )

    sub_node = Node(
        package='turtlesim',
        executable='turtlesim_node'
    )

    ob.add_action(pub_node)
    ob.add_action(sub_node)
    return ob



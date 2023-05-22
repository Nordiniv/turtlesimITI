#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int16, Bool

class my_node(Node):
    def __init__(self):
        super().__init__(node_name="number_counter")
        print("init_node")
        self.create_subscription(String,"str_topic",self.sub_call,10)
        self.pub_obj=self.create_publisher(Int16,"number",10)
        self.pub_obj=self.create_publisher(Bool,"reset_flag",10)


    def sub_call(self,x):
        print(x.data)


def main(args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)
    rclpy.shutdown()

main()

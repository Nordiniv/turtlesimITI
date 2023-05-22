#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int16, Bool

counter = 0
class my_node(Node):
    def __init__(self):
        super().__init__(node_name="str_publisher")
        self.create_timer(0.5,self.timer_call)
        self.pub_obj=self.create_publisher(String,"str_topic",10)
        self.create_subscription(Int16,"number",self.count,10)
        self.create_subscription(Bool,"reset_flag",self.reset,10)
        print("init_node")

    def timer_call(self):
        msg=String()
        msg.data= "NORDIN is publish ,{}".format(counter)
        self.pub_obj.publish(msg)

    def count(self, x):
        global counter
        counter = x


    def reset(self):
        global counter
        counter = 0

def main(args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)
    rclpy.shutdown()

main()

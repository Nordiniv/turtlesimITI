#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from numpy import arctan2, abs, pi, tanh
from numpy.random import randint
from turtlesim.srv import Spawn,Kill
#import clear to clear the background

#Make the turtle move to point (3, 7)


class my_node(Node):

    def __init__(self):
        super().__init__(node_name="turtle_move")
        print("init_node")
        global tx, ty
        self.pub_obj=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.sub_obj=self.create_subscription(Pose,"/turtle1/pose",self.twist_call,10)

        self.client = self.create_client(Spawn, 'spawn')
        self.kill_client = self.create_client(Kill, 'kill')
        self.clr_obj = self.create_client(Empty, 'clear')
        tx, ty = float(randint(1, 11)), float(randint(1, 11))
        self.spawn(tx, ty, float(randint(-pi, pi)), 'KillMe')

    def twist_call(self, msg):
        global tx, ty
        self.spawn(tx, ty, float(randint(-pi, pi)), 'KillMe')
        
        x = msg.x
        y = msg.y
        theta = msg.theta
        msg = Twist()
        msg.linear.x = 2.0
        
        z = tanh((lambda x, y: (arctan2((ty-y),(tx-x)) - theta))(x, y))*1.5*pi
        msg.angular.z = z if -pi < z < pi else z%(2*pi)
        print(msg.angular.z - theta, 3 - x)

        if not(tx - 0.1 < x < tx + 0.1 and ty - 0.1 < y < ty + 0.1):
            self.pub_obj.publish(msg)
        else:
            tx, ty = float(randint(1, 11)), float(randint(1, 11))
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.pub_obj.publish(msg)
            self.kill()
            self.clear()

        self.get_logger().info("x: %f, y: %f, theta: %f" % (x, y, msg.angular.z))


    def clear(self):
        self.clr_obj.wait_for_service()
        request = Empty.Request()
        future = self.clr_obj.call_async(request)

    def kill(self):
        self.kill_client.wait_for_service()
        request = Kill.Request()
        request.name = 'KillMe'
        future = self.kill_client.call_async(request)

    def spawn(self, x, y, theta, name):
        while not self.client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info('service not available, waiting again...')
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = name
        future = self.client.call_async(request)


def main(args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)
    rclpy.shutdown()

main()

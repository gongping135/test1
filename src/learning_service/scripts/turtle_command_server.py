#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将执行/turtle_command服务，服务数据类型std_srvs/Trigger

import rospy
import sys
import _thread as thread ,time
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse

pubCommand = False;
turtle_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)  #创建名为/turtle1/cmd_vel,发送Twist信息的发布者

def command_thread():	
	while True:
		if pubCommand:     #如果为真，则发送信息Twist让海龟运动
			vel_msg = Twist()
			vel_msg.linear.x = 0.5
			vel_msg.angular.z = 0.2
			turtle_vel_pub.publish(vel_msg)
			
		time.sleep(0.1)

def commandCallback(req):         #回调函数，当有请求时，会进入该函数进行操作，取反pubCommand
	global pubCommand
	pubCommand = bool(1-pubCommand)

	# 显示请求数据
	rospy.loginfo("Publish turtle velocity command![%d]", pubCommand)

	# 反馈数据
	return TriggerResponse(1, "Change turtle command state!")

def turtle_command_server():
	# ROS节点初始化
    rospy.init_node('turtle_command_server')

	# 创建一个名为/turtle_command，反馈信息类型为Trigger的server，注册回调函数commandCallback
    s = rospy.Service('/turtle_command', Trigger, commandCallback)

	# 循环等待回调函数
    print("Ready to receive turtle command.")

    thread.start_new_thread(command_thread, ())   #进行一个新的线程，可以理解为不会影响主程序执行的中断，此时command_thread和主程序一起执行
    rospy.spin()			           #阻塞函数，rospy.spin()的作用就是让节点保持运行状态，等待并处理回调。rospy.spin()内部实际上是一个无限循环，它会不断检查						   #是否有新的ROS消息到达或其他事件，然后调用相应的回调函数

if __name__ == "__main__":
    turtle_command_server()

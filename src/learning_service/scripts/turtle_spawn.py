#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将请求/spawn服务，服务数据类型turtlesim::Spawn

import sys
import rospy
from turtlesim.srv import Spawn

def turtle_spawn():
	# ROS节点初始化
    rospy.init_node('turtle_spawn')

	# 发现/spawn服务后，创建一个服务客户端，连接名为/spawn的service
    rospy.wait_for_service('/spawn')   #一直等待，直到连接成功
    try:
        add_turtle = rospy.ServiceProxy('/spawn', Spawn)  

		# 请求服务调用，输入请求数据
        response = add_turtle(2.0, 2.0, 0.0, "turtle2")  #add_turtle会向spawn这个服务这发送请求和所需数据，直到其响应
        return response.name
    except rospy.ServiceException as e:
        print ("Service call failed: %s"%e)

if __name__ == "__main__":
	#服务调用并显示调用结果
    print ("Spwan turtle successfully [name:%s]" %(turtle_spawn()))



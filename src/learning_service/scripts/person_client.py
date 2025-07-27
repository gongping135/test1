#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将请求/show_person服务，服务数据类型learning_service::Person

import sys
import rospy
from learning_service.srv import Person, PersonRequest

def person_client():
	# ROS节点初始化
    rospy.init_node('person_client')

	# 等待发现/spawn服务
    rospy.wait_for_service('/show_person')
    try:
    	#创建一个服务客户端，连接名为/show_person，传递消息类型为Person的service
        person_client = rospy.ServiceProxy('/show_person', Person)

		# 请求服务调用，输入请求数据,每次调用该节点会请求一次
        response = person_client("Tom", 20, PersonRequest.male)
        return response.result
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

if __name__ == "__main__":
	#服务调用并显示调用结果
    print("Show person result : %s" %(person_client()))



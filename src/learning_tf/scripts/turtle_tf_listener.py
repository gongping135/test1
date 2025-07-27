#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将请求/show_person服务，服务数据类型learning_service::Person

import roslib
roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import geometry_msgs.msg  #几何消息类型
import turtlesim.srv      #tutrlesim消息接口

if __name__ == '__main__':
    rospy.init_node('turtle_tf_listener')     #初始化节点

    listener = tf.TransformListener()        #创建TF监听器

    rospy.wait_for_service('spawn')          #等待服务可用
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)   #创建客户端
    spawner(4, 2, 0, 'turtle2')             #发送服务请求，在相应位置创建第二个海龟

    turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)
    #创建速度发布者，
    rate = rospy.Rate(10.0)                 #循环频率
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/turtle2', '/turtle1', rospy.Time(0))
            #获取turtle1相对于turtle2的相对位置,trans为平面位置（xyz），rot为旋转位置
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        angular = 4 * math.atan2(trans[1], trans[0])                #计算转向角速度
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)     #计算前进线速度
        cmd = geometry_msgs.msg.Twist()                             #创建消息变量
        cmd.linear.x = linear					      #线速度
        cmd.angular.z = angular				      #角速度
        turtle_vel.publish(cmd)				      #发送

        rate.sleep() 						      #等待



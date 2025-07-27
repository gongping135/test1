#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将请求/show_person服务，服务数据类型learning_service::Person

import roslib
roslib.load_manifest('learning_tf')
import rospy

import tf     #TF库
import turtlesim.msg    #turtlesim的消息类型

def handle_turtle_pose(msg, turtlename):  #坐标变换广播函数
    br = tf.TransformBroadcaster()        #创建TF广播变量
    br.sendTransform((msg.x, msg.y, 0),   #子坐标系相对于父坐标系的位置偏移，第三个=0表示仅在平面上偏移
                     tf.transformations.quaternion_from_euler(0, 0, msg.theta),
                     #表示相对于父坐标系的旋转，三个参数分别为
    		      #roll: 绕 x 轴旋转 (本例为 0)
    		      #pitch: 绕 y 轴旋转 (本例为 0)
    		      #yaw: 绕 z 轴旋转 (本例为 msg.theta)
                     rospy.Time.now(),         #时间戳，表示变换发生的时间
                     turtlename,		 #子坐标系
                     "world")			 #父坐标系	

if __name__ == '__main__':
    
    rospy.init_node('turtle_tf_broadcaster', anonymous=True)    #初始化ROS节点，加上后面的参数为True可以使得节点不会重名，但会导致节点名字后面加上任意后缀，如turtle_tf_broadcaster_1234
    turtlename = rospy.get_param('~turtle')     #该函数用于从参数服务器获取参数，此处获得具体是1还是2的参数，这是属于类的私有参数，所以加上了~
    rospy.Subscriber('/%s/pose' % turtlename,   #订阅海龟位置
                     turtlesim.msg.Pose,        #消息类型
                     handle_turtle_pose,  	  #回调函数
                     turtlename)		  #传递给回调的额外参数
    rospy.spin()				  #保持节点运行，等待订阅消息



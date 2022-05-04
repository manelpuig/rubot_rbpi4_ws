#!/usr/bin/env python3
import sys
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import csv

robot_x = 0.0
sample = 0
tplot=[]
xplot = []
vxplot=[]
fig, ax = plt.subplots()
plt.ion()
#maxlen = 400

def odom_callback(data):
    global robot_x
    global sample
    global tplot
    global xplot
    global vxplot
    sample +=1
    tplot.append(sample)
    robot_x=data.pose.pose.position.x
    rospy.loginfo("Robot Odometry x= %f\n",robot_x)
    xplot.append(robot_x)
    robot_vx=data.twist.twist.linear.x
    rospy.loginfo("Robot Odometry vx= %f\n",robot_x)
    vxplot.append(robot_vx)
    plt.plot(tplot, vxplot, color='r')
    plt.plot(tplot, xplot, color='b')
    plt.pause(0.05)
    ax.clear()
    fig.ylim([0, 120])
    fig.legend(["Vx and X"],loc = "upper left")
    plt.show()       
    
	
def move_rubot(lin_vel,ang_vel,distance):
    pub = rospy.Publisher('/cmd_vel', Twist)#, queue_size=10)
    rospy.Subscriber('/odom',Odometry, odom_callback)
    rate = rospy.Rate(10) # 10hz
    global robot_x
    vel = Twist()
    while not rospy.is_shutdown():
        vel.linear.x = 0.0
        vel.linear.y = 0.0
        vel.linear.z = 0.0
        vel.angular.x = 0.0
        vel.angular.y = 0.0
        vel.angular.z = 0.0
        rospy.loginfo("Linear Vel = %f: Angular Vel = %f",lin_vel,ang_vel)

        if(robot_x >= distance):
            rospy.loginfo("Robot Reached destination")
            rospy.logwarn("Stopping robot")
            vel.linear.x = 0.0
            vel.linear.y = 0.0
            vel.linear.z = 0.0
            vel.angular.x = 0.0
            vel.angular.y = 0.0
            vel.angular.z = 0.0
            pub.publish(vel)

            with open('CL_PIDcontrol.csv', 'w') as csvfile:
            header = ['vx','xh']
            writer = csv.DictWriter(csvfile,fieldnames=header)
            writer.writeheader()
            for i in range(0,len(vxplot):
                writer.writerow({'vx': vxplot[i],
                                'x': xplot[i]})
            break 
        else:
            rospy.loginfo("Robot moving")
            vel.linear.x = lin_vel
            vel.angular.z = ang_vel
            pub.publish(vel)
            rate.sleep()
try:
    rospy.init_node('rubot_nav', anonymous=False)
    v= rospy.get_param("~v")
    w= rospy.get_param("~w")
    d= rospy.get_param("~d")
    robot_x = 0.0
    move_rubot(v,w,d)
except rospy.ROSInterruptException:
    pass

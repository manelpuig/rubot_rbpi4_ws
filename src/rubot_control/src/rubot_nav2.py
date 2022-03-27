#!/usr/bin/env python3
import sys
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

robot_x = 0.0

def odom_callback(data):
    global robot_x
    robot_x=data.pose.pose.position.x
    rospy.loginfo("Robot Odometry x= %f\n",robot_x)
    
    
	
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

#!/usr/bin/env python3
import sys
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def odom_callback(data):
    global robot_x
    robot_x=data.pose.pose.position.x
    
    rospy.loginfo("Robot Odometry x= %f\n",robot_x)
	
def move_rubot(lin_vel,ang_vel,distance):
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/odom',Odometry, odom_callback)
    rate = rospy.Rate(7) # 10hz
    global robot_x
    vel = Twist()
    vel.linear.x = 0.0
    vel.linear.y = 0.0
    vel.linear.z = 0.0
    vel.angular.x = 0.0
    vel.angular.y = 0.0
    vel.angular.z = 0.0
    while not rospy.is_shutdown():
                
        if(robot_x <= distance):
            rospy.loginfo("Robot running")
            rospy.loginfo("Linear Vel = %f: Angular Vel = %f",lin_vel,ang_vel)
            vel.linear.x = lin_vel
            vel.angular.z = ang_vel
            pub.publish(vel)
            rate.sleep()

        else:
            rospy.logwarn("Stopping robot")
            vel.linear.x = 0.0
            vel.linear.y = 0.0
            vel.angular.z = 0.0
            pub.publish(vel)
            rate.sleep()
    rospy.spin()
    
try:
    rospy.init_node('rubot_nav', anonymous=False)
    v= rospy.get_param("~v")
    w= rospy.get_param("~w")
    d= rospy.get_param("~d")
    robot_x = 0
    move_rubot(v,w,d)
except rospy.ROSInterruptException:
    pass

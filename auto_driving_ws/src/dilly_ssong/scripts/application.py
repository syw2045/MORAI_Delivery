#! /usr/bin/python3

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

rospy.init_node('application', anonymous=True)
client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
client.wait_for_server()

while(True):
    goal = MoveBaseGoal()
    # goal.target_pose.header.frame_id="map"
    # goal.target_pose.header.stamp = rospy.Time.now()
    # goal.target_pose.pose.position.x = 8.63
    # goal.target_pose.pose.position.y = 0.885
    # goal.target_pose.pose.orientation.z = 0.00362
    
    # client.send_goal(goal)
    # wait = client.wait_for_result()
    
    
    # goal.target_pose.header.frame_id="map"
    # goal.target_pose.header.stamp = rospy.Time.now()
    # goal.target_pose.pose.position.x = 15.6
    # goal.target_pose.pose.position.y = -2.69
    # goal.target_pose.pose.orientation.z = 0.00653
    
    
    # client.send_goal(goal)
    # wait = client.wait_for_result()
    
    # goal.target_pose.header.frame_id="map"
    # goal.target_pose.header.stamp = rospy.Time.now()
    # goal.target_pose.pose.position.x = 26
    # goal.target_pose.pose.position.y = -4.81
    # goal.target_pose.pose.orientation.z = 0.803
    
    # client.send_goal(goal)
    # wait = client.wait_for_result()

    # goal.target_pose.header.frame_id="map"
    # goal.target_pose.header.stamp = rospy.Time.now()
    # goal.target_pose.pose.position.x = 31.6
    # goal.target_pose.pose.position.y = -2.25
    # goal.target_pose.pose.orientation.z = 0.995
    
    # client.send_goal(goal)
    # wait = client.wait_for_result()

    # teleport
    goal.target_pose.header.frame_id="map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 8.99
    goal.target_pose.pose.position.y = -2.36
    goal.target_pose.pose.orientation.z = 0.973
    
    client.send_goal(goal)
    wait = client.wait_for_result()
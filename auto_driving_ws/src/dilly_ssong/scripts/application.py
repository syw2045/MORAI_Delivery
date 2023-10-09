import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

rospy.init_node('application', anonymous=True)
client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
client.wait_for_server()

while(True):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id="map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 8.82
    goal.target_pose.pose.position.y = 1.17
    goal.target_pose.pose.orientation.z = -0.000462
    
    client.send_goal(goal)
    wait = client.wait_for_result()
    
    
    goal.target_pose.header.frame_id="map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 15.1
    goal.target_pose.pose.position.y = -0.792
    goal.target_pose.pose.orientation.w = 0.00262
    
    
    client.send_goal(goal)
    wait = client.wait_for_result()
    
    goal.target_pose.header.frame_id="map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 17.6
    goal.target_pose.pose.position.y = -5.95
    goal.target_pose.pose.orientation.z = -0.00154
    
    client.send_goal(goal)
    wait = client.wait_for_result()
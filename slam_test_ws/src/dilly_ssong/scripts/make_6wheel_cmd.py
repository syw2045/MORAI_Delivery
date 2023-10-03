#! /usr/bin/python3
import rospy

from geometry_msgs.msg import Twist
from morai_msgs.msg import SkidSteer6wUGVCtrlCmd

class Make_6wheel_cmd:
    def __init__(self):
        rospy.init_node('Make_6wheel_cmd', anonymous=True)
        
        rospy.Subscriber("/cmd_vel", Twist, self.cmd_vel_CB)
        
        self.wheel_cmd_pub = rospy.Publisher('/6wheel_skid_ctrl_cmd',SkidSteer6wUGVCtrlCmd, queue_size=1)

        rate = rospy.Rate(20)

        self.linear_x = 0
        self.angular_z = 0

        self.driving = SkidSteer6wUGVCtrlCmd()

        while not rospy.is_shutdown():
                self.drivingMsg()
                rate.sleep()


    def cmd_vel_CB(self, data):
        self.linear_x = data.linear.x
        self.angular_z = data.angular.z

    def drivingMsg(self):
        self.driving.Target_linear_velocity = self.linear_x
        self.driving.Target_angular_velocity = self.angular_z

        if self.linear_x == 0:
            self.driving.cmd_type = 0
        else: self.driving.cmd_type = 3

        self.wheel_cmd_pub.publish(self.driving)
         
def main():
    try:
        make_6wheel_cmd=Make_6wheel_cmd()    
    except rospy.ROSInterruptException:
        pass
    
if __name__ == '__main__':
    main()
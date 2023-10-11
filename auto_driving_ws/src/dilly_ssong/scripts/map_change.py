#!/usr/bin/env python3

import os
import rospy
from morai_msgs.msg import GPSMessage

class Map_Change:
    def __init__(self):
        rospy.init_node("map_change")
        rospy.Subscriber("/gps_origin",GPSMessage,self.gpsCB)

        self.gps_data_curr = GPSMessage()
        self.gps_data_prev = GPSMessage()

        self.changed = False
        self.indoor = True
        self.outdoor = False

        rate = rospy.Rate(50)
        
        while not rospy.is_shutdown():
            self.cal_diff()
            rospy.loginfo("mapsetsetestsetetsetset")
            rate.sleep()
            
    def cal_diff(self):
        if self.latitude_differnce > 0.0007 and self.longitude_differnce < - 0.004 : # changed true
            if self.indoor:
                rospy.loginfo("map changed outdoor")
                os.system("roslaunch dilly_ssong outdoor.launch")
                self.outdoor = False
                self.indoor = True
                # map statud : outdoor

            elif self.outdoor:
                rospy.loginfo("map changed outdoor")
                os.system("roslaunch dilly_ssong indoor.launch")
                self.indoor = True
                self.outdoor = False
                # map status : indoor

        else: pass # changed false

    def gpsCB(self,data):
        if self.gps_data_prev is None:
            self.gps_data_prev = data
        else: # value true
            self.gps_data_prev = self.gps_data_curr
        self.gps_data_curr = data

def main():
    try:
        map_change=Map_Change()    
    except rospy.ROSInterruptException:
        pass
    
if __name__ == '__main__':
    main()
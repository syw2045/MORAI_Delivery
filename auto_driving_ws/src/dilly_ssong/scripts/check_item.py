#! /usr/bin/python3

import rospy

from morai_msgs.msg import WoowaDillyStatus


class Item_Check:
    def __init__(self):
        rospy.init_node('item_check', anonymous=True)
        rospy.Subscriber("/WoowaDillyStatus", WoowaDillyStatus, self.wdsCB)

        self.itemList = WoowaDillyStatus()

        rate = rospy.Rate(50)
        
        while not rospy.is_shutdown():
            rospy.INFO("%s", self.itemList)
            rate.sleep()

    def wdsCB(self, data):
        self.itemList = data


def main():
    try:
        item_check=Item_Check()    
    except rospy.ROSInterruptException:
        pass
    
if __name__ == '__main__':
    main()
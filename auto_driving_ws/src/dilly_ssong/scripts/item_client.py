#! /usr/bin/env python3

import rospy

from morai_msgs.srv import WoowaDillyEventCmdSrv

rospy.init_node('item_client')
rospy.wait_for_service('item_count')
item_counter = rospy.ServiceProxy('item_count', WoowaDillyEventCmdSrv)

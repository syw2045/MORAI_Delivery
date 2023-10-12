#! /usr/bin/env python3

import rospy
from morai_msgs.srv import WoowaDillyEventCmdSrv, WoowaDillyEventCmdSrvResponse
from morai_msgs.msg import DillyCmd, DillyCmdResponse

test = WoowaDillyEventCmdSrv()
test._request_class.request.isPickup = True
test._request_class.request.deliveryItemIndex = 10

print(test)

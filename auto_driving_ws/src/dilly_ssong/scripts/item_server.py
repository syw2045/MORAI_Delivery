#! /usr/bin/env python3

import rospy

from morai_msgs.srv import WoowaDillyEventCmdSrv, WoowaDillyEventCmdSrvResponse

def item_resp(request):
	return WoowaDillyEventCmdSrvResponse(request)

def item_server():
    rospy.init_node('service_server')
    service = rospy.Service('item_req', WoowaDillyEventCmdSrv, item_resp)
    
    
if __name__ == '__main__':
    item_server()
    rospy.spin()
#! /usr/bin/env python3

import rospy
from morai_msgs.srv import WoowaDillyEventCmdSrv, WoowaDillyEventCmdSrvResponse
from morai_msgs.msg import DillyCmd, DillyCmdResponse

def handle_dilly_cmd(request):
    # 예제로 간단한 응답을 생성
    print(request.request.isPickup)
    response = WoowaDillyEventCmdSrvResponse()
    if request.request.isPickup and request.request.deliveryItemIndex == 2:
        print("1")
    return response

def woowa_dilly_server():
    rospy.init_node('woowa_dilly_server')
    # 서비스 이름과 타입을 등록
    rospy.Service('woowa_dilly_event_cmd', WoowaDillyEventCmdSrv, handle_dilly_cmd)
    print("Woowa Dilly Event Command Server is ready to receive requests.")
    rospy.spin()

if __name__ == "__main__":
    woowa_dilly_server()

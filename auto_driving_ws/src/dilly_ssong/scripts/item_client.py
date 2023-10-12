#! /usr/bin/env python3

import rospy
from morai_msgs.srv import WoowaDillyEventCmdSrv, WoowaDillyEventCmdSrvRequest

def woowa_dilly_client(is_pickup, delivery_item_index):
    # 클라이언트 노드 초기화
    rospy.init_node('woowa_dilly_client')
    # 서비스 프록시 생성
    rospy.wait_for_service('woowa_dilly_event_cmd')
    try:
        woowa_dilly_service = rospy.ServiceProxy('woowa_dilly_event_cmd', WoowaDillyEventCmdSrv)
        # 서비스 요청 생성
        request = WoowaDillyEventCmdSrvRequest()
        request.request.isPickup = is_pickup
        request.request.deliveryItemIndex = delivery_item_index
        # 서비스 호출
        response = woowa_dilly_service(request)
        # 서비스 응답 처리
        if response:
            print("Command processed successfully.")
        else:
            print("Command processing failed.")
    except rospy.ServiceException as e:
        print("Service call failed:", e)

if __name__ == "__main__":
    # 클라이언트에서 보낼 데이터 정의
    is_pickup = True
    delivery_item_index = 1
    woowa_dilly_client(is_pickup, delivery_item_index)

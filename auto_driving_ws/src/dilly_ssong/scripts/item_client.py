#! /usr/bin/env python3

import rospy
from morai_msgs.srv import WoowaDillyEventCmdSrv, WoowaDillyEventCmdSrvResponse
from morai_msgs.msg import DillyCmd, DillyCmdResponse

def woowa_dilly_client(is_pickup, delivery_item_index):
    rospy.init_node('woowa_dilly_client')

    # 서비스 프록시 생성
    rospy.wait_for_service('woowa_dilly_event_cmd')
    try:
        woowa_dilly_service = rospy.ServiceProxy('woowa_dilly_event_cmd', WoowaDillyEventCmdSrv)
        # 서비스 요청 생성
        request = DillyCmd()
        request.isPickup = is_pickup
        request.deliveryItemIndex = delivery_item_index

        response = woowa_dilly_service(request)
        print(response)
        if response:
                print("Command processed successfully.")
        else:
            print("Command processing failed.")

    except rospy.ServiceException as e:
        print("Service call failed:", e)


if __name__ == "__main__":
    is_pickup_example = True
    delivery_item_index_example = 1
    woowa_dilly_client(is_pickup_example, delivery_item_index_example)

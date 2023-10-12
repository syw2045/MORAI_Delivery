#!/usr/bin/env python
import rospy
import numpy as np
from morai_msgs.msg import GPSMessage

class GPS_Filter_Node:
    def __init__(self):
        rospy.init_node("GPS_Filtering_Node")
        rospy.loginfo("Starting GPS_Filter_Node as GPS_Filtering_Node")
        rospy.Subscriber("/gps_origin", GPSMessage, self.MORAI_GPS_CB)
        self.filtered_pub = rospy.Publisher("gps", GPSMessage, queue_size=10)

        # 초기 위치 정보 설정
        self.initial_latitude = 37.418536874388096  # 초기 위도
        self.initial_longitude = 127.13135627199034  # 초기 경도
        self.initial_altitude = 0.6509203910827637  # 초기 고도

        self.Filtered_GPS = GPSMessage()

        # Kalman Filter 변수 초기화
        self.state = np.array([self.initial_latitude, self.initial_longitude, self.initial_altitude, 0.0, 0.0, 0.0], dtype=float)
        self.covariance = np.eye(6)  # 초기 공분산 행렬

        self.prev_state = self.state.copy()
        self.prev_covariance = self.covariance.copy()
                # Kalman Filter Parameter
        self.transition_matrix = np.array(
                                          [[1,0,0,1,0,0],
                                          [0,1,0,0,0,0],
                                          [0,0,1,0,0,1],
                                          [0,0,0,1,0,0],
                                          [0,0,0,0,1,0],
                                          [0,0,0,0,0,1]]
                                          )  
        # fpr 3rd dimension latitude longitude altitude (fix)
        
        self.process_noise_covariance = np.array(
            [[1.0e-14, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0e-14, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0e-14, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0e-14, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0e-14, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0e-14]]
            )
        # Q value for noise covariance

        self.observation_matrix = np.array(
                                            [[1,0,0,0,0,0],
                                            [0,1,0,0,0,0],
                                            [0,0,1,0,0,0],
                                            [0,0,0,1,0,0],
                                            [0,0,0,0,1,0],
                                            [0,0,0,0,0,1]]
                                            )
        # USE GPS to make observation Matrix (H)
        
        self.observation_noise_covariance = np.array(
                                                [[1.0e-6, 0.0, 0.0, 0.0, 0.0, 0.0],
                                                [0.0, 1.0e-6, 0.0, 0.0, 0.0, 0.0],
                                                [0.0, 0.0, 1.0e-6, 0.0, 0.0, 0.0],
                                                [0.0, 0.0, 0.0, 1.0e-6, 0.0, 0.0],
                                                [0.0, 0.0, 0.0, 0.0, 1.0e-6, 0.0],
                                                [0.0, 0.0, 0.0, 0.0, 0.0, 1.0e-6]]
                                                )
        self.queue_size = 20

        self.gps_queue = []


        rate = rospy.Rate(50)

        while not rospy.is_shutdown():
            self.publish_Filtered_GPS()
            rate.sleep()



    def MORAI_GPS_CB(self, data):
        self.Filtered_GPS = data
        # update
        measurement = np.array([data.latitude, data.longitude, data.altitude, 0.0, 0.0, 0.0], dtype=float)  # set value initial

        # predict
        predicted_state = np.dot(self.transition_matrix, self.state)
        predicted_covariance = np.dot(np.dot(self.transition_matrix, self.covariance), self.transition_matrix.T) + self.process_noise_covariance

        #  compute calman gain
        kalman_gain = np.dot(np.dot(predicted_covariance, self.observation_matrix.T),
                             np.linalg.inv(np.dot(np.dot(self.observation_matrix, predicted_covariance), self.observation_matrix.T) + self.observation_noise_covariance))
        self.state = predicted_state + np.dot(kalman_gain, (measurement - np.dot(self.observation_matrix, predicted_state))) # update estimate x^
        self.covariance = predicted_covariance - np.dot(np.dot(kalman_gain, self.observation_matrix), predicted_covariance) # update error covariance

        self.Filtered_GPS.latitude = self.state[0]
        self.Filtered_GPS.longitude = self.state[1]
        self.Filtered_GPS.altitude = self.state[2]


        self.prev_state = self.state.copy()
        self.prev_covariance = self.covariance.copy()



    def publish_Filtered_GPS(self):
        self.filtered_pub.publish(self.Filtered_GPS)

def main():
    try:
        gps_pub=GPS_Filter_Node()    
    except rospy.ROSInterruptException:
        pass

if __name__ == "__main__":
    main()
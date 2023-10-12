#!/usr/bin/env python
import rospy
import numpy as np
from morai_msgs.msg import GPSMessage

class GPS_filtfilt:
    def __init__(self):
        rospy.init_node("GPS_Filtering_Node")
        rospy.loginfo("Starting GPS_filtfilt as GPS_Filtering_Node")
        rospy.Subscriber("/gps_1", GPSMessage, self.MORAI_GPS_CB)
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
                                          [[1,0,0,0,0,0],
                                          [0,1,0,0,0,0],
                                          [0,0,1,0,0,0],
                                          [0,0,0,1,0,0],
                                          [0,0,0,0,1,0],
                                          [0,0,0,0,0,1]]
                                          )  
        # fpr 3rd dimension latitude longitude altitude (fix)
        
        self.process_noise_covariance = np.array(
            [[1.0e-10, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0e-10, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0e-10, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0e-10, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0e-10, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0e-10]]
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
                                                [[1.0e-05, 0.0, 0.0, 0.0, 0.0, 0.0],
                                                [0.0, 1.0e-05, 0.0, 0.0, 0.0, 0.0],
                                                [0.0, 0.0, 1.0e-05, 0.0, 0.0, 0.0],
                                                [0.0, 0.0, 0.0, 1.0e-05, 0.0, 0.0],
                                                [0.0, 0.0, 0.0, 0.0, 1.0e-05, 0.0],
                                                [0.0, 0.0, 0.0, 0.0, 0.0, 1.0e-05]]
                                                )
        # self.queue_size = 20

        # self.prev_gap_flag = False

        rate = rospy.Rate(50)

        while not rospy.is_shutdown():
            # if not self.need_smooth(): # don't use prev
            self.publish_Filtered_GPS()
            # self.prev_gap_flag = True
            rate.sleep()
            # else:                      # use prev
            #     self.Filtered_GPS.latitude = self.prev_state[0]
            #     self.Filtered_GPS.longitude = self.prev_state[1]
            #     self.Filtered_GPS.altitude = self.prev_state[2]
            #     self.publish_Filtered_GPS()
            #     # self.prev_gap_flag = False
            #     rate.sleep()



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

        # if self.prev_gap_flag:  # use prev_state
        #     pass
        # else:
        self.prev_state = self.state.copy()
        self.prev_covariance = self.covariance.copy()



    def publish_Filtered_GPS(self):
        self.filtered_pub.publish(self.Filtered_GPS)
    
    # def save_queue(self):
    #     if not self.condition_queue.full():
    #         # save gap values
    #         self.state_saver_var[0] = self.prev_state[0]-self.state[0]
    #         self.state_saver_var[1] = self.prev_state[1]-self.state[1]
    #         self.state_saver_var[2] = self.prev_state[2]-self.state[2]
    #         self.condition_queue.put(self.state_saver_var)
    #     else:
    #         self.condition_queue.get()
    #         self.state_saver_var[0] = self.prev_state[0]-self.state[0]
    #         self.state_saver_var[1] = self.prev_state[1]-self.state[1]
    #         self.state_saver_var[2] = self.prev_state[2]-self.state[2]
    #         self.condition_queue.put(self.state_saver_var)


    # def need_smooth(self):
    #     if not self.condition_queue.full():
    #         return False
        
    #     copyed_queue = self.condition_queue
        
    #     sums = np.array([0.0, 0.0, 0.0], dtype=float)
    #     curr = np.array([0.0, 0.0, 0.0], dtype=float)

    #     while not copyed_queue.empty():
    #         states = copyed_queue.get()
    #         sums[0] += states[0]
    #         sums[1] += states[1]
    #         sums[2] += states[2]
        
    #     avg = np.array([sums[0]/self.queue_size, sums[1]/self.queue_size, sums[2]/self.queue_size], dtype=float)

    #     curr[0]=self.prev_state[0]-self.state[0]
    #     curr[1]=self.prev_state[1]-self.state[1]
    #     curr[2]=self.prev_state[2]-self.state[2]
        
    #     if ((abs(curr[0]-avg[0]) > 100) or (abs(curr[1]-avg[1]) > 100) or (abs(curr[2]-avg[2]) > 100)):
    #         return True
    #     else: False

def main():
    try:
        gps_pub=GPS_filtfilt()    
    except rospy.ROSInterruptException:
        pass

if __name__ == "__main__":
    main()
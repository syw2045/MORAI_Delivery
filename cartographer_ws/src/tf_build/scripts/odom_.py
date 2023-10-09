#!/usr/bin/env python
import rospy

from morai_msgs.msg import GPSMessage
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from tf2_msgs.msg import TFMessage

import geometry_msgs.msg
import pyproj
import tf
import tf2_ros
import numpy as np

from math import cos,sin,sqrt,pow,atan2,pi


class Odom_tf_build:
    def __init__(self):
        rospy.init_node("make_odom_tf")
        rospy.loginfo("Starting Odom_tf_build as name_node.")

        rospy.Subscriber("/gps",GPSMessage, self.gpsCB)
        rospy.Subscriber("/imu",Imu, self.imuCB)
        self.odom_pub=rospy.Publisher("odom",Odometry,queue_size=10)

        self.odom=Odometry()
        # self.odom.header.stamp = rospy.Time.now()

        rospy.loginfo(rospy.Time.now())
        self.odom.header.frame_id = "odom"
        self.odom.child_frame_id= "base_link"

        # flag
        self.is_gps = False
        self.is_imu = False

        self.x_offset = 334209.0789507285
        self.y_offset = 4143042.501430065

        # convert gps to UTM
        self.proj_UTM = pyproj.Proj(proj="utm",zone=52,ellps="WGS84",preserve_units=False)

        # 30Hz
        rate = rospy.Rate(50)
        
        while not rospy.is_shutdown():
            self.odom.header.stamp = rospy.get_rostime()
            if self.is_gps and self.is_imu:
                self.MakeOdomMsg()
                self.MakeOdomTF()
                # self.MakeOdomTF2Msg()
                # self.MakeOdomTF2()
                rate.sleep()

    def gpsCB(self, data):
        self.xy_data = self.proj_UTM(data.longitude, data.latitude)
        self.is_gps = True

    def imuCB(self, data):
        self.euler_data = tf.transformations.euler_from_quaternion((data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w))
        self.is_imu = True
    
    def MakeOdomMsg(self):
        quaternion = tf.transformations.quaternion_from_euler(self.euler_data[0], self.euler_data[1], self.euler_data[2])
        self.odom.pose.pose.position.x = self.xy_data[0] - self.x_offset
        self.odom.pose.pose.position.y=self.xy_data[1] - self.y_offset
        self.odom.pose.pose.position.z=0
        self.odom.pose.pose.orientation.x=quaternion[0]
        self.odom.pose.pose.orientation.y=quaternion[1]
        self.odom.pose.pose.orientation.z=quaternion[2]
        self.odom.pose.pose.orientation.w=quaternion[3]
        self.odom_pub.publish(self.odom)


    def MakeOdomTF(self):
        br =tf.TransformBroadcaster()
        position_x = self.xy_data[0] - self.x_offset
        position_y = self.xy_data[1] - self.y_offset
        
        br.sendTransform((position_x, position_y, 0),
                        tf.transformations.quaternion_from_euler(self.euler_data[0], self.euler_data[1], self.euler_data[2]),
                        rospy.Time.now(),
                        "base_link",
                        "odom")
        
    # def MakeOdomTF2Msg(self):
    #     quaternion = tf.transformations.quaternion_from_euler(self.euler_data[0], self.euler_data[1], self.euler_data[2])
    #     self.odom.pose.pose.position.y=self.xy_data[1] - self.y_offset
    #     self.odom.pose.pose.position.z=0
    #     self.odom.pose.pose.orientation.x=quaternion[0]
    #     self.odom.pose.pose.orientation.y=quaternion[1]
    #     self.odom.pose.pose.orientation.z=quaternion[2]
    #     self.odom.pose.pose.orientation.w=quaternion[3]
    #     self.odom_pub.publish(self.odom)



    # def MakeOdomTF2(self):        
    #     broadcaster = tf2_ros.StaticTransformBroadcaster()
    #     quat=tf.transformations.quaternion_from_euler(self.euler_data[0], self.euler_data[1], self.euler_data[2])
    #     static_transformStamped = geometry_msgs.msg.TransformStamped()

    #     # static_transformStamped.header.stamp = rospy.Time.now()
    #     static_transformStamped.header.frame_id = "odom"
    #     static_transformStamped.child_frame_id = "base_link"

    #     static_transformStamped.transform.translation.x = self.xy_data[0] - self.x_offset
    #     static_transformStamped.transform.translation.y = self.xy_data[1] - self.y_offset
    #     static_transformStamped.transform.translation.z = 0.0  # Assuming the base_link is at ground level

    #     static_transformStamped.transform.rotation.x = quat[0]
    #     static_transformStamped.transform.rotation.y = quat[1]
    #     static_transformStamped.transform.rotation.z = quat[2]
    #     static_transformStamped.transform.rotation.w = quat[3]
        
    #     broadcaster.sendTransform(static_transformStamped)
    #     rospy.loginfo("tf publish.")



def main():
    try:
        makeodom=Odom_tf_build()    
    except rospy.ROSInterruptException:
        pass
    
if __name__ == '__main__':
    main()
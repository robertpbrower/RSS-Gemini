#!/usr/bin/env python
#################################################################################
# Copyright 2018 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#################################################################################

# Authors: Gilbert #

import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

LINEAR_VEL = 0.22
STOP_DISTANCE = 0.2
LIDAR_ERROR = 0.05
SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR

class Obstacle():
    def __init__(self):
        self._cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.obstacle()
        
    def get_scan(self):
        scan = rospy.wait_for_message('scan', LaserScan)
        scan_filter = []
        ang_min = scan.angle_min
	ang_max = scan.angle_max
	ang_incr = scan.angle_increment
	
	range_min = scan.range_min
	range_max = scan.range_max

        samples = len(scan.ranges)  # The number of samples is defined in 
                                    # turtlebot3_<model>.gazebo.xacro file,
                                    # the default is 360.

	cvec = [0,0]

	for i in range(0, samples):
	    sample_ang = ang_min + i * ang_incr
	    if range_min <= scan.ranges[i] <= range_max:
		cvec[0] += -math.cos(sample_ang) * pow(scan.ranges[i],-2)
		cvec[1] += -math.sin(sample_ang) * pow(scan.ranges[i],-2)
	
	cvec[0] /= samples
	cvec[1] /= samples
	
	
	mag = math.hypot(cvec[0], cvec[1])
	ang = math.atan2(cvec[1], cvec[0])
       
        return (mag,ang)

    def obstacle(self):
        twist = Twist()
        turtlebot_moving = True

        while not rospy.is_shutdown():
            (mag,ang) = self.get_scan() 
            print('pf res: ',mag,ang)
            if mag < 0.5:
		twist.linear.x = 0.2
		twist.angular.z = 0
	    elif mag < 3 or abs(ang) < 0.5:
		twist.linear.x = 0.15
		twist.angular.z = ang / 7.5
	    elif mag < 5 or abs(ang) < 1.5:
		twist.linear.x = 0.05
		twist.angular.z = ang / 5.0
	    else:
		twist.linear.x = 0
		if ang < 0:
		    twist.angular.z = -0.2
		else:
		    twist.angular.z = 0.2
	    print(twist.linear.x,twist.angular.z)
	    self._cmd_pub.publish(twist)
	    

def main():
    rospy.init_node('turtlebot3_obstacle')
    try:
        obstacle = Obstacle()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()

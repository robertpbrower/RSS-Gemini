#!/usr/bin/env python3
import math
import numpy
import sys
from rclpy.node import Node
from rclpy.qos import QoSProfile
from nav_msgs.msg import OccupancyGrid
import os

def mapToString(w,h,mp):
	tpt = []
	for i in range(0,h):
		tpt.append(''.join(map(mapChar,list(mp[w * i : w * (i + 1)]))))
	return '\n'.join(tpt)
def mapChar(c):
	if c == -1:
		return "?"
	elif c == 0:
		return " "
	else:
		return "X"

class MapObjectiveNode(Node):
    def __init__(self):
        super().__init__('map_objective_finder')
        qos = QoSProfile(depth=10)
        self.map_sub = self.create_subscription(OccupancyGrid,'map',self.onMap,qos)
        
    def onMap(self, new_map):
    	os.system('clear')
    	data_info = new_map.info
    	pix = new_map.data
    	height = data_info.height
    	width = data_info.width
    	
    	print(mapToString(width,height,pix))

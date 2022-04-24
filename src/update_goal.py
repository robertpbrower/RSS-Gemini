#!/usr/bin/env python

import sys
import os
import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist,PoseStamped
from nav_msgs.msg import OccupancyGrid,Odometry
from tf.transformations import euler_from_quaternion
import tf

def printMap(data,w,h,thresh,relRobot):
    for i in range(h-1,-1,-1): # x axis
    	for j in range(0,w): # y axis    
            nex = i * w + j
            if [i,j] == relRobot:
                sys.stdout.write('#')
            elif data[nex] > thresh:
                sys.stdout.write('X')
            elif data[nex] == -1:
                sys.stdout.write('?')
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')
def drawMapWithRobot(grid, robotPos, pathset = set([]), goal = None):
    for (ir,row) in enumerate(grid):
        for (ic,val) in enumerate(row):
            if [ir,ic] == robotPos:
                sys.stdout.write('#')
            elif [ir,ic] == list(goal):
                sys.stdout.write('+')
            elif (ir,ic) in pathset:
                sys.stdout.write('o')
            elif val == 0:
                sys.stdout.write('X')
            elif val == -1:
                sys.stdout.write('?')
            elif val == 1:
                sys.stdout.write(' ')
        sys.stdout.write('\n')

def drawMap(grid):
    for row in grid:
        for val in row:
            if val == 0:
                sys.stdout.write('X')
            elif val == -1:
                sys.stdout.write('?')
            elif val == 1:
                sys.stdout.write(' ')
        sys.stdout.write('\n')
def convertMap(data, w, h, thresh):
    themap = []
    for i in range(h-1,-1,-1): # x axis
        row = []
        for j in range(0,w): # y axis
            nex = i * w + j
            if data[nex] > thresh:
                row.append(0)
            elif data[nex] == -1:
                row.append(-1)
            else:
                row.append(1)
        themap.append(list(row))
    return themap

def thickenMap(mp):
    set_barriers = set([])
    for i in range(0, len(mp)):
        for j in range(0, len(mp[i])):
            if mp[i][j] == 0:
                set_barriers.add((i,j))
    
    new_map = []
    for i in range(0, len(mp)):
        new_row = []
        for j in  range(0,len(mp[i])):
            case_up  = (i-1,j) in set_barriers
            case_down= (i+1,j) in set_barriers
            case_left = (i,j+1) in set_barriers
            case_right = (i,j-1) in set_barriers
            if case_up or case_down or case_left or case_right:
                new_row.append(0)
            else:
                new_row.append(mp[i][j])
        new_map.append(list(new_row))
    return new_map
    
def resolvePath(backprop, ed, src):
    pset = set([ed])
    
    cpt = ed
    while cpt != src:
        cpt = backprop[cpt]
        pset.add(cpt) # finite no loop linking guarantee term
    
    return pset
    
    
def findPath(src, mp):
    visited = set([src])
    bfsq = [src]
    backprop = {}
    while len(bfsq) > 0:
        (nr, nc) = bfsq.pop(0)
        candidates = [(nr-1, nc), (nr+1, nc), (nr, nc+1), (nr, nc-1)]
        for (cr,cc) in candidates:
            if (cr,cc) in visited:
                continue
            if 0 <= cr < len(mp) and 0 <= cc < len(mp[cr]):
                if mp[cr][cc] != 0:
                    backprop[(cr,cc)] = (nr,nc) # link chain
                    visited.add((cr,cc))
                    if mp[cr][cc] == 1:
                        bfsq.append((cr,cc))
                    
                    if mp[cr][cc] == -1:
                        return (resolvePath(backprop, (cr,cc), src), (cr, cc))
    print 'ayayayayayya'             
class GraphExplore():
    def __init__(self):
        self.listener = tf.TransformListener()
        self.map_sub = rospy.Subscriber('map', OccupancyGrid, self.on_map, queue_size = 1)
        self.position_sub = rospy.Subscriber('odom',Odometry,self.on_odom,queue_size=1)        
        self.map_origin = None
        self.robot_origin = None
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            rate.sleep()
    def on_odom(self,odommsg):
		self.lastOdom = odommsg

    def on_map(self,mapmsg):
        mapinfo = mapmsg.info
        trans,rot = self.listener.lookupTransform('tb3_2/map','tb3_2/odom',rospy.Time(0))
        t = PoseStamped()
        t.header = self.lastOdom.header
        t.pose = self.lastOdom.pose.pose
        a = self.listener.transformPose('tb3_2/map',t)
        os.system('clear')
        #print(a)
        #print(mapmsg.header.frame_id)
        #print(mapmsg.info)
        relRobot = [a.pose.position.x -mapinfo.origin.position.x,a.pose.position.y - mapinfo.origin.position.y]
        relRobot[0] = int(relRobot[0]/mapinfo.resolution)
        relRobot[1] = int(relRobot[1]/mapinfo.resolution)
        relRobot = relRobot[::-1]
        #printMap(mapmsg.data,mapinfo.width,mapinfo.height,90, relRobot)
        mp = convertMap(mapmsg.data,mapinfo.width,mapinfo.height,90)
        mp_thicken = thickenMap(thickenMap(mp))
        mapBotPos = [(mapinfo.height-1) - relRobot[0], relRobot[1]]
        
        (pathset, goal) = findPath(tuple(mapBotPos), mp_thicken)
        
        drawMapWithRobot(mp, mapBotPos, pathset = pathset, goal = goal) # overlay it on original map (unthickened)
        

def main():
    rospy.init_node('turtlebot3_obstacle')
    try:
        obstacle = GraphExplore()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()

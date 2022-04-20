# RSS-Gemini
Project Repo for CS4610 final project for Team Gemini

Using ROS 1 Kinetic  with Ubuntu 16.04 (xenial)

## Links
-Turtule Bot starting code
https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/#pc-setup

### Alias
```bash

export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost
export TURTLEBOT3_MODEL=burger
alias resource='source ~/catkin_ws/devel/setup.bash'
alias cb='cd ~/catkin_ws && catkin_make'

alias rungemini='ros2 run RSS_Gemini gemini_node' # dont use this, no node yet

```

(For vmware gazebo cores out)
```bash
export SVGA_VGPU10=0
export QT_X11_NO_MITSHM=1
```


### Commands to run
```bash
cb && resource && rungemini
```

Launch house environment (1 robot)
```bash
roslaunch turtlebot3_gazebo turtlebot3_house.launch
```

Launch hosue environment (3 robot)
```bash
roslaunch turtlebot3_gazebo multi_turtlebot3.launch
```

Launch teleop (1 robot)
```bash
roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
```

Launch teleop (ith robot)
```bash
ROS_NAMESPACE=tb3_i roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
```

Install slam_gmapping
```bash
sudo apt-get install ros-kinetic-slam-gmapping
```
Launch slam_gmapping (base robot)
```bash
roslaunch turtlebot3_slam turtlebot3_gmapping.launch set_base_frame:=base_footprint set_odom_frame:=odom set_map_frame:=map
```

Launch slam_gmapping (for each turtlebot)
```bash
ROS_NAMESPACE=tb3_0 roslaunch turtlebot3_slam turtlebot3_gmapping.launch set_base_frame:=tb3_0/base_footprint set_odom_frame:=tb3_0/odom set_map_frame:=tb3_0/map
ROS_NAMESPACE=tb3_1 roslaunch turtlebot3_slam turtlebot3_gmapping.launch set_base_frame:=tb3_1/base_footprint set_odom_frame:=tb3_1/odom set_map_frame:=tb3_1/map
ROS_NAMESPACE=tb3_2 roslaunch turtlebot3_slam turtlebot3_gmapping.launch set_base_frame:=tb3_2/base_footprint set_odom_frame:=tb3_2/odom set_map_frame:=tb3_2/map
```

Install `multi_map_merge`
```bash
sudo apt-get install ros-kinetic-multirobot-map-merge
```

Launch multi_map_merge
```bash
roslaunch turtlebot3_gazebo multi_map_merge.launch
```

Launch rviz
```bash
rosrun rviz rviz -d rospack find turtlebot3_gazebo /rviz/multi_turtlebot3_slam.rviz
```
alt
```bash
rviz
```
then `File >> Open` and navigate to `/home/ashdawngary/catkin_ws/src/turtlebot3_simulations/turtlebot3_gazebo/rviz` and open `multi_turtlebot3_slam.rviz`

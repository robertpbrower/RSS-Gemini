# RSS-Gemini
Project Repo for CS4610 final project for Team Gemini

Using ROS 2 Foxy with WSL2 running Ubuntu 20.02
## Links
-Install WSL2
https://docs.microsoft.com/en-us/windows/wsl/install

-Turtule Bot starting code
https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/#pc-setup

### Alias
```bash
export ROS_DOMAIN_ID=30 #TURTLEBOT3
export TURTLEBOT3_MODEL=burger

alias resource='source ~/colcon_ws/src/install/setup.bash'
alias rungemini='ros2 run RSS_Gemini gemini_node'

```

(For vmware if textures dont load on gazebo)
```bash
export SVGA_VGPU10=0
```


### Commands to run
```bash
cb && resource && rungemini
```

Launch house environment
```bash
ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
```

Launch teleop
```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

Launch cartographer
```bash
ros2 launch turtlebot3_cartographer cartographer.launch.py
```

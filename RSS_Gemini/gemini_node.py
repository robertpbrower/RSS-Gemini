#!/usr/bin/env python3

import rclpy

from RSS_Gemini.turtlebot3_position_control \
    import Turtlebot3PositionControl

from RSS_Gemini.gemini_map import MapObjectiveNode

def main(args=None):
    rclpy.init(args=args)
    turtlebot3_position_control = MapObjectiveNode()
    rclpy.spin(turtlebot3_position_control)

    turtlebot3_position_control.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

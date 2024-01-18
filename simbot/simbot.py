"""
MASLAB 2024
Map Generation and Display
"""

import sys
from .submodules.gamemap import Map
from .submodules.constants import *

import pygame

from kitware_interface.msg import DriveCmd

import rclpy
from rclpy.node import Node

class SimulationNode(Node):
    """ROS2 Node that displays robot position and orientation on a map"""

    def __init__(self):
        """
        One-time method that sets up the robot, like in Arduino
        Code is run when run_setup() method is called
        """
        super().__init__('simulation_node')

        # Create a subscriber to listen for drive motor commands
        self.drive_sub = self.create_subscription(
            DriveCmd,
            'drive_cmd',
            self.drive_callback,
            10)
        self.drive_sub  # prevent unused variable warning

        self.simulation = Map("2024_map.txt")

        print()
        print("Use WASD to move")
        print("Use R to reset the robot")

        # Draw the map
        self.simulation.draw()

    def drive_callback(self, msg):
        """Processes a new drive command and controls motors appropriately"""
        self.simulation.update(msg.l_speed, msg.r_speed)

        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_r:
                    self.robot, self.angle = self.initial

            if e.type == QUIT:
                sys.exit()

def main():
    rclpy.init()

    sim = SimulationNode()
    rclpy.spin(sim)

    sim.destroy_node()  # Destroys the ROS node
    rclpy.shutdown()

if __name__ == '__main__':
    main()

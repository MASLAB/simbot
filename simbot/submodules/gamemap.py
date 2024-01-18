"""
MASLAB 2024
Constructs a Map object from a map file
"""

import sys
import os
from .constants import *
from .kinematics import convert_velocities

class Map:
    def __init__(self, filename):
        """
        Constructs a new map from an input file
        """
        # Read input file
        with open(filename, "r") as f:
            data = f.read()

        # Initialize robot angle (zero up, positive clockwise)
        self.angle = None

        # Initialize robot image
        img = image.load("botpic_cropped.png")
        imgScale = (float(ROBOT_WIDTH), float(ROBOT_WIDTH))
        self.img = transform.scale(img, imgScale)

        # Save initial robot position
        self.initial = ((0, 0), 0)

        # Parse map file
        w, x, p, b, a, r = self.parse(data)
        
        # Initialize data lists
        self.walls = w
        self.platforms = p
        self.box = x
        self.cubes = b
        self.apriltags = a
        self.robot = r
        
        # Initialize game clock
        self.clock = Clock()

    def draw(self):
        # Initialize pygame
        init()

        # Set up pygame screen
        self.screen = display.set_mode(SIZE)

        # Fill the screen
        self.screen.fill(BLACK)

    def update(self, l_speed, r_speed):
        self.screen.fill(BLACK)

        # Get width and height of canvas
        width, height = SIZE

        # Draw grid coordinates
        x = XOFF
        while x <= width:
            y = YOFF
            while y <= height:
                draw.circle(self.screen, WHITE, (x, y), 1)
                y += RESOLUTION
            x += RESOLUTION

        # Draw walls
        for wall in self.walls:
            draw.line(self.screen, *wall)

        # Draw bounding box
        for box in self.box:
            draw.line(self.screen, *box)

        # Draw cubes
        for cube in self.cubes:
            draw.rect(self.screen, *cube)

        # Draw platforms
        for platform in self.platforms:
            draw.line(self.screen, *platform)

        # Draw AprilTags
        for tag in self.apriltags:
            draw.rect(self.screen, *tag)

        # Get drive velocity
        drive_speed = l_speed, r_speed
        linear, angular = convert_velocities(drive_speed)
        
        # Apply velocity to robot & draw robot
        if not (self.robot is None):
            # Get time since last call (in seconds)
            dt = self.clock.tick(50) / 1000

            # Compute robot motion (flip rotation direction)
            delta_angle = -1 * angular * dt
            drive_angle = radians(self.angle) + delta_angle/2
            dx = linear * dt * sin(drive_angle)
            dy = linear * dt * cos(drive_angle)
            self.angle += degrees(delta_angle)

            # Compute new robot position
            x, y = self.robot
            newimg = transform.rotate(self.img, self.angle)
            x += dx
            y += dy

            # Update robot
            self.robot = x, y

            # Shift robot to account for image padding
            padding_angle = radians(self.angle % 90)
            new_size = ROBOT_WIDTH * (cos(padding_angle) + sin(padding_angle))
            adjustment = (new_size - ROBOT_WIDTH) / 2
            x -= adjustment
            y -= adjustment

            # Draw robot
            self.screen.blit(newimg, (x, y))
            display.update()
            
    def parse(self, data):
        """
        Parses map data
        """
        # Prepare data file
        rows = [r.strip() for r in data.split("\n") if len(r.strip()) > 0 and r[0] != "#"]

        # Initialize object lists
        walls = []
        box = []
        platforms = []
        cubes = []
        apriltags = []

        # Initialize robot
        robot = None

        # Iterate through objects
        for row in rows:
            values = [v.strip() for v in row.split(",")][1:]

            match row[0]:

                # Wall
                case "W":
                    x1, y1, x2, y2 = [float(v) for v in values]
                    walls.append((BLUE, (x1 * RESOLUTION + XOFF, y1 * RESOLUTION + YOFF), (x2 * RESOLUTION + XOFF, y2 * RESOLUTION + YOFF), 2))

                # Bounding box
                case "B":
                    xc, yc = [float(v) for v in values]
                    box.append((GREEN, (xc * RESOLUTION + XOFF - BOX_WIDTH / 2, yc * RESOLUTION + YOFF - BOX_WIDTH / 2), (xc * RESOLUTION + XOFF + BOX_WIDTH / 2, yc * RESOLUTION + YOFF - BOX_WIDTH / 2), 1))
                    box.append((GREEN, (xc * RESOLUTION + XOFF + BOX_WIDTH / 2, yc * RESOLUTION + YOFF - BOX_WIDTH / 2), (xc * RESOLUTION + XOFF + BOX_WIDTH / 2, yc * RESOLUTION + YOFF + BOX_WIDTH / 2), 1))
                    box.append((GREEN, (xc * RESOLUTION + XOFF + BOX_WIDTH / 2, yc * RESOLUTION + YOFF + BOX_WIDTH / 2), (xc * RESOLUTION + XOFF - BOX_WIDTH / 2, yc * RESOLUTION + YOFF + BOX_WIDTH / 2), 1))
                    box.append((GREEN, (xc * RESOLUTION + XOFF - BOX_WIDTH / 2, yc * RESOLUTION + YOFF + BOX_WIDTH / 2), (xc * RESOLUTION + XOFF - BOX_WIDTH / 2, yc * RESOLUTION + YOFF - BOX_WIDTH / 2), 1))

                # Robot
                case "R":
                    x1, y1 = [float(v) for v in values[0:2]]
                    self.angle = 180 - float(values[2]) # negative for clockwise rotation
                    robot = (x1 * RESOLUTION - ROBOT_WIDTH / 2 + XOFF, y1 * RESOLUTION - ROBOT_WIDTH / 2 + YOFF)
                    self.initial = (robot, self.angle)

                # Cube
                case "C":
                    x1, y1, z1 = [float(v) for v in values[0:3]]
                    color = RED if values[3].upper() == "R" else GREEN
                    cubes.append((color, Rect(x1 * RESOLUTION - WIDTH/2 + (z1 - 1) * ZSPACING + XOFF, y1 * RESOLUTION - WIDTH/2 - (z1 - 1) * ZSPACING + YOFF, WIDTH, WIDTH)))

                # Platform
                case "P":
                    x1, y1, x2, y2 = [float(v) for v in values]
                    platforms.append((GRAY, (x1 * RESOLUTION + XOFF, y1 * RESOLUTION + YOFF), (x2 * RESOLUTION + XOFF, y2 * RESOLUTION + YOFF), 10))

                # AprilTag
                case "A":
                    x1, y1 = [float(v) for v in values[0:2]]
                    color = LIGHT_RED if values[2].upper() == "R" else LIGHT_GREEN
                    apriltags.append((color, Rect(x1 * RESOLUTION - WIDTH/2 + XOFF, y1 * RESOLUTION - WIDTH/2 + YOFF, WIDTH, WIDTH)))

                case other:
                    raise Exception(f"Did not recognize game object: {other}")
        
        return walls, box, platforms, cubes, apriltags, robot

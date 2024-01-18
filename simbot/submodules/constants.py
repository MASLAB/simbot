"""
MASLAB 2024
Robot mapping constants & pygame imports
"""

from pygame import init, draw, Rect, display, event, QUIT, image, transform, event, key
from pygame import K_w, K_a, K_s, K_d, K_r, KEYDOWN
from pygame.time import Clock
from math import pi, sin, cos, radians, degrees

# Set robot dimensions (in meters)
RADIUS = 50.8 / 1000
WHEELBASE = 228.6 / 1000

# Set maximum robot RPM
MAX_RPM = 200

# Set commonly used colors
BLACK = (0, 0, 0)
RED = (237, 54, 26)
GREEN = (19, 217, 9)
BLUE = (61, 175, 219)
GRAY = (227, 221, 107)
LIGHT_RED = (255, 135, 135)
LIGHT_GREEN = (199, 224, 164)
WHITE = (255, 255, 255)

# Set key speeds
KEY_SPEEDS = {
    K_w: (0.60, 0.60),
    K_a: (0.40, -0.40),
    K_s: (-0.60, -0.60),
    K_d: (-0.40, 0.40),
}

# Set pixels per foot
PPF = 60

# Set pixels per meter
PPM = PPF / 0.3048

# Set tile width (in feet)
TILE_WIDTH = 2

# Set cube width (in pixels)
WIDTH = 20

# Set robot width (in pixels)
ROBOT_WIDTH = PPF

# Set bounding box width (in inches)
BOX_WIDTH_IN = 20

# Set bounding box width (in pixels)
BOX_WIDTH = BOX_WIDTH_IN / 12 * PPF

# Set Z spacing of cubes (in pixels)
ZSPACING = 8

# Set dimensions of board
XTILES = 5
YTILES = 4

# Set size of 2-foot game tile
RESOLUTION = TILE_WIDTH * PPF

# Set X and Y offsets (in pixels)
XOFF = RESOLUTION / 2
YOFF = RESOLUTION / 2

# Set board dimensions
SIZE = XTILES * RESOLUTION + 2 * XOFF, YTILES * RESOLUTION + 2 * YOFF
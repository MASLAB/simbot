"""
MASLAB 2024
Kinematics engine
"""

from .constants import RADIUS, WHEELBASE, MAX_RPM, PPM
from math import pi

# Rename constants
R = RADIUS
B = WHEELBASE

# Convert RPM to rad/s
MAX_OMEGA = MAX_RPM * pi / 30

def to_radians(drive_speed):
    """
    Converts a drive speed (0 to 1) to rotation rates (rad/s)
    """
    return (drive_speed[0] * MAX_OMEGA, drive_speed[1] * MAX_OMEGA)

def convert_velocities(drive_speed):
    """
    Compute linear (px/s) and angular (rad/s) velocity from drive speed (0 to 1)
    """
    # Convert drive speed to rad/s
    omega_l, omega_r = to_radians(drive_speed)

    # Apply kinematics equations
    linear = R / 2 * (omega_r + omega_l) * PPM
    angular = R / B * (omega_r - omega_l)

    # Return result
    return (linear, angular)
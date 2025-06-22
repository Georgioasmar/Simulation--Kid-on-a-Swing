import numpy as np
import math
from typing import Dict, Tuple

def swing_simulation(
    length: float,
    mass: float,
    drag_coeff: float,
    initial_angle: float,
    initial_velocity: float = 0,
    wind_force: float = 1.0,  # added to match GUI input
    dt: float = 0.01,
    duration: float = 600.0
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:

    g = 9.81
    current_time = 0.0
    current_angle = initial_angle
    current_velocity = initial_velocity
    stopTime = -1

    min_cycles = 3
    max_consecutive_rest = 200
    rest_threshold = 0.0001
    cycle_count = 0
    rest_frame_count = 0

    time_points = []
    angles = []
    velocities = []
    positions = []
    energies = []

    while current_time < duration:
        time_points.append(current_time)
        angles.append(current_angle)
        velocities.append(current_velocity)

        x = length * math.sin(current_angle)
        y = -length * math.cos(current_angle)
        positions.append([x, y])

        pe = mass * g * (length - length * math.cos(current_angle))
        ke = 0.5 * mass * (length * current_velocity) ** 2
        energies.append(pe + ke)

        if len(angles) > 1 and current_angle * angles[-2] < 0:
            cycle_count += 1

        if abs(current_velocity) < rest_threshold:
            rest_frame_count += 1
            if rest_frame_count >= max_consecutive_rest:
                stopTime = current_time - 2
                break


        # --- Main Physics ---
        gravity_component = (-g / length) * math.sin(current_angle)

        # Tangential damping modeled as torque, proportional to v^4
        drag_torque = -wind_force * drag_coeff * current_velocity * abs(current_velocity)**3
        drag_accel = drag_torque / (mass * length**2)

        acceleration = gravity_component + drag_accel

        current_velocity += acceleration * dt
        current_angle += current_velocity * dt
        current_time += dt


    return np.array(time_points), {
        'angles': np.array(angles),
        'velocities': np.array(velocities),
        'positions': np.array(positions),
        'energies': np.array(energies),
        'stopping_time': stopTime
    }
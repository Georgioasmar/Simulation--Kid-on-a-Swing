import pygame
import sys
import numpy as np
import math
from physics.Equations import swing_simulation

class SwingVisualizer:
    def __init__(self, params):
        self.params = params
        self.time_points, self.results = swing_simulation(**params)
        self.current_frame = 0
        self.paused = False
        self.show_forces = True
        self.force_scale = 0.1
        self.stop_time = self.results.get('stopping_time', None)
        self.setup_pygame()

        # Load and prepare kid image
        self.original_kid_img = pygame.image.load('visuals/kid.png').convert_alpha()
        self.original_kid_img = pygame.transform.scale(self.original_kid_img, (40, 60))
        self.kid_img = self.original_kid_img
        self.kid_offset_x = 20
        self.kid_offset_y = 60

    def setup_pygame(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1000, 700
        self.SCALE_FACTOR = 100
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Swing Simulation with Force Vectors by Georgio El Asmar & Georgio Yammine Sem 6 ULFG 2025")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 16)
        self.pivot_pos = (self.WIDTH // 2, self.HEIGHT // 4)

    def get_max_velocity_last_2_seconds(self):
        current_time = self.time_points[self.current_frame]
        start_time = current_time - 2
        # Find indices within last 2 seconds
        indices = [i for i, t in enumerate(self.time_points) if start_time <= t <= current_time]
        if not indices:
            return 0
        velocities = [abs(self.results['velocities'][i]) for i in indices]
        return max(velocities)

    def calculate_forces(self):
        angle = self.results['angles'][self.current_frame]
        velocity = self.results['velocities'][self.current_frame]
        mass = self.params['mass']
        length = self.params['length']
        drag_coeff = self.params['drag_coeff']
        wind_force = self.params['wind_force']
        g = 9.81

        # Weight
        weight_force = mass * g
        weight_vector = (0, -weight_force)

        # Tension
        centripetal = mass * length * velocity**2
        radial = mass * g * math.cos(angle)
        tension_magnitude = centripetal + radial
        tension_vector = (
            -tension_magnitude * math.sin(angle),
            tension_magnitude * math.cos(angle)
        )

        # Aero resistance
        if abs(velocity) > 0.001:
            tangent_x = math.cos(angle)
            tangent_y = math.sin(angle)
            if velocity > 0:
                tangent_x *= -1
                tangent_y *= -1
            drag_magnitude = wind_force * drag_coeff * velocity**4
            drag_x = drag_magnitude * tangent_x
            drag_y = drag_magnitude * tangent_y
        else:
            drag_x, drag_y = 0, 0

        aero_vector = (drag_x, drag_y)
        return {
            'weight': weight_vector,
            'tension': tension_vector,
            'aero': aero_vector
        }

    def draw_force_vector(self, start_pos, force, color, label, label_offset_x=0):

        min_length = 10
        screen_force = (force[0], -force[1])
        raw_length = math.hypot(screen_force[0], screen_force[1])
        if raw_length < 0.01:
            return
        scaled_force = (
            screen_force[0] * self.force_scale,
            screen_force[1] * self.force_scale
        )
        scaled_length = math.hypot(scaled_force[0], scaled_force[1])
        if 0.01 <= scaled_length < min_length:
            norm = (scaled_force[0] / scaled_length, scaled_force[1] / scaled_length)
            scaled_force = (norm[0] * min_length, norm[1] * min_length)

        end_pos = (
            start_pos[0] + scaled_force[0],
            start_pos[1] + scaled_force[1]
        )

        pygame.draw.line(self.screen, color, start_pos, end_pos, 2)
        angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
        arrow_size = 10
        pygame.draw.polygon(self.screen, color, [
            end_pos,
            (
                end_pos[0] - arrow_size * math.cos(angle - math.pi / 6),
                end_pos[1] - arrow_size * math.sin(angle - math.pi / 6)
            ),
            (
                end_pos[0] - arrow_size * math.cos(angle + math.pi / 6),
                end_pos[1] - arrow_size * math.sin(angle + math.pi / 6)
            )
        ])

        label_text = self.font.render(label, True, color)
        label_pos = (
            start_pos[0] + scaled_force[0] * 0.5 - 20 + label_offset_x,
            start_pos[1] + scaled_force[1] * 0.5 - 10
        )

        self.screen.blit(label_text, label_pos)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.reset_simulation()
                    elif event.key == pygame.K_f:
                        self.show_forces = not self.show_forces
                    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                        self.force_scale *= 1.2
                    elif event.key == pygame.K_MINUS:
                        self.force_scale /= 1.2

            if not self.paused and self.current_frame < len(self.time_points) - 1:
                self.current_frame += 1

            # Show stopping time once
            if self.stop_time is not None:
                print(f"Swing came to a complete stop at t = {self.stop_time:.2f} seconds.")
                self.stop_time = None

            self.draw_frame()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def reset_simulation(self):
        pygame.quit()
        from params_gui import ParameterInputGUI
        new_params = ParameterInputGUI().run()
        if new_params:
            self.__init__(new_params)

    def draw_frame(self):
        self.screen.fill((240, 240, 240))

        # Show constant parameters
        params_text = [
            f"Length: {self.params['length']:.2f}m",
            f"Mass: {self.params['mass']:.1f}kg",
            f"Drag: {self.params['drag_coeff']:.2f}",
            f"Wind: {self.params['wind_force']:.1f}N"
        ]
        for i, param in enumerate(params_text):
            text = self.font.render(param, True, (0, 0, 0))
            self.screen.blit(text, (self.WIDTH - 200, 10 + i * 20))

        # Get current state
        current_pos = self.results['positions'][self.current_frame]
        seat_pos = self.scale_position(current_pos)

        # Draw rope and pivot
        pygame.draw.line(self.screen, (100, 100, 100), self.pivot_pos, seat_pos, 3)
        pygame.draw.circle(self.screen, (50, 50, 50), self.pivot_pos, 10)

        # Rotate kid image
        current_angle = self.results['angles'][self.current_frame]
        angle_deg = np.degrees(current_angle)
        rotated_img = pygame.transform.rotozoom(self.original_kid_img, angle_deg, 1)
        kid_rect = rotated_img.get_rect(center=(seat_pos[0], seat_pos[1] - self.kid_offset_y))
        self.screen.blit(rotated_img, (
            seat_pos[0] - kid_rect.width // 2,
            seat_pos[1] - kid_rect.height // 2
        ))

        # Draw forces
        if self.show_forces:
            forces = self.calculate_forces()
            self.draw_force_vector(seat_pos, forces['weight'], (255, 0, 0), f"W={forces['weight'][1]:.1f}N")
            self.draw_force_vector(seat_pos, forces['tension'], (0, 0, 255), f"T={np.linalg.norm(forces['tension']):.1f}N")
            label = f"Air Resist={np.linalg.norm(forces['aero']):.1f}N"
            # Shift label left by ~30 pixels
            self.draw_force_vector(seat_pos, forces['aero'], (0, 200, 100), f"Air Resist={np.linalg.norm(forces['aero']):.1f}N", label_offset_x=-30)


            # To shift label inside draw_force_vector, you can add an offset argument or modify label_pos directly:


        # Draw simulation stats
        stats = [
            f"Time: {self.time_points[self.current_frame]:.2f}s",
            f"Angle: {np.degrees(self.results['angles'][self.current_frame]):.1f}°",
            f"Velocity: {self.results['velocities'][self.current_frame]:.2f} rad/s",
            f"2s Max Velocity: {self.get_max_velocity_last_2_seconds():.2f} rad/s",
            f"Controls: SPACE=Pause, R=Reset, F=Toggle Forces",
            f"+/-=Adjust force scale (Current: {self.force_scale:.1f})"
        ]
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, (0, 0, 0))
            self.screen.blit(text, (10, 10 + i * 20))

    def scale_position(self, phys_pos):
        x = self.pivot_pos[0] + phys_pos[0] * self.SCALE_FACTOR
        y = self.pivot_pos[1] - phys_pos[1] * self.SCALE_FACTOR
        return (int(x), int(y))

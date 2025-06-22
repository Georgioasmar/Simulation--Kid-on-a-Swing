import pygame
import pygame_gui
from pygame.locals import *

class ParameterInputGUI:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 700, 500  # Increased width for text boxes
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Swing Parameters Configuration by Georgio El Asmar & Georgio Yammine Sem 6 ULFG 2025")
        
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))
        
        # Default parameters
        self.params = {
            'length': 2.0,
            'mass': 30.0,
            'drag_coeff': 0.1,
            'initial_angle': 45.0,  # Display in degrees
            'initial_velocity': 0.0,
            'wind_force': 1.0,
            'dt': 0.01,
        }
        
        self.create_ui_elements()
        self.setup_event_listeners()
    
    def create_ui_elements(self):
        y_pos = 20
        slider_width = 200
        text_box_width = 100
        label_width = 200
        row_height = 40
        
        # Length Control
        self.length_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, y_pos, label_width, 30),
            text="Swing Length (m):",
            manager=self.manager)
        
        self.length_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(220, y_pos, slider_width, 30),
            start_value=self.params['length'],
            value_range=(0.5, 5.0),
            manager=self.manager)
        
        self.length_text = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(430, y_pos, text_box_width, 30),
            manager=self.manager)
        self.length_text.set_text(str(self.params['length']))
        y_pos += row_height
        
        # Mass Control
        self.mass_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, y_pos, label_width, 30),
            text="Child Mass (kg):",
            manager=self.manager)
        
        self.mass_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(220, y_pos, slider_width, 30),
            start_value=self.params['mass'],
            value_range=(10.0, 100.0),
            manager=self.manager)
        
        self.mass_text = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(430, y_pos, text_box_width, 30),
            manager=self.manager)
        self.mass_text.set_text(str(self.params['mass']))
        y_pos += row_height
        
        # Initial Angle Control
        self.angle_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, y_pos, label_width, 30),
            text="Initial Angle (deg):",
            manager=self.manager)
        
        self.angle_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(220, y_pos, slider_width, 30),
            start_value=self.params['initial_angle'],
            value_range=(0.0, 90.0),
            manager=self.manager)
        
        self.angle_text = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(430, y_pos, text_box_width, 30),
            manager=self.manager)
        self.angle_text.set_text(str(self.params['initial_angle']))
        y_pos += row_height
        
        # Wind Force Control
        self.wind_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, y_pos, label_width, 30),
            text="Wind Resistance (N/m.s^-1):",
            manager=self.manager)
        
        self.wind_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(220, y_pos, slider_width, 30),
            start_value=self.params['wind_force'],
            value_range=(0.0, 100.0),
            manager=self.manager)
        
        self.wind_text = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(430, y_pos, text_box_width, 30),
            manager=self.manager)
        self.wind_text.set_text(str(self.params['wind_force']))
        y_pos += row_height
        
        # Start Button
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(250, y_pos + 40, 200, 50),
            text="Start Simulation",
            manager=self.manager)
    
    def setup_event_listeners(self):
        # Dictionary to map text boxes to their corresponding sliders
        self.text_slider_pairs = {
            'length': (self.length_text, self.length_slider, 0.5, 5.0),
            'mass': (self.mass_text, self.mass_slider, 10.0, 100.0),
            'initial_angle': (self.angle_text, self.angle_slider, 0.0, 90.0),
            'wind_force': (self.wind_text, self.wind_slider, 0.0, 10.0)
        }
    
    def handle_text_input(self, param_name):
        text_entry, slider, min_val, max_val = self.text_slider_pairs[param_name]
        
        try:
            new_value = float(text_entry.get_text())
            # Clamp the value to the slider's range
            clamped_value = max(min_val, min(max_val, new_value))
            
            # Update both the parameter and the slider
            self.params[param_name] = clamped_value
            slider.set_current_value(clamped_value)
            
            # Update text in case we clamped the value
            text_entry.set_text(f"{clamped_value:.2f}")
        except ValueError:
            # If invalid input, revert to current value
            text_entry.set_text(f"{self.params[param_name]:.2f}")
    
    def handle_slider_change(self, param_name):
        _, slider, _, _ = self.text_slider_pairs[param_name]
        self.params[param_name] = slider.get_current_value()
        self.text_slider_pairs[param_name][0].set_text(f"{self.params[param_name]:.2f}")
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            time_delta = clock.tick(60)/1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        running = False
                
                # Handle text entry changes
                if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_element == self.length_text:
                        self.handle_text_input('length')
                    elif event.ui_element == self.mass_text:
                        self.handle_text_input('mass')
                    elif event.ui_element == self.angle_text:
                        self.handle_text_input('initial_angle')
                    elif event.ui_element == self.wind_text:
                        self.handle_text_input('wind_force')
                
                # Handle slider changes
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.length_slider:
                        self.handle_slider_change('length')
                    elif event.ui_element == self.mass_slider:
                        self.handle_slider_change('mass')
                    elif event.ui_element == self.angle_slider:
                        self.handle_slider_change('initial_angle')
                    elif event.ui_element == self.wind_slider:
                        self.handle_slider_change('wind_force')
                
                self.manager.process_events(event)
            
            self.manager.update(time_delta)
            self.screen.fill((240, 240, 240))
            self.manager.draw_ui(self.screen)
            pygame.display.update()
        
        # Convert angle to radians for physics simulation
        self.params['initial_angle'] = self.params['initial_angle'] * (3.14159 / 180)
        return self.params
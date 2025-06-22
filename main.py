from params_gui import ParameterInputGUI
from visuals import SwingVisualizer

def main():
    # First show parameter input GUI
    input_gui = ParameterInputGUI()
    params = input_gui.run()
    
    if params:  # If user didn't cancel
        # Then run visualization with selected parameters
        visualizer = SwingVisualizer(params)
        visualizer.run()

if __name__ == "__main__":
    main()
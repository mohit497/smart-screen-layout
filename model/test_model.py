import numpy as np
import joblib
from model.media_layout_generator import MediaLayoutGenerator

def generate_test_media_data():
    """Generates test media data."""
    return [
        {'type': 'video', 'width': 1280, 'height': 720, 'duration': 30},
        {'type': 'picture', 'width': 600, 'height': 400},
        {'type': 'text', 'text': 'Test text for layout'},
        {'type': 'video', 'width': 1920, 'height': 1080, 'duration': 60},
        {'type': 'picture', 'width': 300, 'height': 200},
        {'type': 'text', 'text': 'Another layout test'},
        {'type': 'video', 'width': 800, 'height': 600, 'duration': 15},
    ]

# Load the trained model
try:
    trained_model = joblib.load('trained_model.joblib')
except FileNotFoundError:
    print("Error: trained_model.joblib not found. Train the model first.")
    exit()

# Generate test data
test_media_objects = generate_test_media_data()

# Create the layout generator
generator = MediaLayoutGenerator(screen_width=1920, screen_height=1080, trained_model=trained_model)

# Generate the layout
layout = generator.generate_layout(test_media_objects)

# Print the layout
import json
print(json.dumps(layout, indent=4))
import numpy as np
from model.media_layout_generator import MediaLayoutGenerator
import time  # Import time for timeout handling

# Initialize the MediaLayoutGenerator
screen_width = 1200
screen_height = 700
generator = MediaLayoutGenerator(screen_width, screen_height)

# Sample media objects for testing
media_objects = [
    {"type": "video", "width": 1280, "height": 720, "duration": 30, "src": "https://videos.pexels.com/video-files/4625518/4625518-uhd_1440_2560_30fps.mp4"},
    {"type": "picture", "width": 600, "height": 400, "src": "https://picsum.photos/200/300"},
    {"type": "text", "width": 800, "height": 200, "text": "Hello World"},
]

# Add a function to validate the layout
def validate_layout(layout):
    for layer_name, items in layout.items():
        total_area = sum(item["width"] * item["height"] for item in items)
        for item in items:
            if item["width"] * item["height"] > total_area / 2:
                print(f"Warning: Large media object {item} in {layer_name} should be in a separate layer.")

try:
    # Define target screen size
    target_screen_width = 1200
    target_screen_height = 700

    # Start timing the layout generation
    start_time = time.time()
    timeout_seconds = 10  # Set a timeout of 10 seconds

    # Generate the layout
    print("Starting layout generation...")
    layout = generator.generate_layout(media_objects, target_screen_width, target_screen_height)

    # Check for timeout
    elapsed_time = time.time() - start_time
    if elapsed_time > timeout_seconds:
        raise TimeoutError("Layout generation exceeded the timeout limit.")

    print(f"Layout generation completed in {elapsed_time:.2f} seconds.")

    # Add default x and y coordinates if missing
    for layer_key, items in layout.items():
        for item in items:
            item.setdefault("x", 0)
            item.setdefault("y", 0)

    # Validate the generated layout
    validate_layout(layout)

    # Print the generated layout
    print("Generated Layout:")
    print(layout)
except TimeoutError as e:
    print(f"Error: {e}")
except KeyError as e:
    print(f"Error generating layout: Missing key {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
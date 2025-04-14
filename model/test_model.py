import numpy as np
from model.media_layout_generator import MediaLayoutGenerator

# Initialize the MediaLayoutGenerator
screen_width = 1920
screen_height = 1080
generator = MediaLayoutGenerator(screen_width, screen_height)

# Sample media objects for testing
media_objects = [
    {"type": "video", "width": 1280, "height": 720, "duration": 30, "src": "https://videos.pexels.com/video-files/4625518/4625518-uhd_1440_2560_30fps.mp4"},
    {"type": "picture", "width": 600, "height": 400, "src": "https://picsum.photos/200/300"},
    {"type": "text", "width": 800, "height": 200, "text": "Hello World"},
]

try:
    # Define target screen size
    target_screen_width = 1280
    target_screen_height = 720

    # Generate the layout
    layout = generator.generate_layout(media_objects, target_screen_width, target_screen_height)

    # Add default x and y coordinates if missing
    for layer_key, items in layout.items():
        if isinstance(items, list):
            for item in items:
                item.setdefault("x", 0)
                item.setdefault("y", 0)

    # Print the generated layout
    print("Generated Layout:")
    print(layout)
except KeyError as e:
    print(f"Error generating layout: Missing key {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
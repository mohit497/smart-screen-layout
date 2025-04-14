import numpy as np
import random
import json
from model.media_layout_generator import MediaLayoutGenerator

def generate_fuzzy_media_data(num_samples=100, screen_sizes=None):
    """Generates realistic media data for training with valid layouts."""
    if screen_sizes is None:
        screen_sizes = [(1920, 1080), (1280, 720), (1024, 768), (800, 600)]
    media_types = ['video', 'picture', 'text']
    data = []
    for _ in range(num_samples):
        screen_width, screen_height = random.choice(screen_sizes)
        num_sections = random.randint(1, 4)  # Divide the screen into 1 to 4 sections
        sections = []
        for _ in range(num_sections):
            section_width = random.randint(screen_width // 4, screen_width // 2)
            section_height = random.randint(screen_height // 4, screen_height // 2)
            x = random.randint(0, screen_width - section_width)
            y = random.randint(0, screen_height - section_height)
            sections.append({'x': x, 'y': y, 'width': section_width, 'height': section_height})

        for section in sections:
            media_type = random.choice(media_types)
            if media_type == 'video':
                width = random.randint(640, max(640, section['width']))
                height = random.randint(360, max(360, section['height']))
                duration = random.randint(5, 120)
                data.append({
                    'type': media_type,
                    'x': section['x'],
                    'y': section['y'],
                    'width': width,
                    'height': height,
                    'duration': duration,
                    'screen_width': screen_width,
                    'screen_height': screen_height
                })
            elif media_type == 'picture':
                width = random.randint(200, max(200, section['width']))
                height = random.randint(150, max(150, section['height']))
                data.append({
                    'type': media_type,
                    'x': section['x'],
                    'y': section['y'],
                    'width': width,
                    'height': height,
                    'screen_width': screen_width,
                    'screen_height': screen_height
                })
            elif media_type == 'text':
                text_length = random.randint(10, 200)
                text = ' '.join(random.choices(['lorem', 'ipsum', 'dolor', 'sit', 'amet'], k=text_length // 5))
                data.append({
                    'type': media_type,
                    'x': section['x'],
                    'y': section['y'],
                    'text': text,
                    'screen_width': screen_width,
                    'screen_height': screen_height
                })
    return data

# Generate fuzzy training data
training_media_objects = generate_fuzzy_media_data(1000)  # Increased samples and added screen sizes

# Save the generated data to a JSON file
with open('training_data.json', 'w') as json_file:
    json.dump(training_media_objects, json_file, indent=4)

print("Training data generated and saved as training_data.json")

# Load the training data from the JSON file
with open('training_data.json', 'r') as json_file:
    training_media_objects = json.load(json_file)

# Initialize the MediaLayoutGenerator and train the model
generator = MediaLayoutGenerator(screen_width=1920, screen_height=1080)

# Extract features from the training data
features = generator._extract_features(training_media_objects)

# Determine the number of clusters
num_clusters = generator._determine_clusters(features)

# Cluster the media data
clusters = generator._cluster_media(features, num_clusters)

# Train the random forest model
generator.train_random_forest(features, clusters)

# Example usage of generate_layout with target screen size
target_screen_width = 1280
target_screen_height = 720
layout = generator.generate_layout(training_media_objects, target_screen_width, target_screen_height)

print("Generated Layout for Training Data:")
print(layout)

print("Model trained and saved as trained_model.joblib")
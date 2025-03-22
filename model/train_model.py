import numpy as np
import random
from model.media_layout_generator import MediaLayoutGenerator

def generate_fuzzy_media_data(num_samples=100):
    """Generates fuzzy media data for training."""
    media_types = ['video', 'picture', 'text']
    data = []
    for _ in range(num_samples):
        media_type = random.choice(media_types)
        if media_type == 'video':
            width = random.randint(640, 1920)
            height = random.randint(360, 1080)
            duration = random.randint(5, 120)
            data.append({'type': media_type, 'width': width, 'height': height, 'duration': duration})
        elif media_type == 'picture':
            width = random.randint(200, 1280)
            height = random.randint(150, 720)
            data.append({'type': media_type, 'width': width, 'height': height})
        elif media_type == 'text':
            text_length = random.randint(10, 200)
            text = ' '.join(random.choices(['lorem', 'ipsum', 'dolor', 'sit', 'amet'], k=text_length // 5))  # Generate dummy text
            data.append({'type': media_type, 'text': text})
    return data

# Generate fuzzy training data
training_media_objects = generate_fuzzy_media_data(200) #increased samples

generator = MediaLayoutGenerator(screen_width=1920, screen_height=1080)
features = generator._extract_features(training_media_objects)
num_clusters = generator._determine_clusters(features)
clusters = generator._cluster_media(features, num_clusters)

generator.train_random_forest(features, clusters)

print("Model trained and saved as trained_model.joblib")
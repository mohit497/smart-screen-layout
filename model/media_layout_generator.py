import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib  # For saving the trained model

class MediaLayoutGenerator:
    def __init__(self, screen_width, screen_height, trained_model=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.trained_model = trained_model

    def _extract_features(self, media_objects):
        features = []
        type_mapping = {'video': 0, 'picture': 1, 'text': 2}  # Example mapping
        for obj in media_objects:
            # Generate default duration for videos if not provided
            duration = obj.get('duration', 60) if obj.get('type') == 'video' else 5
            width = obj.get('width', 0)
            height = obj.get('height', 0)
            area = width * height
            aspect_ratio = width / height if height > 0 else 0
            feature = [
                width,
                height,
                area,  # Add area as a feature
                aspect_ratio,  # Add aspect ratio as a feature
                type_mapping.get(obj.get('type', 'unknown'), -1),  # -1 for unknown types
                duration,  # Use the default or provided duration
                len(obj.get('text', '')) if obj.get('type') == 'text' else 0,  # Added text length
                obj.get('layer', 0)  # Include layer as a feature
            ]
            features.append(feature)
        return np.array(features)

    def _determine_clusters(self, features):
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        wcss = []
        for i in range(1, min(10, len(features)) + 1):
            kmeans = KMeans(n_clusters=i, random_state=42, n_init="auto")
            kmeans.fit(scaled_features)
            wcss.append(kmeans.inertia_)

        diffs = np.diff(wcss)
        diff_ratios = np.diff(diffs)
        optimal_k = np.argmin(diff_ratios) + 2

        return optimal_k

    def _cluster_media(self, features, num_clusters):
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init="auto")
        clusters = kmeans.fit_predict(scaled_features)
        return clusters

    def train_random_forest(self, features, clusters):
        X_train, X_test, y_train, y_test = train_test_split(features, clusters, test_size=0.2, random_state=42)
        rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_classifier.fit(X_train, y_train)
        joblib.dump(rf_classifier, 'trained_model.joblib')  # Save model
        self.trained_model = rf_classifier
        return rf_classifier

    def generate_layout(self, media_objects, target_screen_width, target_screen_height):
        layout = {}
        try:
            # Validate media_objects input
            if not isinstance(media_objects, list):
                raise ValueError("media_objects must be a list of dictionaries.")

            for obj in media_objects:
                if not isinstance(obj, dict):
                    raise ValueError("Each media object must be a dictionary.")

            features = self._extract_features(media_objects)
            num_clusters = self._determine_clusters(features)
            clusters = self._cluster_media(features, num_clusters)

            if self.trained_model is None:
                self.trained_model = joblib.load('trained_model.joblib')  # Load model

            predicted_clusters = self.trained_model.predict(features)

            # Initialize remaining space for each layer
            layer_remaining_space = {}

            max_iterations = 1000  # Set a maximum number of iterations to prevent infinite loops
            iteration_count = 0
            layer_index = 0  # Initialize layer index

            while True:
                # Debugging: Print the current iteration and layer index
                print(f"Iteration: {iteration_count}, Layer Index: {layer_index}")

                # Generate a layer name
                layer_name = f'layer{layer_index}'

                for media in media_objects:
                    media_width = media.get('width', 0)
                    media_height = media.get('height', 0)
                    media_area = media_width * media_height

                    # Find a layer where the media fits
                    if layer_name not in layout:
                        layout[layer_name] = []
                        layer_remaining_space[layer_name] = target_screen_width * target_screen_height

                    # Check if media fits in the current layer
                    if media_area <= layer_remaining_space[layer_name]:
                        layout[layer_name].append(media)
                        layer_remaining_space[layer_name] -= media_area
                        break
                    else:
                        # Move to the next layer if it doesn't fit
                        layer_index += 1

                iteration_count += 1

                # Termination condition: Stop if all media objects are processed
                if self.are_all_media_objects_processed(media_objects):
                    break

                # Safeguard: Stop if iteration limit is reached
                if iteration_count >= max_iterations:
                    raise RuntimeError("Layout generation exceeded maximum iterations. Check your logic.")

            # Remove empty layers (if any)
            layout = {key: value for key, value in layout.items() if value}

        except ValueError as e:
            print(f"Validation Error: {e}")
        except KeyError as e:
            print(f"Error: Missing key {e} in layout generation.")
        except Exception as e:
            print(f"Unexpected error during layout generation: {e}")
        return layout
    
    def is_layout_complete(self):
        # Placeholder for a method to check if the layout is complete
        # Implement the actual logic to determine if the layout is valid and complete
        return True

    def are_all_media_objects_processed(self, media_objects):
        # Placeholder for logic to check if all media objects are processed
        # Implement the actual condition based on your layout generation logic
        return True
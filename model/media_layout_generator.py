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
            feature = [
                obj.get('width', 0),
                obj.get('height', 0),
                type_mapping.get(obj.get('type', 'unknown'), -1),  # -1 for unknown types
                duration,  # Use the default or provided duration
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
            features = self._extract_features(media_objects)
            num_clusters = self._determine_clusters(features)
            clusters = self._cluster_media(features, num_clusters)

            if self.trained_model is None:
                self.trained_model = joblib.load('trained_model.joblib')  # Load model

            predicted_clusters = self.trained_model.predict(features)

            for i, media in enumerate(media_objects):
                layer_index = 1
                max_layers = 10  # Limit the number of layers to prevent infinite loops
                while layer_index <= max_layers:
                    layer_name = f'layer{layer_index}'
                    if layer_name not in layout:
                        layout[layer_name] = []

                    # Check if media fits within the target screen size
                    if media.get('width', 0) <= target_screen_width and media.get('height', 0) <= target_screen_height:
                        layout[layer_name].append(media)
                        break
                    else:
                        # Move to the next layer if media doesn't fit
                        layer_index += 1

                # Handle case where media cannot fit into any layer
                if layer_index > max_layers:
                    print(f"Warning: Media item {media} could not fit into any layer.")

            # Remove empty layers
            layout = {key: value for key, value in layout.items() if value}

        except KeyError as e:
            print(f"Error: Missing key {e} in layout generation.")
        except Exception as e:
            print(f"Unexpected error during layout generation: {e}")
        return layout
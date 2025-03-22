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
            feature = [
                obj.get('width', 0),
                obj.get('height', 0),
                type_mapping.get(obj.get('type', 'unknown'), -1),  # -1 for unknown types
                obj.get('duration', 5) if obj.get('type') == 'video' else 5, #added duration or 5 seconds
                len(obj.get('text', '')) if obj.get('type') == 'text' else 0 # added text length
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

    def generate_layout(self, media_objects):
        try:
            features = self._extract_features(media_objects)
            num_clusters = self._determine_clusters(features)
            clusters = self._cluster_media(features, num_clusters)

            if self.trained_model is None:
                self.trained_model = joblib.load('trained_model.joblib')  # Load model

            predicted_clusters = self.trained_model.predict(features)

            layout = {}
            for i in range(num_clusters):
                layout[f'layer{i + 1}'] = []

            for i, media in enumerate(media_objects):
                layer_name = f'layer{predicted_clusters[i] + 1}'
                media_with_time = media.copy()
                if media.get('type') == 'video':
                    media_with_time['display_time'] = media.get('duration', 5)
                else:
                    media_with_time['display_time'] = 5
                layout[layer_name].append(media_with_time)

            return layout
        except Exception as e:
            print(f"Error generating layout: {e}")
            return {}  # Return empty layout in case of error
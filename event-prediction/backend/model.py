# model.py
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from preprocess import extract_features

class EventModel:
    def __init__(self):
        self.model = GaussianNB()
        self.scaler = StandardScaler()

    def prepare_data(self, df):
        X = []
        y = []

        event_sums = []

        # Step 1: calculate event-level retweet sums
        for event_id, group in df.groupby("event_id"):
            event_sums.append(group["retweets"].sum())

        import numpy as np

        threshold = np.quantile(event_sums, 0.6)

        # Step 2: assign labels correctly
        for event_id, group in df.groupby("event_id"):
            features = extract_features(group)
            X.append(features)

            event_sum = group["retweets"].sum()

            label = 1 if event_sum > threshold else 0
            y.append(label)

        return X, y

    def train(self, df):
        X, y = self.prepare_data(df)

        import numpy as np

        X = np.array(X)
        y = np.array(y)

        # BALANCE DATASET
        class0_idx = np.where(y == 0)[0]
        class1_idx = np.where(y == 1)[0]

        min_count = min(len(class0_idx), len(class1_idx))

        selected_idx = np.concatenate([
            class0_idx[:min_count],
            class1_idx[:min_count]
        ])

        X_balanced = X[selected_idx]
        y_balanced = y[selected_idx]

        print("Balanced labels:", {
            0: sum(y_balanced == 0),
            1: sum(y_balanced == 1)
        })

        # SCALE
        X_balanced = self.scaler.fit_transform(X_balanced)

        self.model.fit(X_balanced, y_balanced)

        return X_balanced.tolist(), y_balanced.tolist()

    def predict(self, features):
        features_scaled = self.scaler.transform([features])

        pred = self.model.predict(features_scaled)[0]
        prob = self.model.predict_proba(features_scaled)[0][1]

        return pred, prob
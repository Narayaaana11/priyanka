from flask import Flask, request, jsonify
from pathlib import Path
from preprocess import load_twitter_dataset, load_tweets_dataset
from model import EventModel
from sklearn.metrics import accuracy_score
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------- LOAD DATA ----------
print("Loading datasets...")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

df1 = load_twitter_dataset(DATA_DIR / "twitter_dataset.csv")
df2 = load_tweets_dataset(DATA_DIR / "tweets.csv")

print("Datasets loaded successfully!")

# ---------- COMBINE DATA ----------
df_combined = pd.concat([df1, df2])

# ---------- TRAIN MODEL ----------
model = EventModel()

print("Training model...")
X_train, y_train = model.train(df_combined)
print("Training completed!")

print("Label distribution:", {0: y_train.count(0), 1: y_train.count(1)})

# ---------- TEST MODEL ----------
print("Testing model...")

X_test, y_test = model.prepare_data(df2)
X_test_scaled = model.scaler.transform(X_test)

preds = model.model.predict(X_test_scaled)

print("Unique Predictions:", set(preds))

probs = model.model.predict_proba(X_test_scaled)
print("Sample Probabilities:", probs[:5])

accuracy = accuracy_score(y_test, preds)

print("Test Accuracy:", accuracy)
print("Sample Predictions:", preds[:10])
print("Actual Values:", y_test[:10])

# ---------- API ----------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # ---------- RAW INPUTS ----------
    raw_tweet_count = data["tweet_count"]
    raw_unique_users = data["unique_users"]
    raw_retweet_sum = data["retweet_sum"]
    raw_time_span = data["time_span"]

    # ---------- SCALE INPUTS ----------
    tweet_count = raw_tweet_count * 2
    unique_users = raw_unique_users * 2
    retweet_sum = raw_retweet_sum * 5
    time_span = raw_time_span

    # ---------- DERIVED FEATURES ----------
    avg_retweets = retweet_sum / tweet_count if tweet_count > 0 else 0
    user_ratio = unique_users / tweet_count if tweet_count > 0 else 0

    features = [
        tweet_count,
        unique_users,
        retweet_sum,
        time_span,
        avg_retweets,
        user_ratio
    ]

    # ---------- EXPLANATIONS ----------
    explanations = []

    explanations.append("High engagement (retweets)" if raw_retweet_sum > 800 else "Low engagement")
    explanations.append("Wide user spread" if raw_unique_users > 40 else "Limited user reach")
    explanations.append("Fast growth" if raw_time_span < 400 else "Slow growth")
    explanations.append("High activity" if raw_tweet_count > 50 else "Low activity")

    # ---------- MODEL PREDICTION ----------
    pred, prob = model.predict(features)

    # =========================================================
    # 🔥 RULE-BASED CORRECTION (FINAL OPTIMIZED ORDER)
    # =========================================================

    # 🚀 1. Viral burst (highest priority)
    if raw_retweet_sum > 1200 and raw_time_span < 250:
        pred = 1
        prob = max(prob, 0.9)

    # ⚡ 2. Strong engagement + fast growth (FIXED MAIN BUG)
    elif raw_retweet_sum > 700 and raw_time_span < 400:
        pred = 1
        prob = max(prob, 0.8)

    # 📈 3. Strong engagement + wide spread
    elif raw_retweet_sum > 800 and raw_unique_users > 40:
        pred = 1
        prob = max(prob, 0.8)

    # ❄️ 4. Very weak engagement
    elif raw_retweet_sum < 100:
        pred = 0
        prob = min(prob, 0.3)

    # 🐢 5. Slow growth penalty (VERY IMPORTANT FIX)
    elif raw_time_span > 800:
        pred = 0
        prob = min(prob, 0.5)

    # =========================================================

    # ---------- FEATURE IMPORTANCE ----------
    total = raw_retweet_sum + raw_unique_users + raw_tweet_count + raw_time_span

    feature_importance = {
        "retweets": round((raw_retweet_sum / total) * 100, 2) if total else 0,
        "users": round((raw_unique_users / total) * 100, 2) if total else 0,
        "tweets": round((raw_tweet_count / total) * 100, 2) if total else 0,
        "time": round((raw_time_span / total) * 100, 2) if total else 0
    }

    # ---------- RESPONSE ----------
    return jsonify({
        "prediction": int(pred),
        "probability": float(prob),
        "explanations": explanations,
        "feature_importance": feature_importance
    })


if __name__ == "__main__":
    app.run(debug=True)

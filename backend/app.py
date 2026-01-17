from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import difflib

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# === Load Model Artifacts ===
MODELS_DIR = "../models"

vectorizer = joblib.load(f"{MODELS_DIR}/vectorizer.joblib")
svd = joblib.load(f"{MODELS_DIR}/svd.joblib")
X_reduced = joblib.load(f"{MODELS_DIR}/X_reduced.joblib")
knn = joblib.load(f"{MODELS_DIR}/knn.joblib")
meta = joblib.load(f"{MODELS_DIR}/meta.joblib")
titles = joblib.load(f"{MODELS_DIR}/titles.joblib")
title_to_index = {t: i for i, t in enumerate(titles)}

TMDB_IMG_BASE = "https://image.tmdb.org/t/p/w500"

# === Helper to find the closest title ===
def find_closest_title(query):
    match = difflib.get_close_matches(query, titles, n=1, cutoff=0.5)
    return match[0] if match else None


# === API Route: /api/recommend ===
@app.route("/api/recommend")
def recommend():
    movie_name = request.args.get("title", "").strip()
    if not movie_name:
        return jsonify({"error": "Please provide a 'title' parameter."}), 400

    # Try exact match, then fuzzy
    idx = title_to_index.get(movie_name)
    if idx is None:
        match = find_closest_title(movie_name)
        if match:
            idx = title_to_index[match]
        else:
            return jsonify({"error": "Movie not found"}), 404

    # Compute recommendations
    distances, indices = knn.kneighbors([X_reduced[idx]], n_neighbors=6)
    recommendations = []
    for i in indices[0]:
        if i == idx:
            continue
        row = meta.iloc[i]
        recommendations.append({
            "title": row["title"],
            "tmdb_id": int(row["id"]),
            "poster_url": (
                TMDB_IMG_BASE + str(row["poster_path"])
                if "poster_path" in row and pd.notnull(row["poster_path"])
                else None
            )

        })
        if len(recommendations) >= 5:
            break

    return jsonify({
        "input": titles[idx],
        "results": recommendations
    })


# === Root endpoint for sanity check ===
@app.route("/")
def home():
    return jsonify({
        "message": "🎬 Movie Recommender API is running!",
        "endpoint": "/api/recommend?title=Inception"
    })


# === Run app ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

"""
Flask API for Movie Recommendation System

This API serves the trained ML model for movie recommendations.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import difflib
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# === Load Model Artifacts ===
MODELS_DIR = "models"

print("🚀 Loading ML models...")
vectorizer = joblib.load(f"{MODELS_DIR}/vectorizer.joblib")
svd = joblib.load(f"{MODELS_DIR}/svd.joblib")
X_reduced = joblib.load(f"{MODELS_DIR}/X_reduced.joblib")
knn = joblib.load(f"{MODELS_DIR}/knn.joblib")
meta = joblib.load(f"{MODELS_DIR}/meta.joblib")
titles = joblib.load(f"{MODELS_DIR}/titles.joblib")
title_to_index = {t: i for i, t in enumerate(titles)}
print("✅ Models loaded successfully!\n")

TMDB_IMG_BASE = "https://image.tmdb.org/t/p/w500"


# === Helper Functions ===
def find_closest_title(query):
    """Find the closest matching title using fuzzy matching."""
    matches = difflib.get_close_matches(query, titles, n=5, cutoff=0.4)
    return matches


def get_wikipedia_url(title):
    """Generate a Wikipedia URL for a movie title."""
    formatted_title = title.replace(" ", "_")
    return f"https://en.wikipedia.org/wiki/{formatted_title}_(film)"


# === API Routes ===

@app.route("/")
def home():
    """Home endpoint with API information."""
    return jsonify({
        "message": "🎬 Movie Recommendation API is running!",
        "version": "1.0",
        "endpoints": {
            "/api/recommend": "GET - Get movie recommendations (param: title)",
            "/api/search": "GET - Search for movies (param: query)",
            "/api/health": "GET - Health check"
        },
        "total_movies": len(titles)
    })


@app.route("/api/health")
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "models_loaded": True,
        "total_movies": len(titles)
    })


@app.route("/api/search")
def search():
    """Search for movies by partial name."""
    query = request.args.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "Please provide a 'query' parameter"}), 400
    
    if len(query) < 2:
        return jsonify({"error": "Query must be at least 2 characters"}), 400
    
    # Find matches
    matches = find_closest_title(query)
    
    if not matches:
        return jsonify({
            "query": query,
            "matches": [],
            "message": "No matches found"
        })
    
    # Get metadata for matches
    results = []
    for title in matches[:10]:
        idx = title_to_index[title]
        row = meta.iloc[idx]
        results.append({
            "title": title,
            "tmdb_id": int(row["id"]) if "id" in row else None,
            "poster_url": (
                TMDB_IMG_BASE + str(row["poster_path"])
                if "poster_path" in row and pd.notnull(row["poster_path"])
                else None
            ),
            "wiki_url": get_wikipedia_url(title),
            "vote_average": float(row["vote_average"]) if "vote_average" in row else None
        })
    
    return jsonify({
        "query": query,
        "matches": results,
        "total": len(results)
    })


@app.route("/api/recommend")
def recommend():
    """Get movie recommendations."""
    movie_name = request.args.get("title", "").strip()
    
    if not movie_name:
        return jsonify({"error": "Please provide a 'title' parameter"}), 400
    
    # Try exact match first
    idx = title_to_index.get(movie_name)
    matched_title = movie_name
    
    # If no exact match, try fuzzy matching
    if idx is None:
        matches = find_closest_title(movie_name)
        if matches:
            matched_title = matches[0]
            idx = title_to_index[matched_title]
        else:
            return jsonify({
                "error": f"Movie '{movie_name}' not found",
                "suggestion": "Try the /api/search endpoint to find similar titles"
            }), 404
    
    # Get recommendations using KNN
    distances, indices = knn.kneighbors([X_reduced[idx]], n_neighbors=6)
    
    recommendations = []
    for i in indices[0]:
        if i == idx:
            continue
        
        row = meta.iloc[i]
        recommendations.append({
            "title": row["title"],
            "tmdb_id": int(row["id"]) if "id" in row else None,
            "poster_url": (
                TMDB_IMG_BASE + str(row["poster_path"])
                if "poster_path" in row and pd.notnull(row["poster_path"])
                else None
            ),
            "wiki_url": get_wikipedia_url(row["title"]),
            "vote_average": float(row["vote_average"]) if "vote_average" in row else None,
            "distance": float(distances[0][list(indices[0]).index(i)])
        })
        
        if len(recommendations) >= 5:
            break
    
    return jsonify({
        "input": movie_name,
        "matched": matched_title,
        "recommendations": recommendations,
        "total": len(recommendations)
    })


# === Error Handlers ===

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# === Run Application ===

if __name__ == "__main__":
    print("=" * 60)
    print("🎬 Movie Recommendation API Server")
    print("=" * 60)
    print(f"📊 Total movies in database: {len(titles)}")
    print("🌐 Starting server on http://0.0.0.0:5000")
    print("=" * 60)
    print()
    
    app.run(host="0.0.0.0", port=5000, debug=True)

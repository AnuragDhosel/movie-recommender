# 🎬 MovieMate - AI Movie Recommender

A complete movie recommendation system built with **PCA**, **K-Nearest Neighbors (KNN)**, and the **MERN** stack (with a Flask ML service).

## 🚀 Project Architecture

- **Frontend**: React (Vite) + Framer Motion (UI/UX)
- **Backend API**: Node.js + Express (Gateway)
- **ML Service**: Python + Flask (Recommendation Engine)
- **Algorithm**: TF-IDF Vectorization + TruncatedSVD (PCA) + KNN (Cosine Similarity)

## 📁 Folder Structure

```
movie-recommender/
├── ml-service/          # Python ML Backend (Flask)
│   ├── src/             # Preprocessing, Training & Viz
│   ├── data/            # TMDB Datasets
│   ├── models/          # Saved Model Artifacts
│   └── app.py           # ML API
├── backend/             # Node.js Gateway (Express)
│   ├── src/             # Controllers & Services
│   └── server.js        # Backend API
└── frontend/            # React Client (Vite)
```

## 🛠️ Setup Instructions

### 1. ML Service (Python)
```bash
cd ml-service
pip install -r requirements.txt
python src/model_builder.py  # Train the model
python app.py               # Start ML API (Port 5000)
```

### 2. Backend Gateway (Node.js)
```bash
cd backend
npm install
npm start                   # Start Gateway (Port 3000)
```

### 3. Frontend (React)
```bash
cd frontend
npm install
npm run dev                 # Start Frontend (Port 5173)
```

## 📊 Evaluation
The model suggests movies based on:
- **Genres**: High correlation between input and recommended movies.
- **Keywords**: Matches specific plot themes.
- **Cast/Director**: Weighting given to similar creative teams.
- **Overview**: Semantic similarity using TF-IDF.

## ✨ Features
- **Fuzzy Search**: Find movies even with typos.
- **PCA Visualization**: High-dimensional movie data reduced to 2D/3D clusters.
- **Responsive UI**: Beautiful glassmorphic design for all devices.
- **Fast Inference**: Sub-second recommendation generation using KNN.
```

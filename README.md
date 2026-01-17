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
│
├── .git/                                    # Git version control
├── .gitignore
├── README.md
├── __pycache__/
├── venv/                                    # Python virtual environment
│
├── backend/                                 # Node.js/Express Backend (API Gateway)
│   ├── .env
│   ├── app.py
│   ├── server.js
│   ├── package.json
│   ├── package-lock.json
│   ├── node_modules/
│   └── src/
│       ├── controllers/
│       │   └── movieController.js
│       ├── routes/
│       │   └── movies.js
│       ├── services/
│       │   └── mlService.js
│       └── utils/
│           └── errorHandler.js
│
├── frontend/                                # React/Vite Frontend
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── package-lock.json
│   ├── node_modules/
│   ├── public/                              # (empty)
│   └── src/
│       ├── App.css
│       ├── App.jsx
│       ├── index.css
│       ├── main.jsx
│       ├── components/
│       │   ├── LoadingSpinner.jsx
│       │   ├── MovieCard.jsx
│       │   ├── MovieGrid.jsx
│       │   └── SearchBar.jsx
│       └── services/
│           └── api.js
│
├── ml-service/                              # Python/Flask ML Service
│   ├── README.md
│   ├── app.py
│   ├── requirements.txt
│   ├── venv/
│   ├── data/
│   │   ├── tmdb_5000_credits.csv
│   │   └── tmdb_5000_movies.csv
│   ├── models/                              # Trained model artifacts
│   │   ├── X_reduced.joblib
│   │   ├── knn.joblib
│   │   ├── meta.joblib
│   │   ├── svd.joblib
│   │   ├── titles.joblib
│   │   └── vectorizer.joblib
│   ├── notebooks/
│   │   └── analysis.ipynb
│   └── src/
│       ├── __pycache__/
│       ├── data_preprocessing.py
│       ├── evaluator.py
│       ├── model_builder.py
│       └── visualizer.py
│
└── docs/                                    # Documentation
    ├── architecture.md
    └── screenshots/
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

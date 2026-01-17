# Movie Recommendation ML Service

This is the Python-based machine learning service that handles data preprocessing, model training, and provides a Flask API for movie recommendations.

## 🛠️ Components

- **`src/data_preprocessing.py`**: Loads the TMDB 5000 dataset, cleans it, and extracts textual features for content-based filtering.
- **`src/model_builder.py`**: Converts text into TF-IDF vectors, applies TruncatedSVD (PCA) for dimensionality reduction, and trains a K-Nearest Neighbors (KNN) model.
- **`src/visualizer.py`**: Generates 2D and 3D PCA visualizations of the movie clusters.
- **`src/evaluator.py`**: Tests the model with sample movies and evaluates genre similarity performance.
- **`app.py`**: A Flask server that exposes the model via HTTP endpoints.

## 🚀 Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the model**:
   ```bash
   python src/model_builder.py
   ```

3. **Run the API**:
   ```bash
   python app.py
   ```

## 📊 Logic & Algorithm

The system suggests similar movies based on **content features**: genres, keywords, overview, cast, and director.
1. **Vectorization**: Uses TF-IDF (Term Frequency-Inverse Document Frequency) to convert text into numerical vectors.
2. **PCA**: Reduces high-dimensional text vectors into 100 components to improve KNN speed and performance.
3. **KNN**: Uses **Cosine Similarity** to find the 5 "nearest" movies in the feature space.




🚀 How to Run the Movie Recommender Project :-

This project consists of three main parts that need to be running simultaneously:

ML Service (Flask) - Handles the recommendation logic.
Backend Gateway (Node.js) - Acts as the bridge between Frontend and ML.
Frontend (React/Vite) - The user interface.


Phase 1: Start the ML Service (Port 5000)
Open a terminal and navigate to the ml-service directory.

Create/Activate Virtual Environment:
cd ml-service
.\venv\Scripts\activate  -> # If venv doesn't exist: python -m venv venv
pip install -r requirements.txt -> Install Dependencies:, if not install
python app.py   -> run python project or Start the API:

The ML service should now be running at http://localhost:5000.

python src/model_builder.py  # to Train the model (one-time setup only)


Phase 2: Start the Backend Gateway (Port 3000)
Open a new terminal and navigate to the backend directory.

cd backend
npm install -> Install Dependencies
npm start -> Start the Server: 
The backend should now be running at http://localhost:3000.


Phase 3: Start the Frontend (Port 5173)
Open a third terminal and navigate to the frontend directory.

cd frontend
npm install -> Install Dependencies:
npm run dev -> Start the Dev Server:

The frontend should now be running at http://localhost:5173.


✅ Summary of URLs:
Frontend UI: http://localhost:5173
Node Backend: http://localhost:3000
Python ML API: http://localhost:5000
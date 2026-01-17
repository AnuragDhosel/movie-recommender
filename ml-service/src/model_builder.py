"""
Model Building Module for Movie Recommendation System

This module builds the ML model using TF-IDF, PCA/SVD, and KNN.
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.neighbors import NearestNeighbors
from data_preprocessing import DataPreprocessor


class MovieRecommenderModel:
    def __init__(self, models_dir='../models'):
        self.models_dir = models_dir
        os.makedirs(models_dir, exist_ok=True)
        
        self.vectorizer = None
        self.svd = None
        self.pca_2d = None
        self.pca_3d = None
        self.X = None
        self.X_reduced = None
        self.X_pca_2d = None
        self.X_pca_3d = None
        self.knn = None
        self.df = None
        self.meta = None
        self.titles = []
        
    def build_vectorizer(self, df):
        """Create TF-IDF vectors from content."""
        print("\n🔤 Converting text to TF-IDF vectors...")
        
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=3,
            stop_words='english',
            max_features=30000
        )
        
        self.X = self.vectorizer.fit_transform(df['content'])
        print(f"✅ TF-IDF matrix shape: {self.X.shape}")
        return self
    
    def apply_dimensionality_reduction(self):
        """Apply SVD for model and PCA for visualization."""
        print("\n🎛️  Applying dimensionality reduction...")
        
        # TruncatedSVD for the main model (works with sparse matrices)
        print("   - TruncatedSVD (100 components) for KNN model...")
        self.svd = TruncatedSVD(n_components=100, random_state=42)
        self.X_reduced = self.svd.fit_transform(self.X)
        explained_var = sum(self.svd.explained_variance_ratio_)
        print(f"     Explained variance: {explained_var:.2%}")
        
        # PCA for 2D visualization
        print("   - PCA (2 components) for 2D visualization...")
        self.pca_2d = TruncatedSVD(n_components=2, random_state=42)
        self.X_pca_2d = self.pca_2d.fit_transform(self.X)
        
        # PCA for 3D visualization
        print("   - PCA (3 components) for 3D visualization...")
        self.pca_3d = TruncatedSVD(n_components=3, random_state=42)
        self.X_pca_3d = self.pca_3d.fit_transform(self.X)
        
        print(f"✅ Dimensionality reduction complete")
        print(f"   - Model features: {self.X_reduced.shape}")
        print(f"   - 2D visualization: {self.X_pca_2d.shape}")
        print(f"   - 3D visualization: {self.X_pca_3d.shape}")
        return self
    
    def build_knn_model(self):
        """Build KNN model using cosine similarity."""
        print("\n🤖 Training KNN model...")
        
        self.knn = NearestNeighbors(
            n_neighbors=6,
            metric='cosine',
            algorithm='brute'
        )
        self.knn.fit(self.X_reduced)
        
        print("✅ KNN model trained successfully")
        return self
    
    def save_models(self):
        """Save all model artifacts."""
        print(f"\n💾 Saving models to '{self.models_dir}'...")
        
        artifacts = {
            'vectorizer.joblib': self.vectorizer,
            'svd.joblib': self.svd,
            'pca_2d.joblib': self.pca_2d,
            'pca_3d.joblib': self.pca_3d,
            'X_reduced.joblib': self.X_reduced,
            'X_pca_2d.joblib': self.X_pca_2d,
            'X_pca_3d.joblib': self.X_pca_3d,
            'knn.joblib': self.knn,
            'meta.joblib': self.meta,
            'titles.joblib': self.titles
        }
        
        for filename, obj in artifacts.items():
            path = os.path.join(self.models_dir, filename)
            joblib.dump(obj, path)
            print(f"   ✓ {filename}")
        
        print("✅ All artifacts saved successfully")
        return self
    
    def load_models(self):
        """Load all model artifacts."""
        print(f"\n📥 Loading models from '{self.models_dir}'...")
        
        self.vectorizer = joblib.load(f"{self.models_dir}/vectorizer.joblib")
        self.svd = joblib.load(f"{self.models_dir}/svd.joblib")
        self.pca_2d = joblib.load(f"{self.models_dir}/pca_2d.joblib")
        self.pca_3d = joblib.load(f"{self.models_dir}/pca_3d.joblib")
        self.X_reduced = joblib.load(f"{self.models_dir}/X_reduced.joblib")
        self.X_pca_2d = joblib.load(f"{self.models_dir}/X_pca_2d.joblib")
        self.X_pca_3d = joblib.load(f"{self.models_dir}/X_pca_3d.joblib")
        self.knn = joblib.load(f"{self.models_dir}/knn.joblib")
        self.meta = joblib.load(f"{self.models_dir}/meta.joblib")
        self.titles = joblib.load(f"{self.models_dir}/titles.joblib")
        
        print("✅ All models loaded successfully")
        return self
    
    def train(self, df, meta):
        """Complete training pipeline."""
        print("\n" + "="*60)
        print("🚀 Starting Model Training Pipeline")
        print("="*60)
        
        self.df = df
        self.meta = meta
        self.titles = df['title'].tolist()
        
        self.build_vectorizer(df) \
            .apply_dimensionality_reduction() \
            .build_knn_model() \
            .save_models()
        
        print("\n" + "="*60)
        print("🎉 Training Complete!")
        print("="*60)
        return self
    
    def recommend(self, movie_title, n=5):
        """Get recommendations for a movie."""
        if movie_title not in self.titles:
            return None
        
        idx = self.titles.index(movie_title)
        distances, indices = self.knn.kneighbors([self.X_reduced[idx]], n_neighbors=n+1)
        
        recommendations = []
        for i in indices[0]:
            if i == idx:
                continue
            recommendations.append({
                'title': self.titles[i],
                'distance': float(distances[0][list(indices[0]).index(i)])
            })
        
        return recommendations[:n]


def main():
    """Main execution for building the model."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Go up one level from src/
    
    data_dir = os.path.join(project_root, 'data')
    models_dir = os.path.join(project_root, 'models')
    
    # Load and preprocess data
    preprocessor = DataPreprocessor(data_dir=data_dir)
    preprocessor.load_datasets() \
                .drop_irrelevant_columns() \
                .handle_missing_values() \
                .extract_features()
    
    df = preprocessor.get_processed_data()
    meta = preprocessor.get_metadata()
    
    # Build and train model
    model = MovieRecommenderModel(models_dir=models_dir)
    model.train(df, meta)
    
    # Test recommendation
    print("\n📽️  Testing recommendation...")
    test_movie = "Avatar"
    recs = model.recommend(test_movie, n=5)
    
    if recs:
        print(f"\nTop 5 movies similar to '{test_movie}':")
        for i, rec in enumerate(recs, 1):
            print(f"   {i}. {rec['title']} (distance: {rec['distance']:.4f})")


if __name__ == "__main__":
    main()

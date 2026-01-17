"""
Evaluation Module for Movie Recommendation System

Tests the recommendation system with sample movies and analyzes results.
"""

import pandas as pd
import numpy as np
import joblib
import ast
from collections import Counter


class ModelEvaluator:
    def __init__(self, models_dir='../models'):
        self.models_dir = models_dir
        self.load_models()
        
    def load_models(self):
        """Load all necessary models and data."""
        print("📥 Loading models for evaluation...")
        
        self.knn = joblib.load(f"{self.models_dir}/knn.joblib")
        self.X_reduced = joblib.load(f"{self.models_dir}/X_reduced.joblib")
        self.meta = joblib.load(f"{self.models_dir}/meta.joblib")
        self.titles = joblib.load(f"{self.models_dir}/titles.joblib")
        
        self.title_to_index = {t: i for i, t in enumerate(self.titles)}
        print("✅ Models loaded")
        
    def extract_genres(self, genres_str):
        """Extract genre names from JSON string."""
        try:
            genres = ast.literal_eval(genres_str)
            return [g['name'] for g in genres if isinstance(g, dict)]
        except:
            return []
    
    def get_recommendations(self, movie_title, n=5):
        """Get recommendations for a given movie."""
        if movie_title not in self.title_to_index:
            return None
        
        idx = self.title_to_index[movie_title]
        distances, indices = self.knn.kneighbors([self.X_reduced[idx]], n_neighbors=n+1)
        
        recommendations = []
        for i in indices[0]:
            if i == idx:
                continue
            
            movie_data = self.meta.iloc[i]
            recommendations.append({
                'title': self.titles[i],
                'genres': self.extract_genres(movie_data['genres']),
                'distance': float(distances[0][list(indices[0]).index(i)]),
                'vote_average': movie_data.get('vote_average', 'N/A')
            })
            
            if len(recommendations) >= n:
                break
        
        return recommendations
    
    def analyze_genre_similarity(self, input_movie, recommendations):
        """Analyze how similar the genres are."""
        input_idx = self.title_to_index[input_movie]
        input_genres = self.extract_genres(self.meta.iloc[input_idx]['genres'])
        
        print(f"\n   Input Movie Genres: {', '.join(input_genres)}")
        
        all_rec_genres = []
        genre_matches = 0
        
        for rec in recommendations:
            rec_genres = rec['genres']
            all_rec_genres.extend(rec_genres)
            
            # Check if any genre matches
            if any(g in input_genres for g in rec_genres):
                genre_matches += 1
        
        match_percentage = (genre_matches / len(recommendations)) * 100
        print(f"   Genre Match: {genre_matches}/{len(recommendations)} ({match_percentage:.1f}%)")
        
        # Most common genres in recommendations
        genre_counter = Counter(all_rec_genres)
        top_genres = genre_counter.most_common(5)
        print(f"   Top Recommended Genres: {', '.join([g[0] for g in top_genres])}")
        
        return match_percentage
    
    def evaluate_sample_movies(self, sample_movies):
        """Evaluate recommendations for multiple sample movies."""
        print("\n" + "="*70)
        print("🎬 EVALUATING MOVIE RECOMMENDATIONS")
        print("="*70)
        
        total_match = 0
        successful_tests = 0
        
        for movie in sample_movies:
            print(f"\n{'='*70}")
            print(f"🎥 Input Movie: {movie}")
            print(f"{'='*70}")
            
            recommendations = self.get_recommendations(movie, n=5)
            
            if not recommendations:
                print(f"   ❌ Movie '{movie}' not found in dataset")
                continue
            
            print(f"\n   Top 5 Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                genres_str = ', '.join(rec['genres'][:3]) if rec['genres'] else 'N/A'
                print(f"   {i}. {rec['title']}")
                print(f"      └─ Genres: {genres_str}")
                print(f"      └─ Rating: {rec['vote_average']}")
                print(f"      └─ Distance: {rec['distance']:.4f}")
            
            # Analyze genre similarity
            match_pct = self.analyze_genre_similarity(movie, recommendations)
            total_match += match_pct
            successful_tests += 1
        
        # Summary
        print(f"\n{'='*70}")
        print("📊 EVALUATION SUMMARY")
        print(f"{'='*70}")
        print(f"Movies Tested: {successful_tests}/{len(sample_movies)}")
        
        if successful_tests > 0:
            avg_match = total_match / successful_tests
            print(f"Average Genre Match: {avg_match:.1f}%")
            
            if avg_match >= 80:
                print("✅ Excellent! The model shows strong genre similarity")
            elif avg_match >= 60:
                print("✅ Good! The model shows decent genre similarity")
            else:
                print("⚠️  Fair. The model could benefit from more tuning")
        
        print("="*70)


def main():
    """Main execution."""
    evaluator = ModelEvaluator(models_dir='../models')
    
    # Sample movies for testing (diverse genres)
    sample_movies = [
        "Avatar",                    # Sci-fi/Action
        "The Dark Knight",          # Action/Crime/Thriller
        "Toy Story"                 # Animation/Family/Comedy
    ]
    
    evaluator.evaluate_sample_movies(sample_movies)


if __name__ == "__main__":
    main()

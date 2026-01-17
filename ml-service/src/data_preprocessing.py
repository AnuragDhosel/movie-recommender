"""
Data Preprocessing Module for Movie Recommendation System

This module handles loading and cleaning the TMDB 5000 dataset.
"""

import pandas as pd
import ast
import os


class DataPreprocessor:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.df = None
        
    def load_datasets(self):
        """Load movies and credits datasets and merge them."""
        print("📂 Loading datasets...")
        movies = pd.read_csv(f"{self.data_dir}/tmdb_5000_movies.csv")
        credits = pd.read_csv(f"{self.data_dir}/tmdb_5000_credits.csv")
        
        # Merge on 'title'
        self.df = movies.merge(credits, on='title', how='inner')
        print(f"✅ Merged dataset shape: {self.df.shape}")
        return self
    
    def drop_irrelevant_columns(self):
        """Remove columns not needed for recommendations."""
        print("🗑️  Dropping irrelevant columns...")
        drop_cols = ['homepage', 'status', 'tagline', 'production_companies', 
                     'production_countries', 'spoken_languages']
        
        for col in drop_cols:
            if col in self.df.columns:
                self.df.drop(columns=col, inplace=True)
        
        print(f"✅ Remaining columns: {list(self.df.columns)}")
        return self
    
    def handle_missing_values(self):
        """Handle missing values in critical columns."""
        print("🔧 Handling missing values...")
        
        # Remove duplicates
        before = len(self.df)
        self.df.drop_duplicates(subset='title', inplace=True)
        print(f"   Removed {before - len(self.df)} duplicate entries")
        
        # Fill missing text fields
        self.df['overview'] = self.df['overview'].fillna('')
        self.df['genres'] = self.df['genres'].fillna('[]')
        self.df['keywords'] = self.df['keywords'].fillna('[]')
        self.df['cast'] = self.df['cast'].fillna('[]')
        self.df['crew'] = self.df['crew'].fillna('[]')
        
        print(f"✅ Missing values handled. Final shape: {self.df.shape}")
        return self
    
    def extract_names(self, obj_str):
        """Extract 'name' values from JSON-like string fields."""
        try:
            items = ast.literal_eval(obj_str)
        except Exception:
            return []
        
        result = []
        for entry in items:
            if isinstance(entry, dict) and entry.get('name'):
                # Remove spaces for better matching
                result.append(entry['name'].replace(" ", ""))
        return result
    
    def get_top_cast(self, obj_str, top_n=3):
        """Return top N cast members from JSON-like cast field."""
        try:
            items = ast.literal_eval(obj_str)
        except Exception:
            return []
        
        names = []
        for i, entry in enumerate(items):
            if i >= top_n:
                break
            if isinstance(entry, dict) and entry.get('name'):
                names.append(entry['name'].replace(" ", ""))
        return names
    
    def get_director(self, obj_str):
        """Extract director name from crew field."""
        try:
            items = ast.literal_eval(obj_str)
        except Exception:
            return ''
        
        for entry in items:
            if isinstance(entry, dict) and entry.get('job') == 'Director':
                return entry.get('name', '').replace(" ", "")
        return ''
    
    def extract_features(self):
        """Extract and combine text features for content-based filtering."""
        print("🔍 Extracting features...")
        
        # Extract structured fields
        self.df['genres_list'] = self.df['genres'].apply(self.extract_names)
        self.df['keywords_list'] = self.df['keywords'].apply(self.extract_names)
        self.df['cast_list'] = self.df['cast'].apply(lambda x: self.get_top_cast(x, top_n=3))
        self.df['director'] = self.df['crew'].apply(self.get_director)
        
        # Combine into content field
        def create_content(row):
            parts = []
            parts.append(row['overview'])
            parts += row['genres_list']
            parts += row['keywords_list']
            parts += row['cast_list']
            if row['director']:
                parts.append(row['director'])
            return " ".join(parts)
        
        self.df['content'] = self.df.apply(create_content, axis=1)
        
        print(f"✅ Features extracted. Sample content length: {len(self.df['content'].iloc[0])}")
        return self
    
    def get_metadata(self):
        """Extract metadata needed for recommendations display."""
        cols_to_keep = []
        for col in ['title', 'id', 'poster_path', 'genres', 'vote_average', 'release_date']:
            if col in self.df.columns:
                cols_to_keep.append(col)
        
        meta = self.df[cols_to_keep].reset_index(drop=True)
        return meta
    
    def get_processed_data(self):
        """Return the processed dataframe."""
        return self.df


def main():
    """Main execution for testing."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Go up one level from src/
    data_dir = os.path.join(project_root, 'data')
    
    preprocessor = DataPreprocessor(data_dir=data_dir)
    preprocessor.load_datasets() \
                .drop_irrelevant_columns() \
                .handle_missing_values() \
                .extract_features()
    
    df = preprocessor.get_processed_data()
    meta = preprocessor.get_metadata()
    
    print(f"\n📊 Processing complete!")
    print(f"   Total movies: {len(df)}")
    print(f"   Metadata columns: {list(meta.columns)}")
    print(f"\n   Sample movie: {df['title'].iloc[0]}")
    print(f"   Content preview: {df['content'].iloc[0][:200]}...")


if __name__ == "__main__":
    main()

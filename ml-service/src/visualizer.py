"""
Visualization Module for Movie Recommendation System

Creates 2D and 3D PCA visualizations of movie clusters.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import ast
from mpl_toolkits.mplot3d import Axes3D


class MovieVisualizer:
    def __init__(self, models_dir='../models'):
        self.models_dir = models_dir
        self.load_data()
        
    def load_data(self):
        """Load necessary data for visualization."""
        print("📥 Loading visualization data...")
        self.X_pca_2d = joblib.load(f"{self.models_dir}/X_pca_2d.joblib")
        self.X_pca_3d = joblib.load(f"{self.models_dir}/X_pca_3d.joblib")
        self.meta = joblib.load(f"{self.models_dir}/meta.joblib")
        print("✅ Data loaded")
        
    def extract_primary_genre(self, genres_str):
        """Extract the primary genre from genres field."""
        try:
            genres = ast.literal_eval(genres_str)
            if genres and len(genres) > 0:
                return genres[0].get('name', 'Unknown')
        except:
            pass
        return 'Unknown'
    
    def create_2d_visualization(self, output_path='../docs/screenshots/pca_2d.png', 
                                sample_size=None):
        """Create 2D PCA visualization with genre colors."""
        print("\n🎨 Creating 2D PCA visualization...")
        
        # Extract primary genres
        self.meta['primary_genre'] = self.meta['genres'].apply(self.extract_primary_genre)
        
        # Sample if dataset is too large
        if sample_size and len(self.meta) > sample_size:
            indices = np.random.choice(len(self.meta), sample_size, replace=False)
            plot_data = self.meta.iloc[indices].copy()
            plot_coords = self.X_pca_2d[indices]
        else:
            plot_data = self.meta.copy()
            plot_coords = self.X_pca_2d
        
        # Get top genres for better visualization
        top_genres = plot_data['primary_genre'].value_counts().head(10).index.tolist()
        plot_data['genre_plot'] = plot_data['primary_genre'].apply(
            lambda x: x if x in top_genres else 'Other'
        )
        
        # Create figure
        plt.figure(figsize=(14, 10))
        
        # Create scatter plot
        genres = plot_data['genre_plot'].unique()
        colors = sns.color_palette('husl', len(genres))
        
        for genre, color in zip(genres, colors):
            mask = plot_data['genre_plot'] == genre
            indices_mask = mask.values
            plt.scatter(
                plot_coords[indices_mask, 0],
                plot_coords[indices_mask, 1],
                c=[color],
                label=genre,
                alpha=0.6,
                s=50,
                edgecolors='white',
                linewidth=0.5
            )
        
        plt.xlabel('First Principal Component', fontsize=12, fontweight='bold')
        plt.ylabel('Second Principal Component', fontsize=12, fontweight='bold')
        plt.title('Movie Clusters - 2D PCA Visualization\n(Colored by Primary Genre)', 
                  fontsize=14, fontweight='bold', pad=20)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True, 
                   shadow=True, fontsize=10)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()
        
        # Save
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ 2D visualization saved to: {output_path}")
        plt.close()
        
    def create_3d_visualization(self, output_path='../docs/screenshots/pca_3d.png',
                                sample_size=None):
        """Create 3D PCA visualization with genre colors."""
        print("\n🎨 Creating 3D PCA visualization...")
        
        # Extract primary genres (if not already done)
        if 'primary_genre' not in self.meta.columns:
            self.meta['primary_genre'] = self.meta['genres'].apply(self.extract_primary_genre)
        
        # Sample if dataset is too large
        if sample_size and len(self.meta) > sample_size:
            indices = np.random.choice(len(self.meta), sample_size, replace=False)
            plot_data = self.meta.iloc[indices].copy()
            plot_coords = self.X_pca_3d[indices]
        else:
            plot_data = self.meta.copy()
            plot_coords = self.X_pca_3d
        
        # Get top genres
        top_genres = plot_data['primary_genre'].value_counts().head(10).index.tolist()
        plot_data['genre_plot'] = plot_data['primary_genre'].apply(
            lambda x: x if x in top_genres else 'Other'
        )
        
        # Create 3D figure
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot by genre
        genres = plot_data['genre_plot'].unique()
        colors = sns.color_palette('husl', len(genres))
        
        for genre, color in zip(genres, colors):
            mask = plot_data['genre_plot'] == genre
            indices_mask = mask.values
            ax.scatter(
                plot_coords[indices_mask, 0],
                plot_coords[indices_mask, 1],
                plot_coords[indices_mask, 2],
                c=[color],
                label=genre,
                alpha=0.6,
                s=50,
                edgecolors='white',
                linewidth=0.5
            )
        
        ax.set_xlabel('PC1', fontsize=11, fontweight='bold')
        ax.set_ylabel('PC2', fontsize=11, fontweight='bold')
        ax.set_zlabel('PC3', fontsize=11, fontweight='bold')
        ax.set_title('Movie Clusters - 3D PCA Visualization\n(Colored by Primary Genre)',
                     fontsize=14, fontweight='bold', pad=20)
        ax.legend(bbox_to_anchor=(1.15, 1), loc='upper left', frameon=True,
                  shadow=True, fontsize=9)
        
        # Save
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ 3D visualization saved to: {output_path}")
        plt.close()
    
    def create_all_visualizations(self, sample_size=2000):
        """Create all visualizations."""
        print("\n" + "="*60)
        print("🎨 Creating All Visualizations")
        print("="*60)
        
        self.create_2d_visualization(sample_size=sample_size)
        self.create_3d_visualization(sample_size=sample_size)
        
        print("\n" + "="*60)
        print("🎉 Visualizations Complete!")
        print("="*60)


def main():
    """Main execution."""
    visualizer = MovieVisualizer(models_dir='../models')
    visualizer.create_all_visualizations(sample_size=2000)


if __name__ == "__main__":
    main()

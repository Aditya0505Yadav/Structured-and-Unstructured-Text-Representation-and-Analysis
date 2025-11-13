"""Data visualization utilities"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import config

class DataVisualizer:
    """Create visualizations from query results"""
    
    def __init__(self):
        sns.set_style("whitegrid")
        self.figure_size = config.FIGURE_SIZE
    
    def visualize(self, df: pd.DataFrame, title: str = "Query Results"):
        """Auto-detect best visualization for data"""
        
        if df.empty or len(df) <= 1:
            print("📊 Not enough data for visualization")
            return
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not numeric_cols:
            print("📊 No numeric data to visualize")
            return
        
        plt.figure(figsize=self.figure_size)
        
        try:
            if len(numeric_cols) == 1 and len(text_cols) >= 1:
                # Bar chart for categorical + numeric
                self._create_bar_chart(df, text_cols[0], numeric_cols[0])
            elif len(numeric_cols) >= 2:
                # Scatter plot for multiple numeric columns
                self._create_scatter_plot(df, numeric_cols[0], numeric_cols[1])
            else:
                # Line plot for single numeric column
                self._create_line_plot(df, numeric_cols[0])
            
            plt.title(title)
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            plt.close()
            print(f"❌ Visualization error: {e}")
    
    def _create_bar_chart(self, df: pd.DataFrame, x_col: str, y_col: str):
        """Create bar chart"""
        plt.bar(range(len(df)), df[y_col], tick_label=df[x_col])
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.xticks(rotation=45, ha='right')
    
    def _create_scatter_plot(self, df: pd.DataFrame, x_col: str, y_col: str):
        """Create scatter plot"""
        plt.scatter(df[x_col], df[y_col], alpha=0.6)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
    
    def _create_line_plot(self, df: pd.DataFrame, y_col: str):
        """Create line plot"""
        plt.plot(df[y_col], marker='o')
        plt.ylabel(y_col)
        plt.xlabel('Index')
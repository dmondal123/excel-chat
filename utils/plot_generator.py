import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
from typing import Dict, Any, Optional, Tuple
import io
import base64

class PlotGenerator:
    """Handle plot generation and visualization"""
    
    def __init__(self):
        self.supported_plot_types = [
            "bar", "line", "scatter", "histogram", "box", 
            "violin", "heatmap", "pie", "area", "funnel"
        ]
    
    def create_plot(self, data: pd.DataFrame, plot_config: Dict[str, Any]) -> Optional[go.Figure]:
        """
        Create plot based on configuration
        
        Args:
            data: DataFrame to plot
            plot_config: Dictionary with plot configuration
                - type: Plot type
                - x: X-axis column
                - y: Y-axis column  
                - title: Plot title
                - color: Color column (optional)
        """
        try:
            plot_type = plot_config.get('type', 'bar').lower()
            
            if plot_type == 'bar':
                return self._create_bar_plot(data, plot_config)
            elif plot_type == 'line':
                return self._create_line_plot(data, plot_config)
            elif plot_type == 'scatter':
                return self._create_scatter_plot(data, plot_config)
            elif plot_type == 'histogram':
                return self._create_histogram(data, plot_config)
            elif plot_type == 'box':
                return self._create_box_plot(data, plot_config)
            elif plot_type == 'heatmap':
                return self._create_heatmap(data, plot_config)
            elif plot_type == 'pie':
                return self._create_pie_chart(data, plot_config)
            elif plot_type == 'area':
                return self._create_area_plot(data, plot_config)
            else:
                st.error(f"Unsupported plot type: {plot_type}")
                return None
                
        except Exception as e:
            st.error(f"Error creating plot: {str(e)}")
            return None
    
    def _create_bar_plot(self, data: pd.DataFrame, config: Dict[str, Any]) -> go.Figure:
        """Create bar plot"""
        x_col = config.get('x')
        y_col = config.get('y')
        title = config.get('title', 'Bar Plot')
        color_col = config.get('color')
        
        if color_col and color_col in data.columns:
            fig = px.bar(data, x=x_col, y=y_col, color=color_col, title=title)
        else:
            fig = px.bar(data, x=x_col, y=y_col, title=title)
        
        return fig
    
    def _create_line_plot(self, data: pd.DataFrame, config: Dict[str, Any]) -> go.Figure:
        """Create line plot"""
        x_col = config.get('x')
        y_col = config.get('y')
        title = config.get('title', 'Line Plot')
        color_col = config.get('color')
        
        if color_col and color_col in data.columns:
            fig = px.line(data, x=x_col, y=y_col, color=color_col, title=title)
        else:
            fig = px.line(data, x=x_col, y=y_col, title=title)
        
        return fig
    
    def _create_scatter_plot(self, data: pd.DataFrame, config: Dict[str, Any]) -> go.Figure:
        """Create scatter plot"""
        x_col = config.get('x')
        y_col = config.get('y')
        title = config.get('title', 'Scatter Plot')
        color_col = config.get('color')
        size_col = config.get('size')
        
        fig = px.scatter(
            data, 
            x=x_col, 
            y=y_col, 
            color=color_col if color_col and color_col in data.columns else None,
            size=size_col if size_col and size_col in data.columns else None,
            title=title
        )
        
        return fig
    
    def _create_histogram(self, data: pd.DataFrame, config: Dict[str, Any]) -> go.Figure:
        """Create histogram"""
        x_col = config.get('x')
        title = config.get('title', 'Histogram')
        bins = config.get('bins', 30)
        
        fig = px.histogram(data, x=x_col, nbins=bins, title=title)
        return fig
    
    def _create_box_plot(self, data: pd.DataFrame, config: Dict[str, Any]) -> go.Figure:
        """Create box plot"""
        x_col = config.get('x')
        y_col = config.get('y')
        title = config.get('title', 'Box Plot')
        
        fig = px.box(data, x=x_col, y=y_col, title=title)
        return fig
    
    def _create_heatmap(self, data: pd.DataFrame, config: Dict[str, Any]) -> go.Figure:
        """Create heatmap for numerical columns"""
        title = config.get('title', 'Correlation Heatmap')
        
        # Calculate correlation matrix for numerical columns
        numeric_data = data.select_dtypes(include=['number'])
        if numeric_data.empty:
            raise ValueError("No numerical columns found for heatmap")
        
        corr_matrix = numeric_data.corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title=title,
            color_continuous_scale='RdBu_r'
        )
        
        return fig
    
    def _create_pie_chart(self, data: pd.DataFrame, config: Dict[str, Any]) -> go.Figure:
        """Create pie chart"""
        values_col = config.get('values')
        names_col = config.get('names')
        title = config.get('title', 'Pie Chart')
        
        if not values_col or not names_col:
            # Create pie chart from value counts
            col = config.get('x') or data.columns[0]
            value_counts = data[col].value_counts()
            fig = px.pie(values=value_counts.values, names=value_counts.index, title=title)
        else:
            fig = px.pie(data, values=values_col, names=names_col, title=title)
        
        return fig
    
    def _create_area_plot(self, data: pd.DataFrame, config: Dict[str, Any]) -> go.Figure:
        """Create area plot"""
        x_col = config.get('x')
        y_col = config.get('y')
        title = config.get('title', 'Area Plot')
        
        fig = px.area(data, x=x_col, y=y_col, title=title)
        return fig
    
    def suggest_plot_type(self, data: pd.DataFrame, x_col: str, y_col: str = None) -> str:
        """Suggest appropriate plot type based on data types"""
        x_dtype = data[x_col].dtype
        
        if y_col is None:
            # Single column analysis
            if pd.api.types.is_numeric_dtype(x_dtype):
                return "histogram"
            else:
                return "pie"
        
        y_dtype = data[y_col].dtype
        
        # Two column analysis
        if pd.api.types.is_numeric_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype):
            return "scatter"
        elif pd.api.types.is_categorical_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype):
            return "bar"
        elif pd.api.types.is_datetime64_any_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype):
            return "line"
        else:
            return "bar"
    
    def get_plot_config_template(self, plot_type: str, columns: list) -> Dict[str, Any]:
        """Get configuration template for specific plot type"""
        templates = {
            "bar": {"type": "bar", "x": columns[0], "y": columns[1] if len(columns) > 1 else None},
            "line": {"type": "line", "x": columns[0], "y": columns[1] if len(columns) > 1 else None},
            "scatter": {"type": "scatter", "x": columns[0], "y": columns[1] if len(columns) > 1 else None},
            "histogram": {"type": "histogram", "x": columns[0]},
            "box": {"type": "box", "x": columns[0], "y": columns[1] if len(columns) > 1 else None},
            "heatmap": {"type": "heatmap"},
            "pie": {"type": "pie", "x": columns[0]},
            "area": {"type": "area", "x": columns[0], "y": columns[1] if len(columns) > 1 else None}
        }
        
        return templates.get(plot_type, templates["bar"])
    
    def export_plot_as_html(self, fig: go.Figure, filename: str = "plot.html") -> str:
        """Export plot as HTML file"""
        html_str = fig.to_html(include_plotlyjs=True)
        
        # Save to file
        filepath = f"data/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_str)
        
        return filepath
    
    def export_plot_as_png(self, fig: go.Figure, filename: str = "plot.png") -> str:
        """Export plot as PNG image"""
        img_bytes = fig.to_image(format="png")
        
        filepath = f"data/{filename}"
        with open(filepath, 'wb') as f:
            f.write(img_bytes)
        
        return filepath 
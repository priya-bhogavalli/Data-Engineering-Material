# Jupyter Notebooks Interview Questions

## Basic Concepts

### 1. What are Jupyter Notebooks and their key features?
**Answer:** Jupyter Notebooks are interactive computing environments for data science and ML. Key features:

- **Interactive Computing**: Mix code, text, and visualizations
- **Multiple Kernels**: Support for Python, R, Scala, Julia
- **Rich Output**: HTML, images, videos, LaTeX, JavaScript
- **Extensibility**: Custom widgets and extensions
- **Collaboration**: Shareable notebooks and version control
- **Integration**: Works with cloud platforms and IDEs

```python
# Basic Jupyter notebook structure
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Data loading and exploration
df = pd.read_csv('data.csv')
print(f"Dataset shape: {df.shape}")
df.head()

# Interactive visualization
plt.figure(figsize=(10, 6))
sns.histplot(df['column'], bins=30)
plt.title('Distribution Analysis')
plt.show()

# Magic commands
%matplotlib inline
%load_ext autoreload
%autoreload 2
%time result = expensive_computation()
%timeit quick_function()
```

### 2. How do you optimize Jupyter Notebooks for performance and collaboration?
**Answer:** Several strategies improve notebook performance and team collaboration.

```python
# Performance optimization techniques

# 1. Memory management
import gc
import psutil

def check_memory_usage():
    """Monitor memory usage"""
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")

# Clear variables when done
del large_dataframe
gc.collect()

# 2. Efficient data loading
# Use chunking for large datasets
chunk_size = 10000
chunks = []
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    processed_chunk = process_data(chunk)
    chunks.append(processed_chunk)

df = pd.concat(chunks, ignore_index=True)

# 3. Vectorized operations instead of loops
# Slow
results = []
for i, row in df.iterrows():
    results.append(row['col1'] * row['col2'])

# Fast
results = df['col1'] * df['col2']

# 4. Use appropriate data types
df['category_col'] = df['category_col'].astype('category')
df['int_col'] = pd.to_numeric(df['int_col'], downcast='integer')

# Collaboration best practices
def setup_notebook_environment():
    """Standard notebook setup for team consistency"""
    
    # Standard imports
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from datetime import datetime, timedelta
    
    # Configuration
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', 100)
    plt.style.use('seaborn-v0_8')
    
    # Random seed for reproducibility
    np.random.seed(42)
    
    print("Environment setup complete")
    return datetime.now()

# Version control friendly practices
def save_notebook_outputs():
    """Save key outputs for version control"""
    
    # Save important dataframes
    df.to_csv('outputs/processed_data.csv', index=False)
    
    # Save plots
    plt.savefig('outputs/analysis_plot.png', dpi=300, bbox_inches='tight')
    
    # Save model results
    results = {
        'accuracy': 0.95,
        'precision': 0.92,
        'recall': 0.89,
        'timestamp': datetime.now().isoformat()
    }
    
    import json
    with open('outputs/model_results.json', 'w') as f:
        json.dump(results, f, indent=2)
```

### 3. How do you create interactive widgets and dashboards?
**Answer:** Jupyter widgets enable interactive data exploration and dashboard creation.

```python
import ipywidgets as widgets
from IPython.display import display, clear_output
import plotly.graph_objects as go
import plotly.express as px

# Basic interactive widgets
def create_interactive_analysis():
    """Create interactive data analysis dashboard"""
    
    # Sample data
    df = px.data.iris()
    
    # Widget controls
    species_dropdown = widgets.Dropdown(
        options=['All'] + list(df['species'].unique()),
        value='All',
        description='Species:'
    )
    
    feature_x = widgets.Dropdown(
        options=df.select_dtypes(include=[np.number]).columns.tolist(),
        value='sepal_length',
        description='X-axis:'
    )
    
    feature_y = widgets.Dropdown(
        options=df.select_dtypes(include=[np.number]).columns.tolist(),
        value='sepal_width', 
        description='Y-axis:'
    )
    
    plot_type = widgets.RadioButtons(
        options=['scatter', 'histogram', 'box'],
        value='scatter',
        description='Plot type:'
    )
    
    output = widgets.Output()
    
    def update_plot(*args):
        """Update plot based on widget values"""
        with output:
            clear_output(wait=True)
            
            # Filter data
            if species_dropdown.value == 'All':
                filtered_df = df
            else:
                filtered_df = df[df['species'] == species_dropdown.value]
            
            # Create plot
            if plot_type.value == 'scatter':
                fig = px.scatter(
                    filtered_df, 
                    x=feature_x.value, 
                    y=feature_y.value,
                    color='species',
                    title=f'{feature_x.value} vs {feature_y.value}'
                )
            elif plot_type.value == 'histogram':
                fig = px.histogram(
                    filtered_df,
                    x=feature_x.value,
                    color='species',
                    title=f'Distribution of {feature_x.value}'
                )
            elif plot_type.value == 'box':
                fig = px.box(
                    filtered_df,
                    x='species',
                    y=feature_x.value,
                    title=f'{feature_x.value} by Species'
                )
            
            fig.show()
    
    # Connect widgets to update function
    species_dropdown.observe(update_plot, names='value')
    feature_x.observe(update_plot, names='value')
    feature_y.observe(update_plot, names='value')
    plot_type.observe(update_plot, names='value')
    
    # Initial plot
    update_plot()
    
    # Layout
    controls = widgets.VBox([
        species_dropdown,
        feature_x,
        feature_y,
        plot_type
    ])
    
    dashboard = widgets.HBox([controls, output])
    display(dashboard)

# Advanced interactive ML model explorer
def create_ml_model_explorer():
    """Interactive ML model parameter explorer"""
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score
    from sklearn.datasets import make_classification
    
    # Generate sample data
    X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)
    
    # Parameter widgets
    n_estimators_slider = widgets.IntSlider(
        value=100,
        min=10,
        max=500,
        step=10,
        description='Trees:'
    )
    
    max_depth_slider = widgets.IntSlider(
        value=10,
        min=1,
        max=20,
        step=1,
        description='Max Depth:'
    )
    
    min_samples_split_slider = widgets.IntSlider(
        value=2,
        min=2,
        max=20,
        step=1,
        description='Min Split:'
    )
    
    cv_folds_slider = widgets.IntSlider(
        value=5,
        min=3,
        max=10,
        step=1,
        description='CV Folds:'
    )
    
    train_button = widgets.Button(
        description='Train Model',
        button_style='success'
    )
    
    results_output = widgets.Output()
    
    def train_model(button):
        """Train model with current parameters"""
        with results_output:
            clear_output(wait=True)
            
            print("Training model...")
            
            # Create model with current parameters
            model = RandomForestClassifier(
                n_estimators=n_estimators_slider.value,
                max_depth=max_depth_slider.value,
                min_samples_split=min_samples_split_slider.value,
                random_state=42
            )
            
            # Cross-validation
            cv_scores = cross_val_score(
                model, X, y, 
                cv=cv_folds_slider.value,
                scoring='accuracy'
            )
            
            # Display results
            print(f"Cross-validation scores: {cv_scores}")
            print(f"Mean accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
            
            # Plot CV scores
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[f'Fold {i+1}' for i in range(len(cv_scores))],
                y=cv_scores,
                name='CV Scores'
            ))
            fig.add_hline(y=cv_scores.mean(), line_dash="dash", 
                         annotation_text=f"Mean: {cv_scores.mean():.4f}")
            fig.update_layout(title="Cross-Validation Scores", yaxis_title="Accuracy")
            fig.show()
    
    train_button.on_click(train_model)
    
    # Layout
    parameter_controls = widgets.VBox([
        n_estimators_slider,
        max_depth_slider,
        min_samples_split_slider,
        cv_folds_slider,
        train_button
    ])
    
    explorer = widgets.VBox([parameter_controls, results_output])
    display(explorer)

# Custom widget for data quality assessment
def create_data_quality_widget(df):
    """Interactive data quality assessment widget"""
    
    column_selector = widgets.Dropdown(
        options=df.columns.tolist(),
        description='Column:'
    )
    
    analysis_output = widgets.Output()
    
    def analyze_column(change):
        """Analyze selected column"""
        with analysis_output:
            clear_output(wait=True)
            
            col_name = change['new']
            col_data = df[col_name]
            
            print(f"Analysis for column: {col_name}")
            print(f"Data type: {col_data.dtype}")
            print(f"Non-null count: {col_data.count()}")
            print(f"Null count: {col_data.isnull().sum()}")
            print(f"Unique values: {col_data.nunique()}")
            
            if col_data.dtype in ['int64', 'float64']:
                print(f"Mean: {col_data.mean():.2f}")
                print(f"Std: {col_data.std():.2f}")
                print(f"Min: {col_data.min()}")
                print(f"Max: {col_data.max()}")
                
                # Histogram
                fig = px.histogram(x=col_data, title=f'Distribution of {col_name}')
                fig.show()
            else:
                # Value counts for categorical
                value_counts = col_data.value_counts().head(10)
                print(f"Top 10 values:\n{value_counts}")
                
                # Bar chart
                fig = px.bar(x=value_counts.index, y=value_counts.values,
                           title=f'Top Values in {col_name}')
                fig.show()
    
    column_selector.observe(analyze_column, names='value')
    
    # Initial analysis
    analyze_column({'new': df.columns[0]})
    
    widget = widgets.VBox([column_selector, analysis_output])
    display(widget)

# Usage
if __name__ == "__main__":
    # Create interactive dashboards
    create_interactive_analysis()
    create_ml_model_explorer()
    
    # Data quality widget
    sample_df = px.data.tips()
    create_data_quality_widget(sample_df)
```

This focused Jupyter Notebooks interview questions set covers essential interactive computing concepts, providing practical examples for optimization, collaboration, and creating interactive dashboards for data science workflows.
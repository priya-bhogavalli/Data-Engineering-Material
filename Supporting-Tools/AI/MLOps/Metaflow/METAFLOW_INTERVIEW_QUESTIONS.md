# Metaflow Interview Questions

## Basic Concepts

### 1. What is Metaflow and its key features?
**Answer:** Metaflow is a Python framework for building and managing ML workflows. Key features:

- **Flow Definition**: Python-native workflow definition
- **Versioning**: Automatic versioning of code, data, and models
- **Scalability**: Easy scaling from laptop to cloud
- **Reproducibility**: Complete experiment reproducibility
- **Collaboration**: Team sharing and deployment
- **Cloud Integration**: AWS/Azure native integration

```python
from metaflow import FlowSpec, step, Parameter, current

class BasicMLFlow(FlowSpec):
    
    learning_rate = Parameter('learning_rate', default=0.01)
    
    @step
    def start(self):
        print("Starting ML workflow")
        self.data_path = "s3://bucket/data.csv"
        self.next(self.load_data)
    
    @step  
    def load_data(self):
        import pandas as pd
        self.df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.df)} rows")
        self.next(self.preprocess)
    
    @step
    def preprocess(self):
        from sklearn.model_selection import train_test_split
        
        X = self.df.drop('target', axis=1)
        y = self.df['target']
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        self.next(self.train)
    
    @step
    def train(self):
        from sklearn.ensemble import RandomForestClassifier
        
        self.model = RandomForestClassifier()
        self.model.fit(self.X_train, self.y_train)
        
        # Calculate accuracy
        self.accuracy = self.model.score(self.X_test, self.y_test)
        print(f"Model accuracy: {self.accuracy}")
        
        self.next(self.end)
    
    @step
    def end(self):
        print(f"Workflow completed with accuracy: {self.accuracy}")

if __name__ == '__main__':
    BasicMLFlow()
```

### 2. How do you handle data and artifacts in Metaflow?
**Answer:** Metaflow provides automatic data versioning and artifact management.

```python
from metaflow import FlowSpec, step, IncludeFile, S3
import pickle

class DataArtifactFlow(FlowSpec):
    
    # Include local files
    config_file = IncludeFile('config', default='config.json')
    
    @step
    def start(self):
        import json
        
        # Load configuration
        self.config = json.loads(self.config_file)
        print(f"Config: {self.config}")
        
        self.next(self.process_data)
    
    @step
    def process_data(self):
        import pandas as pd
        import numpy as np
        
        # Generate or load data
        self.raw_data = pd.DataFrame({
            'feature1': np.random.randn(1000),
            'feature2': np.random.randn(1000),
            'target': np.random.randint(0, 2, 1000)
        })
        
        # Store data artifact
        with S3(s3root='s3://my-bucket/metaflow-artifacts') as s3:
            # Save processed data
            data_path = s3.put('processed_data.csv', self.raw_data.to_csv(index=False))
            self.data_s3_path = data_path
            
            # Save metadata
            metadata = {
                'rows': len(self.raw_data),
                'columns': list(self.raw_data.columns),
                'processing_time': current.utc_datetime
            }
            
            metadata_path = s3.put('metadata.json', json.dumps(metadata))
            self.metadata_path = metadata_path
        
        self.next(self.train_model)
    
    @step
    def train_model(self):
        from sklearn.ensemble import RandomForestClassifier
        import joblib
        
        # Train model
        X = self.raw_data.drop('target', axis=1)
        y = self.raw_data['target']
        
        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(X, y)
        
        # Store model artifact
        with S3(s3root='s3://my-bucket/metaflow-models') as s3:
            model_bytes = pickle.dumps(self.model)
            self.model_path = s3.put('model.pkl', model_bytes)
        
        self.accuracy = self.model.score(X, y)
        
        self.next(self.end)
    
    @step
    def end(self):
        print(f"Model stored at: {self.model_path}")
        print(f"Data stored at: {self.data_s3_path}")
        print(f"Final accuracy: {self.accuracy}")

if __name__ == '__main__':
    DataArtifactFlow()
```

### 3. How do you implement parallel processing and branching?
**Answer:** Metaflow supports parallel execution and dynamic branching for scalable workflows.

```python
from metaflow import FlowSpec, step, parallel, batch

class ParallelMLFlow(FlowSpec):
    
    @step
    def start(self):
        # Define multiple model configurations
        self.model_configs = [
            {'name': 'rf', 'n_estimators': 100, 'max_depth': 10},
            {'name': 'rf', 'n_estimators': 200, 'max_depth': 15},
            {'name': 'xgb', 'learning_rate': 0.1, 'n_estimators': 100},
            {'name': 'xgb', 'learning_rate': 0.01, 'n_estimators': 200}
        ]
        
        # Load common dataset
        import pandas as pd
        import numpy as np
        
        self.data = pd.DataFrame({
            'feature1': np.random.randn(1000),
            'feature2': np.random.randn(1000), 
            'feature3': np.random.randn(1000),
            'target': np.random.randint(0, 2, 1000)
        })
        
        self.next(self.train_models, foreach='model_configs')
    
    @step
    def train_models(self):
        # Each branch trains a different model
        config = self.input
        
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import cross_val_score
        import xgboost as xgb
        
        X = self.data.drop('target', axis=1)
        y = self.data['target']
        
        # Train model based on configuration
        if config['name'] == 'rf':
            model = RandomForestClassifier(
                n_estimators=config['n_estimators'],
                max_depth=config['max_depth'],
                random_state=42
            )
        elif config['name'] == 'xgb':
            model = xgb.XGBClassifier(
                learning_rate=config['learning_rate'],
                n_estimators=config['n_estimators'],
                random_state=42
            )
        
        # Cross-validation
        cv_scores = cross_val_score(model, X, y, cv=5)
        
        # Store results
        self.model_name = f"{config['name']}_{hash(str(config))}"
        self.config = config
        self.cv_mean = cv_scores.mean()
        self.cv_std = cv_scores.std()
        
        # Train final model
        model.fit(X, y)
        self.trained_model = model
        
        print(f"Model {self.model_name}: CV Score = {self.cv_mean:.3f} ± {self.cv_std:.3f}")
        
        self.next(self.join_results)
    
    @step
    def join_results(self, inputs):
        # Collect results from all parallel branches
        self.results = []
        
        for inp in inputs:
            self.results.append({
                'model_name': inp.model_name,
                'config': inp.config,
                'cv_mean': inp.cv_mean,
                'cv_std': inp.cv_std,
                'model': inp.trained_model
            })
        
        # Find best model
        best_result = max(self.results, key=lambda x: x['cv_mean'])
        self.best_model = best_result['model']
        self.best_config = best_result['config']
        self.best_score = best_result['cv_mean']
        
        print(f"Best model: {best_result['model_name']} with score {self.best_score:.3f}")
        
        self.next(self.end)
    
    @step
    def end(self):
        print(f"Workflow completed. Best model config: {self.best_config}")

if __name__ == '__main__':
    ParallelMLFlow()
```

## Intermediate Concepts

### 4. How do you deploy and scale Metaflow workflows?
**Answer:** Metaflow provides seamless scaling from local to cloud execution.

```python
from metaflow import FlowSpec, step, batch, resources, environment

class ScalableMLFlow(FlowSpec):
    
    @step
    def start(self):
        print("Starting scalable workflow")
        self.datasets = ['dataset1.csv', 'dataset2.csv', 'dataset3.csv']
        self.next(self.process_datasets, foreach='datasets')
    
    @batch(cpu=2, memory=4000, image='python:3.8')
    @environment(vars={'PYTHONPATH': '/opt/ml'})
    @step
    def process_datasets(self):
        # This step runs on AWS Batch with specified resources
        dataset_name = self.input
        
        import pandas as pd
        import numpy as np
        from sklearn.preprocessing import StandardScaler
        
        # Simulate large dataset processing
        print(f"Processing {dataset_name} on AWS Batch")
        
        # Generate large dataset
        n_samples = 100000
        data = pd.DataFrame({
            'feature1': np.random.randn(n_samples),
            'feature2': np.random.randn(n_samples),
            'feature3': np.random.randn(n_samples),
            'target': np.random.randint(0, 2, n_samples)
        })
        
        # Heavy preprocessing
        scaler = StandardScaler()
        features = ['feature1', 'feature2', 'feature3']
        data[features] = scaler.fit_transform(data[features])
        
        # Store processed data
        self.processed_data = data
        self.dataset_name = dataset_name
        self.n_samples = len(data)
        
        self.next(self.join_datasets)
    
    @step
    def join_datasets(self, inputs):
        # Combine processed datasets
        import pandas as pd
        
        combined_data = pd.concat([inp.processed_data for inp in inputs], ignore_index=True)
        self.final_dataset = combined_data
        
        print(f"Combined dataset size: {len(combined_data)} samples")
        
        self.next(self.train_large_model)
    
    @batch(cpu=8, memory=16000, gpu=1)
    @step
    def train_large_model(self):
        # Train model on large dataset with GPU
        from sklearn.ensemble import RandomForestClassifier
        
        X = self.final_dataset.drop('target', axis=1)
        y = self.final_dataset['target']
        
        # Large model training
        model = RandomForestClassifier(
            n_estimators=500,
            max_depth=20,
            n_jobs=-1  # Use all available CPUs
        )
        
        print("Training large model on AWS Batch with GPU...")
        model.fit(X, y)
        
        self.model = model
        self.accuracy = model.score(X, y)
        
        self.next(self.end)
    
    @step
    def end(self):
        print(f"Large-scale training completed. Accuracy: {self.accuracy}")

# Production deployment
class ProductionMLFlow(FlowSpec):
    
    @step
    def start(self):
        self.model_version = "v1.0"
        self.next(self.validate_data)
    
    @step
    def validate_data(self):
        # Data validation step
        import pandas as pd
        
        # Load production data
        self.data = pd.read_csv('s3://prod-bucket/latest-data.csv')
        
        # Validation checks
        self.data_quality_score = self._calculate_data_quality()
        
        if self.data_quality_score < 0.8:
            raise ValueError(f"Data quality too low: {self.data_quality_score}")
        
        self.next(self.retrain_model)
    
    @batch(cpu=4, memory=8000)
    @step
    def retrain_model(self):
        # Retrain model with latest data
        from sklearn.ensemble import RandomForestClassifier
        import joblib
        
        X = self.data.drop('target', axis=1)
        y = self.data['target']
        
        model = RandomForestClassifier(n_estimators=200)
        model.fit(X, y)
        
        self.new_accuracy = model.score(X, y)
        
        # Save model
        model_path = f's3://model-bucket/model_{self.model_version}.pkl'
        joblib.dump(model, model_path)
        self.model_path = model_path
        
        self.next(self.deploy_model)
    
    @step
    def deploy_model(self):
        # Deploy model to production
        deployment_config = {
            'model_path': self.model_path,
            'version': self.model_version,
            'accuracy': self.new_accuracy,
            'deployment_time': current.utc_datetime
        }
        
        # Update model registry
        self._update_model_registry(deployment_config)
        
        print(f"Model {self.model_version} deployed with accuracy {self.new_accuracy}")
        
        self.next(self.end)
    
    @step
    def end(self):
        print("Production deployment completed")
    
    def _calculate_data_quality(self):
        # Calculate data quality metrics
        missing_ratio = self.data.isnull().sum().sum() / (len(self.data) * len(self.data.columns))
        return 1 - missing_ratio
    
    def _update_model_registry(self, config):
        # Update model registry (placeholder)
        print(f"Updated model registry: {config}")

if __name__ == '__main__':
    ScalableMLFlow()
```

This focused Metaflow interview questions set covers essential workflow management concepts, providing practical examples for data handling, parallel processing, and production deployment with cloud scaling capabilities.
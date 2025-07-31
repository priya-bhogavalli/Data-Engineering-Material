# Machine Learning Interview Questions

## Basic Level Questions (1-3 years experience)

### 1. What is Machine Learning and how does it relate to data engineering?
**Answer**: Machine Learning is a subset of AI that enables systems to learn and improve from data without explicit programming.

**Data Engineering's Role in ML**:
- **Data Pipeline**: Collect, clean, and prepare data for ML models
- **Feature Engineering**: Transform raw data into ML-ready features
- **Model Serving**: Deploy and serve ML models in production
- **MLOps**: Automate ML workflows and model lifecycle management

```python
# Data pipeline for ML
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Data extraction and preparation
def prepare_ml_data(raw_data):
    """Prepare raw data for ML training."""
    
    # Data cleaning
    df = raw_data.dropna()
    df = df[df['age'] > 0]  # Remove invalid ages
    
    # Feature engineering
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 45, 65, 100], 
                            labels=['young', 'adult', 'middle', 'senior'])
    
    # Encoding categorical variables
    le = LabelEncoder()
    df['category_encoded'] = le.fit_transform(df['category'])
    
    # Feature scaling
    scaler = StandardScaler()
    numeric_features = ['income', 'spending_score', 'age']
    df[numeric_features] = scaler.fit_transform(df[numeric_features])
    
    return df, scaler, le

# ML model training pipeline
def train_model(df):
    """Train ML model with prepared data."""
    
    # Feature selection
    features = ['income', 'spending_score', 'age', 'category_encoded']
    X = df[features]
    y = df['target']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Model training
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Model evaluation
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Training accuracy: {train_score:.3f}")
    print(f"Testing accuracy: {test_score:.3f}")
    
    return model, X_test, y_test
```

### 2. Explain the difference between supervised and unsupervised learning
**Answer**: Supervised learning uses labeled data to predict outcomes, while unsupervised learning finds patterns in unlabeled data.

```python
# Supervised Learning Example - Classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def supervised_learning_example():
    """Customer churn prediction (supervised)."""
    
    # Features: customer behavior data
    # Target: churn (0 = stayed, 1 = churned)
    
    # Load and prepare data
    df = pd.read_csv('customer_data.csv')
    
    features = ['monthly_charges', 'total_charges', 'tenure', 'num_services']
    X = df[features]
    y = df['churn']  # Labeled target variable
    
    # Train model
    model = LogisticRegression()
    model.fit(X, y)
    
    # Make predictions
    predictions = model.predict(X)
    
    print("Supervised Learning - Churn Prediction:")
    print(classification_report(y, predictions))
    
    return model

# Unsupervised Learning Example - Clustering
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def unsupervised_learning_example():
    """Customer segmentation (unsupervised)."""
    
    # Features: customer behavior data
    # No target variable - find hidden patterns
    
    df = pd.read_csv('customer_data.csv')
    
    features = ['monthly_charges', 'total_charges', 'tenure']
    X = df[features]
    
    # Apply K-means clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(X)
    
    # Add cluster labels to data
    df['cluster'] = clusters
    
    # Analyze clusters
    cluster_summary = df.groupby('cluster')[features].mean()
    print("Unsupervised Learning - Customer Segments:")
    print(cluster_summary)
    
    return kmeans, df

# Semi-supervised Learning Example
from sklearn.semi_supervised import LabelSpreading

def semi_supervised_example():
    """Use small labeled dataset with large unlabeled dataset."""
    
    # Scenario: Only 10% of data is labeled
    df = pd.read_csv('customer_data.csv')
    
    # Simulate partially labeled data
    labeled_mask = df.sample(frac=0.1).index
    y_semi = df['churn'].copy()
    y_semi.loc[~y_semi.index.isin(labeled_mask)] = -1  # -1 for unlabeled
    
    features = ['monthly_charges', 'total_charges', 'tenure']
    X = df[features]
    
    # Semi-supervised learning
    model = LabelSpreading()
    model.fit(X, y_semi)
    
    # Predict on all data
    predictions = model.predict(X)
    
    return model, predictions
```

### 3. What are the main types of ML algorithms?
**Answer**: ML algorithms can be categorized by learning type and problem type.

```python
# 1. REGRESSION ALGORITHMS
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def regression_examples():
    """Predict continuous values (e.g., house prices)."""
    
    # Linear Regression
    lr_model = LinearRegression()
    
    # Ridge Regression (L2 regularization)
    ridge_model = Ridge(alpha=1.0)
    
    # Lasso Regression (L1 regularization)
    lasso_model = Lasso(alpha=1.0)
    
    # Random Forest Regression
    rf_model = RandomForestRegressor(n_estimators=100)
    
    return [lr_model, ridge_model, lasso_model, rf_model]

# 2. CLASSIFICATION ALGORITHMS
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

def classification_examples():
    """Predict categories (e.g., spam/not spam)."""
    
    # Logistic Regression
    lr_model = LogisticRegression()
    
    # Decision Tree
    dt_model = DecisionTreeClassifier()
    
    # Random Forest
    rf_model = RandomForestClassifier(n_estimators=100)
    
    # Support Vector Machine
    svm_model = SVC(kernel='rbf')
    
    # Naive Bayes
    nb_model = GaussianNB()
    
    return [lr_model, dt_model, rf_model, svm_model, nb_model]

# 3. CLUSTERING ALGORITHMS
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering

def clustering_examples():
    """Group similar data points."""
    
    # K-Means Clustering
    kmeans = KMeans(n_clusters=3)
    
    # DBSCAN (Density-based)
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    
    # Hierarchical Clustering
    hierarchical = AgglomerativeClustering(n_clusters=3)
    
    return [kmeans, dbscan, hierarchical]

# 4. DIMENSIONALITY REDUCTION
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

def dimensionality_reduction_examples():
    """Reduce feature dimensions while preserving information."""
    
    # Principal Component Analysis
    pca = PCA(n_components=2)
    
    # t-SNE for visualization
    tsne = TSNE(n_components=2, random_state=42)
    
    return [pca, tsne]

# Algorithm selection based on problem type
def select_algorithm(problem_type, data_size, feature_count):
    """Guide for algorithm selection."""
    
    recommendations = {
        'regression': {
            'small_data': 'Linear Regression',
            'medium_data': 'Random Forest',
            'large_data': 'Gradient Boosting',
            'high_dimensional': 'Ridge/Lasso Regression'
        },
        'classification': {
            'small_data': 'Logistic Regression',
            'medium_data': 'Random Forest',
            'large_data': 'XGBoost',
            'text_data': 'Naive Bayes',
            'image_data': 'Neural Networks'
        },
        'clustering': {
            'spherical_clusters': 'K-Means',
            'arbitrary_shapes': 'DBSCAN',
            'hierarchical_structure': 'Agglomerative Clustering'
        }
    }
    
    return recommendations.get(problem_type, {})
```

### 4. How do you evaluate ML model performance?
**Answer**: Use appropriate metrics based on the problem type and business requirements.

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
    mean_squared_error, mean_absolute_error, r2_score,
    roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns

# Classification Metrics
def evaluate_classification_model(y_true, y_pred, y_prob=None):
    """Comprehensive classification evaluation."""
    
    # Basic metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print(f"F1-Score: {f1:.3f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()
    
    # ROC Curve (for binary classification)
    if y_prob is not None and len(np.unique(y_true)) == 2:
        auc = roc_auc_score(y_true, y_prob)
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.3f})')
        plt.plot([0, 1], [0, 1], 'k--', label='Random')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend()
        plt.show()
    
    # Detailed classification report
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred))

# Regression Metrics
def evaluate_regression_model(y_true, y_pred):
    """Comprehensive regression evaluation."""
    
    # Basic metrics
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    print(f"Mean Squared Error: {mse:.3f}")
    print(f"Root Mean Squared Error: {rmse:.3f}")
    print(f"Mean Absolute Error: {mae:.3f}")
    print(f"R² Score: {r2:.3f}")
    
    # Residual plot
    residuals = y_true - y_pred
    
    plt.figure(figsize=(12, 4))
    
    # Predicted vs Actual
    plt.subplot(1, 2, 1)
    plt.scatter(y_pred, y_true, alpha=0.6)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Predicted vs Actual')
    
    # Residual plot
    plt.subplot(1, 2, 2)
    plt.scatter(y_pred, residuals, alpha=0.6)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted')
    plt.ylabel('Residuals')
    plt.title('Residual Plot')
    
    plt.tight_layout()
    plt.show()

# Cross-validation for robust evaluation
from sklearn.model_selection import cross_val_score, StratifiedKFold

def cross_validate_model(model, X, y, cv=5):
    """Perform cross-validation for robust evaluation."""
    
    # For classification
    if len(np.unique(y)) < 10:  # Assume classification if few unique values
        cv_scores = cross_val_score(model, X, y, cv=StratifiedKFold(n_splits=cv))
        metric_name = "Accuracy"
    else:  # Regression
        cv_scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
        metric_name = "R² Score"
    
    print(f"Cross-Validation {metric_name}:")
    print(f"Mean: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    print(f"Individual scores: {cv_scores}")
    
    return cv_scores

# Business metrics
def calculate_business_metrics(y_true, y_pred, cost_matrix=None):
    """Calculate business-relevant metrics."""
    
    if cost_matrix is None:
        # Default cost matrix for binary classification
        # [TN, FP]
        # [FN, TP]
        cost_matrix = np.array([[0, 1], [5, 0]])  # FN costs 5x more than FP
    
    cm = confusion_matrix(y_true, y_pred)
    
    # Calculate total cost
    total_cost = np.sum(cm * cost_matrix)
    
    # Calculate profit/loss
    tp, fp, fn, tn = cm.ravel()
    
    # Example: fraud detection
    fraud_prevented = tp * 100  # $100 per fraud prevented
    false_alarms = fp * 10      # $10 cost per false alarm
    missed_fraud = fn * 500     # $500 cost per missed fraud
    
    net_benefit = fraud_prevented - false_alarms - missed_fraud
    
    print(f"Business Metrics:")
    print(f"Total Cost: ${total_cost}")
    print(f"Net Benefit: ${net_benefit}")
    print(f"Fraud Prevented: ${fraud_prevented}")
    print(f"False Alarm Cost: ${false_alarms}")
    print(f"Missed Fraud Cost: ${missed_fraud}")
```

### 5. What is overfitting and how do you prevent it?
**Answer**: Overfitting occurs when a model learns training data too well, including noise, leading to poor generalization.

```python
import numpy as np
from sklearn.model_selection import validation_curve, learning_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

# Demonstrate overfitting
def demonstrate_overfitting():
    """Show overfitting with polynomial regression."""
    
    # Generate synthetic data
    np.random.seed(42)
    X = np.linspace(0, 1, 100).reshape(-1, 1)
    y = 1.5 * X.ravel() + np.sin(1.5 * np.pi * X.ravel()) + np.random.normal(0, 0.1, X.shape[0])
    
    # Split data
    X_train, X_test = X[:70], X[70:]
    y_train, y_test = y[:70], y[70:]
    
    # Test different polynomial degrees
    degrees = [1, 3, 9, 15]
    
    plt.figure(figsize=(15, 4))
    
    for i, degree in enumerate(degrees):
        plt.subplot(1, 4, i+1)
        
        # Create polynomial features
        poly_features = PolynomialFeatures(degree=degree)
        X_poly_train = poly_features.fit_transform(X_train)
        X_poly_test = poly_features.transform(X_test)
        
        # Fit model
        model = LinearRegression()
        model.fit(X_poly_train, y_train)
        
        # Predictions
        train_score = model.score(X_poly_train, y_train)
        test_score = model.score(X_poly_test, y_test)
        
        # Plot
        X_plot = np.linspace(0, 1, 100).reshape(-1, 1)
        X_plot_poly = poly_features.transform(X_plot)
        y_plot = model.predict(X_plot_poly)
        
        plt.scatter(X_train, y_train, alpha=0.6, label='Train')
        plt.scatter(X_test, y_test, alpha=0.6, label='Test')
        plt.plot(X_plot, y_plot, 'r-', label='Model')
        plt.title(f'Degree {degree}\nTrain: {train_score:.3f}, Test: {test_score:.3f}')
        plt.legend()
    
    plt.tight_layout()
    plt.show()

# Techniques to prevent overfitting
def prevent_overfitting_techniques():
    """Various techniques to prevent overfitting."""
    
    # 1. Regularization
    from sklearn.linear_model import Ridge, Lasso, ElasticNet
    
    # Ridge (L2) regularization
    ridge_model = Ridge(alpha=1.0)
    
    # Lasso (L1) regularization
    lasso_model = Lasso(alpha=1.0)
    
    # Elastic Net (L1 + L2)
    elastic_model = ElasticNet(alpha=1.0, l1_ratio=0.5)
    
    # 2. Cross-validation for hyperparameter tuning
    from sklearn.model_selection import GridSearchCV
    
    param_grid = {'alpha': [0.1, 1.0, 10.0, 100.0]}
    ridge_cv = GridSearchCV(Ridge(), param_grid, cv=5)
    
    # 3. Early stopping (for iterative algorithms)
    from sklearn.ensemble import GradientBoostingClassifier
    
    gb_model = GradientBoostingClassifier(
        n_estimators=1000,
        validation_fraction=0.2,
        n_iter_no_change=5,  # Early stopping
        random_state=42
    )
    
    # 4. Dropout (for neural networks)
    # from tensorflow.keras.layers import Dropout
    # model.add(Dropout(0.5))
    
    # 5. Data augmentation
    def augment_data(X, y, noise_level=0.1):
        """Add noise to training data."""
        X_augmented = X + np.random.normal(0, noise_level, X.shape)
        return np.vstack([X, X_augmented]), np.hstack([y, y])
    
    # 6. Feature selection
    from sklearn.feature_selection import SelectKBest, f_classif
    
    selector = SelectKBest(score_func=f_classif, k=10)
    
    return {
        'regularization': [ridge_model, lasso_model, elastic_model],
        'cross_validation': ridge_cv,
        'early_stopping': gb_model,
        'feature_selection': selector
    }

# Validation curves to detect overfitting
def plot_validation_curve(model, X, y, param_name, param_range):
    """Plot validation curve to detect overfitting."""
    
    train_scores, test_scores = validation_curve(
        model, X, y, param_name=param_name, param_range=param_range,
        cv=5, scoring='accuracy', n_jobs=-1
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(param_range, train_mean, 'o-', color='blue', label='Training score')
    plt.fill_between(param_range, train_mean - train_std, train_mean + train_std, alpha=0.1, color='blue')
    
    plt.plot(param_range, test_mean, 'o-', color='red', label='Cross-validation score')
    plt.fill_between(param_range, test_mean - test_std, test_mean + test_std, alpha=0.1, color='red')
    
    plt.xlabel(param_name)
    plt.ylabel('Score')
    plt.title('Validation Curve')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

# Learning curves to diagnose overfitting
def plot_learning_curve(model, X, y):
    """Plot learning curve to diagnose overfitting."""
    
    train_sizes, train_scores, test_scores = learning_curve(
        model, X, y, cv=5, n_jobs=-1, train_sizes=np.linspace(0.1, 1.0, 10)
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, 'o-', color='blue', label='Training score')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='blue')
    
    plt.plot(train_sizes, test_mean, 'o-', color='red', label='Cross-validation score')
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1, color='red')
    
    plt.xlabel('Training Set Size')
    plt.ylabel('Score')
    plt.title('Learning Curve')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()
```

## Intermediate Level Questions (3-5 years experience)

### 6. How do you handle imbalanced datasets?
**Answer**: Use sampling techniques, cost-sensitive learning, and appropriate evaluation metrics.

```python
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler, TomekLinks
from imblearn.combine import SMOTETomek
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def handle_imbalanced_data():
    """Techniques for handling imbalanced datasets."""
    
    # Generate imbalanced dataset
    from sklearn.datasets import make_classification
    
    X, y = make_classification(
        n_samples=10000, n_features=20, n_informative=10,
        n_redundant=10, n_clusters_per_class=1, weights=[0.95, 0.05],
        random_state=42
    )
    
    print(f"Original class distribution: {np.bincount(y)}")
    
    # 1. Oversampling techniques
    
    # SMOTE (Synthetic Minority Oversampling Technique)
    smote = SMOTE(random_state=42)
    X_smote, y_smote = smote.fit_resample(X, y)
    print(f"SMOTE class distribution: {np.bincount(y_smote)}")
    
    # ADASYN (Adaptive Synthetic Sampling)
    adasyn = ADASYN(random_state=42)
    X_adasyn, y_adasyn = adasyn.fit_resample(X, y)
    print(f"ADASYN class distribution: {np.bincount(y_adasyn)}")
    
    # 2. Undersampling techniques
    
    # Random undersampling
    undersampler = RandomUnderSampler(random_state=42)
    X_under, y_under = undersampler.fit_resample(X, y)
    print(f"Undersampled class distribution: {np.bincount(y_under)}")
    
    # Tomek links removal
    tomek = TomekLinks()
    X_tomek, y_tomek = tomek.fit_resample(X, y)
    print(f"Tomek links class distribution: {np.bincount(y_tomek)}")
    
    # 3. Combined techniques
    
    # SMOTE + Tomek links
    smote_tomek = SMOTETomek(random_state=42)
    X_combined, y_combined = smote_tomek.fit_resample(X, y)
    print(f"SMOTE+Tomek class distribution: {np.bincount(y_combined)}")
    
    return {
        'original': (X, y),
        'smote': (X_smote, y_smote),
        'adasyn': (X_adasyn, y_adasyn),
        'undersampled': (X_under, y_under),
        'combined': (X_combined, y_combined)
    }

# Cost-sensitive learning
def cost_sensitive_learning(X, y):
    """Use class weights to handle imbalance."""
    
    # Calculate class weights
    from sklearn.utils.class_weight import compute_class_weight
    
    classes = np.unique(y)
    class_weights = compute_class_weight('balanced', classes=classes, y=y)
    class_weight_dict = dict(zip(classes, class_weights))
    
    print(f"Class weights: {class_weight_dict}")
    
    # Models with class weights
    models = {
        'rf_balanced': RandomForestClassifier(class_weight='balanced', random_state=42),
        'rf_custom': RandomForestClassifier(class_weight=class_weight_dict, random_state=42),
        'rf_none': RandomForestClassifier(class_weight=None, random_state=42)
    }
    
    # Compare models
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        results[name] = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1': f1_score(y_test, y_pred, average='weighted')
        }
    
    return results

# Evaluation metrics for imbalanced data
def evaluate_imbalanced_model(y_true, y_pred, y_prob=None):
    """Comprehensive evaluation for imbalanced datasets."""
    
    from sklearn.metrics import (
        precision_recall_curve, average_precision_score,
        matthews_corrcoef, cohen_kappa_score
    )
    
    # Basic metrics
    print("Classification Report:")
    print(classification_report(y_true, y_pred))
    
    # Matthews Correlation Coefficient
    mcc = matthews_corrcoef(y_true, y_pred)
    print(f"Matthews Correlation Coefficient: {mcc:.3f}")
    
    # Cohen's Kappa
    kappa = cohen_kappa_score(y_true, y_pred)
    print(f"Cohen's Kappa: {kappa:.3f}")
    
    if y_prob is not None:
        # Precision-Recall curve (better than ROC for imbalanced data)
        precision, recall, _ = precision_recall_curve(y_true, y_prob)
        ap_score = average_precision_score(y_true, y_prob)
        
        plt.figure(figsize=(12, 4))
        
        # Precision-Recall curve
        plt.subplot(1, 2, 1)
        plt.plot(recall, precision, label=f'AP Score = {ap_score:.3f}')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.legend()
        
        # ROC curve
        plt.subplot(1, 2, 2)
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        auc_score = roc_auc_score(y_true, y_prob)
        plt.plot(fpr, tpr, label=f'AUC = {auc_score:.3f}')
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend()
        
        plt.tight_layout()
        plt.show()

# Threshold optimization for imbalanced data
def optimize_threshold(y_true, y_prob):
    """Find optimal threshold for imbalanced classification."""
    
    from sklearn.metrics import precision_recall_curve, f1_score
    
    # Calculate precision-recall curve
    precision, recall, thresholds = precision_recall_curve(y_true, y_prob)
    
    # Calculate F1 scores for each threshold
    f1_scores = 2 * (precision[:-1] * recall[:-1]) / (precision[:-1] + recall[:-1])
    
    # Find optimal threshold
    optimal_idx = np.argmax(f1_scores)
    optimal_threshold = thresholds[optimal_idx]
    optimal_f1 = f1_scores[optimal_idx]
    
    print(f"Optimal threshold: {optimal_threshold:.3f}")
    print(f"Optimal F1 score: {optimal_f1:.3f}")
    
    # Plot threshold analysis
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(thresholds, precision[:-1], label='Precision')
    plt.plot(thresholds, recall[:-1], label='Recall')
    plt.plot(thresholds, f1_scores, label='F1 Score')
    plt.axvline(optimal_threshold, color='red', linestyle='--', label='Optimal')
    plt.xlabel('Threshold')
    plt.ylabel('Score')
    plt.title('Threshold vs Metrics')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(recall[:-1], precision[:-1])
    plt.scatter(recall[optimal_idx], precision[optimal_idx], 
                color='red', s=100, label='Optimal Point')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    return optimal_threshold
```

This comprehensive set covers ML fundamentals through advanced techniques with practical data engineering examples. The questions progress from basic concepts to complex real-world scenarios.
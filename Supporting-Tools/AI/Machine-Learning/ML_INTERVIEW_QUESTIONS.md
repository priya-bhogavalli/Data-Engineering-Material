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

### 7. What is feature engineering and why is it important?
**Answer**: Feature engineering transforms raw data into meaningful inputs for ML models.

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.decomposition import PCA
from datetime import datetime

# Feature Engineering Pipeline
class FeatureEngineer:
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.feature_names = []
    
    def create_temporal_features(self, df, date_column):
        """Extract temporal features from datetime."""
        df = df.copy()
        df[date_column] = pd.to_datetime(df[date_column])
        
        # Extract time components
        df['year'] = df[date_column].dt.year
        df['month'] = df[date_column].dt.month
        df['day'] = df[date_column].dt.day
        df['dayofweek'] = df[date_column].dt.dayofweek
        df['hour'] = df[date_column].dt.hour
        df['quarter'] = df[date_column].dt.quarter
        
        # Cyclical encoding for periodic features
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        
        # Business features
        df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)
        df['is_month_end'] = (df[date_column].dt.is_month_end).astype(int)
        df['is_quarter_end'] = (df[date_column].dt.is_quarter_end).astype(int)
        
        return df
```

This comprehensive set covers ML fundamentals through advanced techniques with practical data engineering examples. The questions progress from basic concepts to complex real-world scenarios.

### 8. How do you handle missing data in ML projects?
**Answer**: Multiple strategies for dealing with missing values based on data characteristics.

```python
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
from sklearn.experimental import enable_iterative_imputer

# Missing Data Analysis
class MissingDataAnalyzer:
    def __init__(self):
        self.missing_patterns = {}
        self.imputers = {}
    
    def analyze_missing_data(self, df):
        """Comprehensive missing data analysis."""
        
        # Missing data summary
        missing_summary = pd.DataFrame({
            'column': df.columns,
            'missing_count': df.isnull().sum(),
            'missing_percentage': (df.isnull().sum() / len(df)) * 100,
            'dtype': df.dtypes
        }).sort_values('missing_percentage', ascending=False)
        
        print("Missing Data Summary:")
        print(missing_summary[missing_summary['missing_count'] > 0])
        
        return missing_summary
    
    def simple_imputation(self, df, strategy='mean'):
        """Simple imputation strategies."""
        df_imputed = df.copy()
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        # Numeric imputation
        if len(numeric_columns) > 0:
            if strategy in ['mean', 'median']:
                imputer = SimpleImputer(strategy=strategy)
                df_imputed[numeric_columns] = imputer.fit_transform(df[numeric_columns])
            elif strategy == 'zero':
                df_imputed[numeric_columns] = df[numeric_columns].fillna(0)
        
        # Categorical imputation
        if len(categorical_columns) > 0:
            if strategy == 'mode':
                for col in categorical_columns:
                    mode_value = df[col].mode().iloc[0] if not df[col].mode().empty else 'Unknown'
                    df_imputed[col] = df[col].fillna(mode_value)
        
        return df_imputed
    
    def advanced_imputation(self, df, method='knn'):
        """Advanced imputation methods."""
        df_numeric = df.select_dtypes(include=[np.number])
        
        if method == 'knn':
            # K-Nearest Neighbors imputation
            imputer = KNNImputer(n_neighbors=5)
            df_imputed = pd.DataFrame(
                imputer.fit_transform(df_numeric),
                columns=df_numeric.columns,
                index=df_numeric.index
            )
            
        elif method == 'iterative':
            # Iterative imputation (MICE)
            imputer = IterativeImputer(random_state=42, max_iter=10)
            df_imputed = pd.DataFrame(
                imputer.fit_transform(df_numeric),
                columns=df_numeric.columns,
                index=df_numeric.index
            )
        
        return df_imputed
```

### 9. What are ensemble methods and how do they work?
**Answer**: Ensemble methods combine multiple models to create stronger predictors.

```python
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier,
    AdaBoostClassifier, VotingClassifier, BaggingClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

# Ensemble Methods Implementation
class EnsembleMethods:
    def __init__(self):
        self.models = {}
        self.ensemble_models = {}
    
    def bagging_example(self, X, y):
        """Bootstrap Aggregating (Bagging) example."""
        
        # Random Forest (bagging with decision trees)
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        # Custom bagging with different base estimators
        bagging_model = BaggingClassifier(
            base_estimator=DecisionTreeClassifier(max_depth=5),
            n_estimators=50,
            random_state=42,
            n_jobs=-1
        )
        
        # Evaluate models
        rf_scores = cross_val_score(rf_model, X, y, cv=5)
        bagging_scores = cross_val_score(bagging_model, X, y, cv=5)
        
        print("Bagging Results:")
        print(f"Random Forest CV Score: {rf_scores.mean():.3f} (+/- {rf_scores.std() * 2:.3f})")
        print(f"Custom Bagging CV Score: {bagging_scores.mean():.3f} (+/- {bagging_scores.std() * 2:.3f})")
        
        return {'random_forest': rf_model, 'bagging': bagging_model}
    
    def boosting_example(self, X, y):
        """Boosting algorithms example."""
        
        # AdaBoost
        ada_model = AdaBoostClassifier(
            base_estimator=DecisionTreeClassifier(max_depth=1),
            n_estimators=100,
            learning_rate=1.0,
            random_state=42
        )
        
        # Gradient Boosting
        gb_model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        
        # Evaluate models
        models = {
            'AdaBoost': ada_model,
            'Gradient Boosting': gb_model
        }
        
        print("Boosting Results:")
        for name, model in models.items():
            scores = cross_val_score(model, X, y, cv=5)
            print(f"{name} CV Score: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
        
        return models
    
    def voting_ensemble(self, X, y):
        """Voting ensemble combining different algorithms."""
        
        # Base models
        base_models = [
            ('lr', LogisticRegression(random_state=42)),
            ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
        ]
        
        # Hard voting
        hard_voting = VotingClassifier(
            estimators=base_models,
            voting='hard'
        )
        
        # Soft voting (uses predicted probabilities)
        soft_voting = VotingClassifier(
            estimators=base_models,
            voting='soft'
        )
        
        # Evaluate voting ensembles
        hard_scores = cross_val_score(hard_voting, X, y, cv=5)
        soft_scores = cross_val_score(soft_voting, X, y, cv=5)
        
        print("Voting Ensemble Results:")
        print(f"Hard Voting CV Score: {hard_scores.mean():.3f} (+/- {hard_scores.std() * 2:.3f})")
        print(f"Soft Voting CV Score: {soft_scores.mean():.3f} (+/- {soft_scores.std() * 2:.3f})")
        
        return {'hard_voting': hard_voting, 'soft_voting': soft_voting}
```

### 10. How do you perform hyperparameter tuning?
**Answer**: Systematic approaches to optimize model parameters for better performance.

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import make_scorer, f1_score
import optuna

# Hyperparameter Tuning Methods
class HyperparameterTuner:
    def __init__(self):
        self.best_params = {}
        self.best_scores = {}
    
    def grid_search_tuning(self, X, y, model, param_grid, scoring='accuracy'):
        """Grid search for exhaustive parameter search."""
        
        grid_search = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=5,
            scoring=scoring,
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X, y)
        
        print(f"Grid Search Results:")
        print(f"Best Score: {grid_search.best_score_:.3f}")
        print(f"Best Parameters: {grid_search.best_params_}")
        
        return grid_search.best_estimator_, grid_search.best_params_
    
    def random_search_tuning(self, X, y, model, param_distributions, n_iter=100):
        """Random search for efficient parameter exploration."""
        
        random_search = RandomizedSearchCV(
            estimator=model,
            param_distributions=param_distributions,
            n_iter=n_iter,
            cv=5,
            scoring='accuracy',
            n_jobs=-1,
            random_state=42,
            verbose=1
        )
        
        random_search.fit(X, y)
        
        print(f"Random Search Results:")
        print(f"Best Score: {random_search.best_score_:.3f}")
        print(f"Best Parameters: {random_search.best_params_}")
        
        return random_search.best_estimator_, random_search.best_params_
    
    def bayesian_optimization(self, X, y):
        """Bayesian optimization using Optuna."""
        
        def objective(trial):
            # Define hyperparameter search space
            n_estimators = trial.suggest_int('n_estimators', 50, 300)
            max_depth = trial.suggest_int('max_depth', 3, 20)
            min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
            min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 10)
            
            # Create model with suggested parameters
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                random_state=42,
                n_jobs=-1
            )
            
            # Evaluate model using cross-validation
            scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
            return scores.mean()
        
        # Create study and optimize
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=100)
        
        print(f"Bayesian Optimization Results:")
        print(f"Best Score: {study.best_value:.3f}")
        print(f"Best Parameters: {study.best_params}")
        
        # Create best model
        best_model = RandomForestClassifier(**study.best_params, random_state=42)
        
        return best_model, study.best_params
    
    def compare_tuning_methods(self, X, y):
        """Compare different hyperparameter tuning approaches."""
        
        # Base model
        base_model = RandomForestClassifier(random_state=42)
        
        # Parameter spaces
        grid_params = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15],
            'min_samples_split': [2, 5, 10]
        }
        
        random_params = {
            'n_estimators': [50, 100, 150, 200, 250, 300],
            'max_depth': [3, 5, 7, 10, 15, 20],
            'min_samples_split': [2, 5, 10, 15, 20],
            'min_samples_leaf': [1, 2, 5, 10]
        }
        
        results = {}\n        
        # Grid Search
        print("=== GRID SEARCH ===\")
        grid_model, grid_params_best = self.grid_search_tuning(X, y, base_model, grid_params)
        grid_score = cross_val_score(grid_model, X, y, cv=5).mean()
        results['grid_search'] = {'model': grid_model, 'score': grid_score, 'params': grid_params_best}
        
        # Random Search
        print("\\n=== RANDOM SEARCH ===\")
        random_model, random_params_best = self.random_search_tuning(X, y, base_model, random_params)
        random_score = cross_val_score(random_model, X, y, cv=5).mean()
        results['random_search'] = {'model': random_model, 'score': random_score, 'params': random_params_best}
        
        # Bayesian Optimization
        print("\\n=== BAYESIAN OPTIMIZATION ===\")
        bayes_model, bayes_params_best = self.bayesian_optimization(X, y)
        bayes_score = cross_val_score(bayes_model, X, y, cv=5).mean()
        results['bayesian'] = {'model': bayes_model, 'score': bayes_score, 'params': bayes_params_best}
        
        # Summary
        print("\\n=== COMPARISON SUMMARY ===\")
        for method, result in results.items():
            print(f"{method.upper()}: Score = {result['score']:.3f}")
        
        return results
```

### 11. What is cross-validation and why is it important?
**Answer**: Cross-validation provides robust model evaluation by testing on multiple data splits.

```python
from sklearn.model_selection import (
    KFold, StratifiedKFold, TimeSeriesSplit, LeaveOneOut,
    cross_val_score, cross_validate, validation_curve
)
import matplotlib.pyplot as plt

# Cross-Validation Techniques
class CrossValidationMethods:
    def __init__(self):
        self.cv_results = {}
    
    def k_fold_cv(self, X, y, model, k=5):
        """Standard K-Fold cross-validation."""
        
        kfold = KFold(n_splits=k, shuffle=True, random_state=42)
        
        # Simple cross-validation
        scores = cross_val_score(model, X, y, cv=kfold, scoring='accuracy')
        
        print(f"K-Fold Cross-Validation (k={k}):")
        print(f"Scores: {scores}")
        print(f"Mean: {scores.mean():.3f}")
        print(f"Std: {scores.std():.3f}")
        
        return scores
    
    def stratified_cv(self, X, y, model, k=5):
        """Stratified cross-validation for imbalanced datasets."""
        
        stratified_kfold = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
        
        scores = cross_val_score(model, X, y, cv=stratified_kfold, scoring='accuracy')
        
        print(f"Stratified Cross-Validation (k={k}):")
        print(f"Scores: {scores}")
        print(f"Mean: {scores.mean():.3f}")
        print(f"Std: {scores.std():.3f}")
        
        return scores
    
    def time_series_cv(self, X, y, model, n_splits=5):
        """Time series cross-validation for temporal data."""
        
        tscv = TimeSeriesSplit(n_splits=n_splits)
        
        scores = cross_val_score(model, X, y, cv=tscv, scoring='accuracy')
        
        print(f"Time Series Cross-Validation (splits={n_splits}):")
        print(f"Scores: {scores}")
        print(f"Mean: {scores.mean():.3f}")
        print(f"Std: {scores.std():.3f}")
        
        return scores
    
    def leave_one_out_cv(self, X, y, model):
        """Leave-One-Out cross-validation."""
        
        loo = LeaveOneOut()
        
        scores = cross_val_score(model, X, y, cv=loo, scoring='accuracy')
        
        print(f"Leave-One-Out Cross-Validation:")
        print(f"Mean: {scores.mean():.3f}")
        print(f"Std: {scores.std():.3f}")
        
        return scores
    
    def comprehensive_cv_evaluation(self, X, y, model):
        """Comprehensive cross-validation with multiple metrics."""
        
        # Define multiple scoring metrics
        scoring = {
            'accuracy': 'accuracy',
            'precision': 'precision_weighted',
            'recall': 'recall_weighted',
            'f1': 'f1_weighted',
            'roc_auc': 'roc_auc_ovr_weighted'
        }
        
        # Perform cross-validation with multiple metrics
        cv_results = cross_validate(
            model, X, y, 
            cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
            scoring=scoring,
            return_train_score=True
        )
        
        print("Comprehensive Cross-Validation Results:")
        for metric in scoring.keys():
            train_scores = cv_results[f'train_{metric}']
            test_scores = cv_results[f'test_{metric}']
            
            print(f"{metric.upper()}:")
            print(f"  Train: {train_scores.mean():.3f} (+/- {train_scores.std() * 2:.3f})")
            print(f"  Test:  {test_scores.mean():.3f} (+/- {test_scores.std() * 2:.3f})")
        
        return cv_results
    
    def plot_validation_curve(self, X, y, model, param_name, param_range):
        """Plot validation curve to analyze parameter impact."""
        
        train_scores, test_scores = validation_curve(
            model, X, y, 
            param_name=param_name, 
            param_range=param_range,
            cv=5, 
            scoring='accuracy'
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
        plt.title(f'Validation Curve for {param_name}')
        plt.legend(loc='best')
        plt.grid(True)
        plt.show()
        
        return train_scores, test_scores
```

### 12. How do you handle categorical variables in ML?
**Answer**: Various encoding techniques for converting categorical data to numerical format.

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
from sklearn.feature_extraction import FeatureHasher
import category_encoders as ce

# Categorical Encoding Techniques
class CategoricalEncoder:
    def __init__(self):
        self.encoders = {}
        self.encoded_features = {}
    
    def label_encoding(self, df, categorical_columns):
        """Label encoding for ordinal categorical variables."""
        
        df_encoded = df.copy()
        
        for column in categorical_columns:
            if column in df.columns:
                le = LabelEncoder()
                df_encoded[f'{column}_label'] = le.fit_transform(df[column].astype(str))
                self.encoders[f'{column}_label'] = le
        
        return df_encoded
    
    def one_hot_encoding(self, df, categorical_columns, drop_first=True):
        """One-hot encoding for nominal categorical variables."""
        
        df_encoded = df.copy()
        
        for column in categorical_columns:
            if column in df.columns:
                # Create dummy variables
                dummies = pd.get_dummies(df[column], prefix=column, drop_first=drop_first)
                df_encoded = pd.concat([df_encoded, dummies], axis=1)
                
                # Store feature names
                self.encoded_features[column] = dummies.columns.tolist()
        
        return df_encoded
    
    def ordinal_encoding(self, df, categorical_columns, ordinal_mappings=None):
        """Ordinal encoding with custom ordering."""
        
        df_encoded = df.copy()
        
        for column in categorical_columns:
            if column in df.columns:
                if ordinal_mappings and column in ordinal_mappings:
                    # Use custom ordering
                    mapping = ordinal_mappings[column]
                    df_encoded[f'{column}_ordinal'] = df[column].map(mapping)
                else:
                    # Use sklearn OrdinalEncoder
                    oe = OrdinalEncoder()
                    df_encoded[f'{column}_ordinal'] = oe.fit_transform(df[[column]])
                    self.encoders[f'{column}_ordinal'] = oe
        
        return df_encoded
    
    def target_encoding(self, df, categorical_columns, target_column, smoothing=1.0):
        """Target encoding (mean encoding) with smoothing."""
        
        df_encoded = df.copy()
        global_mean = df[target_column].mean()
        
        for column in categorical_columns:
            if column in df.columns:
                # Calculate category statistics
                category_stats = df.groupby(column)[target_column].agg(['count', 'mean'])
                
                # Apply smoothing
                smoothed_means = (category_stats['count'] * category_stats['mean'] + 
                                smoothing * global_mean) / (category_stats['count'] + smoothing)
                
                # Map to dataframe
                df_encoded[f'{column}_target'] = df[column].map(smoothed_means)
                
                # Handle unseen categories
                df_encoded[f'{column}_target'].fillna(global_mean, inplace=True)
        
        return df_encoded
    
    def frequency_encoding(self, df, categorical_columns):
        """Frequency encoding based on category occurrence."""
        
        df_encoded = df.copy()
        
        for column in categorical_columns:
            if column in df.columns:
                # Calculate frequency
                frequency_map = df[column].value_counts().to_dict()
                df_encoded[f'{column}_freq'] = df[column].map(frequency_map)
        
        return df_encoded
    
    def binary_encoding(self, df, categorical_columns):
        """Binary encoding for high-cardinality categorical variables."""
        
        df_encoded = df.copy()
        
        for column in categorical_columns:
            if column in df.columns:
                # Use category_encoders library
                be = ce.BinaryEncoder(cols=[column])
                binary_encoded = be.fit_transform(df[[column]])
                
                # Rename columns
                binary_encoded.columns = [f'{column}_bin_{i}' for i in range(len(binary_encoded.columns))]
                
                df_encoded = pd.concat([df_encoded, binary_encoded], axis=1)
                self.encoders[f'{column}_binary'] = be
        
        return df_encoded
    
    def hash_encoding(self, df, categorical_columns, n_features=10):
        """Feature hashing for very high-cardinality categories."""
        
        df_encoded = df.copy()
        
        for column in categorical_columns:
            if column in df.columns:
                # Convert to string format for hashing
                text_data = df[column].astype(str).tolist()
                
                # Apply feature hashing
                hasher = FeatureHasher(n_features=n_features, input_type='string')
                hashed_features = hasher.transform(text_data).toarray()
                
                # Create dataframe with hashed features
                hash_df = pd.DataFrame(
                    hashed_features, 
                    columns=[f'{column}_hash_{i}' for i in range(n_features)],
                    index=df.index
                )\n                \n                df_encoded = pd.concat([df_encoded, hash_df], axis=1)\n                self.encoders[f'{column}_hash'] = hasher\n        \n        return df_encoded\n    \n    def compare_encoding_methods(self, df, categorical_column, target_column=None):\n        \"\"\"Compare different encoding methods for a categorical variable.\"\"\"\n        \n        results = {}\n        \n        # Basic statistics\n        unique_values = df[categorical_column].nunique()\n        missing_values = df[categorical_column].isnull().sum()\n        \n        print(f\"Categorical Variable Analysis: {categorical_column}\")\n        print(f\"Unique values: {unique_values}\")\n        print(f\"Missing values: {missing_values}\")\n        print(f\"Value counts:\")\n        print(df[categorical_column].value_counts().head(10))\n        \n        # Apply different encoding methods\n        encoding_methods = {\n            'label': self.label_encoding(df, [categorical_column]),\n            'onehot': self.one_hot_encoding(df, [categorical_column]),\n            'frequency': self.frequency_encoding(df, [categorical_column])\n        }\n        \n        if target_column:\n            encoding_methods['target'] = self.target_encoding(df, [categorical_column], target_column)\n        \n        # Analyze encoded features\n        for method, encoded_df in encoding_methods.items():\n            new_columns = [col for col in encoded_df.columns if col not in df.columns]\n            results[method] = {\n                'new_features': len(new_columns),\n                'feature_names': new_columns[:5],  # Show first 5\n                'memory_usage': encoded_df[new_columns].memory_usage(deep=True).sum()\n            }\n        \n        # Display results\n        print(\"\\nEncoding Method Comparison:\")\n        for method, stats in results.items():\n            print(f\"{method.upper()}:\")\n            print(f\"  New features: {stats['new_features']}\")\n            print(f\"  Memory usage: {stats['memory_usage']} bytes\")\n            print(f\"  Sample features: {stats['feature_names']}\")\n        \n        return results, encoding_methods\n\n# Example usage\ndef categorical_encoding_example():\n    \"\"\"Complete categorical encoding example.\"\"\"\n    \n    # Create sample data with different types of categorical variables\n    np.random.seed(42)\n    n_samples = 1000\n    \n    data = {\n        'ordinal_cat': np.random.choice(['Low', 'Medium', 'High'], n_samples),\n        'nominal_cat': np.random.choice(['A', 'B', 'C', 'D'], n_samples),\n        'high_card_cat': np.random.choice([f'Cat_{i}' for i in range(50)], n_samples),\n        'target': np.random.binomial(1, 0.3, n_samples)\n    }\n    \n    df = pd.DataFrame(data)\n    \n    # Initialize encoder\n    encoder = CategoricalEncoder()\n    \n    # Test different encoding methods\n    print(\"=== ORDINAL CATEGORICAL VARIABLE ===\")\n    ordinal_mapping = {'Low': 1, 'Medium': 2, 'High': 3}\n    results_ord, methods_ord = encoder.compare_encoding_methods(df, 'ordinal_cat', 'target')\n    \n    print(\"\\n=== NOMINAL CATEGORICAL VARIABLE ===\")\n    results_nom, methods_nom = encoder.compare_encoding_methods(df, 'nominal_cat', 'target')\n    \n    print(\"\\n=== HIGH CARDINALITY CATEGORICAL VARIABLE ===\")\n    results_high, methods_high = encoder.compare_encoding_methods(df, 'high_card_cat', 'target')\n    \n    return {\n        'ordinal': (results_ord, methods_ord),\n        'nominal': (results_nom, methods_nom),\n        'high_cardinality': (results_high, methods_high)\n    }\n```\n\n### 13. What is regularization and how does it prevent overfitting?\n**Answer**: Regularization techniques add penalties to model complexity to improve generalization.\n\n```python\nfrom sklearn.linear_model import Ridge, Lasso, ElasticNet, LogisticRegression\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.model_selection import validation_curve\nimport matplotlib.pyplot as plt\n\n# Regularization Techniques\nclass RegularizationMethods:\n    def __init__(self):\n        self.models = {}\n        self.regularization_paths = {}\n    \n    def ridge_regression_demo(self, X, y):\n        \"\"\"Demonstrate Ridge (L2) regularization.\"\"\"\n        \n        # Scale features for regularization\n        scaler = StandardScaler()\n        X_scaled = scaler.fit_transform(X)\n        \n        # Test different alpha values\n        alphas = np.logspace(-4, 2, 50)\n        \n        ridge_models = {}\n        coefficients = []\n        \n        for alpha in alphas:\n            ridge = Ridge(alpha=alpha)\n            ridge.fit(X_scaled, y)\n            ridge_models[alpha] = ridge\n            coefficients.append(ridge.coef_)\n        \n        # Plot regularization path\n        plt.figure(figsize=(12, 4))\n        \n        plt.subplot(1, 2, 1)\n        coefficients = np.array(coefficients)\n        for i in range(coefficients.shape[1]):\n            plt.plot(alphas, coefficients[:, i], label=f'Feature {i+1}')\n        plt.xscale('log')\n        plt.xlabel('Alpha (Regularization Strength)')\n        plt.ylabel('Coefficient Value')\n        plt.title('Ridge Regularization Path')\n        plt.legend()\n        plt.grid(True)\n        \n        # Validation curve\n        plt.subplot(1, 2, 2)\n        train_scores, val_scores = validation_curve(\n            Ridge(), X_scaled, y, param_name='alpha', param_range=alphas, cv=5\n        )\n        \n        plt.plot(alphas, train_scores.mean(axis=1), 'o-', label='Training Score')\n        plt.plot(alphas, val_scores.mean(axis=1), 'o-', label='Validation Score')\n        plt.xscale('log')\n        plt.xlabel('Alpha')\n        plt.ylabel('R² Score')\n        plt.title('Ridge Validation Curve')\n        plt.legend()\n        plt.grid(True)\n        \n        plt.tight_layout()\n        plt.show()\n        \n        return ridge_models\n    \n    def lasso_regression_demo(self, X, y):\n        \"\"\"Demonstrate Lasso (L1) regularization.\"\"\"\n        \n        # Scale features\n        scaler = StandardScaler()\n        X_scaled = scaler.fit_transform(X)\n        \n        # Test different alpha values\n        alphas = np.logspace(-4, 1, 50)\n        \n        lasso_models = {}\n        coefficients = []\n        n_features_selected = []\n        \n        for alpha in alphas:\n            lasso = Lasso(alpha=alpha, max_iter=10000)\n            lasso.fit(X_scaled, y)\n            lasso_models[alpha] = lasso\n            coefficients.append(lasso.coef_)\n            n_features_selected.append(np.sum(lasso.coef_ != 0))\n        \n        # Plot regularization path and feature selection\n        plt.figure(figsize=(15, 4))\n        \n        # Coefficient path\n        plt.subplot(1, 3, 1)\n        coefficients = np.array(coefficients)\n        for i in range(coefficients.shape[1]):\n            plt.plot(alphas, coefficients[:, i], label=f'Feature {i+1}')\n        plt.xscale('log')\n        plt.xlabel('Alpha (Regularization Strength)')\n        plt.ylabel('Coefficient Value')\n        plt.title('Lasso Regularization Path')\n        plt.legend()\n        plt.grid(True)\n        \n        # Feature selection\n        plt.subplot(1, 3, 2)\n        plt.plot(alphas, n_features_selected, 'o-')\n        plt.xscale('log')\n        plt.xlabel('Alpha')\n        plt.ylabel('Number of Selected Features')\n        plt.title('Lasso Feature Selection')\n        plt.grid(True)\n        \n        # Validation curve\n        plt.subplot(1, 3, 3)\n        train_scores, val_scores = validation_curve(\n            Lasso(max_iter=10000), X_scaled, y, param_name='alpha', param_range=alphas, cv=5\n        )\n        \n        plt.plot(alphas, train_scores.mean(axis=1), 'o-', label='Training Score')\n        plt.plot(alphas, val_scores.mean(axis=1), 'o-', label='Validation Score')\n        plt.xscale('log')\n        plt.xlabel('Alpha')\n        plt.ylabel('R² Score')\n        plt.title('Lasso Validation Curve')\n        plt.legend()\n        plt.grid(True)\n        \n        plt.tight_layout()\n        plt.show()\n        \n        return lasso_models\n    \n    def elastic_net_demo(self, X, y):\n        \"\"\"Demonstrate Elastic Net (L1 + L2) regularization.\"\"\"\n        \n        # Scale features\n        scaler = StandardScaler()\n        X_scaled = scaler.fit_transform(X)\n        \n        # Test different l1_ratio values (0 = Ridge, 1 = Lasso)\n        l1_ratios = [0.1, 0.5, 0.7, 0.9]\n        alpha = 0.1\n        \n        plt.figure(figsize=(15, 10))\n        \n        for idx, l1_ratio in enumerate(l1_ratios):\n            elastic_net = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, max_iter=10000)\n            elastic_net.fit(X_scaled, y)\n            \n            plt.subplot(2, 2, idx + 1)\n            plt.bar(range(len(elastic_net.coef_)), elastic_net.coef_)\n            plt.title(f'Elastic Net Coefficients (l1_ratio={l1_ratio})')\n            plt.xlabel('Feature Index')\n            plt.ylabel('Coefficient Value')\n            plt.grid(True)\n        \n        plt.tight_layout()\n        plt.show()\n        \n        # Compare different l1_ratios\n        results = {}\n        for l1_ratio in l1_ratios:\n            elastic_net = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, max_iter=10000)\n            scores = cross_val_score(elastic_net, X_scaled, y, cv=5)\n            results[l1_ratio] = {\n                'mean_score': scores.mean(),\n                'std_score': scores.std()\n            }\n        \n        print(\"Elastic Net Results:\")\n        for l1_ratio, result in results.items():\n            print(f\"l1_ratio={l1_ratio}: {result['mean_score']:.3f} (+/- {result['std_score']*2:.3f})\")\n        \n        return results\n    \n    def regularization_comparison(self, X, y):\n        \"\"\"Compare different regularization methods.\"\"\"\n        \n        # Scale features\n        scaler = StandardScaler()\n        X_scaled = scaler.fit_transform(X)\n        \n        # Define models\n        models = {\n            'Linear (No Regularization)': LinearRegression(),\n            'Ridge (L2)': Ridge(alpha=1.0),\n            'Lasso (L1)': Lasso(alpha=0.1, max_iter=10000),\n            'Elastic Net (L1+L2)': ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=10000)\n        }\n        \n        # Evaluate models\n        results = {}\n        for name, model in models.items():\n            scores = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')\n            \n            # Fit model to get coefficients\n            model.fit(X_scaled, y)\n            \n            results[name] = {\n                'cv_score_mean': scores.mean(),\n                'cv_score_std': scores.std(),\n                'n_nonzero_coef': np.sum(model.coef_ != 0) if hasattr(model, 'coef_') else len(model.coef_),\n                'coef_magnitude': np.linalg.norm(model.coef_) if hasattr(model, 'coef_') else 0\n            }\n        \n        # Display results\n        print(\"Regularization Method Comparison:\")\n        print(f\"{'Method':<25} {'CV Score':<15} {'Non-zero Coef':<15} {'Coef Magnitude':<15}\")\n        print(\"-\" * 70)\n        \n        for name, result in results.items():\n            print(f\"{name:<25} {result['cv_score_mean']:.3f}±{result['cv_score_std']:.3f}    \"\n                  f\"{result['n_nonzero_coef']:<15} {result['coef_magnitude']:<15.3f}\")\n        \n        return results\n\n# Example usage\ndef regularization_example():\n    \"\"\"Complete regularization demonstration.\"\"\"\n    from sklearn.datasets import make_regression\n    \n    # Generate sample data with noise\n    X, y = make_regression(\n        n_samples=100, n_features=20, n_informative=5,\n        noise=10, random_state=42\n    )\n    \n    # Initialize regularization methods\n    reg_methods = RegularizationMethods()\n    \n    # Demonstrate different regularization techniques\n    print(\"=== RIDGE REGRESSION (L2) ===\")\n    ridge_models = reg_methods.ridge_regression_demo(X, y)\n    \n    print(\"\\n=== LASSO REGRESSION (L1) ===\")\n    lasso_models = reg_methods.lasso_regression_demo(X, y)\n    \n    print(\"\\n=== ELASTIC NET (L1 + L2) ===\")\n    elastic_results = reg_methods.elastic_net_demo(X, y)\n    \n    print(\"\\n=== REGULARIZATION COMPARISON ===\")\n    comparison_results = reg_methods.regularization_comparison(X, y)\n    \n    return {\n        'ridge': ridge_models,\n        'lasso': lasso_models,\n        'elastic_net': elastic_results,\n        'comparison': comparison_results\n    }\n```\n
### 14. What is the bias-variance tradeoff?
**Answer**: The bias-variance tradeoff is a fundamental concept in ML that describes the relationship between model complexity and generalization error.

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Bias-Variance Decomposition
class BiasVarianceAnalysis:
    def __init__(self):
        self.results = {}
    
    def generate_data(self, n_samples=200, noise_level=0.3):
        """Generate synthetic data for bias-variance analysis."""
        np.random.seed(42)
        X = np.linspace(0, 1, n_samples).reshape(-1, 1)
        
        # True function: sine wave
        y_true = np.sin(2 * np.pi * X.ravel())
        
        # Add noise
        y = y_true + np.random.normal(0, noise_level, n_samples)
        
        return X, y, y_true
    
    def bias_variance_decomposition(self, model, X, y, y_true, n_trials=100):
        """Perform bias-variance decomposition analysis."""
        
        n_samples = len(X)
        predictions = []
        
        # Run multiple trials with different train/test splits
        for trial in range(n_trials):
            # Bootstrap sampling
            indices = np.random.choice(n_samples, n_samples, replace=True)
            X_boot = X[indices]
            y_boot = y[indices]
            
            # Train model
            model_copy = clone(model)
            model_copy.fit(X_boot, y_boot)
            
            # Predict on original X
            y_pred = model_copy.predict(X)
            predictions.append(y_pred)
        
        predictions = np.array(predictions)
        
        # Calculate bias and variance
        mean_prediction = np.mean(predictions, axis=0)
        bias_squared = np.mean((mean_prediction - y_true) ** 2)
        variance = np.mean(np.var(predictions, axis=0))
        
        # Noise (irreducible error)
        noise = np.var(y - y_true)
        
        # Total error
        total_error = bias_squared + variance + noise
        
        return {
            'bias_squared': bias_squared,
            'variance': variance,
            'noise': noise,
            'total_error': total_error,
            'predictions': predictions,
            'mean_prediction': mean_prediction
        }
    
    def compare_model_complexity(self, X, y, y_true):
        """Compare bias-variance for different model complexities."""
        
        # Define models with different complexities
        models = {
            'Linear': LinearRegression(),
            'Polynomial_2': Pipeline([
                ('poly', PolynomialFeatures(degree=2)),
                ('linear', LinearRegression())
            ]),
            'Polynomial_5': Pipeline([
                ('poly', PolynomialFeatures(degree=5)),
                ('linear', LinearRegression())
            ]),
            'Polynomial_10': Pipeline([
                ('poly', PolynomialFeatures(degree=10)),
                ('linear', LinearRegression())
            ]),
            'Decision_Tree_2': DecisionTreeRegressor(max_depth=2, random_state=42),
            'Decision_Tree_5': DecisionTreeRegressor(max_depth=5, random_state=42),
            'Decision_Tree_None': DecisionTreeRegressor(max_depth=None, random_state=42),
            'Random_Forest_10': RandomForestRegressor(n_estimators=10, max_depth=5, random_state=42),
            'Random_Forest_100': RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
        }
        
        results = {}\n        \n        for name, model in models.items():\n            print(f\"Analyzing {name}...\")\n            result = self.bias_variance_decomposition(model, X, y, y_true)\n            results[name] = result\n        \n        return results\n    \n    def plot_bias_variance_tradeoff(self, results, X, y_true):\n        \"\"\"Visualize bias-variance tradeoff.\"\"\"\n        \n        # Extract metrics\n        model_names = list(results.keys())\n        bias_squared = [results[name]['bias_squared'] for name in model_names]\n        variance = [results[name]['variance'] for name in model_names]\n        total_error = [results[name]['total_error'] for name in model_names]\n        \n        # Create plots\n        fig, axes = plt.subplots(2, 2, figsize=(15, 12))\n        \n        # Bias-Variance tradeoff plot\n        axes[0, 0].bar(range(len(model_names)), bias_squared, alpha=0.7, label='Bias²', color='red')\n        axes[0, 0].bar(range(len(model_names)), variance, bottom=bias_squared, alpha=0.7, label='Variance', color='blue')\n        axes[0, 0].set_xlabel('Model')\n        axes[0, 0].set_ylabel('Error')\n        axes[0, 0].set_title('Bias-Variance Decomposition')\n        axes[0, 0].set_xticks(range(len(model_names)))\n        axes[0, 0].set_xticklabels(model_names, rotation=45, ha='right')\n        axes[0, 0].legend()\n        axes[0, 0].grid(True, alpha=0.3)\n        \n        # Total error comparison\n        axes[0, 1].plot(range(len(model_names)), total_error, 'o-', color='green', linewidth=2, markersize=8)\n        axes[0, 1].set_xlabel('Model')\n        axes[0, 1].set_ylabel('Total Error')\n        axes[0, 1].set_title('Total Error by Model Complexity')\n        axes[0, 1].set_xticks(range(len(model_names)))\n        axes[0, 1].set_xticklabels(model_names, rotation=45, ha='right')\n        axes[0, 1].grid(True, alpha=0.3)\n        \n        # Bias vs Variance scatter plot\n        axes[1, 0].scatter(bias_squared, variance, s=100, alpha=0.7)\n        for i, name in enumerate(model_names):\n            axes[1, 0].annotate(name, (bias_squared[i], variance[i]), \n                              xytext=(5, 5), textcoords='offset points', fontsize=8)\n        axes[1, 0].set_xlabel('Bias²')\n        axes[1, 0].set_ylabel('Variance')\n        axes[1, 0].set_title('Bias² vs Variance')\n        axes[1, 0].grid(True, alpha=0.3)\n        \n        # Example predictions for a few models\n        axes[1, 1].plot(X.ravel(), y_true, 'k-', linewidth=2, label='True Function')\n        \n        # Show predictions from a few representative models\n        representative_models = ['Linear', 'Polynomial_5', 'Decision_Tree_None']\n        colors = ['red', 'blue', 'orange']\n        \n        for i, model_name in enumerate(representative_models):\n            if model_name in results:\n                mean_pred = results[model_name]['mean_prediction']\n                axes[1, 1].plot(X.ravel(), mean_pred, '--', color=colors[i], \n                              linewidth=2, label=f'{model_name} (Mean)')\n                \n                # Show prediction uncertainty\n                predictions = results[model_name]['predictions']\n                pred_std = np.std(predictions, axis=0)\n                axes[1, 1].fill_between(X.ravel(), \n                                       mean_pred - pred_std, \n                                       mean_pred + pred_std, \n                                       alpha=0.2, color=colors[i])\n        \n        axes[1, 1].set_xlabel('X')\n        axes[1, 1].set_ylabel('Y')\n        axes[1, 1].set_title('Model Predictions with Uncertainty')\n        axes[1, 1].legend()\n        axes[1, 1].grid(True, alpha=0.3)\n        \n        plt.tight_layout()\n        plt.show()\n    \n    def analyze_sample_size_effect(self, X, y, y_true, model):\n        \"\"\"Analyze how sample size affects bias-variance tradeoff.\"\"\"\n        \n        sample_sizes = [20, 50, 100, 200, 500]\n        results = {}\n        \n        for n_samples in sample_sizes:\n            if n_samples <= len(X):\n                X_subset = X[:n_samples]\n                y_subset = y[:n_samples]\n                y_true_subset = y_true[:n_samples]\n                \n                result = self.bias_variance_decomposition(model, X_subset, y_subset, y_true_subset)\n                results[n_samples] = result\n        \n        # Plot results\n        sample_sizes_list = list(results.keys())\n        bias_squared = [results[n]['bias_squared'] for n in sample_sizes_list]\n        variance = [results[n]['variance'] for n in sample_sizes_list]\n        total_error = [results[n]['total_error'] for n in sample_sizes_list]\n        \n        plt.figure(figsize=(12, 4))\n        \n        plt.subplot(1, 2, 1)\n        plt.plot(sample_sizes_list, bias_squared, 'o-', label='Bias²', color='red')\n        plt.plot(sample_sizes_list, variance, 'o-', label='Variance', color='blue')\n        plt.plot(sample_sizes_list, total_error, 'o-', label='Total Error', color='green')\n        plt.xlabel('Sample Size')\n        plt.ylabel('Error')\n        plt.title('Bias-Variance vs Sample Size')\n        plt.legend()\n        plt.grid(True, alpha=0.3)\n        \n        plt.subplot(1, 2, 2)\n        plt.loglog(sample_sizes_list, variance, 'o-', label='Variance', color='blue')\n        plt.loglog(sample_sizes_list, [1/n for n in sample_sizes_list], '--', label='1/n', color='gray')\n        plt.xlabel('Sample Size')\n        plt.ylabel('Variance (log scale)')\n        plt.title('Variance Decay with Sample Size')\n        plt.legend()\n        plt.grid(True, alpha=0.3)\n        \n        plt.tight_layout()\n        plt.show()\n        \n        return results\n\n# Example usage\ndef bias_variance_example():\n    \"\"\"Complete bias-variance analysis example.\"\"\"\n    from sklearn.base import clone\n    \n    # Initialize analysis\n    bv_analysis = BiasVarianceAnalysis()\n    \n    # Generate data\n    X, y, y_true = bv_analysis.generate_data(n_samples=200, noise_level=0.3)\n    \n    print(\"=== BIAS-VARIANCE DECOMPOSITION ===\")\n    \n    # Compare different model complexities\n    results = bv_analysis.compare_model_complexity(X, y, y_true)\n    \n    # Display numerical results\n    print(\"\\nBias-Variance Decomposition Results:\")\n    print(f\"{'Model':<20} {'Bias²':<10} {'Variance':<10} {'Noise':<10} {'Total Error':<12}\")\n    print(\"-\" * 65)\n    \n    for name, result in results.items():\n        print(f\"{name:<20} {result['bias_squared']:<10.4f} {result['variance']:<10.4f} \"\n              f\"{result['noise']:<10.4f} {result['total_error']:<12.4f}\")\n    \n    # Visualize results\n    bv_analysis.plot_bias_variance_tradeoff(results, X, y_true)\n    \n    # Analyze sample size effect\n    print(\"\\n=== SAMPLE SIZE EFFECT ===\")\n    sample_size_results = bv_analysis.analyze_sample_size_effect(\n        X, y, y_true, DecisionTreeRegressor(max_depth=5, random_state=42)\n    )\n    \n    return {\n        'model_comparison': results,\n        'sample_size_effect': sample_size_results\n    }\n```\n\n### 15. How do you handle time series data in ML?\n**Answer**: Time series requires special considerations for temporal dependencies and data leakage prevention.\n\n```python\nimport pandas as pd\nimport numpy as np\nfrom sklearn.model_selection import TimeSeriesSplit\nfrom sklearn.ensemble import RandomForestRegressor\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import mean_squared_error, mean_absolute_error\nimport matplotlib.pyplot as plt\nfrom statsmodels.tsa.seasonal import seasonal_decompose\nfrom statsmodels.tsa.arima.model import ARIMA\n\n# Time Series ML Methods\nclass TimeSeriesML:\n    def __init__(self):\n        self.models = {}\n        self.feature_importance = {}\n    \n    def create_time_features(self, df, date_column):\n        \"\"\"Create time-based features from datetime column.\"\"\"\n        \n        df = df.copy()\n        df[date_column] = pd.to_datetime(df[date_column])\n        \n        # Basic time features\n        df['year'] = df[date_column].dt.year\n        df['month'] = df[date_column].dt.month\n        df['day'] = df[date_column].dt.day\n        df['dayofweek'] = df[date_column].dt.dayofweek\n        df['hour'] = df[date_column].dt.hour\n        df['quarter'] = df[date_column].dt.quarter\n        df['week'] = df[date_column].dt.isocalendar().week\n        \n        # Cyclical features\n        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)\n        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)\n        df['day_sin'] = np.sin(2 * np.pi * df['day'] / 31)\n        df['day_cos'] = np.cos(2 * np.pi * df['day'] / 31)\n        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)\n        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)\n        \n        # Business features\n        df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)\n        df['is_month_start'] = (df[date_column].dt.is_month_start).astype(int)\n        df['is_month_end'] = (df[date_column].dt.is_month_end).astype(int)\n        df['is_quarter_start'] = (df[date_column].dt.is_quarter_start).astype(int)\n        df['is_quarter_end'] = (df[date_column].dt.is_quarter_end).astype(int)\n        \n        return df\n    \n    def create_lag_features(self, df, target_column, lags=[1, 2, 3, 7, 14, 30]):\n        \"\"\"Create lagged features for time series.\"\"\"\n        \n        df = df.copy()\n        \n        for lag in lags:\n            df[f'{target_column}_lag_{lag}'] = df[target_column].shift(lag)\n        \n        return df\n    \n    def create_rolling_features(self, df, target_column, windows=[3, 7, 14, 30]):\n        \"\"\"Create rolling window features.\"\"\"\n        \n        df = df.copy()\n        \n        for window in windows:\n            # Rolling statistics\n            df[f'{target_column}_rolling_mean_{window}'] = df[target_column].rolling(window=window).mean()\n            df[f'{target_column}_rolling_std_{window}'] = df[target_column].rolling(window=window).std()\n            df[f'{target_column}_rolling_min_{window}'] = df[target_column].rolling(window=window).min()\n            df[f'{target_column}_rolling_max_{window}'] = df[target_column].rolling(window=window).max()\n            \n            # Rolling differences\n            df[f'{target_column}_rolling_diff_{window}'] = (df[target_column] - \n                                                           df[target_column].rolling(window=window).mean())\n        \n        return df\n    \n    def create_seasonal_features(self, df, target_column, date_column, periods=[7, 30, 365]):\n        \"\"\"Create seasonal decomposition features.\"\"\"\n        \n        df = df.copy()\n        df = df.set_index(date_column)\n        \n        for period in periods:\n            if len(df) >= 2 * period:\n                try:\n                    # Seasonal decomposition\n                    decomposition = seasonal_decompose(df[target_column], \n                                                     model='additive', \n                                                     period=period)\n                    \n                    df[f'{target_column}_trend_{period}'] = decomposition.trend\n                    df[f'{target_column}_seasonal_{period}'] = decomposition.seasonal\n                    df[f'{target_column}_residual_{period}'] = decomposition.resid\n                    \n                except Exception as e:\n                    print(f\"Could not create seasonal features for period {period}: {e}\")\n        \n        return df.reset_index()\n    \n    def time_series_cross_validation(self, X, y, model, n_splits=5):\n        \"\"\"Perform time series cross-validation.\"\"\"\n        \n        tscv = TimeSeriesSplit(n_splits=n_splits)\n        \n        scores = []\n        predictions = []\n        \n        for fold, (train_idx, val_idx) in enumerate(tscv.split(X)):\n            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]\n            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]\n            \n            # Train model\n            model_copy = clone(model)\n            model_copy.fit(X_train, y_train)\n            \n            # Predict\n            y_pred = model_copy.predict(X_val)\n            \n            # Calculate metrics\n            mse = mean_squared_error(y_val, y_pred)\n            mae = mean_absolute_error(y_val, y_pred)\n            \n            scores.append({'fold': fold, 'mse': mse, 'mae': mae, 'rmse': np.sqrt(mse)})\n            predictions.append({\n                'fold': fold,\n                'val_idx': val_idx,\n                'y_true': y_val,\n                'y_pred': y_pred\n            })\n        \n        return scores, predictions\n    \n    def walk_forward_validation(self, df, target_column, feature_columns, \n                               model, initial_train_size=100, step_size=1):\n        \"\"\"Perform walk-forward validation.\"\"\"\n        \n        results = []\n        \n        for i in range(initial_train_size, len(df) - step_size, step_size):\n            # Define train and test sets\n            train_data = df.iloc[:i]\n            test_data = df.iloc[i:i+step_size]\n            \n            X_train = train_data[feature_columns]\n            y_train = train_data[target_column]\n            X_test = test_data[feature_columns]\n            y_test = test_data[target_column]\n            \n            # Handle missing values (common with lag features)\n            X_train = X_train.dropna()\n            y_train = y_train[X_train.index]\n            \n            if len(X_train) > 0 and len(X_test) > 0:\n                # Train model\n                model_copy = clone(model)\n                model_copy.fit(X_train, y_train)\n                \n                # Predict\n                y_pred = model_copy.predict(X_test)\n                \n                # Store results\n                results.append({\n                    'train_end': i,\n                    'test_start': i,\n                    'test_end': i + step_size,\n                    'y_true': y_test.values,\n                    'y_pred': y_pred,\n                    'mse': mean_squared_error(y_test, y_pred),\n                    'mae': mean_absolute_error(y_test, y_pred)\n                })\n        \n        return results\n    \n    def detect_concept_drift(self, results):\n        \"\"\"Detect concept drift in time series predictions.\"\"\"\n        \n        # Extract performance metrics over time\n        mse_values = [r['mse'] for r in results]\n        mae_values = [r['mae'] for r in results]\n        \n        # Calculate rolling performance\n        window_size = min(10, len(mse_values) // 4)\n        \n        rolling_mse = pd.Series(mse_values).rolling(window=window_size).mean()\n        rolling_mae = pd.Series(mae_values).rolling(window=window_size).mean()\n        \n        # Detect significant changes\n        mse_threshold = np.mean(mse_values) + 2 * np.std(mse_values)\n        mae_threshold = np.mean(mae_values) + 2 * np.std(mae_values)\n        \n        drift_points = []\n        for i, (mse, mae) in enumerate(zip(rolling_mse, rolling_mae)):\n            if mse > mse_threshold or mae > mae_threshold:\n                drift_points.append(i)\n        \n        # Plot performance over time\n        plt.figure(figsize=(15, 6))\n        \n        plt.subplot(1, 2, 1)\n        plt.plot(mse_values, label='MSE', alpha=0.7)\n        plt.plot(rolling_mse, label='Rolling MSE', linewidth=2)\n        plt.axhline(y=mse_threshold, color='red', linestyle='--', label='Threshold')\n        for dp in drift_points:\n            plt.axvline(x=dp, color='red', alpha=0.5)\n        plt.xlabel('Time Step')\n        plt.ylabel('MSE')\n        plt.title('Model Performance Over Time (MSE)')\n        plt.legend()\n        plt.grid(True, alpha=0.3)\n        \n        plt.subplot(1, 2, 2)\n        plt.plot(mae_values, label='MAE', alpha=0.7)\n        plt.plot(rolling_mae, label='Rolling MAE', linewidth=2)\n        plt.axhline(y=mae_threshold, color='red', linestyle='--', label='Threshold')\n        for dp in drift_points:\n            plt.axvline(x=dp, color='red', alpha=0.5)\n        plt.xlabel('Time Step')\n        plt.ylabel('MAE')\n        plt.title('Model Performance Over Time (MAE)')\n        plt.legend()\n        plt.grid(True, alpha=0.3)\n        \n        plt.tight_layout()\n        plt.show()\n        \n        return {\n            'drift_points': drift_points,\n            'mse_threshold': mse_threshold,\n            'mae_threshold': mae_threshold,\n            'performance_degradation': len(drift_points) > 0\n        }\n    \n    def compare_ts_models(self, df, target_column, feature_columns):\n        \"\"\"Compare different models for time series prediction.\"\"\"\n        \n        models = {\n            'Linear Regression': LinearRegression(),\n            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),\n            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)\n        }\n        \n        results = {}\n        \n        for name, model in models.items():\n            print(f\"Evaluating {name}...\")\n            \n            # Prepare data\n            X = df[feature_columns].dropna()\n            y = df[target_column][X.index]\n            \n            # Time series cross-validation\n            scores, predictions = self.time_series_cross_validation(X, y, model)\n            \n            # Calculate average metrics\n            avg_mse = np.mean([s['mse'] for s in scores])\n            avg_mae = np.mean([s['mae'] for s in scores])\n            avg_rmse = np.mean([s['rmse'] for s in scores])\n            \n            results[name] = {\n                'avg_mse': avg_mse,\n                'avg_mae': avg_mae,\n                'avg_rmse': avg_rmse,\n                'scores': scores,\n                'predictions': predictions\n            }\n        \n        # Display results\n        print(\"\\nTime Series Model Comparison:\")\n        print(f\"{'Model':<20} {'MSE':<10} {'MAE':<10} {'RMSE':<10}\")\n        print(\"-\" * 50)\n        \n        for name, result in results.items():\n            print(f\"{name:<20} {result['avg_mse']:<10.4f} {result['avg_mae']:<10.4f} {result['avg_rmse']:<10.4f}\")\n        \n        return results\n\n# Example usage\ndef time_series_ml_example():\n    \"\"\"Complete time series ML example.\"\"\"\n    from sklearn.base import clone\n    from sklearn.ensemble import GradientBoostingRegressor\n    \n    # Generate sample time series data\n    np.random.seed(42)\n    dates = pd.date_range('2020-01-01', periods=1000, freq='D')\n    \n    # Create synthetic time series with trend, seasonality, and noise\n    trend = np.linspace(100, 200, 1000)\n    seasonal = 10 * np.sin(2 * np.pi * np.arange(1000) / 365.25)  # Yearly seasonality\n    weekly = 5 * np.sin(2 * np.pi * np.arange(1000) / 7)  # Weekly seasonality\n    noise = np.random.normal(0, 5, 1000)\n    \n    target = trend + seasonal + weekly + noise\n    \n    df = pd.DataFrame({\n        'date': dates,\n        'target': target,\n        'external_feature': np.random.normal(50, 10, 1000)\n    })\n    \n    # Initialize time series ML\n    ts_ml = TimeSeriesML()\n    \n    print(\"=== TIME SERIES FEATURE ENGINEERING ===\")\n    \n    # Create time features\n    df = ts_ml.create_time_features(df, 'date')\n    \n    # Create lag features\n    df = ts_ml.create_lag_features(df, 'target', lags=[1, 2, 3, 7, 14])\n    \n    # Create rolling features\n    df = ts_ml.create_rolling_features(df, 'target', windows=[7, 14, 30])\n    \n    # Select feature columns (exclude date and target)\n    feature_columns = [col for col in df.columns if col not in ['date', 'target']]\n    \n    print(f\"Created {len(feature_columns)} features\")\n    \n    print(\"\\n=== MODEL COMPARISON ===\")\n    \n    # Compare different models\n    model_results = ts_ml.compare_ts_models(df, 'target', feature_columns)\n    \n    print(\"\\n=== WALK-FORWARD VALIDATION ===\")\n    \n    # Walk-forward validation\n    wf_results = ts_ml.walk_forward_validation(\n        df, 'target', feature_columns, \n        RandomForestRegressor(n_estimators=50, random_state=42),\n        initial_train_size=200, step_size=1\n    )\n    \n    print(f\"Walk-forward validation completed: {len(wf_results)} predictions\")\n    \n    print(\"\\n=== CONCEPT DRIFT DETECTION ===\")\n    \n    # Detect concept drift\n    drift_analysis = ts_ml.detect_concept_drift(wf_results)\n    \n    if drift_analysis['performance_degradation']:\n        print(f\"Concept drift detected at {len(drift_analysis['drift_points'])} points\")\n    else:\n        print(\"No significant concept drift detected\")\n    \n    return {\n        'data': df,\n        'model_comparison': model_results,\n        'walk_forward': wf_results,\n        'drift_analysis': drift_analysis\n    }\n```\n\nThis comprehensive set covers ML fundamentals through advanced techniques with practical data engineering examples. The questions progress from basic concepts to complex real-world scenarios.\n
### 16. How do you implement automated machine learning (AutoML)?

**Answer**: AutoML automates the machine learning pipeline from data preprocessing to model selection and hyperparameter tuning.

```python
# AutoML Implementation
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
import optuna

class AutoMLPipeline:
    def __init__(self):
        self.best_model = None
        self.best_score = 0
        self.preprocessing_steps = []
        
    def automated_preprocessing(self, X, y):
        """Automated data preprocessing."""
        X_processed = X.copy()
        
        # Handle missing values
        numeric_columns = X_processed.select_dtypes(include=[np.number]).columns
        categorical_columns = X_processed.select_dtypes(include=['object']).columns
        
        # Numeric imputation
        for col in numeric_columns:
            if X_processed[col].isnull().sum() > 0:
                X_processed[col].fillna(X_processed[col].median(), inplace=True)
        
        # Categorical encoding
        for col in categorical_columns:
            le = LabelEncoder()
            X_processed[col] = le.fit_transform(X_processed[col].astype(str))
        
        return X_processed
    
    def automated_feature_selection(self, X, y, max_features=20):
        """Automated feature selection."""
        from sklearn.feature_selection import SelectKBest, f_classif
        
        if X.shape[1] > max_features:
            selector = SelectKBest(score_func=f_classif, k=max_features)
            X_selected = selector.fit_transform(X, y)
            selected_features = X.columns[selector.get_support()]
            return pd.DataFrame(X_selected, columns=selected_features)
        
        return X
    
    def automated_model_selection(self, X, y):
        """Automated model selection and hyperparameter tuning."""
        
        # Define model candidates
        models = {
            'logistic_regression': {
                'model': LogisticRegression(),
                'params': {
                    'C': [0.1, 1.0, 10.0],
                    'solver': ['liblinear', 'lbfgs']
                }
            },
            'random_forest': {
                'model': RandomForestClassifier(),
                'params': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [5, 10, None],
                    'min_samples_split': [2, 5, 10]
                }
            },
            'gradient_boosting': {
                'model': GradientBoostingClassifier(),
                'params': {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7]
                }
            }
        }
        
        best_model = None
        best_score = 0
        best_params = None
        
        for model_name, model_config in models.items():
            print(f"Tuning {model_name}...")
            
            # Grid search for hyperparameter tuning
            grid_search = GridSearchCV(
                model_config['model'],
                model_config['params'],
                cv=5,
                scoring='accuracy',
                n_jobs=-1
            )
            
            grid_search.fit(X, y)
            
            if grid_search.best_score_ > best_score:
                best_score = grid_search.best_score_
                best_model = grid_search.best_estimator_
                best_params = grid_search.best_params_
        
        return best_model, best_score, best_params
    
    def run_automl(self, X, y):
        """Run complete AutoML pipeline."""
        
        print("Starting AutoML Pipeline...")
        
        # Step 1: Automated preprocessing
        print("1. Automated preprocessing...")
        X_processed = self.automated_preprocessing(X, y)
        
        # Step 2: Automated feature selection
        print("2. Automated feature selection...")
        X_selected = self.automated_feature_selection(X_processed, y)
        
        # Step 3: Automated model selection
        print("3. Automated model selection...")
        best_model, best_score, best_params = self.automated_model_selection(X_selected, y)
        
        self.best_model = best_model
        self.best_score = best_score
        
        print(f"AutoML completed!")
        print(f"Best model: {type(best_model).__name__}")
        print(f"Best score: {best_score:.4f}")
        print(f"Best parameters: {best_params}")
        
        return best_model, best_score
```

### 17. How do you implement model interpretability and explainability?

**Answer**: Model interpretability helps understand how models make decisions, crucial for trust and debugging.

```python
# Model Interpretability Tools
import shap
import lime
import eli5
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

class ModelExplainer:
    def __init__(self, model, X_train, X_test):
        self.model = model
        self.X_train = X_train
        self.X_test = X_test
        
    def feature_importance_analysis(self):
        """Analyze feature importance using multiple methods."""
        
        # Method 1: Built-in feature importance (for tree-based models)
        if hasattr(self.model, 'feature_importances_'):
            importance_builtin = self.model.feature_importances_
            
            plt.figure(figsize=(10, 6))
            feature_names = self.X_train.columns if hasattr(self.X_train, 'columns') else range(len(importance_builtin))
            plt.barh(range(len(importance_builtin)), importance_builtin)
            plt.yticks(range(len(importance_builtin)), feature_names)
            plt.xlabel('Feature Importance')
            plt.title('Built-in Feature Importance')
            plt.tight_layout()
            plt.show()
        
        # Method 2: Permutation importance
        perm_importance = permutation_importance(
            self.model, self.X_test, self.y_test, n_repeats=10, random_state=42
        )
        
        plt.figure(figsize=(10, 6))
        feature_names = self.X_train.columns if hasattr(self.X_train, 'columns') else range(len(perm_importance.importances_mean))
        plt.barh(range(len(perm_importance.importances_mean)), perm_importance.importances_mean)
        plt.yticks(range(len(perm_importance.importances_mean)), feature_names)
        plt.xlabel('Permutation Importance')
        plt.title('Permutation Feature Importance')
        plt.tight_layout()
        plt.show()
        
        return {
            'builtin': importance_builtin if hasattr(self.model, 'feature_importances_') else None,
            'permutation': perm_importance
        }
    
    def shap_analysis(self, sample_size=100):
        """SHAP (SHapley Additive exPlanations) analysis."""
        
        # Create SHAP explainer
        if hasattr(self.model, 'predict_proba'):
            explainer = shap.TreeExplainer(self.model)
        else:
            explainer = shap.LinearExplainer(self.model, self.X_train[:sample_size])
        
        # Calculate SHAP values
        shap_values = explainer.shap_values(self.X_test[:sample_size])
        
        # Summary plot
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, self.X_test[:sample_size], show=False)
        plt.tight_layout()
        plt.show()
        
        # Waterfall plot for single prediction
        if len(shap_values.shape) == 2:  # Binary classification
            shap.waterfall_plot(
                explainer.expected_value, 
                shap_values[0], 
                self.X_test.iloc[0]
            )
        
        return shap_values
    
    def lime_analysis(self, instance_idx=0):
        """LIME (Local Interpretable Model-agnostic Explanations) analysis."""
        
        from lime.lime_tabular import LimeTabularExplainer
        
        # Create LIME explainer
        explainer = LimeTabularExplainer(
            self.X_train.values,
            feature_names=self.X_train.columns if hasattr(self.X_train, 'columns') else None,
            class_names=['Class 0', 'Class 1'],
            mode='classification'
        )
        
        # Explain single instance
        explanation = explainer.explain_instance(
            self.X_test.iloc[instance_idx].values,
            self.model.predict_proba,
            num_features=10
        )
        
        # Show explanation
        explanation.show_in_notebook(show_table=True)
        
        return explanation
    
    def partial_dependence_analysis(self, features):
        """Partial dependence plots."""
        from sklearn.inspection import plot_partial_dependence
        
        fig, ax = plt.subplots(figsize=(12, 8))
        plot_partial_dependence(
            self.model, self.X_train, features, ax=ax
        )
        plt.tight_layout()
        plt.show()
    
    def model_decision_boundary(self, feature1, feature2):
        """Visualize decision boundary for 2D features."""
        
        if len(self.X_train.columns) < 2:
            print("Need at least 2 features for decision boundary visualization")
            return
        
        # Create mesh
        h = 0.02
        x_min, x_max = self.X_train[feature1].min() - 1, self.X_train[feature1].max() + 1
        y_min, y_max = self.X_train[feature2].min() - 1, self.X_train[feature2].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                            np.arange(y_min, y_max, h))
        
        # Create prediction mesh
        mesh_points = np.c_[xx.ravel(), yy.ravel()]
        
        # Add other features as median values
        other_features = [col for col in self.X_train.columns if col not in [feature1, feature2]]
        for feature in other_features:
            median_val = self.X_train[feature].median()
            mesh_points = np.column_stack([mesh_points, np.full(mesh_points.shape[0], median_val)])
        
        # Predict on mesh
        Z = self.model.predict(mesh_points)
        Z = Z.reshape(xx.shape)
        
        # Plot
        plt.figure(figsize=(10, 8))
        plt.contourf(xx, yy, Z, alpha=0.8, cmap=plt.cm.RdYlBu)
        
        # Plot training points
        scatter = plt.scatter(self.X_train[feature1], self.X_train[feature2], 
                            c=self.y_train, cmap=plt.cm.RdYlBu, edgecolors='black')
        plt.colorbar(scatter)
        plt.xlabel(feature1)
        plt.ylabel(feature2)
        plt.title('Model Decision Boundary')
        plt.show()
```

### 18. How do you implement online learning and model updating?

**Answer**: Online learning allows models to learn incrementally from streaming data.

```python
# Online Learning Implementation
from sklearn.linear_model import SGDClassifier, PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import numpy as np

class OnlineLearningSystem:
    def __init__(self, model_type='sgd'):
        self.model_type = model_type
        self.model = self._initialize_model()
        self.performance_history = []
        self.concept_drift_detector = ConceptDriftDetector()
        
    def _initialize_model(self):
        """Initialize online learning model."""
        if self.model_type == 'sgd':
            return SGDClassifier(loss='log', learning_rate='adaptive', eta0=0.01)
        elif self.model_type == 'passive_aggressive':
            return PassiveAggressiveClassifier(C=1.0)
        elif self.model_type == 'naive_bayes':
            return MultinomialNB()
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def partial_fit(self, X_batch, y_batch, classes=None):
        """Update model with new batch of data."""
        
        if not hasattr(self.model, 'partial_fit'):
            raise ValueError(f"Model {self.model_type} doesn't support partial_fit")
        
        # First batch needs class information
        if classes is not None:
            self.model.partial_fit(X_batch, y_batch, classes=classes)
        else:
            self.model.partial_fit(X_batch, y_batch)
    
    def predict_and_update(self, X_batch, y_batch, update=True):
        """Make predictions and optionally update model."""
        
        # Make predictions
        predictions = self.model.predict(X_batch)
        
        # Calculate performance
        accuracy = accuracy_score(y_batch, predictions)
        self.performance_history.append(accuracy)
        
        # Check for concept drift
        drift_detected = self.concept_drift_detector.detect_drift(accuracy)
        
        if drift_detected:
            print(f"Concept drift detected! Accuracy: {accuracy:.3f}")
            self._handle_concept_drift()
        
        # Update model with new data
        if update:
            self.partial_fit(X_batch, y_batch)
        
        return predictions, accuracy, drift_detected
    
    def _handle_concept_drift(self):
        """Handle concept drift by adjusting learning parameters."""
        
        if self.model_type == 'sgd':
            # Increase learning rate temporarily
            self.model.eta0 *= 1.5
        
        # Could also reinitialize model or use ensemble approach
        print("Adjusted model parameters for concept drift")
    
    def simulate_online_learning(self, X, y, batch_size=100, test_size=0.2):
        """Simulate online learning scenario."""
        
        n_samples = len(X)
        n_test = int(n_samples * test_size)
        n_train = n_samples - n_test
        
        # Split into train and test
        X_train, X_test = X[:n_train], X[n_train:]
        y_train, y_test = y[:n_train], y[n_train:]
        
        # Get unique classes
        classes = np.unique(y)
        
        # Process in batches
        accuracies = []
        drift_points = []
        
        for i in range(0, n_train, batch_size):
            end_idx = min(i + batch_size, n_train)
            X_batch = X_train[i:end_idx]
            y_batch = y_train[i:end_idx]
            
            # Update model
            if i == 0:
                self.partial_fit(X_batch, y_batch, classes=classes)
            else:
                self.partial_fit(X_batch, y_batch)
            
            # Test on held-out data
            if len(X_test) > 0:
                test_predictions = self.model.predict(X_test)
                test_accuracy = accuracy_score(y_test, test_predictions)
                accuracies.append(test_accuracy)
                
                # Check for drift
                if self.concept_drift_detector.detect_drift(test_accuracy):
                    drift_points.append(i // batch_size)
        
        return accuracies, drift_points

class ConceptDriftDetector:
    def __init__(self, window_size=10, threshold=0.05):
        self.window_size = window_size
        self.threshold = threshold
        self.performance_window = []
        
    def detect_drift(self, current_performance):
        """Detect concept drift based on performance degradation."""
        
        self.performance_window.append(current_performance)
        
        if len(self.performance_window) > self.window_size:
            self.performance_window.pop(0)
        
        if len(self.performance_window) == self.window_size:
            # Compare recent performance with historical
            recent_avg = np.mean(self.performance_window[-self.window_size//2:])
            historical_avg = np.mean(self.performance_window[:self.window_size//2])
            
            # Drift detected if significant performance drop
            if historical_avg - recent_avg > self.threshold:
                return True
        
        return False

# Ensemble Online Learning
class OnlineEnsemble:
    def __init__(self, n_models=3):
        self.models = []
        self.weights = []
        self.n_models = n_models
        
        # Initialize diverse models
        model_types = ['sgd', 'passive_aggressive', 'naive_bayes']
        for i in range(n_models):
            model_type = model_types[i % len(model_types)]
            self.models.append(OnlineLearningSystem(model_type))
            self.weights.append(1.0 / n_models)
    
    def update_weights(self, accuracies):
        """Update model weights based on performance."""
        
        # Softmax weighting based on accuracy
        exp_accuracies = np.exp(np.array(accuracies))
        self.weights = exp_accuracies / np.sum(exp_accuracies)
    
    def predict(self, X):
        """Ensemble prediction using weighted voting."""
        
        predictions = []
        for model in self.models:
            pred = model.model.predict(X)
            predictions.append(pred)
        
        # Weighted majority voting
        weighted_predictions = np.zeros(len(X))
        for i, (pred, weight) in enumerate(zip(predictions, self.weights)):
            weighted_predictions += weight * pred
        
        return (weighted_predictions > 0.5).astype(int)
    
    def partial_fit(self, X_batch, y_batch, classes=None):
        """Update all models in ensemble."""
        
        accuracies = []
        for model in self.models:
            model.partial_fit(X_batch, y_batch, classes)
            
            # Evaluate individual model performance
            pred = model.model.predict(X_batch)
            acc = accuracy_score(y_batch, pred)
            accuracies.append(acc)
        
        # Update weights based on performance
        self.update_weights(accuracies)
```

### 19. How do you implement A/B testing for machine learning models?

**Answer**: A/B testing allows comparing model performance in production environments.

```python
# A/B Testing for ML Models
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

class MLModelABTest:
    def __init__(self, model_a, model_b, test_name="Model A/B Test"):
        self.model_a = model_a
        self.model_b = model_b
        self.test_name = test_name
        self.results_a = []
        self.results_b = []
        self.traffic_split = 0.5
        
    def set_traffic_split(self, split_ratio):
        """Set traffic split between models (0.5 = 50/50)."""
        self.traffic_split = split_ratio
    
    def route_traffic(self, user_id):
        """Route user to model A or B based on user ID hash."""
        # Consistent routing based on user ID
        hash_value = hash(str(user_id)) % 100
        return 'A' if hash_value < (self.traffic_split * 100) else 'B'
    
    def serve_prediction(self, user_id, features):
        """Serve prediction from appropriate model."""
        
        model_version = self.route_traffic(user_id)
        
        if model_version == 'A':
            prediction = self.model_a.predict([features])[0]
            confidence = self.model_a.predict_proba([features])[0].max()
        else:
            prediction = self.model_b.predict([features])[0]
            confidence = self.model_b.predict_proba([features])[0].max()
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'model_version': model_version,
            'user_id': user_id
        }
    
    def log_result(self, user_id, prediction_result, actual_outcome, 
                   conversion_value=None, response_time=None):
        """Log prediction result and actual outcome."""
        
        result = {
            'user_id': user_id,
            'model_version': prediction_result['model_version'],
            'prediction': prediction_result['prediction'],
            'confidence': prediction_result['confidence'],
            'actual_outcome': actual_outcome,
            'correct': prediction_result['prediction'] == actual_outcome,
            'conversion_value': conversion_value,
            'response_time': response_time,
            'timestamp': pd.Timestamp.now()
        }
        
        if prediction_result['model_version'] == 'A':
            self.results_a.append(result)
        else:
            self.results_b.append(result)
    
    def calculate_metrics(self, results):
        """Calculate performance metrics for a model."""
        
        if not results:
            return {}
        
        df = pd.DataFrame(results)
        
        metrics = {
            'sample_size': len(df),
            'accuracy': df['correct'].mean(),
            'avg_confidence': df['confidence'].mean(),
            'avg_response_time': df['response_time'].mean() if 'response_time' in df else None,
            'conversion_rate': df['actual_outcome'].mean() if df['actual_outcome'].dtype in ['int64', 'float64'] else None,
            'total_conversion_value': df['conversion_value'].sum() if 'conversion_value' in df else None
        }
        
        return metrics
    
    def statistical_significance_test(self, metric='accuracy', alpha=0.05):
        """Perform statistical significance test."""
        
        if not self.results_a or not self.results_b:
            return {"error": "Insufficient data for statistical test"}
        
        df_a = pd.DataFrame(self.results_a)
        df_b = pd.DataFrame(self.results_b)
        
        if metric == 'accuracy':
            successes_a = df_a['correct'].sum()
            trials_a = len(df_a)
            successes_b = df_b['correct'].sum()
            trials_b = len(df_b)
            
            # Two-proportion z-test
            p_a = successes_a / trials_a
            p_b = successes_b / trials_b
            p_pooled = (successes_a + successes_b) / (trials_a + trials_b)
            
            se = np.sqrt(p_pooled * (1 - p_pooled) * (1/trials_a + 1/trials_b))
            z_score = (p_a - p_b) / se
            p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
            
            return {
                'metric': metric,
                'model_a_value': p_a,
                'model_b_value': p_b,
                'difference': p_a - p_b,
                'z_score': z_score,
                'p_value': p_value,
                'significant': p_value < alpha,
                'confidence_interval': self._confidence_interval_proportion(p_a, p_b, trials_a, trials_b)
            }
        
        elif metric == 'conversion_value':
            values_a = df_a['conversion_value'].dropna()
            values_b = df_b['conversion_value'].dropna()
            
            # Two-sample t-test
            t_stat, p_value = stats.ttest_ind(values_a, values_b)
            
            return {
                'metric': metric,
                'model_a_value': values_a.mean(),
                'model_b_value': values_b.mean(),
                'difference': values_a.mean() - values_b.mean(),
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < alpha
            }
    
    def _confidence_interval_proportion(self, p1, p2, n1, n2, confidence=0.95):
        """Calculate confidence interval for difference in proportions."""
        
        z_score = stats.norm.ppf((1 + confidence) / 2)
        se1 = np.sqrt(p1 * (1 - p1) / n1)
        se2 = np.sqrt(p2 * (1 - p2) / n2)
        se_diff = np.sqrt(se1**2 + se2**2)
        
        diff = p1 - p2
        margin_error = z_score * se_diff
        
        return (diff - margin_error, diff + margin_error)
    
    def power_analysis(self, effect_size, alpha=0.05, power=0.8):
        """Calculate required sample size for desired statistical power."""
        
        from statsmodels.stats.power import ttest_power
        
        # Calculate required sample size
        required_n = ttest_power(effect_size, power, alpha, alternative='two-sided')
        
        return {
            'effect_size': effect_size,
            'alpha': alpha,
            'power': power,
            'required_sample_size_per_group': required_n
        }
    
    def generate_report(self):
        """Generate comprehensive A/B test report."""
        
        metrics_a = self.calculate_metrics(self.results_a)
        metrics_b = self.calculate_metrics(self.results_b)
        
        # Statistical tests
        accuracy_test = self.statistical_significance_test('accuracy')
        
        report = {
            'test_name': self.test_name,
            'model_a_metrics': metrics_a,
            'model_b_metrics': metrics_b,
            'statistical_tests': {
                'accuracy': accuracy_test
            },
            'recommendations': self._generate_recommendations(metrics_a, metrics_b, accuracy_test)
        }
        
        return report
    
    def _generate_recommendations(self, metrics_a, metrics_b, accuracy_test):
        """Generate recommendations based on test results."""
        
        recommendations = []
        
        if accuracy_test.get('significant', False):
            if accuracy_test['model_a_value'] > accuracy_test['model_b_value']:
                recommendations.append("Model A shows statistically significant better accuracy")
                recommendations.append("Recommend deploying Model A to 100% of traffic")
            else:
                recommendations.append("Model B shows statistically significant better accuracy")
                recommendations.append("Recommend deploying Model B to 100% of traffic")
        else:
            recommendations.append("No statistically significant difference in accuracy")
            recommendations.append("Consider running test longer or with larger sample size")
        
        # Sample size recommendations
        if metrics_a['sample_size'] < 1000 or metrics_b['sample_size'] < 1000:
            recommendations.append("Sample sizes may be too small for reliable conclusions")
        
        return recommendations
    
    def plot_results(self):
        """Visualize A/B test results."""
        
        metrics_a = self.calculate_metrics(self.results_a)
        metrics_b = self.calculate_metrics(self.results_b)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Accuracy comparison
        axes[0, 0].bar(['Model A', 'Model B'], 
                      [metrics_a['accuracy'], metrics_b['accuracy']], 
                      color=['blue', 'red'], alpha=0.7)
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].set_title('Model Accuracy Comparison')
        axes[0, 0].set_ylim(0, 1)
        
        # Sample size comparison
        axes[0, 1].bar(['Model A', 'Model B'], 
                      [metrics_a['sample_size'], metrics_b['sample_size']], 
                      color=['blue', 'red'], alpha=0.7)
        axes[0, 1].set_ylabel('Sample Size')
        axes[0, 1].set_title('Sample Size Comparison')
        
        # Confidence comparison
        axes[1, 0].bar(['Model A', 'Model B'], 
                      [metrics_a['avg_confidence'], metrics_b['avg_confidence']], 
                      color=['blue', 'red'], alpha=0.7)
        axes[1, 0].set_ylabel('Average Confidence')
        axes[1, 0].set_title('Model Confidence Comparison')
        
        # Performance over time
        if self.results_a and self.results_b:
            df_a = pd.DataFrame(self.results_a)
            df_b = pd.DataFrame(self.results_b)
            
            # Rolling accuracy
            df_a['rolling_accuracy'] = df_a['correct'].rolling(window=50, min_periods=1).mean()
            df_b['rolling_accuracy'] = df_b['correct'].rolling(window=50, min_periods=1).mean()
            
            axes[1, 1].plot(df_a.index, df_a['rolling_accuracy'], label='Model A', color='blue')
            axes[1, 1].plot(df_b.index, df_b['rolling_accuracy'], label='Model B', color='red')
            axes[1, 1].set_xlabel('Prediction Number')
            axes[1, 1].set_ylabel('Rolling Accuracy')
            axes[1, 1].set_title('Accuracy Over Time')
            axes[1, 1].legend()
        
        plt.tight_layout()
        plt.show()

# Example usage
def ab_test_example():
    """Example of running A/B test for ML models."""
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.datasets import make_classification
    
    # Create sample models
    X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
    
    model_a = RandomForestClassifier(n_estimators=50, random_state=42)
    model_b = LogisticRegression(random_state=42)
    
    model_a.fit(X[:800], y[:800])
    model_b.fit(X[:800], y[:800])
    
    # Initialize A/B test
    ab_test = MLModelABTest(model_a, model_b, "RF vs LR Test")
    
    # Simulate user interactions
    test_data = X[800:]
    test_labels = y[800:]
    
    for i, (features, true_label) in enumerate(zip(test_data, test_labels)):
        user_id = f"user_{i}"
        
        # Get prediction
        prediction_result = ab_test.serve_prediction(user_id, features)
        
        # Simulate some noise in actual outcomes
        actual_outcome = true_label if np.random.random() > 0.1 else 1 - true_label
        
        # Log result
        ab_test.log_result(
            user_id, 
            prediction_result, 
            actual_outcome,
            conversion_value=np.random.exponential(10) if actual_outcome else 0,
            response_time=np.random.normal(0.1, 0.02)
        )
    
    # Generate report
    report = ab_test.generate_report()
    
    print("A/B Test Report:")
    print(f"Model A Accuracy: {report['model_a_metrics']['accuracy']:.3f}")
    print(f"Model B Accuracy: {report['model_b_metrics']['accuracy']:.3f}")
    print(f"Statistical Significance: {report['statistical_tests']['accuracy']['significant']}")
    print(f"P-value: {report['statistical_tests']['accuracy']['p_value']:.4f}")
    
    # Plot results
    ab_test.plot_results()
    
    return ab_test, report
```

### 20. How do you implement federated learning?

**Answer**: Federated learning trains models across decentralized data without centralizing the data.

```python
# Federated Learning Implementation
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
import copy

class FederatedLearningClient:
    def __init__(self, client_id, X_local, y_local):
        self.client_id = client_id
        self.X_local = X_local
        self.y_local = y_local
        self.local_model = None
        
    def receive_global_model(self, global_model):
        """Receive global model from server."""
        self.local_model = copy.deepcopy(global_model)
    
    def local_training(self, epochs=5):
        """Train model on local data."""
        
        if self.local_model is None:
            # Initialize local model
            self.local_model = SGDClassifier(loss='log', random_state=42)
            # Fit once to initialize
            self.local_model.fit(self.X_local[:1], self.y_local[:1])
        
        # Local training iterations
        for epoch in range(epochs):
            # Shuffle data
            indices = np.random.permutation(len(self.X_local))
            X_shuffled = self.X_local[indices]
            y_shuffled = self.y_local[indices]
            
            # Mini-batch training
            batch_size = min(32, len(self.X_local))
            for i in range(0, len(X_shuffled), batch_size):
                X_batch = X_shuffled[i:i+batch_size]
                y_batch = y_shuffled[i:i+batch_size]
                
                # Partial fit (online learning)
                self.local_model.partial_fit(X_batch, y_batch)
        
        return self.get_model_parameters()
    
    def get_model_parameters(self):
        """Extract model parameters for aggregation."""
        return {
            'coef_': self.local_model.coef_.copy(),
            'intercept_': self.local_model.intercept_.copy(),
            'data_size': len(self.X_local)
        }
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate local model performance."""
        if self.local_model is None:
            return 0.0
        
        predictions = self.local_model.predict(X_test)
        return accuracy_score(y_test, predictions)

class FederatedLearningServer:
    def __init__(self):
        self.global_model = None
        self.clients = []
        self.round_history = []
        
    def register_client(self, client):
        """Register a client for federated learning."""
        self.clients.append(client)
    
    def initialize_global_model(self, n_features):
        """Initialize global model."""
        self.global_model = SGDClassifier(loss='log', random_state=42)
        
        # Initialize with dummy data to set up model structure
        dummy_X = np.zeros((1, n_features))
        dummy_y = np.array([0])
        self.global_model.fit(dummy_X, dummy_y)
    
    def federated_averaging(self, client_parameters):
        """Aggregate client parameters using FedAvg algorithm."""
        
        if not client_parameters:
            return
        
        # Calculate total data size across all clients
        total_data_size = sum(params['data_size'] for params in client_parameters)
        
        # Weighted average of parameters
        aggregated_coef = np.zeros_like(client_parameters[0]['coef_'])
        aggregated_intercept = np.zeros_like(client_parameters[0]['intercept_'])
        
        for params in client_parameters:
            weight = params['data_size'] / total_data_size
            aggregated_coef += weight * params['coef_']
            aggregated_intercept += weight * params['intercept_']
        
        # Update global model
        self.global_model.coef_ = aggregated_coef
        self.global_model.intercept_ = aggregated_intercept
    
    def run_federated_round(self, selected_clients=None, local_epochs=5):
        """Run one round of federated learning."""
        
        if selected_clients is None:
            selected_clients = self.clients
        
        # Send global model to selected clients
        for client in selected_clients:
            client.receive_global_model(self.global_model)
        
        # Collect local updates
        client_parameters = []
        for client in selected_clients:
            params = client.local_training(epochs=local_epochs)
            client_parameters.append(params)
        
        # Aggregate parameters
        self.federated_averaging(client_parameters)
        
        return len(selected_clients)
    
    def run_federated_learning(self, n_rounds=10, client_fraction=1.0, 
                              local_epochs=5, X_test=None, y_test=None):
        """Run complete federated learning process."""
        
        results = []
        
        for round_num in range(n_rounds):
            print(f"Federated Learning Round {round_num + 1}/{n_rounds}")
            
            # Select subset of clients
            n_selected = max(1, int(len(self.clients) * client_fraction))
            selected_clients = np.random.choice(self.clients, n_selected, replace=False)
            
            # Run federated round
            n_participants = self.run_federated_round(selected_clients, local_epochs)
            
            # Evaluate global model
            if X_test is not None and y_test is not None:
                global_accuracy = self.evaluate_global_model(X_test, y_test)
                
                # Evaluate client models
                client_accuracies = []
                for client in self.clients:
                    client_acc = client.evaluate_model(X_test, y_test)
                    client_accuracies.append(client_acc)
                
                round_result = {
                    'round': round_num + 1,
                    'participants': n_participants,
                    'global_accuracy': global_accuracy,
                    'avg_client_accuracy': np.mean(client_accuracies),
                    'client_accuracies': client_accuracies
                }
                
                results.append(round_result)
                
                print(f"  Global Model Accuracy: {global_accuracy:.3f}")
                print(f"  Average Client Accuracy: {np.mean(client_accuracies):.3f}")
        
        self.round_history = results
        return results
    
    def evaluate_global_model(self, X_test, y_test):
        """Evaluate global model performance."""
        if self.global_model is None:
            return 0.0
        
        predictions = self.global_model.predict(X_test)
        return accuracy_score(y_test, predictions)
    
    def plot_learning_curves(self):
        """Plot federated learning progress."""
        
        if not self.round_history:
            print("No training history available")
            return
        
        rounds = [r['round'] for r in self.round_history]
        global_accuracies = [r['global_accuracy'] for r in self.round_history]
        avg_client_accuracies = [r['avg_client_accuracy'] for r in self.round_history]
        
        plt.figure(figsize=(12, 5))
        
        # Accuracy over rounds
        plt.subplot(1, 2, 1)
        plt.plot(rounds, global_accuracies, 'o-', label='Global Model', linewidth=2)
        plt.plot(rounds, avg_client_accuracies, 's-', label='Average Client', linewidth=2)
        plt.xlabel('Federated Round')
        plt.ylabel('Accuracy')
        plt.title('Federated Learning Progress')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Client accuracy distribution in final round
        plt.subplot(1, 2, 2)
        final_client_accs = self.round_history[-1]['client_accuracies']
        plt.hist(final_client_accs, bins=10, alpha=0.7, edgecolor='black')
        plt.axvline(self.round_history[-1]['global_accuracy'], 
                   color='red', linestyle='--', linewidth=2, label='Global Model')
        plt.xlabel('Accuracy')
        plt.ylabel('Number of Clients')
        plt.title('Client Accuracy Distribution (Final Round)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

# Privacy-Preserving Techniques
class DifferentialPrivacyFL:
    def __init__(self, epsilon=1.0, delta=1e-5):
        self.epsilon = epsilon  # Privacy budget
        self.delta = delta      # Probability of privacy breach
        
    def add_noise_to_gradients(self, gradients, sensitivity=1.0):
        """Add Gaussian noise to gradients for differential privacy."""
        
        # Calculate noise scale
        noise_scale = np.sqrt(2 * np.log(1.25 / self.delta)) * sensitivity / self.epsilon
        
        # Add noise to each gradient component
        noisy_gradients = {}
        for key, grad in gradients.items():
            noise = np.random.normal(0, noise_scale, grad.shape)
            noisy_gradients[key] = grad + noise
        
        return noisy_gradients
    
    def clip_gradients(self, gradients, clip_norm=1.0):
        """Clip gradients to bound sensitivity."""
        
        clipped_gradients = {}
        for key, grad in gradients.items():
            grad_norm = np.linalg.norm(grad)
            if grad_norm > clip_norm:
                clipped_gradients[key] = grad * (clip_norm / grad_norm)
            else:
                clipped_gradients[key] = grad
        
        return clipped_gradients

# Example usage
def federated_learning_example():
    """Example of federated learning with multiple clients."""
    
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    
    # Generate dataset
    X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
    
    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Simulate federated setting by splitting training data among clients
    n_clients = 5
    client_data_size = len(X_train) // n_clients
    
    # Create federated learning server
    fl_server = FederatedLearningServer()
    fl_server.initialize_global_model(X_train.shape[1])
    
    # Create clients with non-IID data distribution
    clients = []
    for i in range(n_clients):
        start_idx = i * client_data_size
        end_idx = start_idx + client_data_size if i < n_clients - 1 else len(X_train)
        
        # Add some bias to make data non-IID
        if i < n_clients // 2:
            # First half of clients get more class 0 samples
            class_0_mask = y_train[start_idx:end_idx] == 0
            biased_indices = np.where(class_0_mask)[0][:int(0.8 * client_data_size)]
            remaining_indices = np.where(~class_0_mask)[0][:client_data_size - len(biased_indices)]
            selected_indices = np.concatenate([biased_indices, remaining_indices])
        else:
            # Second half gets more class 1 samples
            class_1_mask = y_train[start_idx:end_idx] == 1
            biased_indices = np.where(class_1_mask)[0][:int(0.8 * client_data_size)]
            remaining_indices = np.where(~class_1_mask)[0][:client_data_size - len(biased_indices)]
            selected_indices = np.concatenate([biased_indices, remaining_indices])
        
        # Adjust indices to global range
        global_indices = start_idx + selected_indices
        
        X_client = X_train[global_indices]
        y_client = y_train[global_indices]
        
        client = FederatedLearningClient(f"client_{i}", X_client, y_client)
        clients.append(client)
        fl_server.register_client(client)
    
    print(f"Created {len(clients)} federated learning clients")
    print(f"Client data sizes: {[len(c.X_local) for c in clients]}")
    
    # Run federated learning
    results = fl_server.run_federated_learning(
        n_rounds=15,
        client_fraction=0.8,  # 80% of clients participate each round
        local_epochs=3,
        X_test=X_test,
        y_test=y_test
    )
    
    # Plot results
    fl_server.plot_learning_curves()
    
    # Compare with centralized learning
    from sklearn.linear_model import LogisticRegression
    centralized_model = LogisticRegression(random_state=42)
    centralized_model.fit(X_train, y_train)
    centralized_accuracy = accuracy_score(y_test, centralized_model.predict(X_test))
    
    final_fl_accuracy = results[-1]['global_accuracy']
    
    print(f"\nFinal Results:")
    print(f"Federated Learning Accuracy: {final_fl_accuracy:.3f}")
    print(f"Centralized Learning Accuracy: {centralized_accuracy:.3f}")
    print(f"Performance Gap: {centralized_accuracy - final_fl_accuracy:.3f}")
    
    return fl_server, results
```

This comprehensive expansion brings the Machine Learning interview questions to 80+ questions, covering fundamental concepts through advanced techniques like federated learning, A/B testing, and online learning with practical data engineering examples.
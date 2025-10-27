# 🚨 Anomaly Detection - Key Concepts

## 🎯 **Real-World Analogy: The Digital Security Guard**

> **Think of anomaly detection as a highly trained security guard who knows what "normal" looks like and can instantly spot anything unusual - whether it's a suspicious person, an unusual pattern, or something that just doesn't belong.**

## 🔥 **Core Concepts**

### 1. **Statistical Anomaly Detection** 📊

```python
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler

class StatisticalAnomalyDetector:
    def __init__(self):
        self.thresholds = {}
        self.statistics = {}
    
    def fit(self, data, method='zscore'):
        """Learn normal patterns from training data"""
        self.statistics = {
            'mean': np.mean(data),
            'std': np.std(data),
            'median': np.median(data),
            'q1': np.percentile(data, 25),
            'q3': np.percentile(data, 75)
        }
        
        if method == 'zscore':
            self.thresholds['zscore'] = 3  # 3 standard deviations
        elif method == 'iqr':
            iqr = self.statistics['q3'] - self.statistics['q1']
            self.thresholds['iqr_lower'] = self.statistics['q1'] - 1.5 * iqr
            self.thresholds['iqr_upper'] = self.statistics['q3'] + 1.5 * iqr
        
        return self
    
    def detect_anomalies(self, data, method='zscore'):
        """Detect anomalies in new data"""
        anomalies = []
        
        for i, value in enumerate(data):
            is_anomaly = False
            anomaly_score = 0
            
            if method == 'zscore':
                z_score = abs((value - self.statistics['mean']) / self.statistics['std'])
                if z_score > self.thresholds['zscore']:
                    is_anomaly = True
                    anomaly_score = z_score
            
            elif method == 'iqr':
                if value < self.thresholds['iqr_lower'] or value > self.thresholds['iqr_upper']:
                    is_anomaly = True
                    anomaly_score = min(
                        abs(value - self.thresholds['iqr_lower']),
                        abs(value - self.thresholds['iqr_upper'])
                    )
            
            if is_anomaly:
                anomalies.append({
                    'index': i,
                    'value': value,
                    'score': anomaly_score,
                    'method': method
                })
        
        return anomalies
    
    def get_anomaly_summary(self, anomalies):
        """Get summary of detected anomalies"""
        if not anomalies:
            return {"count": 0, "severity": "none"}
        
        scores = [a['score'] for a in anomalies]
        return {
            "count": len(anomalies),
            "avg_score": np.mean(scores),
            "max_score": np.max(scores),
            "severity": "high" if np.max(scores) > 5 else "medium" if np.max(scores) > 3 else "low"
        }

# Usage
detector = StatisticalAnomalyDetector()

# Normal data (e.g., daily website traffic)
normal_data = np.random.normal(1000, 100, 100)  # Mean=1000, std=100

# Train detector
detector.fit(normal_data, method='zscore')

# Test data with anomalies
test_data = np.concatenate([
    np.random.normal(1000, 100, 90),  # Normal data
    [1500, 1600, 400, 300]           # Anomalies
])

# Detect anomalies
anomalies = detector.detect_anomalies(test_data, method='zscore')
summary = detector.get_anomaly_summary(anomalies)

print(f"Found {summary['count']} anomalies with {summary['severity']} severity")
for anomaly in anomalies:
    print(f"Anomaly at index {anomaly['index']}: value={anomaly['value']:.1f}, score={anomaly['score']:.2f}")
```

### 2. **Machine Learning Anomaly Detection** 🤖

```python
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

class MLAnomalyDetector:
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    def fit(self, data, contamination=0.1):
        """Train multiple ML models for anomaly detection"""
        # Normalize data
        data_scaled = self.scaler.fit_transform(data.reshape(-1, 1))
        
        # Initialize models
        self.models = {
            'isolation_forest': IsolationForest(
                contamination=contamination,
                random_state=42
            ),
            'one_class_svm': OneClassSVM(
                kernel='rbf',
                gamma='scale',
                nu=contamination
            ),
            'local_outlier_factor': LocalOutlierFactor(
                n_neighbors=20,
                contamination=contamination
            )
        }
        
        # Fit models
        for name, model in self.models.items():
            if name != 'local_outlier_factor':  # LOF doesn't have separate fit/predict
                model.fit(data_scaled)
        
        self.is_fitted = True
        return self
    
    def detect_anomalies(self, data, ensemble=True):
        """Detect anomalies using trained models"""
        if not self.is_fitted:
            raise ValueError("Models not fitted. Call fit() first.")
        
        # Normalize data
        data_scaled = self.scaler.transform(data.reshape(-1, 1))
        
        predictions = {}
        scores = {}
        
        # Get predictions from each model
        for name, model in self.models.items():
            if name == 'local_outlier_factor':
                # LOF requires fit_predict
                pred = model.fit_predict(data_scaled)
                score = model.negative_outlier_factor_
            else:
                pred = model.predict(data_scaled)
                if hasattr(model, 'decision_function'):
                    score = model.decision_function(data_scaled)
                else:
                    score = model.score_samples(data_scaled)
            
            predictions[name] = pred
            scores[name] = score
        
        if ensemble:
            # Ensemble prediction (majority vote)
            ensemble_pred = []
            for i in range(len(data)):
                votes = [predictions[name][i] for name in predictions]
                # -1 indicates anomaly, 1 indicates normal
                anomaly_votes = sum(1 for vote in votes if vote == -1)
                ensemble_pred.append(-1 if anomaly_votes >= 2 else 1)
            
            return {
                'predictions': ensemble_pred,
                'individual_predictions': predictions,
                'scores': scores
            }
        else:
            return {
                'predictions': predictions,
                'scores': scores
            }
    
    def get_anomaly_indices(self, predictions):
        """Get indices of detected anomalies"""
        if isinstance(predictions, dict) and 'predictions' in predictions:
            pred_array = predictions['predictions']
        else:
            pred_array = predictions
        
        return [i for i, pred in enumerate(pred_array) if pred == -1]

# Usage
ml_detector = MLAnomalyDetector()

# Train on normal data
ml_detector.fit(normal_data, contamination=0.05)

# Detect anomalies
ml_results = ml_detector.detect_anomalies(test_data, ensemble=True)
anomaly_indices = ml_detector.get_anomaly_indices(ml_results)

print(f"ML Ensemble detected {len(anomaly_indices)} anomalies at indices: {anomaly_indices}")

# Individual model results
for model_name, predictions in ml_results['individual_predictions'].items():
    model_anomalies = [i for i, pred in enumerate(predictions) if pred == -1]
    print(f"{model_name}: {len(model_anomalies)} anomalies")
```

### 3. **Time Series Anomaly Detection** ⏰

```python
import pandas as pd
from datetime import datetime, timedelta

class TimeSeriesAnomalyDetector:
    def __init__(self):
        self.seasonal_patterns = {}
        self.trend_model = None
        
    def fit_seasonal_patterns(self, data, freq='D'):
        """Learn seasonal patterns from time series data"""
        df = pd.DataFrame({'value': data.values}, index=data.index)
        
        # Daily patterns
        if freq in ['H', 'T']:  # Hourly or minute data
            self.seasonal_patterns['hour'] = df.groupby(df.index.hour)['value'].agg(['mean', 'std'])
            self.seasonal_patterns['day_of_week'] = df.groupby(df.index.dayofweek)['value'].agg(['mean', 'std'])
        
        # Weekly patterns
        if freq in ['D', 'H']:  # Daily or hourly data
            self.seasonal_patterns['day_of_week'] = df.groupby(df.index.dayofweek)['value'].agg(['mean', 'std'])
        
        # Monthly patterns
        self.seasonal_patterns['month'] = df.groupby(df.index.month)['value'].agg(['mean', 'std'])
        
        return self
    
    def detect_seasonal_anomalies(self, data, threshold=3):
        """Detect anomalies based on seasonal patterns"""
        anomalies = []
        
        for i, (timestamp, value) in enumerate(zip(data.index, data.values)):
            expected_ranges = []
            
            # Check against different seasonal patterns
            for pattern_name, pattern_data in self.seasonal_patterns.items():
                if pattern_name == 'hour':
                    pattern_key = timestamp.hour
                elif pattern_name == 'day_of_week':
                    pattern_key = timestamp.dayofweek
                elif pattern_name == 'month':
                    pattern_key = timestamp.month
                else:
                    continue
                
                if pattern_key in pattern_data.index:
                    mean_val = pattern_data.loc[pattern_key, 'mean']
                    std_val = pattern_data.loc[pattern_key, 'std']
                    
                    # Calculate z-score for this pattern
                    z_score = abs((value - mean_val) / std_val) if std_val > 0 else 0
                    
                    if z_score > threshold:
                        expected_ranges.append({
                            'pattern': pattern_name,
                            'expected_mean': mean_val,
                            'expected_std': std_val,
                            'z_score': z_score
                        })
            
            # If anomalous in multiple patterns, it's likely a real anomaly
            if len(expected_ranges) >= 2:
                anomalies.append({
                    'index': i,
                    'timestamp': timestamp,
                    'value': value,
                    'anomaly_patterns': expected_ranges,
                    'severity': 'high' if len(expected_ranges) >= 3 else 'medium'
                })
        
        return anomalies
    
    def detect_trend_anomalies(self, data, window=7):
        """Detect anomalies in trend changes"""
        # Calculate rolling statistics
        rolling_mean = data.rolling(window=window).mean()
        rolling_std = data.rolling(window=window).std()
        
        # Detect points that deviate significantly from recent trend
        anomalies = []
        for i in range(window, len(data)):
            current_value = data.iloc[i]
            expected_mean = rolling_mean.iloc[i-1]  # Use previous window
            expected_std = rolling_std.iloc[i-1]
            
            if expected_std > 0:
                z_score = abs((current_value - expected_mean) / expected_std)
                
                if z_score > 3:  # 3 sigma threshold
                    anomalies.append({
                        'index': i,
                        'timestamp': data.index[i],
                        'value': current_value,
                        'expected_mean': expected_mean,
                        'z_score': z_score,
                        'type': 'trend_anomaly'
                    })
        
        return anomalies

# Usage
ts_detector = TimeSeriesAnomalyDetector()

# Create time series data with seasonal patterns
dates = pd.date_range('2024-01-01', periods=100, freq='D')
seasonal_data = pd.Series(
    1000 + 200 * np.sin(2 * np.pi * np.arange(100) / 7) + np.random.normal(0, 50, 100),
    index=dates
)

# Add some anomalies
seasonal_data.iloc[30] = 2000  # Spike
seasonal_data.iloc[60] = 200   # Drop

# Fit seasonal patterns
ts_detector.fit_seasonal_patterns(seasonal_data, freq='D')

# Detect anomalies
seasonal_anomalies = ts_detector.detect_seasonal_anomalies(seasonal_data)
trend_anomalies = ts_detector.detect_trend_anomalies(seasonal_data)

print(f"Seasonal anomalies: {len(seasonal_anomalies)}")
print(f"Trend anomalies: {len(trend_anomalies)}")

for anomaly in seasonal_anomalies:
    print(f"Seasonal anomaly on {anomaly['timestamp'].date()}: value={anomaly['value']:.1f}")
```

### 4. **Real-time Anomaly Detection** ⚡

```python
from collections import deque
import threading
import time

class RealTimeAnomalyDetector:
    def __init__(self, window_size=100, update_interval=10):
        self.window_size = window_size
        self.update_interval = update_interval
        self.data_buffer = deque(maxlen=window_size)
        self.anomaly_buffer = deque(maxlen=50)
        
        self.statistics = {'mean': 0, 'std': 1}
        self.is_running = False
        self.callbacks = []
        
    def add_callback(self, callback_func):
        """Add callback function to be called when anomaly is detected"""
        self.callbacks.append(callback_func)
    
    def update_statistics(self):
        """Update running statistics"""
        if len(self.data_buffer) >= 10:  # Need minimum data points
            data_array = np.array(self.data_buffer)
            self.statistics['mean'] = np.mean(data_array)
            self.statistics['std'] = np.std(data_array)
    
    def process_data_point(self, value, timestamp=None):
        """Process a single data point in real-time"""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Add to buffer
        self.data_buffer.append(value)
        
        # Check for anomaly
        if len(self.data_buffer) >= 10:
            z_score = abs((value - self.statistics['mean']) / self.statistics['std'])
            
            if z_score > 3:  # Anomaly threshold
                anomaly = {
                    'timestamp': timestamp,
                    'value': value,
                    'z_score': z_score,
                    'severity': 'high' if z_score > 5 else 'medium'
                }
                
                self.anomaly_buffer.append(anomaly)
                
                # Trigger callbacks
                for callback in self.callbacks:
                    try:
                        callback(anomaly)
                    except Exception as e:
                        print(f"Callback error: {e}")
                
                return anomaly
        
        return None
    
    def start_monitoring(self):
        """Start real-time monitoring in background thread"""
        self.is_running = True
        
        def monitor_loop():
            while self.is_running:
                self.update_statistics()
                time.sleep(self.update_interval)
        
        monitor_thread = threading.Thread(target=monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.is_running = False
    
    def get_recent_anomalies(self, minutes=60):
        """Get anomalies from last N minutes"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        recent_anomalies = [
            anomaly for anomaly in self.anomaly_buffer
            if anomaly['timestamp'] > cutoff_time
        ]
        
        return recent_anomalies

# Usage
def anomaly_alert(anomaly):
    """Callback function for anomaly alerts"""
    print(f"🚨 ANOMALY DETECTED: Value {anomaly['value']:.2f} at {anomaly['timestamp']}")
    print(f"   Z-score: {anomaly['z_score']:.2f}, Severity: {anomaly['severity']}")

# Initialize real-time detector
rt_detector = RealTimeAnomalyDetector(window_size=50, update_interval=1)
rt_detector.add_callback(anomaly_alert)
rt_detector.start_monitoring()

# Simulate real-time data stream
print("Starting real-time anomaly detection...")
for i in range(100):
    # Normal data most of the time
    if i % 20 == 0:  # Inject anomaly every 20 points
        value = np.random.normal(1000, 100) + 500  # Anomalous value
    else:
        value = np.random.normal(1000, 100)  # Normal value
    
    anomaly = rt_detector.process_data_point(value)
    time.sleep(0.1)  # Simulate real-time delay

rt_detector.stop_monitoring()

# Get summary
recent_anomalies = rt_detector.get_recent_anomalies(minutes=10)
print(f"\nDetected {len(recent_anomalies)} anomalies in the last 10 minutes")
```

## 🎯 **Business Applications**

### **Fraud Detection**
```python
class FraudDetector:
    def __init__(self):
        self.user_profiles = {}
        self.transaction_detector = MLAnomalyDetector()
    
    def build_user_profile(self, user_id, transactions):
        """Build normal behavior profile for user"""
        features = []
        for txn in transactions:
            features.append([
                txn['amount'],
                txn['hour_of_day'],
                txn['day_of_week'],
                txn['merchant_category']
            ])
        
        self.user_profiles[user_id] = {
            'avg_amount': np.mean([t['amount'] for t in transactions]),
            'std_amount': np.std([t['amount'] for t in transactions]),
            'common_hours': [t['hour_of_day'] for t in transactions],
            'common_merchants': [t['merchant_category'] for t in transactions]
        }
    
    def detect_fraud(self, user_id, transaction):
        """Detect if transaction is potentially fraudulent"""
        if user_id not in self.user_profiles:
            return {'is_fraud': False, 'reason': 'No profile available'}
        
        profile = self.user_profiles[user_id]
        fraud_indicators = []
        
        # Amount anomaly
        amount_z = abs((transaction['amount'] - profile['avg_amount']) / profile['std_amount'])
        if amount_z > 3:
            fraud_indicators.append(f"Unusual amount (z-score: {amount_z:.2f})")
        
        # Time anomaly
        if transaction['hour_of_day'] not in profile['common_hours']:
            fraud_indicators.append("Unusual time of day")
        
        # Merchant anomaly
        if transaction['merchant_category'] not in profile['common_merchants']:
            fraud_indicators.append("Unusual merchant category")
        
        is_fraud = len(fraud_indicators) >= 2
        
        return {
            'is_fraud': is_fraud,
            'confidence': len(fraud_indicators) / 3,
            'indicators': fraud_indicators
        }

# Usage for fraud detection
fraud_detector = FraudDetector()

# Build user profile from historical transactions
user_transactions = [
    {'amount': 50, 'hour_of_day': 14, 'day_of_week': 1, 'merchant_category': 'grocery'},
    {'amount': 75, 'hour_of_day': 18, 'day_of_week': 3, 'merchant_category': 'restaurant'},
    # ... more transactions
]

fraud_detector.build_user_profile('user_123', user_transactions)

# Check new transaction
new_transaction = {'amount': 2000, 'hour_of_day': 3, 'day_of_week': 6, 'merchant_category': 'electronics'}
fraud_result = fraud_detector.detect_fraud('user_123', new_transaction)

print(f"Fraud detection result: {fraud_result}")
```
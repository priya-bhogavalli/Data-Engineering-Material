# 📈 AI-Powered Forecasting - Key Concepts

## 🎯 **Real-World Analogy: The Weather Forecaster with AI Superpowers**

> **Think of AI forecasting like a weather forecaster who can predict not just tomorrow's weather, but also sales trends, stock prices, and customer behavior. It uses historical patterns, seasonal trends, and external factors to make predictions with superhuman accuracy.**

## 🔥 **Core Concepts**

### 1. **Time Series Fundamentals** 📊

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TimeSeriesAnalyzer:
    def __init__(self):
        self.data = None
        self.trends = {}
    
    def load_data(self, data, date_column, value_column):
        """Load and prepare time series data"""
        df = pd.DataFrame(data)
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.sort_values(date_column)
        df.set_index(date_column, inplace=True)
        
        self.data = df[value_column]
        return self.data
    
    def detect_patterns(self):
        """Detect key patterns in time series"""
        patterns = {}
        
        # Trend detection
        patterns['trend'] = self.detect_trend()
        
        # Seasonality detection
        patterns['seasonality'] = self.detect_seasonality()
        
        # Outliers
        patterns['outliers'] = self.detect_outliers()
        
        return patterns
    
    def detect_trend(self):
        """Detect overall trend direction"""
        # Simple linear trend
        x = np.arange(len(self.data))
        coeffs = np.polyfit(x, self.data.values, 1)
        
        if coeffs[0] > 0.01:
            return "increasing"
        elif coeffs[0] < -0.01:
            return "decreasing"
        else:
            return "stable"
    
    def detect_seasonality(self):
        """Detect seasonal patterns"""
        # Check for weekly seasonality
        if len(self.data) >= 14:
            weekly_pattern = self.data.groupby(self.data.index.dayofweek).mean()
            weekly_variance = weekly_pattern.var()
            
            if weekly_variance > self.data.var() * 0.1:
                return {"type": "weekly", "strength": weekly_variance}
        
        return {"type": "none", "strength": 0}
    
    def detect_outliers(self, threshold=2):
        """Detect outliers using z-score"""
        z_scores = np.abs((self.data - self.data.mean()) / self.data.std())
        outliers = self.data[z_scores > threshold]
        
        return {
            "count": len(outliers),
            "dates": outliers.index.tolist(),
            "values": outliers.values.tolist()
        }

# Usage
analyzer = TimeSeriesAnalyzer()

# Sample sales data
sales_data = [
    {"date": "2024-01-01", "sales": 1000},
    {"date": "2024-01-02", "sales": 1200},
    {"date": "2024-01-03", "sales": 1100},
    # ... more data
]

ts_data = analyzer.load_data(sales_data, "date", "sales")
patterns = analyzer.detect_patterns()

print(f"Trend: {patterns['trend']}")
print(f"Seasonality: {patterns['seasonality']['type']}")
print(f"Outliers found: {patterns['outliers']['count']}")
```

### 2. **Traditional Forecasting Models** 📉

```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from sklearn.metrics import mean_absolute_error, mean_squared_error

class TraditionalForecaster:
    def __init__(self):
        self.models = {}
        self.fitted_models = {}
    
    def fit_arima(self, data, order=(1,1,1)):
        """Fit ARIMA model"""
        model = ARIMA(data, order=order)
        fitted_model = model.fit()
        
        self.fitted_models['arima'] = fitted_model
        return fitted_model
    
    def fit_exponential_smoothing(self, data, seasonal_periods=7):
        """Fit Exponential Smoothing model"""
        model = ETSModel(
            data, 
            error='add', 
            trend='add', 
            seasonal='add',
            seasonal_periods=seasonal_periods
        )
        fitted_model = model.fit()
        
        self.fitted_models['ets'] = fitted_model
        return fitted_model
    
    def forecast(self, model_name, steps=7):
        """Generate forecasts"""
        if model_name not in self.fitted_models:
            raise ValueError(f"Model {model_name} not fitted")
        
        model = self.fitted_models[model_name]
        
        if model_name == 'arima':
            forecast = model.forecast(steps=steps)
            conf_int = model.get_forecast(steps=steps).conf_int()
        else:  # ETS
            forecast = model.forecast(steps=steps)
            conf_int = None
        
        return {
            "forecast": forecast.tolist(),
            "confidence_interval": conf_int.values.tolist() if conf_int is not None else None
        }
    
    def evaluate_model(self, model_name, test_data):
        """Evaluate model performance"""
        if model_name not in self.fitted_models:
            raise ValueError(f"Model {model_name} not fitted")
        
        model = self.fitted_models[model_name]
        predictions = model.forecast(steps=len(test_data))
        
        mae = mean_absolute_error(test_data, predictions)
        mse = mean_squared_error(test_data, predictions)
        rmse = np.sqrt(mse)
        
        return {
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
            "mape": np.mean(np.abs((test_data - predictions) / test_data)) * 100
        }

# Usage
forecaster = TraditionalForecaster()

# Fit models
arima_model = forecaster.fit_arima(ts_data)
ets_model = forecaster.fit_exponential_smoothing(ts_data)

# Generate forecasts
arima_forecast = forecaster.forecast('arima', steps=7)
ets_forecast = forecaster.forecast('ets', steps=7)

print(f"ARIMA 7-day forecast: {arima_forecast['forecast']}")
print(f"ETS 7-day forecast: {ets_forecast['forecast']}")
```

### 3. **Deep Learning Forecasting** 🧠

```python
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MinMaxScaler

class LSTMForecaster(nn.Module):
    def __init__(self, input_size=1, hidden_size=50, num_layers=2, output_size=1):
        super(LSTMForecaster, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

class TimeSeriesDataset(Dataset):
    def __init__(self, data, sequence_length=10):
        self.data = data
        self.sequence_length = sequence_length
        
    def __len__(self):
        return len(self.data) - self.sequence_length
    
    def __getitem__(self, idx):
        x = self.data[idx:idx + self.sequence_length]
        y = self.data[idx + self.sequence_length]
        return torch.FloatTensor(x), torch.FloatTensor([y])

class DeepLearningForecaster:
    def __init__(self, sequence_length=10):
        self.sequence_length = sequence_length
        self.scaler = MinMaxScaler()
        self.model = None
        
    def prepare_data(self, data):
        """Prepare data for LSTM training"""
        # Normalize data
        data_scaled = self.scaler.fit_transform(data.values.reshape(-1, 1)).flatten()
        
        # Create dataset
        dataset = TimeSeriesDataset(data_scaled, self.sequence_length)
        dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
        
        return dataloader, data_scaled
    
    def train_model(self, data, epochs=100):
        """Train LSTM model"""
        dataloader, scaled_data = self.prepare_data(data)
        
        self.model = LSTMForecaster()
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            for batch_x, batch_y in dataloader:
                optimizer.zero_grad()
                
                # Reshape for LSTM (batch_size, sequence_length, input_size)
                batch_x = batch_x.unsqueeze(-1)
                
                outputs = self.model(batch_x)
                loss = criterion(outputs, batch_y)
                
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            if epoch % 20 == 0:
                print(f'Epoch [{epoch}/{epochs}], Loss: {total_loss/len(dataloader):.4f}')
    
    def forecast(self, data, steps=7):
        """Generate forecasts using trained model"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        self.model.eval()
        
        # Prepare last sequence
        data_scaled = self.scaler.transform(data.values.reshape(-1, 1)).flatten()
        last_sequence = data_scaled[-self.sequence_length:]
        
        forecasts = []
        current_sequence = last_sequence.copy()
        
        with torch.no_grad():
            for _ in range(steps):
                # Prepare input
                input_tensor = torch.FloatTensor(current_sequence).unsqueeze(0).unsqueeze(-1)
                
                # Predict next value
                prediction = self.model(input_tensor)
                predicted_value = prediction.item()
                
                forecasts.append(predicted_value)
                
                # Update sequence for next prediction
                current_sequence = np.append(current_sequence[1:], predicted_value)
        
        # Inverse transform to original scale
        forecasts_scaled = np.array(forecasts).reshape(-1, 1)
        forecasts_original = self.scaler.inverse_transform(forecasts_scaled).flatten()
        
        return forecasts_original.tolist()

# Usage
dl_forecaster = DeepLearningForecaster(sequence_length=14)
dl_forecaster.train_model(ts_data, epochs=100)
dl_forecast = dl_forecaster.forecast(ts_data, steps=7)

print(f"Deep Learning 7-day forecast: {dl_forecast}")
```

### 4. **Multi-variate Forecasting** 🔗

```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

class MultivariateForecaster:
    def __init__(self):
        self.models = {}
        self.feature_columns = []
        
    def create_features(self, data, target_column, external_features=None):
        """Create features for multivariate forecasting"""
        df = data.copy()
        
        # Lag features
        for lag in [1, 7, 14, 30]:
            df[f'{target_column}_lag_{lag}'] = df[target_column].shift(lag)
        
        # Rolling statistics
        for window in [7, 14, 30]:
            df[f'{target_column}_rolling_mean_{window}'] = df[target_column].rolling(window).mean()
            df[f'{target_column}_rolling_std_{window}'] = df[target_column].rolling(window).std()
        
        # Time-based features
        df['day_of_week'] = df.index.dayofweek
        df['month'] = df.index.month
        df['quarter'] = df.index.quarter
        df['is_weekend'] = (df.index.dayofweek >= 5).astype(int)
        
        # External features
        if external_features:
            for feature_name, feature_data in external_features.items():
                df[feature_name] = feature_data
        
        # Remove rows with NaN values
        df = df.dropna()
        
        # Store feature columns
        self.feature_columns = [col for col in df.columns if col != target_column]
        
        return df
    
    def train_model(self, data, target_column, model_type='random_forest'):
        """Train multivariate forecasting model"""
        # Create features
        df_features = self.create_features(data, target_column)
        
        X = df_features[self.feature_columns]
        y = df_features[target_column]
        
        # Train model
        if model_type == 'random_forest':
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        elif model_type == 'linear':
            model = LinearRegression()
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        model.fit(X, y)
        self.models[model_type] = model
        
        return model
    
    def forecast_multivariate(self, data, target_column, model_type='random_forest', steps=7):
        """Generate multivariate forecasts"""
        if model_type not in self.models:
            raise ValueError(f"Model {model_type} not trained")
        
        model = self.models[model_type]
        forecasts = []
        
        # Create a copy of data for iterative forecasting
        forecast_data = data.copy()
        
        for step in range(steps):
            # Create features for current state
            df_features = self.create_features(forecast_data, target_column)
            
            if len(df_features) == 0:
                break
            
            # Get latest features
            latest_features = df_features[self.feature_columns].iloc[-1:].values
            
            # Predict next value
            prediction = model.predict(latest_features)[0]
            forecasts.append(prediction)
            
            # Add prediction to data for next iteration
            next_date = forecast_data.index[-1] + pd.Timedelta(days=1)
            forecast_data.loc[next_date] = {target_column: prediction}
        
        return forecasts
    
    def get_feature_importance(self, model_type='random_forest'):
        """Get feature importance for interpretation"""
        if model_type not in self.models:
            raise ValueError(f"Model {model_type} not trained")
        
        model = self.models[model_type]
        
        if hasattr(model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            return importance_df
        else:
            return None

# Usage
mv_forecaster = MultivariateForecaster()

# Add external features (e.g., weather, holidays, marketing spend)
external_features = {
    'temperature': np.random.normal(20, 5, len(ts_data)),
    'is_holiday': np.random.choice([0, 1], len(ts_data), p=[0.9, 0.1]),
    'marketing_spend': np.random.normal(1000, 200, len(ts_data))
}

# Create DataFrame with target and features
forecast_df = pd.DataFrame({
    'sales': ts_data.values
}, index=ts_data.index)

# Train model
mv_forecaster.train_model(forecast_df, 'sales', model_type='random_forest')

# Generate forecasts
mv_forecast = mv_forecaster.forecast_multivariate(forecast_df, 'sales', steps=7)

print(f"Multivariate 7-day forecast: {mv_forecast}")

# Feature importance
importance = mv_forecaster.get_feature_importance()
print("\nTop 5 most important features:")
print(importance.head())
```

## 🎯 **Business Applications**

### **Demand Forecasting**
```python
class DemandForecaster:
    def __init__(self):
        self.product_forecasters = {}
    
    def forecast_product_demand(self, product_id, historical_sales, external_factors):
        """Forecast demand for specific product"""
        # Combine multiple forecasting methods
        forecasters = {
            'arima': TraditionalForecaster(),
            'lstm': DeepLearningForecaster(),
            'multivariate': MultivariateForecaster()
        }
        
        forecasts = {}
        for name, forecaster in forecasters.items():
            try:
                if name == 'multivariate':
                    forecaster.train_model(historical_sales, 'demand')
                    forecast = forecaster.forecast_multivariate(historical_sales, 'demand')
                else:
                    forecaster.fit_arima(historical_sales['demand'])
                    forecast = forecaster.forecast('arima', steps=30)['forecast']
                
                forecasts[name] = forecast
            except Exception as e:
                print(f"Error with {name} forecaster: {e}")
        
        # Ensemble forecast (simple average)
        if forecasts:
            ensemble_forecast = np.mean(list(forecasts.values()), axis=0)
            return {
                'product_id': product_id,
                'forecast_30_days': ensemble_forecast.tolist(),
                'individual_forecasts': forecasts,
                'confidence': 'high' if len(forecasts) >= 2 else 'medium'
            }
        
        return None

# Usage for business planning
demand_forecaster = DemandForecaster()
product_forecast = demand_forecaster.forecast_product_demand(
    'PROD_001', 
    forecast_df, 
    external_factors
)

print(f"30-day demand forecast for PROD_001: {product_forecast['forecast_30_days'][:7]}...")  # Show first 7 days
```
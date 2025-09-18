# 🤖 Machine Learning Advanced Interview Questions & Answers

## 📋 Table of Contents
- [Advanced Algorithms](#advanced-algorithms)
- [Deep Learning](#deep-learning)
- [Model Optimization](#model-optimization)
- [MLOps & Production](#mlops--production)
- [Specialized Domains](#specialized-domains)
- [Research & Innovation](#research--innovation)

---

## Advanced Algorithms

### 1. Explain ensemble methods and their mathematical foundations.
**Answer:**
**Bagging (Bootstrap Aggregating):**
```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

# Mathematical foundation: Variance reduction
# Var(average) = Var(X)/n for independent variables
# For correlated variables: Var = ρσ² + (1-ρ)σ²/n

class CustomBagging:
    def __init__(self, base_estimator, n_estimators=10):
        self.base_estimator = base_estimator
        self.n_estimators = n_estimators
        self.estimators = []
    
    def fit(self, X, y):
        n_samples = X.shape[0]
        
        for _ in range(self.n_estimators):
            # Bootstrap sampling
            indices = np.random.choice(n_samples, n_samples, replace=True)
            X_bootstrap = X[indices]
            y_bootstrap = y[indices]
            
            # Train base estimator
            estimator = self.base_estimator.__class__(**self.base_estimator.get_params())
            estimator.fit(X_bootstrap, y_bootstrap)
            self.estimators.append(estimator)
    
    def predict(self, X):
        predictions = np.array([est.predict(X) for est in self.estimators])
        # Majority voting for classification
        return np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=predictions)
```

**Boosting (AdaBoost):**
```python
class AdaBoost:
    def __init__(self, n_estimators=50):
        self.n_estimators = n_estimators
        self.estimators = []
        self.estimator_weights = []
    
    def fit(self, X, y):
        n_samples = X.shape[0]
        sample_weights = np.ones(n_samples) / n_samples
        
        for _ in range(self.n_estimators):
            # Train weak learner
            estimator = DecisionTreeClassifier(max_depth=1)
            estimator.fit(X, y, sample_weight=sample_weights)
            
            # Calculate predictions and error
            predictions = estimator.predict(X)
            error = np.sum(sample_weights * (predictions != y))
            
            # Calculate estimator weight
            alpha = 0.5 * np.log((1 - error) / max(error, 1e-10))
            
            # Update sample weights
            sample_weights *= np.exp(-alpha * y * predictions)
            sample_weights /= np.sum(sample_weights)
            
            self.estimators.append(estimator)
            self.estimator_weights.append(alpha)
    
    def predict(self, X):
        predictions = np.zeros(X.shape[0])
        for estimator, weight in zip(self.estimators, self.estimator_weights):
            predictions += weight * estimator.predict(X)
        return np.sign(predictions)
```

**Gradient Boosting:**
```python
class GradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=0.1):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.estimators = []
    
    def fit(self, X, y):
        # Initialize with mean
        self.initial_prediction = np.mean(y)
        predictions = np.full(y.shape, self.initial_prediction)
        
        for _ in range(self.n_estimators):
            # Calculate residuals (negative gradient)
            residuals = y - predictions
            
            # Fit estimator to residuals
            estimator = DecisionTreeClassifier(max_depth=3)
            estimator.fit(X, residuals)
            
            # Update predictions
            update = self.learning_rate * estimator.predict(X)
            predictions += update
            
            self.estimators.append(estimator)
    
    def predict(self, X):
        predictions = np.full(X.shape[0], self.initial_prediction)
        for estimator in self.estimators:
            predictions += self.learning_rate * estimator.predict(X)
        return predictions
```

### 2. How do you implement and optimize Support Vector Machines?
**Answer:**
**SVM Mathematical Foundation:**
```python
import numpy as np
from scipy.optimize import minimize
import cvxpy as cp

class SVM:
    def __init__(self, C=1.0, kernel='rbf', gamma=1.0):
        self.C = C
        self.kernel = kernel
        self.gamma = gamma
    
    def _kernel_function(self, X1, X2):
        if self.kernel == 'linear':
            return np.dot(X1, X2.T)
        elif self.kernel == 'rbf':
            # RBF kernel: K(x,y) = exp(-γ||x-y||²)
            pairwise_sq_dists = np.sum(X1**2, axis=1).reshape(-1, 1) + \
                               np.sum(X2**2, axis=1) - 2 * np.dot(X1, X2.T)
            return np.exp(-self.gamma * pairwise_sq_dists)
        elif self.kernel == 'poly':
            return (np.dot(X1, X2.T) + 1) ** 3
    
    def fit(self, X, y):
        n_samples = X.shape[0]
        
        # Compute kernel matrix
        K = self._kernel_function(X, X)
        
        # Quadratic programming formulation
        # Minimize: (1/2) * α^T * Q * α - 1^T * α
        # Subject to: 0 ≤ α ≤ C and y^T * α = 0
        
        P = cp.Variable(n_samples)
        Q = np.outer(y, y) * K
        
        objective = cp.Minimize(0.5 * cp.quad_form(P, Q) - cp.sum(P))
        constraints = [
            P >= 0,
            P <= self.C,
            cp.sum(cp.multiply(y, P)) == 0
        ]
        
        problem = cp.Problem(objective, constraints)
        problem.solve()
        
        self.alpha = P.value
        self.support_vectors_idx = np.where(self.alpha > 1e-5)[0]
        self.support_vectors = X[self.support_vectors_idx]
        self.support_vector_labels = y[self.support_vectors_idx]
        self.alpha_sv = self.alpha[self.support_vectors_idx]
        
        # Calculate bias term
        self.b = np.mean(
            self.support_vector_labels - 
            np.sum(self.alpha_sv * self.support_vector_labels * 
                   self._kernel_function(self.support_vectors, self.support_vectors), axis=1)
        )
    
    def predict(self, X):
        decision_function = (
            np.sum(self.alpha_sv * self.support_vector_labels * 
                   self._kernel_function(self.support_vectors, X).T, axis=1) + self.b
        )
        return np.sign(decision_function)
```

**SMO (Sequential Minimal Optimization):**
```python
class SMO_SVM:
    def __init__(self, C=1.0, tol=1e-3, max_passes=5):
        self.C = C
        self.tol = tol
        self.max_passes = max_passes
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.alpha = np.zeros(n_samples)
        self.b = 0
        self.X = X
        self.y = y
        
        passes = 0
        while passes < self.max_passes:
            num_changed_alphas = 0
            
            for i in range(n_samples):
                Ei = self._decision_function(X[i]) - y[i]
                
                if ((y[i] * Ei < -self.tol and self.alpha[i] < self.C) or
                    (y[i] * Ei > self.tol and self.alpha[i] > 0)):
                    
                    # Select j randomly
                    j = np.random.choice([k for k in range(n_samples) if k != i])
                    Ej = self._decision_function(X[j]) - y[j]
                    
                    # Save old alphas
                    alpha_i_old = self.alpha[i]
                    alpha_j_old = self.alpha[j]
                    
                    # Compute bounds
                    if y[i] != y[j]:
                        L = max(0, self.alpha[j] - self.alpha[i])
                        H = min(self.C, self.C + self.alpha[j] - self.alpha[i])
                    else:
                        L = max(0, self.alpha[i] + self.alpha[j] - self.C)
                        H = min(self.C, self.alpha[i] + self.alpha[j])
                    
                    if L == H:
                        continue
                    
                    # Compute eta
                    eta = 2 * np.dot(X[i], X[j]) - np.dot(X[i], X[i]) - np.dot(X[j], X[j])
                    if eta >= 0:
                        continue
                    
                    # Update alpha[j]
                    self.alpha[j] -= y[j] * (Ei - Ej) / eta
                    self.alpha[j] = max(L, min(H, self.alpha[j]))
                    
                    if abs(self.alpha[j] - alpha_j_old) < 1e-5:
                        continue
                    
                    # Update alpha[i]
                    self.alpha[i] += y[i] * y[j] * (alpha_j_old - self.alpha[j])
                    
                    # Update bias
                    b1 = self.b - Ei - y[i] * (self.alpha[i] - alpha_i_old) * np.dot(X[i], X[i]) - \
                         y[j] * (self.alpha[j] - alpha_j_old) * np.dot(X[i], X[j])
                    b2 = self.b - Ej - y[i] * (self.alpha[i] - alpha_i_old) * np.dot(X[i], X[j]) - \
                         y[j] * (self.alpha[j] - alpha_j_old) * np.dot(X[j], X[j])
                    
                    if 0 < self.alpha[i] < self.C:
                        self.b = b1
                    elif 0 < self.alpha[j] < self.C:
                        self.b = b2
                    else:
                        self.b = (b1 + b2) / 2
                    
                    num_changed_alphas += 1
            
            if num_changed_alphas == 0:
                passes += 1
            else:
                passes = 0
    
    def _decision_function(self, x):
        return np.sum(self.alpha * self.y * np.dot(self.X, x)) + self.b
```

### 3. Implement advanced dimensionality reduction techniques.
**Answer:**
**t-SNE Implementation:**
```python
import numpy as np
from scipy.spatial.distance import pdist, squareform

class TSNE:
    def __init__(self, n_components=2, perplexity=30, learning_rate=200, n_iter=1000):
        self.n_components = n_components
        self.perplexity = perplexity
        self.learning_rate = learning_rate
        self.n_iter = n_iter
    
    def _compute_pairwise_affinities(self, X):
        """Compute pairwise affinities with Gaussian kernel"""
        n = X.shape[0]
        P = np.zeros((n, n))
        
        for i in range(n):
            # Binary search for sigma that gives desired perplexity
            beta_min, beta_max = -np.inf, np.inf
            beta = 1.0
            
            for _ in range(50):  # Max iterations for binary search
                # Compute probabilities
                diff = X[i] - X
                distances = np.sum(diff**2, axis=1)
                Pi = np.exp(-distances * beta)
                Pi[i] = 0
                sum_Pi = np.sum(Pi)
                
                if sum_Pi == 0:
                    Pi = np.ones(n) / n
                    sum_Pi = 1.0
                
                Pi /= sum_Pi
                
                # Compute perplexity
                H = -np.sum(Pi * np.log2(Pi + 1e-8))
                perp = 2**H
                
                # Adjust beta
                if perp > self.perplexity:
                    beta_min = beta
                    beta = (beta + beta_max) / 2 if beta_max != np.inf else beta * 2
                else:
                    beta_max = beta
                    beta = (beta + beta_min) / 2 if beta_min != -np.inf else beta / 2
                
                if abs(perp - self.perplexity) < 1e-5:
                    break
            
            P[i] = Pi
        
        # Symmetrize
        P = (P + P.T) / (2 * n)
        P = np.maximum(P, 1e-12)
        return P
    
    def fit_transform(self, X):
        n, d = X.shape
        
        # Compute pairwise affinities
        P = self._compute_pairwise_affinities(X)
        
        # Initialize low-dimensional embedding
        Y = np.random.normal(0, 1e-4, (n, self.n_components))
        
        # Gradient descent
        for iter in range(self.n_iter):
            # Compute low-dimensional affinities
            sum_Y = np.sum(Y**2, axis=1)
            num = -2 * np.dot(Y, Y.T)
            num = 1 / (1 + np.add(np.add(num, sum_Y).T, sum_Y))
            np.fill_diagonal(num, 0)
            Q = num / np.sum(num)
            Q = np.maximum(Q, 1e-12)
            
            # Compute gradient
            PQ = P - Q
            gradient = np.zeros((n, self.n_components))
            
            for i in range(n):
                gradient[i] = np.sum(
                    ((PQ[i] * num[i]).reshape(-1, 1) * (Y[i] - Y)), axis=0
                )
            
            # Update Y
            Y -= self.learning_rate * gradient
            
            # Center Y
            Y -= np.mean(Y, axis=0)
            
            if iter % 100 == 0:
                cost = np.sum(P * np.log(P / Q))
                print(f"Iteration {iter}: KL divergence = {cost}")
        
        return Y
```

**UMAP Implementation:**
```python
import numba
from sklearn.neighbors import NearestNeighbors

class UMAP:
    def __init__(self, n_neighbors=15, n_components=2, min_dist=0.1, spread=1.0):
        self.n_neighbors = n_neighbors
        self.n_components = n_components
        self.min_dist = min_dist
        self.spread = spread
    
    def _fuzzy_simplicial_set(self, X):
        """Construct fuzzy simplicial set"""
        n_samples = X.shape[0]
        
        # Find k-nearest neighbors
        nn = NearestNeighbors(n_neighbors=self.n_neighbors)
        nn.fit(X)
        distances, indices = nn.kneighbors(X)
        
        # Compute local connectivity
        sigmas = np.zeros(n_samples)
        rhos = np.zeros(n_samples)
        
        for i in range(n_samples):
            # Find sigma such that sum of probabilities equals log2(k)
            target = np.log2(self.n_neighbors)
            
            # Binary search for sigma
            lo, hi = 0, np.inf
            for _ in range(64):
                if hi == np.inf:
                    sigma = lo * 2
                else:
                    sigma = (lo + hi) / 2
                
                if sigma == 0:
                    break
                
                # Compute probabilities
                d = distances[i, 1:]  # Exclude self
                prob_sum = np.sum(np.exp(-np.maximum(d - distances[i, 1], 0) / sigma))
                
                if abs(prob_sum - target) < 1e-5:
                    break
                
                if prob_sum > target:
                    hi = sigma
                else:
                    lo = sigma
            
            sigmas[i] = sigma
            rhos[i] = distances[i, 1]  # Distance to nearest neighbor
        
        # Construct membership strengths
        rows, cols, vals = [], [], []
        
        for i in range(n_samples):
            for j in range(1, self.n_neighbors):
                neighbor = indices[i, j]
                distance = distances[i, j]
                
                # Compute membership strength
                val = np.exp(-max(distance - rhos[i], 0) / sigmas[i])
                
                rows.append(i)
                cols.append(neighbor)
                vals.append(val)
        
        # Create sparse matrix and symmetrize
        from scipy.sparse import coo_matrix
        graph = coo_matrix((vals, (rows, cols)), shape=(n_samples, n_samples))
        graph = graph + graph.T - graph.multiply(graph.T)
        
        return graph
    
    def fit_transform(self, X):
        # Construct high-dimensional graph
        graph = self._fuzzy_simplicial_set(X)
        
        # Initialize low-dimensional embedding
        n_samples = X.shape[0]
        embedding = np.random.uniform(-10, 10, (n_samples, self.n_components))
        
        # Optimize embedding using SGD
        n_epochs = 200
        alpha = 1.0
        
        for epoch in range(n_epochs):
            # Sample edges
            edges = np.array(list(zip(*graph.nonzero())))
            weights = np.array(graph.data)
            
            # Shuffle edges
            indices = np.random.permutation(len(edges))
            edges = edges[indices]
            weights = weights[indices]
            
            # Update embedding
            for edge, weight in zip(edges, weights):
                i, j = edge
                
                # Attractive force
                diff = embedding[i] - embedding[j]
                dist_sq = np.sum(diff**2)
                
                if dist_sq > 0:
                    grad_coeff = -2 * weight / (1 + dist_sq)
                    embedding[i] += alpha * grad_coeff * diff
                    embedding[j] -= alpha * grad_coeff * diff
                
                # Repulsive force (negative sampling)
                for _ in range(5):  # Number of negative samples
                    k = np.random.randint(n_samples)
                    if k != i:
                        diff = embedding[i] - embedding[k]
                        dist_sq = np.sum(diff**2)
                        
                        if dist_sq > 0:
                            grad_coeff = 2 / ((0.001 + dist_sq) * (1 + dist_sq))
                            embedding[i] += alpha * grad_coeff * diff
            
            # Decay learning rate
            alpha = 1.0 - epoch / n_epochs
        
        return embedding
```

---

## Deep Learning

### 4. Implement attention mechanisms and transformers from scratch.
**Answer:**
**Multi-Head Attention:**
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads, dropout=0.1):
        super().__init__()
        assert d_model % n_heads == 0
        
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
        
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        # Q, K, V: (batch_size, n_heads, seq_len, d_k)
        d_k = Q.size(-1)
        
        # Compute attention scores
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
        
        # Apply mask if provided
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        # Apply softmax
        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        
        # Apply attention to values
        output = torch.matmul(attention_weights, V)
        
        return output, attention_weights
    
    def forward(self, query, key, value, mask=None):
        batch_size, seq_len, d_model = query.size()
        
        # Linear transformations and reshape
        Q = self.W_q(query).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        
        # Apply attention
        attention_output, attention_weights = self.scaled_dot_product_attention(Q, K, V, mask)
        
        # Concatenate heads
        attention_output = attention_output.transpose(1, 2).contiguous().view(
            batch_size, seq_len, d_model
        )
        
        # Final linear transformation
        output = self.W_o(attention_output)
        
        return output, attention_weights

class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        super().__init__()
        
        self.attention = MultiHeadAttention(d_model, n_heads, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        
        self.feed_forward = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model)
        )
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Self-attention with residual connection
        attn_output, _ = self.attention(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_output))
        
        # Feed-forward with residual connection
        ff_output = self.feed_forward(x)
        x = self.norm2(x + self.dropout(ff_output))
        
        return x

class Transformer(nn.Module):
    def __init__(self, vocab_size, d_model, n_heads, n_layers, d_ff, max_seq_len, dropout=0.1):
        super().__init__()
        
        self.d_model = d_model
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = self._create_positional_encoding(max_seq_len, d_model)
        
        self.transformer_blocks = nn.ModuleList([
            TransformerBlock(d_model, n_heads, d_ff, dropout)
            for _ in range(n_layers)
        ])
        
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(d_model)
        self.output_projection = nn.Linear(d_model, vocab_size)
    
    def _create_positional_encoding(self, max_seq_len, d_model):
        pe = torch.zeros(max_seq_len, d_model)
        position = torch.arange(0, max_seq_len).unsqueeze(1).float()
        
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                           -(math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        return pe.unsqueeze(0)
    
    def forward(self, x, mask=None):
        seq_len = x.size(1)
        
        # Embedding + positional encoding
        x = self.embedding(x) * math.sqrt(self.d_model)
        x = x + self.pos_encoding[:, :seq_len, :].to(x.device)
        x = self.dropout(x)
        
        # Apply transformer blocks
        for transformer_block in self.transformer_blocks:
            x = transformer_block(x, mask)
        
        x = self.layer_norm(x)
        output = self.output_projection(x)
        
        return output
```

### 5. Implement advanced CNN architectures (ResNet, DenseNet).
**Answer:**
**ResNet Implementation:**
```python
import torch
import torch.nn as nn

class BasicBlock(nn.Module):
    expansion = 1
    
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super().__init__()
        
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, 
                              stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3,
                              stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.downsample = downsample
        self.stride = stride
    
    def forward(self, x):
        identity = x
        
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        out = self.conv2(out)
        out = self.bn2(out)
        
        if self.downsample is not None:
            identity = self.downsample(x)
        
        out += identity
        out = self.relu(out)
        
        return out

class Bottleneck(nn.Module):
    expansion = 4
    
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super().__init__()
        
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3,
                              stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.conv3 = nn.Conv2d(out_channels, out_channels * self.expansion,
                              kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels * self.expansion)
        
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
    
    def forward(self, x):
        identity = x
        
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)
        
        out = self.conv3(out)
        out = self.bn3(out)
        
        if self.downsample is not None:
            identity = self.downsample(x)
        
        out += identity
        out = self.relu(out)
        
        return out

class ResNet(nn.Module):
    def __init__(self, block, layers, num_classes=1000):
        super().__init__()
        
        self.in_channels = 64
        
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        
        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2)
        
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)
        
        # Initialize weights
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
    
    def _make_layer(self, block, out_channels, blocks, stride=1):
        downsample = None
        
        if stride != 1 or self.in_channels != out_channels * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.in_channels, out_channels * block.expansion,
                         kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels * block.expansion)
            )
        
        layers = []
        layers.append(block(self.in_channels, out_channels, stride, downsample))
        self.in_channels = out_channels * block.expansion
        
        for _ in range(1, blocks):
            layers.append(block(self.in_channels, out_channels))
        
        return nn.Sequential(*layers)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        
        return x

def resnet50(num_classes=1000):
    return ResNet(Bottleneck, [3, 4, 6, 3], num_classes)
```

**DenseNet Implementation:**
```python
class DenseLayer(nn.Module):
    def __init__(self, in_channels, growth_rate, bn_size, drop_rate):
        super().__init__()
        
        self.norm1 = nn.BatchNorm2d(in_channels)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv1 = nn.Conv2d(in_channels, bn_size * growth_rate,
                              kernel_size=1, stride=1, bias=False)
        
        self.norm2 = nn.BatchNorm2d(bn_size * growth_rate)
        self.relu2 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(bn_size * growth_rate, growth_rate,
                              kernel_size=3, stride=1, padding=1, bias=False)
        
        self.drop_rate = drop_rate
    
    def forward(self, x):
        new_features = self.norm1(x)
        new_features = self.relu1(new_features)
        new_features = self.conv1(new_features)
        
        new_features = self.norm2(new_features)
        new_features = self.relu2(new_features)
        new_features = self.conv2(new_features)
        
        if self.drop_rate > 0:
            new_features = F.dropout(new_features, p=self.drop_rate, training=self.training)
        
        return torch.cat([x, new_features], 1)

class DenseBlock(nn.Module):
    def __init__(self, num_layers, in_channels, bn_size, growth_rate, drop_rate):
        super().__init__()
        
        layers = []
        for i in range(num_layers):
            layer = DenseLayer(
                in_channels + i * growth_rate,
                growth_rate,
                bn_size,
                drop_rate
            )
            layers.append(layer)
        
        self.layers = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.layers(x)

class Transition(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        
        self.norm = nn.BatchNorm2d(in_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, bias=False)
        self.pool = nn.AvgPool2d(kernel_size=2, stride=2)
    
    def forward(self, x):
        x = self.norm(x)
        x = self.relu(x)
        x = self.conv(x)
        x = self.pool(x)
        return x

class DenseNet(nn.Module):
    def __init__(self, growth_rate=32, block_config=(6, 12, 24, 16),
                 num_init_features=64, bn_size=4, drop_rate=0, num_classes=1000):
        super().__init__()
        
        # First convolution
        self.features = nn.Sequential(
            nn.Conv2d(3, num_init_features, kernel_size=7, stride=2, padding=3, bias=False),
            nn.BatchNorm2d(num_init_features),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )
        
        # Dense blocks
        num_features = num_init_features
        for i, num_layers in enumerate(block_config):
            block = DenseBlock(
                num_layers=num_layers,
                in_channels=num_features,
                bn_size=bn_size,
                growth_rate=growth_rate,
                drop_rate=drop_rate
            )
            self.features.add_module(f'denseblock{i+1}', block)
            num_features = num_features + num_layers * growth_rate
            
            if i != len(block_config) - 1:
                trans = Transition(in_channels=num_features,
                                 out_channels=num_features // 2)
                self.features.add_module(f'transition{i+1}', trans)
                num_features = num_features // 2
        
        # Final batch norm
        self.features.add_module('norm5', nn.BatchNorm2d(num_features))
        
        # Linear layer
        self.classifier = nn.Linear(num_features, num_classes)
        
        # Initialize weights
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        features = self.features(x)
        out = F.relu(features, inplace=True)
        out = F.adaptive_avg_pool2d(out, (1, 1))
        out = torch.flatten(out, 1)
        out = self.classifier(out)
        return out
```

---

## Model Optimization

### 6. Implement advanced optimization algorithms (Adam, RMSprop, AdaGrad).
**Answer:**
**Custom Optimizer Implementations:**
```python
import torch
import math

class SGD:
    def __init__(self, params, lr=0.01, momentum=0, weight_decay=0):
        self.params = list(params)
        self.lr = lr
        self.momentum = momentum
        self.weight_decay = weight_decay
        self.velocity = [torch.zeros_like(p) for p in self.params]
    
    def step(self):
        for i, param in enumerate(self.params):
            if param.grad is None:
                continue
            
            grad = param.grad.data
            
            # Add weight decay
            if self.weight_decay != 0:
                grad = grad.add(param.data, alpha=self.weight_decay)
            
            # Apply momentum
            if self.momentum != 0:
                self.velocity[i] = self.momentum * self.velocity[i] + grad
                grad = self.velocity[i]
            
            # Update parameters
            param.data.add_(grad, alpha=-self.lr)
    
    def zero_grad(self):
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()

class AdaGrad:
    def __init__(self, params, lr=0.01, eps=1e-10, weight_decay=0):
        self.params = list(params)
        self.lr = lr
        self.eps = eps
        self.weight_decay = weight_decay
        self.sum_squared_grads = [torch.zeros_like(p) for p in self.params]
    
    def step(self):
        for i, param in enumerate(self.params):
            if param.grad is None:
                continue
            
            grad = param.grad.data
            
            # Add weight decay
            if self.weight_decay != 0:
                grad = grad.add(param.data, alpha=self.weight_decay)
            
            # Accumulate squared gradients
            self.sum_squared_grads[i].add_(grad.pow(2))
            
            # Compute adaptive learning rate
            std = self.sum_squared_grads[i].sqrt().add_(self.eps)
            
            # Update parameters
            param.data.addcdiv_(grad, std, value=-self.lr)
    
    def zero_grad(self):
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()

class RMSprop:
    def __init__(self, params, lr=0.01, alpha=0.99, eps=1e-8, weight_decay=0, momentum=0):
        self.params = list(params)
        self.lr = lr
        self.alpha = alpha
        self.eps = eps
        self.weight_decay = weight_decay
        self.momentum = momentum
        
        self.square_avg = [torch.zeros_like(p) for p in self.params]
        if momentum > 0:
            self.momentum_buffer = [torch.zeros_like(p) for p in self.params]
    
    def step(self):
        for i, param in enumerate(self.params):
            if param.grad is None:
                continue
            
            grad = param.grad.data
            
            # Add weight decay
            if self.weight_decay != 0:
                grad = grad.add(param.data, alpha=self.weight_decay)
            
            # Update biased second moment estimate
            self.square_avg[i].mul_(self.alpha).addcmul_(grad, grad, value=1 - self.alpha)
            
            # Compute update
            avg = self.square_avg[i].sqrt().add_(self.eps)
            
            if self.momentum > 0:
                self.momentum_buffer[i].mul_(self.momentum).addcdiv_(grad, avg)
                param.data.add_(self.momentum_buffer[i], alpha=-self.lr)
            else:
                param.data.addcdiv_(grad, avg, value=-self.lr)
    
    def zero_grad(self):
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()

class Adam:
    def __init__(self, params, lr=0.001, betas=(0.9, 0.999), eps=1e-8, weight_decay=0):
        self.params = list(params)
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        
        self.step_count = 0
        self.exp_avg = [torch.zeros_like(p) for p in self.params]
        self.exp_avg_sq = [torch.zeros_like(p) for p in self.params]
    
    def step(self):
        self.step_count += 1
        
        for i, param in enumerate(self.params):
            if param.grad is None:
                continue
            
            grad = param.grad.data
            
            # Add weight decay
            if self.weight_decay != 0:
                grad = grad.add(param.data, alpha=self.weight_decay)
            
            # Update biased first moment estimate
            self.exp_avg[i].mul_(self.beta1).add_(grad, alpha=1 - self.beta1)
            
            # Update biased second raw moment estimate
            self.exp_avg_sq[i].mul_(self.beta2).addcmul_(grad, grad, value=1 - self.beta2)
            
            # Compute bias correction
            bias_correction1 = 1 - self.beta1 ** self.step_count
            bias_correction2 = 1 - self.beta2 ** self.step_count
            
            # Compute bias-corrected estimates
            corrected_exp_avg = self.exp_avg[i] / bias_correction1
            corrected_exp_avg_sq = self.exp_avg_sq[i] / bias_correction2
            
            # Update parameters
            denom = corrected_exp_avg_sq.sqrt().add_(self.eps)
            step_size = self.lr / bias_correction1
            
            param.data.addcdiv_(corrected_exp_avg, denom, value=-step_size)
    
    def zero_grad(self):
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()

class AdamW:
    """Adam with decoupled weight decay"""
    def __init__(self, params, lr=0.001, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.01):
        self.params = list(params)
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        
        self.step_count = 0
        self.exp_avg = [torch.zeros_like(p) for p in self.params]
        self.exp_avg_sq = [torch.zeros_like(p) for p in self.params]
    
    def step(self):
        self.step_count += 1
        
        for i, param in enumerate(self.params):
            if param.grad is None:
                continue
            
            grad = param.grad.data
            
            # Decoupled weight decay
            param.data.mul_(1 - self.lr * self.weight_decay)
            
            # Update biased first moment estimate
            self.exp_avg[i].mul_(self.beta1).add_(grad, alpha=1 - self.beta1)
            
            # Update biased second raw moment estimate
            self.exp_avg_sq[i].mul_(self.beta2).addcmul_(grad, grad, value=1 - self.beta2)
            
            # Compute bias correction
            bias_correction1 = 1 - self.beta1 ** self.step_count
            bias_correction2 = 1 - self.beta2 ** self.step_count
            
            # Update parameters
            denom = (self.exp_avg_sq[i].sqrt() / math.sqrt(bias_correction2)).add_(self.eps)
            step_size = self.lr / bias_correction1
            
            param.data.addcdiv_(self.exp_avg[i], denom, value=-step_size)
```

---

*This comprehensive guide covers 6+ advanced machine learning interview questions with detailed mathematical foundations and practical implementations for senior ML engineer interviews.*
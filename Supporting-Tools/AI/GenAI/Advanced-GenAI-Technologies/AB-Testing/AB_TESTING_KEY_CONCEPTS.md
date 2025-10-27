# 🧪 A/B Testing for AI Systems - Key Concepts

## 🎯 **Real-World Analogy: The Scientific Laboratory**

> **Think of A/B testing for AI as running controlled experiments in a laboratory. You test two different approaches (like two different medicines) on similar groups to see which one works better, but instead of testing medicines, you're testing AI models, prompts, or user interfaces.**

## 🔥 **Core Concepts**

### 1. **Experiment Design Framework** 🔬

```python
import random
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

class AIExperimentDesigner:
    def __init__(self):
        self.experiments = {}
        self.user_assignments = {}
    
    def create_experiment(self, experiment_id, variants, success_metric, sample_size_per_variant=1000):
        """Create A/B test experiment for AI system"""
        experiment = {
            'id': experiment_id,
            'variants': variants,
            'success_metric': success_metric,
            'sample_size_per_variant': sample_size_per_variant,
            'start_date': datetime.now(),
            'status': 'active',
            'results': {variant['name']: [] for variant in variants}
        }
        
        self.experiments[experiment_id] = experiment
        return experiment
    
    def assign_user_to_variant(self, experiment_id, user_id):
        """Randomly assign user to experiment variant"""
        if experiment_id not in self.experiments:
            return None
        
        experiment = self.experiments[experiment_id]
        
        # Check if user already assigned
        if user_id in self.user_assignments.get(experiment_id, {}):
            return self.user_assignments[experiment_id][user_id]
        
        # Random assignment
        variant = random.choice(experiment['variants'])
        
        # Store assignment
        if experiment_id not in self.user_assignments:
            self.user_assignments[experiment_id] = {}
        
        self.user_assignments[experiment_id][user_id] = variant['name']
        
        return variant['name']
    
    def record_result(self, experiment_id, user_id, metric_value):
        """Record experiment result for user"""
        if experiment_id not in self.experiments:
            return False
        
        variant = self.user_assignments.get(experiment_id, {}).get(user_id)
        if not variant:
            return False
        
        self.experiments[experiment_id]['results'][variant].append({
            'user_id': user_id,
            'value': metric_value,
            'timestamp': datetime.now()
        })
        
        return True
    
    def analyze_results(self, experiment_id, confidence_level=0.95):
        """Analyze A/B test results with statistical significance"""
        if experiment_id not in self.experiments:
            return None
        
        experiment = self.experiments[experiment_id]
        results = experiment['results']
        
        # Calculate statistics for each variant
        variant_stats = {}
        for variant_name, data in results.items():
            if data:
                values = [d['value'] for d in data]
                variant_stats[variant_name] = {
                    'count': len(values),
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'conversion_rate': sum(1 for v in values if v > 0) / len(values)
                }
        
        # Statistical significance test (t-test for two variants)
        variant_names = list(variant_stats.keys())
        if len(variant_names) == 2:
            variant_a_data = [d['value'] for d in results[variant_names[0]]]
            variant_b_data = [d['value'] for d in results[variant_names[1]]]
            
            if len(variant_a_data) > 0 and len(variant_b_data) > 0:
                t_stat, p_value = stats.ttest_ind(variant_a_data, variant_b_data)
                
                is_significant = p_value < (1 - confidence_level)
                
                return {
                    'variant_stats': variant_stats,
                    'statistical_test': {
                        't_statistic': t_stat,
                        'p_value': p_value,
                        'is_significant': is_significant,
                        'confidence_level': confidence_level
                    },
                    'recommendation': self.generate_recommendation(variant_stats, is_significant)
                }
        
        return {'variant_stats': variant_stats}
    
    def generate_recommendation(self, variant_stats, is_significant):
        """Generate recommendation based on results"""
        if not is_significant:
            return "No statistically significant difference found. Continue testing or implement based on other factors."
        
        # Find best performing variant
        best_variant = max(variant_stats.items(), key=lambda x: x[1]['mean'])
        
        return f"Implement {best_variant[0]} - shows {best_variant[1]['mean']:.2f} average performance vs others."

# Usage
experiment_designer = AIExperimentDesigner()

# Create experiment: Testing two different AI prompts
variants = [
    {'name': 'prompt_a', 'description': 'Direct, concise prompts'},
    {'name': 'prompt_b', 'description': 'Detailed, context-rich prompts'}
]

experiment = experiment_designer.create_experiment(
    'prompt_optimization_001',
    variants,
    'user_satisfaction_score',
    sample_size_per_variant=500
)

# Simulate user interactions
for user_id in range(100):
    variant = experiment_designer.assign_user_to_variant('prompt_optimization_001', f'user_{user_id}')
    
    # Simulate different performance for each variant
    if variant == 'prompt_a':
        satisfaction = np.random.normal(3.2, 0.8)  # Lower satisfaction
    else:
        satisfaction = np.random.normal(3.8, 0.7)  # Higher satisfaction
    
    experiment_designer.record_result('prompt_optimization_001', f'user_{user_id}', satisfaction)

# Analyze results
results = experiment_designer.analyze_results('prompt_optimization_001')
print(f"Experiment results: {results['recommendation']}")
```

### 2. **Model Performance Testing** 🤖

```python
class ModelABTester:
    def __init__(self):
        self.model_experiments = {}
        self.performance_metrics = ['accuracy', 'latency', 'cost', 'user_satisfaction']
    
    def setup_model_comparison(self, experiment_id, model_a, model_b, traffic_split=0.5):
        """Setup A/B test between two AI models"""
        experiment = {
            'id': experiment_id,
            'model_a': model_a,
            'model_b': model_b,
            'traffic_split': traffic_split,
            'results': {'model_a': [], 'model_b': []},
            'start_time': datetime.now()
        }
        
        self.model_experiments[experiment_id] = experiment
        return experiment
    
    def route_request(self, experiment_id, request_data):
        """Route request to appropriate model based on traffic split"""
        experiment = self.model_experiments[experiment_id]
        
        # Random routing based on traffic split
        if random.random() < experiment['traffic_split']:
            selected_model = 'model_a'
            model = experiment['model_a']
        else:
            selected_model = 'model_b'
            model = experiment['model_b']
        
        return selected_model, model
    
    def record_model_performance(self, experiment_id, model_name, metrics):
        """Record performance metrics for model"""
        if experiment_id in self.model_experiments:
            self.model_experiments[experiment_id]['results'][model_name].append({
                'timestamp': datetime.now(),
                'metrics': metrics
            })
    
    def analyze_model_performance(self, experiment_id):
        """Analyze comparative model performance"""
        experiment = self.model_experiments[experiment_id]
        results = experiment['results']
        
        analysis = {}
        
        for model_name, data in results.items():
            if data:
                # Calculate average metrics
                avg_metrics = {}
                for metric in self.performance_metrics:
                    values = [d['metrics'].get(metric, 0) for d in data if metric in d['metrics']]
                    if values:
                        avg_metrics[metric] = {
                            'mean': np.mean(values),
                            'std': np.std(values),
                            'count': len(values)
                        }
                
                analysis[model_name] = avg_metrics
        
        # Compare models
        comparison = self.compare_models(analysis)
        
        return {
            'model_performance': analysis,
            'comparison': comparison,
            'recommendation': self.recommend_model(comparison)
        }
    
    def compare_models(self, analysis):
        """Compare performance between models"""
        if len(analysis) != 2:
            return {}
        
        model_names = list(analysis.keys())
        model_a_stats = analysis[model_names[0]]
        model_b_stats = analysis[model_names[1]]
        
        comparison = {}
        
        for metric in self.performance_metrics:
            if metric in model_a_stats and metric in model_b_stats:
                a_mean = model_a_stats[metric]['mean']
                b_mean = model_b_stats[metric]['mean']
                
                improvement = ((b_mean - a_mean) / a_mean) * 100 if a_mean != 0 else 0
                
                comparison[metric] = {
                    f'{model_names[0]}_mean': a_mean,
                    f'{model_names[1]}_mean': b_mean,
                    'improvement_percent': improvement,
                    'winner': model_names[1] if b_mean > a_mean else model_names[0]
                }
        
        return comparison
    
    def recommend_model(self, comparison):
        """Recommend which model to use based on comparison"""
        if not comparison:
            return "Insufficient data for recommendation"
        
        # Weight different metrics (customize based on business priorities)
        metric_weights = {
            'accuracy': 0.4,
            'user_satisfaction': 0.3,
            'latency': 0.2,
            'cost': 0.1
        }
        
        model_scores = {}
        
        for metric, data in comparison.items():
            if metric in metric_weights:
                winner = data['winner']
                improvement = abs(data['improvement_percent'])
                
                if winner not in model_scores:
                    model_scores[winner] = 0
                
                model_scores[winner] += metric_weights[metric] * improvement
        
        if model_scores:
            best_model = max(model_scores, key=model_scores.get)
            return f"Recommend {best_model} with weighted score: {model_scores[best_model]:.2f}"
        
        return "No clear winner - consider business priorities"

# Usage
model_tester = ModelABTester()

# Setup model comparison
experiment = model_tester.setup_model_comparison(
    'gpt4_vs_claude',
    model_a={'name': 'gpt-4', 'version': '1.0'},
    model_b={'name': 'claude-3', 'version': '1.0'},
    traffic_split=0.5
)

# Simulate requests and performance recording
for i in range(200):
    selected_model, model = model_tester.route_request('gpt4_vs_claude', {'query': f'test_query_{i}'})
    
    # Simulate different performance characteristics
    if selected_model == 'model_a':  # GPT-4
        metrics = {
            'accuracy': np.random.normal(0.85, 0.05),
            'latency': np.random.normal(2.5, 0.5),
            'cost': np.random.normal(0.06, 0.01),
            'user_satisfaction': np.random.normal(4.2, 0.3)
        }
    else:  # Claude-3
        metrics = {
            'accuracy': np.random.normal(0.82, 0.06),
            'latency': np.random.normal(1.8, 0.4),
            'cost': np.random.normal(0.04, 0.008),
            'user_satisfaction': np.random.normal(4.0, 0.4)
        }
    
    model_tester.record_model_performance('gpt4_vs_claude', selected_model, metrics)

# Analyze results
performance_analysis = model_tester.analyze_model_performance('gpt4_vs_claude')
print(f"Model recommendation: {performance_analysis['recommendation']}")
```

### 3. **Prompt Optimization Testing** ✍️

```python
class PromptABTester:
    def __init__(self):
        self.prompt_experiments = {}
        self.response_quality_metrics = ['relevance', 'clarity', 'completeness', 'helpfulness']
    
    def create_prompt_experiment(self, experiment_id, prompt_variants, evaluation_criteria):
        """Create A/B test for different prompt variations"""
        experiment = {
            'id': experiment_id,
            'prompt_variants': prompt_variants,
            'evaluation_criteria': evaluation_criteria,
            'results': {variant['name']: [] for variant in prompt_variants},
            'created_at': datetime.now()
        }
        
        self.prompt_experiments[experiment_id] = experiment
        return experiment
    
    def test_prompt_variant(self, experiment_id, user_query, variant_name=None):
        """Test specific prompt variant or randomly select one"""
        experiment = self.prompt_experiments[experiment_id]
        
        if variant_name is None:
            variant = random.choice(experiment['prompt_variants'])
            variant_name = variant['name']
        else:
            variant = next(v for v in experiment['prompt_variants'] if v['name'] == variant_name)
        
        # Apply prompt template to user query
        formatted_prompt = variant['template'].format(user_query=user_query)
        
        return {
            'variant_name': variant_name,
            'formatted_prompt': formatted_prompt,
            'prompt_config': variant
        }
    
    def evaluate_response_quality(self, response_text, evaluation_criteria):
        """Evaluate quality of AI response (simplified simulation)"""
        quality_scores = {}
        
        # Simulate quality evaluation (in practice, use human evaluators or AI judges)
        for criterion in evaluation_criteria:
            if criterion == 'relevance':
                # Simulate relevance scoring based on response length and keywords
                score = min(5.0, len(response_text.split()) / 20 + np.random.normal(3.5, 0.5))
            elif criterion == 'clarity':
                # Simulate clarity scoring
                score = np.random.normal(3.8, 0.6)
            elif criterion == 'completeness':
                # Simulate completeness scoring
                score = min(5.0, len(response_text) / 100 + np.random.normal(3.2, 0.7))
            elif criterion == 'helpfulness':
                # Simulate helpfulness scoring
                score = np.random.normal(3.6, 0.8)
            else:
                score = np.random.normal(3.5, 0.5)
            
            quality_scores[criterion] = max(1.0, min(5.0, score))  # Clamp to 1-5 scale
        
        return quality_scores
    
    def record_prompt_result(self, experiment_id, variant_name, user_query, response, quality_scores):
        """Record result of prompt test"""
        experiment = self.prompt_experiments[experiment_id]
        
        result = {
            'timestamp': datetime.now(),
            'user_query': user_query,
            'response': response,
            'quality_scores': quality_scores,
            'overall_score': np.mean(list(quality_scores.values()))
        }
        
        experiment['results'][variant_name].append(result)
    
    def analyze_prompt_performance(self, experiment_id):
        """Analyze performance of different prompt variants"""
        experiment = self.prompt_experiments[experiment_id]
        results = experiment['results']
        
        analysis = {}
        
        for variant_name, data in results.items():
            if data:
                # Calculate statistics for each quality metric
                variant_analysis = {
                    'sample_size': len(data),
                    'overall_performance': {}
                }
                
                # Overall score statistics
                overall_scores = [d['overall_score'] for d in data]
                variant_analysis['overall_performance'] = {
                    'mean': np.mean(overall_scores),
                    'std': np.std(overall_scores),
                    'median': np.median(overall_scores)
                }
                
                # Individual metric statistics
                for metric in self.response_quality_metrics:
                    metric_scores = [d['quality_scores'].get(metric, 0) for d in data if metric in d['quality_scores']]
                    if metric_scores:
                        variant_analysis[metric] = {
                            'mean': np.mean(metric_scores),
                            'std': np.std(metric_scores)
                        }
                
                analysis[variant_name] = variant_analysis
        
        # Find best performing variant
        best_variant = self.find_best_prompt_variant(analysis)
        
        return {
            'variant_analysis': analysis,
            'best_variant': best_variant,
            'recommendation': self.generate_prompt_recommendation(analysis, best_variant)
        }
    
    def find_best_prompt_variant(self, analysis):
        """Find the best performing prompt variant"""
        if not analysis:
            return None
        
        best_variant = None
        best_score = 0
        
        for variant_name, data in analysis.items():
            if 'overall_performance' in data:
                score = data['overall_performance']['mean']
                if score > best_score:
                    best_score = score
                    best_variant = variant_name
        
        return best_variant
    
    def generate_prompt_recommendation(self, analysis, best_variant):
        """Generate recommendation for prompt optimization"""
        if not best_variant:
            return "Insufficient data for recommendation"
        
        best_data = analysis[best_variant]
        best_score = best_data['overall_performance']['mean']
        
        # Compare with other variants
        improvements = []
        for variant_name, data in analysis.items():
            if variant_name != best_variant and 'overall_performance' in data:
                other_score = data['overall_performance']['mean']
                improvement = ((best_score - other_score) / other_score) * 100
                improvements.append(improvement)
        
        avg_improvement = np.mean(improvements) if improvements else 0
        
        return f"Use {best_variant} - shows {avg_improvement:.1f}% average improvement over other variants (score: {best_score:.2f}/5.0)"

# Usage
prompt_tester = PromptABTester()

# Define prompt variants to test
prompt_variants = [
    {
        'name': 'concise_prompt',
        'template': 'Answer this question briefly: {user_query}'
    },
    {
        'name': 'detailed_prompt', 
        'template': 'Provide a comprehensive answer to: {user_query}. Include examples and explanations.'
    },
    {
        'name': 'structured_prompt',
        'template': 'Answer: {user_query}\n\nFormat your response as:\n1. Main answer\n2. Key points\n3. Examples'
    }
]

# Create experiment
experiment = prompt_tester.create_prompt_experiment(
    'prompt_optimization_test',
    prompt_variants,
    ['relevance', 'clarity', 'completeness', 'helpfulness']
)

# Simulate testing
test_queries = [
    "How do I optimize database performance?",
    "What are the best practices for data security?",
    "Explain machine learning model deployment"
]

for query in test_queries:
    for _ in range(10):  # Test each query 10 times per variant
        for variant in prompt_variants:
            # Test prompt variant
            test_result = prompt_tester.test_prompt_variant('prompt_optimization_test', query, variant['name'])
            
            # Simulate AI response (in practice, call actual AI model)
            simulated_response = f"Response to '{query}' using {variant['name']} prompt..."
            
            # Evaluate response quality
            quality_scores = prompt_tester.evaluate_response_quality(
                simulated_response, 
                ['relevance', 'clarity', 'completeness', 'helpfulness']
            )
            
            # Record result
            prompt_tester.record_prompt_result(
                'prompt_optimization_test',
                variant['name'],
                query,
                simulated_response,
                quality_scores
            )

# Analyze results
prompt_analysis = prompt_tester.analyze_prompt_performance('prompt_optimization_test')
print(f"Prompt recommendation: {prompt_analysis['recommendation']}")
```
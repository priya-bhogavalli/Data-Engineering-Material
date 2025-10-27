# 👥 User Research & Human-AI Interaction - Key Concepts

## 🎯 **Real-World Analogy: The UX Detective**

> **Think of user research for AI as being a detective who studies how people interact with technology. You observe, ask questions, and uncover insights about what makes AI systems truly helpful versus frustrating.**

## 🔥 **Core Concepts**

### 1. **User Journey Mapping** 🗺️

```python
class AIUserJourneyMapper:
    def __init__(self):
        self.journey_stages = [
            'discovery', 'first_use', 'learning', 'adoption', 'mastery'
        ]
        self.touchpoints = {}
        self.pain_points = {}
    
    def map_user_journey(self, user_interactions):
        """Map user journey with AI system"""
        journey_map = {}
        
        for stage in self.journey_stages:
            journey_map[stage] = {
                'actions': [],
                'emotions': [],
                'pain_points': [],
                'opportunities': []
            }
        
        # Analyze interactions by stage
        for interaction in user_interactions:
            stage = self.classify_interaction_stage(interaction)
            
            journey_map[stage]['actions'].append(interaction['action'])
            journey_map[stage]['emotions'].append(interaction['sentiment'])
            
            if interaction['success'] == False:
                journey_map[stage]['pain_points'].append(interaction['issue'])
        
        return journey_map
    
    def classify_interaction_stage(self, interaction):
        """Classify interaction into journey stage"""
        session_count = interaction.get('session_count', 1)
        
        if session_count == 1:
            return 'first_use'
        elif session_count <= 5:
            return 'learning'
        elif session_count <= 20:
            return 'adoption'
        else:
            return 'mastery'

# Usage
journey_mapper = AIUserJourneyMapper()

user_interactions = [
    {'action': 'ask_question', 'session_count': 1, 'success': True, 'sentiment': 'curious'},
    {'action': 'complex_query', 'session_count': 3, 'success': False, 'sentiment': 'frustrated', 'issue': 'unclear_response'},
    # ... more interactions
]

journey = journey_mapper.map_user_journey(user_interactions)
```

### 2. **Usability Testing Framework** 🧪

```python
class AIUsabilityTester:
    def __init__(self):
        self.test_scenarios = []
        self.metrics = {
            'task_completion_rate': [],
            'time_to_completion': [],
            'error_rate': [],
            'satisfaction_score': []
        }
    
    def create_test_scenario(self, task_description, success_criteria):
        """Create usability test scenario"""
        scenario = {
            'id': len(self.test_scenarios) + 1,
            'task': task_description,
            'success_criteria': success_criteria,
            'results': []
        }
        
        self.test_scenarios.append(scenario)
        return scenario
    
    def conduct_test_session(self, user_id, scenario_id, interactions):
        """Conduct usability test session"""
        scenario = self.test_scenarios[scenario_id - 1]
        
        # Analyze user interactions
        start_time = interactions[0]['timestamp']
        end_time = interactions[-1]['timestamp']
        completion_time = (end_time - start_time).total_seconds()
        
        # Check success criteria
        task_completed = self.evaluate_task_completion(interactions, scenario['success_criteria'])
        
        # Count errors
        errors = [i for i in interactions if i.get('error', False)]
        error_rate = len(errors) / len(interactions)
        
        # Record results
        result = {
            'user_id': user_id,
            'completed': task_completed,
            'completion_time': completion_time,
            'error_rate': error_rate,
            'interactions_count': len(interactions)
        }
        
        scenario['results'].append(result)
        return result
    
    def evaluate_task_completion(self, interactions, success_criteria):
        """Evaluate if user completed task successfully"""
        # Simple evaluation - check if final interaction achieved goal
        final_interaction = interactions[-1]
        return final_interaction.get('achieved_goal', False)
    
    def generate_usability_report(self):
        """Generate comprehensive usability report"""
        report = {
            'overall_metrics': {},
            'scenario_analysis': [],
            'recommendations': []
        }
        
        # Calculate overall metrics
        all_results = []
        for scenario in self.test_scenarios:
            all_results.extend(scenario['results'])
        
        if all_results:
            report['overall_metrics'] = {
                'avg_completion_rate': sum(r['completed'] for r in all_results) / len(all_results),
                'avg_completion_time': sum(r['completion_time'] for r in all_results) / len(all_results),
                'avg_error_rate': sum(r['error_rate'] for r in all_results) / len(all_results)
            }
        
        return report

# Usage
usability_tester = AIUsabilityTester()

# Create test scenarios
scenario1 = usability_tester.create_test_scenario(
    "Ask the AI to analyze sales data and provide insights",
    {"achieved_goal": True, "insights_provided": True}
)

# Simulate test session
test_interactions = [
    {'timestamp': datetime.now(), 'action': 'upload_data', 'error': False},
    {'timestamp': datetime.now(), 'action': 'ask_analysis', 'error': False, 'achieved_goal': True}
]

result = usability_tester.conduct_test_session('user_001', 1, test_interactions)
```

### 3. **AI Trust & Explainability** 🤝

```python
class AITrustMeasurement:
    def __init__(self):
        self.trust_factors = [
            'accuracy', 'transparency', 'reliability', 
            'fairness', 'privacy', 'control'
        ]
        self.trust_scores = {}
    
    def measure_trust(self, user_feedback):
        """Measure user trust in AI system"""
        trust_metrics = {}
        
        for factor in self.trust_factors:
            if factor in user_feedback:
                trust_metrics[factor] = user_feedback[factor]
            else:
                trust_metrics[factor] = 0
        
        # Calculate overall trust score
        overall_trust = sum(trust_metrics.values()) / len(trust_metrics)
        
        return {
            'overall_trust': overall_trust,
            'factor_scores': trust_metrics,
            'trust_level': self.categorize_trust_level(overall_trust)
        }
    
    def categorize_trust_level(self, score):
        """Categorize trust level"""
        if score >= 4.0:
            return 'high'
        elif score >= 3.0:
            return 'medium'
        else:
            return 'low'
    
    def generate_explanation_quality_score(self, explanation, user_understanding):
        """Score quality of AI explanations"""
        quality_factors = {
            'clarity': user_understanding.get('clarity', 0),
            'completeness': user_understanding.get('completeness', 0),
            'relevance': user_understanding.get('relevance', 0),
            'actionability': user_understanding.get('actionability', 0)
        }
        
        return {
            'explanation_quality': sum(quality_factors.values()) / len(quality_factors),
            'factors': quality_factors
        }

# Usage
trust_measurement = AITrustMeasurement()

user_feedback = {
    'accuracy': 4.2,
    'transparency': 3.8,
    'reliability': 4.0,
    'fairness': 3.5,
    'privacy': 4.5,
    'control': 3.2
}

trust_result = trust_measurement.measure_trust(user_feedback)
print(f"Trust level: {trust_result['trust_level']} ({trust_result['overall_trust']:.1f}/5.0)")
```

### 4. **Conversation Analysis** 💬

```python
class ConversationAnalyzer:
    def __init__(self):
        self.conversation_patterns = {}
        self.satisfaction_indicators = [
            'task_completed', 'quick_resolution', 'positive_sentiment'
        ]
    
    def analyze_conversation(self, conversation_log):
        """Analyze AI-human conversation"""
        analysis = {
            'conversation_length': len(conversation_log),
            'user_satisfaction': 0,
            'ai_performance': {},
            'improvement_areas': []
        }
        
        # Analyze conversation flow
        user_messages = [msg for msg in conversation_log if msg['sender'] == 'user']
        ai_messages = [msg for msg in conversation_log if msg['sender'] == 'ai']
        
        # Calculate response times
        response_times = []
        for i in range(len(ai_messages)):
            if i < len(user_messages):
                response_time = (ai_messages[i]['timestamp'] - user_messages[i]['timestamp']).total_seconds()
                response_times.append(response_time)
        
        analysis['ai_performance']['avg_response_time'] = np.mean(response_times) if response_times else 0
        
        # Analyze sentiment progression
        sentiments = [msg.get('sentiment', 0) for msg in user_messages]
        if sentiments:
            analysis['sentiment_trend'] = 'improving' if sentiments[-1] > sentiments[0] else 'declining'
        
        # Identify conversation patterns
        analysis['patterns'] = self.identify_conversation_patterns(conversation_log)
        
        return analysis
    
    def identify_conversation_patterns(self, conversation_log):
        """Identify common conversation patterns"""
        patterns = {
            'clarification_requests': 0,
            'repetitive_questions': 0,
            'escalation_attempts': 0
        }
        
        user_messages = [msg['content'].lower() for msg in conversation_log if msg['sender'] == 'user']
        
        for message in user_messages:
            if any(phrase in message for phrase in ['what do you mean', 'can you clarify', 'i don\'t understand']):
                patterns['clarification_requests'] += 1
            
            if any(phrase in message for phrase in ['let me speak to', 'human agent', 'escalate']):
                patterns['escalation_attempts'] += 1
        
        # Check for repetitive questions
        unique_messages = set(user_messages)
        if len(unique_messages) < len(user_messages) * 0.8:
            patterns['repetitive_questions'] = len(user_messages) - len(unique_messages)
        
        return patterns

# Usage
conversation_analyzer = ConversationAnalyzer()

conversation_log = [
    {'sender': 'user', 'content': 'How do I analyze my sales data?', 'timestamp': datetime.now(), 'sentiment': 0.1},
    {'sender': 'ai', 'content': 'I can help you analyze sales data...', 'timestamp': datetime.now()},
    # ... more messages
]

analysis = conversation_analyzer.analyze_conversation(conversation_log)
```
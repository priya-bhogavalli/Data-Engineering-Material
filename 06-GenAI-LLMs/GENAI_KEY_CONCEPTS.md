# Generative AI Key Concepts

## 1. Artificial Intelligence that Creates
**What it is**: AI systems that can generate new content including text, images, code, audio, and video from prompts or training data.

**Core Capabilities**:
- **Text Generation**: Articles, code, documentation
- **Image Creation**: Art, designs, photographs
- **Code Generation**: Programming in multiple languages
- **Audio Synthesis**: Music, speech, sound effects
- **Video Production**: Animations, realistic footage

## 2. Foundation Models
**Large Language Models (LLMs)**:
```yaml
# Major Models
GPT-4: OpenAI's most advanced language model
Claude: Anthropic's constitutional AI model
PaLM: Google's Pathways Language Model
LLaMA: Meta's large language model

# Model Characteristics
Parameters: Billions to trillions of weights
Training Data: Massive text corpora from internet
Context Window: 4K to 100K+ tokens
Capabilities: Text, code, reasoning, analysis
```

**Multimodal Models**:
```yaml
# Vision-Language Models
GPT-4V: Text and image understanding
DALL-E 3: Text-to-image generation
Midjourney: Artistic image creation
Stable Diffusion: Open-source image generation

# Audio Models
Whisper: Speech-to-text transcription
MusicLM: Text-to-music generation
Bark: Text-to-speech synthesis
```

## 3. Training Methodologies
**Pre-training**:
```yaml
# Unsupervised Learning
Objective: Predict next token in sequence
Data: Massive text datasets (web, books, articles)
Compute: Thousands of GPUs for months
Result: General language understanding

# Self-Supervised Learning
- No human labels required
- Learn patterns from data structure
- Emergent capabilities at scale
```

**Fine-tuning**:
```yaml
# Supervised Fine-tuning (SFT)
Data: Human-labeled examples
Purpose: Adapt to specific tasks
Examples: Question-answering, summarization

# Reinforcement Learning from Human Feedback (RLHF)
Process: Human preferences → Reward model → Policy optimization
Purpose: Align model behavior with human values
Result: More helpful, harmless, honest responses
```

## 4. Prompt Engineering
**Prompt Structure**:
```python
# Basic prompt
prompt = "Explain data warehousing concepts"

# Structured prompt
prompt = """
Role: You are an expert data engineer
Task: Explain data warehousing concepts
Context: For a technical interview preparation
Format: Provide key concepts with examples
Tone: Professional and educational
"""

# Few-shot prompting
prompt = """
Convert business requirements to SQL queries:

Example 1:
Requirement: Find customers who made purchases last month
SQL: SELECT DISTINCT customer_id FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)

Example 2:
Requirement: Calculate total revenue by product category
SQL: SELECT category, SUM(price * quantity) as revenue FROM products p JOIN order_items oi ON p.id = oi.product_id GROUP BY category

Now convert:
Requirement: Find top 5 customers by total spending
SQL:
"""
```

**Advanced Techniques**:
```python
# Chain of Thought
prompt = """
Problem: A data pipeline processes 1TB of data daily. If processing speed is 100GB/hour, 
and we need to complete within 8 hours, how many parallel processes do we need?

Let me think step by step:
1. Total data to process: 1TB = 1000GB
2. Available time: 8 hours
3. Single process capacity: 100GB/hour × 8 hours = 800GB
4. Required parallel processes: 1000GB ÷ 800GB = 1.25, so we need 2 processes

Answer: 2 parallel processes
"""

# Tree of Thoughts
prompt = """
Design a real-time analytics system. Consider multiple approaches:

Approach 1: Stream processing with Kafka + Spark
Pros: High throughput, fault tolerance
Cons: Complex setup, higher latency

Approach 2: In-memory database with Redis
Pros: Ultra-low latency, simple queries
Cons: Limited storage, data persistence issues

Approach 3: Hybrid approach with both
Pros: Best of both worlds
Cons: Increased complexity

Evaluate each approach for a financial trading system...
"""
```

## 5. Model Architectures
**Transformer Architecture**:
```yaml
# Key Components
Attention Mechanism: Focus on relevant parts of input
Multi-Head Attention: Parallel attention computations
Feed-Forward Networks: Process attention outputs
Layer Normalization: Stabilize training
Positional Encoding: Understand sequence order

# Variants
Encoder-Only: BERT (bidirectional understanding)
Decoder-Only: GPT (autoregressive generation)
Encoder-Decoder: T5 (text-to-text transfer)
```

**Attention Mechanisms**:
```python
# Simplified attention concept
def attention(query, key, value):
    """
    query: What we're looking for
    key: What we're comparing against  
    value: What we want to retrieve
    """
    scores = query @ key.T  # Compute similarity
    weights = softmax(scores)  # Normalize to probabilities
    output = weights @ value  # Weighted combination
    return output

# Multi-head attention allows parallel processing
# of different types of relationships
```

## 6. Capabilities and Limitations
**Emergent Abilities**:
```yaml
# Scale-Dependent Capabilities
Few-shot Learning: Learn from examples in prompt
Chain of Thought: Step-by-step reasoning
Code Generation: Write functional programs
Mathematical Reasoning: Solve complex problems
Multilingual Understanding: Work across languages

# Threshold Effects
- Capabilities emerge suddenly at certain scales
- Not predictable from smaller models
- Quality improvements with size
```

**Current Limitations**:
```yaml
# Knowledge Limitations
Training Cutoff: Knowledge frozen at training time
Hallucinations: Generate plausible but false information
Factual Errors: Inconsistent with reality
Bias: Reflect training data biases

# Reasoning Limitations
Logical Consistency: May contradict itself
Mathematical Accuracy: Errors in complex calculations
Causal Understanding: Correlation vs causation confusion
```

## 7. Evaluation Metrics
**Text Generation Metrics**:
```python
# BLEU Score (machine translation)
from nltk.translate.bleu_score import sentence_bleu

reference = [['the', 'cat', 'is', 'on', 'the', 'mat']]
candidate = ['the', 'cat', 'sits', 'on', 'the', 'mat']
score = sentence_bleu(reference, candidate)

# ROUGE Score (summarization)
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])
scores = scorer.score('reference summary', 'generated summary')

# Perplexity (language modeling)
import torch
import torch.nn.functional as F

def perplexity(model, text):
    tokens = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**tokens)
        loss = F.cross_entropy(outputs.logits.view(-1, outputs.logits.size(-1)), 
                              tokens.input_ids.view(-1))
    return torch.exp(loss).item()
```

**Human Evaluation**:
```yaml
# Quality Dimensions
Helpfulness: Does it answer the question?
Harmlessness: Is it safe and appropriate?
Honesty: Is it truthful and acknowledges uncertainty?
Coherence: Is it logically consistent?
Relevance: Does it stay on topic?

# Evaluation Methods
Pairwise Comparison: A vs B preference
Likert Scales: 1-5 rating on dimensions
Task-Specific: Success rate on specific tasks
```

## 8. Deployment Patterns
**API-Based Deployment**:
```python
# OpenAI API pattern
import openai

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content

# Advantages: No infrastructure, always updated
# Disadvantages: Cost per call, latency, data privacy
```

**Self-Hosted Models**:
```python
# Hugging Face Transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_local(prompt):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=100, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Advantages: Data privacy, cost control, customization
# Disadvantages: Infrastructure, maintenance, updates
```

## 9. Fine-tuning and Customization
**Parameter-Efficient Fine-tuning**:
```python
# LoRA (Low-Rank Adaptation)
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
)

model = get_peft_model(base_model, config)

# Advantages: Faster training, less memory, preserve base model
```

**Domain Adaptation**:
```python
# Custom dataset preparation
training_data = [
    {"input": "What is ETL?", "output": "ETL stands for Extract, Transform, Load..."},
    {"input": "Explain data warehousing", "output": "Data warehousing is..."},
    # More domain-specific examples
]

# Fine-tuning process
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./fine-tuned-model",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=5e-5,
    logging_steps=100,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

## 10. Ethical Considerations
**Bias and Fairness**:
```yaml
# Types of Bias
Training Data Bias: Reflects societal biases
Representation Bias: Underrepresented groups
Confirmation Bias: Reinforces existing beliefs
Selection Bias: Non-representative training data

# Mitigation Strategies
Diverse Training Data: Include varied perspectives
Bias Testing: Evaluate across demographics
Human Oversight: Review outputs for bias
Continuous Monitoring: Track bias metrics
```

**Safety and Alignment**:
```yaml
# Safety Concerns
Misinformation: False or misleading content
Harmful Content: Violence, hate speech, illegal activities
Privacy Violations: Exposing personal information
Manipulation: Persuasive but deceptive content

# Alignment Techniques
Constitutional AI: Train with explicit principles
Red Teaming: Adversarial testing for vulnerabilities
Human Feedback: Incorporate human preferences
Content Filtering: Block harmful outputs
```

## 11. Future Directions
**Emerging Trends**:
```yaml
# Multimodal Integration
Vision + Language: Understand images and text together
Audio + Text: Process speech and written content
Video Understanding: Analyze temporal visual content

# Reasoning Improvements
Tool Use: Integrate with external APIs and databases
Planning: Multi-step problem solving
Memory: Long-term context and learning

# Efficiency Advances
Model Compression: Smaller models with similar performance
Edge Deployment: Run on mobile and IoT devices
Specialized Hardware: Custom chips for AI inference
```

**Research Frontiers**:
```yaml
# Scientific Applications
Drug Discovery: Generate novel molecular structures
Materials Science: Design new materials
Climate Modeling: Improve weather predictions

# Creative Applications
Content Creation: Automated writing, art, music
Game Development: Procedural content generation
Education: Personalized learning experiences
```
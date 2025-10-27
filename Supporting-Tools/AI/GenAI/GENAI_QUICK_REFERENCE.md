# 🚀 Generative AI - Quick Reference Guide (2024)

> **The ultimate GenAI cheat sheet for data engineers - everything you need in one place**

## 📋 **Quick Navigation**

| 🎯 **Section** | ⏱️ **Read Time** | 🎯 **Best For** |
|----------------|------------------|------------------|
| **[Model Comparison](#-model-comparison-2024)** | 2 min | Choosing the right model |
| **[Prompt Templates](#-prompt-engineering-templates)** | 3 min | Writing better prompts |
| **[Code Examples](#-practical-code-examples)** | 5 min | Implementation |
| **[Cost Calculator](#-cost-calculator)** | 1 min | Budget planning |
| **[Best Practices](#-best-practices-checklist)** | 3 min | Production deployment |

---

## 🏆 **Model Comparison (2024)**

### 🥇 **Top-Tier Models** (Best Performance)

| Model | Provider | Strengths | Cost/1K tokens | Best For |
|-------|----------|-----------|----------------|----------|
| **GPT-4 Turbo** | OpenAI | Best overall, coding, reasoning | $0.01/$0.03 | Complex analysis, code generation |
| **Claude 3 Opus** | Anthropic | Long context, safety, analysis | $0.015/$0.075 | Document analysis, research |
| **Gemini Ultra** | Google | Multimodal, fast, integrated | $0.0125/$0.0375 | Data analysis, visualization |

### 🥈 **Mid-Tier Models** (Best Value)

| Model | Provider | Strengths | Cost/1K tokens | Best For |
|-------|----------|-----------|----------------|----------|
| **GPT-3.5 Turbo** | OpenAI | Fast, reliable, cheap | $0.0005/$0.0015 | Simple tasks, high volume |
| **Claude 3 Haiku** | Anthropic | Fast, efficient, safe | $0.00025/$0.00125 | Quick responses, filtering |
| **Gemini Pro** | Google | Good balance, free tier | $0.0005/$0.0015 | General purpose, experimentation |

### 🥉 **Specialized Models**

| Model | Provider | Specialization | Cost/1K tokens | Best For |
|-------|----------|----------------|----------------|----------|
| **Code Llama** | Meta | Code generation | Free (self-hosted) | Programming, debugging |
| **Whisper** | OpenAI | Speech-to-text | $0.006/minute | Audio transcription |
| **DALL-E 3** | OpenAI | Image generation | $0.04-0.08/image | Visual content creation |

---

## 🎯 **Prompt Engineering Templates**

### 📝 **Basic Template Structure**

```python
# ✅ GOOD: Structured prompt template
prompt_template = """
Role: You are a {role} with {experience} years of experience
Task: {specific_task}
Context: {relevant_context}
Requirements:
1. {requirement_1}
2. {requirement_2}
3. {requirement_3}
Format: {output_format}
Constraints: {limitations}

Input: {user_input}
"""

# ❌ BAD: Vague prompt
bad_prompt = "Help me with data engineering"
```

### 🔧 **Data Engineering Specific Templates**

#### **SQL Generation Template**
```python
sql_prompt = """
Role: You are a senior database engineer with expertise in {database_type}
Task: Convert the business requirement to an optimized SQL query

Schema Information:
{schema_details}

Business Requirement: {requirement}

Requirements:
1. Write syntactically correct {database_type} SQL
2. Optimize for performance (use indexes, avoid subqueries where possible)
3. Include proper error handling
4. Add comments explaining complex logic
5. Follow naming conventions: snake_case for columns/tables

Output Format: 
- SQL query only
- No explanations unless requested
"""

# Example usage
sql_query = sql_prompt.format(
    database_type="PostgreSQL",
    schema_details="customers(id, name, email), orders(id, customer_id, date, amount)",
    requirement="Find top 5 customers by total spending in 2024"
)
```

#### **Code Review Template**
```python
code_review_prompt = """
Role: You are a principal data engineer conducting a code review
Task: Review the following {language} code for a data pipeline

Code to Review:
```{language}
{code}
```

Review Criteria:
1. **Correctness**: Does the code work as intended?
2. **Performance**: Are there optimization opportunities?
3. **Maintainability**: Is the code readable and well-structured?
4. **Error Handling**: Are edge cases and errors handled properly?
5. **Security**: Are there any security vulnerabilities?
6. **Best Practices**: Does it follow {language} and data engineering best practices?

Output Format:
## Strengths
- [List 2-3 positive aspects]

## Issues Found
- **Critical**: [Issues that must be fixed]
- **Major**: [Important improvements]
- **Minor**: [Nice-to-have improvements]

## Recommendations
- [Specific actionable suggestions]
"""
```

#### **Data Analysis Template**
```python
analysis_prompt = """
Role: You are a senior data analyst with expertise in {domain}
Task: Analyze the provided dataset and generate insights

Dataset Information:
- Rows: {row_count}
- Columns: {column_info}
- Time Period: {time_period}
- Business Context: {context}

Analysis Requirements:
1. Identify key trends and patterns
2. Highlight anomalies or outliers
3. Provide business-relevant insights
4. Suggest actionable recommendations
5. Include statistical significance where relevant

Data Sample:
{data_sample}

Output Format:
## Executive Summary
[2-3 sentence overview]

## Key Findings
1. [Finding with supporting data]
2. [Finding with supporting data]
3. [Finding with supporting data]

## Recommendations
- [Actionable recommendation 1]
- [Actionable recommendation 2]

## Technical Notes
[Any caveats or limitations]
"""
```

### 🧠 **Advanced Prompt Techniques**

#### **Chain of Thought Prompting**
```python
cot_prompt = """
Problem: {problem_description}

Solve this step-by-step:

Step 1: Understand the problem
- What are we trying to achieve?
- What constraints do we have?
- What data/resources are available?

Step 2: Break down the approach
- What are the main components?
- How do they interact?
- What's the logical sequence?

Step 3: Implementation details
- What specific technologies/tools?
- What are the key considerations?
- How do we handle edge cases?

Step 4: Validation and testing
- How do we verify correctness?
- What metrics should we track?
- What could go wrong?

Final Answer: [Comprehensive solution]
"""
```

#### **Few-Shot Learning Template**
```python
few_shot_prompt = """
Convert natural language data requirements to Python pandas code:

Example 1:
Requirement: "Calculate the average order value by customer segment"
Code:
```python
avg_order_by_segment = df.groupby('customer_segment')['order_value'].mean()
print(avg_order_by_segment)
```

Example 2:
Requirement: "Find customers who haven't ordered in the last 30 days"
Code:
```python
from datetime import datetime, timedelta
cutoff_date = datetime.now() - timedelta(days=30)
inactive_customers = df[df['last_order_date'] < cutoff_date]['customer_id'].unique()
print(f"Inactive customers: {len(inactive_customers)}")
```

Example 3:
Requirement: "Identify the top 10% of products by revenue"
Code:
```python
product_revenue = df.groupby('product_id')['revenue'].sum()
top_10_percent_threshold = product_revenue.quantile(0.9)
top_products = product_revenue[product_revenue >= top_10_percent_threshold]
print(top_products.sort_values(ascending=False))
```

Now convert:
Requirement: "{new_requirement}"
Code:
"""
```

---

## 💻 **Practical Code Examples**

### 🔌 **OpenAI API Integration**

```python
import openai
from typing import Dict, List, Optional
import json
import time

class DataEngineeringAI:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        
    def generate_sql(self, requirement: str, schema: Dict) -> str:
        """Generate SQL from natural language requirement."""
        prompt = f"""
        Generate PostgreSQL query for: {requirement}
        
        Schema: {json.dumps(schema, indent=2)}
        
        Return only the SQL query, properly formatted.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.1
        )
        
        return response.choices[0].message.content.strip()
    
    def explain_data_pattern(self, data_description: str) -> str:
        """Explain patterns in data analysis results."""
        prompt = f"""
        As a senior data analyst, explain this data pattern in business terms:
        
        {data_description}
        
        Provide:
        1. What this pattern means
        2. Possible causes
        3. Business implications
        4. Recommended actions
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def review_pipeline_code(self, code: str, language: str = "python") -> Dict:
        """Get AI code review for data pipeline."""
        prompt = f"""
        Review this {language} data pipeline code:
        
        ```{language}
        {code}
        ```
        
        Provide structured feedback in JSON format:
        {{
            "overall_score": 1-10,
            "strengths": ["strength1", "strength2"],
            "issues": {{
                "critical": ["issue1"],
                "major": ["issue1", "issue2"],
                "minor": ["issue1"]
            }},
            "recommendations": ["rec1", "rec2"],
            "security_concerns": ["concern1"]
        }}
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.2
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI response"}

# Usage example
ai = DataEngineeringAI("your-api-key")

# Generate SQL
schema = {
    "customers": ["id", "name", "email", "signup_date"],
    "orders": ["id", "customer_id", "order_date", "amount"]
}
sql = ai.generate_sql("Find customers who spent more than $1000 total", schema)
print(sql)
```

### 🏗️ **RAG System Implementation**

```python
import chromadb
from sentence_transformers import SentenceTransformer
import openai
from typing import List, Dict

class SimpleRAG:
    def __init__(self, openai_key: str):
        self.client = openai.OpenAI(api_key=openai_key)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection("docs")
        
    def add_document(self, text: str, metadata: Dict = None):
        """Add document to knowledge base."""
        embedding = self.embedder.encode(text).tolist()
        doc_id = f"doc_{len(self.collection.get()['ids'])}"
        
        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
    
    def query(self, question: str, top_k: int = 3) -> str:
        """Query the knowledge base."""
        # Get relevant documents
        query_embedding = self.embedder.encode(question).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Build context
        context = "\n\n".join(results['documents'][0])
        
        # Generate answer
        prompt = f"""
        Based on the following context, answer the question:
        
        Context:
        {context}
        
        Question: {question}
        
        Answer based only on the provided context. If the context doesn't contain enough information, say so.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        return response.choices[0].message.content

# Usage
rag = SimpleRAG("your-openai-key")

# Add documents
rag.add_document("Apache Spark is a distributed computing framework for big data processing.")
rag.add_document("Kafka is a distributed streaming platform for real-time data pipelines.")

# Query
answer = rag.query("What is Apache Spark used for?")
print(answer)
```

### 🔄 **Batch Processing with AI**

```python
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import openai
from typing import List
import time

class BatchAIProcessor:
    def __init__(self, api_key: str, max_workers: int = 5):
        self.client = openai.OpenAI(api_key=api_key)
        self.max_workers = max_workers
        
    def process_batch(self, texts: List[str], task: str) -> List[str]:
        """Process multiple texts in parallel."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(self._process_single, text, task) 
                for text in texts
            ]
            results = [future.result() for future in futures]
        return results
    
    def _process_single(self, text: str, task: str) -> str:
        """Process single text with rate limiting."""
        prompt = f"""
        Task: {task}
        
        Text: {text}
        
        Provide a concise response.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_customer_feedback(self, feedback_df: pd.DataFrame) -> pd.DataFrame:
        """Analyze customer feedback sentiment and themes."""
        feedback_texts = feedback_df['feedback'].tolist()
        
        # Analyze sentiment
        sentiments = self.process_batch(
            feedback_texts, 
            "Classify sentiment as Positive, Negative, or Neutral"
        )
        
        # Extract themes
        themes = self.process_batch(
            feedback_texts,
            "Extract main theme/topic in 2-3 words"
        )
        
        # Add results to dataframe
        feedback_df['ai_sentiment'] = sentiments
        feedback_df['ai_theme'] = themes
        
        return feedback_df

# Usage
processor = BatchAIProcessor("your-api-key")

# Sample data
df = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'feedback': [
        "Great service, very satisfied!",
        "Slow response time, needs improvement",
        "Average experience, nothing special"
    ]
})

# Process
results = processor.analyze_customer_feedback(df)
print(results)
```

---

## 💰 **Cost Calculator**

### 📊 **Token Estimation**

```python
def estimate_tokens(text: str) -> int:
    """Rough token estimation (1 token ≈ 4 characters)."""
    return len(text) // 4

def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Calculate API cost for different models."""
    
    pricing = {
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
        "gemini-pro": {"input": 0.0005, "output": 0.0015}
    }
    
    if model not in pricing:
        return 0.0
    
    input_cost = (input_tokens / 1000) * pricing[model]["input"]
    output_cost = (output_tokens / 1000) * pricing[model]["output"]
    
    return input_cost + output_cost

# Example usage
prompt = "Analyze this data and provide insights..."
estimated_input = estimate_tokens(prompt)
estimated_output = 500  # Expected response length

cost_gpt4 = calculate_cost(estimated_input, estimated_output, "gpt-4-turbo")
cost_gpt35 = calculate_cost(estimated_input, estimated_output, "gpt-3.5-turbo")

print(f"GPT-4 Turbo cost: ${cost_gpt4:.4f}")
print(f"GPT-3.5 Turbo cost: ${cost_gpt35:.4f}")
```

### 💡 **Cost Optimization Tips**

```yaml
# 🎯 Model Selection Strategy
Simple Tasks: Use GPT-3.5 Turbo (10x cheaper than GPT-4)
Complex Analysis: Use GPT-4 Turbo only when needed
High Volume: Consider Claude 3 Haiku for basic tasks

# ⚡ Prompt Optimization
- Be concise but specific
- Use system messages to set context once
- Batch similar requests together
- Cache common responses

# 🔄 Smart Routing
def choose_model(task_complexity: str) -> str:
    if task_complexity == "simple":
        return "gpt-3.5-turbo"  # $0.002 per 1K tokens
    elif task_complexity == "medium":
        return "claude-3-haiku"  # $0.00125 per 1K tokens  
    else:
        return "gpt-4-turbo"  # $0.04 per 1K tokens

# 📊 Monthly Budget Planning
Daily Requests: 1000
Average Tokens per Request: 1000 (500 in + 500 out)
Model: GPT-3.5 Turbo

Daily Cost: 1000 * (1000/1000) * $0.002 = $2
Monthly Cost: $2 * 30 = $60
```

---

## ✅ **Best Practices Checklist**

### 🔒 **Security & Privacy**

```yaml
✅ Input Validation:
  - Sanitize user inputs
  - Validate prompt injection attempts
  - Limit input length and complexity

✅ Data Protection:
  - Never send sensitive data to external APIs
  - Use data masking for PII
  - Implement proper access controls

✅ Output Filtering:
  - Scan for harmful content
  - Validate generated code before execution
  - Implement content moderation

✅ API Security:
  - Rotate API keys regularly
  - Use environment variables for secrets
  - Implement rate limiting
  - Monitor API usage and costs
```

### 🎯 **Quality Assurance**

```yaml
✅ Testing Strategy:
  - Test with diverse input examples
  - Validate outputs against expected results
  - Implement automated quality checks
  - Use human evaluation for critical tasks

✅ Monitoring:
  - Track model performance metrics
  - Monitor response quality over time
  - Set up alerts for anomalies
  - Log all interactions for debugging

✅ Fallback Mechanisms:
  - Handle API failures gracefully
  - Implement retry logic with backoff
  - Provide alternative solutions
  - Maintain system availability
```

### 🚀 **Performance Optimization**

```yaml
✅ Prompt Engineering:
  - Use clear, specific instructions
  - Provide relevant examples
  - Optimize for consistency
  - Test different prompt variations

✅ Caching Strategy:
  - Cache common responses
  - Use semantic similarity for cache hits
  - Implement cache invalidation
  - Monitor cache hit rates

✅ Batch Processing:
  - Group similar requests
  - Use parallel processing
  - Implement proper rate limiting
  - Optimize for throughput vs latency
```

### 📊 **Production Deployment**

```yaml
✅ Infrastructure:
  - Use containerized deployments
  - Implement auto-scaling
  - Set up proper monitoring
  - Plan for disaster recovery

✅ Model Management:
  - Version control for prompts
  - A/B testing for improvements
  - Gradual rollout strategies
  - Rollback procedures

✅ Compliance:
  - Document AI usage and decisions
  - Implement audit trails
  - Ensure regulatory compliance
  - Regular bias and fairness testing
```

---

## 🔧 **Troubleshooting Guide**

### ❌ **Common Issues & Solutions**

| Problem | Cause | Solution |
|---------|-------|----------|
| **Inconsistent outputs** | Temperature too high | Lower temperature (0.1-0.3) |
| **Generic responses** | Vague prompts | Add specific examples and context |
| **API timeouts** | Large requests | Break into smaller chunks |
| **High costs** | Wrong model choice | Use cheaper models for simple tasks |
| **Hallucinations** | Lack of grounding | Implement RAG or fact-checking |
| **Biased outputs** | Training data bias | Add bias detection and mitigation |

### 🔍 **Debugging Checklist**

```python
def debug_ai_response(prompt: str, response: str) -> Dict:
    """Debug AI response quality."""
    
    checks = {
        "prompt_clarity": len(prompt.split()) > 10,  # Sufficient detail
        "response_length": 50 < len(response) < 2000,  # Reasonable length
        "contains_code": "```" in response,  # Code blocks if expected
        "factual_claims": "according to" in response.lower(),  # Source attribution
        "uncertainty": any(word in response.lower() for word in ["might", "could", "possibly"])
    }
    
    return checks

# Usage
result = debug_ai_response(prompt, ai_response)
print("Debug results:", result)
```

---

## 📚 **Additional Resources**

### 🔗 **Essential Links**

- **[OpenAI Documentation](https://platform.openai.com/docs)** - Official API docs
- **[Anthropic Claude](https://docs.anthropic.com/)** - Claude API documentation  
- **[Hugging Face](https://huggingface.co/)** - Open source models and datasets
- **[LangChain](https://python.langchain.com/)** - AI application framework
- **[Prompt Engineering Guide](https://www.promptingguide.ai/)** - Comprehensive prompting techniques

### 📖 **Recommended Reading**

- **"Attention Is All You Need"** - Original Transformer paper
- **"Language Models are Few-Shot Learners"** - GPT-3 paper
- **"Constitutional AI"** - Anthropic's safety approach
- **"Retrieval-Augmented Generation"** - RAG methodology

---

**🎯 Keep this guide handy for quick reference during development and interviews!**

*Last updated: 2024 | Next update: Check for new model releases and pricing changes*
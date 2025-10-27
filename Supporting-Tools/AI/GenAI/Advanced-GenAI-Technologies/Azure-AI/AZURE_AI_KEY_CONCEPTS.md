# ☁️ Azure AI Services - Key Concepts

## 🎯 **Real-World Analogy: The Cloud-Based AI Toolkit**

> **Think of Azure AI as a comprehensive toolkit in the cloud where you can pick and choose different AI services like tools from a workshop - each specialized for specific tasks but all working together seamlessly.**

## 🔥 **Core Azure AI Services**

### 1. **Azure OpenAI Service** 🤖

```python
# Azure OpenAI integration
import openai
from azure.identity import DefaultAzureCredential

# Configure Azure OpenAI
openai.api_type = "azure"
openai.api_base = "https://your-resource.openai.azure.com/"
openai.api_version = "2023-12-01-preview"
openai.api_key = "your-api-key"

# Chat completion
response = openai.ChatCompletion.create(
    engine="gpt-4",  # Your deployment name
    messages=[
        {"role": "system", "content": "You are a helpful data analyst."},
        {"role": "user", "content": "Analyze this sales data and provide insights."}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### 2. **Azure Cognitive Search** 🔍

```python
# Azure AI Search with vector capabilities
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential

# Initialize clients
search_client = SearchClient(
    endpoint="https://your-service.search.windows.net",
    index_name="documents",
    credential=AzureKeyCredential("your-key")
)

# Hybrid search (keyword + vector)
results = search_client.search(
    search_text="data engineering best practices",
    vector_queries=[{
        "vector": query_embedding,
        "k_nearest_neighbors": 5,
        "fields": "content_vector"
    }],
    select=["title", "content", "category"],
    top=10
)

for result in results:
    print(f"Title: {result['title']}")
    print(f"Score: {result['@search.score']}")
```

### 3. **Azure Document Intelligence** 📄

```python
# Document processing and extraction
from azure.ai.formrecognizer import DocumentAnalysisClient

document_client = DocumentAnalysisClient(
    endpoint="https://your-resource.cognitiveservices.azure.com/",
    credential=AzureKeyCredential("your-key")
)

# Analyze document
with open("invoice.pdf", "rb") as f:
    poller = document_client.begin_analyze_document(
        "prebuilt-invoice", document=f
    )
    result = poller.result()

# Extract structured data
for invoice in result.documents:
    vendor_name = invoice.fields.get("VendorName")
    invoice_total = invoice.fields.get("InvoiceTotal")
    
    print(f"Vendor: {vendor_name.value if vendor_name else 'N/A'}")
    print(f"Total: {invoice_total.value if invoice_total else 'N/A'}")
```

### 4. **Azure Speech Services** 🎤

```python
# Speech-to-text and text-to-speech
import azure.cognitiveservices.speech as speechsdk

# Configure speech service
speech_config = speechsdk.SpeechConfig(
    subscription="your-key",
    region="your-region"
)

# Speech-to-text
def speech_to_text(audio_file):
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    
    result = speech_recognizer.recognize_once()
    return result.text

# Text-to-speech
def text_to_speech(text, output_file):
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    
    result = speech_synthesizer.speak_text_async(text).get()
    return result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted
```

## 🏗️ **Enterprise Integration Patterns**

### **Multi-Service AI Pipeline**
```python
# Complete Azure AI pipeline
class AzureAIPipeline:
    def __init__(self):
        self.openai_client = self.setup_openai()
        self.search_client = self.setup_search()
        self.document_client = self.setup_document_intelligence()
        self.speech_client = self.setup_speech()
    
    async def process_document_query(self, document_path, user_query):
        # Step 1: Extract text from document
        document_content = await self.extract_document_content(document_path)
        
        # Step 2: Index document for search
        await self.index_document(document_content)
        
        # Step 3: Search for relevant content
        search_results = await self.search_content(user_query)
        
        # Step 4: Generate AI response
        response = await self.generate_response(user_query, search_results)
        
        return response
    
    async def extract_document_content(self, document_path):
        with open(document_path, "rb") as f:
            poller = self.document_client.begin_analyze_document(
                "prebuilt-layout", document=f
            )
            result = poller.result()
        
        # Extract text content
        content = ""
        for page in result.pages:
            for line in page.lines:
                content += line.content + "\n"
        
        return content
    
    async def generate_response(self, query, context):
        prompt = f"""
        Based on the following document content:
        {context}
        
        Answer this question: {query}
        
        Provide a comprehensive answer based only on the document content.
        """
        
        response = openai.ChatCompletion.create(
            engine="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        return response.choices[0].message.content
```

### **Azure AI Studio Integration**
```python
# Azure AI Studio project integration
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

class AzureAIStudioIntegration:
    def __init__(self, subscription_id, resource_group, workspace_name):
        self.ml_client = MLClient(
            DefaultAzureCredential(),
            subscription_id,
            resource_group,
            workspace_name
        )
    
    def deploy_model(self, model_name, deployment_config):
        # Deploy model to Azure AI Studio
        deployment = self.ml_client.online_deployments.begin_create_or_update(
            deployment_config
        ).result()
        
        return deployment
    
    def create_ai_project(self, project_config):
        # Create new AI project
        project = self.ml_client.workspaces.begin_create(
            project_config
        ).result()
        
        return project
```

## 🔒 **Security and Compliance**

### **Azure AI Security Best Practices**
```python
# Secure Azure AI implementation
class SecureAzureAI:
    def __init__(self):
        self.setup_security()
    
    def setup_security(self):
        # Use managed identity
        from azure.identity import ManagedIdentityCredential
        self.credential = ManagedIdentityCredential()
        
        # Configure private endpoints
        self.private_endpoint_config = {
            "enable_private_endpoint": True,
            "vnet_integration": True,
            "firewall_rules": ["allow_azure_services"]
        }
    
    def secure_api_call(self, service_endpoint, data):
        # Encrypt data in transit
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json",
            "X-Content-Type-Options": "nosniff"
        }
        
        # Log API calls for audit
        self.audit_log.log_api_call(service_endpoint, data)
        
        response = requests.post(
            service_endpoint,
            json=data,
            headers=headers,
            verify=True  # SSL verification
        )
        
        return response
    
    def implement_data_governance(self):
        governance_config = {
            "data_classification": "confidential",
            "retention_policy": "7_years",
            "encryption_at_rest": True,
            "audit_logging": True,
            "access_controls": "rbac"
        }
        
        return governance_config
```

## 💰 **Cost Optimization**

### **Azure AI Cost Management**
```python
# Cost optimization strategies
class AzureAICostOptimizer:
    def __init__(self):
        self.cost_tracker = {}
        self.budget_limits = {
            "openai": 1000,  # $1000/month
            "search": 500,   # $500/month
            "speech": 200    # $200/month
        }
    
    def optimize_openai_usage(self):
        strategies = {
            "model_selection": {
                "simple_tasks": "gpt-3.5-turbo",  # Cheaper
                "complex_tasks": "gpt-4",         # More expensive but better
                "cost_savings": "60-80%"
            },
            
            "prompt_optimization": {
                "technique": "Reduce token usage",
                "methods": ["Shorter prompts", "Efficient formatting"],
                "cost_savings": "20-40%"
            },
            
            "caching": {
                "implementation": "Cache common responses",
                "hit_ratio_target": "70%",
                "cost_savings": "50-70%"
            }
        }
        
        return strategies
    
    def monitor_costs(self):
        # Real-time cost monitoring
        current_costs = self.get_current_month_costs()
        
        for service, cost in current_costs.items():
            if cost > self.budget_limits[service] * 0.8:  # 80% threshold
                self.send_cost_alert(service, cost)
        
        return current_costs
```
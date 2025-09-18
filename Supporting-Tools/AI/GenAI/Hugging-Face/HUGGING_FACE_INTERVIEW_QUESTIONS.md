# Hugging Face Interview Questions

## Basic Concepts

### 1. What is Hugging Face and what are its main components?
**Answer:** Hugging Face is an open-source platform for machine learning, particularly focused on Natural Language Processing (NLP) and transformers. Main components:

- **Transformers Library**: Pre-trained models and tokenizers
- **Datasets Library**: Access to ML datasets
- **Tokenizers**: Fast tokenization library
- **Hub**: Model and dataset repository
- **Spaces**: ML app hosting platform

```python
from transformers import AutoTokenizer, AutoModel, pipeline

# Load pre-trained model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Quick pipeline usage
classifier = pipeline("sentiment-analysis")
result = classifier("I love Hugging Face!")
print(result)
# Output: [{'label': 'POSITIVE', 'score': 0.9998}]

# Text generation pipeline
generator = pipeline("text-generation", model="gpt2")
output = generator("The future of AI is", max_length=50, num_return_sequences=2)
print(output)
```

### 2. How do you use Hugging Face tokenizers?
**Answer:** Tokenizers convert text into numerical representations that models can process.

```python
from transformers import AutoTokenizer, BertTokenizer

# Auto tokenizer (recommended)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Basic tokenization
text = "Hello, how are you doing today?"
tokens = tokenizer.tokenize(text)
print(f"Tokens: {tokens}")

# Encoding (text to IDs)
encoded = tokenizer.encode(text, add_special_tokens=True)
print(f"Token IDs: {encoded}")

# Batch encoding
texts = ["Hello world!", "How are you?", "Fine, thank you."]
batch_encoded = tokenizer(
    texts,
    padding=True,
    truncation=True,
    max_length=128,
    return_tensors="pt"
)
print(f"Input IDs shape: {batch_encoded['input_ids'].shape}")
print(f"Attention mask shape: {batch_encoded['attention_mask'].shape}")

# Decoding (IDs back to text)
decoded = tokenizer.decode(encoded, skip_special_tokens=True)
print(f"Decoded: {decoded}")

# Advanced tokenization features
encoded_advanced = tokenizer(
    text,
    add_special_tokens=True,
    padding='max_length',
    max_length=64,
    truncation=True,
    return_attention_mask=True,
    return_token_type_ids=True,
    return_tensors='pt'
)

print("Advanced encoding:")
for key, value in encoded_advanced.items():
    print(f"{key}: {value}")

# Custom tokenizer training
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

# Create custom tokenizer
tokenizer_custom = Tokenizer(BPE(unk_token="[UNK]"))
trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
tokenizer_custom.pre_tokenizer = Whitespace()

# Train on custom data
# files = ["path/to/dataset.txt"]
# tokenizer_custom.train(files, trainer)
```

### 3. How do you load and use pre-trained models from Hugging Face Hub?
**Answer:** Hugging Face Hub provides thousands of pre-trained models for various tasks.

```python
from transformers import (
    AutoModel, AutoTokenizer, AutoModelForSequenceClassification,
    AutoModelForQuestionAnswering, AutoModelForTokenClassification
)
import torch

# Basic model loading
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Task-specific models
# Sentiment Analysis
sentiment_model = AutoModelForSequenceClassification.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment-latest"
)

# Question Answering
qa_model = AutoModelForQuestionAnswering.from_pretrained(
    "distilbert-base-cased-distilled-squad"
)

# Named Entity Recognition
ner_model = AutoModelForTokenClassification.from_pretrained(
    "dbmdz/bert-large-cased-finetuned-conll03-english"
)

# Model inference
def classify_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad():
        outputs = sentiment_model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
    labels = ["NEGATIVE", "NEUTRAL", "POSITIVE"]
    predicted_class = torch.argmax(predictions, dim=-1).item()
    confidence = predictions[0][predicted_class].item()
    
    return {
        "label": labels[predicted_class],
        "confidence": confidence
    }

# Usage
result = classify_sentiment("I love this product!")
print(result)

# Model with custom configuration
from transformers import BertConfig

config = BertConfig(
    vocab_size=30522,
    hidden_size=768,
    num_hidden_layers=12,
    num_attention_heads=12,
    intermediate_size=3072,
    max_position_embeddings=512,
    num_labels=3  # For classification
)

custom_model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    config=config
)

# Save model locally
model.save_pretrained("./my_model")
tokenizer.save_pretrained("./my_model")

# Load from local directory
loaded_model = AutoModel.from_pretrained("./my_model")
loaded_tokenizer = AutoTokenizer.from_pretrained("./my_model")
```

### 4. How do you use Hugging Face pipelines for different NLP tasks?
**Answer:** Pipelines provide a high-level interface for common NLP tasks.

```python
from transformers import pipeline
import torch

# Text Classification
classifier = pipeline(
    "text-classification",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    device=0 if torch.cuda.is_available() else -1
)

texts = [
    "I love this movie!",
    "This is terrible.",
    "It's okay, nothing special."
]

results = classifier(texts)
for text, result in zip(texts, results):
    print(f"Text: {text}")
    print(f"Sentiment: {result['label']} (confidence: {result['score']:.4f})")

# Question Answering
qa_pipeline = pipeline("question-answering")

context = """
Hugging Face is a company that develops tools for building applications using 
machine learning. It is most notable for its transformers library built for 
natural language processing applications and its platform that allows users 
to share machine learning models and datasets.
"""

questions = [
    "What does Hugging Face develop?",
    "What is Hugging Face most notable for?",
    "What can users share on the platform?"
]

for question in questions:
    result = qa_pipeline(question=question, context=context)
    print(f"Q: {question}")
    print(f"A: {result['answer']} (confidence: {result['score']:.4f})")
    print()

# Named Entity Recognition
ner_pipeline = pipeline("ner", aggregation_strategy="simple")

text = "Apple Inc. was founded by Steve Jobs in Cupertino, California."
entities = ner_pipeline(text)

for entity in entities:
    print(f"Entity: {entity['word']}")
    print(f"Label: {entity['entity_group']}")
    print(f"Confidence: {entity['score']:.4f}")
    print()

# Text Generation
generator = pipeline("text-generation", model="gpt2")

prompts = [
    "The future of artificial intelligence",
    "In a world where robots"
]

for prompt in prompts:
    generated = generator(
        prompt,
        max_length=100,
        num_return_sequences=2,
        temperature=0.7,
        do_sample=True,
        pad_token_id=generator.tokenizer.eos_token_id
    )
    
    print(f"Prompt: {prompt}")
    for i, gen in enumerate(generated):
        print(f"Generation {i+1}: {gen['generated_text']}")
    print()

# Summarization
summarizer = pipeline("summarization")

long_text = """
Artificial intelligence (AI) is intelligence demonstrated by machines, 
in contrast to the natural intelligence displayed by humans and animals. 
Leading AI textbooks define the field as the study of "intelligent agents": 
any device that perceives its environment and takes actions that maximize 
its chance of successfully achieving its goals. Colloquially, the term 
"artificial intelligence" is often used to describe machines that mimic 
"cognitive" functions that humans associate with the human mind, such as 
"learning" and "problem solving".
"""

summary = summarizer(long_text, max_length=50, min_length=25, do_sample=False)
print(f"Original length: {len(long_text.split())}")
print(f"Summary: {summary[0]['summary_text']}")
print(f"Summary length: {len(summary[0]['summary_text'].split())}")

# Translation
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

english_texts = [
    "Hello, how are you?",
    "I love machine learning.",
    "The weather is beautiful today."
]

for text in english_texts:
    translation = translator(text)
    print(f"English: {text}")
    print(f"French: {translation[0]['translation_text']}")
    print()

# Zero-shot Classification
zero_shot_classifier = pipeline("zero-shot-classification")

text = "I have a problem with my iPhone that needs to be resolved asap!"
candidate_labels = ["urgent", "not urgent", "phone", "tablet", "computer"]

result = zero_shot_classifier(text, candidate_labels)
print(f"Text: {text}")
print("Classification results:")
for label, score in zip(result['labels'], result['scores']):
    print(f"  {label}: {score:.4f}")
```

## Intermediate Concepts

### 5. How do you fine-tune Hugging Face models for custom tasks?
**Answer:** Fine-tuning adapts pre-trained models to specific tasks and datasets.

```python
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    TrainingArguments, Trainer, DataCollatorWithPadding
)
from datasets import Dataset
import torch
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Prepare custom dataset
def prepare_dataset():
    # Sample data (replace with your actual data)
    texts = [
        "This movie is amazing!",
        "I hate this film.",
        "It's an okay movie.",
        "Best movie ever!",
        "Worst movie I've seen.",
        "Not bad, could be better."
    ]
    labels = [1, 0, 2, 1, 0, 2]  # 0: negative, 1: positive, 2: neutral
    
    return Dataset.from_dict({
        "text": texts,
        "labels": labels
    })

# Tokenization function
def tokenize_function(examples, tokenizer):
    return tokenizer(
        examples["text"],
        truncation=True,
        padding=True,
        max_length=128
    )

# Fine-tuning setup
def setup_fine_tuning():
    model_name = "bert-base-uncased"
    num_labels = 3  # negative, positive, neutral
    
    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=num_labels
    )
    
    # Prepare dataset
    dataset = prepare_dataset()
    tokenized_dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True
    )
    
    # Split dataset
    train_size = int(0.8 * len(tokenized_dataset))
    train_dataset = tokenized_dataset.select(range(train_size))
    eval_dataset = tokenized_dataset.select(range(train_size, len(tokenized_dataset)))
    
    return model, tokenizer, train_dataset, eval_dataset

# Metrics computation
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions, average='weighted'
    )
    accuracy = accuracy_score(labels, predictions)
    
    return {
        'accuracy': accuracy,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

# Training function
def fine_tune_model():
    model, tokenizer, train_dataset, eval_dataset = setup_fine_tuning()
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=64,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
    )
    
    # Data collator
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    
    # Train model
    trainer.train()
    
    # Evaluate model
    eval_results = trainer.evaluate()
    print(f"Evaluation results: {eval_results}")
    
    # Save model
    trainer.save_model("./fine_tuned_model")
    tokenizer.save_pretrained("./fine_tuned_model")
    
    return trainer

# Custom training loop (alternative to Trainer)
def custom_training_loop():
    model, tokenizer, train_dataset, eval_dataset = setup_fine_tuning()
    
    # Prepare data loaders
    from torch.utils.data import DataLoader
    
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=16,
        shuffle=True,
        collate_fn=DataCollatorWithPadding(tokenizer)
    )
    
    eval_dataloader = DataLoader(
        eval_dataset,
        batch_size=64,
        collate_fn=DataCollatorWithPadding(tokenizer)
    )
    
    # Optimizer and scheduler
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
    
    from transformers import get_linear_schedule_with_warmup
    num_training_steps = len(train_dataloader) * 3  # 3 epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=num_training_steps
    )
    
    # Training loop
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    for epoch in range(3):
        model.train()
        total_loss = 0
        
        for batch in train_dataloader:
            # Move batch to device
            batch = {k: v.to(device) for k, v in batch.items()}
            
            # Forward pass
            outputs = model(**batch)
            loss = outputs.loss
            
            # Backward pass
            loss.backward()
            
            # Update weights
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
            
            total_loss += loss.item()
        
        # Evaluation
        model.eval()
        eval_loss = 0
        predictions = []
        true_labels = []
        
        with torch.no_grad():
            for batch in eval_dataloader:
                batch = {k: v.to(device) for k, v in batch.items()}
                outputs = model(**batch)
                
                eval_loss += outputs.loss.item()
                
                preds = torch.argmax(outputs.logits, dim=-1)
                predictions.extend(preds.cpu().numpy())
                true_labels.extend(batch['labels'].cpu().numpy())
        
        # Calculate metrics
        accuracy = accuracy_score(true_labels, predictions)
        
        print(f"Epoch {epoch + 1}:")
        print(f"  Train Loss: {total_loss / len(train_dataloader):.4f}")
        print(f"  Eval Loss: {eval_loss / len(eval_dataloader):.4f}")
        print(f"  Eval Accuracy: {accuracy:.4f}")

# Usage
if __name__ == "__main__":
    trainer = fine_tune_model()
```

### 6. How do you work with Hugging Face Datasets library?
**Answer:** The Datasets library provides easy access to ML datasets with efficient processing.

```python
from datasets import Dataset, DatasetDict, load_dataset
import pandas as pd
import numpy as np

# Load popular datasets
# Text classification
imdb_dataset = load_dataset("imdb")
print(f"IMDB dataset: {imdb_dataset}")

# Question answering
squad_dataset = load_dataset("squad")
print(f"SQuAD dataset: {squad_dataset}")

# Translation
wmt_dataset = load_dataset("wmt14", "fr-en")
print(f"WMT dataset: {wmt_dataset}")

# Create custom dataset from pandas DataFrame
def create_custom_dataset():
    # Sample data
    data = {
        'text': [
            "This is a positive review",
            "This is a negative review",
            "This is a neutral review"
        ],
        'label': [1, 0, 2],
        'metadata': [
            {'source': 'review_site_1'},
            {'source': 'review_site_2'},
            {'source': 'review_site_1'}
        ]
    }
    
    df = pd.DataFrame(data)
    dataset = Dataset.from_pandas(df)
    
    return dataset

# Dataset operations
def dataset_operations():
    dataset = create_custom_dataset()
    
    # Basic info
    print(f"Dataset length: {len(dataset)}")
    print(f"Dataset features: {dataset.features}")
    print(f"First example: {dataset[0]}")
    
    # Filtering
    positive_examples = dataset.filter(lambda x: x['label'] == 1)
    print(f"Positive examples: {len(positive_examples)}")
    
    # Mapping (preprocessing)
    def preprocess_text(example):
        example['text'] = example['text'].lower()
        example['text_length'] = len(example['text'])
        return example
    
    processed_dataset = dataset.map(preprocess_text)
    print(f"Processed example: {processed_dataset[0]}")
    
    # Batch processing
    def batch_preprocess(examples):
        examples['text'] = [text.upper() for text in examples['text']]
        return examples
    
    batch_processed = dataset.map(batch_preprocess, batched=True)
    
    # Select columns
    text_only = dataset.select_columns(['text'])
    
    # Rename columns
    renamed_dataset = dataset.rename_column('text', 'review_text')
    
    # Add column
    def add_sentiment_score(example):
        # Dummy sentiment score
        example['sentiment_score'] = np.random.random()
        return example
    
    dataset_with_score = dataset.map(add_sentiment_score)
    
    return processed_dataset

# Train/validation/test splits
def create_splits():
    dataset = load_dataset("imdb")
    
    # Split training set
    train_test_split = dataset['train'].train_test_split(test_size=0.2)
    
    # Create validation split from training
    train_val_split = train_test_split['train'].train_test_split(test_size=0.25)
    
    # Combine into DatasetDict
    dataset_splits = DatasetDict({
        'train': train_val_split['train'],
        'validation': train_val_split['test'],
        'test': train_test_split['test']
    })
    
    print(f"Train size: {len(dataset_splits['train'])}")
    print(f"Validation size: {len(dataset_splits['validation'])}")
    print(f"Test size: {len(dataset_splits['test'])}")
    
    return dataset_splits

# Streaming large datasets
def stream_large_dataset():
    # For very large datasets, use streaming
    dataset = load_dataset("oscar", "unshuffled_deduplicated_en", streaming=True)
    
    # Take first 1000 examples
    dataset_head = dataset['train'].take(1000)
    
    for i, example in enumerate(dataset_head):
        if i < 5:  # Print first 5 examples
            print(f"Example {i}: {example['text'][:100]}...")
        if i >= 1000:
            break
    
    return dataset_head

# Custom dataset loading
def load_custom_data():
    # From CSV
    csv_dataset = load_dataset('csv', data_files='path/to/data.csv')
    
    # From JSON
    json_dataset = load_dataset('json', data_files='path/to/data.json')
    
    # From text files
    text_dataset = load_dataset('text', data_files='path/to/data.txt')
    
    # Multiple files
    multi_file_dataset = load_dataset(
        'csv',
        data_files={
            'train': 'path/to/train.csv',
            'test': 'path/to/test.csv'
        }
    )
    
    return multi_file_dataset

# Dataset caching and saving
def dataset_caching():
    dataset = load_dataset("imdb")
    
    # Cache processed dataset
    def tokenize_function(examples):
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        return tokenizer(examples['text'], truncation=True, padding=True)
    
    # This will be cached automatically
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        cache_file_names={
            'train': 'cache/train_tokenized.arrow',
            'test': 'cache/test_tokenized.arrow'
        }
    )
    
    # Save dataset
    tokenized_dataset.save_to_disk("./processed_imdb")
    
    # Load saved dataset
    loaded_dataset = Dataset.load_from_disk("./processed_imdb")
    
    return loaded_dataset

# Advanced dataset features
def advanced_dataset_features():
    dataset = load_dataset("squad")
    
    # Flatten nested structure
    def flatten_squad(example):
        return {
            'context': example['context'],
            'question': example['question'],
            'answer_text': example['answers']['text'][0] if example['answers']['text'] else '',
            'answer_start': example['answers']['answer_start'][0] if example['answers']['answer_start'] else 0
        }
    
    flattened_dataset = dataset.map(flatten_squad)
    
    # Sort dataset
    sorted_dataset = flattened_dataset.sort('answer_start')
    
    # Shuffle dataset
    shuffled_dataset = dataset.shuffle(seed=42)
    
    # Concatenate datasets
    train_part1 = dataset['train'].select(range(1000))
    train_part2 = dataset['train'].select(range(1000, 2000))
    
    from datasets import concatenate_datasets
    combined_dataset = concatenate_datasets([train_part1, train_part2])
    
    # Dataset statistics
    def compute_stats(dataset):
        text_lengths = [len(example['context']) for example in dataset]
        
        stats = {
            'mean_length': np.mean(text_lengths),
            'std_length': np.std(text_lengths),
            'min_length': np.min(text_lengths),
            'max_length': np.max(text_lengths)
        }
        
        return stats
    
    stats = compute_stats(dataset['train'])
    print(f"Dataset statistics: {stats}")
    
    return flattened_dataset

# Usage examples
if __name__ == "__main__":
    # Create and process custom dataset
    processed_data = dataset_operations()
    
    # Create train/val/test splits
    splits = create_splits()
    
    # Advanced features
    advanced_data = advanced_dataset_features()
```

### 7. How do you implement custom models using Hugging Face transformers?
**Answer:** Create custom transformer architectures by extending base classes.

```python
import torch
import torch.nn as nn
from transformers import (
    PreTrainedModel, PretrainedConfig,
    BertModel, BertConfig, BertPreTrainedModel
)
from transformers.modeling_outputs import SequenceClassifierOutput

# Custom configuration
class CustomBertConfig(BertConfig):
    def __init__(
        self,
        num_labels=2,
        dropout_rate=0.1,
        use_custom_head=True,
        custom_head_size=256,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.num_labels = num_labels
        self.dropout_rate = dropout_rate
        self.use_custom_head = use_custom_head
        self.custom_head_size = custom_head_size

# Custom model for sequence classification
class CustomBertForSequenceClassification(BertPreTrainedModel):
    config_class = CustomBertConfig
    
    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels
        self.config = config
        
        # BERT backbone
        self.bert = BertModel(config)
        
        # Custom classification head
        if config.use_custom_head:
            self.classifier = nn.Sequential(
                nn.Linear(config.hidden_size, config.custom_head_size),
                nn.ReLU(),
                nn.Dropout(config.dropout_rate),
                nn.Linear(config.custom_head_size, config.custom_head_size // 2),
                nn.ReLU(),
                nn.Dropout(config.dropout_rate),
                nn.Linear(config.custom_head_size // 2, config.num_labels)
            )
        else:
            self.classifier = nn.Linear(config.hidden_size, config.num_labels)
        
        # Initialize weights
        self.init_weights()
    
    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        labels=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict
        
        # BERT forward pass
        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        
        # Get pooled output
        pooled_output = outputs[1]  # [CLS] token representation
        
        # Classification
        logits = self.classifier(pooled_output)
        
        loss = None
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
        
        if not return_dict:
            output = (logits,) + outputs[2:]
            return ((loss,) + output) if loss is not None else output
        
        return SequenceClassifierOutput(
            loss=loss,
            logits=logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )

# Multi-task model
class MultiTaskBertModel(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        
        self.bert = BertModel(config)
        
        # Multiple task heads
        self.sentiment_classifier = nn.Linear(config.hidden_size, 3)  # pos/neg/neutral
        self.emotion_classifier = nn.Linear(config.hidden_size, 6)    # 6 emotions
        self.ner_classifier = nn.Linear(config.hidden_size, 9)        # NER tags
        
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.init_weights()
    
    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        token_type_ids=None,
        labels_sentiment=None,
        labels_emotion=None,
        labels_ner=None,
        task_type="sentiment",
        **kwargs
    ):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            **kwargs
        )
        
        if task_type == "sentiment":
            pooled_output = self.dropout(outputs[1])
            logits = self.sentiment_classifier(pooled_output)
            
            loss = None
            if labels_sentiment is not None:
                loss_fct = nn.CrossEntropyLoss()
                loss = loss_fct(logits, labels_sentiment)
                
        elif task_type == "emotion":
            pooled_output = self.dropout(outputs[1])
            logits = self.emotion_classifier(pooled_output)
            
            loss = None
            if labels_emotion is not None:
                loss_fct = nn.CrossEntropyLoss()
                loss = loss_fct(logits, labels_emotion)
                
        elif task_type == "ner":
            sequence_output = self.dropout(outputs[0])
            logits = self.ner_classifier(sequence_output)
            
            loss = None
            if labels_ner is not None:
                loss_fct = nn.CrossEntropyLoss()
                loss = loss_fct(logits.view(-1, 9), labels_ner.view(-1))
        
        return SequenceClassifierOutput(loss=loss, logits=logits)

# Custom attention mechanism
class CustomAttentionModel(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        
        self.bert = BertModel(config)
        self.attention_weights = nn.Linear(config.hidden_size, 1)
        self.classifier = nn.Linear(config.hidden_size, config.num_labels)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        
        self.init_weights()
    
    def forward(self, input_ids=None, attention_mask=None, labels=None, **kwargs):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            **kwargs
        )
        
        # Get all hidden states
        sequence_output = outputs[0]  # (batch_size, seq_len, hidden_size)
        
        # Compute attention weights
        attention_scores = self.attention_weights(sequence_output)  # (batch_size, seq_len, 1)
        attention_scores = attention_scores.squeeze(-1)  # (batch_size, seq_len)
        
        # Apply attention mask
        if attention_mask is not None:
            attention_scores = attention_scores.masked_fill(
                attention_mask == 0, -1e9
            )
        
        # Softmax to get attention weights
        attention_weights = torch.softmax(attention_scores, dim=-1)  # (batch_size, seq_len)
        
        # Weighted sum of hidden states
        weighted_output = torch.sum(
            sequence_output * attention_weights.unsqueeze(-1), 
            dim=1
        )  # (batch_size, hidden_size)
        
        # Classification
        pooled_output = self.dropout(weighted_output)
        logits = self.classifier(pooled_output)
        
        loss = None
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits, labels)
        
        return SequenceClassifierOutput(
            loss=loss,
            logits=logits,
            attentions=attention_weights
        )

# Usage and training
def train_custom_model():
    # Initialize custom configuration
    config = CustomBertConfig(
        num_labels=3,
        dropout_rate=0.2,
        use_custom_head=True,
        custom_head_size=256
    )
    
    # Initialize model
    model = CustomBertForSequenceClassification(config)
    
    # Load pre-trained weights (optional)
    # model = CustomBertForSequenceClassification.from_pretrained(
    #     "bert-base-uncased",
    #     config=config
    # )
    
    # Training setup
    from transformers import AutoTokenizer, TrainingArguments, Trainer
    
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    
    # Sample training data
    train_texts = ["This is great!", "This is bad!", "This is okay."]
    train_labels = [2, 0, 1]  # positive, negative, neutral
    
    # Tokenize data
    train_encodings = tokenizer(
        train_texts,
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors="pt"
    )
    
    # Create dataset
    class CustomDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels
        
        def __getitem__(self, idx):
            item = {key: val[idx] for key, val in self.encodings.items()}
            item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
            return item
        
        def __len__(self):
            return len(self.labels)
    
    train_dataset = CustomDataset(train_encodings, train_labels)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir='./custom_model_results',
        num_train_epochs=3,
        per_device_train_batch_size=16,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
    )
    
    # Train
    trainer.train()
    
    # Save model
    model.save_pretrained("./custom_bert_model")
    tokenizer.save_pretrained("./custom_bert_model")
    
    return model, tokenizer

# Load and use custom model
def use_custom_model():
    # Load custom model
    model = CustomBertForSequenceClassification.from_pretrained("./custom_bert_model")
    tokenizer = AutoTokenizer.from_pretrained("./custom_bert_model")
    
    # Inference
    text = "This product is amazing!"
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(predictions, dim=-1)
    
    labels = ["negative", "neutral", "positive"]
    print(f"Text: {text}")
    print(f"Predicted class: {labels[predicted_class.item()]}")
    print(f"Confidence: {predictions[0][predicted_class].item():.4f}")

if __name__ == "__main__":
    # Train custom model
    model, tokenizer = train_custom_model()
    
    # Use custom model
    use_custom_model()
```

This comprehensive Hugging Face interview questions set covers fundamental concepts through advanced custom implementations, providing practical examples for transformers, fine-tuning, datasets, and custom model architectures.
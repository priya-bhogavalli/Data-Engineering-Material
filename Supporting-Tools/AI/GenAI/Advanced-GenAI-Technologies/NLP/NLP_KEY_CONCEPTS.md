# 📝 Natural Language Processing (NLP) - Key Concepts

## 🎯 **Real-World Analogy: The Language Understanding Expert**

> **Think of NLP as a highly skilled linguist who can read, understand, and analyze text in multiple languages, extract meaning, sentiment, and key information, then transform it into structured data that computers can work with.**

## 🔥 **Core NLP Concepts**

### 1. **Text Preprocessing** 🧹

```python
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
    
    def clean_text(self, text):
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords
        tokens = [token for token in tokens if token not in self.stop_words]
        
        # Lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return ' '.join(tokens)

# Example usage
preprocessor = TextPreprocessor()
raw_text = "The customers are really unhappy with the service quality!"
clean_text = preprocessor.clean_text(raw_text)
print(f"Original: {raw_text}")
print(f"Cleaned: {clean_text}")
# Output: customer really unhappy service quality
```

### 2. **Named Entity Recognition (NER)** 🏷️

```python
import spacy

# Load pre-trained model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    
    entities = {}
    for ent in doc.ents:
        entity_type = ent.label_
        entity_text = ent.text
        
        if entity_type not in entities:
            entities[entity_type] = []
        entities[entity_type].append(entity_text)
    
    return entities

# Example
text = "Apple Inc. was founded by Steve Jobs in Cupertino, California on April 1, 1976."
entities = extract_entities(text)

for entity_type, values in entities.items():
    print(f"{entity_type}: {values}")

# Output:
# ORG: ['Apple Inc.']
# PERSON: ['Steve Jobs']
# GPE: ['Cupertino', 'California']
# DATE: ['April 1, 1976']
```

### 3. **Sentiment Analysis** 😊😐😞

```python
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

class SentimentAnalyzer:
    def __init__(self):
        # Load pre-trained sentiment model
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
    
    def analyze_sentiment(self, text):
        result = self.sentiment_pipeline(text)[0]
        
        # Convert to standardized format
        label_mapping = {
            'LABEL_0': 'negative',
            'LABEL_1': 'neutral', 
            'LABEL_2': 'positive'
        }
        
        sentiment = label_mapping.get(result['label'], result['label'].lower())
        confidence = result['score']
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'raw_result': result
        }
    
    def batch_analyze(self, texts):
        results = []
        for text in texts:
            results.append(self.analyze_sentiment(text))
        return results

# Example usage
analyzer = SentimentAnalyzer()

reviews = [
    "This product is amazing! I love it.",
    "The service was okay, nothing special.",
    "Terrible experience, would not recommend."
]

for review in reviews:
    result = analyzer.analyze_sentiment(review)
    print(f"Text: {review}")
    print(f"Sentiment: {result['sentiment']} (confidence: {result['confidence']:.2f})")
    print()
```

### 4. **Text Classification** 📊

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

class TextClassifier:
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=10000, stop_words='english')),
            ('classifier', MultinomialNB())
        ])
        self.is_trained = False
    
    def train(self, texts, labels):
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42
        )
        
        self.pipeline.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate
        accuracy = self.pipeline.score(X_test, y_test)
        return accuracy
    
    def predict(self, texts):
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        predictions = self.pipeline.predict(texts)
        probabilities = self.pipeline.predict_proba(texts)
        
        return predictions, probabilities
    
    def predict_single(self, text):
        predictions, probabilities = self.predict([text])
        return predictions[0], probabilities[0]

# Example: Email classification
emails = [
    "Congratulations! You've won $1000000! Click here now!",  # spam
    "Meeting scheduled for tomorrow at 2 PM in conference room A",  # work
    "Your order has been shipped and will arrive tomorrow",  # personal
    "URGENT: Your account will be closed unless you verify now!"  # spam
]

labels = ['spam', 'work', 'personal', 'spam']

classifier = TextClassifier()
accuracy = classifier.train(emails, labels)
print(f"Training accuracy: {accuracy:.2f}")

# Test prediction
new_email = "Please review the attached document for our meeting"
prediction, probability = classifier.predict_single(new_email)
print(f"Email: {new_email}")
print(f"Predicted category: {prediction}")
```

### 5. **Text Summarization** 📄

```python
from transformers import pipeline

class TextSummarizer:
    def __init__(self):
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )
    
    def summarize(self, text, max_length=150, min_length=50):
        # Split long text into chunks if needed
        max_chunk_length = 1024  # BART's max input length
        
        if len(text) <= max_chunk_length:
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )[0]['summary_text']
        else:
            # Handle long documents
            chunks = self.split_text(text, max_chunk_length)
            summaries = []
            
            for chunk in chunks:
                chunk_summary = self.summarizer(
                    chunk,
                    max_length=max_length//len(chunks),
                    min_length=min_length//len(chunks),
                    do_sample=False
                )[0]['summary_text']
                summaries.append(chunk_summary)
            
            # Combine and summarize again
            combined = ' '.join(summaries)
            summary = self.summarizer(
                combined,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )[0]['summary_text']
        
        return summary
    
    def split_text(self, text, max_length):
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_chunk.append(word)
                current_length += len(word) + 1
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

# Example usage
summarizer = TextSummarizer()

long_article = """
Artificial Intelligence has revolutionized many industries in recent years. 
From healthcare to finance, AI applications are transforming how businesses operate. 
Machine learning algorithms can now process vast amounts of data to identify patterns 
and make predictions with unprecedented accuracy. Natural language processing enables 
computers to understand and generate human language, while computer vision allows 
machines to interpret visual information. The impact of AI extends beyond business 
applications to scientific research, where it accelerates discovery and innovation. 
However, the rapid advancement of AI also raises important ethical considerations 
about privacy, bias, and the future of work. As AI continues to evolve, society 
must carefully balance the benefits of this technology with its potential risks.
"""

summary = summarizer.summarize(long_article)
print("Original length:", len(long_article.split()))
print("Summary length:", len(summary.split()))
print("\nSummary:", summary)
```

## 🚀 **Advanced NLP Techniques**

### **Topic Modeling** 🎯

```python
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

class TopicModeler:
    def __init__(self, n_topics=5):
        self.n_topics = n_topics
        self.vectorizer = CountVectorizer(
            max_features=1000,
            stop_words='english',
            min_df=2,
            max_df=0.8
        )
        self.lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42
        )
    
    def fit_transform(self, documents):
        # Convert documents to term-document matrix
        doc_term_matrix = self.vectorizer.fit_transform(documents)
        
        # Fit LDA model
        self.lda.fit(doc_term_matrix)
        
        # Transform documents to topic space
        doc_topic_matrix = self.lda.transform(doc_term_matrix)
        
        return doc_topic_matrix
    
    def get_topics(self, n_words=10):
        feature_names = self.vectorizer.get_feature_names_out()
        topics = []
        
        for topic_idx, topic in enumerate(self.lda.components_):
            top_words_idx = topic.argsort()[-n_words:][::-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topics.append({
                'topic_id': topic_idx,
                'words': top_words,
                'weights': topic[top_words_idx]
            })
        
        return topics
    
    def predict_topic(self, document):
        doc_vector = self.vectorizer.transform([document])
        topic_probs = self.lda.transform(doc_vector)[0]
        
        dominant_topic = np.argmax(topic_probs)
        confidence = topic_probs[dominant_topic]
        
        return dominant_topic, confidence, topic_probs

# Example usage
documents = [
    "Machine learning algorithms are transforming healthcare diagnostics",
    "Stock market analysis using artificial intelligence shows promising results",
    "Natural language processing helps in customer service automation",
    "Computer vision applications in autonomous vehicles are advancing rapidly",
    "Financial fraud detection systems use advanced AI techniques"
]

topic_modeler = TopicModeler(n_topics=3)
doc_topics = topic_modeler.fit_transform(documents)

print("Discovered Topics:")
topics = topic_modeler.get_topics(n_words=5)
for topic in topics:
    print(f"Topic {topic['topic_id']}: {', '.join(topic['words'])}")
```

### **Text Similarity and Clustering** 🔍

```python
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TextSimilarityAnalyzer:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def encode_texts(self, texts):
        return self.model.encode(texts)
    
    def calculate_similarity(self, text1, text2):
        embeddings = self.encode_texts([text1, text2])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return similarity
    
    def find_similar_texts(self, query, text_corpus, top_k=5):
        query_embedding = self.encode_texts([query])
        corpus_embeddings = self.encode_texts(text_corpus)
        
        similarities = cosine_similarity(query_embedding, corpus_embeddings)[0]
        
        # Get top-k most similar texts
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                'text': text_corpus[idx],
                'similarity': similarities[idx],
                'index': idx
            })
        
        return results
    
    def cluster_texts(self, texts, n_clusters=3):
        embeddings = self.encode_texts(texts)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(embeddings)
        
        # Group texts by cluster
        clusters = {}
        for i, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append({
                'text': texts[i],
                'index': i
            })
        
        return clusters, cluster_labels

# Example usage
analyzer = TextSimilarityAnalyzer()

# Text similarity
text1 = "Machine learning is a subset of artificial intelligence"
text2 = "AI includes machine learning as one of its components"
similarity = analyzer.calculate_similarity(text1, text2)
print(f"Similarity: {similarity:.3f}")

# Find similar documents
query = "artificial intelligence applications"
corpus = [
    "Machine learning algorithms for data analysis",
    "AI applications in healthcare and medicine", 
    "Natural language processing techniques",
    "Computer vision for image recognition",
    "Artificial intelligence in business automation"
]

similar_texts = analyzer.find_similar_texts(query, corpus, top_k=3)
print("\nMost similar texts:")
for result in similar_texts:
    print(f"Similarity: {result['similarity']:.3f} - {result['text']}")
```
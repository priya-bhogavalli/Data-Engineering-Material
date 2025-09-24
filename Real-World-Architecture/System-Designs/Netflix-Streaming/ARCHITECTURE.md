# 🎬 Netflix-Style Streaming Platform Architecture

> **Complete system design for a global video streaming platform serving 200M+ users**

## 📊 **System Scale & Requirements**

### **Scale Metrics**
- **Users**: 200M+ global subscribers
- **Content**: 15K+ movies, 5K+ TV series
- **Streaming**: 1B+ hours watched daily
- **Peak Traffic**: 15M concurrent streams
- **Global Reach**: 190+ countries
- **Data Volume**: 500TB+ daily

### **Core Services Architecture**

#### **User Management Service**
```python
from cassandra.cluster import Cluster
import redis
import jwt

class UserService:
    def __init__(self):
        self.cassandra = Cluster(['cassandra-node1', 'cassandra-node2'])
        self.session = self.cassandra.connect('netflix')
        self.redis = redis.Redis(host='redis-cluster')
    
    def authenticate_user(self, email, password):
        user = self.session.execute(
            "SELECT user_id, password_hash FROM users WHERE email = ?",
            [email]
        ).one()
        
        if user and self.verify_password(password, user.password_hash):
            token = jwt.encode({
                'user_id': user.user_id,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, 'secret_key')
            
            self.redis.setex(f"session:{user.user_id}", 86400, token)
            return {'token': token, 'user_id': user.user_id}
        
        return None
```

#### **Recommendation Engine**
```python
class RecommendationService:
    def __init__(self):
        self.spark = SparkSession.builder.appName("Netflix-Recommendations").getOrCreate()
        self.redis = redis.Redis(host='redis-cluster')
    
    def generate_recommendations(self, user_id, num_recommendations=20):
        cached_recs = self.redis.get(f"recommendations:{user_id}")
        if cached_recs:
            return json.loads(cached_recs)
        
        # Collaborative filtering using Spark MLlib
        from pyspark.ml.recommendation import ALS
        
        interactions_df = self.spark.read \
            .format("org.apache.spark.sql.cassandra") \
            .options(table="user_interactions", keyspace="netflix") \
            .load()
        
        als = ALS(
            maxIter=10,
            regParam=0.1,
            userCol="user_id",
            itemCol="content_id",
            ratingCol="rating"
        )
        
        model = als.fit(interactions_df)
        user_df = self.spark.createDataFrame([(user_id,)], ["user_id"])
        recommendations = model.recommendForUserSubset(user_df, 50)
        
        # Cache for 2 hours
        self.redis.setex(f"recommendations:{user_id}", 7200, 
                        json.dumps(recommendations.collect()[0]['recommendations']))
        
        return recommendations.collect()[0]['recommendations']
```

### **Database Schema**

#### **Cassandra (User Data)**
```sql
CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY,
    email TEXT,
    subscription_type TEXT,
    preferences MAP<TEXT, TEXT>,
    created_at TIMESTAMP
);

CREATE TABLE viewing_history (
    user_id UUID,
    content_id UUID,
    watched_at TIMESTAMP,
    watch_duration INT,
    completion_percentage FLOAT,
    PRIMARY KEY (user_id, watched_at)
) WITH CLUSTERING ORDER BY (watched_at DESC);
```

#### **MySQL (Content Metadata)**
```sql
CREATE TABLE content (
    content_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    genre VARCHAR(100),
    duration INT,
    release_date DATE,
    content_type ENUM('movie', 'series', 'documentary'),
    INDEX idx_genre (genre)
);
```

### **Performance Metrics**
- **Video Start Time**: <2 seconds (95th percentile)
- **API Response Time**: <100ms (99th percentile)
- **Concurrent Streams**: 15M+ peak capacity
- **Global Availability**: 99.99% uptime

### **Cost Structure (Monthly)**
- **Compute**: $2.5M
- **Storage**: $1.8M
- **CDN**: $3.2M
- **Databases**: $800K
- **Total**: ~$10M/month

---

**🎯 This architecture handles Netflix-scale streaming with microservices, real-time recommendations, and global CDN distribution.**
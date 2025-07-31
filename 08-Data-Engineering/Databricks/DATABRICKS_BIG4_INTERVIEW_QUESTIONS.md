# Databricks Interview Questions - Big4 Companies

## Google Interview Questions

### 1. Design a real-time analytics platform using Databricks for YouTube data
**Answer:**
```python
# Architecture: Kafka -> Databricks Streaming -> Delta Lake -> Analytics

# Stream processing setup
def setup_youtube_analytics():
    # Read from Kafka
    streaming_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "youtube-events") \
        .load()
    
    # Parse YouTube events
    from pyspark.sql.types import *
    schema = StructType([
        StructField("video_id", StringType()),
        StructField("user_id", StringType()),
        StructField("event_type", StringType()),
        StructField("timestamp", TimestampType()),
        StructField("duration_watched", IntegerType()),
        StructField("device_type", StringType())
    ])
    
    parsed_df = streaming_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # Real-time aggregations
    windowed_metrics = parsed_df \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy(
            window(col("timestamp"), "5 minutes"),
            col("video_id"),
            col("event_type")
        ).agg(
            count("*").alias("event_count"),
            countDistinct("user_id").alias("unique_viewers"),
            avg("duration_watched").alias("avg_watch_time")
        )
    
    # Write to Delta Lake
    query = windowed_metrics.writeStream \
        .format("delta") \
        .outputMode("update") \
        .option("checkpointLocation", "/delta/checkpoints/youtube") \
        .trigger(processingTime="30 seconds") \
        .start("/delta/youtube/real_time_metrics")
    
    return query

# ML-based content recommendation
def build_recommendation_engine():
    from databricks.feature_store import FeatureStoreClient
    
    fs = FeatureStoreClient()
    
    # Create user features
    user_features = spark.sql("""
        SELECT 
            user_id,
            COUNT(DISTINCT video_id) as videos_watched,
            AVG(duration_watched) as avg_watch_duration,
            COUNT(DISTINCT category) as category_diversity,
            MAX(timestamp) as last_activity
        FROM youtube_events
        WHERE timestamp >= current_timestamp() - INTERVAL 30 DAYS
        GROUP BY user_id
    """)
    
    # Store in feature store
    fs.create_table(
        name="youtube.user_features",
        primary_keys=["user_id"],
        df=user_features
    )
    
    return user_features
```

### 2. Implement distributed data processing for Google Search logs
**Answer:**
```python
def process_search_logs():
    # Read massive search log files
    search_logs = spark.read.format("json") \
        .option("multiline", "false") \
        .load("/mnt/google-search-logs/")
    
    # Optimize for large-scale processing
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
    
    # Process search patterns
    search_analysis = search_logs.select(
        col("query"),
        col("user_id"),
        col("timestamp"),
        col("results_clicked"),
        col("session_id")
    ).filter(
        col("query").isNotNull() & 
        (length(col("query")) > 2)
    )
    
    # Generate search insights
    search_insights = search_analysis.groupBy(
        window(col("timestamp"), "1 hour"),
        col("query")
    ).agg(
        count("*").alias("search_frequency"),
        countDistinct("user_id").alias("unique_users"),
        avg(size(col("results_clicked"))).alias("avg_clicks")
    )
    
    # Partition by hour for efficient querying
    search_insights.write \
        .format("delta") \
        .partitionBy("window") \
        .mode("overwrite") \
        .save("/delta/search/hourly_insights")
    
    return search_insights
```

## Amazon Interview Questions

### 3. Design a data lake architecture for Amazon's product catalog
**Answer:**
```python
def amazon_product_catalog_pipeline():
    # Bronze Layer - Raw product data ingestion
    def ingest_product_data():
        # Multiple data sources
        sources = {
            "inventory": "/mnt/s3/inventory/",
            "pricing": "/mnt/s3/pricing/",
            "reviews": "/mnt/s3/reviews/",
            "vendor_data": "/mnt/s3/vendors/"
        }
        
        bronze_tables = {}
        for source_name, path in sources.items():
            df = spark.read.format("json").load(path)
            
            # Add metadata
            bronze_df = df.withColumn("ingestion_time", current_timestamp()) \
                         .withColumn("source_system", lit(source_name)) \
                         .withColumn("file_path", input_file_name())
            
            # Write to bronze layer
            bronze_df.write.format("delta") \
                .mode("append") \
                .save(f"/delta/bronze/{source_name}")
            
            bronze_tables[source_name] = bronze_df
        
        return bronze_tables
    
    # Silver Layer - Data quality and standardization
    def create_silver_layer():
        # Product master data
        inventory_df = spark.read.format("delta").load("/delta/bronze/inventory")
        pricing_df = spark.read.format("delta").load("/delta/bronze/pricing")
        
        # Data quality checks
        clean_inventory = inventory_df.filter(
            col("product_id").isNotNull() &
            col("category").isNotNull() &
            (col("stock_quantity") >= 0)
        ).dropDuplicates(["product_id"])
        
        # Join and enrich
        product_master = clean_inventory.alias("inv").join(
            pricing_df.alias("price"),
            col("inv.product_id") == col("price.product_id"),
            "left"
        ).select(
            col("inv.product_id"),
            col("inv.product_name"),
            col("inv.category"),
            col("inv.stock_quantity"),
            col("price.current_price"),
            col("price.discount_percent"),
            when(col("price.current_price").isNull(), 0)
                .otherwise(col("price.current_price")).alias("final_price")
        )
        
        # Write to silver layer
        product_master.write.format("delta") \
            .mode("overwrite") \
            .save("/delta/silver/product_master")
        
        return product_master
    
    # Gold Layer - Business aggregations
    def create_gold_layer():
        product_master = spark.read.format("delta").load("/delta/silver/product_master")
        reviews_df = spark.read.format("delta").load("/delta/bronze/reviews")
        
        # Category performance metrics
        category_metrics = product_master.alias("pm").join(
            reviews_df.alias("rev"),
            col("pm.product_id") == col("rev.product_id"),
            "left"
        ).groupBy("category").agg(
            count("pm.product_id").alias("total_products"),
            sum("stock_quantity").alias("total_inventory"),
            avg("final_price").alias("avg_price"),
            avg("rev.rating").alias("avg_rating"),
            count("rev.review_id").alias("total_reviews")
        )
        
        category_metrics.write.format("delta") \
            .mode("overwrite") \
            .save("/delta/gold/category_performance")
        
        return category_metrics
    
    # Execute pipeline
    bronze_data = ingest_product_data()
    silver_data = create_silver_layer()
    gold_data = create_gold_layer()
    
    return gold_data
```

### 4. Implement real-time inventory management system
**Answer:**
```python
def real_time_inventory_system():
    # Stream processing for inventory updates
    def process_inventory_stream():
        # Read from Kinesis
        inventory_stream = spark.readStream \
            .format("kinesis") \
            .option("streamName", "inventory-updates") \
            .option("region", "us-east-1") \
            .option("initialPosition", "TRIM_HORIZON") \
            .load()
        
        # Parse inventory events
        inventory_events = inventory_stream.select(
            from_json(col("data").cast("string"), inventory_schema).alias("event")
        ).select("event.*")
        
        # Apply business logic
        processed_events = inventory_events.withColumn(
            "alert_level",
            when(col("stock_quantity") < col("reorder_point"), "LOW_STOCK")
            .when(col("stock_quantity") == 0, "OUT_OF_STOCK")
            .otherwise("NORMAL")
        )
        
        # Update inventory table
        def update_inventory(batch_df, batch_id):
            from delta.tables import DeltaTable
            
            inventory_table = DeltaTable.forPath(spark, "/delta/inventory/current")
            
            inventory_table.alias("inventory").merge(
                batch_df.alias("updates"),
                "inventory.product_id = updates.product_id AND inventory.warehouse_id = updates.warehouse_id"
            ).whenMatchedUpdate(set={
                "stock_quantity": "updates.stock_quantity",
                "last_updated": "updates.timestamp",
                "alert_level": "updates.alert_level"
            }).whenNotMatchedInsert(values={
                "product_id": "updates.product_id",
                "warehouse_id": "updates.warehouse_id",
                "stock_quantity": "updates.stock_quantity",
                "alert_level": "updates.alert_level",
                "last_updated": "updates.timestamp"
            }).execute()
        
        # Write stream with custom logic
        query = processed_events.writeStream \
            .foreachBatch(update_inventory) \
            .option("checkpointLocation", "/delta/checkpoints/inventory") \
            .trigger(processingTime="10 seconds") \
            .start()
        
        return query
    
    # Alert system for low stock
    def generate_stock_alerts():
        current_inventory = spark.read.format("delta").load("/delta/inventory/current")
        
        alerts = current_inventory.filter(
            col("alert_level").isin(["LOW_STOCK", "OUT_OF_STOCK"])
        ).select(
            col("product_id"),
            col("warehouse_id"),
            col("stock_quantity"),
            col("alert_level"),
            current_timestamp().alias("alert_timestamp")
        )
        
        # Send to notification system
        alerts.write.format("delta") \
            .mode("append") \
            .save("/delta/alerts/inventory_alerts")
        
        return alerts
    
    return process_inventory_stream(), generate_stock_alerts()
```

## Microsoft Interview Questions

### 5. Design a data platform for Microsoft Teams analytics
**Answer:**
```python
def teams_analytics_platform():
    # Process Teams meeting data
    def analyze_meeting_patterns():
        meetings_df = spark.read.format("delta").load("/delta/teams/meetings")
        participants_df = spark.read.format("delta").load("/delta/teams/participants")
        
        # Meeting effectiveness metrics
        meeting_metrics = meetings_df.alias("m").join(
            participants_df.alias("p"),
            col("m.meeting_id") == col("p.meeting_id")
        ).groupBy(
            col("m.meeting_id"),
            col("m.organizer_id"),
            col("m.scheduled_duration"),
            col("m.meeting_type")
        ).agg(
            count("p.participant_id").alias("invited_count"),
            countDistinct(
                when(col("p.joined_time").isNotNull(), col("p.participant_id"))
            ).alias("actual_attendees"),
            avg("p.attendance_duration").alias("avg_attendance_duration"),
            max("p.attendance_duration").alias("max_attendance_duration")
        ).withColumn(
            "attendance_rate",
            col("actual_attendees") / col("invited_count")
        ).withColumn(
            "engagement_score",
            col("avg_attendance_duration") / col("scheduled_duration")
        )
        
        # Identify meeting patterns
        meeting_insights = meeting_metrics.withColumn(
            "effectiveness_category",
            when(col("attendance_rate") > 0.8 & col("engagement_score") > 0.7, "High")
            .when(col("attendance_rate") > 0.6 & col("engagement_score") > 0.5, "Medium")
            .otherwise("Low")
        )
        
        meeting_insights.write.format("delta") \
            .mode("overwrite") \
            .save("/delta/teams/meeting_effectiveness")
        
        return meeting_insights
    
    # User productivity analysis
    def analyze_user_productivity():
        # Combine multiple data sources
        messages_df = spark.read.format("delta").load("/delta/teams/messages")
        calls_df = spark.read.format("delta").load("/delta/teams/calls")
        files_df = spark.read.format("delta").load("/delta/teams/files")
        
        # User activity metrics
        user_productivity = messages_df.groupBy("user_id", "date").agg(
            count("message_id").alias("messages_sent"),
            countDistinct("channel_id").alias("channels_active")
        ).alias("msg").join(
            calls_df.groupBy("user_id", "date").agg(
                count("call_id").alias("calls_made"),
                sum("duration_minutes").alias("total_call_time")
            ).alias("calls"),
            ["user_id", "date"],
            "full"
        ).join(
            files_df.groupBy("user_id", "date").agg(
                count("file_id").alias("files_shared")
            ).alias("files"),
            ["user_id", "date"],
            "full"
        ).fillna(0)
        
        # Calculate productivity score
        productivity_scored = user_productivity.withColumn(
            "productivity_score",
            (col("messages_sent") * 0.2 +
             col("channels_active") * 0.3 +
             col("calls_made") * 0.3 +
             col("files_shared") * 0.2)
        )
        
        productivity_scored.write.format("delta") \
            .partitionBy("date") \
            .mode("overwrite") \
            .save("/delta/teams/user_productivity")
        
        return productivity_scored
    
    return analyze_meeting_patterns(), analyze_user_productivity()
```

### 6. Implement Azure integration with Databricks
**Answer:**
```python
def azure_databricks_integration():
    # Azure Data Lake integration
    def setup_adls_integration():
        # Service principal authentication
        spark.conf.set("fs.azure.account.auth.type.storage.dfs.core.windows.net", "OAuth")
        spark.conf.set("fs.azure.account.oauth.provider.type.storage.dfs.core.windows.net", 
                      "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
        spark.conf.set("fs.azure.account.oauth2.client.id.storage.dfs.core.windows.net", 
                      dbutils.secrets.get("azure", "client-id"))
        spark.conf.set("fs.azure.account.oauth2.client.secret.storage.dfs.core.windows.net", 
                      dbutils.secrets.get("azure", "client-secret"))
        spark.conf.set("fs.azure.account.oauth2.client.endpoint.storage.dfs.core.windows.net", 
                      "https://login.microsoftonline.com/tenant-id/oauth2/token")
        
        # Read from ADLS
        adls_df = spark.read.format("parquet") \
            .load("abfss://container@storage.dfs.core.windows.net/data/")
        
        return adls_df
    
    # Azure SQL Database integration
    def integrate_azure_sql():
        # Connection properties
        jdbc_url = "jdbc:sqlserver://server.database.windows.net:1433;database=analytics"
        connection_properties = {
            "user": dbutils.secrets.get("azure", "sql-user"),
            "password": dbutils.secrets.get("azure", "sql-password"),
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
        
        # Read from Azure SQL
        sql_df = spark.read.jdbc(jdbc_url, "dbo.sales_data", properties=connection_properties)
        
        # Process and write back
        processed_df = sql_df.groupBy("region", "product_category").agg(
            sum("sales_amount").alias("total_sales"),
            count("order_id").alias("order_count")
        )
        
        # Write back to Azure SQL
        processed_df.write.jdbc(
            jdbc_url, 
            "dbo.sales_summary", 
            mode="overwrite", 
            properties=connection_properties
        )
        
        return processed_df
    
    # Azure Event Hubs streaming
    def process_event_hubs_stream():
        # Event Hubs configuration
        connectionString = dbutils.secrets.get("azure", "eventhubs-connection")
        ehConf = {
            'eventhubs.connectionString': connectionString,
            'eventhubs.consumerGroup': 'databricks-consumer'
        }
        
        # Read stream
        stream_df = spark.readStream \
            .format("eventhubs") \
            .options(**ehConf) \
            .load()
        
        # Parse events
        parsed_df = stream_df.select(
            col("body").cast("string").alias("json_data"),
            col("enqueuedTime").alias("event_time")
        ).select(
            from_json(col("json_data"), event_schema).alias("data"),
            col("event_time")
        ).select("data.*", "event_time")
        
        # Write to Delta Lake
        query = parsed_df.writeStream \
            .format("delta") \
            .outputMode("append") \
            .option("checkpointLocation", "/delta/checkpoints/eventhubs") \
            .start("/delta/streaming/events")
        
        return query
    
    return setup_adls_integration(), integrate_azure_sql(), process_event_hubs_stream()
```

## Meta Interview Questions

### 7. Design a social media analytics platform using Databricks
**Answer:**
```python
def social_media_analytics():
    # Process user engagement data
    def analyze_user_engagement():
        # Read social media events
        events_df = spark.read.format("delta").load("/delta/social/events")
        
        # Calculate engagement metrics
        user_engagement = events_df.groupBy("user_id", "date").agg(
            count(when(col("event_type") == "like", 1)).alias("likes_given"),
            count(when(col("event_type") == "comment", 1)).alias("comments_made"),
            count(when(col("event_type") == "share", 1)).alias("shares_made"),
            count(when(col("event_type") == "post", 1)).alias("posts_created"),
            countDistinct("session_id").alias("sessions"),
            sum("time_spent_seconds").alias("total_time_spent")
        )
        
        # Engagement scoring
        engagement_scored = user_engagement.withColumn(
            "engagement_score",
            (col("likes_given") * 1 +
             col("comments_made") * 3 +
             col("shares_made") * 5 +
             col("posts_created") * 10) / 
            greatest(col("sessions"), lit(1))
        ).withColumn(
            "user_segment",
            when(col("engagement_score") > 50, "Power User")
            .when(col("engagement_score") > 20, "Active User")
            .when(col("engagement_score") > 5, "Casual User")
            .otherwise("Inactive User")
        )
        
        engagement_scored.write.format("delta") \
            .partitionBy("date") \
            .mode("overwrite") \
            .save("/delta/social/user_engagement")
        
        return engagement_scored
    
    # Content virality prediction
    def predict_viral_content():
        posts_df = spark.read.format("delta").load("/delta/social/posts")
        interactions_df = spark.read.format("delta").load("/delta/social/interactions")
        
        # Feature engineering for virality
        post_features = posts_df.alias("p").join(
            interactions_df.alias("i"),
            col("p.post_id") == col("i.post_id")
        ).groupBy(
            col("p.post_id"),
            col("p.author_id"),
            col("p.post_type"),
            col("p.created_time"),
            col("p.content_length")
        ).agg(
            count("i.interaction_id").alias("total_interactions"),
            count(when(col("i.interaction_type") == "like", 1)).alias("likes"),
            count(when(col("i.interaction_type") == "share", 1)).alias("shares"),
            count(when(col("i.interaction_type") == "comment", 1)).alias("comments"),
            countDistinct("i.user_id").alias("unique_users")
        )
        
        # Calculate virality metrics
        viral_features = post_features.withColumn(
            "hours_since_post",
            (unix_timestamp(current_timestamp()) - unix_timestamp(col("created_time"))) / 3600
        ).withColumn(
            "interaction_rate",
            col("total_interactions") / greatest(col("hours_since_post"), lit(1))
        ).withColumn(
            "share_rate",
            col("shares") / greatest(col("total_interactions"), lit(1))
        ).withColumn(
            "virality_score",
            col("interaction_rate") * col("share_rate") * log(col("unique_users") + 1)
        )
        
        # Identify viral content
        viral_content = viral_features.filter(col("virality_score") > 10)
        
        viral_content.write.format("delta") \
            .mode("overwrite") \
            .save("/delta/social/viral_content")
        
        return viral_content
    
    # Real-time content moderation
    def content_moderation_pipeline():
        # Stream processing for new posts
        posts_stream = spark.readStream \
            .format("delta") \
            .load("/delta/social/posts_stream")
        
        # Content analysis (simplified)
        def analyze_content(batch_df, batch_id):
            # Toxicity detection (placeholder for ML model)
            analyzed_df = batch_df.withColumn(
                "toxicity_score",
                when(col("content").rlike("(?i)(hate|spam|abuse)"), 0.8)
                .otherwise(0.1)
            ).withColumn(
                "moderation_action",
                when(col("toxicity_score") > 0.7, "BLOCK")
                .when(col("toxicity_score") > 0.4, "REVIEW")
                .otherwise("APPROVE")
            )
            
            # Write moderation results
            analyzed_df.write.format("delta") \
                .mode("append") \
                .save("/delta/social/moderation_results")
        
        # Process stream
        query = posts_stream.writeStream \
            .foreachBatch(analyze_content) \
            .option("checkpointLocation", "/delta/checkpoints/moderation") \
            .trigger(processingTime="5 seconds") \
            .start()
        
        return query
    
    return analyze_user_engagement(), predict_viral_content(), content_moderation_pipeline()
```

### 8. Implement graph analytics for social networks
**Answer:**
```python
def social_network_graph_analytics():
    # Build social graph
    def create_social_graph():
        # User connections
        connections_df = spark.read.format("delta").load("/delta/social/connections")
        
        # Create vertices (users)
        vertices = spark.read.format("delta").load("/delta/social/users") \
            .select("user_id", "username", "join_date", "location")
        
        # Create edges (relationships)
        edges = connections_df.select(
            col("user_id").alias("src"),
            col("friend_id").alias("dst"),
            col("connection_type").alias("relationship"),
            col("created_date").alias("since")
        )
        
        # Create GraphFrame
        from graphframes import GraphFrame
        graph = GraphFrame(vertices, edges)
        
        return graph
    
    # Community detection
    def detect_communities(graph):
        # Label propagation algorithm
        communities = graph.labelPropagation(maxIter=5)
        
        # Analyze community characteristics
        community_stats = communities.groupBy("label").agg(
            count("*").alias("community_size"),
            countDistinct("location").alias("location_diversity"),
            min("join_date").alias("oldest_member"),
            max("join_date").alias("newest_member")
        )
        
        # Save results
        communities.write.format("delta") \
            .mode("overwrite") \
            .save("/delta/social/communities")
        
        community_stats.write.format("delta") \
            .mode("overwrite") \
            .save("/delta/social/community_stats")
        
        return communities, community_stats
    
    # Influence analysis
    def analyze_influence(graph):
        # PageRank for influence scoring
        pagerank_results = graph.pageRank(resetProbability=0.15, maxIter=10)
        
        # Extract influential users
        influential_users = pagerank_results.vertices \
            .select("user_id", "username", "pagerank") \
            .orderBy(col("pagerank").desc()) \
            .limit(100)
        
        # Betweenness centrality (simplified)
        # In production, use more sophisticated algorithms
        shortest_paths = graph.shortestPaths(landmarks=["user1", "user2", "user3"])
        
        influential_users.write.format("delta") \
            .mode("overwrite") \
            .save("/delta/social/influential_users")
        
        return influential_users
    
    # Execute graph analytics
    graph = create_social_graph()
    communities, community_stats = detect_communities(graph)
    influential_users = analyze_influence(graph)
    
    return graph, communities, influential_users
```
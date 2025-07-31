# Big 4 Consulting Apache Spark Interview Questions

## Architecture & System Design Questions

**Q1: Design a real-time fraud detection system using Apache Spark for a global bank processing 10 million transactions per day across 50 countries.**

**Answer**: I would design a multi-layered, globally distributed architecture:

**Global Architecture Design**:
```scala
// Multi-region Spark Streaming setup
class GlobalFraudDetectionSystem {
  
  // Regional processing clusters
  val regions = Map(
    "US" -> SparkSession.builder().master("spark://us-cluster:7077"),
    "EU" -> SparkSession.builder().master("spark://eu-cluster:7077"),
    "APAC" -> SparkSession.builder().master("spark://apac-cluster:7077")
  )
  
  def setupRegionalStreaming(region: String, spark: SparkSession) = {
    val transactionStream = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", s"${region}-kafka:9092")
      .option("subscribe", "transactions")
      .option("maxOffsetsPerTrigger", 50000) // Handle high throughput
      .load()
    
    // Real-time feature engineering
    val enrichedStream = transactionStream
      .select(from_json(col("value").cast("string"), transactionSchema).alias("txn"))
      .select("txn.*")
      .withColumn("processing_timestamp", current_timestamp())
      .withColumn("region", lit(region))
  }
}
```

**Multi-Model Fraud Detection Pipeline**:
```scala
class FraudDetectionPipeline {
  
  // Rule-based detection (sub-second response)
  def applyRuleBasedDetection(df: DataFrame): DataFrame = {
    df.withColumn("rule_score",
      when(col("amount") > 10000 && col("merchant_country") =!= col("card_country"), 0.9)
      .when(col("transaction_count_last_hour") > 10, 0.8)
      .when(col("velocity_score") > 0.7, 0.7)
      .when(col("merchant_risk_score") > 0.6, 0.6)
      .otherwise(0.0)
    )
  }
  
  // ML-based detection (batch scoring every 5 minutes)
  def applyMLDetection(df: DataFrame, model: PipelineModel): DataFrame = {
    val features = new VectorAssembler()
      .setInputCols(Array("amount", "merchant_category", "time_features", "location_features"))
      .setOutputCol("features")
    
    val featurizedDF = features.transform(df)
    model.transform(featurizedDF)
      .withColumn("ml_score", col("probability").getItem(1))
  }
  
  // Graph-based network analysis
  def applyNetworkAnalysis(df: DataFrame): DataFrame = {
    // Create transaction graph
    val vertices = df.select("customer_id").distinct()
      .withColumnRenamed("customer_id", "id")
    
    val edges = df.select("customer_id", "merchant_id", "amount")
      .withColumnRenamed("customer_id", "src")
      .withColumnRenamed("merchant_id", "dst")
    
    val graph = GraphFrame(vertices, edges)
    
    // Calculate PageRank and connected components
    val pageRank = graph.pageRank.resetProbability(0.15).maxIter(10).run()
    val connectedComponents = graph.connectedComponents.run()
    
    // Join back network features
    df.join(pageRank.vertices.select("id", "pagerank"), 
            col("customer_id") === col("id"), "left")
      .withColumn("network_risk_score", 
                  when(col("pagerank") > 2.0, 0.8).otherwise(0.2))
  }
}
```

**Global Coordination and Scaling**:
```scala
// Cross-region coordination for global patterns
class GlobalCoordinator {
  
  def detectGlobalPatterns(regionalResults: Map[String, DataFrame]): DataFrame = {
    // Aggregate patterns across regions
    val globalPatterns = regionalResults.values.reduce(_.union(_))
      .groupBy("merchant_id", "card_bin")
      .agg(
        count("*").alias("global_transaction_count"),
        sum("amount").alias("global_amount"),
        countDistinct("region").alias("regions_active")
      )
      .filter(col("regions_active") >= 3) // Multi-region activity
    
    globalPatterns
  }
  
  // Auto-scaling based on transaction volume
  def autoScaleCluster(currentLoad: Double, region: String): Unit = {
    if (currentLoad > 0.8) {
      // Scale up executors
      val newExecutors = Math.min(currentExecutors * 1.5, maxExecutors).toInt
      sparkContext.requestTotalExecutors(newExecutors, 0, Map.empty)
    } else if (currentLoad < 0.3) {
      // Scale down executors
      val newExecutors = Math.max(currentExecutors * 0.7, minExecutors).toInt
      sparkContext.requestTotalExecutors(newExecutors, 0, Map.empty)
    }
  }
}
```

**Performance Requirements**:
- Sub-second response for rule-based detection
- 5-minute batch ML scoring
- 99.9% uptime with automatic failover
- Handle 10M transactions/day with peak loads of 50K/minute

**Q2: A Fortune 100 retail client wants to build a customer 360 platform processing 500TB of historical data and 50GB of daily incremental data. Design the complete Spark-based solution.**

**Answer**: Comprehensive Customer 360 platform design:

**Lambda Architecture Implementation**:
```scala
class Customer360Platform {
  
  // Batch Layer - Historical data processing
  class BatchLayer {
    def processHistoricalData(spark: SparkSession): Unit = {
      // Optimized for large-scale batch processing
      val batchConfig = Map(
        "spark.sql.adaptive.enabled" -> "true",
        "spark.sql.adaptive.coalescePartitions.enabled" -> "true",
        "spark.sql.adaptive.skewJoin.enabled" -> "true",
        "spark.executor.memory" -> "16g",
        "spark.executor.cores" -> "5",
        "spark.executor.instances" -> "100"
      )
      
      batchConfig.foreach { case (key, value) => spark.conf.set(key, value) }
      
      // Process customer transactions (largest dataset)
      val transactions = spark.read
        .option("mergeSchema", "true")
        .parquet("s3://data-lake/transactions/")
        .repartition(1000, col("customer_id")) // Optimize for customer-centric processing
      
      // Customer profile aggregations
      val customerProfiles = buildCustomerProfiles(transactions)
      
      // Write to Delta Lake with Z-ordering
      customerProfiles.write
        .format("delta")
        .option("optimizeWrite", "true")
        .mode("overwrite")
        .save("s3://customer360/batch/customer_profiles")
      
      // Optimize table for query performance
      spark.sql("OPTIMIZE customer360.customer_profiles ZORDER BY (customer_id, last_transaction_date)")
    }
    
    def buildCustomerProfiles(transactions: DataFrame): DataFrame = {
      // Complex customer analytics
      val customerMetrics = transactions
        .groupBy("customer_id")
        .agg(
          count("*").alias("total_transactions"),
          sum("amount").alias("lifetime_value"),
          avg("amount").alias("avg_transaction_value"),
          min("transaction_date").alias("first_transaction_date"),
          max("transaction_date").alias("last_transaction_date"),
          countDistinct("product_category").alias("category_diversity"),
          countDistinct("channel").alias("channel_usage"),
          stddev("amount").alias("spending_volatility")
        )
      
      // Customer segmentation using ML
      val segmentationModel = trainCustomerSegmentationModel(customerMetrics)
      val segmentedCustomers = segmentationModel.transform(customerMetrics)
      
      // Add derived features
      segmentedCustomers
        .withColumn("customer_tenure_days", 
                    datediff(current_date(), col("first_transaction_date")))
        .withColumn("days_since_last_transaction",
                    datediff(current_date(), col("last_transaction_date")))
        .withColumn("transaction_frequency",
                    col("total_transactions") / (col("customer_tenure_days") / 30.0))
        .withColumn("churn_risk_score", calculateChurnRisk(col("days_since_last_transaction")))
    }
  }
  
  // Speed Layer - Real-time incremental processing
  class SpeedLayer {
    def processIncrementalData(spark: SparkSession): Unit = {
      val incrementalStream = spark
        .readStream
        .format("delta")
        .option("ignoreChanges", "true")
        .load("s3://data-lake/incremental/")
      
      // Real-time customer profile updates
      val updatedProfiles = incrementalStream
        .groupBy("customer_id")
        .agg(
          count("*").alias("new_transactions"),
          sum("amount").alias("new_spending"),
          max("transaction_date").alias("latest_transaction")
        )
      
      // Merge with existing profiles
      val query = updatedProfiles
        .writeStream
        .format("delta")
        .outputMode("update")
        .option("checkpointLocation", "s3://checkpoints/customer360")
        .foreachBatch { (batchDF: DataFrame, batchId: Long) =>
          mergeIncrementalUpdates(batchDF, batchId)
        }
        .trigger(Trigger.ProcessingTime("5 minutes"))
        .start()
    }
    
    def mergeIncrementalUpdates(incrementalDF: DataFrame, batchId: Long): Unit = {
      // Delta Lake MERGE operation for UPSERT
      val deltaTable = DeltaTable.forPath(spark, "s3://customer360/profiles")
      
      deltaTable.alias("profiles")
        .merge(incrementalDF.alias("updates"), "profiles.customer_id = updates.customer_id")
        .whenMatched()
        .updateExpr(Map(
          "total_transactions" -> "profiles.total_transactions + updates.new_transactions",
          "lifetime_value" -> "profiles.lifetime_value + updates.new_spending",
          "last_transaction_date" -> "updates.latest_transaction",
          "updated_timestamp" -> "current_timestamp()"
        ))
        .whenNotMatched()
        .insertExpr(Map(
          "customer_id" -> "updates.customer_id",
          "total_transactions" -> "updates.new_transactions",
          "lifetime_value" -> "updates.new_spending",
          "last_transaction_date" -> "updates.latest_transaction",
          "created_timestamp" -> "current_timestamp()"
        ))
        .execute()
    }
  }
  
  // Serving Layer - Query optimization
  class ServingLayer {
    def optimizeForQueries(): Unit = {
      // Create materialized views for common queries
      spark.sql("""
        CREATE OR REPLACE VIEW high_value_customers AS
        SELECT customer_id, lifetime_value, segment, churn_risk_score
        FROM customer360.profiles
        WHERE lifetime_value > 10000
      """)
      
      // Partition tables for query performance
      spark.sql("""
        CREATE TABLE customer360.profiles_partitioned
        USING DELTA
        PARTITIONED BY (segment, churn_risk_category)
        AS SELECT * FROM customer360.profiles
      """)
      
      // Create indexes for fast lookups
      spark.sql("CREATE BLOOM FILTER INDEX ON customer360.profiles FOR COLUMNS (customer_id)")
    }
  }
}
```

**Data Quality and Governance Framework**:
```scala
class DataGovernanceFramework {
  
  def implementDataQuality(df: DataFrame): DataFrame = {
    // Comprehensive data quality checks
    val qualityRules = Seq(
      ("completeness", checkCompleteness _),
      ("uniqueness", checkUniqueness _),
      ("validity", checkValidity _),
      ("consistency", checkConsistency _),
      ("timeliness", checkTimeliness _)
    )
    
    var qualifiedDF = df
    val qualityMetrics = mutable.Map[String, Double]()
    
    qualityRules.foreach { case (ruleName, ruleFunction) =>
      val (updatedDF, score) = ruleFunction(qualifiedDF)
      qualifiedDF = updatedDF
      qualityMetrics(ruleName) = score
    }
    
    // Log quality metrics
    logQualityMetrics(qualityMetrics.toMap)
    
    qualifiedDF
  }
  
  def implementDataLineage(): Unit = {
    // Track data lineage using Delta Lake history
    val lineageTracker = new DataLineageTracker()
    
    // Custom listener to track transformations
    spark.sparkContext.addSparkListener(new SparkListener {
      override def onJobStart(jobStart: SparkListenerJobStart): Unit = {
        lineageTracker.recordTransformation(jobStart)
      }
    })
  }
  
  def implementDataSecurity(): Unit = {
    // Column-level encryption for PII
    val encryptionUDF = udf((data: String) => encrypt(data, getEncryptionKey()))
    
    // Apply encryption to sensitive columns
    val securedDF = df
      .withColumn("encrypted_email", encryptionUDF(col("email")))
      .withColumn("encrypted_phone", encryptionUDF(col("phone")))
      .drop("email", "phone")
    
    // Implement row-level security
    val userContext = getCurrentUserContext()
    val filteredDF = securedDF.filter(
      col("data_classification") <= lit(userContext.clearanceLevel)
    )
  }
}
```

## Performance & Optimization Questions

**Q3: Your Spark application processing 100TB of data is running for 12 hours instead of the target 4 hours. Walk through your systematic optimization approach.**

**Answer**: Comprehensive performance optimization methodology:

**Phase 1: Profiling and Root Cause Analysis**
```scala
class SparkPerformanceAnalyzer {
  
  def analyzeApplicationPerformance(applicationId: String): PerformanceReport = {
    // Analyze Spark History Server logs
    val historyServer = new SparkHistoryServer()
    val appInfo = historyServer.getApplicationInfo(applicationId)
    
    val analysis = PerformanceReport(
      executorMetrics = analyzeExecutorMetrics(appInfo),
      stageMetrics = analyzeStageMetrics(appInfo),
      taskMetrics = analyzeTaskMetrics(appInfo),
      ioMetrics = analyzeIOMetrics(appInfo),
      shuffleMetrics = analyzeShuffleMetrics(appInfo)
    )
    
    identifyBottlenecks(analysis)
  }
  
  def analyzeExecutorMetrics(appInfo: ApplicationInfo): ExecutorMetrics = {
    val executors = appInfo.executors
    
    ExecutorMetrics(
      memoryUtilization = executors.map(_.memoryUsed.toDouble / _.maxMemory).max,
      gcTime = executors.map(_.totalGCTime).sum,
      taskFailures = executors.map(_.failedTasks).sum,
      dataSkew = calculateDataSkew(executors.map(_.totalInputBytes))
    )
  }
  
  def identifyBottlenecks(report: PerformanceReport): List[Bottleneck] = {
    val bottlenecks = mutable.ListBuffer[Bottleneck]()
    
    // Memory bottlenecks
    if (report.executorMetrics.memoryUtilization > 0.9) {
      bottlenecks += MemoryBottleneck("High memory utilization", "Increase executor memory or reduce partition size")
    }
    
    // Data skew detection
    if (report.executorMetrics.dataSkew > 5.0) {
      bottlenecks += DataSkewBottleneck("Severe data skew detected", "Implement salting or custom partitioning")
    }
    
    // I/O bottlenecks
    if (report.ioMetrics.avgReadTime > 1000) {
      bottlenecks += IOBottleneck("Slow I/O operations", "Optimize file format or increase parallelism")
    }
    
    bottlenecks.toList
  }
}
```

**Phase 2: Targeted Optimizations**
```scala
class PerformanceOptimizer {
  
  def optimizeMemoryUsage(spark: SparkSession): Unit = {
    // Optimize memory configuration
    val optimalConfig = calculateOptimalMemoryConfig(
      dataSize = 100.TB,
      availableMemory = getClusterMemory(),
      workloadType = "ETL"
    )
    
    spark.conf.set("spark.executor.memory", optimalConfig.executorMemory)
    spark.conf.set("spark.executor.memoryFraction", optimalConfig.memoryFraction)
    spark.conf.set("spark.storage.memoryFraction", optimalConfig.storageFraction)
    
    // Enable off-heap memory for large datasets
    spark.conf.set("spark.sql.columnVector.offheap.enabled", "true")
    spark.conf.set("spark.memory.offHeap.enabled", "true")
    spark.conf.set("spark.memory.offHeap.size", "8g")
  }
  
  def optimizePartitioning(df: DataFrame): DataFrame = {
    // Calculate optimal partition count
    val dataSize = estimateDataSize(df)
    val optimalPartitions = (dataSize / (128 * 1024 * 1024)).toInt // 128MB per partition
    
    // Repartition based on data distribution
    val skewAnalysis = analyzeDataSkew(df, "partition_key")
    
    if (skewAnalysis.isSkewed) {
      // Apply salting for skewed data
      val saltedDF = df.withColumn("salted_key", 
        concat(col("partition_key"), lit("_"), (rand() * 100).cast("int")))
      saltedDF.repartition(optimalPartitions, col("salted_key"))
    } else {
      df.repartition(optimalPartitions, col("partition_key"))
    }
  }
  
  def optimizeJoins(leftDF: DataFrame, rightDF: DataFrame, joinKey: String): DataFrame = {
    val leftSize = estimateDataSize(leftDF)
    val rightSize = estimateDataSize(rightDF)
    
    // Choose optimal join strategy
    if (rightSize < 10 * 1024 * 1024) { // 10MB threshold for broadcast
      leftDF.join(broadcast(rightDF), joinKey)
    } else if (leftSize > rightSize * 10) { // Size difference > 10x
      // Use bucket join for large tables
      createBucketedTables(leftDF, rightDF, joinKey)
      spark.sql("SELECT * FROM bucketed_left l JOIN bucketed_right r ON l.key = r.key")
    } else {
      // Use sort-merge join with optimal partitioning
      val partitionedLeft = leftDF.repartition(200, col(joinKey))
      val partitionedRight = rightDF.repartition(200, col(joinKey))
      partitionedLeft.join(partitionedRight, joinKey)
    }
  }
  
  def optimizeIO(inputPath: String, outputPath: String): Unit = {
    // Optimize file format
    val df = spark.read.parquet(inputPath)
    
    // Compress and optimize writes
    df.write
      .option("compression", "snappy")
      .option("parquet.block.size", "268435456") // 256MB blocks
      .mode("overwrite")
      .parquet(outputPath)
    
    // Compact small files
    spark.sql(s"OPTIMIZE delta.`$outputPath`")
  }
}
```

**Phase 3: Advanced Optimizations**
```scala
class AdvancedOptimizations {
  
  def implementCustomCatalystRules(): Unit = {
    // Custom optimization rules
    val customRule = new Rule[LogicalPlan] {
      def apply(plan: LogicalPlan): LogicalPlan = plan transform {
        case filter @ Filter(condition, child) =>
          // Push down filters more aggressively
          optimizeFilterPushdown(filter, condition, child)
      }
    }
    
    // Register custom rule
    spark.experimental.extraOptimizations = Seq(customRule)
  }
  
  def implementCustomPartitioner(): Unit = {
    // Custom partitioner for domain-specific data distribution
    class CustomerPartitioner(numPartitions: Int) extends Partitioner {
      override def getPartition(key: Any): Int = {
        key match {
          case customerId: String =>
            // Distribute high-value customers evenly
            if (isHighValueCustomer(customerId)) {
              Math.abs(customerId.hashCode) % (numPartitions / 2)
            } else {
              (numPartitions / 2) + (Math.abs(customerId.hashCode) % (numPartitions / 2))
            }
          case _ => Math.abs(key.hashCode) % numPartitions
        }
      }
    }
  }
  
  def implementAdaptiveQueryExecution(): Unit = {
    // Enable all AQE features
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
    spark.conf.set("spark.sql.adaptive.localShuffleReader.enabled", "true")
    
    // Fine-tune AQE parameters
    spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "134217728") // 128MB
    spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "268435456") // 256MB
    spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
  }
}
```

**Expected Results**:
- 70% reduction in execution time (12 hours → 4 hours)
- 50% reduction in resource usage
- Improved fault tolerance and stability
- Better resource utilization across the cluster

## Machine Learning & Advanced Analytics Questions

**Q4: Design and implement a distributed machine learning pipeline using Spark MLlib for real-time customer churn prediction serving 1 million predictions per day.**

**Answer**: Comprehensive ML pipeline for production-scale churn prediction:

**Feature Engineering Pipeline**:
```scala
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.feature._
import org.apache.spark.ml.classification._
import org.apache.spark.ml.evaluation._
import org.apache.spark.ml.tuning._

class ChurnPredictionMLPipeline {
  
  def createFeatureEngineeringPipeline(): Pipeline = {
    // Temporal features
    val temporalTransformer = new SQLTransformer().setStatement("""
      SELECT *,
             DATEDIFF(CURRENT_DATE(), last_transaction_date) as days_since_last_transaction,
             DATEDIFF(last_transaction_date, first_transaction_date) as customer_lifetime_days,
             MONTH(registration_date) as registration_month,
             DAYOFWEEK(last_login_date) as last_login_day_of_week
      FROM __THIS__
    """)
    
    // Behavioral features
    val behavioralTransformer = new SQLTransformer().setStatement("""
      SELECT *,
             total_transactions / (customer_lifetime_days / 30.0) as monthly_transaction_frequency,
             total_amount / total_transactions as avg_transaction_amount,
             support_tickets / (customer_lifetime_days / 30.0) as monthly_support_rate,
             CASE WHEN login_frequency > 20 THEN 1 ELSE 0 END as high_engagement_flag
      FROM __THIS__
    """)
    
    // Categorical encoding
    val categoricalCols = Array("subscription_type", "payment_method", "region", "device_type")
    val stringIndexers = categoricalCols.map { col =>
      new StringIndexer()
        .setInputCol(col)
        .setOutputCol(s"${col}_indexed")
        .setHandleInvalid("keep")
    }
    
    val oneHotEncoders = categoricalCols.map { col =>
      new OneHotEncoder()
        .setInputCol(s"${col}_indexed")
        .setOutputCol(s"${col}_encoded")
    }
    
    // Numerical feature scaling
    val numericalCols = Array("monthly_charges", "total_charges", "tenure_months", 
                             "monthly_transaction_frequency", "avg_transaction_amount")
    
    val vectorAssembler = new VectorAssembler()
      .setInputCols(numericalCols)
      .setOutputCol("numerical_features")
    
    val scaler = new StandardScaler()
      .setInputCol("numerical_features")
      .setOutputCol("scaled_numerical_features")
      .setWithStd(true)
      .setWithMean(true)
    
    // Feature selection
    val featureSelector = new ChiSqSelector()
      .setNumTopFeatures(50)
      .setFeaturesCol("all_features")
      .setOutputCol("selected_features")
      .setLabelCol("churn_label")
    
    // Final feature assembly
    val allFeatureCols = categoricalCols.map(_ + "_encoded") ++ Array("scaled_numerical_features")
    val finalAssembler = new VectorAssembler()
      .setInputCols(allFeatureCols)
      .setOutputCol("all_features")
    
    new Pipeline().setStages(
      Array(temporalTransformer, behavioralTransformer) ++
      stringIndexers ++ oneHotEncoders ++
      Array(vectorAssembler, scaler, finalAssembler, featureSelector)
    )
  }
  
  def createEnsembleModel(): Pipeline = {
    // Label encoding
    val labelIndexer = new StringIndexer()
      .setInputCol("churn")
      .setOutputCol("churn_label")
    
    // Multiple base models
    val randomForest = new RandomForestClassifier()
      .setLabelCol("churn_label")
      .setFeaturesCol("selected_features")
      .setNumTrees(100)
      .setMaxDepth(10)
      .setSubsamplingRate(0.8)
      .setSeed(42)
    
    val gradientBoosting = new GBTClassifier()
      .setLabelCol("churn_label")
      .setFeaturesCol("selected_features")
      .setMaxIter(100)
      .setMaxDepth(6)
      .setStepSize(0.1)
      .setSeed(42)
    
    val logisticRegression = new LogisticRegression()
      .setLabelCol("churn_label")
      .setFeaturesCol("selected_features")
      .setMaxIter(100)
      .setRegParam(0.01)
      .setElasticNetParam(0.5)
    
    // Ensemble using voting classifier
    val ensemble = new VotingClassifier()
      .setEstimators(Array(randomForest, gradientBoosting, logisticRegression))
      .setWeights(Array(0.4, 0.4, 0.2)) // Weight based on validation performance
    
    new Pipeline().setStages(Array(labelIndexer, ensemble))
  }
  
  def performHyperparameterTuning(pipeline: Pipeline, trainingData: DataFrame): CrossValidatorModel = {
    // Parameter grid
    val paramGrid = new ParamGridBuilder()
      .addGrid(randomForest.numTrees, Array(50, 100, 200))
      .addGrid(randomForest.maxDepth, Array(5, 10, 15))
      .addGrid(gradientBoosting.maxIter, Array(50, 100, 150))
      .addGrid(gradientBoosting.maxDepth, Array(4, 6, 8))
      .addGrid(logisticRegression.regParam, Array(0.01, 0.1, 1.0))
      .build()
    
    // Evaluator
    val evaluator = new BinaryClassificationEvaluator()
      .setLabelCol("churn_label")
      .setRawPredictionCol("rawPrediction")
      .setMetricName("areaUnderROC")
    
    // Cross-validation
    val cv = new CrossValidator()
      .setEstimator(pipeline)
      .setEvaluator(evaluator)
      .setEstimatorParamMaps(paramGrid)
      .setNumFolds(5)
      .setParallelism(4)
      .setSeed(42)
    
    cv.fit(trainingData)
  }
}
```

**Real-time Serving Infrastructure**:
```scala
class RealTimeChurnPredictionService {
  
  def setupStreamingPrediction(): Unit = {
    // Load trained model
    val model = PipelineModel.load("models/churn_prediction/v1.0")
    
    // Real-time feature store
    val featureStore = new FeatureStore(spark)
    
    // Streaming prediction pipeline
    val customerStream = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "kafka:9092")
      .option("subscribe", "customer_events")
      .option("maxOffsetsPerTrigger", 10000) // Handle 1M predictions/day
      .load()
    
    val predictions = customerStream
      .select(from_json(col("value").cast("string"), customerSchema).alias("customer"))
      .select("customer.*")
      .transform(enrichWithFeatures(featureStore))
      .transform(model.transform)
      .select(
        col("customer_id"),
        col("prediction").alias("churn_prediction"),
        col("probability").getItem(1).alias("churn_probability"),
        current_timestamp().alias("prediction_timestamp")
      )
    
    // Write predictions to multiple sinks
    val query = predictions
      .writeStream
      .foreachBatch { (batchDF: DataFrame, batchId: Long) =>
        // Write to cache for real-time serving
        writeToRedis(batchDF)
        
        // Write to data lake for analytics
        batchDF.write
          .format("delta")
          .mode("append")
          .save("predictions/churn_predictions")
        
        // Send high-risk alerts
        sendHighRiskAlerts(batchDF.filter(col("churn_probability") > 0.8))
      }
      .trigger(Trigger.ProcessingTime("30 seconds"))
      .start()
  }
  
  def enrichWithFeatures(featureStore: FeatureStore)(df: DataFrame): DataFrame = {
    // Join with pre-computed features
    val customerFeatures = featureStore.getFeatures("customer_features", df.select("customer_id"))
    val transactionFeatures = featureStore.getFeatures("transaction_features", df.select("customer_id"))
    val behavioralFeatures = featureStore.getFeatures("behavioral_features", df.select("customer_id"))
    
    df.join(customerFeatures, "customer_id")
      .join(transactionFeatures, "customer_id")
      .join(behavioralFeatures, "customer_id")
  }
  
  def setupBatchScoring(): Unit = {
    // Daily batch scoring for all customers
    val dailyBatchJob = spark
      .read
      .format("delta")
      .load("customer_profiles")
      .filter(col("last_updated") >= date_sub(current_date(), 1))
    
    val model = PipelineModel.load("models/churn_prediction/v1.0")
    val predictions = model.transform(dailyBatchJob)
    
    // Update customer risk scores
    predictions
      .select("customer_id", "churn_probability", "prediction_timestamp")
      .write
      .format("delta")
      .mode("overwrite")
      .option("replaceWhere", s"prediction_date = '${java.time.LocalDate.now()}'")
      .save("customer_risk_scores")
  }
}
```

**Model Monitoring and Retraining**:
```scala
class ModelMonitoringFramework {
  
  def monitorModelPerformance(): Unit = {
    // Calculate model drift
    val recentPredictions = spark.read
      .format("delta")
      .load("predictions/churn_predictions")
      .filter(col("prediction_timestamp") >= date_sub(current_date(), 7))
    
    val actualChurn = spark.read
      .format("delta")
      .load("customer_churn_labels")
      .filter(col("churn_date") >= date_sub(current_date(), 7))
    
    val performanceMetrics = recentPredictions
      .join(actualChurn, "customer_id")
      .select("churn_prediction", "actual_churn", "churn_probability")
    
    val accuracy = calculateAccuracy(performanceMetrics)
    val auc = calculateAUC(performanceMetrics)
    val precision = calculatePrecision(performanceMetrics)
    val recall = calculateRecall(performanceMetrics)
    
    // Data drift detection
    val featureDrift = detectFeatureDrift(recentPredictions)
    
    // Trigger retraining if performance degrades
    if (accuracy < 0.85 || auc < 0.8 || featureDrift > 0.1) {
      triggerModelRetraining()
    }
    
    // Log metrics
    logModelMetrics(Map(
      "accuracy" -> accuracy,
      "auc" -> auc,
      "precision" -> precision,
      "recall" -> recall,
      "feature_drift" -> featureDrift
    ))
  }
  
  def triggerModelRetraining(): Unit = {
    // Get fresh training data
    val trainingData = spark.read
      .format("delta")
      .load("training_data")
      .filter(col("data_date") >= date_sub(current_date(), 365)) // Last year of data
    
    // Retrain model
    val pipeline = new ChurnPredictionMLPipeline()
    val featurePipeline = pipeline.createFeatureEngineeringPipeline()
    val modelPipeline = pipeline.createEnsembleModel()
    
    val fullPipeline = new Pipeline().setStages(
      featurePipeline.getStages ++ modelPipeline.getStages
    )
    
    val newModel = pipeline.performHyperparameterTuning(fullPipeline, trainingData)
    
    // A/B test new model
    deployModelForABTest(newModel, "v2.0")
  }
  
  def deployModelForABTest(model: CrossValidatorModel, version: String): Unit = {
    // Deploy new model to serve 10% of traffic
    val modelRegistry = new ModelRegistry()
    modelRegistry.registerModel("churn_prediction", version, model)
    
    // Update serving configuration
    val servingConfig = ServingConfig(
      models = Map(
        "v1.0" -> 0.9, // 90% traffic
        "v2.0" -> 0.1  // 10% traffic
      ),
      routingStrategy = "random"
    )
    
    updateServingConfiguration(servingConfig)
  }
}
```

**Performance Characteristics**:
- Handle 1M predictions per day (11.6 predictions/second average)
- Sub-second prediction latency for real-time requests
- 99.9% availability with automatic failover
- Model accuracy > 85% with AUC > 0.8
- Automatic model retraining when performance degrades
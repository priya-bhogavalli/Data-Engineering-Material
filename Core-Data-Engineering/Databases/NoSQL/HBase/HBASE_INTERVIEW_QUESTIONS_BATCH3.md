## 🔴 Advanced Level Questions

### 21. How do you design and implement a distributed counter system in HBase?
**Answer**: Distributed counters require careful design to avoid hotspotting while maintaining accuracy.

```java
public class DistributedCounter {
    
    // Sharded counter implementation
    public class ShardedCounter {
        private final int numShards;
        private final String counterName;
        private final Table counterTable;
        
        public ShardedCounter(String counterName, int numShards, Table counterTable) {
            this.counterName = counterName;
            this.numShards = numShards;
            this.counterTable = counterTable;
        }
        
        // Increment counter with random sharding
        public void increment(long delta) throws IOException {
            int shard = ThreadLocalRandom.current().nextInt(numShards);
            String rowKey = counterName + "_shard_" + String.format("%03d", shard);
            
            counterTable.incrementColumnValue(
                Bytes.toBytes(rowKey),
                Bytes.toBytes("counters"),
                Bytes.toBytes("value"),
                delta
            );
        }
        
        // Get total counter value
        public long getValue() throws IOException {
            long total = 0;
            
            // Scan all shards
            Scan scan = new Scan();
            scan.setStartRow(Bytes.toBytes(counterName + "_shard_"));
            scan.setStopRow(Bytes.toBytes(counterName + "_shard_" + "~"));
            scan.addFamily(Bytes.toBytes("counters"));
            
            ResultScanner scanner = counterTable.getScanner(scan);
            
            try {
                for (Result result : scanner) {
                    byte[] value = result.getValue(Bytes.toBytes("counters"), 
                                                 Bytes.toBytes("value"));
                    if (value != null) {
                        total += Bytes.toLong(value);
                    }
                }
            } finally {
                scanner.close();
            }
            
            return total;
        }
        
        // Reset counter
        public void reset() throws IOException {
            List<Delete> deletes = new ArrayList<>();
            
            Scan scan = new Scan();
            scan.setStartRow(Bytes.toBytes(counterName + "_shard_"));
            scan.setStopRow(Bytes.toBytes(counterName + "_shard_" + "~"));
            scan.setFilter(new KeyOnlyFilter());
            
            ResultScanner scanner = counterTable.getScanner(scan);
            
            try {
                for (Result result : scanner) {
                    Delete delete = new Delete(result.getRow());
                    deletes.add(delete);
                }
            } finally {
                scanner.close();
            }
            
            if (!deletes.isEmpty()) {
                counterTable.delete(deletes);
            }
        }
    }
    
    // Time-based counter with automatic rollover
    public class TimeBasedCounter {
        private final String counterName;
        private final Table counterTable;
        private final long rolloverPeriod; // in milliseconds
        
        public TimeBasedCounter(String counterName, Table counterTable, long rolloverPeriod) {
            this.counterName = counterName;
            this.counterTable = counterTable;
            this.rolloverPeriod = rolloverPeriod;
        }
        
        public void increment(long delta) throws IOException {
            long currentTime = System.currentTimeMillis();
            long bucket = currentTime / rolloverPeriod;
            
            String rowKey = counterName + "_" + bucket;
            
            counterTable.incrementColumnValue(
                Bytes.toBytes(rowKey),
                Bytes.toBytes("counters"),
                Bytes.toBytes("value"),
                delta
            );
            
            // Store metadata
            Put metaPut = new Put(Bytes.toBytes(rowKey));
            metaPut.addColumn(Bytes.toBytes("meta"), Bytes.toBytes("start_time"), 
                             Bytes.toBytes(bucket * rolloverPeriod));
            metaPut.addColumn(Bytes.toBytes("meta"), Bytes.toBytes("end_time"), 
                             Bytes.toBytes((bucket + 1) * rolloverPeriod));
            counterTable.put(metaPut);
        }
        
        public long getCurrentValue() throws IOException {
            long currentTime = System.currentTimeMillis();
            long bucket = currentTime / rolloverPeriod;
            String rowKey = counterName + "_" + bucket;
            
            Get get = new Get(Bytes.toBytes(rowKey));
            Result result = counterTable.get(get);
            
            if (result.isEmpty()) {
                return 0;
            }
            
            byte[] value = result.getValue(Bytes.toBytes("counters"), Bytes.toBytes("value"));
            return value != null ? Bytes.toLong(value) : 0;
        }
        
        public Map<Long, Long> getHistoricalValues(long startTime, long endTime) throws IOException {
            Map<Long, Long> values = new HashMap<>();
            
            long startBucket = startTime / rolloverPeriod;
            long endBucket = endTime / rolloverPeriod;
            
            for (long bucket = startBucket; bucket <= endBucket; bucket++) {
                String rowKey = counterName + "_" + bucket;
                Get get = new Get(Bytes.toBytes(rowKey));
                Result result = counterTable.get(get);
                
                if (!result.isEmpty()) {
                    byte[] value = result.getValue(Bytes.toBytes("counters"), Bytes.toBytes("value"));
                    if (value != null) {
                        values.put(bucket * rolloverPeriod, Bytes.toLong(value));
                    }
                }
            }
            
            return values;
        }
    }
    
    // Approximate counter using HyperLogLog
    public class ApproximateCounter {
        private final String counterName;
        private final Table counterTable;
        
        public ApproximateCounter(String counterName, Table counterTable) {
            this.counterName = counterName;
            this.counterTable = counterTable;
        }
        
        public void addElement(String element) throws IOException {
            // Simple hash-based approximation (in practice, use HyperLogLog library)
            int hash = element.hashCode();
            int bucket = Math.abs(hash) % 1024; // 1024 buckets
            int leadingZeros = Integer.numberOfLeadingZeros(hash);
            
            String rowKey = counterName + "_bucket_" + String.format("%04d", bucket);
            
            // Store maximum leading zeros for this bucket
            Get get = new Get(Bytes.toBytes(rowKey));
            Result result = counterTable.get(get);
            
            int currentMax = 0;
            if (!result.isEmpty()) {
                byte[] value = result.getValue(Bytes.toBytes("hll"), Bytes.toBytes("max_zeros"));
                if (value != null) {
                    currentMax = Bytes.toInt(value);
                }
            }
            
            if (leadingZeros > currentMax) {
                Put put = new Put(Bytes.toBytes(rowKey));
                put.addColumn(Bytes.toBytes("hll"), Bytes.toBytes("max_zeros"), 
                             Bytes.toBytes(leadingZeros));
                counterTable.put(put);
            }
        }
        
        public long estimateCardinality() throws IOException {
            // Simplified HyperLogLog estimation
            double sum = 0.0;
            int buckets = 0;
            
            Scan scan = new Scan();
            scan.setStartRow(Bytes.toBytes(counterName + "_bucket_"));
            scan.setStopRow(Bytes.toBytes(counterName + "_bucket_" + "~"));
            scan.addFamily(Bytes.toBytes("hll"));
            
            ResultScanner scanner = counterTable.getScanner(scan);
            
            try {
                for (Result result : scanner) {
                    byte[] value = result.getValue(Bytes.toBytes("hll"), Bytes.toBytes("max_zeros"));
                    if (value != null) {
                        int maxZeros = Bytes.toInt(value);
                        sum += Math.pow(2, -maxZeros);
                        buckets++;
                    }
                }
            } finally {
                scanner.close();
            }
            
            if (buckets == 0) return 0;
            
            // HyperLogLog estimation formula (simplified)
            double alpha = 0.7213 / (1 + 1.079 / buckets);
            return Math.round(alpha * buckets * buckets / sum);
        }
    }
}
```

### 22. How do you implement cross-datacenter replication in HBase?
**Answer**: HBase supports cross-datacenter replication for disaster recovery and geographic distribution.

```java
public class CrossDatacenterReplication {
    
    // Setup replication between clusters
    public void setupReplication() throws IOException {
        Admin admin = connection.getAdmin();
        
        // Add replication peer
        ReplicationPeerConfig peerConfig = ReplicationPeerConfig.newBuilder()
            .setClusterKey("zk1,zk2,zk3:2181:/hbase") // Remote cluster ZK
            .setReplicateAllUserTables(false) // Selective replication
            .build();
        
        admin.addReplicationPeer("peer1", peerConfig);
        
        // Enable replication for specific table
        TableName tableName = TableName.valueOf("replicated_table");
        admin.enableTableReplication(tableName);
        
        // Set replication scope for column families
        TableDescriptor tableDesc = admin.getDescriptor(tableName);
        TableDescriptorBuilder builder = TableDescriptorBuilder.newBuilder(tableDesc);
        
        for (ColumnFamilyDescriptor cfDesc : tableDesc.getColumnFamilies()) {
            ColumnFamilyDescriptorBuilder cfBuilder = ColumnFamilyDescriptorBuilder
                .newBuilder(cfDesc)
                .setScope(HConstants.REPLICATION_SCOPE_GLOBAL); // Enable replication
            builder.modifyColumnFamily(cfBuilder.build());
        }
        
        admin.disableTable(tableName);
        admin.modifyTable(builder.build());
        admin.enableTable(tableName);
    }
    
    // Monitor replication lag
    public class ReplicationMonitor {
        
        public void monitorReplicationLag() throws IOException {
            Admin admin = connection.getAdmin();
            
            // Get replication peer status
            List<ReplicationPeerDescription> peers = admin.listReplicationPeers();
            
            for (ReplicationPeerDescription peer : peers) {
                String peerId = peer.getPeerId();
                System.out.println("Peer ID: " + peerId);
                System.out.println("State: " + peer.isEnabled());
                
                // Get replication status
                ClusterMetrics metrics = admin.getClusterMetrics();
                for (ServerMetrics serverMetrics : metrics.getLiveServerMetrics().values()) {
                    Map<String, ReplicationLoadSource> replicationLoad = 
                        serverMetrics.getReplicationLoadSourceMap();
                    
                    ReplicationLoadSource loadSource = replicationLoad.get(peerId);
                    if (loadSource != null) {
                        System.out.println("Replication lag: " + loadSource.getReplicationLag());
                        System.out.println("Queue size: " + loadSource.getQueueSize());
                    }
                }
            }
        }
        
        // Custom replication lag calculation
        public long calculateReplicationLag(String tableName, String peerId) throws IOException {
            // Get latest timestamp from source table
            Table sourceTable = connection.getTable(TableName.valueOf(tableName));
            Scan scan = new Scan();
            scan.setReversed(true); // Get latest entries first
            scan.setLimit(1);
            scan.addFamily(Bytes.toBytes("cf1"));
            
            ResultScanner scanner = sourceTable.getScanner(scan);
            long sourceLatestTimestamp = 0;
            
            try {
                Result result = scanner.next();
                if (result != null) {
                    sourceLatestTimestamp = result.rawCells()[0].getTimestamp();
                }
            } finally {
                scanner.close();
            }
            
            // Compare with peer cluster (requires connection to peer)
            // This is a simplified example - in practice, you'd need
            // to connect to the peer cluster and check timestamps
            
            return System.currentTimeMillis() - sourceLatestTimestamp;
        }
    }
    
    // Bidirectional replication setup
    public void setupBidirectionalReplication() throws IOException {
        Admin admin = connection.getAdmin();
        
        // Cluster A -> Cluster B
        ReplicationPeerConfig peerConfigB = ReplicationPeerConfig.newBuilder()
            .setClusterKey("zkB1,zkB2,zkB3:2181:/hbase")
            .setReplicateAllUserTables(false)
            .build();
        admin.addReplicationPeer("clusterB", peerConfigB);
        
        // Cluster B -> Cluster A (configure on cluster B)
        // ReplicationPeerConfig peerConfigA = ReplicationPeerConfig.newBuilder()
        //     .setClusterKey("zkA1,zkA2,zkA3:2181:/hbase")
        //     .setReplicateAllUserTables(false)
        //     .build();
        // adminB.addReplicationPeer("clusterA", peerConfigA);
        
        // Enable replication for tables
        TableName tableName = TableName.valueOf("bidirectional_table");
        admin.enableTableReplication(tableName);
        
        // Configure conflict resolution (timestamp-based)
        TableDescriptor tableDesc = admin.getDescriptor(tableName);
        TableDescriptorBuilder builder = TableDescriptorBuilder.newBuilder(tableDesc);
        
        // Add conflict resolution metadata
        builder.setValue("replication.conflict.resolution", "timestamp");
        
        admin.disableTable(tableName);
        admin.modifyTable(builder.build());
        admin.enableTable(tableName);
    }
    
    // Selective replication with filters
    public void setupSelectiveReplication() throws IOException {
        Admin admin = connection.getAdmin();
        
        // Create replication peer with table filter
        Map<TableName, List<String>> tableCFs = new HashMap<>();
        tableCFs.put(TableName.valueOf("user_data"), Arrays.asList("profile", "activity"));
        tableCFs.put(TableName.valueOf("system_logs"), Arrays.asList("events"));
        
        ReplicationPeerConfig peerConfig = ReplicationPeerConfig.newBuilder()
            .setClusterKey("remote-zk1,remote-zk2:2181:/hbase")
            .setReplicateAllUserTables(false)
            .setTableCFsMap(tableCFs)
            .build();
        
        admin.addReplicationPeer("selective_peer", peerConfig);
        
        // Enable replication for specific tables
        for (TableName tableName : tableCFs.keySet()) {
            admin.enableTableReplication(tableName);
        }
    }
    
    // Replication failure handling
    public class ReplicationFailureHandler {
        
        public void handleReplicationFailure(String peerId) throws IOException {
            Admin admin = connection.getAdmin();
            
            // Disable failed peer temporarily
            admin.disableReplicationPeer(peerId);
            
            // Check and fix issues
            boolean issueResolved = diagnoseAndFixIssues(peerId);
            
            if (issueResolved) {
                // Re-enable replication
                admin.enableReplicationPeer(peerId);
                
                // Trigger catch-up replication
                triggerCatchUpReplication(peerId);
            }
        }
        
        private boolean diagnoseAndFixIssues(String peerId) {
            // Check network connectivity
            // Verify peer cluster health
            // Check authentication/authorization
            // Validate configuration
            
            return true; // Simplified
        }
        
        private void triggerCatchUpReplication(String peerId) throws IOException {
            // Force replication queue processing
            Admin admin = connection.getAdmin();
            
            // Get cluster metrics to identify RegionServers
            ClusterMetrics metrics = admin.getClusterMetrics();
            
            for (ServerName serverName : metrics.getLiveServerMetrics().keySet()) {
                // Trigger replication queue processing on each server
                // This is typically done through JMX or admin operations
                System.out.println("Triggering catch-up replication on: " + serverName);
            }
        }
    }
}
```

### 23. How do you implement custom data serialization and deserialization in HBase?
**Answer**: Custom serialization allows efficient storage and retrieval of complex data types.

```java
public class CustomSerialization {
    
    // Custom serializable object
    public static class UserProfile implements Serializable {
        private String userId;
        private String name;
        private String email;
        private int age;
        private List<String> interests;
        private Map<String, String> metadata;
        private long lastLoginTime;
        
        // Constructors, getters, setters...
        
        // Custom binary serialization
        public byte[] serialize() throws IOException {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            DataOutputStream dos = new DataOutputStream(baos);
            
            // Write fields in specific order
            dos.writeUTF(userId != null ? userId : "");
            dos.writeUTF(name != null ? name : "");
            dos.writeUTF(email != null ? email : "");
            dos.writeInt(age);
            dos.writeLong(lastLoginTime);
            
            // Write interests list
            dos.writeInt(interests != null ? interests.size() : 0);
            if (interests != null) {
                for (String interest : interests) {
                    dos.writeUTF(interest);
                }
            }
            
            // Write metadata map
            dos.writeInt(metadata != null ? metadata.size() : 0);
            if (metadata != null) {
                for (Map.Entry<String, String> entry : metadata.entrySet()) {
                    dos.writeUTF(entry.getKey());
                    dos.writeUTF(entry.getValue());
                }
            }
            
            dos.close();
            return baos.toByteArray();
        }
        
        public static UserProfile deserialize(byte[] data) throws IOException {
            if (data == null || data.length == 0) {
                return null;
            }
            
            ByteArrayInputStream bais = new ByteArrayInputStream(data);
            DataInputStream dis = new DataInputStream(bais);
            
            UserProfile profile = new UserProfile();
            
            // Read fields in same order
            profile.userId = dis.readUTF();
            profile.name = dis.readUTF();
            profile.email = dis.readUTF();
            profile.age = dis.readInt();
            profile.lastLoginTime = dis.readLong();
            
            // Read interests list
            int interestsSize = dis.readInt();
            if (interestsSize > 0) {
                profile.interests = new ArrayList<>();
                for (int i = 0; i < interestsSize; i++) {
                    profile.interests.add(dis.readUTF());
                }
            }
            
            // Read metadata map
            int metadataSize = dis.readInt();
            if (metadataSize > 0) {
                profile.metadata = new HashMap<>();
                for (int i = 0; i < metadataSize; i++) {
                    String key = dis.readUTF();
                    String value = dis.readUTF();
                    profile.metadata.put(key, value);
                }
            }
            
            dis.close();
            return profile;
        }
    }
    
    // Protocol Buffers serialization
    public static class ProtobufSerialization {
        
        // Assuming UserProfileProto is generated from .proto file
        public void storeUserProfile(String userId, UserProfile profile) throws IOException {
            // Convert to protobuf
            UserProfileProto.Builder builder = UserProfileProto.newBuilder()
                .setUserId(profile.getUserId())
                .setName(profile.getName())
                .setEmail(profile.getEmail())
                .setAge(profile.getAge())
                .setLastLoginTime(profile.getLastLoginTime());
            
            if (profile.getInterests() != null) {
                builder.addAllInterests(profile.getInterests());
            }
            
            if (profile.getMetadata() != null) {
                builder.putAllMetadata(profile.getMetadata());
            }
            
            UserProfileProto proto = builder.build();
            
            // Store in HBase
            Put put = new Put(Bytes.toBytes(userId));
            put.addColumn(Bytes.toBytes("profile"), Bytes.toBytes("data"), 
                         proto.toByteArray());
            table.put(put);
        }
        
        public UserProfile getUserProfile(String userId) throws IOException {
            Get get = new Get(Bytes.toBytes(userId));
            Result result = table.get(get);
            
            if (result.isEmpty()) {
                return null;
            }
            
            byte[] data = result.getValue(Bytes.toBytes("profile"), Bytes.toBytes("data"));
            if (data == null) {
                return null;
            }
            
            // Deserialize from protobuf
            UserProfileProto proto = UserProfileProto.parseFrom(data);
            
            UserProfile profile = new UserProfile();
            profile.setUserId(proto.getUserId());
            profile.setName(proto.getName());
            profile.setEmail(proto.getEmail());
            profile.setAge(proto.getAge());
            profile.setLastLoginTime(proto.getLastLoginTime());
            profile.setInterests(new ArrayList<>(proto.getInterestsList()));
            profile.setMetadata(new HashMap<>(proto.getMetadataMap()));
            
            return profile;
        }
    }
    
    // Avro serialization
    public static class AvroSerialization {
        private Schema schema;
        
        public AvroSerialization() {
            // Load Avro schema
            String schemaString = """
                {
                    "type": "record",
                    "name": "UserProfile",
                    "fields": [
                        {"name": "userId", "type": "string"},
                        {"name": "name", "type": "string"},
                        {"name": "email", "type": "string"},
                        {"name": "age", "type": "int"},
                        {"name": "lastLoginTime", "type": "long"},
                        {"name": "interests", "type": {"type": "array", "items": "string"}},
                        {"name": "metadata", "type": {"type": "map", "values": "string"}}
                    ]
                }
            """;
            this.schema = new Schema.Parser().parse(schemaString);
        }
        
        public byte[] serialize(UserProfile profile) throws IOException {
            GenericRecord record = new GenericData.Record(schema);
            record.put("userId", profile.getUserId());
            record.put("name", profile.getName());
            record.put("email", profile.getEmail());
            record.put("age", profile.getAge());
            record.put("lastLoginTime", profile.getLastLoginTime());
            record.put("interests", profile.getInterests());
            record.put("metadata", profile.getMetadata());
            
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            DatumWriter<GenericRecord> writer = new GenericDatumWriter<>(schema);
            Encoder encoder = EncoderFactory.get().binaryEncoder(baos, null);
            writer.write(record, encoder);
            encoder.flush();
            
            return baos.toByteArray();
        }
        
        public UserProfile deserialize(byte[] data) throws IOException {
            if (data == null || data.length == 0) {
                return null;
            }
            
            DatumReader<GenericRecord> reader = new GenericDatumReader<>(schema);
            Decoder decoder = DecoderFactory.get().binaryDecoder(data, null);
            GenericRecord record = reader.read(null, decoder);
            
            UserProfile profile = new UserProfile();
            profile.setUserId(record.get("userId").toString());
            profile.setName(record.get("name").toString());
            profile.setEmail(record.get("email").toString());
            profile.setAge((Integer) record.get("age"));
            profile.setLastLoginTime((Long) record.get("lastLoginTime"));
            
            @SuppressWarnings("unchecked")
            List<String> interests = (List<String>) record.get("interests");
            profile.setInterests(interests);
            
            @SuppressWarnings("unchecked")
            Map<String, String> metadata = (Map<String, String>) record.get("metadata");
            profile.setMetadata(metadata);
            
            return profile;
        }
    }
    
    // JSON serialization with compression
    public static class JsonSerialization {
        private ObjectMapper objectMapper;
        
        public JsonSerialization() {
            this.objectMapper = new ObjectMapper();
            this.objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        }
        
        public byte[] serialize(UserProfile profile) throws IOException {
            String json = objectMapper.writeValueAsString(profile);
            
            // Compress JSON
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            try (GZIPOutputStream gzipOut = new GZIPOutputStream(baos)) {
                gzipOut.write(json.getBytes(StandardCharsets.UTF_8));
            }
            
            return baos.toByteArray();
        }
        
        public UserProfile deserialize(byte[] data) throws IOException {
            if (data == null || data.length == 0) {
                return null;
            }
            
            // Decompress JSON
            ByteArrayInputStream bais = new ByteArrayInputStream(data);
            String json;
            try (GZIPInputStream gzipIn = new GZIPInputStream(bais)) {
                json = new String(gzipIn.readAllBytes(), StandardCharsets.UTF_8);
            }
            
            return objectMapper.readValue(json, UserProfile.class);
        }
    }
    
    // Performance comparison utility
    public static class SerializationBenchmark {
        
        public void compareSerializationMethods(UserProfile profile, int iterations) throws IOException {
            // Binary serialization
            long startTime = System.nanoTime();
            for (int i = 0; i < iterations; i++) {
                byte[] data = profile.serialize();
                UserProfile.deserialize(data);
            }
            long binaryTime = System.nanoTime() - startTime;
            
            // Protobuf serialization
            ProtobufSerialization protobuf = new ProtobufSerialization();
            startTime = System.nanoTime();
            for (int i = 0; i < iterations; i++) {
                // Simulate protobuf serialization/deserialization
            }
            long protobufTime = System.nanoTime() - startTime;
            
            // Avro serialization
            AvroSerialization avro = new AvroSerialization();
            startTime = System.nanoTime();
            for (int i = 0; i < iterations; i++) {
                byte[] data = avro.serialize(profile);
                avro.deserialize(data);
            }
            long avroTime = System.nanoTime() - startTime;
            
            // JSON serialization
            JsonSerialization json = new JsonSerialization();
            startTime = System.nanoTime();
            for (int i = 0; i < iterations; i++) {
                byte[] data = json.serialize(profile);
                json.deserialize(data);
            }
            long jsonTime = System.nanoTime() - startTime;
            
            System.out.println("Serialization Performance (ns per operation):");
            System.out.println("Binary: " + (binaryTime / iterations));
            System.out.println("Protobuf: " + (protobufTime / iterations));
            System.out.println("Avro: " + (avroTime / iterations));
            System.out.println("JSON: " + (jsonTime / iterations));
        }
        
        public void compareSizes(UserProfile profile) throws IOException {
            byte[] binaryData = profile.serialize();
            
            AvroSerialization avro = new AvroSerialization();
            byte[] avroData = avro.serialize(profile);
            
            JsonSerialization json = new JsonSerialization();
            byte[] jsonData = json.serialize(profile);
            
            System.out.println("Serialization Sizes (bytes):");
            System.out.println("Binary: " + binaryData.length);
            System.out.println("Avro: " + avroData.length);
            System.out.println("JSON (compressed): " + jsonData.length);
        }
    }
}
```

### 24. How do you implement efficient range queries and pagination in HBase?
**Answer**: Range queries and pagination require careful design of row keys and scan parameters.

```java
public class RangeQueriesAndPagination {
    
    // Time-based range queries
    public class TimeBasedRangeQuery {
        
        public List<Result> queryTimeRange(String deviceId, long startTime, long endTime, 
                                         int limit) throws IOException {
            // Row key format: deviceId_reverseTimestamp
            long reverseEndTime = Long.MAX_VALUE - endTime;
            long reverseStartTime = Long.MAX_VALUE - startTime;
            
            String startRowKey = deviceId + "_" + String.format("%019d", reverseEndTime);
            String endRowKey = deviceId + "_" + String.format("%019d", reverseStartTime);
            
            Scan scan = new Scan();
            scan.setStartRow(Bytes.toBytes(startRowKey));
            scan.setStopRow(Bytes.toBytes(endRowKey));
            scan.setLimit(limit);
            scan.setCaching(Math.min(limit, 1000));
            scan.addFamily(Bytes.toBytes("data"));
            
            List<Result> results = new ArrayList<>();
            ResultScanner scanner = table.getScanner(scan);
            
            try {
                for (Result result : scanner) {
                    results.add(result);
                }
            } finally {
                scanner.close();
            }
            
            return results;
        }
        
        // Paginated time-based query
        public PagedResult<SensorReading> queryTimeRangePaginated(String deviceId, 
                                                                 long startTime, long endTime,
                                                                 int pageSize, String pageToken) 
                                                                 throws IOException {
            long reverseEndTime = Long.MAX_VALUE - endTime;
            long reverseStartTime = Long.MAX_VALUE - startTime;
            
            String startRowKey;
            if (pageToken != null && !pageToken.isEmpty()) {
                // Continue from page token
                startRowKey = new String(Base64.getDecoder().decode(pageToken));
            } else {
                // Start from beginning
                startRowKey = deviceId + "_" + String.format("%019d", reverseEndTime);
            }
            
            String endRowKey = deviceId + "_" + String.format("%019d", reverseStartTime);
            
            Scan scan = new Scan();
            scan.setStartRow(Bytes.toBytes(startRowKey));
            scan.setStopRow(Bytes.toBytes(endRowKey));
            scan.setLimit(pageSize + 1); // Get one extra to check if more pages exist
            scan.setCaching(pageSize);
            
            List<SensorReading> readings = new ArrayList<>();
            String nextPageToken = null;
            
            ResultScanner scanner = table.getScanner(scan);
            
            try {
                int count = 0;
                for (Result result : scanner) {
                    if (count < pageSize) {
                        SensorReading reading = convertToSensorReading(result);
                        readings.add(reading);
                    } else {
                        // More results available, create next page token
                        nextPageToken = Base64.getEncoder().encodeToString(result.getRow());
                        break;
                    }
                    count++;
                }
            } finally {
                scanner.close();
            }
            
            return new PagedResult<>(readings, nextPageToken);
        }
    }
    
    // Geographic range queries
    public class GeographicRangeQuery {
        
        // Row key format: geohash_timestamp_deviceId
        public List<Result> queryGeographicRange(double minLat, double maxLat, 
                                                double minLon, double maxLon,
                                                long startTime, long endTime) throws IOException {
            
            // Generate geohash ranges for the bounding box
            List<String> geohashRanges = generateGeohashRanges(minLat, maxLat, minLon, maxLon);
            
            List<Result> allResults = new ArrayList<>();
            
            for (String geohashPrefix : geohashRanges) {
                List<Result> rangeResults = queryGeohashRange(geohashPrefix, startTime, endTime);
                allResults.addAll(rangeResults);
            }
            
            // Sort by timestamp
            allResults.sort((r1, r2) -> {
                long ts1 = extractTimestampFromRowKey(r1.getRow());
                long ts2 = extractTimestampFromRowKey(r2.getRow());
                return Long.compare(ts2, ts1); // Descending order
            });
            
            return allResults;
        }
        
        private List<Result> queryGeohashRange(String geohashPrefix, long startTime, long endTime) 
                throws IOException {
            
            String startRowKey = geohashPrefix + "_" + String.format("%019d", Long.MAX_VALUE - endTime);
            String endRowKey = geohashPrefix + "_" + String.format("%019d", Long.MAX_VALUE - startTime);
            
            Scan scan = new Scan();
            scan.setStartRow(Bytes.toBytes(startRowKey));
            scan.setStopRow(Bytes.toBytes(endRowKey));
            scan.setCaching(1000);
            
            List<Result> results = new ArrayList<>();
            ResultScanner scanner = table.getScanner(scan);
            
            try {
                for (Result result : scanner) {
                    results.add(result);
                }
            } finally {
                scanner.close();
            }
            
            return results;
        }
        
        private List<String> generateGeohashRanges(double minLat, double maxLat, 
                                                  double minLon, double maxLon) {
            // Simplified geohash range generation
            // In practice, use a proper geohash library
            List<String> ranges = new ArrayList<>();
            
            // Generate geohash prefixes that cover the bounding box
            int precision = 6; // Adjust based on query precision needs
            
            for (double lat = minLat; lat <= maxLat; lat += 0.01) {
                for (double lon = minLon; lon <= maxLon; lon += 0.01) {
                    String geohash = encodeGeohash(lat, lon, precision);
                    String prefix = geohash.substring(0, Math.min(4, geohash.length()));
                    if (!ranges.contains(prefix)) {
                        ranges.add(prefix);
                    }
                }
            }
            
            return ranges;
        }
        
        private String encodeGeohash(double lat, double lon, int precision) {
            // Simplified geohash encoding
            // Use proper geohash library in production
            return "geohash_" + lat + "_" + lon;
        }
        
        private long extractTimestampFromRowKey(byte[] rowKey) {
            String key = Bytes.toString(rowKey);
            String[] parts = key.split("_");
            if (parts.length >= 2) {
                return Long.MAX_VALUE - Long.parseLong(parts[1]);
            }
            return 0;
        }
    }
    
    // Cursor-based pagination
    public class CursorBasedPagination {
        
        public PagedResult<UserData> getUsersPaginated(int pageSize, String cursor) 
                throws IOException {
            
            Scan scan = new Scan();
            
            if (cursor != null && !cursor.isEmpty()) {
                // Decode cursor to get last row key
                byte[] lastRowKey = Base64.getDecoder().decode(cursor);
                scan.setStartRow(Bytes.add(lastRowKey, new byte[]{0})); // Start after last row
            }
            
            scan.setLimit(pageSize + 1); // Get one extra to check for more pages
            scan.setCaching(pageSize);
            scan.addFamily(Bytes.toBytes("profile"));
            
            List<UserData> users = new ArrayList<>();
            String nextCursor = null;
            
            ResultScanner scanner = table.getScanner(scan);
            
            try {
                int count = 0;
                Result lastResult = null;
                
                for (Result result : scanner) {
                    if (count < pageSize) {
                        UserData user = convertToUserData(result);
                        users.add(user);
                        lastResult = result;
                    } else {
                        // More results available
                        nextCursor = Base64.getEncoder().encodeToString(lastResult.getRow());
                        break;
                    }
                    count++;
                }
                
                // If we got exactly pageSize results and no extra, check if more exist
                if (count == pageSize && nextCursor == null) {
                    nextCursor = Base64.getEncoder().encodeToString(lastResult.getRow());
                }
                
            } finally {
                scanner.close();
            }
            
            return new PagedResult<>(users, nextCursor);
        }
    }
    
    // Offset-based pagination (less efficient but sometimes needed)
    public class OffsetBasedPagination {
        
        public PagedResult<UserData> getUsersWithOffset(int offset, int limit) throws IOException {
            Scan scan = new Scan();
            scan.setCaching(1000);
            scan.addFamily(Bytes.toBytes("profile"));
            
            List<UserData> users = new ArrayList<>();
            int currentOffset = 0;
            int collected = 0;
            
            ResultScanner scanner = table.getScanner(scan);
            
            try {
                for (Result result : scanner) {
                    if (currentOffset < offset) {
                        currentOffset++;
                        continue;
                    }
                    
                    if (collected >= limit) {
                        break;
                    }
                    
                    UserData user = convertToUserData(result);
                    users.add(user);
                    collected++;
                }
            } finally {
                scanner.close();
            }
            
            // Check if more results exist
            boolean hasMore = collected == limit;
            String nextPageToken = hasMore ? String.valueOf(offset + limit) : null;
            
            return new PagedResult<>(users, nextPageToken);
        }
    }
    
    // Parallel range queries
    public class ParallelRangeQuery {
        
        public List<Result> parallelRangeQuery(List<String> deviceIds, long startTime, long endTime) 
                throws InterruptedException, ExecutionException {
            
            ExecutorService executor = Executors.newFixedThreadPool(deviceIds.size());
            List<Future<List<Result>>> futures = new ArrayList<>();
            
            for (String deviceId : deviceIds) {
                Future<List<Result>> future = executor.submit(() -> {
                    try {
                        return queryDeviceTimeRange(deviceId, startTime, endTime);
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                });
                futures.add(future);
            }
            
            List<Result> allResults = new ArrayList<>();
            
            for (Future<List<Result>> future : futures) {
                List<Result> results = future.get();
                allResults.addAll(results);
            }
            
            executor.shutdown();
            
            // Sort combined results by timestamp
            allResults.sort((r1, r2) -> {
                long ts1 = extractTimestampFromResult(r1);
                long ts2 = extractTimestampFromResult(r2);
                return Long.compare(ts2, ts1);
            });
            
            return allResults;
        }
        
        private List<Result> queryDeviceTimeRange(String deviceId, long startTime, long endTime) 
                throws IOException {
            
            TimeBasedRangeQuery timeQuery = new TimeBasedRangeQuery();
            return timeQuery.queryTimeRange(deviceId, startTime, endTime, 10000);
        }
        
        private long extractTimestampFromResult(Result result) {
            // Extract timestamp from row key or cell timestamp
            return result.rawCells()[0].getTimestamp();
        }
    }
    
    // Helper classes
    public static class PagedResult<T> {
        private final List<T> data;
        private final String nextPageToken;
        
        public PagedResult(List<T> data, String nextPageToken) {
            this.data = data;
            this.nextPageToken = nextPageToken;
        }
        
        public List<T> getData() { return data; }
        public String getNextPageToken() { return nextPageToken; }
        public boolean hasMore() { return nextPageToken != null; }
    }
    
    public static class SensorReading {
        private String deviceId;
        private long timestamp;
        private Map<String, Double> readings;
        
        // Constructors, getters, setters...
    }
    
    public static class UserData {
        private String userId;
        private String name;
        private String email;
        
        // Constructors, getters, setters...
    }
    
    // Conversion utilities
    private SensorReading convertToSensorReading(Result result) {
        // Convert HBase Result to SensorReading object
        SensorReading reading = new SensorReading();
        
        String rowKey = Bytes.toString(result.getRow());
        String[] parts = rowKey.split("_");
        reading.setDeviceId(parts[0]);
        reading.setTimestamp(Long.MAX_VALUE - Long.parseLong(parts[1]));
        
        // Extract sensor readings from columns
        Map<String, Double> readings = new HashMap<>();
        NavigableMap<byte[], byte[]> familyMap = result.getFamilyMap(Bytes.toBytes("data"));
        
        for (Map.Entry<byte[], byte[]> entry : familyMap.entrySet()) {
            String sensorName = Bytes.toString(entry.getKey());
            Double value = Double.parseDouble(Bytes.toString(entry.getValue()));
            readings.put(sensorName, value);
        }
        
        reading.setReadings(readings);
        return reading;
    }
    
    private UserData convertToUserData(Result result) {
        // Convert HBase Result to UserData object
        UserData user = new UserData();
        user.setUserId(Bytes.toString(result.getRow()));
        
        byte[] name = result.getValue(Bytes.toBytes("profile"), Bytes.toBytes("name"));
        if (name != null) {
            user.setName(Bytes.toString(name));
        }
        
        byte[] email = result.getValue(Bytes.toBytes("profile"), Bytes.toBytes("email"));
        if (email != null) {
            user.setEmail(Bytes.toString(email));
        }
        
        return user;
    }
}
```

### 25. How do you implement multi-tenancy in HBase?
**Answer**: Multi-tenancy allows multiple tenants to share HBase resources while maintaining isolation.

```java
public class MultiTenancy {
    
    // Namespace-based multi-tenancy
    public class NamespaceBasedMultiTenancy {
        
        public void setupTenantNamespace(String tenantId) throws IOException {
            Admin admin = connection.getAdmin();
            
            // Create namespace for tenant
            NamespaceDescriptor namespaceDesc = NamespaceDescriptor.create(tenantId)
                .addConfiguration("hbase.namespace.quota.maxtables", "100")
                .addConfiguration("hbase.namespace.quota.maxregions", "1000")
                .build();
            
            try {
                admin.createNamespace(namespaceDesc);
            } catch (NamespaceExistException e) {
                // Namespace already exists
                System.out.println("Namespace " + tenantId + " already exists");
            }
            
            // Set resource quotas for namespace
            QuotaSettings quotaSettings = QuotaSettingsFactory.limitNamespaceSpace(
                tenantId, 100L * 1024 * 1024 * 1024); // 100GB limit
            admin.setQuota(quotaSettings);
            
            // Set throttle quotas
            QuotaSettings throttleSettings = QuotaSettingsFactory.throttleNamespace(
                tenantId, ThrottleType.REQUEST_NUMBER, 10000, TimeUnit.SECONDS);
            admin.setQuota(throttleSettings);
        }
        
        public void createTenantTable(String tenantId, String tableName, 
                                    String[] columnFamilies) throws IOException {
            Admin admin = connection.getAdmin();
            
            // Create table in tenant namespace
            TableName qualifiedTableName = TableName.valueOf(tenantId, tableName);
            
            TableDescriptorBuilder builder = TableDescriptorBuilder.newBuilder(qualifiedTableName);
            
            for (String cf : columnFamilies) {
                ColumnFamilyDescriptor cfDesc = ColumnFamilyDescriptorBuilder
                    .newBuilder(Bytes.toBytes(cf))
                    .setMaxVersions(1)
                    .setCompressionType(Compression.Algorithm.SNAPPY)
                    .build();
                builder.setColumnFamily(cfDesc);
            }
            
            admin.createTable(builder.build());
            
            // Set table-level quotas
            QuotaSettings tableQuota = QuotaSettingsFactory.limitTableSpace(
                qualifiedTableName, 10L * 1024 * 1024 * 1024); // 10GB per table
            admin.setQuota(tableQuota);
        }
        
        public Table getTenantTable(String tenantId, String tableName) throws IOException {
            TableName qualifiedTableName = TableName.valueOf(tenantId, tableName);
            return connection.getTable(qualifiedTableName);
        }
    }
    
    // Row-key prefix based multi-tenancy
    public class RowKeyPrefixMultiTenancy {
        
        public void insertTenantData(String tenantId, String entityId, 
                                   Map<String, String> data) throws IOException {
            // Row key format: tenantId_entityId
            String rowKey = tenantId + "_" + entityId;
            
            Put put = new Put(Bytes.toBytes(rowKey));
            
            for (Map.Entry<String, String> entry : data.entrySet()) {
                put.addColumn(Bytes.toBytes("data"), Bytes.toBytes(entry.getKey()), 
                             Bytes.toBytes(entry.getValue()));
            }
            
            // Add tenant metadata
            put.addColumn(Bytes.toBytes("meta"), Bytes.toBytes("tenant_id"), 
                         Bytes.toBytes(tenantId));
            put.addColumn(Bytes.toBytes("meta"), Bytes.toBytes("created_time"), 
                         Bytes.toBytes(System.currentTimeMillis()));
            
            table.put(put);
        }
        
        public List<Result> queryTenantData(String tenantId, int limit) throws IOException {
            // Scan with tenant prefix
            Scan scan = new Scan();
            scan.setStartRow(Bytes.toBytes(tenantId + "_"));
            scan.setStopRow(Bytes.toBytes(tenantId + "_" + "~")); // ~ is after all chars
            scan.setLimit(limit);
            scan.setCaching(1000);
            
            // Add filter to ensure tenant isolation
            Filter tenantFilter = new SingleColumnValueFilter(
                Bytes.toBytes("meta"), Bytes.toBytes("tenant_id"),
                CompareOperator.EQUAL, Bytes.toBytes(tenantId)
            );
            scan.setFilter(tenantFilter);
            
            List<Result> results = new ArrayList<>();
            ResultScanner scanner = table.getScanner(scan);
            
            try {
                for (Result result : scanner) {
                    results.add(result);
                }
            } finally {
                scanner.close();
            }
            
            return results;
        }
        
        public void deleteTenantData(String tenantId) throws IOException {
            // Scan and delete all tenant data
            Scan scan = new Scan();
            scan.setStartRow(Bytes.toBytes(tenantId + "_"));
            scan.setStopRow(Bytes.toBytes(tenantId + "_" + "~"));
            scan.setFilter(new KeyOnlyFilter()); // Only need row keys
            
            List<Delete> deletes = new ArrayList<>();
            ResultScanner scanner = table.getScanner(scan);
            
            try {
                for (Result result : scanner) {
                    Delete delete = new Delete(result.getRow());
                    deletes.add(delete);
                    
                    // Batch delete every 1000 rows
                    if (deletes.size() >= 1000) {
                        table.delete(deletes);
                        deletes.clear();
                    }
                }
                
                // Delete remaining rows
                if (!deletes.isEmpty()) {
                    table.delete(deletes);
                }
            } finally {
                scanner.close();
            }
        }
    }
    
    // Security-based multi-tenancy
    public class SecurityBasedMultiTenancy {
        
        public void setupTenantSecurity(String tenantId, List<String> tenantUsers) 
                throws IOException {
            Admin admin = connection.getAdmin();
            
            // Create tenant-specific tables
            TableName tenantTable = TableName.valueOf("tenant_" + tenantId + "_data");
            
            TableDescriptor tableDesc = TableDescriptorBuilder
                .newBuilder(tenantTable)
                .setColumnFamily(ColumnFamilyDescriptorBuilder.of("data"))
                .build();
            
            admin.createTable(tableDesc);
            
            // Grant permissions to tenant users
            for (String user : tenantUsers) {
                // Grant read/write access to tenant table
                admin.grant(new UserPermission(user,
                    Permission.newBuilder(tenantTable)
                        .withActions(Permission.Action.READ, Permission.Action.WRITE)
                        .build()));
                
                // Deny access to other tenant tables
                denyAccessToOtherTenants(admin, user, tenantId);
            }
        }
        
        private void denyAccessToOtherTenants(Admin admin, String user, String currentTenantId) 
                throws IOException {
            // Get all tables and revoke access to other tenant tables
            List<TableDescriptor> tables = admin.listTableDescriptors();
            
            for (TableDescriptor table : tables) {
                String tableName = table.getTableName().getNameAsString();
                if (tableName.startsWith("tenant_") && !tableName.contains(currentTenantId)) {
                    // This is another tenant's table, ensure no access
                    try {
                        admin.revoke(new UserPermission(user,
                            Permission.newBuilder(table.getTableName())
                                .withActions(Permission.Action.READ, Permission.Action.WRITE)
                                .build()));
                    } catch (Exception e) {
                        // Permission might not exist, ignore
                    }
                }
            }
        }
        
        // Cell-level security for multi-tenancy
        public void setupCellLevelSecurity(String tenantId) throws IOException {
            // Set up visibility labels for tenant
            VisibilityLabelsRequest.Builder builder = VisibilityLabelsRequest.newBuilder();
            builder.addVisLabel(ByteString.copyFromUtf8("TENANT_" + tenantId));
            
            // Configure user authorizations
            SetAuthsRequest authsRequest = SetAuthsRequest.newBuilder()
                .setUser(ByteString.copyFromUtf8("tenant_user_" + tenantId))
                .addAuth(ByteString.copyFromUtf8("TENANT_" + tenantId))
                .build();
        }
        
        public void insertTenantDataWithSecurity(String tenantId, String rowKey, 
                                               Map<String, String> data) throws IOException {
            Put put = new Put(Bytes.toBytes(rowKey));
            
            for (Map.Entry<String, String> entry : data.entrySet()) {
                put.addColumn(Bytes.toBytes("data"), Bytes.toBytes(entry.getKey()), 
                             Bytes.toBytes(entry.getValue()));
            }
            
            // Set cell visibility for tenant isolation
            put.setCellVisibility(new CellVisibility("TENANT_" + tenantId));
            
            Table tenantTable = connection.getTable(TableName.valueOf("tenant_" + tenantId + "_data"));
            tenantTable.put(put);
            tenantTable.close();
        }
    }
    
    // Resource monitoring and management
    public class TenantResourceMonitor {
        
        public TenantResourceUsage getTenantResourceUsage(String tenantId) throws IOException {
            Admin admin = connection.getAdmin();
            
            TenantResourceUsage usage = new TenantResourceUsage(tenantId);
            
            // Get namespace quotas
            List<QuotaSettings> quotas = admin.getQuota(null);
            for (QuotaSettings quota : quotas) {
                if (quota.getNamespace() != null && quota.getNamespace().equals(tenantId)) {
                    if (quota instanceof SpaceQuotaSettings) {
                        SpaceQuotaSettings spaceQuota = (SpaceQuotaSettings) quota;
                        usage.setSpaceQuota(spaceQuota.getSoftLimit());
                    }
                }
            }
            
            // Calculate actual usage
            long totalSize = 0;
            int tableCount = 0;
            
            List<TableDescriptor> tables = admin.listTableDescriptorsByNamespace(tenantId);
            for (TableDescriptor table : tables) {
                tableCount++;
                
                // Get table size (simplified - in practice use HBase metrics)
                ClusterMetrics metrics = admin.getClusterMetrics();
                for (ServerMetrics serverMetrics : metrics.getLiveServerMetrics().values()) {
                    Map<byte[], RegionMetrics> regionMetrics = serverMetrics.getRegionMetrics();
                    for (RegionMetrics regionMetric : regionMetrics.values()) {
                        if (Bytes.toString(regionMetric.getRegionName()).contains(table.getTableName().getNameAsString())) {
                            totalSize += regionMetric.getStoreFileSize();
                        }
                    }
                }
            }
            
            usage.setActualSpaceUsage(totalSize);
            usage.setTableCount(tableCount);
            
            return usage;
        }
        
        public void enforceTenantQuotas(String tenantId) throws IOException {
            TenantResourceUsage usage = getTenantResourceUsage(tenantId);
            
            // Check if tenant exceeds quotas
            if (usage.getActualSpaceUsage() > usage.getSpaceQuota()) {
                // Implement quota enforcement
                System.out.println("Tenant " + tenantId + " exceeds space quota");
                
                // Options:
                // 1. Throttle writes
                // 2. Send alerts
                // 3. Disable tables
                // 4. Delete old data
                
                throttleTenantWrites(tenantId);
            }
        }
        
        private void throttleTenantWrites(String tenantId) throws IOException {
            Admin admin = connection.getAdmin();
            
            // Set aggressive write throttling
            QuotaSettings throttleSettings = QuotaSettingsFactory.throttleNamespace(
                tenantId, ThrottleType.WRITE_NUMBER, 100, TimeUnit.SECONDS);
            admin.setQuota(throttleSettings);
        }
    }
    
    // Tenant data migration
    public class TenantDataMigration {
        
        public void migrateTenantToNewCluster(String tenantId, Connection targetConnection) 
                throws IOException {
            
            // Export tenant data
            List<TableDescriptor> tables = connection.getAdmin().listTableDescriptorsByNamespace(tenantId);
            
            for (TableDescriptor tableDesc : tables) {
                migrateTenantTable(tableDesc.getTableName(), targetConnection);
            }
        }
        
        private void migrateTenantTable(TableName tableName, Connection targetConnection) 
                throws IOException {
            
            // Create table in target cluster
            Admin targetAdmin = targetConnection.getAdmin();
            TableDescriptor sourceTableDesc = connection.getAdmin().getDescriptor(tableName);
            
            if (!targetAdmin.tableExists(tableName)) {
                targetAdmin.createTable(sourceTableDesc);
            }
            
            // Copy data
            Table sourceTable = connection.getTable(tableName);
            Table targetTable = targetConnection.getTable(tableName);
            
            Scan scan = new Scan();
            scan.setCaching(1000);
            
            ResultScanner scanner = sourceTable.getScanner(scan);
            List<Put> puts = new ArrayList<>();
            
            try {
                for (Result result : scanner) {
                    Put put = new Put(result.getRow());
                    
                    for (Cell cell : result.rawCells()) {
                        put.add(cell);
                    }
                    
                    puts.add(put);
                    
                    // Batch insert
                    if (puts.size() >= 1000) {
                        targetTable.put(puts);
                        puts.clear();
                    }
                }
                
                // Insert remaining data
                if (!puts.isEmpty()) {
                    targetTable.put(puts);
                }
            } finally {
                scanner.close();
                sourceTable.close();
                targetTable.close();
            }
        }
    }
    
    // Helper classes
    public static class TenantResourceUsage {
        private String tenantId;
        private long spaceQuota;
        private long actualSpaceUsage;
        private int tableCount;
        
        public TenantResourceUsage(String tenantId) {
            this.tenantId = tenantId;
        }
        
        // Getters and setters...
        public String getTenantId() { return tenantId; }
        public long getSpaceQuota() { return spaceQuota; }
        public void setSpaceQuota(long spaceQuota) { this.spaceQuota = spaceQuota; }
        public long getActualSpaceUsage() { return actualSpaceUsage; }
        public void setActualSpaceUsage(long actualSpaceUsage) { this.actualSpaceUsage = actualSpaceUsage; }
        public int getTableCount() { return tableCount; }
        public void setTableCount(int tableCount) { this.tableCount = tableCount; }
    }
}
```

---

I'll continue with the remaining sections (Architecture & Performance, Streaming & Real-time Processing, Production & Operations, and Scenario-Based Questions) in the next batch to complete the comprehensive interview questions file.
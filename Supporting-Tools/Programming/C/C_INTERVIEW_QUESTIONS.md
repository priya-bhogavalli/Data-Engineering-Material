# C Programming Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts Questions (1-15)](#core-concepts-questions-1-15)
2. [Memory Management Questions (16-30)](#memory-management-questions-16-30)
3. [Data Structures Questions (31-45)](#data-structures-questions-31-45)
4. [System Programming Questions (46-60)](#system-programming-questions-46-60)

---

## 🎯 **Introduction**

C programming is fundamental for data engineers working on system-level programming, performance-critical applications, and understanding how higher-level data tools work under the hood.

**Why C is Important for Data Engineers:**
- **Performance**: Low-level control for high-performance computing
- **System Programming**: Building data processing tools and drivers
- **Memory Management**: Understanding memory-efficient data structures
- **Foundation**: Understanding how databases and data tools are built
- **Integration**: Writing C extensions for Python/other languages

---

## Core Concepts Questions (1-15)

### 1. What are the key differences between C and higher-level languages used in data engineering?
**Answer**: 
C provides low-level control that's essential for understanding data system internals.

**Key Differences:**
- **Memory Management**: Manual memory allocation/deallocation
- **Performance**: Direct hardware access, no garbage collection overhead
- **Pointers**: Direct memory address manipulation
- **Compilation**: Compiled to machine code vs interpreted
- **Type System**: Static typing with explicit type conversions

```c
// C - Manual memory management
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    size_t size;
    size_t capacity;
} DataArray;

DataArray* create_array(size_t initial_capacity) {
    DataArray *arr = malloc(sizeof(DataArray));
    if (!arr) return NULL;
    
    arr->data = malloc(initial_capacity * sizeof(int));
    if (!arr->data) {
        free(arr);
        return NULL;
    }
    
    arr->size = 0;
    arr->capacity = initial_capacity;
    return arr;
}

void destroy_array(DataArray *arr) {
    if (arr) {
        free(arr->data);
        free(arr);
    }
}
```

### 2. How do you implement efficient data structures in C for data processing?
**Answer**: Efficient data structures require careful memory layout and access patterns.

```c
// Hash table for data aggregation
#define HASH_SIZE 1024

typedef struct HashNode {
    char *key;
    long long value;
    struct HashNode *next;
} HashNode;

typedef struct {
    HashNode *buckets[HASH_SIZE];
    size_t count;
} HashTable;

unsigned int hash_function(const char *key) {
    unsigned int hash = 5381;
    int c;
    while ((c = *key++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash % HASH_SIZE;
}

void hash_insert(HashTable *table, const char *key, long long value) {
    unsigned int index = hash_function(key);
    HashNode *node = table->buckets[index];
    
    // Check if key exists
    while (node) {
        if (strcmp(node->key, key) == 0) {
            node->value += value;  // Aggregate values
            return;
        }
        node = node->next;
    }
    
    // Create new node
    HashNode *new_node = malloc(sizeof(HashNode));
    new_node->key = strdup(key);
    new_node->value = value;
    new_node->next = table->buckets[index];
    table->buckets[index] = new_node;
    table->count++;
}
```

### 3. How do you handle file I/O efficiently in C for data processing?
**Answer**: Efficient file I/O strategies for large datasets.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 8192

// Buffered file reader for CSV processing
typedef struct {
    FILE *file;
    char buffer[BUFFER_SIZE];
    size_t buffer_pos;
    size_t buffer_size;
    int eof_reached;
} BufferedReader;

BufferedReader* create_reader(const char *filename) {
    BufferedReader *reader = malloc(sizeof(BufferedReader));
    if (!reader) return NULL;
    
    reader->file = fopen(filename, "r");
    if (!reader->file) {
        free(reader);
        return NULL;
    }
    
    reader->buffer_pos = 0;
    reader->buffer_size = 0;
    reader->eof_reached = 0;
    
    return reader;
}

int read_line(BufferedReader *reader, char *line, size_t max_len) {
    size_t line_pos = 0;
    
    while (line_pos < max_len - 1) {
        // Refill buffer if needed
        if (reader->buffer_pos >= reader->buffer_size) {
            reader->buffer_size = fread(reader->buffer, 1, BUFFER_SIZE, reader->file);
            reader->buffer_pos = 0;
            
            if (reader->buffer_size == 0) {
                reader->eof_reached = 1;
                break;
            }
        }
        
        char c = reader->buffer[reader->buffer_pos++];
        
        if (c == '\n') {
            break;
        }
        
        line[line_pos++] = c;
    }
    
    line[line_pos] = '\0';
    return line_pos > 0 || !reader->eof_reached;
}

// CSV parser
typedef struct {
    char **fields;
    size_t field_count;
    size_t capacity;
} CSVRow;

CSVRow* parse_csv_line(const char *line) {
    CSVRow *row = malloc(sizeof(CSVRow));
    row->capacity = 16;
    row->fields = malloc(row->capacity * sizeof(char*));
    row->field_count = 0;
    
    char *line_copy = strdup(line);
    char *token = strtok(line_copy, ",");
    
    while (token) {
        if (row->field_count >= row->capacity) {
            row->capacity *= 2;
            row->fields = realloc(row->fields, row->capacity * sizeof(char*));
        }
        
        row->fields[row->field_count++] = strdup(token);
        token = strtok(NULL, ",");
    }
    
    free(line_copy);
    return row;
}
```

### 4. How do you implement memory-efficient data aggregation in C?
**Answer**: Memory-efficient aggregation using streaming algorithms.

```c
// Streaming statistics calculator
typedef struct {
    long long count;
    double sum;
    double sum_squares;
    double min_value;
    double max_value;
} StreamingStats;

void init_stats(StreamingStats *stats) {
    stats->count = 0;
    stats->sum = 0.0;
    stats->sum_squares = 0.0;
    stats->min_value = INFINITY;
    stats->max_value = -INFINITY;
}

void update_stats(StreamingStats *stats, double value) {
    stats->count++;
    stats->sum += value;
    stats->sum_squares += value * value;
    
    if (value < stats->min_value) {
        stats->min_value = value;
    }
    if (value > stats->max_value) {
        stats->max_value = value;
    }
}

double get_mean(const StreamingStats *stats) {
    return stats->count > 0 ? stats->sum / stats->count : 0.0;
}

double get_variance(const StreamingStats *stats) {
    if (stats->count <= 1) return 0.0;
    
    double mean = get_mean(stats);
    return (stats->sum_squares - stats->count * mean * mean) / (stats->count - 1);
}

// Group-by aggregation
typedef struct GroupStats {
    char *group_key;
    StreamingStats stats;
    struct GroupStats *next;
} GroupStats;

typedef struct {
    GroupStats *groups[HASH_SIZE];
} GroupAggregator;

void aggregate_by_group(GroupAggregator *agg, const char *group, double value) {
    unsigned int index = hash_function(group);
    GroupStats *current = agg->groups[index];
    
    // Find existing group
    while (current) {
        if (strcmp(current->group_key, group) == 0) {
            update_stats(&current->stats, value);
            return;
        }
        current = current->next;
    }
    
    // Create new group
    GroupStats *new_group = malloc(sizeof(GroupStats));
    new_group->group_key = strdup(group);
    init_stats(&new_group->stats);
    update_stats(&new_group->stats, value);
    new_group->next = agg->groups[index];
    agg->groups[index] = new_group;
}
```

## Memory Management Questions (16-30)

### 5. How do you prevent memory leaks in data processing applications?
**Answer**: Memory leak prevention strategies and tools.

```c
// Memory pool for efficient allocation
typedef struct MemoryBlock {
    void *data;
    size_t size;
    int in_use;
    struct MemoryBlock *next;
} MemoryBlock;

typedef struct {
    MemoryBlock *blocks;
    size_t total_allocated;
    size_t total_used;
} MemoryPool;

MemoryPool* create_memory_pool() {
    MemoryPool *pool = malloc(sizeof(MemoryPool));
    if (!pool) return NULL;
    
    pool->blocks = NULL;
    pool->total_allocated = 0;
    pool->total_used = 0;
    
    return pool;
}

void* pool_alloc(MemoryPool *pool, size_t size) {
    // Try to find a free block of sufficient size
    MemoryBlock *block = pool->blocks;
    while (block) {
        if (!block->in_use && block->size >= size) {
            block->in_use = 1;
            pool->total_used += block->size;
            return block->data;
        }
        block = block->next;
    }
    
    // Allocate new block
    MemoryBlock *new_block = malloc(sizeof(MemoryBlock));
    if (!new_block) return NULL;
    
    new_block->data = malloc(size);
    if (!new_block->data) {
        free(new_block);
        return NULL;
    }
    
    new_block->size = size;
    new_block->in_use = 1;
    new_block->next = pool->blocks;
    pool->blocks = new_block;
    
    pool->total_allocated += size;
    pool->total_used += size;
    
    return new_block->data;
}

void pool_free(MemoryPool *pool, void *ptr) {
    MemoryBlock *block = pool->blocks;
    while (block) {
        if (block->data == ptr && block->in_use) {
            block->in_use = 0;
            pool->total_used -= block->size;
            return;
        }
        block = block->next;
    }
}

void destroy_memory_pool(MemoryPool *pool) {
    if (!pool) return;
    
    MemoryBlock *block = pool->blocks;
    while (block) {
        MemoryBlock *next = block->next;
        free(block->data);
        free(block);
        block = next;
    }
    
    free(pool);
}
```

### 6. How do you implement cache-friendly data structures?
**Answer**: Cache-optimized data structures for better performance.

```c
// Cache-friendly array of structures vs structure of arrays
// Less cache-friendly: Array of Structures (AoS)
typedef struct {
    int id;
    double value;
    char category[16];
    long timestamp;
} Record_AoS;

// More cache-friendly: Structure of Arrays (SoA)
typedef struct {
    int *ids;
    double *values;
    char (*categories)[16];
    long *timestamps;
    size_t count;
    size_t capacity;
} Records_SoA;

// Process only values (cache-friendly with SoA)
double sum_values_soa(const Records_SoA *records) {
    double sum = 0.0;
    for (size_t i = 0; i < records->count; i++) {
        sum += records->values[i];  // Sequential memory access
    }
    return sum;
}

// Cache-friendly matrix operations
typedef struct {
    double *data;
    size_t rows;
    size_t cols;
} Matrix;

// Row-major matrix multiplication (cache-friendly)
void matrix_multiply(const Matrix *a, const Matrix *b, Matrix *result) {
    for (size_t i = 0; i < a->rows; i++) {
        for (size_t j = 0; j < b->cols; j++) {
            double sum = 0.0;
            for (size_t k = 0; k < a->cols; k++) {
                sum += a->data[i * a->cols + k] * b->data[k * b->cols + j];
            }
            result->data[i * result->cols + j] = sum;
        }
    }
}
```

## Data Structures Questions (31-45)

### 7. How do you implement a high-performance priority queue for data processing?
**Answer**: Binary heap implementation for efficient priority operations.

```c
typedef struct {
    double priority;
    void *data;
} PriorityItem;

typedef struct {
    PriorityItem *items;
    size_t size;
    size_t capacity;
    int (*compare)(double a, double b);  // Comparison function
} PriorityQueue;

PriorityQueue* create_priority_queue(size_t initial_capacity, int (*cmp)(double, double)) {
    PriorityQueue *pq = malloc(sizeof(PriorityQueue));
    if (!pq) return NULL;
    
    pq->items = malloc(initial_capacity * sizeof(PriorityItem));
    if (!pq->items) {
        free(pq);
        return NULL;
    }
    
    pq->size = 0;
    pq->capacity = initial_capacity;
    pq->compare = cmp;
    
    return pq;
}

void heapify_up(PriorityQueue *pq, size_t index) {
    if (index == 0) return;
    
    size_t parent = (index - 1) / 2;
    if (pq->compare(pq->items[index].priority, pq->items[parent].priority) > 0) {
        // Swap with parent
        PriorityItem temp = pq->items[index];
        pq->items[index] = pq->items[parent];
        pq->items[parent] = temp;
        
        heapify_up(pq, parent);
    }
}

void heapify_down(PriorityQueue *pq, size_t index) {
    size_t left = 2 * index + 1;
    size_t right = 2 * index + 2;
    size_t largest = index;
    
    if (left < pq->size && 
        pq->compare(pq->items[left].priority, pq->items[largest].priority) > 0) {
        largest = left;
    }
    
    if (right < pq->size && 
        pq->compare(pq->items[right].priority, pq->items[largest].priority) > 0) {
        largest = right;
    }
    
    if (largest != index) {
        PriorityItem temp = pq->items[index];
        pq->items[index] = pq->items[largest];
        pq->items[largest] = temp;
        
        heapify_down(pq, largest);
    }
}

int pq_insert(PriorityQueue *pq, double priority, void *data) {
    if (pq->size >= pq->capacity) {
        size_t new_capacity = pq->capacity * 2;
        PriorityItem *new_items = realloc(pq->items, new_capacity * sizeof(PriorityItem));
        if (!new_items) return 0;
        
        pq->items = new_items;
        pq->capacity = new_capacity;
    }
    
    pq->items[pq->size].priority = priority;
    pq->items[pq->size].data = data;
    
    heapify_up(pq, pq->size);
    pq->size++;
    
    return 1;
}

PriorityItem* pq_extract_max(PriorityQueue *pq) {
    if (pq->size == 0) return NULL;
    
    static PriorityItem result;
    result = pq->items[0];
    
    pq->items[0] = pq->items[pq->size - 1];
    pq->size--;
    
    if (pq->size > 0) {
        heapify_down(pq, 0);
    }
    
    return &result;
}
```

### 8. How do you implement a lock-free data structure for concurrent data processing?
**Answer**: Lock-free queue implementation using atomic operations.

```c
#include <stdatomic.h>

typedef struct Node {
    atomic_uintptr_t data;
    atomic_uintptr_t next;
} Node;

typedef struct {
    atomic_uintptr_t head;
    atomic_uintptr_t tail;
} LockFreeQueue;

LockFreeQueue* create_lockfree_queue() {
    LockFreeQueue *queue = malloc(sizeof(LockFreeQueue));
    if (!queue) return NULL;
    
    Node *dummy = malloc(sizeof(Node));
    if (!dummy) {
        free(queue);
        return NULL;
    }
    
    atomic_store(&dummy->data, 0);
    atomic_store(&dummy->next, 0);
    
    atomic_store(&queue->head, (uintptr_t)dummy);
    atomic_store(&queue->tail, (uintptr_t)dummy);
    
    return queue;
}

int enqueue(LockFreeQueue *queue, void *data) {
    Node *new_node = malloc(sizeof(Node));
    if (!new_node) return 0;
    
    atomic_store(&new_node->data, (uintptr_t)data);
    atomic_store(&new_node->next, 0);
    
    while (1) {
        Node *tail = (Node*)atomic_load(&queue->tail);
        Node *next = (Node*)atomic_load(&tail->next);
        
        if (tail == (Node*)atomic_load(&queue->tail)) {
            if (next == NULL) {
                if (atomic_compare_exchange_weak(&tail->next, (uintptr_t*)&next, (uintptr_t)new_node)) {
                    break;
                }
            } else {
                atomic_compare_exchange_weak(&queue->tail, (uintptr_t*)&tail, (uintptr_t)next);
            }
        }
    }
    
    atomic_compare_exchange_weak(&queue->tail, (uintptr_t*)&((Node*)atomic_load(&queue->tail)), (uintptr_t)new_node);
    return 1;
}

void* dequeue(LockFreeQueue *queue) {
    while (1) {
        Node *head = (Node*)atomic_load(&queue->head);
        Node *tail = (Node*)atomic_load(&queue->tail);
        Node *next = (Node*)atomic_load(&head->next);
        
        if (head == (Node*)atomic_load(&queue->head)) {
            if (head == tail) {
                if (next == NULL) {
                    return NULL;  // Queue is empty
                }
                atomic_compare_exchange_weak(&queue->tail, (uintptr_t*)&tail, (uintptr_t)next);
            } else {
                void *data = (void*)atomic_load(&next->data);
                if (atomic_compare_exchange_weak(&queue->head, (uintptr_t*)&head, (uintptr_t)next)) {
                    free(head);
                    return data;
                }
            }
        }
    }
}
```

## System Programming Questions (46-60)

### 9. How do you implement memory-mapped file I/O for large dataset processing?
**Answer**: Memory-mapped I/O for efficient large file processing.

```c
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

typedef struct {
    void *data;
    size_t size;
    int fd;
} MappedFile;

MappedFile* map_file(const char *filename) {
    MappedFile *mf = malloc(sizeof(MappedFile));
    if (!mf) return NULL;
    
    mf->fd = open(filename, O_RDONLY);
    if (mf->fd == -1) {
        free(mf);
        return NULL;
    }
    
    struct stat st;
    if (fstat(mf->fd, &st) == -1) {
        close(mf->fd);
        free(mf);
        return NULL;
    }
    
    mf->size = st.st_size;
    mf->data = mmap(NULL, mf->size, PROT_READ, MAP_PRIVATE, mf->fd, 0);
    
    if (mf->data == MAP_FAILED) {
        close(mf->fd);
        free(mf);
        return NULL;
    }
    
    return mf;
}

void unmap_file(MappedFile *mf) {
    if (mf) {
        munmap(mf->data, mf->size);
        close(mf->fd);
        free(mf);
    }
}

// Process large CSV file using memory mapping
void process_large_csv(const char *filename) {
    MappedFile *mf = map_file(filename);
    if (!mf) return;
    
    char *data = (char*)mf->data;
    size_t pos = 0;
    
    while (pos < mf->size) {
        // Find end of line
        size_t line_start = pos;
        while (pos < mf->size && data[pos] != '\n') {
            pos++;
        }
        
        // Process line
        size_t line_length = pos - line_start;
        if (line_length > 0) {
            // Process line data[line_start] to data[pos-1]
            process_csv_line(data + line_start, line_length);
        }
        
        pos++; // Skip newline
    }
    
    unmap_file(mf);
}
```

### 10. How do you implement a custom memory allocator for data processing?
**Answer**: Custom allocator optimized for data processing patterns.

```c
// Slab allocator for fixed-size objects
typedef struct Slab {
    void *memory;
    size_t object_size;
    size_t objects_per_slab;
    unsigned char *free_bitmap;
    size_t free_count;
    struct Slab *next;
} Slab;

typedef struct {
    Slab *slabs;
    size_t object_size;
    size_t slab_size;
} SlabAllocator;

SlabAllocator* create_slab_allocator(size_t object_size, size_t slab_size) {
    SlabAllocator *allocator = malloc(sizeof(SlabAllocator));
    if (!allocator) return NULL;
    
    allocator->slabs = NULL;
    allocator->object_size = object_size;
    allocator->slab_size = slab_size;
    
    return allocator;
}

Slab* create_slab(SlabAllocator *allocator) {
    Slab *slab = malloc(sizeof(Slab));
    if (!slab) return NULL;
    
    slab->memory = aligned_alloc(64, allocator->slab_size); // 64-byte aligned
    if (!slab->memory) {
        free(slab);
        return NULL;
    }
    
    slab->object_size = allocator->object_size;
    slab->objects_per_slab = allocator->slab_size / allocator->object_size;
    
    size_t bitmap_size = (slab->objects_per_slab + 7) / 8;
    slab->free_bitmap = calloc(bitmap_size, 1);
    if (!slab->free_bitmap) {
        free(slab->memory);
        free(slab);
        return NULL;
    }
    
    slab->free_count = slab->objects_per_slab;
    slab->next = allocator->slabs;
    allocator->slabs = slab;
    
    return slab;
}

void* slab_alloc(SlabAllocator *allocator) {
    Slab *slab = allocator->slabs;
    
    // Find slab with free objects
    while (slab && slab->free_count == 0) {
        slab = slab->next;
    }
    
    // Create new slab if needed
    if (!slab) {
        slab = create_slab(allocator);
        if (!slab) return NULL;
    }
    
    // Find free object
    for (size_t i = 0; i < slab->objects_per_slab; i++) {
        size_t byte_index = i / 8;
        size_t bit_index = i % 8;
        
        if (!(slab->free_bitmap[byte_index] & (1 << bit_index))) {
            // Mark as used
            slab->free_bitmap[byte_index] |= (1 << bit_index);
            slab->free_count--;
            
            return (char*)slab->memory + i * slab->object_size;
        }
    }
    
    return NULL;
}

void slab_free(SlabAllocator *allocator, void *ptr) {
    Slab *slab = allocator->slabs;
    
    while (slab) {
        if (ptr >= slab->memory && 
            ptr < (char*)slab->memory + allocator->slab_size) {
            
            size_t offset = (char*)ptr - (char*)slab->memory;
            size_t index = offset / slab->object_size;
            
            size_t byte_index = index / 8;
            size_t bit_index = index % 8;
            
            // Mark as free
            slab->free_bitmap[byte_index] &= ~(1 << bit_index);
            slab->free_count++;
            
            return;
        }
        slab = slab->next;
    }
}
```

---

## 📚 **C Programming Study Guide & Best Practices**

### 🎯 **Essential C Concepts for Data Engineers**

#### **Core Principles**
1. **Memory Management**: Manual allocation/deallocation
2. **Pointer Arithmetic**: Direct memory manipulation
3. **Performance**: Low-level optimization techniques
4. **System Calls**: Direct OS interaction
5. **Data Structures**: Efficient implementations

#### **Data Engineering Applications**
1. **Database Engines**: Understanding storage engines
2. **Data Processing**: High-performance algorithms
3. **System Tools**: Building data pipeline components
4. **Extensions**: C extensions for Python/other languages
5. **Embedded Systems**: IoT data collection

### 🚀 **Performance Optimization**

#### **Memory Optimization**
- Use memory pools for frequent allocations
- Implement cache-friendly data layouts
- Minimize memory fragmentation
- Use appropriate data alignment

#### **Algorithm Optimization**
- Choose optimal data structures
- Implement efficient sorting/searching
- Use bit manipulation techniques
- Optimize loop structures

### 🔗 **Essential Resources**

- **C Programming**: "The C Programming Language" by Kernighan & Ritchie
- **Systems Programming**: "Advanced Programming in the UNIX Environment"
- **Performance**: "Computer Systems: A Programmer's Perspective"
- **Data Structures**: "Introduction to Algorithms" by CLRS

### 11. How do you implement efficient string processing in C for data parsing?
**Answer**: Optimized string operations for high-performance data processing.

```c
// Efficient string tokenizer for CSV parsing
typedef struct {
    char *start;
    char *end;
    size_t length;
} StringView;

// Zero-copy string tokenization
int tokenize_line(const char *line, char delimiter, StringView *tokens, int max_tokens) {
    int token_count = 0;
    const char *start = line;
    const char *current = line;
    
    while (*current && token_count < max_tokens) {
        if (*current == delimiter || *current == '\0') {
            tokens[token_count].start = (char*)start;
            tokens[token_count].end = (char*)current;
            tokens[token_count].length = current - start;
            token_count++;
            
            start = current + 1;
        }
        current++;
    }
    
    // Handle last token if line doesn't end with delimiter
    if (start < current && token_count < max_tokens) {
        tokens[token_count].start = (char*)start;
        tokens[token_count].end = (char*)current;
        tokens[token_count].length = current - start;
        token_count++;
    }
    
    return token_count;
}

// String to number conversion with error handling
double safe_string_to_double(const StringView *sv, int *error) {
    char buffer[32];
    size_t len = sv->length < 31 ? sv->length : 31;
    
    memcpy(buffer, sv->start, len);
    buffer[len] = '\0';
    
    char *endptr;
    double result = strtod(buffer, &endptr);
    
    *error = (endptr == buffer || *endptr != '\0') ? 1 : 0;
    return result;
}

// Fast string comparison
int string_view_equals(const StringView *sv, const char *str) {
    size_t str_len = strlen(str);
    if (sv->length != str_len) return 0;
    
    return memcmp(sv->start, str, str_len) == 0;
}
```

### 12. How do you implement thread-safe data structures in C?
**Answer**: Thread-safe implementations using mutexes and atomic operations.

```c
#include <pthread.h>
#include <stdatomic.h>

// Thread-safe queue
typedef struct QueueNode {
    void *data;
    struct QueueNode *next;
} QueueNode;

typedef struct {
    QueueNode *head;
    QueueNode *tail;
    pthread_mutex_t mutex;
    pthread_cond_t not_empty;
    atomic_int size;
    int max_size;
} ThreadSafeQueue;

ThreadSafeQueue* create_thread_safe_queue(int max_size) {
    ThreadSafeQueue *queue = malloc(sizeof(ThreadSafeQueue));
    if (!queue) return NULL;
    
    queue->head = queue->tail = NULL;
    pthread_mutex_init(&queue->mutex, NULL);
    pthread_cond_init(&queue->not_empty, NULL);
    atomic_init(&queue->size, 0);
    queue->max_size = max_size;
    
    return queue;
}

int enqueue_safe(ThreadSafeQueue *queue, void *data) {
    pthread_mutex_lock(&queue->mutex);
    
    if (atomic_load(&queue->size) >= queue->max_size) {
        pthread_mutex_unlock(&queue->mutex);
        return 0; // Queue full
    }
    
    QueueNode *new_node = malloc(sizeof(QueueNode));
    if (!new_node) {
        pthread_mutex_unlock(&queue->mutex);
        return 0;
    }
    
    new_node->data = data;
    new_node->next = NULL;
    
    if (queue->tail) {
        queue->tail->next = new_node;
    } else {
        queue->head = new_node;
    }
    queue->tail = new_node;
    
    atomic_fetch_add(&queue->size, 1);
    pthread_cond_signal(&queue->not_empty);
    pthread_mutex_unlock(&queue->mutex);
    
    return 1;
}

void* dequeue_safe(ThreadSafeQueue *queue) {
    pthread_mutex_lock(&queue->mutex);
    
    while (queue->head == NULL) {
        pthread_cond_wait(&queue->not_empty, &queue->mutex);
    }
    
    QueueNode *node = queue->head;
    void *data = node->data;
    
    queue->head = node->next;
    if (queue->head == NULL) {
        queue->tail = NULL;
    }
    
    free(node);
    atomic_fetch_sub(&queue->size, 1);
    pthread_mutex_unlock(&queue->mutex);
    
    return data;
}
```

### 13. How do you implement efficient sorting algorithms for large datasets?
**Answer**: Optimized sorting implementations for different data characteristics.

```c
// Quicksort with 3-way partitioning for duplicate handling
void quicksort_3way(int arr[], int low, int high) {
    if (low >= high) return;
    
    int lt = low, gt = high;
    int pivot = arr[low];
    int i = low + 1;
    
    while (i <= gt) {
        if (arr[i] < pivot) {
            swap(&arr[lt++], &arr[i++]);
        } else if (arr[i] > pivot) {
            swap(&arr[i], &arr[gt--]);
        } else {
            i++;
        }
    }
    
    quicksort_3way(arr, low, lt - 1);
    quicksort_3way(arr, gt + 1, high);
}

// External merge sort for datasets larger than memory
typedef struct {
    FILE *file;
    int current_value;
    int has_value;
} SortedRun;

void external_merge_sort(const char *input_file, const char *output_file, 
                        size_t memory_limit) {
    // Phase 1: Create sorted runs
    FILE *input = fopen(input_file, "rb");
    int run_count = create_sorted_runs(input, memory_limit);
    fclose(input);
    
    // Phase 2: Merge runs
    merge_sorted_runs(run_count, output_file);
}

int create_sorted_runs(FILE *input, size_t memory_limit) {
    int *buffer = malloc(memory_limit);
    int buffer_size = memory_limit / sizeof(int);
    int run_count = 0;
    
    while (1) {
        int count = fread(buffer, sizeof(int), buffer_size, input);
        if (count == 0) break;
        
        // Sort in-memory chunk
        qsort(buffer, count, sizeof(int), compare_ints);
        
        // Write sorted run to temporary file
        char filename[256];
        sprintf(filename, "run_%d.tmp", run_count);
        
        FILE *run_file = fopen(filename, "wb");
        fwrite(buffer, sizeof(int), count, run_file);
        fclose(run_file);
        
        run_count++;
    }
    
    free(buffer);
    return run_count;
}

void merge_sorted_runs(int run_count, const char *output_file) {
    SortedRun *runs = malloc(run_count * sizeof(SortedRun));
    
    // Open all run files
    for (int i = 0; i < run_count; i++) {
        char filename[256];
        sprintf(filename, "run_%d.tmp", i);
        runs[i].file = fopen(filename, "rb");
        
        // Read first value from each run
        if (fread(&runs[i].current_value, sizeof(int), 1, runs[i].file) == 1) {
            runs[i].has_value = 1;
        } else {
            runs[i].has_value = 0;
        }
    }
    
    FILE *output = fopen(output_file, "wb");
    
    // Merge using min-heap
    while (1) {
        int min_idx = -1;
        int min_value = INT_MAX;
        
        // Find minimum value among all runs
        for (int i = 0; i < run_count; i++) {
            if (runs[i].has_value && runs[i].current_value < min_value) {
                min_value = runs[i].current_value;
                min_idx = i;
            }
        }
        
        if (min_idx == -1) break; // All runs exhausted
        
        // Write minimum value to output
        fwrite(&min_value, sizeof(int), 1, output);
        
        // Read next value from the selected run
        if (fread(&runs[min_idx].current_value, sizeof(int), 1, runs[min_idx].file) != 1) {
            runs[min_idx].has_value = 0;
        }
    }
    
    // Cleanup
    for (int i = 0; i < run_count; i++) {
        fclose(runs[i].file);
        char filename[256];
        sprintf(filename, "run_%d.tmp", i);
        remove(filename);
    }
    
    free(runs);
    fclose(output);
}
```

### 14. How do you implement bit manipulation techniques for data compression?
**Answer**: Bit-level operations for efficient data storage and processing.

```c
// Bit vector for efficient boolean storage
typedef struct {
    uint64_t *bits;
    size_t size;
    size_t capacity;
} BitVector;

BitVector* create_bit_vector(size_t initial_capacity) {
    BitVector *bv = malloc(sizeof(BitVector));
    if (!bv) return NULL;
    
    size_t word_count = (initial_capacity + 63) / 64;
    bv->bits = calloc(word_count, sizeof(uint64_t));
    if (!bv->bits) {
        free(bv);
        return NULL;
    }
    
    bv->size = 0;
    bv->capacity = word_count * 64;
    
    return bv;
}

void set_bit(BitVector *bv, size_t index) {
    if (index >= bv->capacity) return;
    
    size_t word_index = index / 64;
    size_t bit_index = index % 64;
    
    bv->bits[word_index] |= (1ULL << bit_index);
    
    if (index >= bv->size) {
        bv->size = index + 1;
    }
}

int get_bit(const BitVector *bv, size_t index) {
    if (index >= bv->size) return 0;
    
    size_t word_index = index / 64;
    size_t bit_index = index % 64;
    
    return (bv->bits[word_index] >> bit_index) & 1;
}

// Population count (number of set bits)
size_t popcount_bit_vector(const BitVector *bv) {
    size_t count = 0;
    size_t word_count = (bv->size + 63) / 64;
    
    for (size_t i = 0; i < word_count; i++) {
        count += __builtin_popcountll(bv->bits[i]);
    }
    
    return count;
}

// Simple run-length encoding
typedef struct {
    uint8_t value;
    uint32_t count;
} RLEPair;

size_t rle_encode(const uint8_t *input, size_t input_size, 
                  RLEPair *output, size_t max_output) {
    if (input_size == 0) return 0;
    
    size_t output_count = 0;
    uint8_t current_value = input[0];
    uint32_t current_count = 1;
    
    for (size_t i = 1; i < input_size && output_count < max_output; i++) {
        if (input[i] == current_value && current_count < UINT32_MAX) {
            current_count++;
        } else {
            output[output_count].value = current_value;
            output[output_count].count = current_count;
            output_count++;
            
            current_value = input[i];
            current_count = 1;
        }
    }
    
    // Add final run
    if (output_count < max_output) {
        output[output_count].value = current_value;
        output[output_count].count = current_count;
        output_count++;
    }
    
    return output_count;
}

size_t rle_decode(const RLEPair *input, size_t input_count, 
                  uint8_t *output, size_t max_output) {
    size_t output_pos = 0;
    
    for (size_t i = 0; i < input_count; i++) {
        for (uint32_t j = 0; j < input[i].count && output_pos < max_output; j++) {
            output[output_pos++] = input[i].value;
        }
    }
    
    return output_pos;
}
```

### 15. How do you implement network programming for data transfer?
**Answer**: Socket programming for efficient data communication.

```c
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

// TCP server for data streaming
typedef struct {
    int socket_fd;
    struct sockaddr_in address;
    int port;
    int max_connections;
} TCPServer;

TCPServer* create_tcp_server(int port, int max_connections) {
    TCPServer *server = malloc(sizeof(TCPServer));
    if (!server) return NULL;
    
    server->socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server->socket_fd == -1) {
        free(server);
        return NULL;
    }
    
    // Set socket options
    int opt = 1;
    setsockopt(server->socket_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    
    server->address.sin_family = AF_INET;
    server->address.sin_addr.s_addr = INADDR_ANY;
    server->address.sin_port = htons(port);
    server->port = port;
    server->max_connections = max_connections;
    
    if (bind(server->socket_fd, (struct sockaddr*)&server->address, 
             sizeof(server->address)) < 0) {
        close(server->socket_fd);
        free(server);
        return NULL;
    }
    
    if (listen(server->socket_fd, max_connections) < 0) {
        close(server->socket_fd);
        free(server);
        return NULL;
    }
    
    return server;
}

// Data transfer with progress tracking
typedef struct {
    size_t bytes_sent;
    size_t total_bytes;
    double start_time;
    double last_update;
} TransferProgress;

ssize_t send_data_with_progress(int socket_fd, const void *data, size_t size,
                               TransferProgress *progress) {
    const char *buffer = (const char*)data;
    size_t bytes_sent = 0;
    
    progress->total_bytes = size;
    progress->start_time = get_current_time();
    
    while (bytes_sent < size) {
        ssize_t result = send(socket_fd, buffer + bytes_sent, 
                             size - bytes_sent, MSG_NOSIGNAL);
        
        if (result <= 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                continue; // Try again
            }
            return -1; // Error
        }
        
        bytes_sent += result;
        progress->bytes_sent = bytes_sent;
        
        // Update progress every 100ms
        double current_time = get_current_time();
        if (current_time - progress->last_update > 0.1) {
            double elapsed = current_time - progress->start_time;
            double rate = bytes_sent / elapsed;
            double eta = (size - bytes_sent) / rate;
            
            printf("Progress: %.1f%% (%.2f MB/s, ETA: %.1fs)\r",
                   (double)bytes_sent / size * 100, rate / 1024 / 1024, eta);
            fflush(stdout);
            
            progress->last_update = current_time;
        }
    }
    
    return bytes_sent;
}

// UDP multicast for data broadcasting
int create_multicast_sender(const char *multicast_ip, int port) {
    int socket_fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (socket_fd == -1) return -1;
    
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr(multicast_ip);
    addr.sin_port = htons(port);
    
    // Set TTL for multicast
    int ttl = 64;
    setsockopt(socket_fd, IPPROTO_IP, IP_MULTICAST_TTL, &ttl, sizeof(ttl));
    
    if (connect(socket_fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        close(socket_fd);
        return -1;
    }
    
    return socket_fd;
}

int broadcast_data(int socket_fd, const void *data, size_t size) {
    const char *buffer = (const char*)data;
    size_t chunk_size = 1400; // MTU consideration
    size_t offset = 0;
    
    while (offset < size) {
        size_t send_size = (size - offset < chunk_size) ? size - offset : chunk_size;
        
        ssize_t result = send(socket_fd, buffer + offset, send_size, 0);
        if (result <= 0) return -1;
        
        offset += result;
        usleep(1000); // Small delay to prevent flooding
    }
    
    return 0;
}
```

---

## Advanced C Programming Questions (61-80)

### 16. How do you implement a custom garbage collector in C?
**Answer**: Mark-and-sweep garbage collection for automatic memory management.

```c
// Simple mark-and-sweep garbage collector
typedef struct GCObject {
    struct GCObject *next;
    int marked;
    size_t size;
    char data[];
} GCObject;

typedef struct {
    GCObject *objects;
    size_t total_allocated;
    size_t gc_threshold;
    void **roots;
    size_t root_count;
    size_t root_capacity;
} GarbageCollector;

GarbageCollector* create_gc(size_t initial_threshold) {
    GarbageCollector *gc = malloc(sizeof(GarbageCollector));
    if (!gc) return NULL;
    
    gc->objects = NULL;
    gc->total_allocated = 0;
    gc->gc_threshold = initial_threshold;
    gc->roots = malloc(16 * sizeof(void*));
    gc->root_count = 0;
    gc->root_capacity = 16;
    
    return gc;
}

void* gc_alloc(GarbageCollector *gc, size_t size) {
    // Trigger GC if threshold exceeded
    if (gc->total_allocated > gc->gc_threshold) {
        gc_collect(gc);
    }
    
    GCObject *obj = malloc(sizeof(GCObject) + size);
    if (!obj) return NULL;
    
    obj->next = gc->objects;
    obj->marked = 0;
    obj->size = size;
    gc->objects = obj;
    gc->total_allocated += size;
    
    return obj->data;
}

void gc_add_root(GarbageCollector *gc, void *ptr) {
    if (gc->root_count >= gc->root_capacity) {
        gc->root_capacity *= 2;
        gc->roots = realloc(gc->roots, gc->root_capacity * sizeof(void*));
    }
    
    gc->roots[gc->root_count++] = ptr;
}

void gc_mark_object(GarbageCollector *gc, void *ptr) {
    if (!ptr) return;
    
    GCObject *obj = gc->objects;
    while (obj) {
        if (obj->data <= (char*)ptr && (char*)ptr < obj->data + obj->size) {
            if (!obj->marked) {
                obj->marked = 1;
                // Mark referenced objects (simplified)
                gc_mark_references(gc, obj->data, obj->size);
            }
            break;
        }
        obj = obj->next;
    }
}

void gc_collect(GarbageCollector *gc) {
    // Mark phase
    for (size_t i = 0; i < gc->root_count; i++) {
        gc_mark_object(gc, gc->roots[i]);
    }
    
    // Sweep phase
    GCObject **current = &gc->objects;
    while (*current) {
        GCObject *obj = *current;
        if (obj->marked) {
            obj->marked = 0; // Reset for next collection
            current = &obj->next;
        } else {
            *current = obj->next;
            gc->total_allocated -= obj->size;
            free(obj);
        }
    }
}
```

### 17. How do you implement SIMD operations for data processing?
**Answer**: Single Instruction Multiple Data for parallel processing.

```c
#include <immintrin.h>

// SIMD vector addition
void vector_add_simd(const float *a, const float *b, float *result, size_t size) {
    size_t simd_size = size - (size % 8);
    
    // Process 8 floats at a time using AVX
    for (size_t i = 0; i < simd_size; i += 8) {
        __m256 va = _mm256_load_ps(&a[i]);
        __m256 vb = _mm256_load_ps(&b[i]);
        __m256 vresult = _mm256_add_ps(va, vb);
        _mm256_store_ps(&result[i], vresult);
    }
    
    // Handle remaining elements
    for (size_t i = simd_size; i < size; i++) {
        result[i] = a[i] + b[i];
    }
}

// SIMD matrix multiplication
void matrix_multiply_simd(const float *a, const float *b, float *c,
                         int rows_a, int cols_a, int cols_b) {
    for (int i = 0; i < rows_a; i++) {
        for (int j = 0; j < cols_b; j += 8) {
            __m256 sum = _mm256_setzero_ps();
            
            for (int k = 0; k < cols_a; k++) {
                __m256 va = _mm256_broadcast_ss(&a[i * cols_a + k]);
                __m256 vb = _mm256_load_ps(&b[k * cols_b + j]);
                sum = _mm256_fmadd_ps(va, vb, sum);
            }
            
            _mm256_store_ps(&c[i * cols_b + j], sum);
        }
    }
}

// SIMD string search
int simd_string_search(const char *text, size_t text_len, 
                      const char *pattern, size_t pattern_len) {
    if (pattern_len > 16) return -1; // Limitation for this implementation
    
    __m128i pattern_vec = _mm_loadu_si128((__m128i*)pattern);
    
    for (size_t i = 0; i <= text_len - pattern_len; i += 16) {
        __m128i text_vec = _mm_loadu_si128((__m128i*)(text + i));
        __m128i cmp = _mm_cmpeq_epi8(text_vec, pattern_vec);
        
        int mask = _mm_movemask_epi8(cmp);
        if (mask != 0) {
            // Found potential match, verify
            for (int j = 0; j < 16 && i + j <= text_len - pattern_len; j++) {
                if ((mask & (1 << j)) && 
                    memcmp(text + i + j, pattern, pattern_len) == 0) {
                    return i + j;
                }
            }
        }
    }
    
    return -1;
}
```

### 18. How do you implement a high-performance JSON parser in C?
**Answer**: Optimized JSON parsing for data processing pipelines.

```c
// JSON token types
typedef enum {
    JSON_NULL, JSON_BOOL, JSON_NUMBER, JSON_STRING,
    JSON_ARRAY, JSON_OBJECT
} JsonType;

typedef struct JsonValue {
    JsonType type;
    union {
        int boolean;
        double number;
        char *string;
        struct {
            struct JsonValue *items;
            size_t count;
        } array;
        struct {
            char **keys;
            struct JsonValue *values;
            size_t count;
        } object;
    } data;
} JsonValue;

// Fast JSON parser with minimal allocations
typedef struct {
    const char *json;
    size_t pos;
    size_t length;
    char *string_buffer;
    size_t buffer_size;
} JsonParser;

JsonParser* create_json_parser(const char *json, size_t length) {
    JsonParser *parser = malloc(sizeof(JsonParser));
    if (!parser) return NULL;
    
    parser->json = json;
    parser->pos = 0;
    parser->length = length;
    parser->buffer_size = length / 4; // Estimate
    parser->string_buffer = malloc(parser->buffer_size);
    
    return parser;
}

void skip_whitespace(JsonParser *parser) {
    while (parser->pos < parser->length) {
        char c = parser->json[parser->pos];
        if (c != ' ' && c != '\t' && c != '\n' && c != '\r') break;
        parser->pos++;
    }
}

char* parse_string(JsonParser *parser) {
    if (parser->json[parser->pos] != '"') return NULL;
    parser->pos++; // Skip opening quote
    
    size_t start = parser->pos;
    size_t buffer_pos = 0;
    
    while (parser->pos < parser->length) {
        char c = parser->json[parser->pos];
        
        if (c == '"') {
            parser->string_buffer[buffer_pos] = '\0';
            parser->pos++; // Skip closing quote
            
            char *result = malloc(buffer_pos + 1);
            memcpy(result, parser->string_buffer, buffer_pos + 1);
            return result;
        }
        
        if (c == '\\') {
            parser->pos++;
            if (parser->pos >= parser->length) break;
            
            char escaped = parser->json[parser->pos];
            switch (escaped) {
                case '"': case '\\': case '/': 
                    parser->string_buffer[buffer_pos++] = escaped; break;
                case 'b': parser->string_buffer[buffer_pos++] = '\b'; break;
                case 'f': parser->string_buffer[buffer_pos++] = '\f'; break;
                case 'n': parser->string_buffer[buffer_pos++] = '\n'; break;
                case 'r': parser->string_buffer[buffer_pos++] = '\r'; break;
                case 't': parser->string_buffer[buffer_pos++] = '\t'; break;
                default: return NULL; // Invalid escape
            }
        } else {
            parser->string_buffer[buffer_pos++] = c;
        }
        
        parser->pos++;
    }
    
    return NULL; // Unterminated string
}

double parse_number(JsonParser *parser) {
    size_t start = parser->pos;
    
    // Handle negative sign
    if (parser->json[parser->pos] == '-') parser->pos++;
    
    // Parse integer part
    if (!isdigit(parser->json[parser->pos])) return NAN;
    
    while (parser->pos < parser->length && isdigit(parser->json[parser->pos])) {
        parser->pos++;
    }
    
    // Parse decimal part
    if (parser->pos < parser->length && parser->json[parser->pos] == '.') {
        parser->pos++;
        while (parser->pos < parser->length && isdigit(parser->json[parser->pos])) {
            parser->pos++;
        }
    }
    
    // Parse exponent
    if (parser->pos < parser->length && 
        (parser->json[parser->pos] == 'e' || parser->json[parser->pos] == 'E')) {
        parser->pos++;
        if (parser->json[parser->pos] == '+' || parser->json[parser->pos] == '-') {
            parser->pos++;
        }
        while (parser->pos < parser->length && isdigit(parser->json[parser->pos])) {
            parser->pos++;
        }
    }
    
    // Convert to double
    size_t length = parser->pos - start;
    char *number_str = malloc(length + 1);
    memcpy(number_str, parser->json + start, length);
    number_str[length] = '\0';
    
    double result = strtod(number_str, NULL);
    free(number_str);
    
    return result;
}
```

### 19. How do you implement efficient data serialization in C?
**Answer**: Binary serialization for fast data exchange.

```c
// Binary serialization format
typedef struct {
    uint32_t magic;     // Format identifier
    uint32_t version;   // Version number
    uint32_t checksum;  // Data integrity
    uint32_t size;      // Data size
} SerializationHeader;

#define SERIALIZATION_MAGIC 0x44415441 // "DATA"
#define SERIALIZATION_VERSION 1

// Serialization buffer
typedef struct {
    uint8_t *data;
    size_t size;
    size_t capacity;
    size_t position;
} SerializationBuffer;

SerializationBuffer* create_serialization_buffer(size_t initial_capacity) {
    SerializationBuffer *buffer = malloc(sizeof(SerializationBuffer));
    if (!buffer) return NULL;
    
    buffer->data = malloc(initial_capacity);
    if (!buffer->data) {
        free(buffer);
        return NULL;
    }
    
    buffer->size = 0;
    buffer->capacity = initial_capacity;
    buffer->position = 0;
    
    return buffer;
}

void serialize_uint32(SerializationBuffer *buffer, uint32_t value) {
    if (buffer->size + sizeof(uint32_t) > buffer->capacity) {
        buffer->capacity *= 2;
        buffer->data = realloc(buffer->data, buffer->capacity);
    }
    
    // Convert to little-endian
    uint32_t le_value = htole32(value);
    memcpy(buffer->data + buffer->size, &le_value, sizeof(uint32_t));
    buffer->size += sizeof(uint32_t);
}

void serialize_string(SerializationBuffer *buffer, const char *str) {
    uint32_t length = str ? strlen(str) : 0;
    serialize_uint32(buffer, length);
    
    if (length > 0) {
        if (buffer->size + length > buffer->capacity) {
            while (buffer->size + length > buffer->capacity) {
                buffer->capacity *= 2;
            }
            buffer->data = realloc(buffer->data, buffer->capacity);
        }
        
        memcpy(buffer->data + buffer->size, str, length);
        buffer->size += length;
    }
}

void serialize_array(SerializationBuffer *buffer, const void *array, 
                    size_t element_size, size_t count) {
    serialize_uint32(buffer, count);
    
    size_t total_size = element_size * count;
    if (buffer->size + total_size > buffer->capacity) {
        while (buffer->size + total_size > buffer->capacity) {
            buffer->capacity *= 2;
        }
        buffer->data = realloc(buffer->data, buffer->capacity);
    }
    
    memcpy(buffer->data + buffer->size, array, total_size);
    buffer->size += total_size;
}

// Deserialization
uint32_t deserialize_uint32(SerializationBuffer *buffer) {
    if (buffer->position + sizeof(uint32_t) > buffer->size) {
        return 0; // Error
    }
    
    uint32_t value;
    memcpy(&value, buffer->data + buffer->position, sizeof(uint32_t));
    buffer->position += sizeof(uint32_t);
    
    return le32toh(value);
}

char* deserialize_string(SerializationBuffer *buffer) {
    uint32_t length = deserialize_uint32(buffer);
    if (length == 0) return NULL;
    
    if (buffer->position + length > buffer->size) {
        return NULL; // Error
    }
    
    char *str = malloc(length + 1);
    memcpy(str, buffer->data + buffer->position, length);
    str[length] = '\0';
    buffer->position += length;
    
    return str;
}

// Calculate CRC32 checksum
uint32_t calculate_crc32(const uint8_t *data, size_t length) {
    static uint32_t crc_table[256];
    static int table_computed = 0;
    
    if (!table_computed) {
        for (uint32_t i = 0; i < 256; i++) {
            uint32_t c = i;
            for (int j = 0; j < 8; j++) {
                if (c & 1) {
                    c = 0xEDB88320L ^ (c >> 1);
                } else {
                    c = c >> 1;
                }
            }
            crc_table[i] = c;
        }
        table_computed = 1;
    }
    
    uint32_t crc = 0xFFFFFFFF;
    for (size_t i = 0; i < length; i++) {
        crc = crc_table[(crc ^ data[i]) & 0xFF] ^ (crc >> 8);
    }
    
    return crc ^ 0xFFFFFFFF;
}
```

### 20. How do you implement a real-time data processing system in C?
**Answer**: Event-driven architecture for real-time data streams.

```c
#include <sys/epoll.h>
#include <sys/timerfd.h>

// Event types
typedef enum {
    EVENT_DATA_RECEIVED,
    EVENT_TIMER_EXPIRED,
    EVENT_CONNECTION_CLOSED,
    EVENT_ERROR
} EventType;

typedef struct {
    EventType type;
    int fd;
    void *data;
    size_t data_size;
    double timestamp;
} Event;

// Real-time processor
typedef struct {
    int epoll_fd;
    int timer_fd;
    Event *event_queue;
    size_t queue_size;
    size_t queue_capacity;
    pthread_mutex_t queue_mutex;
    
    // Processing statistics
    uint64_t events_processed;
    double total_latency;
    double max_latency;
} RealTimeProcessor;

RealTimeProcessor* create_realtime_processor() {
    RealTimeProcessor *processor = malloc(sizeof(RealTimeProcessor));
    if (!processor) return NULL;
    
    processor->epoll_fd = epoll_create1(EPOLL_CLOEXEC);
    if (processor->epoll_fd == -1) {
        free(processor);
        return NULL;
    }
    
    // Create timer for periodic processing
    processor->timer_fd = timerfd_create(CLOCK_MONOTONIC, TFD_CLOEXEC);
    if (processor->timer_fd == -1) {
        close(processor->epoll_fd);
        free(processor);
        return NULL;
    }
    
    // Set up timer for 1ms intervals
    struct itimerspec timer_spec = {
        .it_interval = {.tv_sec = 0, .tv_nsec = 1000000}, // 1ms
        .it_value = {.tv_sec = 0, .tv_nsec = 1000000}
    };
    timerfd_settime(processor->timer_fd, 0, &timer_spec, NULL);
    
    // Add timer to epoll
    struct epoll_event event = {
        .events = EPOLLIN,
        .data.fd = processor->timer_fd
    };
    epoll_ctl(processor->epoll_fd, EPOLL_CTL_ADD, processor->timer_fd, &event);
    
    processor->queue_capacity = 1000;
    processor->event_queue = malloc(processor->queue_capacity * sizeof(Event));
    processor->queue_size = 0;
    pthread_mutex_init(&processor->queue_mutex, NULL);
    
    processor->events_processed = 0;
    processor->total_latency = 0.0;
    processor->max_latency = 0.0;
    
    return processor;
}

void add_data_source(RealTimeProcessor *processor, int fd) {
    struct epoll_event event = {
        .events = EPOLLIN | EPOLLET, // Edge-triggered
        .data.fd = fd
    };
    epoll_ctl(processor->epoll_fd, EPOLL_CTL_ADD, fd, &event);
}

void process_events(RealTimeProcessor *processor) {
    struct epoll_event events[64];
    
    while (1) {
        int event_count = epoll_wait(processor->epoll_fd, events, 64, -1);
        
        for (int i = 0; i < event_count; i++) {
            int fd = events[i].data.fd;
            double event_time = get_current_time();
            
            if (fd == processor->timer_fd) {
                // Timer event - process queued events
                uint64_t timer_expirations;
                read(processor->timer_fd, &timer_expirations, sizeof(timer_expirations));
                
                process_event_queue(processor);
            } else {
                // Data event
                char buffer[8192];
                ssize_t bytes_read = read(fd, buffer, sizeof(buffer));
                
                if (bytes_read > 0) {
                    // Queue event for processing
                    pthread_mutex_lock(&processor->queue_mutex);
                    
                    if (processor->queue_size < processor->queue_capacity) {
                        Event *event = &processor->event_queue[processor->queue_size++];
                        event->type = EVENT_DATA_RECEIVED;
                        event->fd = fd;
                        event->data = malloc(bytes_read);
                        memcpy(event->data, buffer, bytes_read);
                        event->data_size = bytes_read;
                        event->timestamp = event_time;
                    }
                    
                    pthread_mutex_unlock(&processor->queue_mutex);
                } else if (bytes_read == 0) {
                    // Connection closed
                    epoll_ctl(processor->epoll_fd, EPOLL_CTL_DEL, fd, NULL);
                    close(fd);
                }
            }
        }
    }
}

void process_event_queue(RealTimeProcessor *processor) {
    pthread_mutex_lock(&processor->queue_mutex);
    
    for (size_t i = 0; i < processor->queue_size; i++) {
        Event *event = &processor->event_queue[i];
        double processing_start = get_current_time();
        
        // Process the event based on type
        switch (event->type) {
            case EVENT_DATA_RECEIVED:
                process_data_event(processor, event);
                break;
            default:
                break;
        }
        
        // Calculate latency
        double latency = processing_start - event->timestamp;
        processor->total_latency += latency;
        if (latency > processor->max_latency) {
            processor->max_latency = latency;
        }
        processor->events_processed++;
        
        // Cleanup
        free(event->data);
    }
    
    processor->queue_size = 0;
    pthread_mutex_unlock(&processor->queue_mutex);
}

void process_data_event(RealTimeProcessor *processor, Event *event) {
    // Example: Parse and aggregate data
    const char *data = (const char*)event->data;
    
    // Simple CSV parsing for real-time metrics
    char *line = strtok((char*)data, "\n");
    while (line) {
        char *timestamp_str = strtok(line, ",");
        char *value_str = strtok(NULL, ",");
        char *metric_name = strtok(NULL, ",");
        
        if (timestamp_str && value_str && metric_name) {
            double timestamp = strtod(timestamp_str, NULL);
            double value = strtod(value_str, NULL);
            
            // Update real-time aggregates
            update_metric(metric_name, value, timestamp);
        }
        
        line = strtok(NULL, "\n");
    }
}

// Performance monitoring
void print_performance_stats(RealTimeProcessor *processor) {
    if (processor->events_processed > 0) {
        double avg_latency = processor->total_latency / processor->events_processed;
        
        printf("Performance Statistics:\n");
        printf("Events processed: %lu\n", processor->events_processed);
        printf("Average latency: %.3f ms\n", avg_latency * 1000);
        printf("Maximum latency: %.3f ms\n", processor->max_latency * 1000);
        printf("Throughput: %.2f events/sec\n", 
               processor->events_processed / (processor->total_latency + 0.001));
    }
}
```

---

**Remember**: C programming provides the foundation for understanding how data systems work at the lowest level. Focus on memory management, performance optimization, and system-level programming concepts.
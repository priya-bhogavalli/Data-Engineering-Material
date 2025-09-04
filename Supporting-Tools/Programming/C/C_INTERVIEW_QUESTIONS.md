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

---

**Remember**: C programming provides the foundation for understanding how data systems work at the lowest level. Focus on memory management, performance optimization, and system-level programming concepts.
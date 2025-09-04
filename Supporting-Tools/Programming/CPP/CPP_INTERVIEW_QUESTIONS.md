# C++ Programming Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts Questions (1-15)](#core-concepts-questions-1-15)
2. [STL & Templates Questions (16-30)](#stl--templates-questions-16-30)
3. [Object-Oriented Programming Questions (31-45)](#object-oriented-programming-questions-31-45)
4. [Performance & Memory Questions (46-60)](#performance--memory-questions-46-60)

---

## 🎯 **Introduction**

C++ is crucial for data engineers working on high-performance data processing systems, database engines, and performance-critical applications where both low-level control and high-level abstractions are needed.

**Why C++ is Important for Data Engineers:**
- **Performance**: Zero-cost abstractions with manual memory control
- **STL**: Rich standard library for data structures and algorithms
- **Templates**: Generic programming for reusable data processing code
- **RAII**: Automatic resource management
- **Integration**: Interface with C libraries and system APIs

---

## Core Concepts Questions (1-15)

### 1. What are the key advantages of C++ over C for data engineering applications?
**Answer**: 
C++ provides higher-level abstractions while maintaining C's performance characteristics.

**Key Advantages:**
- **STL Containers**: vector, map, unordered_map, set for data structures
- **Templates**: Generic programming for type-safe, reusable code
- **RAII**: Automatic resource management
- **Function Overloading**: Multiple functions with same name
- **Namespaces**: Better code organization

```cpp
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <memory>

// Modern C++ data processing class
class DataProcessor {
private:
    std::vector<double> data_;
    std::unordered_map<std::string, double> aggregates_;
    
public:
    // RAII - automatic resource management
    DataProcessor(const std::vector<double>& data) : data_(data) {}
    
    // Template function for generic aggregation
    template<typename Func>
    double aggregate(Func func) {
        return std::accumulate(data_.begin(), data_.end(), 0.0, func);
    }
    
    // STL algorithms for data processing
    void process() {
        // Sort data
        std::sort(data_.begin(), data_.end());
        
        // Calculate statistics
        aggregates_["sum"] = aggregate(std::plus<double>());
        aggregates_["mean"] = aggregates_["sum"] / data_.size();
        
        // Find outliers using lambda
        auto outlier_threshold = aggregates_["mean"] * 2;
        auto outliers = std::count_if(data_.begin(), data_.end(),
            [outlier_threshold](double val) { return val > outlier_threshold; });
        
        aggregates_["outliers"] = static_cast<double>(outliers);
    }
    
    const std::unordered_map<std::string, double>& getAggregates() const {
        return aggregates_;
    }
};
```

### 2. How do you implement efficient data structures using C++ STL?
**Answer**: STL provides optimized containers for different use cases.

```cpp
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <chrono>

// Hash table for data aggregation
class DataAggregator {
private:
    std::unordered_map<std::string, std::vector<double>> groups_;
    
public:
    void addValue(const std::string& group, double value) {
        groups_[group].push_back(value);
    }
    
    struct GroupStats {
        double sum;
        double mean;
        double min;
        double max;
        size_t count;
    };
    
    GroupStats calculateStats(const std::string& group) const {
        auto it = groups_.find(group);
        if (it == groups_.end()) {
            return {0.0, 0.0, 0.0, 0.0, 0};
        }
        
        const auto& values = it->second;
        GroupStats stats;
        stats.count = values.size();
        
        if (stats.count == 0) return stats;
        
        stats.sum = std::accumulate(values.begin(), values.end(), 0.0);
        stats.mean = stats.sum / stats.count;
        
        auto minmax = std::minmax_element(values.begin(), values.end());
        stats.min = *minmax.first;
        stats.max = *minmax.second;
        
        return stats;
    }
    
    // Get all group names
    std::vector<std::string> getGroups() const {
        std::vector<std::string> groups;
        groups.reserve(groups_.size());
        
        for (const auto& pair : groups_) {
            groups.push_back(pair.first);
        }
        
        return groups;
    }
};

// Priority queue for top-K processing
template<typename T>
class TopKProcessor {
private:
    std::priority_queue<T, std::vector<T>, std::greater<T>> min_heap_;
    size_t k_;
    
public:
    explicit TopKProcessor(size_t k) : k_(k) {}
    
    void process(const T& value) {
        if (min_heap_.size() < k_) {
            min_heap_.push(value);
        } else if (value > min_heap_.top()) {
            min_heap_.pop();
            min_heap_.push(value);
        }
    }
    
    std::vector<T> getTopK() const {
        std::vector<T> result;
        auto temp_heap = min_heap_;
        
        while (!temp_heap.empty()) {
            result.push_back(temp_heap.top());
            temp_heap.pop();
        }
        
        std::reverse(result.begin(), result.end());
        return result;
    }
};
```

### 3. How do you implement RAII for resource management in data processing?
**Answer**: RAII ensures automatic resource cleanup and exception safety.

```cpp
#include <fstream>
#include <memory>
#include <stdexcept>

// RAII file handler
class FileProcessor {
private:
    std::unique_ptr<std::ifstream> file_;
    std::string filename_;
    
public:
    explicit FileProcessor(const std::string& filename) 
        : filename_(filename), file_(std::make_unique<std::ifstream>(filename)) {
        
        if (!file_->is_open()) {
            throw std::runtime_error("Failed to open file: " + filename);
        }
    }
    
    // No need for explicit destructor - unique_ptr handles cleanup
    
    // Move constructor for efficiency
    FileProcessor(FileProcessor&& other) noexcept 
        : file_(std::move(other.file_)), filename_(std::move(other.filename_)) {}
    
    // Move assignment
    FileProcessor& operator=(FileProcessor&& other) noexcept {
        if (this != &other) {
            file_ = std::move(other.file_);
            filename_ = std::move(other.filename_);
        }
        return *this;
    }
    
    // Delete copy operations to prevent resource duplication
    FileProcessor(const FileProcessor&) = delete;
    FileProcessor& operator=(const FileProcessor&) = delete;
    
    std::vector<std::string> readLines() {
        std::vector<std::string> lines;
        std::string line;
        
        while (std::getline(*file_, line)) {
            lines.push_back(std::move(line));
        }
        
        return lines;
    }
    
    bool isOpen() const {
        return file_ && file_->is_open();
    }
};

// RAII memory pool
class MemoryPool {
private:
    std::vector<std::unique_ptr<char[]>> blocks_;
    size_t block_size_;
    size_t current_block_;
    size_t current_offset_;
    
public:
    explicit MemoryPool(size_t block_size = 1024 * 1024) // 1MB blocks
        : block_size_(block_size), current_block_(0), current_offset_(0) {
        addBlock();
    }
    
    void* allocate(size_t size) {
        if (current_offset_ + size > block_size_) {
            addBlock();
        }
        
        void* ptr = blocks_[current_block_].get() + current_offset_;
        current_offset_ += size;
        return ptr;
    }
    
    void reset() {
        current_block_ = 0;
        current_offset_ = 0;
    }
    
private:
    void addBlock() {
        blocks_.push_back(std::make_unique<char[]>(block_size_));
        current_block_ = blocks_.size() - 1;
        current_offset_ = 0;
    }
};
```

### 4. How do you use templates for generic data processing algorithms?
**Answer**: Templates enable type-safe, reusable algorithms.

```cpp
#include <vector>
#include <algorithm>
#include <functional>
#include <type_traits>

// Generic data transformer
template<typename InputType, typename OutputType, typename TransformFunc>
class DataTransformer {
private:
    TransformFunc transform_func_;
    
public:
    explicit DataTransformer(TransformFunc func) : transform_func_(func) {}
    
    std::vector<OutputType> transform(const std::vector<InputType>& input) {
        std::vector<OutputType> output;
        output.reserve(input.size());
        
        std::transform(input.begin(), input.end(), std::back_inserter(output), transform_func_);
        return output;
    }
    
    // Parallel transformation
    std::vector<OutputType> transformParallel(const std::vector<InputType>& input) {
        std::vector<OutputType> output(input.size());
        
        std::transform(std::execution::par_unseq, 
                      input.begin(), input.end(), output.begin(), transform_func_);
        return output;
    }
};

// Generic aggregator with SFINAE
template<typename T>
class GenericAggregator {
private:
    static_assert(std::is_arithmetic_v<T>, "T must be an arithmetic type");
    
public:
    struct Statistics {
        T sum;
        T mean;
        T min;
        T max;
        size_t count;
        T variance;
    };
    
    template<typename Container>
    Statistics calculate(const Container& data) {
        static_assert(std::is_same_v<typename Container::value_type, T>, 
                     "Container value type must match T");
        
        Statistics stats{};
        stats.count = data.size();
        
        if (stats.count == 0) return stats;
        
        // Calculate sum
        stats.sum = std::accumulate(data.begin(), data.end(), T{});
        stats.mean = stats.sum / static_cast<T>(stats.count);
        
        // Calculate min/max
        auto minmax = std::minmax_element(data.begin(), data.end());
        stats.min = *minmax.first;
        stats.max = *minmax.second;
        
        // Calculate variance
        T sum_squared_diff = std::accumulate(data.begin(), data.end(), T{},
            [mean = stats.mean](T acc, T val) {
                T diff = val - mean;
                return acc + diff * diff;
            });
        
        stats.variance = sum_squared_diff / static_cast<T>(stats.count);
        
        return stats;
    }
};

// Template specialization for string processing
template<>
class GenericAggregator<std::string> {
public:
    struct StringStatistics {
        size_t total_length;
        size_t count;
        double average_length;
        std::string longest;
        std::string shortest;
    };
    
    template<typename Container>
    StringStatistics calculate(const Container& data) {
        StringStatistics stats{};
        stats.count = data.size();
        
        if (stats.count == 0) return stats;
        
        stats.total_length = 0;
        stats.longest = data.front();
        stats.shortest = data.front();
        
        for (const auto& str : data) {
            stats.total_length += str.length();
            
            if (str.length() > stats.longest.length()) {
                stats.longest = str;
            }
            if (str.length() < stats.shortest.length()) {
                stats.shortest = str;
            }
        }
        
        stats.average_length = static_cast<double>(stats.total_length) / stats.count;
        return stats;
    }
};

// Usage examples
void demonstrateTemplates() {
    // Numeric data processing
    std::vector<double> numbers = {1.5, 2.3, 3.7, 4.1, 5.9};
    
    GenericAggregator<double> numeric_agg;
    auto numeric_stats = numeric_agg.calculate(numbers);
    
    // String data processing
    std::vector<std::string> strings = {"hello", "world", "cpp", "templates"};
    
    GenericAggregator<std::string> string_agg;
    auto string_stats = string_agg.calculate(strings);
    
    // Data transformation
    DataTransformer<double, int, std::function<int(double)>> transformer(
        [](double d) { return static_cast<int>(d * 10); });
    
    auto transformed = transformer.transform(numbers);
}
```

## STL & Templates Questions (16-30)

### 5. How do you implement efficient sorting and searching for large datasets?
**Answer**: STL algorithms with custom comparators and optimizations.

```cpp
#include <vector>
#include <algorithm>
#include <execution>
#include <random>

// Custom data record
struct DataRecord {
    int id;
    double value;
    std::string category;
    
    // Multiple comparison operators for different sorting needs
    bool operator<(const DataRecord& other) const {
        return value < other.value;
    }
};

class DataSorter {
public:
    // Sort by different criteria
    static void sortById(std::vector<DataRecord>& data) {
        std::sort(data.begin(), data.end(), 
                 [](const DataRecord& a, const DataRecord& b) {
                     return a.id < b.id;
                 });
    }
    
    static void sortByValue(std::vector<DataRecord>& data) {
        std::sort(data.begin(), data.end());  // Uses operator<
    }
    
    static void sortByCategory(std::vector<DataRecord>& data) {
        std::sort(data.begin(), data.end(),
                 [](const DataRecord& a, const DataRecord& b) {
                     return a.category < b.category;
                 });
    }
    
    // Parallel sorting for large datasets
    static void parallelSort(std::vector<DataRecord>& data) {
        std::sort(std::execution::par_unseq, data.begin(), data.end());
    }
    
    // Partial sorting for top-K
    static void partialSort(std::vector<DataRecord>& data, size_t k) {
        if (k >= data.size()) {
            std::sort(data.begin(), data.end());
        } else {
            std::partial_sort(data.begin(), data.begin() + k, data.end());
        }
    }
    
    // Nth element for median finding
    static double findMedian(std::vector<DataRecord> data) {
        size_t n = data.size();
        if (n == 0) return 0.0;
        
        if (n % 2 == 1) {
            std::nth_element(data.begin(), data.begin() + n/2, data.end());
            return data[n/2].value;
        } else {
            std::nth_element(data.begin(), data.begin() + n/2 - 1, data.end());
            double first = data[n/2 - 1].value;
            
            std::nth_element(data.begin(), data.begin() + n/2, data.end());
            double second = data[n/2].value;
            
            return (first + second) / 2.0;
        }
    }
};

// Binary search utilities
class DataSearcher {
public:
    // Binary search on sorted data
    static auto findById(const std::vector<DataRecord>& data, int target_id) {
        return std::lower_bound(data.begin(), data.end(), target_id,
                               [](const DataRecord& record, int id) {
                                   return record.id < id;
                               });
    }
    
    // Range queries
    static std::pair<std::vector<DataRecord>::const_iterator, 
                    std::vector<DataRecord>::const_iterator>
    findValueRange(const std::vector<DataRecord>& data, double min_val, double max_val) {
        auto lower = std::lower_bound(data.begin(), data.end(), min_val,
                                     [](const DataRecord& record, double val) {
                                         return record.value < val;
                                     });
        
        auto upper = std::upper_bound(data.begin(), data.end(), max_val,
                                     [](double val, const DataRecord& record) {
                                         return val < record.value;
                                     });
        
        return {lower, upper};
    }
};
```

### 6. How do you implement custom iterators for data processing?
**Answer**: Custom iterators for specialized data access patterns.

```cpp
#include <iterator>
#include <vector>

// Custom iterator for filtering data
template<typename Iterator, typename Predicate>
class FilterIterator {
private:
    Iterator current_;
    Iterator end_;
    Predicate predicate_;
    
    void advance_to_valid() {
        while (current_ != end_ && !predicate_(*current_)) {
            ++current_;
        }
    }
    
public:
    using iterator_category = std::forward_iterator_tag;
    using value_type = typename Iterator::value_type;
    using difference_type = typename Iterator::difference_type;
    using pointer = typename Iterator::pointer;
    using reference = typename Iterator::reference;
    
    FilterIterator(Iterator current, Iterator end, Predicate pred)
        : current_(current), end_(end), predicate_(pred) {
        advance_to_valid();
    }
    
    reference operator*() const { return *current_; }
    pointer operator->() const { return current_.operator->(); }
    
    FilterIterator& operator++() {
        ++current_;
        advance_to_valid();
        return *this;
    }
    
    FilterIterator operator++(int) {
        FilterIterator temp = *this;
        ++(*this);
        return temp;
    }
    
    bool operator==(const FilterIterator& other) const {
        return current_ == other.current_;
    }
    
    bool operator!=(const FilterIterator& other) const {
        return !(*this == other);
    }
};

// Helper function to create filter iterator
template<typename Iterator, typename Predicate>
FilterIterator<Iterator, Predicate> make_filter_iterator(
    Iterator current, Iterator end, Predicate pred) {
    return FilterIterator<Iterator, Predicate>(current, end, pred);
}

// Custom range class for filtered data
template<typename Container, typename Predicate>
class FilteredRange {
private:
    Container& container_;
    Predicate predicate_;
    
public:
    FilteredRange(Container& container, Predicate pred)
        : container_(container), predicate_(pred) {}
    
    auto begin() {
        return make_filter_iterator(container_.begin(), container_.end(), predicate_);
    }
    
    auto end() {
        return make_filter_iterator(container_.end(), container_.end(), predicate_);
    }
};

// Usage example
void demonstrateCustomIterators() {
    std::vector<DataRecord> data = {
        {1, 10.5, "A"}, {2, 5.2, "B"}, {3, 15.7, "A"}, {4, 8.1, "C"}
    };
    
    // Filter records with value > 8.0
    auto filtered = FilteredRange(data, [](const DataRecord& r) {
        return r.value > 8.0;
    });
    
    // Process filtered data
    for (const auto& record : filtered) {
        // Process only records with value > 8.0
        std::cout << "ID: " << record.id << ", Value: " << record.value << std::endl;
    }
}
```

## Object-Oriented Programming Questions (31-45)

### 7. How do you design a data processing pipeline using OOP principles?
**Answer**: Pipeline design with inheritance, polymorphism, and composition.

```cpp
#include <memory>
#include <vector>
#include <functional>

// Abstract base class for pipeline stages
template<typename InputType, typename OutputType>
class PipelineStage {
public:
    virtual ~PipelineStage() = default;
    virtual std::vector<OutputType> process(const std::vector<InputType>& input) = 0;
    virtual std::string getName() const = 0;
};

// Concrete pipeline stages
class DataValidator : public PipelineStage<std::string, std::string> {
public:
    std::vector<std::string> process(const std::vector<std::string>& input) override {
        std::vector<std::string> output;
        
        for (const auto& item : input) {
            if (isValid(item)) {
                output.push_back(item);
            }
        }
        
        return output;
    }
    
    std::string getName() const override { return "DataValidator"; }
    
private:
    bool isValid(const std::string& data) const {
        return !data.empty() && data.length() > 3;
    }
};

class DataTransformer : public PipelineStage<std::string, double> {
public:
    std::vector<double> process(const std::vector<std::string>& input) override {
        std::vector<double> output;
        output.reserve(input.size());
        
        for (const auto& item : input) {
            try {
                output.push_back(std::stod(item));
            } catch (const std::exception&) {
                output.push_back(0.0);  // Default value for invalid conversions
            }
        }
        
        return output;
    }
    
    std::string getName() const override { return "DataTransformer"; }
};

class DataAggregator : public PipelineStage<double, double> {
private:
    std::function<double(const std::vector<double>&)> aggregation_func_;
    
public:
    explicit DataAggregator(std::function<double(const std::vector<double>&)> func)
        : aggregation_func_(func) {}
    
    std::vector<double> process(const std::vector<double>& input) override {
        if (input.empty()) return {};
        
        double result = aggregation_func_(input);
        return {result};
    }
    
    std::string getName() const override { return "DataAggregator"; }
};

// Pipeline orchestrator
class DataPipeline {
private:
    struct StageInfo {
        std::string name;
        std::function<void()> execute;
    };
    
    std::vector<StageInfo> stages_;
    
public:
    template<typename InputType, typename OutputType>
    void addStage(std::unique_ptr<PipelineStage<InputType, OutputType>> stage) {
        std::string name = stage->getName();
        
        // Store stage execution logic
        stages_.push_back({
            name,
            [stage = std::move(stage)]() {
                // Stage execution would be handled by pipeline runner
            }
        });
    }
    
    void execute() {
        for (const auto& stage : stages_) {
            std::cout << "Executing stage: " << stage.name << std::endl;
            stage.execute();
        }
    }
    
    size_t getStageCount() const { return stages_.size(); }
};

// Factory pattern for stage creation
class StageFactory {
public:
    enum class StageType {
        VALIDATOR,
        TRANSFORMER,
        AGGREGATOR
    };
    
    template<typename InputType, typename OutputType>
    static std::unique_ptr<PipelineStage<InputType, OutputType>> 
    createStage(StageType type) {
        switch (type) {
            case StageType::VALIDATOR:
                if constexpr (std::is_same_v<InputType, std::string> && 
                             std::is_same_v<OutputType, std::string>) {
                    return std::make_unique<DataValidator>();
                }
                break;
            case StageType::TRANSFORMER:
                if constexpr (std::is_same_v<InputType, std::string> && 
                             std::is_same_v<OutputType, double>) {
                    return std::make_unique<DataTransformer>();
                }
                break;
            case StageType::AGGREGATOR:
                if constexpr (std::is_same_v<InputType, double> && 
                             std::is_same_v<OutputType, double>) {
                    return std::make_unique<DataAggregator>(
                        [](const std::vector<double>& data) {
                            return std::accumulate(data.begin(), data.end(), 0.0) / data.size();
                        });
                }
                break;
        }
        return nullptr;
    }
};
```

### 8. How do you implement the Strategy pattern for different data processing algorithms?
**Answer**: Strategy pattern for pluggable algorithms.

```cpp
#include <memory>
#include <unordered_map>

// Strategy interface for sorting algorithms
template<typename T>
class SortingStrategy {
public:
    virtual ~SortingStrategy() = default;
    virtual void sort(std::vector<T>& data) = 0;
    virtual std::string getName() const = 0;
};

// Concrete sorting strategies
template<typename T>
class QuickSortStrategy : public SortingStrategy<T> {
public:
    void sort(std::vector<T>& data) override {
        std::sort(data.begin(), data.end());
    }
    
    std::string getName() const override { return "QuickSort"; }
};

template<typename T>
class MergeSortStrategy : public SortingStrategy<T> {
public:
    void sort(std::vector<T>& data) override {
        std::stable_sort(data.begin(), data.end());
    }
    
    std::string getName() const override { return "MergeSort"; }
};

template<typename T>
class HeapSortStrategy : public SortingStrategy<T> {
public:
    void sort(std::vector<T>& data) override {
        std::make_heap(data.begin(), data.end());
        std::sort_heap(data.begin(), data.end());
    }
    
    std::string getName() const override { return "HeapSort"; }
};

// Context class that uses strategies
template<typename T>
class DataSorter {
private:
    std::unique_ptr<SortingStrategy<T>> strategy_;
    
public:
    explicit DataSorter(std::unique_ptr<SortingStrategy<T>> strategy)
        : strategy_(std::move(strategy)) {}
    
    void setStrategy(std::unique_ptr<SortingStrategy<T>> strategy) {
        strategy_ = std::move(strategy);
    }
    
    void sortData(std::vector<T>& data) {
        if (strategy_) {
            strategy_->sort(data);
        }
    }
    
    std::string getCurrentStrategy() const {
        return strategy_ ? strategy_->getName() : "None";
    }
};

// Strategy factory
template<typename T>
class SortingStrategyFactory {
public:
    enum class Algorithm {
        QUICK_SORT,
        MERGE_SORT,
        HEAP_SORT
    };
    
    static std::unique_ptr<SortingStrategy<T>> create(Algorithm algo) {
        switch (algo) {
            case Algorithm::QUICK_SORT:
                return std::make_unique<QuickSortStrategy<T>>();
            case Algorithm::MERGE_SORT:
                return std::make_unique<MergeSortStrategy<T>>();
            case Algorithm::HEAP_SORT:
                return std::make_unique<HeapSortStrategy<T>>();
            default:
                return nullptr;
        }
    }
};

// Usage example
void demonstrateStrategyPattern() {
    std::vector<int> data = {64, 34, 25, 12, 22, 11, 90};
    
    // Create sorter with QuickSort strategy
    auto sorter = DataSorter<int>(
        SortingStrategyFactory<int>::create(
            SortingStrategyFactory<int>::Algorithm::QUICK_SORT));
    
    std::cout << "Using: " << sorter.getCurrentStrategy() << std::endl;
    sorter.sortData(data);
    
    // Switch to MergeSort strategy
    sorter.setStrategy(
        SortingStrategyFactory<int>::create(
            SortingStrategyFactory<int>::Algorithm::MERGE_SORT));
    
    std::cout << "Switched to: " << sorter.getCurrentStrategy() << std::endl;
}
```

## Performance & Memory Questions (46-60)

### 9. How do you optimize C++ code for high-performance data processing?
**Answer**: Performance optimization techniques for data-intensive applications.

```cpp
#include <vector>
#include <algorithm>
#include <execution>
#include <immintrin.h>  // For SIMD
#include <chrono>

class PerformanceOptimizer {
public:
    // Cache-friendly data layout (Structure of Arrays)
    struct DataSoA {
        std::vector<double> values;
        std::vector<int> ids;
        std::vector<char> categories;
        
        void reserve(size_t size) {
            values.reserve(size);
            ids.reserve(size);
            categories.reserve(size);
        }
        
        size_t size() const { return values.size(); }
    };
    
    // SIMD-optimized vector operations
    static double vectorSum(const std::vector<double>& data) {
        const size_t simd_size = 4;  // AVX can process 4 doubles at once
        const size_t simd_end = (data.size() / simd_size) * simd_size;
        
        __m256d sum_vec = _mm256_setzero_pd();
        
        // Process 4 elements at a time
        for (size_t i = 0; i < simd_end; i += simd_size) {
            __m256d data_vec = _mm256_loadu_pd(&data[i]);
            sum_vec = _mm256_add_pd(sum_vec, data_vec);
        }
        
        // Extract sum from vector
        double result[4];
        _mm256_storeu_pd(result, sum_vec);
        double total = result[0] + result[1] + result[2] + result[3];
        
        // Handle remaining elements
        for (size_t i = simd_end; i < data.size(); ++i) {
            total += data[i];
        }
        
        return total;
    }
    
    // Memory pool for frequent allocations
    template<typename T>
    class ObjectPool {
    private:
        std::vector<std::unique_ptr<T>> pool_;
        std::vector<T*> available_;
        
    public:
        T* acquire() {
            if (available_.empty()) {
                pool_.push_back(std::make_unique<T>());
                return pool_.back().get();
            }
            
            T* obj = available_.back();
            available_.pop_back();
            return obj;
        }
        
        void release(T* obj) {
            if (obj) {
                available_.push_back(obj);
            }
        }
        
        size_t poolSize() const { return pool_.size(); }
        size_t availableCount() const { return available_.size(); }
    };
    
    // Branch prediction optimization
    static void processDataWithBranchOptimization(std::vector<int>& data) {
        // Sort data to improve branch prediction
        std::sort(data.begin(), data.end());
        
        int positive_count = 0;
        int negative_count = 0;
        
        for (int value : data) {
            // Now branches are more predictable
            if (value >= 0) {
                ++positive_count;
            } else {
                ++negative_count;
            }
        }
    }
    
    // Loop unrolling for better performance
    static void processArrayUnrolled(const double* input, double* output, size_t size) {
        const size_t unroll_factor = 4;
        const size_t unrolled_size = (size / unroll_factor) * unroll_factor;
        
        // Process 4 elements at a time
        for (size_t i = 0; i < unrolled_size; i += unroll_factor) {
            output[i] = input[i] * 2.0;
            output[i + 1] = input[i + 1] * 2.0;
            output[i + 2] = input[i + 2] * 2.0;
            output[i + 3] = input[i + 3] * 2.0;
        }
        
        // Handle remaining elements
        for (size_t i = unrolled_size; i < size; ++i) {
            output[i] = input[i] * 2.0;
        }
    }
};

// Benchmark utility
class Benchmark {
public:
    template<typename Func>
    static double measureTime(Func&& func) {
        auto start = std::chrono::high_resolution_clock::now();
        func();
        auto end = std::chrono::high_resolution_clock::now();
        
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        return duration.count() / 1000.0;  // Return milliseconds
    }
    
    template<typename Func>
    static double benchmarkFunction(Func&& func, int iterations = 100) {
        double total_time = 0.0;
        
        for (int i = 0; i < iterations; ++i) {
            total_time += measureTime(func);
        }
        
        return total_time / iterations;
    }
};
```

### 10. How do you implement lock-free data structures in C++?
**Answer**: Lock-free programming using atomic operations.

```cpp
#include <atomic>
#include <memory>

// Lock-free stack
template<typename T>
class LockFreeStack {
private:
    struct Node {
        T data;
        std::atomic<Node*> next;
        
        Node(const T& item) : data(item), next(nullptr) {}
    };
    
    std::atomic<Node*> head_;
    
public:
    LockFreeStack() : head_(nullptr) {}
    
    ~LockFreeStack() {
        while (Node* old_head = head_.load()) {
            head_ = old_head->next;
            delete old_head;
        }
    }
    
    void push(const T& item) {
        Node* new_node = new Node(item);
        new_node->next = head_.load();
        
        while (!head_.compare_exchange_weak(new_node->next, new_node)) {
            // CAS failed, retry with updated next pointer
        }
    }
    
    bool pop(T& result) {
        Node* old_head = head_.load();
        
        while (old_head && !head_.compare_exchange_weak(old_head, old_head->next.load())) {
            // CAS failed, retry
        }
        
        if (old_head) {
            result = old_head->data;
            delete old_head;
            return true;
        }
        
        return false;  // Stack was empty
    }
    
    bool empty() const {
        return head_.load() == nullptr;
    }
};

// Lock-free queue using hazard pointers
template<typename T>
class LockFreeQueue {
private:
    struct Node {
        std::atomic<T*> data;
        std::atomic<Node*> next;
        
        Node() : data(nullptr), next(nullptr) {}
    };
    
    std::atomic<Node*> head_;
    std::atomic<Node*> tail_;
    
public:
    LockFreeQueue() {
        Node* dummy = new Node;
        head_.store(dummy);
        tail_.store(dummy);
    }
    
    ~LockFreeQueue() {
        while (Node* old_head = head_.load()) {
            head_.store(old_head->next);
            delete old_head;
        }
    }
    
    void enqueue(const T& item) {
        Node* new_node = new Node;
        T* data = new T(item);
        new_node->data.store(data);
        
        while (true) {
            Node* last = tail_.load();
            Node* next = last->next.load();
            
            if (last == tail_.load()) {  // Still the same tail?
                if (next == nullptr) {
                    // Try to link new node at the end of the list
                    if (last->next.compare_exchange_weak(next, new_node)) {
                        break;  // Successfully linked
                    }
                } else {
                    // Try to swing tail to the next node
                    tail_.compare_exchange_weak(last, next);
                }
            }
        }
        
        // Try to swing tail to the new node
        tail_.compare_exchange_weak(tail_.load(), new_node);
    }
    
    bool dequeue(T& result) {
        while (true) {
            Node* first = head_.load();
            Node* last = tail_.load();
            Node* next = first->next.load();
            
            if (first == head_.load()) {  // Still the same head?
                if (first == last) {
                    if (next == nullptr) {
                        return false;  // Queue is empty
                    }
                    // Try to advance tail
                    tail_.compare_exchange_weak(last, next);
                } else {
                    if (next == nullptr) {
                        continue;  // Inconsistent state, retry
                    }
                    
                    // Read data before CAS
                    T* data = next->data.load();
                    if (data == nullptr) {
                        continue;  // Another thread got the data
                    }
                    
                    // Try to swing head to the next node
                    if (head_.compare_exchange_weak(first, next)) {
                        result = *data;
                        delete data;
                        delete first;
                        return true;
                    }
                }
            }
        }
    }
};
```

---

## 📚 **C++ Study Guide & Best Practices**

### 🎯 **Essential C++ Concepts for Data Engineers**

#### **Core Modern C++ Features**
1. **Smart Pointers**: RAII and automatic memory management
2. **Move Semantics**: Efficient resource transfer
3. **Templates**: Generic programming and metaprogramming
4. **STL Algorithms**: Efficient, tested algorithms
5. **Concurrency**: std::thread, std::async, atomics

#### **Performance Optimization**
1. **Memory Layout**: Cache-friendly data structures
2. **SIMD**: Vectorized operations for numerical data
3. **Move Semantics**: Avoid unnecessary copies
4. **Template Metaprogramming**: Compile-time optimizations
5. **Lock-Free Programming**: High-performance concurrent data structures

### 🚀 **Best Practices for Data Engineering**

#### **Memory Management**
- Use RAII for automatic resource cleanup
- Prefer smart pointers over raw pointers
- Implement custom allocators for specific use cases
- Use memory pools for frequent allocations

#### **Performance**
- Profile before optimizing
- Use appropriate STL containers
- Leverage parallel algorithms
- Optimize for cache locality

### 🔗 **Essential Resources**

- **Modern C++**: "Effective Modern C++" by Scott Meyers
- **Performance**: "Optimized C++" by Kurt Guntheroth
- **Concurrency**: "C++ Concurrency in Action" by Anthony Williams
- **Templates**: "C++ Templates: The Complete Guide" by Vandevoorde & Josuttis

---

**Remember**: C++ provides both high-level abstractions and low-level control. Focus on modern C++ features, RAII, and performance optimization techniques for data engineering applications.
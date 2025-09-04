# Shell Scripting Interview Questions for Data Engineering

## Bash Fundamentals

### Q1: How do you process CSV files with shell commands?
**Answer:**
```bash
# Extract specific columns
cut -d',' -f1,3,5 data.csv > selected_columns.csv

# Filter rows based on conditions
awk -F',' '$3 > 1000 {print}' sales.csv > high_value_sales.csv

# Remove header and process data
tail -n +2 data.csv | while IFS=',' read -r id name value; do
    echo "Processing: $name with value $value"
done

# Count unique values in a column
cut -d',' -f2 data.csv | sort | uniq -c | sort -nr

# Calculate sum of a column
awk -F',' '{sum += $3} END {print "Total:", sum}' data.csv
```

### Q2: How do you monitor and process log files?
**Answer:**
```bash
# Real-time log monitoring
tail -f /var/log/application.log | grep ERROR

# Extract error patterns
grep -E "(ERROR|FATAL)" app.log | awk '{print $1, $2, $NF}'

# Count log levels
awk '{print $3}' app.log | sort | uniq -c

# Process logs by date range
awk '/2023-12-01/,/2023-12-31/ {print}' app.log

# Extract and analyze response times
grep "response_time" app.log | \
awk '{print $NF}' | \
awk '{sum+=$1; count++} END {print "Avg:", sum/count}'
```

## Data Processing Scripts

### Q3: How do you create a data pipeline script?
**Answer:**
```bash
#!/bin/bash

# Data pipeline script
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
SOURCE_DIR="/data/input"
PROCESSED_DIR="/data/processed"
ARCHIVE_DIR="/data/archive"
LOG_FILE="/var/log/data_pipeline.log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Process data files
process_files() {
    local file_count=0
    
    for file in "$SOURCE_DIR"/*.csv; do
        if [[ -f "$file" ]]; then
            local filename=$(basename "$file")
            log "Processing $filename"
            
            # Data validation
            if ! validate_csv "$file"; then
                log "ERROR: Invalid CSV format in $filename"
                continue
            fi
            
            # Transform data
            awk -F',' '
                NR==1 {print; next}  # Keep header
                $3 > 0 {             # Filter positive values
                    $4 = $3 * 1.1    # Apply transformation
                    print
                }
            ' "$file" > "$PROCESSED_DIR/$filename"
            
            # Archive original
            mv "$file" "$ARCHIVE_DIR/"
            ((file_count++))
        fi
    done
    
    log "Processed $file_count files"
}

# CSV validation function
validate_csv() {
    local file="$1"
    local expected_cols=4
    
    # Check if file has consistent column count
    awk -F',' 'NF != '$expected_cols' {exit 1}' "$file"
}

# Main execution
main() {
    log "Starting data pipeline"
    
    # Create directories if they don't exist
    mkdir -p "$PROCESSED_DIR" "$ARCHIVE_DIR"
    
    # Process files
    process_files
    
    log "Pipeline completed successfully"
}

# Run main function
main "$@"
```

### Q4: How do you implement error handling and retry logic?
**Answer:**
```bash
#!/bin/bash

# Retry function with exponential backoff
retry_with_backoff() {
    local max_attempts=5
    local delay=1
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if "$@"; then
            return 0
        fi
        
        echo "Attempt $attempt failed. Retrying in ${delay}s..."
        sleep $delay
        
        ((attempt++))
        delay=$((delay * 2))  # Exponential backoff
    done
    
    echo "All $max_attempts attempts failed"
    return 1
}

# Database connection with retry
connect_to_db() {
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "SELECT 1;" &>/dev/null
}

# File download with retry
download_file() {
    local url="$1"
    local output="$2"
    
    curl -f -o "$output" "$url"
}

# Usage examples
if retry_with_backoff connect_to_db; then
    echo "Database connection successful"
else
    echo "Failed to connect to database after retries"
    exit 1
fi

if retry_with_backoff download_file "https://api.example.com/data.csv" "data.csv"; then
    echo "File downloaded successfully"
else
    echo "Failed to download file"
    exit 1
fi
```

## System Administration

### Q5: How do you monitor system resources for data processing?
**Answer:**
```bash
#!/bin/bash

# System monitoring script
monitor_system() {
    local threshold_cpu=80
    local threshold_memory=85
    local threshold_disk=90
    
    # CPU usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    
    # Memory usage
    memory_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    
    # Disk usage
    disk_usage=$(df -h / | awk 'NR==2 {print $5}' | cut -d'%' -f1)
    
    echo "System Resources:"
    echo "CPU: ${cpu_usage}%"
    echo "Memory: ${memory_usage}%"
    echo "Disk: ${disk_usage}%"
    
    # Alerts
    if (( $(echo "$cpu_usage > $threshold_cpu" | bc -l) )); then
        echo "ALERT: High CPU usage!"
    fi
    
    if [[ $memory_usage -gt $threshold_memory ]]; then
        echo "ALERT: High memory usage!"
    fi
    
    if [[ $disk_usage -gt $threshold_disk ]]; then
        echo "ALERT: High disk usage!"
    fi
}

# Process monitoring
monitor_processes() {
    echo "Top CPU consuming processes:"
    ps aux --sort=-%cpu | head -10
    
    echo -e "\nTop Memory consuming processes:"
    ps aux --sort=-%mem | head -10
}

# Network monitoring
monitor_network() {
    echo "Network connections:"
    netstat -tuln | grep LISTEN
    
    echo -e "\nNetwork traffic:"
    sar -n DEV 1 1 | grep -v "^$"
}

# Run monitoring
monitor_system
monitor_processes
monitor_network
```

### Q6: How do you automate database operations?
**Answer:**
```bash
#!/bin/bash

# Database operations script
DB_HOST="localhost"
DB_USER="dataeng"
DB_NAME="analytics"

# Execute SQL query
execute_query() {
    local query="$1"
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "$query"
}

# Backup database
backup_database() {
    local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
    
    mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$backup_file"
    
    if [[ $? -eq 0 ]]; then
        echo "Backup created: $backup_file"
        gzip "$backup_file"
    else
        echo "Backup failed"
        return 1
    fi
}

# Data import from CSV
import_csv_to_table() {
    local csv_file="$1"
    local table_name="$2"
    
    # Validate CSV file
    if [[ ! -f "$csv_file" ]]; then
        echo "CSV file not found: $csv_file"
        return 1
    fi
    
    # Import data
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" \
        --local-infile=1 -e "
        LOAD DATA LOCAL INFILE '$csv_file'
        INTO TABLE $table_name
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS;"
}

# Data quality checks
run_data_quality_checks() {
    echo "Running data quality checks..."
    
    # Check for duplicates
    local duplicates=$(execute_query "
        SELECT COUNT(*) as duplicate_count 
        FROM (
            SELECT customer_id, COUNT(*) 
            FROM customers 
            GROUP BY customer_id 
            HAVING COUNT(*) > 1
        ) as dups;")
    
    echo "Duplicate records: $duplicates"
    
    # Check for null values
    local null_count=$(execute_query "
        SELECT COUNT(*) as null_count 
        FROM customers 
        WHERE email IS NULL OR email = '';")
    
    echo "Records with null emails: $null_count"
}

# Usage
backup_database
import_csv_to_table "new_customers.csv" "customers"
run_data_quality_checks
```

## Advanced Scripting

### Q7: How do you implement parallel processing in shell scripts?
**Answer:**
```bash
#!/bin/bash

# Parallel processing with background jobs
process_files_parallel() {
    local max_jobs=4
    local job_count=0
    
    for file in *.csv; do
        # Wait if we've reached max jobs
        while [[ $job_count -ge $max_jobs ]]; do
            wait -n  # Wait for any job to complete
            ((job_count--))
        done
        
        # Start background job
        {
            echo "Processing $file"
            process_single_file "$file"
            echo "Completed $file"
        } &
        
        ((job_count++))
    done
    
    # Wait for all remaining jobs
    wait
}

# Using xargs for parallel execution
parallel_with_xargs() {
    find . -name "*.csv" | xargs -n 1 -P 4 process_single_file
}

# GNU parallel (if available)
parallel_with_gnu() {
    parallel -j 4 process_single_file ::: *.csv
}

# Process single file function
process_single_file() {
    local file="$1"
    
    # Simulate processing time
    sleep 2
    
    # Actual processing
    awk -F',' '{sum += $3} END {print FILENAME, sum}' "$file" >> results.txt
}

# Choose method based on availability
if command -v parallel &> /dev/null; then
    parallel_with_gnu
elif command -v xargs &> /dev/null; then
    parallel_with_xargs
else
    process_files_parallel
fi
```

### Q8: How do you create configuration-driven scripts?
**Answer:**
```bash
#!/bin/bash

# Configuration file: config.conf
# SOURCE_DIR=/data/input
# TARGET_DIR=/data/output
# LOG_LEVEL=INFO
# MAX_RETRIES=3
# BATCH_SIZE=1000

# Load configuration
load_config() {
    local config_file="${1:-config.conf}"
    
    if [[ -f "$config_file" ]]; then
        # Source the config file
        source "$config_file"
        
        # Set defaults for missing values
        SOURCE_DIR="${SOURCE_DIR:-/tmp/input}"
        TARGET_DIR="${TARGET_DIR:-/tmp/output}"
        LOG_LEVEL="${LOG_LEVEL:-INFO}"
        MAX_RETRIES="${MAX_RETRIES:-3}"
        BATCH_SIZE="${BATCH_SIZE:-100}"
        
        echo "Configuration loaded from $config_file"
    else
        echo "Config file not found, using defaults"
        set_defaults
    fi
}

# Set default values
set_defaults() {
    SOURCE_DIR="/tmp/input"
    TARGET_DIR="/tmp/output"
    LOG_LEVEL="INFO"
    MAX_RETRIES=3
    BATCH_SIZE=100
}

# Logging with levels
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$LOG_LEVEL" in
        DEBUG) levels="DEBUG INFO WARN ERROR" ;;
        INFO)  levels="INFO WARN ERROR" ;;
        WARN)  levels="WARN ERROR" ;;
        ERROR) levels="ERROR" ;;
    esac
    
    if [[ " $levels " =~ " $level " ]]; then
        echo "[$timestamp] [$level] $message"
    fi
}

# Main processing function
main() {
    load_config "$1"
    
    log "INFO" "Starting data processing"
    log "DEBUG" "Source: $SOURCE_DIR, Target: $TARGET_DIR"
    
    # Create directories
    mkdir -p "$TARGET_DIR"
    
    # Process files in batches
    local file_count=0
    for file in "$SOURCE_DIR"/*.csv; do
        if [[ -f "$file" ]]; then
            log "INFO" "Processing $(basename "$file")"
            
            # Process in batches
            split -l "$BATCH_SIZE" "$file" "${TARGET_DIR}/batch_"
            
            ((file_count++))
        fi
    done
    
    log "INFO" "Processed $file_count files"
}

# Run with config file as argument
main "$@"
```

## Key Takeaways

**Essential Shell Scripting for Data Engineering:**
- File processing with awk, sed, cut
- Error handling and retry mechanisms
- Parallel processing for performance
- System monitoring and alerting
- Database automation
- Configuration management
- Logging and debugging
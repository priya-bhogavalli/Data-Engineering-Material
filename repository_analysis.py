#!/usr/bin/env python3
"""
Repository Analysis Script
Identifies redundant, incomplete, and duplicate files throughout the repository.
"""

import os
import hashlib
from collections import defaultdict
from pathlib import Path

def get_file_hash(filepath):
    """Calculate MD5 hash of file content"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def get_file_size(filepath):
    """Get file size in bytes"""
    try:
        return os.path.getsize(filepath)
    except:
        return 0

def analyze_repository(root_path):
    """Analyze repository for duplicates, redundancy, and incomplete files"""
    
    # Data structures for analysis
    files_by_hash = defaultdict(list)
    files_by_name = defaultdict(list)
    files_by_content_similarity = defaultdict(list)
    incomplete_files = []
    redundant_structures = []
    
    # Walk through all files
    for root, dirs, files in os.walk(root_path):
        # Skip hidden directories and common build/cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'build', 'dist']]
        
        for file in files:
            if file.startswith('.'):
                continue
                
            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, root_path)
            
            # Get file info
            file_hash = get_file_hash(filepath)
            file_size = get_file_size(filepath)
            
            if file_hash:
                files_by_hash[file_hash].append({
                    'path': relative_path,
                    'size': file_size,
                    'name': file
                })
            
            # Group by filename
            files_by_name[file].append({
                'path': relative_path,
                'size': file_size,
                'hash': file_hash
            })
            
            # Check for incomplete files (very small or empty)
            if file_size < 100 and file.endswith('.md'):
                incomplete_files.append({
                    'path': relative_path,
                    'size': file_size
                })
    
    return {
        'duplicates_by_hash': {k: v for k, v in files_by_hash.items() if len(v) > 1},
        'duplicates_by_name': {k: v for k, v in files_by_name.items() if len(v) > 1},
        'incomplete_files': incomplete_files
    }

def identify_structural_redundancy(root_path):
    """Identify redundant directory structures and file patterns"""
    
    redundant_patterns = []
    
    # Known duplicate patterns from manual inspection
    known_duplicates = [
        # SnapLogic duplicates
        ('Core-Data-Engineering/Data-Processing/ETL/SNAPLOGIC_KEY_CONCEPTS.md',
         'Core-Data-Engineering/Data-Processing/ETL/Snaplogic/SNAPLOGIC_KEY_CONCEPTS.md'),
        
        # Neo4j duplicates
        ('Core-Data-Engineering/Databases/NoSQL/Neo4j/NEO4J_KEY_CONCEPTS.md',
         'Core-Data-Engineering/Databases/Graph-Databases/Neo4j/NEO4J_KEY_CONCEPTS.md'),
        ('Core-Data-Engineering/Databases/NoSQL/Neo4j/NEO4J_INTERVIEW_QUESTIONS.md',
         'Core-Data-Engineering/Databases/Graph-Databases/Neo4j/NEO4J_INTERVIEW_QUESTIONS.md'),
        
        # Redis duplicates
        ('Core-Data-Engineering/Databases/NoSQL/Redis/',
         'Core-Data-Engineering/Databases/In-Memory/Redis/'),
        
        # GenAI duplicates
        ('Supporting-Tools/AI/GenAI/EMBEDDINGS_KEY_CONCEPTS.md',
         'Supporting-Tools/AI/GenAI/Embeddings/EMBEDDINGS_KEY_CONCEPTS.md'),
        ('Supporting-Tools/AI/GenAI/OPENAI_API_KEY_CONCEPTS.md',
         'Supporting-Tools/AI/GenAI/OpenAI-API/OPENAI_API_KEY_CONCEPTS.md'),
        ('Supporting-Tools/AI/GenAI/RAGS_KEY_CONCEPTS.md',
         'Supporting-Tools/AI/GenAI/RAGs/RAGS_KEY_CONCEPTS.md'),
        ('Supporting-Tools/AI/GenAI/VECTOR_DB_KEY_CONCEPTS.md',
         'Supporting-Tools/AI/GenAI/Vector-DB/VECTOR_DB_KEY_CONCEPTS.md'),
        ('Supporting-Tools/AI/GenAI/GENAI_KEY_CONCEPTS.md',
         'Supporting-Tools/AI/GenAI/GenAI/'),
        
        # CI/CD duplicates
        ('Supporting-Tools/DevOps-Automation/CICD_KEY_CONCEPTS.md',
         'Supporting-Tools/DevOps-Automation/CI-CD/CICD_KEY_CONCEPTS.md'),
        ('Supporting-Tools/DevOps-Automation/CIRCLECI_KEY_CONCEPTS.md',
         'Supporting-Tools/DevOps-Automation/CircleCI/CIRCLECI_KEY_CONCEPTS.md'),
        
        # Elasticsearch duplicates
        ('Core-Data-Engineering/Databases/Search-Engines/Elasticsearch/',
         'Supporting-Tools/Visualization-Reporting/Elastic-Search/')
    ]
    
    return known_duplicates

def generate_report(analysis_results, structural_redundancy, root_path):
    """Generate comprehensive analysis report"""
    
    report = []
    report.append("# Repository Analysis Report")
    report.append("=" * 50)
    report.append("")
    
    # Exact duplicates by hash
    report.append("## 1. EXACT DUPLICATES (Same Content)")
    report.append("-" * 40)
    if analysis_results['duplicates_by_hash']:
        for file_hash, files in analysis_results['duplicates_by_hash'].items():
            report.append(f"\n**Duplicate Set (Hash: {file_hash[:8]}...):**")
            for file_info in files:
                report.append(f"  - {file_info['path']} ({file_info['size']} bytes)")
    else:
        report.append("No exact duplicates found.")
    report.append("")
    
    # Files with same name
    report.append("## 2. SAME FILENAME (Potential Duplicates)")
    report.append("-" * 40)
    if analysis_results['duplicates_by_name']:
        for filename, files in analysis_results['duplicates_by_name'].items():
            if len(files) > 1:
                report.append(f"\n**Filename: {filename}**")
                for file_info in files:
                    report.append(f"  - {file_info['path']} ({file_info['size']} bytes)")
    else:
        report.append("No filename duplicates found.")
    report.append("")
    
    # Structural redundancy
    report.append("## 3. STRUCTURAL REDUNDANCY")
    report.append("-" * 40)
    report.append("**Known redundant structures:**")
    for duplicate_pair in structural_redundancy:
        report.append(f"  - {duplicate_pair[0]}")
        report.append(f"    DUPLICATE OF: {duplicate_pair[1]}")
        report.append("")
    
    # Incomplete files
    report.append("## 4. INCOMPLETE FILES (< 100 bytes)")
    report.append("-" * 40)
    if analysis_results['incomplete_files']:
        for file_info in analysis_results['incomplete_files']:
            report.append(f"  - {file_info['path']} ({file_info['size']} bytes)")
    else:
        report.append("No incomplete files found.")
    report.append("")
    
    # Recommendations
    report.append("## 5. RECOMMENDATIONS")
    report.append("-" * 40)
    report.append("### Immediate Actions:")
    report.append("1. **Remove duplicate files** - Keep one version, delete others")
    report.append("2. **Consolidate redundant structures** - Merge similar directories")
    report.append("3. **Complete incomplete files** - Add content or remove empty files")
    report.append("4. **Standardize naming** - Use consistent file naming conventions")
    report.append("")
    
    report.append("### Structural Improvements:")
    report.append("1. **Neo4j**: Remove from NoSQL, keep only in Graph-Databases")
    report.append("2. **Redis**: Remove from NoSQL, keep only in In-Memory")
    report.append("3. **GenAI**: Remove root-level files, keep only in subdirectories")
    report.append("4. **CI/CD**: Consolidate into single location")
    report.append("5. **Elasticsearch**: Choose one location (Database vs Visualization)")
    report.append("")
    
    return "\n".join(report)

def main():
    root_path = r"c:\Users\z00542ky\Data-Engineering-Material"
    
    print("Analyzing repository structure...")
    analysis_results = analyze_repository(root_path)
    structural_redundancy = identify_structural_redundancy(root_path)
    
    print("Generating report...")
    report = generate_report(analysis_results, structural_redundancy, root_path)
    
    # Save report
    report_path = os.path.join(root_path, "REPOSITORY_ANALYSIS_REPORT.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Analysis complete! Report saved to: {report_path}")
    print("\nSummary:")
    print(f"- Exact duplicates: {len(analysis_results['duplicates_by_hash'])}")
    print(f"- Filename duplicates: {len([k for k, v in analysis_results['duplicates_by_name'].items() if len(v) > 1])}")
    print(f"- Structural redundancies: {len(structural_redundancy)}")
    print(f"- Incomplete files: {len(analysis_results['incomplete_files'])}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3

import os
import sys

def check_folder_structure(root_path):
    """Check which folders are missing KEY_CONCEPTS.md and INTERVIEW_QUESTIONS.md files"""
    
    missing_files = []
    
    # Walk through all directories
    for root, dirs, files in os.walk(root_path):
        # Skip hidden directories and common non-tool directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git']]
        
        # Check if this directory contains any .md files (indicating it's a tool directory)
        md_files = [f for f in files if f.endswith('.md')]
        
        if md_files:
            # Get relative path for cleaner output
            rel_path = os.path.relpath(root, root_path)
            if rel_path == '.':
                rel_path = 'root'
            
            # Check for KEY_CONCEPTS.md
            key_concepts_files = [f for f in md_files if 'KEY_CONCEPTS' in f.upper()]
            interview_files = [f for f in md_files if 'INTERVIEW_QUESTIONS' in f.upper()]
            
            missing = []
            if not key_concepts_files:
                missing.append('KEY_CONCEPTS')
            if not interview_files:
                missing.append('INTERVIEW_QUESTIONS')
            
            if missing:
                missing_files.append({
                    'path': rel_path,
                    'missing': missing,
                    'existing_files': md_files
                })
    
    return missing_files

def main():
    root_path = r"c:\Users\z00542ky\Data-Engineering-Material"
    
    print("Checking repository structure for missing KEY_CONCEPTS.md and INTERVIEW_QUESTIONS.md files...")
    print("=" * 80)
    
    missing_files = check_folder_structure(root_path)
    
    if not missing_files:
        print("✅ All folders have the required KEY_CONCEPTS.md and INTERVIEW_QUESTIONS.md files!")
        return
    
    print(f"Found {len(missing_files)} folders missing required files:\n")
    
    for item in missing_files:
        print(f"📁 Path: {item['path']}")
        print(f"❌ Missing: {', '.join(item['missing'])}")
        print(f"📄 Existing files: {', '.join(item['existing_files'][:3])}{'...' if len(item['existing_files']) > 3 else ''}")
        print("-" * 60)

if __name__ == "__main__":
    main()
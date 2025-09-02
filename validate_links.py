#!/usr/bin/env python3
"""
Link Validation Script for Data Engineering Material Repository
Checks all markdown files for broken internal links and generates a report.
"""

import os
import re
import glob
from pathlib import Path
from collections import defaultdict

def find_markdown_files(root_dir):
    """Find all markdown files in the repository."""
    markdown_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip .git and other hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def extract_links(file_path):
    """Extract all markdown links from a file."""
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find markdown links [text](link)
        link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, content)
        
        for text, link in matches:
            # Skip external links (http/https)
            if not link.startswith(('http://', 'https://', 'mailto:', '#')):
                links.append((text, link, file_path))
                
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        
    return links

def validate_link(link, source_file):
    """Validate if a link exists."""
    # Convert relative path to absolute
    source_dir = os.path.dirname(source_file)
    
    # Handle anchor links (skip for now)
    if link.startswith('#'):
        return True
        
    # Clean up the link
    link = link.split('#')[0]  # Remove anchor part
    
    # Handle different link formats
    if link.startswith('./'):
        link = link[2:]
        target_path = os.path.normpath(os.path.join(source_dir, link))
    elif link.startswith('../'):
        # Handle relative paths
        target_path = os.path.normpath(os.path.join(source_dir, link))
    else:
        # Assume it's relative to source directory
        target_path = os.path.normpath(os.path.join(source_dir, link))
    
    # Check if it's a directory or file
    if os.path.exists(target_path):
        return True
    
    # If it doesn't exist as-is, try adding .md extension
    if not target_path.endswith('.md'):
        md_path = target_path + '.md'
        if os.path.exists(md_path):
            return True
            
    return False

def main():
    """Main function to validate all links."""
    repo_root = os.path.dirname(os.path.abspath(__file__))
    print(f"Validating links in: {repo_root}")
    
    # Find all markdown files
    markdown_files = find_markdown_files(repo_root)
    print(f"Found {len(markdown_files)} markdown files")
    
    # Extract and validate links
    broken_links = []
    total_links = 0
    
    for md_file in markdown_files:
        links = extract_links(md_file)
        total_links += len(links)
        
        for text, link, source in links:
            if not validate_link(link, source):
                broken_links.append({
                    'source': source.replace(repo_root, ''),
                    'text': text,
                    'link': link
                })
    
    # Generate report
    print(f"\n=== LINK VALIDATION REPORT ===")
    print(f"Total links checked: {total_links}")
    print(f"Broken links found: {len(broken_links)}")
    
    if broken_links:
        print(f"\n=== BROKEN LINKS ===")
        by_file = defaultdict(list)
        for broken in broken_links:
            by_file[broken['source']].append(broken)
            
        for file_path, links in sorted(by_file.items()):
            print(f"\nFile: {file_path}")
            for link in links:
                print(f"  - [{link['text']}]({link['link']})")
    else:
        print("All links are valid!")
    
    # Save report to file
    report_file = os.path.join(repo_root, 'link_validation_report.txt')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("LINK VALIDATION REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Total links checked: {total_links}\n")
        f.write(f"Broken links found: {len(broken_links)}\n\n")
        
        if broken_links:
            f.write("BROKEN LINKS:\n")
            f.write("-" * 20 + "\n")
            by_file = defaultdict(list)
            for broken in broken_links:
                by_file[broken['source']].append(broken)
                
            for file_path, links in sorted(by_file.items()):
                f.write(f"\nFile: {file_path}\n")
                for link in links:
                    f.write(f"  - [{link['text']}]({link['link']})\n")
        else:
            f.write("All links are valid!\n")
    
    print(f"\nReport saved to: {report_file}")

if __name__ == "__main__":
    main()
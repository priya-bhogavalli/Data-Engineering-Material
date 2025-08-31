#!/usr/bin/env python3
"""
Script to identify and fix broken links in markdown files.
This script scans markdown files for internal links and checks if the referenced files exist.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict

def find_markdown_files(root_dir: str) -> List[Path]:
    """Find all markdown files in the directory tree."""
    markdown_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(Path(root) / file)
    return markdown_files

def extract_internal_links(content: str) -> List[str]:
    """Extract internal links from markdown content."""
    # Pattern to match markdown links: [text](./path/to/file.md)
    pattern = r'\[([^\]]+)\]\((\./[^)]+)\)'
    matches = re.findall(pattern, content)
    return [match[1] for match in matches]

def check_link_exists(base_path: Path, link: str) -> bool:
    """Check if a link target exists."""
    # Remove leading './' from link
    clean_link = link.lstrip('./')
    target_path = base_path.parent / clean_link
    
    # If it's a directory link, check if directory exists
    if not clean_link.endswith('.md'):
        return target_path.is_dir()
    
    # If it's a file link, check if file exists
    return target_path.is_file()

def analyze_broken_links(root_dir: str) -> Dict[str, List[Tuple[str, bool]]]:
    """Analyze all markdown files for broken links."""
    markdown_files = find_markdown_files(root_dir)
    results = {}
    
    for md_file in markdown_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            links = extract_internal_links(content)
            link_status = []
            
            for link in links:
                exists = check_link_exists(md_file, link)
                link_status.append((link, exists))
            
            if link_status:  # Only include files that have links
                results[str(md_file)] = link_status
                
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    return results

def generate_report(results: Dict[str, List[Tuple[str, bool]]]) -> None:
    """Generate a report of broken links."""
    print("=" * 80)
    print("BROKEN LINKS ANALYSIS REPORT")
    print("=" * 80)
    
    total_files = len(results)
    total_links = sum(len(links) for links in results.values())
    broken_links = sum(1 for links in results.values() for link, exists in links if not exists)
    
    print(f"\nSUMMARY:")
    print(f"- Files analyzed: {total_files}")
    print(f"- Total internal links: {total_links}")
    print(f"- Broken links: {broken_links}")
    print(f"- Success rate: {((total_links - broken_links) / total_links * 100):.1f}%" if total_links > 0 else "N/A")
    
    print(f"\nBROKEN LINKS BY FILE:")
    print("-" * 80)
    
    for file_path, links in results.items():
        broken_in_file = [(link, exists) for link, exists in links if not exists]
        if broken_in_file:
            print(f"\n[FILE] {file_path}")
            for link, _ in broken_in_file:
                print(f"   [BROKEN] {link}")
    
    print(f"\nWORKING LINKS:")
    print("-" * 80)
    
    for file_path, links in results.items():
        working_in_file = [(link, exists) for link, exists in links if exists]
        if working_in_file:
            print(f"\n[FILE] {file_path}")
            for link, _ in working_in_file:
                print(f"   [OK] {link}")

def suggest_fixes(results: Dict[str, List[Tuple[str, bool]]]) -> None:
    """Suggest fixes for broken links."""
    print("\n" + "=" * 80)
    print("SUGGESTED FIXES")
    print("=" * 80)
    
    # Common patterns and suggestions
    suggestions = {
        'by-skill-area': 'Replace with ./Core-Data-Engineering/ or ./Supporting-Tools/',
        'interview-simulator': 'Replace with ./docs/INTERVIEW_QUESTIONS_MASTER_INDEX.md',
        '_INTERVIEW_QUESTIONS.md': 'Check if file exists with different naming convention',
        'examples/': 'Verify examples directory exists in the target folder'
    }
    
    for file_path, links in results.items():
        broken_in_file = [(link, exists) for link, exists in links if not exists]
        if broken_in_file:
            print(f"\n[FILE] {file_path}")
            for link, _ in broken_in_file:
                print(f"   [FIX] {link}")
                
                # Provide specific suggestions
                for pattern, suggestion in suggestions.items():
                    if pattern in link:
                        print(f"      [SUGGESTION] {suggestion}")
                        break
                else:
                    print(f"      [SUGGESTION] Check if path exists or use directory link instead")

if __name__ == "__main__":
    # Get the current directory (should be the repo root)
    root_directory = os.getcwd()
    
    print(f"Analyzing markdown files in: {root_directory}")
    print("This may take a moment...")
    
    # Analyze broken links
    results = analyze_broken_links(root_directory)
    
    # Generate report
    generate_report(results)
    
    # Suggest fixes
    suggest_fixes(results)
    
    print(f"\n" + "=" * 80)
    print("NEXT STEPS:")
    print("1. Review the broken links above")
    print("2. Update the markdown files to fix broken links")
    print("3. Consider creating missing files or directories")
    print("4. Re-run this script to verify fixes")
    print("=" * 80)
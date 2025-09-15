import os
import json

def analyze_tool_structure():
    """Analyze repository structure and identify inconsistencies"""
    
    # Expected structure based on Apache Spark pattern
    expected_files = {
        'KEY_CONCEPTS': '*_KEY_CONCEPTS.md',
        'INTERVIEW_QUESTIONS': '*_INTERVIEW_QUESTIONS.md',
        'examples': 'examples/',
        'ALL_FEATURES_REFERENCE': '*_ALL_FEATURES_REFERENCE.md',
        'COMPLETE_GUIDE': '*_COMPLETE_GUIDE.md',
        'BEST_PRACTICES': '*_BEST_PRACTICES.md'
    }
    
    # Core expected files (minimum)
    core_files = ['KEY_CONCEPTS', 'INTERVIEW_QUESTIONS']
    
    results = {
        'well_structured': [],
        'missing_core_files': [],
        'missing_examples': [],
        'missing_advanced_files': [],
        'inconsistent_naming': [],
        'empty_directories': []
    }
    
    base_path = r"c:\Users\z00542ky\Data-Engineering-Material"
    
    def scan_directory(path, tool_name=""):
        """Recursively scan directories for tool folders"""
        try:
            items = os.listdir(path)
            
            # Check if this is a tool directory (has .md files)
            md_files = [f for f in items if f.endswith('.md')]
            subdirs = [d for d in items if os.path.isdir(os.path.join(path, d)) and not d.startswith('.')]
            
            if md_files:  # This is a tool directory
                analyze_tool_directory(path, tool_name or os.path.basename(path), md_files, subdirs)
            
            # Recurse into subdirectories
            for subdir in subdirs:
                subdir_path = os.path.join(path, subdir)
                scan_directory(subdir_path, subdir)
                
        except PermissionError:
            pass
    
    def analyze_tool_directory(path, tool_name, md_files, subdirs):
        """Analyze individual tool directory structure"""
        relative_path = path.replace(base_path, "").replace("\\", "/").lstrip("/")
        
        # Check for core files
        has_key_concepts = any('KEY_CONCEPTS' in f.upper() for f in md_files)
        has_interview_questions = any('INTERVIEW_QUESTIONS' in f.upper() for f in md_files)
        has_examples = 'examples' in subdirs
        
        # Check for advanced files
        has_all_features = any('ALL_FEATURES_REFERENCE' in f.upper() for f in md_files)
        has_complete_guide = any('COMPLETE_GUIDE' in f.upper() for f in md_files)
        has_best_practices = any('BEST_PRACTICES' in f.upper() for f in md_files)
        
        # Categorize the tool
        if has_key_concepts and has_interview_questions:
            if has_examples and (has_all_features or has_complete_guide):
                results['well_structured'].append({
                    'tool': tool_name,
                    'path': relative_path,
                    'files': md_files,
                    'has_examples': has_examples
                })
            elif not has_examples:
                results['missing_examples'].append({
                    'tool': tool_name,
                    'path': relative_path,
                    'files': md_files
                })
            elif not (has_all_features or has_complete_guide):
                results['missing_advanced_files'].append({
                    'tool': tool_name,
                    'path': relative_path,
                    'files': md_files,
                    'has_examples': has_examples
                })
        else:
            missing = []
            if not has_key_concepts:
                missing.append('KEY_CONCEPTS')
            if not has_interview_questions:
                missing.append('INTERVIEW_QUESTIONS')
            
            results['missing_core_files'].append({
                'tool': tool_name,
                'path': relative_path,
                'files': md_files,
                'missing': missing
            })
        
        # Check for naming inconsistencies
        inconsistent = []
        for f in md_files:
            if not any(pattern in f.upper() for pattern in ['KEY_CONCEPTS', 'INTERVIEW_QUESTIONS', 'ALL_FEATURES', 'COMPLETE_GUIDE', 'BEST_PRACTICES']):
                inconsistent.append(f)
        
        if inconsistent:
            results['inconsistent_naming'].append({
                'tool': tool_name,
                'path': relative_path,
                'inconsistent_files': inconsistent
            })
    
    # Start analysis
    scan_directory(base_path)
    
    return results

def generate_report(results):
    """Generate comprehensive report"""
    report = []
    
    report.append("# Repository Structure Analysis Report")
    report.append("## Tools Not Following Apache Spark Structure Pattern\n")
    
    # Summary statistics
    total_tools = (len(results['well_structured']) + 
                  len(results['missing_core_files']) + 
                  len(results['missing_examples']) + 
                  len(results['missing_advanced_files']))
    
    report.append(f"**Total Tools Analyzed:** {total_tools}")
    report.append(f"**Well Structured:** {len(results['well_structured'])}")
    report.append(f"**Missing Core Files:** {len(results['missing_core_files'])}")
    report.append(f"**Missing Examples:** {len(results['missing_examples'])}")
    report.append(f"**Missing Advanced Files:** {len(results['missing_advanced_files'])}")
    report.append("")
    
    # Detailed analysis
    if results['missing_core_files']:
        report.append("## 🚨 Critical Issues: Missing Core Files")
        report.append("These tools are missing essential KEY_CONCEPTS.md or INTERVIEW_QUESTIONS.md files:\n")
        for item in results['missing_core_files']:
            report.append(f"### {item['tool']}")
            report.append(f"**Path:** `{item['path']}`")
            report.append(f"**Missing:** {', '.join(item['missing'])}")
            report.append(f"**Current Files:** {', '.join(item['files'])}")
            report.append("")
    
    if results['missing_examples']:
        report.append("## 📁 Missing Examples Directory")
        report.append("These tools lack practical code examples:\n")
        for item in results['missing_examples']:
            report.append(f"### {item['tool']}")
            report.append(f"**Path:** `{item['path']}`")
            report.append(f"**Files:** {', '.join(item['files'])}")
            report.append("")
    
    if results['missing_advanced_files']:
        report.append("## 📚 Missing Advanced Documentation")
        report.append("These tools lack comprehensive guides or feature references:\n")
        for item in results['missing_advanced_files']:
            report.append(f"### {item['tool']}")
            report.append(f"**Path:** `{item['path']}`")
            report.append(f"**Files:** {', '.join(item['files'])}")
            report.append(f"**Has Examples:** {'✅' if item['has_examples'] else '❌'}")
            report.append("")
    
    if results['inconsistent_naming']:
        report.append("## 🏷️ Inconsistent File Naming")
        report.append("These tools have files that don't follow naming conventions:\n")
        for item in results['inconsistent_naming']:
            report.append(f"### {item['tool']}")
            report.append(f"**Path:** `{item['path']}`")
            report.append(f"**Inconsistent Files:** {', '.join(item['inconsistent_files'])}")
            report.append("")
    
    # Well-structured tools (for reference)
    if results['well_structured']:
        report.append("## ✅ Well-Structured Tools (Reference)")
        report.append("These tools follow the Apache Spark structure pattern:\n")
        for item in results['well_structured'][:10]:  # Show first 10
            report.append(f"- **{item['tool']}** (`{item['path']}`)")
        if len(results['well_structured']) > 10:
            report.append(f"- ... and {len(results['well_structured']) - 10} more")
        report.append("")
    
    # Recommendations
    report.append("## 🎯 Recommendations")
    report.append("### Priority 1: Fix Critical Issues")
    report.append("- Add missing KEY_CONCEPTS.md and INTERVIEW_QUESTIONS.md files")
    report.append("- Ensure consistent naming conventions")
    report.append("")
    report.append("### Priority 2: Add Examples")
    report.append("- Create examples/ directories with minimal code samples")
    report.append("- Follow the pattern: minimal_[tool].py with outputs")
    report.append("")
    report.append("### Priority 3: Enhance Documentation")
    report.append("- Add ALL_FEATURES_REFERENCE.md or COMPLETE_GUIDE.md")
    report.append("- Consider adding BEST_PRACTICES.md for major tools")
    
    return "\n".join(report)

if __name__ == "__main__":
    print("Analyzing repository structure...")
    results = analyze_tool_structure()
    
    print("Generating report...")
    report = generate_report(results)
    
    # Save report
    with open(r"c:\Users\z00542ky\Data-Engineering-Material\STRUCTURE_ANALYSIS_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("Report saved to STRUCTURE_ANALYSIS_REPORT.md")
    
    # Print summary
    print(f"\nSummary:")
    print(f"- Well structured: {len(results['well_structured'])}")
    print(f"- Missing core files: {len(results['missing_core_files'])}")
    print(f"- Missing examples: {len(results['missing_examples'])}")
    print(f"- Missing advanced files: {len(results['missing_advanced_files'])}")
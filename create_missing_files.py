import os
import json

def get_missing_tools():
    """Get list of tools missing core files"""
    missing_tools = [
        # High Priority Core Tools
        {"path": "Supporting-Tools/DevOps-Automation/Docker", "tool": "Docker", "missing": ["KEY_CONCEPTS"]},
        {"path": "Supporting-Tools/DevOps-Automation/Kubernetes", "tool": "Kubernetes", "missing": ["KEY_CONCEPTS"]},
        {"path": "Core-Data-Engineering/Programming-Languages/Python", "tool": "Python", "missing": ["KEY_CONCEPTS"]},
        {"path": "Supporting-Tools/Programming/Web/GraphQL", "tool": "GraphQL", "missing": ["KEY_CONCEPTS"]},
        {"path": "Supporting-Tools/Systems/Linux", "tool": "Linux", "missing": ["KEY_CONCEPTS"]},
        
        # Cloud Services
        {"path": "Core-Data-Engineering/Cloud/Azure", "tool": "Azure", "missing": ["KEY_CONCEPTS"]},
        {"path": "Core-Data-Engineering/Cloud/GCP", "tool": "GCP", "missing": ["KEY_CONCEPTS"]},
        {"path": "Core-Data-Engineering/Cloud/AWS/EMR", "tool": "EMR", "missing": ["KEY_CONCEPTS"]},
        
        # Networking
        {"path": "Supporting-Tools/Systems/Networking/DNS", "tool": "DNS", "missing": ["INTERVIEW_QUESTIONS"]},
        {"path": "Supporting-Tools/Systems/Networking/HTTP-HTTPS", "tool": "HTTP-HTTPS", "missing": ["INTERVIEW_QUESTIONS"]},
        
        # Data Processing
        {"path": "Core-Data-Engineering/Data-Processing/Orchestration/Dagster", "tool": "Dagster", "missing": ["KEY_CONCEPTS"]},
        {"path": "Core-Data-Engineering/Data-Processing/Orchestration/Luigi", "tool": "Luigi", "missing": ["KEY_CONCEPTS"]},
        
        # Monitoring
        {"path": "Supporting-Tools/Monitoring/Bigeye", "tool": "Bigeye", "missing": ["KEY_CONCEPTS"]},
        {"path": "Supporting-Tools/Monitoring/Prometheus", "tool": "Prometheus", "missing": ["KEY_CONCEPTS"]},
    ]
    return missing_tools

def create_key_concepts_template(tool_name):
    """Create KEY_CONCEPTS.md template"""
    return f"""# {tool_name} Key Concepts

## 📋 Table of Contents
1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Core Features](#core-features)
4. [Use Cases](#use-cases)
5. [Integration Capabilities](#integration-capabilities)
6. [Best Practices](#best-practices)
7. [Limitations](#limitations)
8. [Version Highlights](#version-highlights)

## 🎯 Introduction

### What is {tool_name}?
{tool_name} is [brief description of the tool and its primary purpose].

### Key Benefits
- **[Benefit 1]**: Description
- **[Benefit 2]**: Description
- **[Benefit 3]**: Description

### Primary Use Cases
- [Use case 1]
- [Use case 2]
- [Use case 3]

## 🏗️ Architecture

### Core Components
1. **[Component 1]**
   - Purpose: [Description]
   - Functionality: [Details]

2. **[Component 2]**
   - Purpose: [Description]
   - Functionality: [Details]

### Architecture Patterns
- **[Pattern 1]**: [Description]
- **[Pattern 2]**: [Description]

## ⚡ Core Features

### Essential Features
1. **[Feature 1]**
   - Description: [Details]
   - Benefits: [Advantages]

2. **[Feature 2]**
   - Description: [Details]
   - Benefits: [Advantages]

### Advanced Features
- **[Advanced Feature 1]**: [Description]
- **[Advanced Feature 2]**: [Description]

## 🎯 Use Cases

### Primary Use Cases
1. **[Use Case 1]**
   - Scenario: [Description]
   - Implementation: [How to implement]
   - Benefits: [Advantages]

2. **[Use Case 2]**
   - Scenario: [Description]
   - Implementation: [How to implement]
   - Benefits: [Advantages]

### Industry Applications
- **[Industry 1]**: [Specific applications]
- **[Industry 2]**: [Specific applications]

## 🔗 Integration Capabilities

### Native Integrations
- **[Integration 1]**: [Description and benefits]
- **[Integration 2]**: [Description and benefits]

### Third-Party Integrations
- **[Tool/Service 1]**: [Integration details]
- **[Tool/Service 2]**: [Integration details]

### APIs and SDKs
- **REST API**: [Capabilities]
- **SDKs**: [Available languages and features]

## 📋 Best Practices

### Configuration Best Practices
1. **[Practice 1]**: [Description and rationale]
2. **[Practice 2]**: [Description and rationale]

### Performance Optimization
- **[Optimization 1]**: [Details]
- **[Optimization 2]**: [Details]

### Security Best Practices
- **[Security Practice 1]**: [Implementation]
- **[Security Practice 2]**: [Implementation]

### Monitoring and Maintenance
- **[Monitoring Practice 1]**: [Details]
- **[Maintenance Practice 1]**: [Details]

## ⚠️ Limitations

### Technical Limitations
- **[Limitation 1]**: [Description and impact]
- **[Limitation 2]**: [Description and impact]

### Scalability Considerations
- **[Consideration 1]**: [Details]
- **[Consideration 2]**: [Details]

### Cost Considerations
- **[Cost Factor 1]**: [Impact]
- **[Cost Factor 2]**: [Impact]

## 🔄 Version Highlights

### Latest Version Features
- **Version [X.X]**: [Key features and improvements]
- **Version [X.X]**: [Key features and improvements]

### Migration Considerations
- **From Version [X] to [Y]**: [Important changes]
- **Breaking Changes**: [Details]

### Roadmap
- **Upcoming Features**: [Planned enhancements]
- **Deprecations**: [Features being phased out]

## 📚 Additional Resources

### Official Documentation
- [Official Documentation](link)
- [API Reference](link)

### Community Resources
- [Community Forum](link)
- [GitHub Repository](link)

### Training and Certification
- [Official Training](link)
- [Certification Programs](link)
"""

def create_interview_questions_template(tool_name):
    """Create INTERVIEW_QUESTIONS.md template"""
    return f"""# {tool_name} Interview Questions

## 📋 Table of Contents
1. [Basic Level Questions](#basic-level-questions)
2. [Intermediate Level Questions](#intermediate-level-questions)
3. [Advanced Level Questions](#advanced-level-questions)
4. [Architecture & Performance](#architecture--performance)
5. [Integration & Development](#integration--development)
6. [Production & Operations](#production--operations)
7. [Scenario-Based Questions](#scenario-based-questions)

## 🟢 Basic Level Questions

### Fundamentals (Questions 1-20)

**1. What is {tool_name} and what is its primary purpose?**
- **Answer**: [Comprehensive answer about the tool's purpose and core functionality]

**2. What are the key benefits of using {tool_name}?**
- **Answer**: [List and explain main advantages]

**3. How does {tool_name} differ from similar tools in the market?**
- **Answer**: [Comparison with competitors and unique features]

**4. What are the main components of {tool_name} architecture?**
- **Answer**: [Explain core architectural components]

**5. What are the system requirements for {tool_name}?**
- **Answer**: [Hardware, software, and network requirements]

**6. How do you install and set up {tool_name}?**
- **Answer**: [Installation steps and initial configuration]

**7. What are the different deployment options for {tool_name}?**
- **Answer**: [On-premises, cloud, hybrid deployment options]

**8. What is the basic workflow when using {tool_name}?**
- **Answer**: [Step-by-step basic usage workflow]

**9. What are the main configuration files in {tool_name}?**
- **Answer**: [Key configuration files and their purposes]

**10. How do you perform basic operations in {tool_name}?**
- **Answer**: [Common operations and commands]

### Core Concepts (Questions 11-20)

**11. What are the key concepts you need to understand to work with {tool_name}?**
- **Answer**: [Essential concepts and terminology]

**12. How does {tool_name} handle [relevant concept like data, requests, etc.]?**
- **Answer**: [Explanation of core processing mechanisms]

**13. What are the different types of [relevant entities] in {tool_name}?**
- **Answer**: [Classification and types of main entities]

**14. How do you configure basic settings in {tool_name}?**
- **Answer**: [Basic configuration procedures]

**15. What are the common use cases for {tool_name}?**
- **Answer**: [Typical applications and scenarios]

**16. How do you troubleshoot common issues in {tool_name}?**
- **Answer**: [Common problems and solutions]

**17. What are the basic security considerations when using {tool_name}?**
- **Answer**: [Fundamental security practices]

**18. How do you backup and restore {tool_name} configurations?**
- **Answer**: [Backup and recovery procedures]

**19. What are the licensing considerations for {tool_name}?**
- **Answer**: [Licensing models and compliance]

**20. How do you get help and support for {tool_name}?**
- **Answer**: [Support channels and resources]

## 🟡 Intermediate Level Questions

### Configuration & Management (Questions 21-50)

**21. How do you optimize {tool_name} performance for medium-scale deployments?**
- **Answer**: [Performance tuning strategies]

**22. What are the advanced configuration options in {tool_name}?**
- **Answer**: [Advanced settings and their impacts]

**23. How do you implement high availability in {tool_name}?**
- **Answer**: [HA setup and best practices]

**24. What are the different authentication methods supported by {tool_name}?**
- **Answer**: [Authentication mechanisms and setup]

**25. How do you implement role-based access control in {tool_name}?**
- **Answer**: [RBAC configuration and management]

[Continue with more intermediate questions...]

## 🔴 Advanced Level Questions

### Expert Configuration (Questions 51-80)

**51. How do you design a highly scalable {tool_name} architecture?**
- **Answer**: [Scalability patterns and implementation]

**52. What are the advanced performance tuning techniques for {tool_name}?**
- **Answer**: [Expert-level optimization strategies]

[Continue with advanced questions...]

## 🏗️ Architecture & Performance

### System Design (Questions 81-100)

**81. How would you design a {tool_name} solution for enterprise-scale requirements?**
- **Answer**: [Enterprise architecture considerations]

[Continue with architecture questions...]

## 🔗 Integration & Development

### Development & APIs (Questions 101-120)

**101. How do you integrate {tool_name} with other systems using APIs?**
- **Answer**: [API integration patterns and examples]

[Continue with integration questions...]

## 🚀 Production & Operations

### Operations & Maintenance (Questions 121-150)

**121. How do you monitor {tool_name} in production environments?**
- **Answer**: [Monitoring strategies and tools]

[Continue with production questions...]

## 🎯 Scenario-Based Questions

### Real-World Scenarios (Questions 151-200)

**151. You need to migrate from [alternative tool] to {tool_name}. How would you approach this?**
- **Answer**: [Migration strategy and considerations]

**152. Your {tool_name} deployment is experiencing performance issues. How do you diagnose and resolve them?**
- **Answer**: [Troubleshooting methodology]

[Continue with scenario questions...]

## 📚 Additional Resources

### Study Materials
- [Official Documentation](link)
- [Best Practices Guide](link)
- [Community Forums](link)

### Hands-On Practice
- [Official Tutorials](link)
- [Sample Projects](link)
- [Certification Prep](link)
"""

def create_files_for_tool(tool_info, base_path):
    """Create missing files for a specific tool"""
    tool_path = os.path.join(base_path, tool_info["path"])
    tool_name = tool_info["tool"]
    
    print(f"Creating files for {tool_name} at {tool_path}")
    
    for missing_type in tool_info["missing"]:
        if missing_type == "KEY_CONCEPTS":
            file_path = os.path.join(tool_path, f"{tool_name.upper()}_KEY_CONCEPTS.md")
            content = create_key_concepts_template(tool_name)
        elif missing_type == "INTERVIEW_QUESTIONS":
            file_path = os.path.join(tool_path, f"{tool_name.upper()}_INTERVIEW_QUESTIONS.md")
            content = create_interview_questions_template(tool_name)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created: {file_path}")
        except Exception as e:
            print(f"❌ Error creating {file_path}: {e}")

if __name__ == "__main__":
    base_path = r"c:\Users\z00542ky\Data-Engineering-Material"
    missing_tools = get_missing_tools()
    
    print(f"Creating files for {len(missing_tools)} tools...")
    
    for tool_info in missing_tools:
        create_files_for_tool(tool_info, base_path)
    
    print("File creation completed!")
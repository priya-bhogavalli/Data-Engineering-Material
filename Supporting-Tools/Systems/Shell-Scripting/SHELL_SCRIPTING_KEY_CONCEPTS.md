# Shell Scripting - Key Concepts

## Overview
Shell scripting involves writing scripts for command-line interpreters to automate tasks, system administration, and data processing workflows.

## Shell Types

### Common Shells
- **Bash**: Bourne Again Shell (most common)
- **Zsh**: Z Shell (macOS default)
- **Fish**: Friendly Interactive Shell
- **Dash**: Debian Almquist Shell
- **Ksh**: Korn Shell

### Script Basics
- **Shebang**: #!/bin/bash
- **Permissions**: chmod +x script.sh
- **Execution**: ./script.sh or bash script.sh
- **Comments**: # for documentation
- **Exit codes**: 0 for success, non-zero for error

## Variables & Data

### Variable Types
- **Local variables**: script-specific
- **Environment variables**: $HOME, $PATH
- **Special variables**: $0, $1, $#, $@, $?
- **Arrays**: indexed and associative
- **Read-only**: readonly variable

### String Operations
- **Concatenation**: var="$str1$str2"
- **Length**: ${#string}
- **Substring**: ${string:start:length}
- **Pattern matching**: ${string/pattern/replacement}
- **Case conversion**: ${string^^}, ${string,,}

## Control Structures

### Conditionals
- **if/then/else**: Basic conditions
- **elif**: Multiple conditions
- **case/esac**: Pattern matching
- **Test operators**: -eq, -ne, -lt, -gt
- **File tests**: -f, -d, -r, -w, -x

### Loops
- **for**: Iterate over lists
- **while**: Condition-based loops
- **until**: Inverse while loop
- **break/continue**: Loop control
- **Nested loops**: Loops within loops

## Functions

### Function Definition
- **Syntax**: function_name() { commands; }
- **Parameters**: $1, $2, ..., $n
- **Local variables**: local var=value
- **Return values**: return code
- **Function calls**: function_name args

### Advanced Functions
- **Recursive functions**: Self-calling
- **Function libraries**: Source external files
- **Error handling**: Trap signals
- **Debugging**: set -x for tracing
- **Best practices**: Modular design

## Input/Output

### Standard Streams
- **stdin**: Standard input (0)
- **stdout**: Standard output (1)
- **stderr**: Standard error (2)
- **Redirection**: >, >>, <, 2>
- **Pipes**: | for command chaining

### File Operations
- **Reading files**: while read line
- **Writing files**: echo > file
- **File processing**: awk, sed, grep
- **Temporary files**: mktemp
- **File permissions**: chmod, chown

## Text Processing

### Command-line Tools
- **grep**: Pattern searching
- **sed**: Stream editing
- **awk**: Text processing language
- **cut**: Column extraction
- **sort**: Sorting lines
- **uniq**: Remove duplicates

### Regular Expressions
- **Basic regex**: grep patterns
- **Extended regex**: egrep/grep -E
- **Character classes**: [a-z], [0-9]
- **Quantifiers**: *, +, ?, {n,m}
- **Anchors**: ^, $

## System Administration

### Process Management
- **Background jobs**: command &
- **Job control**: jobs, fg, bg
- **Process monitoring**: ps, top, htop
- **Signal handling**: kill, trap
- **Cron jobs**: Scheduled execution

### System Information
- **System stats**: df, du, free
- **Network**: netstat, ss, ping
- **Users**: who, w, id
- **Environment**: env, printenv
- **Hardware**: lscpu, lsmem

## Best Practices
- **Error handling**: Check exit codes
- **Quoting**: Proper variable quoting
- **Portability**: POSIX compliance
- **Security**: Input validation
- **Documentation**: Clear comments and usage
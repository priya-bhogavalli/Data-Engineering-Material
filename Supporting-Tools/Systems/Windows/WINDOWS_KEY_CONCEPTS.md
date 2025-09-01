# Windows - Key Concepts

## Overview
Windows is Microsoft's operating system family providing graphical user interface, multitasking, and comprehensive system management for desktop and server environments.

## System Architecture

### Core Components
- **Kernel**: Windows NT kernel
- **HAL**: Hardware Abstraction Layer
- **Executive**: System services layer
- **Subsystems**: Win32, POSIX support
- **Registry**: Configuration database

### Process Management
- **Processes**: Executable programs
- **Threads**: Execution units
- **Services**: Background processes
- **Task Manager**: Process monitoring
- **Resource Monitor**: Detailed system stats

## File System

### NTFS Features
- **Security**: Access control lists (ACLs)
- **Compression**: File/folder compression
- **Encryption**: EFS (Encrypting File System)
- **Journaling**: Transaction logging
- **Quotas**: Disk space management

### File Operations
- **Paths**: Drive letters (C:, D:)
- **UNC paths**: \\server\share
- **Permissions**: Read, write, execute, full control
- **Attributes**: Hidden, system, read-only
- **Symbolic links**: mklink command

## Command Line

### Command Prompt (cmd)
- **Basic commands**: dir, copy, move, del
- **Navigation**: cd, pushd, popd
- **Environment**: set, echo
- **Batch files**: .bat/.cmd scripts
- **Redirection**: >, >>, <, |

### PowerShell
- **Cmdlets**: Verb-Noun syntax
- **Objects**: .NET object pipeline
- **Variables**: $variable syntax
- **Scripts**: .ps1 files
- **Modules**: Reusable code libraries

### Windows Subsystem for Linux (WSL)
- **Linux compatibility**: Run Linux binaries
- **File system**: Access Windows files
- **Networking**: Shared network stack
- **Integration**: Windows-Linux interop
- **Development**: Linux development tools

## System Administration

### User Management
- **Local accounts**: Computer-specific users
- **Domain accounts**: Active Directory users
- **Groups**: User collections
- **UAC**: User Account Control
- **Privileges**: Administrative rights

### Services Management
- **Services console**: services.msc
- **Service states**: Running, stopped, paused
- **Startup types**: Automatic, manual, disabled
- **Dependencies**: Service relationships
- **Recovery**: Failure handling

### Registry
- **Hives**: HKEY_* root keys
- **Keys and values**: Hierarchical structure
- **Data types**: REG_SZ, REG_DWORD, REG_BINARY
- **Registry Editor**: regedit.exe
- **Backup/restore**: Registry maintenance

## Networking

### Network Configuration
- **TCP/IP**: IP addressing, DNS
- **Network adapters**: Ethernet, Wi-Fi
- **Network profiles**: Public, private, domain
- **Firewall**: Windows Defender Firewall
- **Network discovery**: File/printer sharing

### Remote Access
- **Remote Desktop**: RDP protocol
- **WinRM**: Windows Remote Management
- **SSH**: OpenSSH client/server
- **VPN**: Virtual private networks
- **Network shares**: SMB/CIFS protocol

## Security

### Windows Security
- **Windows Defender**: Built-in antivirus
- **BitLocker**: Drive encryption
- **Windows Hello**: Biometric authentication
- **Credential Manager**: Password storage
- **Security policies**: Group Policy settings

### Event Logging
- **Event Viewer**: System log analysis
- **Event logs**: System, application, security
- **Event IDs**: Specific event identification
- **Log forwarding**: Centralized logging
- **Auditing**: Security event tracking

## Performance & Monitoring

### System Monitoring
- **Performance Monitor**: perfmon.exe
- **Resource Monitor**: resmon.exe
- **Task Manager**: Real-time monitoring
- **Event Tracing**: ETW (Event Tracing for Windows)
- **WMI**: Windows Management Instrumentation

### Troubleshooting
- **System File Checker**: sfc /scannow
- **Memory Diagnostic**: mdsched.exe
- **Disk Check**: chkdsk command
- **Safe Mode**: Diagnostic startup
- **System Restore**: Rollback changes

## Development Environment
- **Visual Studio**: IDE for development
- **Windows SDK**: Development tools
- **Package managers**: Chocolatey, winget
- **Containers**: Docker Desktop, Windows containers
- **Virtualization**: Hyper-V, VirtualBox
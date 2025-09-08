# File Systems - Interview Questions

## 1. What are different types of file systems?

**Answer:**
File systems organize and manage data storage with different characteristics for various use cases.

**Local File Systems:**
- **NTFS**: Windows file system with security features
- **ext4**: Linux file system with journaling
- **APFS**: Apple file system with encryption
- **ZFS**: Advanced file system with data integrity

**Distributed File Systems:**
- **HDFS**: Hadoop Distributed File System for big data
- **GFS**: Google File System for distributed applications
- **Amazon EFS**: Elastic File System for AWS
- **Azure Files**: Managed file shares in Azure

**Object Storage:**
- **Amazon S3**: Scalable object storage
- **Azure Blob**: Binary large object storage
- **Google Cloud Storage**: Multi-class object storage
- **MinIO**: Open-source object storage

**Network File Systems:**
- **NFS**: Network File System for Unix/Linux
- **SMB/CIFS**: Server Message Block for Windows
- **FTP/SFTP**: File Transfer Protocol

**Comparison:**
```
Type          | Scalability | Performance | Use Case
--------------|-------------|-------------|----------
Local FS      | Limited     | High        | OS, Apps
Distributed   | High        | Medium      | Big Data
Object Store  | Very High   | Medium      | Cloud, Backup
Network FS    | Medium      | Variable    | File Sharing
```

## 2. How do you choose the right file system for data engineering?

**Answer:**
Consider data volume, access patterns, and infrastructure requirements.

**For Big Data:**
- HDFS for Hadoop ecosystem
- S3 for cloud-native applications
- Azure Data Lake for Microsoft stack

**For Real-time Processing:**
- Local SSD for low latency
- In-memory file systems for speed

**For Backup/Archive:**
- Object storage for cost efficiency
- Tape systems for long-term retention
# Windows Interview Questions for Data Engineering

## Windows Fundamentals

### Q1: How do you manage data processing tasks on Windows?
**Answer:**
```powershell
# PowerShell for data processing
# Process CSV files
Import-Csv "sales_data.csv" | 
    Where-Object {$_.Revenue -gt 1000} |
    Group-Object Category |
    Select-Object Name, Count, @{Name="TotalRevenue"; Expression={($_.Group | Measure-Object Revenue -Sum).Sum}}

# Batch file processing
Get-ChildItem "C:\Data\*.csv" | ForEach-Object {
    $data = Import-Csv $_.FullName
    $processed = $data | Where-Object {$_.Status -eq "Active"}
    $processed | Export-Csv "C:\Processed\$($_.BaseName)_processed.csv" -NoTypeInformation
}

# Task Scheduler for automation
schtasks /create /tn "DataProcessing" /tr "powershell.exe -File C:\Scripts\process_data.ps1" /sc daily /st 02:00
```

### Q2: How do you monitor system performance for data workloads?
**Answer:**
```powershell
# Performance monitoring
Get-Counter "\Processor(_Total)\% Processor Time", "\Memory\Available MBytes", "\LogicalDisk(_Total)\% Disk Time"

# Process monitoring
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, CPU, WorkingSet

# Memory usage by process
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10 Name, @{Name="Memory(MB)"; Expression={[math]::Round($_.WorkingSet/1MB,2)}}

# Disk space monitoring
Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, @{Name="Size(GB)"; Expression={[math]::Round($_.Size/1GB,2)}}, @{Name="FreeSpace(GB)"; Expression={[math]::Round($_.FreeSpace/1GB,2)}}
```

## PowerShell for Data Engineering

### Q3: How do you process large datasets with PowerShell?
**Answer:**
```powershell
# Stream processing for large files
function Process-LargeCSV {
    param([string]$FilePath, [string]$OutputPath)
    
    $reader = [System.IO.StreamReader]::new($FilePath)
    $writer = [System.IO.StreamWriter]::new($OutputPath)
    
    # Write header
    $header = $reader.ReadLine()
    $writer.WriteLine($header)
    
    # Process line by line
    while (($line = $reader.ReadLine()) -ne $null) {
        $fields = $line -split ','
        
        # Apply transformations
        if ([double]$fields[2] -gt 1000) {
            $fields[3] = [double]$fields[3] * 1.1  # Apply discount
            $writer.WriteLine($fields -join ',')
        }
    }
    
    $reader.Close()
    $writer.Close()
}

# Parallel processing
$files = Get-ChildItem "C:\Data\*.csv"
$files | ForEach-Object -Parallel {
    $data = Import-Csv $_.FullName
    $processed = $data | Where-Object {$_.Status -eq "Active"}
    $outputPath = "C:\Processed\$($_.BaseName)_processed.csv"
    $processed | Export-Csv $outputPath -NoTypeInformation
} -ThrottleLimit 4
```

### Q4: How do you interact with databases from PowerShell?
**Answer:**
```powershell
# SQL Server connection
$connectionString = "Server=localhost;Database=Analytics;Integrated Security=true;"
$connection = New-Object System.Data.SqlClient.SqlConnection($connectionString)

function Invoke-SqlQuery {
    param([string]$Query, [System.Data.SqlClient.SqlConnection]$Connection)
    
    $command = New-Object System.Data.SqlClient.SqlCommand($Query, $Connection)
    $adapter = New-Object System.Data.SqlClient.SqlDataAdapter($command)
    $dataset = New-Object System.Data.DataSet
    
    $adapter.Fill($dataset) | Out-Null
    return $dataset.Tables[0]
}

# Execute queries
$connection.Open()
$results = Invoke-SqlQuery -Query "SELECT * FROM sales WHERE date >= '2023-01-01'" -Connection $connection
$connection.Close()

# Bulk insert from CSV
$bulkCopy = New-Object System.Data.SqlClient.SqlBulkCopy($connectionString)
$bulkCopy.DestinationTableName = "staging_table"

$dataTable = Import-Csv "data.csv" | ConvertTo-DataTable
$bulkCopy.WriteToServer($dataTable)
$bulkCopy.Close()
```

## Windows Services & Automation

### Q5: How do you create Windows services for data processing?
**Answer:**
```powershell
# Create a Windows service using PowerShell
$serviceName = "DataProcessingService"
$serviceDisplayName = "Data Processing Service"
$servicePath = "C:\Services\DataProcessor.exe"

# Install service
New-Service -Name $serviceName -DisplayName $serviceDisplayName -BinaryPathName $servicePath -StartupType Automatic

# Service management
Start-Service -Name $serviceName
Stop-Service -Name $serviceName
Restart-Service -Name $serviceName

# Monitor service status
Get-Service -Name $serviceName | Select-Object Name, Status, StartType

# Service configuration
Set-Service -Name $serviceName -StartupType Manual
Set-Service -Name $serviceName -Description "Processes data files automatically"
```

### Q6: How do you implement file system monitoring?
**Answer:**
```powershell
# File system watcher
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "C:\Data\Input"
$watcher.Filter = "*.csv"
$watcher.EnableRaisingEvents = $true

# Event handler
$action = {
    $path = $Event.SourceEventArgs.FullPath
    $changeType = $Event.SourceEventArgs.ChangeType
    $name = $Event.SourceEventArgs.Name
    
    Write-Host "File $name was $changeType at $path"
    
    # Process the file
    if ($changeType -eq "Created") {
        Start-Sleep -Seconds 2  # Wait for file to be fully written
        Process-DataFile -FilePath $path
    }
}

# Register events
Register-ObjectEvent -InputObject $watcher -EventName "Created" -Action $action
Register-ObjectEvent -InputObject $watcher -EventName "Changed" -Action $action

# Keep script running
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    $watcher.Dispose()
}
```

## Windows Administration

### Q7: How do you manage Windows event logs for monitoring?
**Answer:**
```powershell
# Read event logs
Get-EventLog -LogName Application -Newest 100 | Where-Object {$_.EntryType -eq "Error"}

# Filter by source
Get-EventLog -LogName Application -Source "DataProcessor" -Newest 50

# Write to event log
New-EventLog -LogName Application -Source "DataProcessingApp"
Write-EventLog -LogName Application -Source "DataProcessingApp" -EventId 1001 -EntryType Information -Message "Data processing completed successfully"

# Export logs
Get-EventLog -LogName Application -After (Get-Date).AddDays(-7) | Export-Csv "application_logs.csv" -NoTypeInformation

# Monitor logs in real-time
Get-WinEvent -FilterHashtable @{LogName='Application'; Level=2} -MaxEvents 10
```

### Q8: How do you manage Windows permissions for data directories?
**Answer:**
```powershell
# Set folder permissions
$path = "C:\Data"
$user = "DOMAIN\DataProcessingService"

# Get current ACL
$acl = Get-Acl $path

# Create new access rule
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($user, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")

# Add rule to ACL
$acl.SetAccessRule($accessRule)

# Apply ACL
Set-Acl -Path $path -AclObject $acl

# Verify permissions
Get-Acl $path | Select-Object -ExpandProperty Access

# Remove permissions
$acl.RemoveAccessRule($accessRule)
Set-Acl -Path $path -AclObject $acl
```

## Registry & Configuration

### Q9: How do you manage application configuration in Windows Registry?
**Answer:**
```powershell
# Create registry keys for application config
$regPath = "HKLM:\SOFTWARE\DataProcessingApp"

# Create key if it doesn't exist
if (!(Test-Path $regPath)) {
    New-Item -Path $regPath -Force
}

# Set configuration values
Set-ItemProperty -Path $regPath -Name "DataSourcePath" -Value "C:\Data\Input"
Set-ItemProperty -Path $regPath -Name "ProcessingInterval" -Value 300
Set-ItemProperty -Path $regPath -Name "MaxRetries" -Value 3

# Read configuration
$config = @{}
$config.DataSourcePath = Get-ItemProperty -Path $regPath -Name "DataSourcePath" | Select-Object -ExpandProperty DataSourcePath
$config.ProcessingInterval = Get-ItemProperty -Path $regPath -Name "ProcessingInterval" | Select-Object -ExpandProperty ProcessingInterval

# Remove configuration
Remove-ItemProperty -Path $regPath -Name "OldSetting"
```

### Q10: How do you implement Windows-based ETL processes?
**Answer:**
```powershell
# ETL Pipeline script
function Start-ETLPipeline {
    param(
        [string]$SourcePath,
        [string]$DestinationPath,
        [string]$LogPath
    )
    
    try {
        # Extract
        Write-Host "Starting extraction..."
        $data = @()
        Get-ChildItem $SourcePath -Filter "*.csv" | ForEach-Object {
            $fileData = Import-Csv $_.FullName
            $data += $fileData
        }
        
        # Transform
        Write-Host "Starting transformation..."
        $transformedData = $data | ForEach-Object {
            [PSCustomObject]@{
                ID = $_.ID
                Name = $_.Name.ToUpper()
                Revenue = [double]$_.Revenue * 1.1
                ProcessedDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            }
        }
        
        # Load
        Write-Host "Starting load..."
        $transformedData | Export-Csv "$DestinationPath\processed_data_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv" -NoTypeInformation
        
        # Log success
        Add-Content -Path $LogPath -Value "$(Get-Date): ETL pipeline completed successfully. Processed $($transformedData.Count) records."
        
        return $true
    }
    catch {
        # Log error
        Add-Content -Path $LogPath -Value "$(Get-Date): ETL pipeline failed. Error: $($_.Exception.Message)"
        return $false
    }
}

# Schedule ETL pipeline
$trigger = New-ScheduledTaskTrigger -Daily -At "02:00AM"
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\Scripts\ETL_Pipeline.ps1"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "DailyETL" -Trigger $trigger -Action $action -Settings $settings -Description "Daily ETL processing"
```

## Key Takeaways

**Windows Skills for Data Engineering:**
- PowerShell for data processing and automation
- Windows services for background processing
- Event log monitoring and management
- File system monitoring and permissions
- Registry configuration management
- Task scheduling and automation
- Performance monitoring and optimization
- Integration with SQL Server and other databases
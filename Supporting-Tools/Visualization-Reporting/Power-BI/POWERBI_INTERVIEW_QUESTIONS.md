# Power BI Interview Questions for Data Engineers

## Basic Level Questions

### 1. What is Power BI and its key components for data engineering?
**Answer**: Power BI is Microsoft's business intelligence platform that enables data visualization and analytics. Key components for data engineers:
- **Power BI Desktop**: Development environment for reports and data models
- **Power BI Service**: Cloud-based platform for sharing and collaboration
- **Power BI Gateway**: Connects cloud service to on-premises data
- **Power Query**: Data transformation and preparation tool
- **DAX**: Data Analysis Expressions for calculations and measures

```
Power BI Architecture:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│  Power Query    │───▶│   Data Model    │
│ (SQL, Files,    │    │ (Transform)     │    │ (Tables, Rels)  │
│  APIs, Cloud)   │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Power BI Service│◀───│    Reports      │◀───│      DAX        │
│ (Dashboards,    │    │ (Visualizations)│    │ (Measures,      │
│  Sharing)       │    │                 │    │  Calculations)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2. Explain Power Query and its role in data transformation
**Answer**: Power Query is the data transformation engine in Power BI that enables ETL operations:
- **Data Connectivity**: Connect to various data sources
- **Data Transformation**: Clean, reshape, and combine data
- **M Language**: Functional language for advanced transformations
- **Query Folding**: Push transformations back to source systems

```m
// Power Query M code example
let
    // Connect to SQL Server
    Source = Sql.Database("server", "database"),
    
    // Get sales table
    SalesTable = Source{[Schema="dbo",Item="Sales"]}[Data],
    
    // Filter recent data
    FilteredRows = Table.SelectRows(SalesTable, 
        each [OrderDate] >= Date.AddDays(DateTime.Date(DateTime.LocalNow()), -365)),
    
    // Add calculated columns
    AddedCustom = Table.AddColumn(FilteredRows, "Revenue", 
        each [Quantity] * [UnitPrice], type number),
    
    // Group by customer
    GroupedRows = Table.Group(AddedCustom, {"CustomerID"}, 
        {{"TotalRevenue", each List.Sum([Revenue]), type number},
         {"OrderCount", each Table.RowCount(_), type number}}),
    
    // Sort by revenue
    SortedRows = Table.Sort(GroupedRows, {{"TotalRevenue", Order.Descending}})
in
    SortedRows
```

### 3. What are the different data connection modes in Power BI?
**Answer**: Power BI supports different data connection modes:
- **Import**: Data is loaded into Power BI model (fastest queries, limited by memory)
- **DirectQuery**: Queries sent directly to source (real-time data, slower performance)
- **Live Connection**: Direct connection to Analysis Services or Power BI datasets
- **Composite Models**: Mix of Import and DirectQuery in same model

```
Import Mode:
Data Source → Power BI Model (In-Memory) → Visualizations
- Fast query performance
- Data refresh required
- Memory limitations

DirectQuery Mode:
Visualizations → Power BI → Data Source (Real-time queries)
- Real-time data access
- Slower performance
- No memory limitations

Composite Model:
Import Tables + DirectQuery Tables → Combined Model
- Best of both modes
- Complex relationships possible
```

### 4. How do you create relationships between tables in Power BI?
**Answer**: Relationships connect tables in the data model:
- **One-to-Many**: Most common relationship type
- **Many-to-Many**: Supported with bidirectional filtering
- **One-to-One**: Less common, used for table splitting
- **Cross Filter Direction**: Single or bidirectional

```
// Example data model relationships
Customers (CustomerID) ──1:M── Orders (CustomerID)
    │                              │
    │                              │
    └──1:M── CustomerCategories    └──1:M── OrderDetails
                                              │
Products (ProductID) ──1:M─────────────────────┘
    │
    └──M:1── Categories (CategoryID)

// DAX to handle relationships
TotalSales = 
CALCULATE(
    SUM(Orders[Amount]),
    RELATED(Customers[CustomerType]) = "Premium"
)
```

### 5. What is DAX and its basic functions?
**Answer**: DAX (Data Analysis Expressions) is a formula language for calculations in Power BI:
- **Calculated Columns**: Computed at row level during data refresh
- **Measures**: Computed at query time based on filter context
- **Calculated Tables**: Create new tables using DAX expressions

```dax
// Basic DAX measures
Total Sales = SUM(Sales[Amount])

Average Order Value = 
DIVIDE(
    SUM(Sales[Amount]),
    COUNTROWS(Sales)
)

// Time intelligence
Sales YTD = TOTALYTD(SUM(Sales[Amount]), Calendar[Date])

Sales Previous Year = 
CALCULATE(
    SUM(Sales[Amount]),
    SAMEPERIODLASTYEAR(Calendar[Date])
)

// Calculated column
Profit Margin = 
DIVIDE(
    Sales[Revenue] - Sales[Cost],
    Sales[Revenue]
)

// Calculated table
Top Customers = 
TOPN(
    10,
    SUMMARIZE(
        Sales,
        Customer[CustomerName],
        "Total Sales", SUM(Sales[Amount])
    ),
    [Total Sales],
    DESC
)
```

## Intermediate Level Questions

### 6. How do you implement incremental data refresh in Power BI?
**Answer**: Incremental refresh optimizes data loading for large datasets:
- **Range Parameters**: Define date ranges for incremental loading
- **Partition Strategy**: Automatically partition data by date
- **Refresh Policies**: Configure historical and incremental periods

```m
// Power Query parameters for incremental refresh
// RangeStart parameter (DateTime)
#datetime(2020, 1, 1, 0, 0, 0)

// RangeEnd parameter (DateTime)  
#datetime(2024, 12, 31, 23, 59, 59)

// Filter table using parameters
let
    Source = Sql.Database("server", "database"),
    SalesTable = Source{[Schema="dbo",Item="Sales"]}[Data],
    
    // Apply incremental filter
    FilteredRows = Table.SelectRows(SalesTable, 
        each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd)
in
    FilteredRows
```

```json
// Incremental refresh policy (configured in Power BI Desktop)
{
    "incrementalRefresh": {
        "policiesToApply": [
            {
                "name": "SalesTable",
                "sourceExpression": "Sales",
                "refreshPolicy": {
                    "incrementalWindowStart": "-2 years",
                    "incrementalWindowEnd": "0 days",
                    "incrementalGranularity": "Day",
                    "archiveWindowStart": "-5 years",
                    "archiveWindowEnd": "-2 years"
                }
            }
        ]
    }
}
```

### 7. How do you optimize Power BI data models for performance?
**Answer**: Data model optimization strategies:
- **Star Schema Design**: Fact tables connected to dimension tables
- **Column Optimization**: Remove unnecessary columns, optimize data types
- **Relationships**: Minimize bidirectional relationships
- **Aggregations**: Pre-calculate common aggregations

```dax
// Optimize data types and remove unnecessary columns
// In Power Query
let
    Source = Sql.Database("server", "database"),
    SalesTable = Source{[Schema="dbo",Item="Sales"]}[Data],
    
    // Remove unnecessary columns
    RemovedColumns = Table.RemoveColumns(SalesTable, 
        {"InternalNotes", "CreatedBy", "ModifiedBy"}),
    
    // Optimize data types
    ChangedTypes = Table.TransformColumnTypes(RemovedColumns, {
        {"OrderDate", type date},
        {"CustomerID", Int64.Type},
        {"Amount", Currency.Type},
        {"Quantity", Int32.Type}
    })
in
    ChangedTypes

// Create aggregation tables
Monthly Sales Summary = 
SUMMARIZECOLUMNS(
    Calendar[Year],
    Calendar[Month],
    Customer[Region],
    Product[Category],
    "Total Sales", SUM(Sales[Amount]),
    "Total Quantity", SUM(Sales[Quantity]),
    "Order Count", COUNTROWS(Sales)
)

// Use variables in DAX for better performance
Sales Performance = 
VAR CurrentSales = SUM(Sales[Amount])
VAR PreviousYearSales = 
    CALCULATE(
        SUM(Sales[Amount]),
        SAMEPERIODLASTYEAR(Calendar[Date])
    )
VAR GrowthRate = 
    DIVIDE(
        CurrentSales - PreviousYearSales,
        PreviousYearSales
    )
RETURN
    GrowthRate
```

### 8. How do you implement row-level security (RLS) in Power BI?
**Answer**: RLS restricts data access based on user identity:
- **Static RLS**: Fixed roles with predefined filters
- **Dynamic RLS**: User-based filtering using functions
- **Role Management**: Define roles and assign users

```dax
// Static RLS - Sales role can only see specific regions
// Create role: "Sales_West"
[Region] = "West"

// Create role: "Sales_East"  
[Region] = "East"

// Dynamic RLS - Users see data based on their profile
// User table with email and allowed regions
Users Table:
Email               | Region
john@company.com    | West
jane@company.com    | East
admin@company.com   | All

// Dynamic RLS filter
[Region] = 
IF(
    USERPRINCIPALNAME() = "admin@company.com",
    [Region], // Admin sees all regions
    LOOKUPVALUE(
        Users[Region],
        Users[Email],
        USERPRINCIPALNAME()
    )
)

// Multi-level security
// Manager role - see their team's data
[SalesPersonID] IN 
VALUES(
    FILTER(
        TeamHierarchy,
        TeamHierarchy[ManagerEmail] = USERPRINCIPALNAME()
    )[SalesPersonID]
)

// Department-based security
[Department] IN 
VALUES(
    FILTER(
        UserDepartments,
        UserDepartments[UserEmail] = USERPRINCIPALNAME()
    )[Department]
)
```

### 9. How do you handle complex data transformations in Power Query?
**Answer**: Advanced Power Query transformations:

```m
// Complex data transformation example
let
    // Connect to multiple sources
    SalesSource = Sql.Database("server", "salesdb"),
    CRMSource = Web.Contents("https://api.crm.com/customers"),
    
    // Get sales data
    Sales = SalesSource{[Schema="dbo",Item="Sales"]}[Data],
    
    // Parse JSON from CRM API
    CRMJson = Json.Document(CRMSource),
    CRMTable = Table.FromRecords(CRMJson[customers]),
    
    // Merge sales with CRM data
    MergedData = Table.NestedJoin(
        Sales, {"CustomerID"},
        CRMTable, {"id"},
        "CRMData", JoinKind.LeftOuter
    ),
    
    // Expand CRM columns
    ExpandedCRM = Table.ExpandRecordColumn(
        MergedData, "CRMData",
        {"name", "segment", "lifetime_value"},
        {"CustomerName", "Segment", "LifetimeValue"}
    ),
    
    // Custom function for data cleansing
    CleanPhoneNumber = (phone as text) as text =>
        let
            // Remove non-numeric characters
            NumericOnly = Text.Select(phone, {"0".."9"}),
            // Format as (XXX) XXX-XXXX
            Formatted = if Text.Length(NumericOnly) = 10 then
                "(" & Text.Range(NumericOnly, 0, 3) & ") " &
                Text.Range(NumericOnly, 3, 3) & "-" &
                Text.Range(NumericOnly, 6, 4)
            else
                NumericOnly
        in
            Formatted,
    
    // Apply custom function
    CleanedPhone = Table.TransformColumns(
        ExpandedCRM,
        {{"Phone", CleanPhoneNumber}}
    ),
    
    // Conditional column based on multiple criteria
    AddedTier = Table.AddColumn(
        CleanedPhone,
        "CustomerTier",
        each if [LifetimeValue] >= 10000 and [Segment] = "Enterprise" then "Platinum"
             else if [LifetimeValue] >= 5000 then "Gold"
             else if [LifetimeValue] >= 1000 then "Silver"
             else "Bronze"
    ),
    
    // Group and aggregate
    CustomerSummary = Table.Group(
        AddedTier,
        {"CustomerID", "CustomerName", "CustomerTier"},
        {
            {"TotalOrders", each Table.RowCount(_), Int64.Type},
            {"TotalRevenue", each List.Sum([Amount]), type number},
            {"AvgOrderValue", each List.Average([Amount]), type number},
            {"FirstOrderDate", each List.Min([OrderDate]), type date},
            {"LastOrderDate", each List.Max([OrderDate]), type date}
        }
    )
in
    CustomerSummary
```

### 10. How do you implement advanced DAX patterns for complex calculations?
**Answer**: Advanced DAX patterns and techniques:

```dax
// Time intelligence with custom calendar
Sales Same Period Last Year = 
VAR CurrentPeriodStart = MIN(Calendar[Date])
VAR CurrentPeriodEnd = MAX(Calendar[Date])
VAR DaysInCurrentPeriod = CurrentPeriodEnd - CurrentPeriodStart + 1
VAR LastYearStart = DATE(YEAR(CurrentPeriodStart) - 1, MONTH(CurrentPeriodStart), DAY(CurrentPeriodStart))
VAR LastYearEnd = LastYearStart + DaysInCurrentPeriod - 1
RETURN
CALCULATE(
    SUM(Sales[Amount]),
    Calendar[Date] >= LastYearStart && Calendar[Date] <= LastYearEnd
)

// Running totals with reset
Running Total by Category = 
VAR CurrentCategory = Sales[Category]
VAR CurrentDate = Sales[Date]
RETURN
CALCULATE(
    SUM(Sales[Amount]),
    FILTER(
        ALL(Sales),
        Sales[Category] = CurrentCategory &&
        Sales[Date] <= CurrentDate
    )
)

// Cohort analysis
Customer Retention Rate = 
VAR FirstPurchaseMonth = 
    CALCULATE(
        MIN(Sales[Date]),
        ALLEXCEPT(Sales, Sales[CustomerID])
    )
VAR CurrentMonth = MAX(Calendar[Date])
VAR MonthsFromFirst = DATEDIFF(FirstPurchaseMonth, CurrentMonth, MONTH)
VAR CustomersInCohort = 
    CALCULATE(
        DISTINCTCOUNT(Sales[CustomerID]),
        Calendar[Date] = FirstPurchaseMonth
    )
VAR ActiveCustomers = 
    CALCULATE(
        DISTINCTCOUNT(Sales[CustomerID]),
        Calendar[Date] = CurrentMonth
    )
RETURN
DIVIDE(ActiveCustomers, CustomersInCohort)

// ABC Analysis (Pareto)
Customer ABC Classification = 
VAR CustomerRevenue = SUM(Sales[Amount])
VAR TotalRevenue = CALCULATE(SUM(Sales[Amount]), ALL(Customer))
VAR CustomerRank = RANKX(ALL(Customer), SUM(Sales[Amount]), , DESC)
VAR TotalCustomers = COUNTROWS(ALL(Customer))
VAR CumulativeRevenue = 
    SUMX(
        FILTER(
            ALL(Customer),
            RANKX(ALL(Customer), SUM(Sales[Amount]), , DESC) <= CustomerRank
        ),
        SUM(Sales[Amount])
    )
VAR CumulativePercentage = DIVIDE(CumulativeRevenue, TotalRevenue)
RETURN
SWITCH(
    TRUE(),
    CumulativePercentage <= 0.8, "A",
    CumulativePercentage <= 0.95, "B",
    "C"
)

// Dynamic segmentation
Dynamic Customer Segment = 
VAR SelectedMetric = SELECTEDVALUE(Parameters[Metric])
VAR CustomerValue = 
    SWITCH(
        SelectedMetric,
        "Revenue", SUM(Sales[Amount]),
        "Frequency", DISTINCTCOUNT(Sales[OrderID]),
        "Recency", DATEDIFF(MAX(Sales[Date]), TODAY(), DAY),
        BLANK()
    )
VAR Percentile80 = PERCENTILE.INC(ALL(Customer[CustomerID]), CustomerValue, 0.8)
VAR Percentile50 = PERCENTILE.INC(ALL(Customer[CustomerID]), CustomerValue, 0.5)
RETURN
SWITCH(
    TRUE(),
    CustomerValue >= Percentile80, "High",
    CustomerValue >= Percentile50, "Medium",
    "Low"
)
```

## Advanced Level Questions

### 11. How do you implement Power BI embedded analytics for applications?
**Answer**: Power BI Embedded integration strategies:

```javascript
// Power BI Embedded JavaScript SDK
// Authentication and token generation
const getAccessToken = async () => {
    const response = await fetch('/api/powerbi/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            reportId: 'your-report-id',
            datasetId: 'your-dataset-id'
        })
    });
    return await response.json();
};

// Embed Power BI report
const embedReport = async () => {
    const tokenData = await getAccessToken();
    
    const config = {
        type: 'report',
        id: 'your-report-id',
        embedUrl: 'https://app.powerbi.com/reportEmbed',
        accessToken: tokenData.accessToken,
        tokenType: models.TokenType.Embed,
        settings: {
            filterPaneEnabled: false,
            navContentPaneEnabled: false,
            background: models.BackgroundType.Transparent,
            customLayout: {
                displayOption: models.DisplayOption.FitToPage
            }
        },
        filters: [
            {
                $schema: "http://powerbi.com/product/schema#basic",
                target: {
                    table: "Sales",
                    column: "Region"
                },
                operator: "In",
                values: ["West", "East"]
            }
        ]
    };
    
    const reportContainer = document.getElementById('reportContainer');
    const report = powerbi.embed(reportContainer, config);
    
    // Handle events
    report.on('loaded', () => {
        console.log('Report loaded');
    });
    
    report.on('rendered', () => {
        console.log('Report rendered');
    });
    
    report.on('error', (event) => {
        console.error('Report error:', event.detail);
    });
};

// Dynamic filtering
const applyFilters = async (filterValues) => {
    const basicFilter = {
        $schema: "http://powerbi.com/product/schema#basic",
        target: {
            table: "Sales",
            column: "CustomerSegment"
        },
        operator: "In",
        values: filterValues
    };
    
    await report.setFilters([basicFilter]);
};

// Row-level security with embedded tokens
const generateEmbedToken = async (userId, roles) => {
    const tokenRequest = {
        datasets: [{
            id: datasetId,
            xmlaPermissions: "ReadOnly"
        }],
        reports: [{
            id: reportId,
            allowEdit: false
        }],
        identities: [{
            username: userId,
            roles: roles,
            datasets: [datasetId]
        }]
    };
    
    // Call Power BI REST API to generate embed token
    const response = await powerBIClient.embedTokens.generateToken(tokenRequest);
    return response.token;
};
```

### 12. How do you implement Power BI REST API for automation and administration?
**Answer**: Power BI REST API for programmatic operations:

```python
# Power BI REST API automation
import requests
import json
from datetime import datetime, timedelta

class PowerBIAPI:
    def __init__(self, tenant_id, client_id, client_secret):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self._get_access_token()
        self.base_url = "https://api.powerbi.com/v1.0/myorg"
        
    def _get_access_token(self):
        """Get Azure AD access token for Power BI API"""
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://analysis.windows.net/powerbi/api/.default'
        }
        
        response = requests.post(url, data=data)
        return response.json()['access_token']
    
    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def refresh_dataset(self, dataset_id):
        """Trigger dataset refresh"""
        url = f"{self.base_url}/datasets/{dataset_id}/refreshes"
        
        refresh_request = {
            "type": "full",
            "commitMode": "transactional",
            "maxParallelism": 2,
            "retryCount": 3,
            "objects": [
                {
                    "table": "Sales",
                    "partition": "Sales_Current"
                }
            ]
        }
        
        response = requests.post(url, 
                               headers=self.get_headers(), 
                               json=refresh_request)
        return response.json()
    
    def get_refresh_history(self, dataset_id, top=10):
        """Get dataset refresh history"""
        url = f"{self.base_url}/datasets/{dataset_id}/refreshes?$top={top}"
        
        response = requests.get(url, headers=self.get_headers())
        return response.json()
    
    def update_datasource_credentials(self, dataset_id, datasource_id, credentials):
        """Update datasource credentials"""
        url = f"{self.base_url}/datasets/{dataset_id}/datasources/{datasource_id}"
        
        credential_details = {
            "credentialType": "Basic",
            "credentials": json.dumps({
                "username": credentials['username'],
                "password": credentials['password']
            }),
            "encryptedConnection": "Encrypted",
            "encryptionAlgorithm": "None",
            "privacyLevel": "Private"
        }
        
        response = requests.patch(url, 
                                headers=self.get_headers(), 
                                json=credential_details)
        return response.status_code == 200
    
    def export_report(self, report_id, format_type="PDF"):
        """Export report to file"""
        url = f"{self.base_url}/reports/{report_id}/export"
        
        export_request = {
            "format": format_type,
            "powerBIReportConfiguration": {
                "settings": {
                    "includeHiddenPages": False,
                    "locale": "en-US"
                },
                "reportLevelFilters": [
                    {
                        "$schema": "http://powerbi.com/product/schema#basic",
                        "target": {
                            "table": "Sales",
                            "column": "Date"
                        },
                        "operator": "GreaterThanOrEqual",
                        "values": [(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")]
                    }
                ]
            }
        }
        
        response = requests.post(url, 
                               headers=self.get_headers(), 
                               json=export_request)
        return response.json()
    
    def create_workspace(self, workspace_name):
        """Create new workspace"""
        url = f"{self.base_url}/groups"
        
        workspace_request = {
            "name": workspace_name,
            "type": "Workspace"
        }
        
        response = requests.post(url, 
                               headers=self.get_headers(), 
                               json=workspace_request)
        return response.json()
    
    def deploy_dataflow(self, workspace_id, dataflow_definition):
        """Deploy dataflow to workspace"""
        url = f"{self.base_url}/groups/{workspace_id}/dataflows"
        
        response = requests.post(url, 
                               headers=self.get_headers(), 
                               json=dataflow_definition)
        return response.json()

# Usage example
pbi_api = PowerBIAPI(tenant_id, client_id, client_secret)

# Automated refresh with monitoring
def automated_refresh_with_monitoring(dataset_id):
    # Trigger refresh
    refresh_result = pbi_api.refresh_dataset(dataset_id)
    refresh_id = refresh_result['id']
    
    # Monitor refresh status
    while True:
        history = pbi_api.get_refresh_history(dataset_id, top=1)
        latest_refresh = history['value'][0]
        
        if latest_refresh['id'] == refresh_id:
            status = latest_refresh['status']
            if status == 'Completed':
                print("Refresh completed successfully")
                break
            elif status == 'Failed':
                print(f"Refresh failed: {latest_refresh['serviceExceptionJson']}")
                break
        
        time.sleep(30)  # Check every 30 seconds
```

### 13. How do you implement Power BI dataflows for self-service data preparation?
**Answer**: Power BI dataflows for centralized data preparation:

```json
// Dataflow definition JSON
{
    "name": "Customer Analytics Dataflow",
    "description": "Centralized customer data preparation",
    "entities": [
        {
            "name": "Customers",
            "description": "Cleaned and enriched customer data",
            "source": {
                "type": "sql",
                "connectionString": "Server=server;Database=CRM;",
                "query": "SELECT CustomerID, FirstName, LastName, Email, Phone, RegistrationDate FROM Customers WHERE IsActive = 1"
            },
            "transformations": [
                {
                    "type": "removeColumns",
                    "columns": ["InternalNotes", "CreatedBy"]
                },
                {
                    "type": "changeDataType",
                    "column": "RegistrationDate",
                    "dataType": "Date"
                },
                {
                    "type": "addColumn",
                    "name": "FullName",
                    "expression": "[FirstName] & \" \" & [LastName]"
                },
                {
                    "type": "addColumn",
                    "name": "CustomerTenure",
                    "expression": "Duration.Days(DateTime.LocalNow() - [RegistrationDate])"
                }
            ]
        },
        {
            "name": "CustomerSegments",
            "description": "Customer segmentation based on behavior",
            "source": {
                "type": "dataflow",
                "entity": "Customers"
            },
            "transformations": [
                {
                    "type": "merge",
                    "rightTable": {
                        "type": "sql",
                        "connectionString": "Server=server;Database=Sales;",
                        "query": "SELECT CustomerID, SUM(Amount) as TotalSpent, COUNT(*) as OrderCount FROM Orders GROUP BY CustomerID"
                    },
                    "joinKind": "LeftOuter",
                    "leftColumns": ["CustomerID"],
                    "rightColumns": ["CustomerID"]
                },
                {
                    "type": "addColumn",
                    "name": "Segment",
                    "expression": "if [TotalSpent] >= 10000 then \"VIP\" else if [TotalSpent] >= 1000 then \"Premium\" else \"Standard\""
                }
            ]
        }
    ],
    "refreshSchedule": {
        "frequency": "Daily",
        "time": "06:00",
        "timezone": "UTC"
    }
}
```

```m
// Advanced Power Query in Dataflows
// Custom function for data quality scoring
let
    DataQualityScore = (inputTable as table) as table =>
    let
        // Add completeness score
        AddCompletenessScore = Table.AddColumn(
            inputTable,
            "CompletenessScore",
            each 
                let
                    totalFields = Record.FieldCount(_),
                    nonNullFields = List.Count(
                        List.Select(
                            Record.FieldValues(_),
                            each _ <> null and _ <> ""
                        )
                    )
                in
                    Number.Round(nonNullFields / totalFields, 2)
        ),
        
        // Add validity score based on business rules
        AddValidityScore = Table.AddColumn(
            AddCompletenessScore,
            "ValidityScore",
            each 
                let
                    emailValid = if Text.Contains([Email], "@") then 1 else 0,
                    phoneValid = if Text.Length(Text.Select([Phone], {"0".."9"})) >= 10 then 1 else 0,
                    dateValid = if [RegistrationDate] <= DateTime.Date(DateTime.LocalNow()) then 1 else 0
                in
                    Number.Round((emailValid + phoneValid + dateValid) / 3, 2)
        ),
        
        // Overall quality score
        AddOverallScore = Table.AddColumn(
            AddValidityScore,
            "OverallQualityScore",
            each Number.Round(([CompletenessScore] + [ValidityScore]) / 2, 2)
        )
    in
        AddOverallScore,
    
    // Apply function to source data
    Source = Sql.Database("server", "database"),
    CustomersTable = Source{[Schema="dbo",Item="Customers"]}[Data],
    
    // Apply data quality scoring
    QualityScored = DataQualityScore(CustomersTable),
    
    // Filter high-quality records
    HighQualityCustomers = Table.SelectRows(
        QualityScored,
        each [OverallQualityScore] >= 0.8
    )
in
    HighQualityCustomers
```

### 14. How do you implement advanced Power BI governance and monitoring?
**Answer**: Comprehensive governance and monitoring framework:

```python
# Power BI Governance Framework
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

class PowerBIGovernance:
    def __init__(self, pbi_api):
        self.pbi_api = pbi_api
        self.governance_rules = self._load_governance_rules()
        
    def _load_governance_rules(self):
        return {
            'naming_conventions': {
                'datasets': r'^(DEV|TEST|PROD)_[A-Z][a-zA-Z0-9_]*$',
                'reports': r'^[A-Z][a-zA-Z0-9\s]*\s-\s(Dashboard|Report)$',
                'workspaces': r'^(Development|Testing|Production)\s-\s[A-Z][a-zA-Z0-9\s]*$'
            },
            'refresh_frequency': {
                'max_daily_refreshes': 8,
                'max_hourly_refreshes': 2
            },
            'data_freshness': {
                'critical_datasets': 4,  # hours
                'standard_datasets': 24  # hours
            },
            'security_rules': {
                'require_rls': ['customer_data', 'financial_data'],
                'max_workspace_admins': 3
            }
        }
    
    def audit_naming_conventions(self):
        """Audit workspace, dataset, and report naming conventions"""
        violations = []
        
        # Get all workspaces
        workspaces = self.pbi_api.get_workspaces()
        
        for workspace in workspaces['value']:
            workspace_name = workspace['name']
            workspace_id = workspace['id']
            
            # Check workspace naming
            if not re.match(self.governance_rules['naming_conventions']['workspaces'], workspace_name):
                violations.append({
                    'type': 'naming_convention',
                    'object_type': 'workspace',
                    'object_name': workspace_name,
                    'violation': 'Invalid workspace naming convention'
                })
            
            # Check datasets in workspace
            datasets = self.pbi_api.get_datasets(workspace_id)
            for dataset in datasets['value']:
                if not re.match(self.governance_rules['naming_conventions']['datasets'], dataset['name']):
                    violations.append({
                        'type': 'naming_convention',
                        'object_type': 'dataset',
                        'object_name': dataset['name'],
                        'workspace': workspace_name,
                        'violation': 'Invalid dataset naming convention'
                    })
            
            # Check reports in workspace
            reports = self.pbi_api.get_reports(workspace_id)
            for report in reports['value']:
                if not re.match(self.governance_rules['naming_conventions']['reports'], report['name']):
                    violations.append({
                        'type': 'naming_convention',
                        'object_type': 'report',
                        'object_name': report['name'],
                        'workspace': workspace_name,
                        'violation': 'Invalid report naming convention'
                    })
        
        return violations
    
    def monitor_data_freshness(self):
        """Monitor dataset freshness and identify stale data"""
        freshness_violations = []
        
        workspaces = self.pbi_api.get_workspaces()
        
        for workspace in workspaces['value']:
            datasets = self.pbi_api.get_datasets(workspace['id'])
            
            for dataset in datasets['value']:
                refresh_history = self.pbi_api.get_refresh_history(dataset['id'], top=1)
                
                if refresh_history['value']:
                    last_refresh = refresh_history['value'][0]
                    last_refresh_time = datetime.fromisoformat(last_refresh['endTime'].replace('Z', '+00:00'))
                    hours_since_refresh = (datetime.now() - last_refresh_time).total_seconds() / 3600
                    
                    # Determine freshness requirement
                    is_critical = any(keyword in dataset['name'].lower() 
                                    for keyword in self.governance_rules['security_rules']['require_rls'])
                    max_hours = (self.governance_rules['data_freshness']['critical_datasets'] 
                               if is_critical 
                               else self.governance_rules['data_freshness']['standard_datasets'])
                    
                    if hours_since_refresh > max_hours:
                        freshness_violations.append({
                            'type': 'data_freshness',
                            'dataset_name': dataset['name'],
                            'workspace': workspace['name'],
                            'hours_since_refresh': round(hours_since_refresh, 2),
                            'max_allowed_hours': max_hours,
                            'violation': f'Dataset not refreshed within {max_hours} hours'
                        })
        
        return freshness_violations
    
    def audit_security_compliance(self):
        """Audit security settings and RLS implementation"""
        security_violations = []
        
        workspaces = self.pbi_api.get_workspaces()
        
        for workspace in workspaces['value']:
            # Check workspace admin count
            workspace_users = self.pbi_api.get_workspace_users(workspace['id'])
            admin_count = len([user for user in workspace_users['value'] 
                             if user['groupUserAccessRight'] == 'Admin'])
            
            if admin_count > self.governance_rules['security_rules']['max_workspace_admins']:
                security_violations.append({
                    'type': 'security',
                    'workspace': workspace['name'],
                    'violation': f'Too many workspace admins ({admin_count})',
                    'recommendation': f'Reduce to max {self.governance_rules["security_rules"]["max_workspace_admins"]} admins'
                })
            
            # Check RLS implementation for sensitive datasets
            datasets = self.pbi_api.get_datasets(workspace['id'])
            for dataset in datasets['value']:
                requires_rls = any(keyword in dataset['name'].lower() 
                                 for keyword in self.governance_rules['security_rules']['require_rls'])
                
                if requires_rls:
                    # Check if RLS is implemented (this would require additional API calls)
                    # For demonstration, assuming we have this information
                    has_rls = self._check_rls_implementation(dataset['id'])
                    
                    if not has_rls:
                        security_violations.append({
                            'type': 'security',
                            'dataset_name': dataset['name'],
                            'workspace': workspace['name'],
                            'violation': 'RLS not implemented for sensitive dataset',
                            'recommendation': 'Implement row-level security'
                        })
        
        return security_violations
    
    def generate_governance_report(self):
        """Generate comprehensive governance report"""
        report_data = {
            'report_date': datetime.now().isoformat(),
            'naming_violations': self.audit_naming_conventions(),
            'freshness_violations': self.monitor_data_freshness(),
            'security_violations': self.audit_security_compliance()
        }
        
        # Create summary
        summary = {
            'total_violations': (len(report_data['naming_violations']) + 
                               len(report_data['freshness_violations']) + 
                               len(report_data['security_violations'])),
            'critical_violations': len([v for v in report_data['security_violations'] 
                                      if 'RLS' in v.get('violation', '')]),
            'workspaces_audited': len(set([v.get('workspace', '') for v in 
                                         report_data['naming_violations'] + 
                                         report_data['freshness_violations'] + 
                                         report_data['security_violations']]))
        }
        
        report_data['summary'] = summary
        return report_data
    
    def send_governance_alerts(self, violations, recipients):
        """Send email alerts for governance violations"""
        if not violations:
            return
        
        msg = MimeMultipart()
        msg['From'] = 'powerbi-governance@company.com'
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = f'Power BI Governance Alert - {len(violations)} Violations Found'
        
        body = self._format_violations_email(violations)
        msg.attach(MimeText(body, 'html'))
        
        # Send email (configure SMTP settings)
        server = smtplib.SMTP('smtp.company.com', 587)
        server.starttls()
        server.login('username', 'password')
        server.send_message(msg)
        server.quit()

# Usage
governance = PowerBIGovernance(pbi_api)
governance_report = governance.generate_governance_report()

# Schedule daily governance checks
if governance_report['summary']['total_violations'] > 0:
    governance.send_governance_alerts(
        governance_report['naming_violations'] + 
        governance_report['freshness_violations'] + 
        governance_report['security_violations'],
        ['admin@company.com', 'bi-team@company.com']
    )
```

### 15. How do you implement Power BI Premium and capacity optimization?
**Answer**: Premium capacity management and optimization:

```python
# Power BI Premium Capacity Management
class PowerBIPremiumManager:
    def __init__(self, pbi_api):
        self.pbi_api = pbi_api
        
    def monitor_capacity_utilization(self, capacity_id):
        """Monitor Premium capacity utilization and performance"""
        
        # Get capacity utilization metrics
        utilization_url = f"https://api.powerbi.com/v1.0/myorg/admin/capacities/{capacity_id}/utilization"
        utilization_data = self.pbi_api.get(utilization_url)
        
        metrics = {
            'cpu_utilization': [],
            'memory_utilization': [],
            'query_duration': [],
            'refresh_duration': []
        }
        
        for datapoint in utilization_data['utilizationData']:
            metrics['cpu_utilization'].append(datapoint['cpuPercentage'])
            metrics['memory_utilization'].append(datapoint['memoryPercentage'])
            
            # Analyze workload performance
            for workload in datapoint['workloads']:
                if workload['name'] == 'Datasets':
                    metrics['query_duration'].extend([op['duration'] for op in workload['operations'] if op['type'] == 'Query'])
                    metrics['refresh_duration'].extend([op['duration'] for op in workload['operations'] if op['type'] == 'Refresh'])
        
        # Calculate performance indicators
        performance_summary = {
            'avg_cpu_utilization': sum(metrics['cpu_utilization']) / len(metrics['cpu_utilization']),
            'max_cpu_utilization': max(metrics['cpu_utilization']),
            'avg_memory_utilization': sum(metrics['memory_utilization']) / len(metrics['memory_utilization']),
            'max_memory_utilization': max(metrics['memory_utilization']),
            'avg_query_duration': sum(metrics['query_duration']) / len(metrics['query_duration']) if metrics['query_duration'] else 0,
            'avg_refresh_duration': sum(metrics['refresh_duration']) / len(metrics['refresh_duration']) if metrics['refresh_duration'] else 0
        }
        
        return performance_summary
    
    def optimize_capacity_workloads(self, capacity_id):
        """Optimize workload distribution across capacity"""
        
        # Get workspaces assigned to capacity
        workspaces = self.pbi_api.get_capacity_workspaces(capacity_id)
        
        optimization_recommendations = []
        
        for workspace in workspaces:
            workspace_metrics = self.analyze_workspace_performance(workspace['id'])
            
            # Identify resource-intensive workspaces
            if workspace_metrics['avg_cpu_usage'] > 80:
                optimization_recommendations.append({
                    'workspace': workspace['name'],
                    'issue': 'High CPU usage',
                    'recommendation': 'Consider moving to dedicated capacity or optimizing queries',
                    'priority': 'High'
                })
            
            if workspace_metrics['large_datasets_count'] > 5:
                optimization_recommendations.append({
                    'workspace': workspace['name'],
                    'issue': 'Multiple large datasets',
                    'recommendation': 'Implement incremental refresh or data archiving',
                    'priority': 'Medium'
                })
            
            if workspace_metrics['concurrent_users'] > 100:
                optimization_recommendations.append({
                    'workspace': workspace['name'],
                    'issue': 'High concurrent user load',
                    'recommendation': 'Consider implementing aggregations or caching',
                    'priority': 'High'
                })
        
        return optimization_recommendations
    
    def implement_autoscale_policies(self, capacity_id):
        """Implement autoscaling policies for Premium capacity"""
        
        autoscale_config = {
            'capacity_id': capacity_id,
            'policies': [
                {
                    'name': 'CPU_Based_Scaling',
                    'trigger': {
                        'metric': 'cpu_utilization',
                        'threshold': 85,
                        'duration_minutes': 10
                    },
                    'action': {
                        'type': 'scale_up',
                        'target_sku': 'P2'  # Scale from P1 to P2
                    }
                },
                {
                    'name': 'Memory_Based_Scaling',
                    'trigger': {
                        'metric': 'memory_utilization',
                        'threshold': 90,
                        'duration_minutes': 5
                    },
                    'action': {
                        'type': 'scale_up',
                        'target_sku': 'P3'  # Scale to P3 for memory-intensive workloads
                    }
                },
                {
                    'name': 'Scale_Down_Policy',
                    'trigger': {
                        'metric': 'cpu_utilization',
                        'threshold': 30,
                        'duration_minutes': 60
                    },
                    'action': {
                        'type': 'scale_down',
                        'target_sku': 'P1'  # Scale down during low usage
                    }
                }
            ]
        }
        
        # Implement autoscale logic (pseudo-code)
        return self._configure_autoscale(autoscale_config)
    
    def optimize_dataset_performance(self, dataset_id):
        """Optimize individual dataset performance"""
        
        # Analyze dataset structure and usage
        dataset_info = self.pbi_api.get_dataset(dataset_id)
        dataset_usage = self.pbi_api.get_dataset_usage(dataset_id)
        
        optimizations = []
        
        # Check for large tables without partitioning
        for table in dataset_info['tables']:
            if table['rowCount'] > 10000000 and not table.get('isPartitioned', False):
                optimizations.append({
                    'type': 'partitioning',
                    'table': table['name'],
                    'recommendation': 'Implement table partitioning for large tables',
                    'estimated_improvement': '30-50% query performance'
                })
        
        # Check for unused columns
        for table in dataset_info['tables']:
            unused_columns = [col for col in table['columns'] 
                            if col['name'] not in dataset_usage['used_columns']]
            if unused_columns:
                optimizations.append({
                    'type': 'column_removal',
                    'table': table['name'],
                    'columns': [col['name'] for col in unused_columns],
                    'recommendation': 'Remove unused columns to reduce memory usage',
                    'estimated_improvement': f'{len(unused_columns) * 5}% memory reduction'
                })
        
        # Check for missing aggregations
        frequent_queries = dataset_usage['frequent_query_patterns']
        for query_pattern in frequent_queries:
            if query_pattern['aggregation_level'] == 'detail' and query_pattern['frequency'] > 100:
                optimizations.append({
                    'type': 'aggregation',
                    'query_pattern': query_pattern['pattern'],
                    'recommendation': 'Create aggregation table for frequent summary queries',
                    'estimated_improvement': '70-90% query performance'
                })
        
        return optimizations

# Usage example
premium_manager = PowerBIPremiumManager(pbi_api)

# Monitor capacity performance
capacity_performance = premium_manager.monitor_capacity_utilization('capacity-id')
print(f"Average CPU utilization: {capacity_performance['avg_cpu_utilization']:.2f}%")

# Get optimization recommendations
optimizations = premium_manager.optimize_capacity_workloads('capacity-id')
for opt in optimizations:
    print(f"Workspace: {opt['workspace']}, Issue: {opt['issue']}, Priority: {opt['priority']}")

# Optimize specific dataset
dataset_optimizations = premium_manager.optimize_dataset_performance('dataset-id')
for opt in dataset_optimizations:
    print(f"Optimization: {opt['type']}, Improvement: {opt['estimated_improvement']}")
```

This comprehensive Power BI interview question set covers essential knowledge for data engineers, from basic Power BI concepts to advanced enterprise implementation patterns, governance frameworks, and Premium capacity optimization strategies.
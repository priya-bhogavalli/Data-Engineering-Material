# Metabase Interview Questions

## 📋 Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [Installation & Setup](#installation--setup)
3. [Data Sources & Connections](#data-sources--connections)
4. [Questions & Dashboards](#questions--dashboards)
5. [Administration & Security](#administration--security)
6. [Performance & Optimization](#performance--optimization)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic Concepts

### Q1: What is Metabase and what are its key features?
**Answer:**
Metabase is an open-source business intelligence tool that makes it easy for everyone in your company to ask questions and learn from data.

**Key Features:**
- **Easy Setup**: Quick installation and configuration
- **Question Builder**: Visual query builder for non-technical users
- **SQL Editor**: Native SQL support for advanced users
- **Dashboards**: Interactive dashboards with filters
- **Alerts**: Automated notifications based on data changes
- **Embedding**: Embed charts and dashboards in other applications
- **Multi-database Support**: Connect to various data sources
- **User Management**: Role-based access control
- **Open Source**: Free community edition available

### Q2: What are the different types of questions you can create in Metabase?
**Answer:**
1. **Simple Questions**: Using the visual query builder
2. **Custom Questions**: Using SQL queries
3. **Native Queries**: Database-specific SQL
4. **Saved Questions**: Reusable queries
5. **Parameterized Questions**: Questions with variables

### Q3: Explain Metabase's architecture components.
**Answer:**
- **Web Application**: Frontend interface
- **Application Database**: Stores Metabase metadata
- **Data Sources**: Connected databases
- **Query Processor**: Handles query execution
- **Caching Layer**: Improves performance
- **Authentication System**: User management

---

## Installation & Setup

### Q4: How do you install Metabase?
**Answer:**
**Installation Methods:**
1. **JAR File**: `java -jar metabase.jar`
2. **Docker**: `docker run -p 3000:3000 metabase/metabase`
3. **Cloud Deployment**: AWS, GCP, Azure
4. **Source Code**: Build from GitHub

**Basic Setup:**
```bash
# Download JAR
wget https://downloads.metabase.com/latest/metabase.jar

# Run Metabase
java -jar metabase.jar
```

### Q5: What environment variables are important for Metabase configuration?
**Answer:**
```bash
# Database configuration
MB_DB_TYPE=postgres
MB_DB_DBNAME=metabase
MB_DB_PORT=5432
MB_DB_USER=metabase
MB_DB_PASS=password
MB_DB_HOST=localhost

# Application settings
MB_SITE_URL=https://metabase.company.com
MB_JETTY_PORT=3000
MB_JAVA_TIMEZONE=UTC

# Email configuration
MB_EMAIL_SMTP_HOST=smtp.gmail.com
MB_EMAIL_SMTP_PORT=587
MB_EMAIL_SMTP_USERNAME=user@company.com
MB_EMAIL_SMTP_PASSWORD=password
```

---

## Data Sources & Connections

### Q6: What databases does Metabase support?
**Answer:**
**Supported Databases:**
- PostgreSQL, MySQL, MariaDB
- SQL Server, Oracle
- SQLite, H2
- MongoDB
- BigQuery, Redshift, Snowflake
- Presto, Athena, Spark SQL
- ClickHouse, Vertica
- And many more...

### Q7: How do you connect a new database to Metabase?
**Answer:**
1. **Admin Panel**: Go to Admin → Databases
2. **Add Database**: Click "Add database"
3. **Configure Connection**:
   ```json
   {
     "engine": "postgres",
     "name": "Production DB",
     "host": "db.company.com",
     "port": 5432,
     "dbname": "production",
     "user": "metabase_user",
     "password": "secure_password"
   }
   ```
4. **Test Connection**: Verify connectivity
5. **Sync Schema**: Import table metadata

### Q8: What is database syncing in Metabase?
**Answer:**
Database syncing is the process where Metabase:
- **Discovers Tables**: Identifies available tables and views
- **Analyzes Schema**: Understands column types and relationships
- **Generates Metadata**: Creates field descriptions and suggestions
- **Updates Regularly**: Keeps schema information current

**Sync Types:**
- **Full Sync**: Complete schema analysis
- **Quick Sync**: Updates table list only
- **Manual Sync**: Triggered by admin

---

## Questions & Dashboards

### Q9: Explain the difference between Simple and Custom questions.
**Answer:**
**Simple Questions:**
- Visual query builder interface
- No SQL knowledge required
- Point-and-click interface
- Limited to basic operations
- Good for business users

**Custom Questions:**
- SQL-based queries
- Full database capabilities
- Advanced filtering and joins
- Complex calculations
- Suitable for technical users

### Q10: How do you create a parameterized question?
**Answer:**
```sql
-- Example parameterized query
SELECT 
    product_name,
    SUM(revenue) as total_revenue
FROM sales s
JOIN products p ON s.product_id = p.id
WHERE s.created_at >= {{start_date}}
  AND s.created_at <= {{end_date}}
  AND p.category = {{category}}
GROUP BY product_name
ORDER BY total_revenue DESC
```

**Parameter Types:**
- Date ranges: `{{start_date}}`
- Text filters: `{{category}}`
- Number filters: `{{min_amount}}`
- Optional parameters: `[[AND status = {{status}}]]`

### Q11: How do you create and customize dashboards?
**Answer:**
**Dashboard Creation:**
1. **Create Dashboard**: Click "New" → "Dashboard"
2. **Add Questions**: Drag saved questions
3. **Arrange Layout**: Resize and position cards
4. **Add Filters**: Create dashboard-level filters
5. **Configure Auto-refresh**: Set update intervals

**Customization Options:**
- Card sizing and positioning
- Color schemes and styling
- Filter connections
- Text cards for context
- Click behavior settings

---

## Administration & Security

### Q12: What are the different user permission levels in Metabase?
**Answer:**
**Permission Levels:**
1. **Admin**: Full system access
2. **User**: Can create questions and dashboards
3. **Viewer**: Read-only access

**Database Permissions:**
- **No Access**: Cannot see database
- **View Data**: Can view but not query
- **Create Queries**: Can create questions
- **Native Querying**: Can write SQL

### Q13: How do you implement row-level security in Metabase?
**Answer:**
**Sandboxing Approach:**
1. **Create User Attributes**: Define user properties
2. **Set Up Sandboxes**: Configure table-level restrictions
3. **Apply Filters**: Use attributes in WHERE clauses

**Example:**
```sql
-- Sandbox configuration
WHERE user_id = {{current_user_id}}
-- or
WHERE region = {{user_region}}
```

### Q14: How do you manage user groups and permissions?
**Answer:**
1. **Create Groups**: Admin → People → Groups
2. **Assign Users**: Add users to appropriate groups
3. **Set Permissions**: Configure database access per group
4. **Collection Access**: Control dashboard/question visibility

---

## Performance & Optimization

### Q15: How does Metabase caching work?
**Answer:**
**Caching Layers:**
1. **Question Results**: Cache query results
2. **Database Schema**: Cache table metadata
3. **Dashboard Filters**: Cache filter values

**Cache Configuration:**
- **TTL Settings**: Time-to-live for cached results
- **Cache Invalidation**: Manual or automatic refresh
- **Memory Limits**: Configure cache size

### Q16: What strategies can you use to optimize Metabase performance?
**Answer:**
**Database Optimization:**
- Create appropriate indexes
- Optimize query structure
- Use database views for complex logic
- Implement data partitioning

**Metabase Configuration:**
- Increase JVM heap size
- Configure connection pooling
- Enable result caching
- Use read replicas

**Query Optimization:**
- Limit result sets
- Use efficient WHERE clauses
- Avoid SELECT *
- Implement pagination

---

## Advanced Features

### Q17: How do you embed Metabase dashboards in external applications?
**Answer:**
**Embedding Options:**
1. **Public Embedding**: No authentication required
2. **Signed Embedding**: JWT-based authentication
3. **Full App Embedding**: Complete Metabase interface

**Implementation:**
```javascript
// Signed embedding example
const payload = {
  resource: {dashboard: 123},
  params: {user_id: 456},
  exp: Math.round(Date.now() / 1000) + (10 * 60) // 10 minutes
};

const token = jwt.sign(payload, METABASE_SECRET_KEY);
const iframeUrl = `${METABASE_SITE_URL}/embed/dashboard/${token}#bordered=true&titled=true`;
```

### Q18: How do you set up alerts in Metabase?
**Answer:**
**Alert Configuration:**
1. **Create Question**: Build the monitoring query
2. **Set Up Alert**: Define trigger conditions
3. **Configure Recipients**: Email or Slack notifications
4. **Schedule Checks**: Set frequency

**Alert Types:**
- Goal line alerts
- Progress alerts
- Custom condition alerts

### Q19: What is the Metabase API and how do you use it?
**Answer:**
**API Capabilities:**
- Create and manage questions
- Export data
- Manage users and permissions
- Automate dashboard creation

**Example Usage:**
```python
import requests

# Authentication
response = requests.post('http://localhost:3000/api/session', {
    'username': 'admin@company.com',
    'password': 'password'
})
session_id = response.json()['id']

# Create question via API
headers = {'X-Metabase-Session': session_id}
question_data = {
    'name': 'Sales Report',
    'dataset_query': {...},
    'display': 'table'
}
requests.post('http://localhost:3000/api/card', 
              json=question_data, headers=headers)
```

---

## Troubleshooting

### Q20: How do you troubleshoot common Metabase issues?
**Answer:**
**Common Issues:**
1. **Connection Problems**: Check database credentials and network
2. **Performance Issues**: Review query complexity and indexes
3. **Memory Errors**: Increase JVM heap size
4. **Sync Failures**: Check database permissions

**Debugging Steps:**
- Check Metabase logs
- Verify database connectivity
- Test queries directly in database
- Monitor system resources

### Q21: How do you backup and restore Metabase?
**Answer:**
**Backup Strategy:**
1. **Application Database**: Backup Metabase's metadata
2. **Configuration Files**: Save environment settings
3. **Custom Content**: Export dashboards and questions

**Backup Commands:**
```bash
# H2 Database (default)
cp metabase.db.mv.db backup/

# PostgreSQL
pg_dump metabase > metabase_backup.sql

# Export via API
curl -X GET "http://localhost:3000/api/database" \
  -H "X-Metabase-Session: $SESSION_ID"
```

---

## Best Practices

### Q22: What are the best practices for organizing Metabase content?
**Answer:**
**Organization Strategy:**
- **Collections**: Group related dashboards and questions
- **Naming Conventions**: Use consistent, descriptive names
- **Tagging**: Apply relevant tags for searchability
- **Documentation**: Add descriptions and context
- **Archiving**: Remove outdated content

**Folder Structure:**
```
Company Analytics/
├── Executive Dashboards/
├── Sales Reports/
├── Marketing Analytics/
├── Operations Metrics/
└── Ad-hoc Analysis/
```

### Q23: How do you ensure data quality in Metabase?
**Answer:**
**Data Quality Measures:**
- **Data Validation**: Implement checks at source
- **Documentation**: Clearly describe metrics
- **Testing**: Validate question results
- **Monitoring**: Set up data freshness alerts
- **Governance**: Establish approval processes

---

## Scenario-Based Questions

### Q24: How would you migrate from another BI tool to Metabase?
**Answer:**
**Migration Strategy:**
1. **Assessment**: Inventory existing reports and dashboards
2. **Data Mapping**: Identify data sources and connections
3. **User Training**: Educate team on Metabase features
4. **Gradual Migration**: Move reports incrementally
5. **Validation**: Ensure data accuracy

**Technical Steps:**
- Export existing queries and logic
- Recreate dashboards in Metabase
- Set up user accounts and permissions
- Configure data connections
- Test and validate results

### Q25: How would you scale Metabase for a large organization?
**Answer:**
**Scaling Strategies:**
1. **Infrastructure**: Use load balancers and multiple instances
2. **Database**: Implement read replicas and caching
3. **Performance**: Optimize queries and indexes
4. **Governance**: Establish content management processes
5. **Training**: Provide comprehensive user education

**Technical Implementation:**
- Deploy on cloud platforms (AWS, GCP, Azure)
- Use container orchestration (Kubernetes)
- Implement monitoring and alerting
- Set up automated backups
- Configure high availability

---

## 🎯 Key Takeaways

- **Easy Setup**: Metabase is designed for quick deployment and user adoption
- **Flexible Querying**: Supports both visual and SQL-based question creation
- **Strong Security**: Comprehensive permission and sandboxing capabilities
- **Embedding**: Powerful options for integrating with external applications
- **Open Source**: Cost-effective solution with active community support
- **Performance**: Requires proper optimization for large-scale deployments
- **Governance**: Benefits from structured content organization and management

Remember: Metabase excels at democratizing data access while maintaining security and performance standards.
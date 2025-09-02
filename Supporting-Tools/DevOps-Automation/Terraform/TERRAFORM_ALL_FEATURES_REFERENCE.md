# Terraform All Features Reference

## 🎯 Overview
Comprehensive reference for Terraform features, providers, state management, modules, and infrastructure automation best practices.

## 📍 Legend

### Feature Status
- 🟢 **Stable** - Production-ready, fully supported
- 🟡 **Beta** - Available but may change
- 🔴 **Alpha** - Early development, experimental
- ⚫ **Deprecated** - Being phased out

### Provider Tiers
- **Official** - HashiCorp maintained
- **Partner** - Third-party verified
- **Community** - Community maintained

## 🏗️ Core Components

| Component | Purpose | Scope | Management | File Extension |
|-----------|---------|-------|------------|----------------|
| **Configuration** | Infrastructure definition | Project | Version control | `.tf` |
| **State** | Resource tracking | Workspace | Backend storage | `.tfstate` |
| **Providers** | Cloud/service APIs | Global | Registry | N/A |
| **Modules** | Reusable components | Configurable | Registry/Git | `.tf` |
| **Variables** | Parameterization | Input | Configuration | `.tfvars` |
| **Outputs** | Exported values | Output | State | `.tf` |

## 🔧 Configuration Language (HCL)

### Basic Syntax Elements
| Element | Purpose | Syntax | Example | Use Cases |
|---------|---------|--------|---------|-----------|
| **Blocks** | Configuration containers | `type "name" {}` | `resource "aws_instance" "web"` | Resource definition |
| **Arguments** | Block parameters | `key = value` | `instance_type = "t3.micro"` | Configuration |
| **Expressions** | Dynamic values | `${expression}` | `"${var.environment}-server"` | Computed values |
| **Comments** | Documentation | `#` or `//` or `/* */` | `# This is a comment` | Code documentation |
| **Functions** | Built-in operations | `function(args)` | `length(var.list)` | Data transformation |

### Data Types
| Type | Description | Syntax | Example | Use Cases |
|------|-------------|--------|---------|-----------|
| **String** | Text values | `"text"` | `"production"` | Names, descriptions |
| **Number** | Numeric values | `123` | `80` | Ports, counts |
| **Bool** | Boolean values | `true/false` | `true` | Feature flags |
| **List** | Ordered collection | `[item1, item2]` | `["web", "app", "db"]` | Multiple values |
| **Map** | Key-value pairs | `{key = value}` | `{env = "prod", team = "data"}` | Tags, configuration |
| **Set** | Unique collection | `toset([items])` | `toset(["a", "b"])` | Unique values |
| **Object** | Complex structure | `{attr = type}` | `{name = string, count = number}` | Complex data |
| **Tuple** | Ordered types | `[type1, type2]` | `[string, number]` | Mixed collections |

## 🌐 Major Providers

### Cloud Providers
| Provider | Resources | Authentication | State Storage | Popularity |
|----------|-----------|----------------|---------------|------------|
| **AWS** | 1000+ | IAM, profiles, env vars | S3 + DynamoDB | Very High |
| **Azure** | 800+ | Service principal, CLI | Storage Account | High |
| **GCP** | 600+ | Service account, ADC | Cloud Storage | High |
| **Alibaba Cloud** | 400+ | Access keys, RAM | OSS | Medium |
| **Oracle Cloud** | 300+ | API keys, instance principal | Object Storage | Medium |

### Infrastructure Providers
| Provider | Focus | Resources | Use Cases | Complexity |
|----------|-------|-----------|-----------|------------|
| **Kubernetes** | Container orchestration | 100+ | K8s resources | Medium |
| **Helm** | Package management | 20+ | Chart deployment | Low |
| **Docker** | Containerization | 30+ | Container management | Low |
| **VMware vSphere** | Virtualization | 50+ | VM management | High |
| **Proxmox** | Virtualization | 20+ | Home labs, small business | Medium |

### Service Providers
| Provider | Category | Resources | Integration | Use Cases |
|----------|----------|-----------|-------------|-----------|
| **Datadog** | Monitoring | 50+ | API-based | Infrastructure monitoring |
| **PagerDuty** | Incident management | 30+ | Webhook/API | Alerting setup |
| **GitHub** | Version control | 40+ | Token-based | Repository management |
| **Cloudflare** | CDN/Security | 80+ | API key | DNS, security |
| **Auth0** | Identity | 25+ | Management API | Authentication |

## 📊 State Management

### Backend Types
| Backend | Storage | Locking | Encryption | Use Cases | Setup Complexity |
|---------|---------|---------|------------|-----------|------------------|
| **Local** | File system | No | No | Development | None |
| **S3** | AWS S3 | DynamoDB | Yes | Production (AWS) | Low |
| **Azure RM** | Storage Account | Blob lease | Yes | Production (Azure) | Low |
| **GCS** | Cloud Storage | No | Yes | Production (GCP) | Low |
| **Consul** | Consul KV | Yes | Yes | Multi-cloud | Medium |
| **etcd** | etcd cluster | Yes | Yes | Kubernetes | Medium |
| **Terraform Cloud** | Managed | Yes | Yes | Enterprise | Low |

### State Operations
| Command | Purpose | Risk Level | Use Cases | Best Practices |
|---------|---------|------------|-----------|----------------|
| **terraform state list** | List resources | Safe | Inventory | Regular auditing |
| **terraform state show** | Show resource | Safe | Debugging | Troubleshooting |
| **terraform state mv** | Move resource | Medium | Refactoring | Backup first |
| **terraform state rm** | Remove from state | High | Cleanup | Manual verification |
| **terraform import** | Import existing | Medium | Migration | Test thoroughly |
| **terraform refresh** | Sync state | Low | Drift detection | Regular maintenance |

## 🧩 Modules & Composition

### Module Structure
| Component | Purpose | Required | Location | Best Practices |
|-----------|---------|----------|----------|----------------|
| **main.tf** | Primary configuration | Yes | Root | Resource definitions |
| **variables.tf** | Input variables | No | Root | Input parameters |
| **outputs.tf** | Output values | No | Root | Exported values |
| **versions.tf** | Provider requirements | Recommended | Root | Version constraints |
| **README.md** | Documentation | Recommended | Root | Usage instructions |
| **examples/** | Usage examples | Recommended | Subdirectory | Common patterns |

### Module Sources
| Source Type | Syntax | Versioning | Use Cases | Security |
|-------------|--------|------------|-----------|----------|
| **Local** | `./modules/vpc` | None | Development | High |
| **Git** | `git::https://...` | Tags/branches | Private repos | Medium |
| **GitHub** | `github.com/user/repo` | Tags | Public repos | Medium |
| **Registry** | `namespace/name/provider` | Semantic versions | Public modules | High |
| **S3** | `s3::https://...` | Object versions | Private storage | High |
| **HTTP** | `https://...` | None | Direct download | Low |

### Module Registry
| Registry | Type | Quality | Verification | Use Cases |
|----------|------|---------|--------------|-----------|
| **Terraform Registry** | Public | Verified | HashiCorp | Standard modules |
| **Private Registry** | Private | Custom | Organization | Internal modules |
| **GitHub Releases** | Public/Private | Variable | Manual | Custom modules |
| **GitLab Packages** | Private | Variable | CI/CD | Enterprise |

## 🔄 Workflow Commands

### Core Workflow
| Command | Purpose | Idempotent | Side Effects | Typical Usage |
|---------|---------|------------|--------------|---------------|
| **terraform init** | Initialize working directory | Yes | Downloads providers/modules | First run, provider updates |
| **terraform plan** | Show execution plan | Yes | None | Review changes |
| **terraform apply** | Apply changes | No | Infrastructure changes | Deploy infrastructure |
| **terraform destroy** | Destroy infrastructure | No | Resource deletion | Cleanup |
| **terraform validate** | Validate configuration | Yes | None | CI/CD validation |
| **terraform fmt** | Format code | Yes | File modifications | Code formatting |

### Advanced Commands
| Command | Purpose | Risk Level | Use Cases | Prerequisites |
|---------|---------|------------|-----------|---------------|
| **terraform import** | Import existing resources | Medium | Migration | Resource identification |
| **terraform taint** | Mark for recreation | High | Force replacement | Resource issues |
| **terraform untaint** | Remove taint | Low | Cancel taint | Accidental tainting |
| **terraform workspace** | Manage workspaces | Low | Environment separation | Multiple environments |
| **terraform force-unlock** | Remove state lock | High | Lock issues | Lock ID |

## 🔒 Security & Best Practices

### Secrets Management
| Method | Security Level | Complexity | Use Cases | Tools |
|--------|----------------|------------|-----------|-------|
| **Environment Variables** | Medium | Low | CI/CD, local dev | Shell, Docker |
| **Variable Files** | Low | Low | Non-sensitive config | `.tfvars` files |
| **External Data Sources** | High | Medium | Dynamic secrets | Vault, AWS Secrets |
| **Provider Authentication** | High | Medium | Cloud credentials | IAM, Service Accounts |
| **Encrypted Backends** | High | Low | State protection | Cloud KMS |

### Access Control
| Level | Scope | Implementation | Granularity | Tools |
|-------|-------|----------------|-------------|-------|
| **Backend Access** | State files | Cloud IAM | File-level | AWS IAM, Azure RBAC |
| **Provider Permissions** | Resources | Cloud policies | Resource-level | IAM policies |
| **Workspace Isolation** | Environments | Separate backends | Environment-level | Multiple backends |
| **Module Access** | Code | Git permissions | Repository-level | Git hosting |

### Compliance Features
| Feature | Purpose | Implementation | Auditing | Standards |
|---------|---------|----------------|----------|-----------|
| **Policy as Code** | Governance | Sentinel, OPA | Built-in | Custom policies |
| **Drift Detection** | Compliance monitoring | Scheduled plans | State comparison | Infrastructure standards |
| **Audit Logging** | Change tracking | Backend logs | Automatic | SOC 2, ISO 27001 |
| **Encryption** | Data protection | Backend encryption | Transparent | FIPS 140-2 |

## ⚡ Performance Optimization

### Plan Optimization
| Technique | Impact | Complexity | Use Cases | Implementation |
|-----------|--------|------------|-----------|----------------|
| **Parallelism** | High | Low | Large deployments | `-parallelism=n` |
| **Targeted Plans** | High | Low | Specific resources | `-target=resource` |
| **Refresh Optimization** | Medium | Low | Large state | `-refresh=false` |
| **Module Caching** | Medium | Medium | Repeated modules | Local cache |
| **Provider Caching** | Low | Low | Multiple runs | Plugin cache |

### State Optimization
| Technique | Impact | Complexity | Use Cases | Implementation |
|-----------|--------|------------|-----------|----------------|
| **State Splitting** | High | High | Large infrastructures | Multiple backends |
| **Remote State** | Medium | Low | Team collaboration | Cloud backends |
| **State Locking** | High | Low | Concurrent access | Backend locking |
| **Partial Configuration** | Medium | Medium | Dynamic backends | CLI arguments |

## 🔧 Advanced Features

### Dynamic Blocks
| Use Case | Syntax | Complexity | Benefits | Example |
|----------|--------|------------|---------|---------|
| **Conditional Resources** | `count` | Low | Optional resources | `count = var.create ? 1 : 0` |
| **Multiple Instances** | `for_each` | Medium | Resource iteration | `for_each = var.instances` |
| **Dynamic Configuration** | `dynamic` | High | Flexible blocks | `dynamic "ingress" { ... }` |
| **Computed Values** | `locals` | Low | Derived values | `locals { name = "${var.env}-app" }` |

### Functions & Expressions
| Category | Functions | Use Cases | Examples |
|----------|-----------|-----------|----------|
| **String** | `join`, `split`, `replace` | Text manipulation | `join("-", [var.env, "web"])` |
| **Collection** | `length`, `keys`, `values` | Data processing | `length(var.subnets)` |
| **Encoding** | `base64encode`, `jsonencode` | Data transformation | `jsonencode(var.tags)` |
| **Filesystem** | `file`, `templatefile` | External data | `file("${path.module}/script.sh")` |
| **Date/Time** | `timestamp`, `formatdate` | Time operations | `formatdate("YYYY-MM-DD", timestamp())` |
| **Network** | `cidrsubnet`, `cidrhost` | IP calculations | `cidrsubnet("10.0.0.0/16", 8, 1)` |

### Provisioners
| Type | Purpose | Platform | Use Cases | Alternatives |
|------|---------|----------|-----------|--------------|
| **local-exec** | Local commands | Any | CI/CD integration | External tools |
| **remote-exec** | Remote commands | Unix/Windows | Configuration | Cloud-init, user data |
| **file** | File transfer | Any | Config files | Cloud storage |
| **null_resource** | Trigger actions | Any | Custom logic | External data sources |

## 🌍 Multi-Cloud & Hybrid

### Cross-Cloud Patterns
| Pattern | Complexity | Use Cases | Challenges | Solutions |
|---------|------------|-----------|------------|-----------|
| **Multi-Provider** | Medium | Hybrid deployments | State management | Separate modules |
| **Cross-Cloud Networking** | High | Interconnected services | Connectivity | VPN, peering |
| **Disaster Recovery** | High | Business continuity | Data synchronization | Replication |
| **Cloud Migration** | High | Platform transitions | Gradual migration | Phased approach |

### Hybrid Infrastructure
| Component | On-Premises | Cloud | Hybrid Tools | Complexity |
|-----------|-------------|-------|--------------|------------|
| **Compute** | VMware, Hyper-V | EC2, VMs | Outposts, Arc | High |
| **Storage** | SAN, NAS | Object, Block | Hybrid storage | Medium |
| **Networking** | Physical switches | VPC, VNet | SD-WAN | High |
| **Identity** | Active Directory | Cloud IAM | Federated identity | Medium |

## 📊 Testing & Validation

### Testing Approaches
| Type | Scope | Tools | Complexity | Use Cases |
|------|-------|-------|------------|-----------|
| **Syntax Validation** | Configuration | `terraform validate` | Low | CI/CD |
| **Plan Testing** | Changes | `terraform plan` | Low | Pre-deployment |
| **Integration Testing** | Infrastructure | Terratest, Kitchen | High | Quality assurance |
| **Compliance Testing** | Policies | Sentinel, OPA | Medium | Governance |
| **Security Scanning** | Vulnerabilities | Checkov, tfsec | Medium | Security |

### Validation Tools
| Tool | Type | Language | Features | Integration |
|------|------|----------|----------|-------------|
| **Terratest** | Integration | Go | Full testing framework | CI/CD |
| **Kitchen-Terraform** | Integration | Ruby | Test Kitchen integration | Chef ecosystem |
| **Terraform Compliance** | Policy | Python | BDD-style tests | Simple setup |
| **Conftest** | Policy | Rego | OPA integration | Kubernetes-friendly |
| **tfsec** | Security | Go | Security scanning | CLI, CI/CD |

## 💰 Cost Management

### Cost Optimization
| Strategy | Impact | Complexity | Implementation | Tools |
|----------|--------|------------|----------------|-------|
| **Resource Tagging** | High | Low | Consistent tags | Cloud cost tools |
| **Right-sizing** | High | Medium | Instance optimization | Cloud advisors |
| **Spot Instances** | High | Medium | Fault-tolerant workloads | Provider features |
| **Scheduled Resources** | Medium | Medium | Time-based scaling | Automation |
| **Reserved Instances** | High | Low | Predictable workloads | Provider programs |

### Cost Monitoring
| Tool | Provider | Features | Granularity | Alerting |
|------|---------|----------|-------------|----------|
| **AWS Cost Explorer** | AWS | Detailed analysis | Resource-level | Yes |
| **Azure Cost Management** | Azure | Budget tracking | Subscription-level | Yes |
| **GCP Billing** | GCP | Usage reports | Project-level | Yes |
| **Infracost** | Multi-cloud | Terraform integration | Resource-level | CI/CD |
| **CloudHealth** | Multi-cloud | Optimization recommendations | Account-level | Yes |

## 🚨 Troubleshooting & Debugging

### Common Issues
| Issue | Symptoms | Causes | Solutions | Prevention |
|-------|----------|--------|-----------|-----------|
| **State Lock** | Apply failures | Concurrent operations | Force unlock | Coordination |
| **Provider Errors** | Authentication failures | Invalid credentials | Check auth | Proper setup |
| **Dependency Cycles** | Plan failures | Circular references | Refactor dependencies | Design review |
| **Resource Conflicts** | Apply errors | Naming conflicts | Unique naming | Naming conventions |
| **Version Conflicts** | Compatibility issues | Provider versions | Version constraints | Lock files |

### Debugging Tools
| Tool | Purpose | Output | Use Cases | Availability |
|------|---------|--------|-----------|--------------|
| **TF_LOG** | Debug logging | Detailed logs | Troubleshooting | Environment variable |
| **terraform show** | State inspection | Human-readable | State analysis | Built-in |
| **terraform graph** | Dependency visualization | DOT format | Architecture review | Built-in |
| **terraform console** | Interactive testing | REPL | Expression testing | Built-in |

## 📚 Learning Resources & Certification

### Certification Path
| Certification | Level | Focus | Duration | Prerequisites |
|---------------|-------|-------|---------|---------------|
| **Terraform Associate** | Associate | Core concepts | 1 hour | Basic Terraform knowledge |
| **Terraform Professional** | Professional | Advanced topics | 2 hours | Associate certification |

### Learning Resources
| Resource | Type | Focus | Level | Cost |
|----------|------|-------|-------|------|
| **HashiCorp Learn** | Interactive | Hands-on tutorials | All | Free |
| **Terraform Documentation** | Reference | Complete features | All | Free |
| **Terraform Up & Running** | Book | Practical guide | Intermediate | Paid |
| **Cloud Provider Workshops** | Hands-on | Provider-specific | Intermediate | Free |
| **Community Forums** | Support | Problem-solving | All | Free |

## 🆚 Terraform vs Alternatives

| Alternative | Terraform Advantage | Alternative Advantage | Best Choice When |
|-------------|-------------------|----------------------|------------------|
| **CloudFormation** | Multi-cloud, HCL syntax | AWS native, no state management | Need multi-cloud flexibility |
| **Pulumi** | Mature ecosystem, declarative | Real programming languages | Prefer declarative approach |
| **Ansible** | Infrastructure focus | Configuration management | Need pure infrastructure |
| **CDK** | Provider agnostic | Type safety, IDE support | Want cloud-agnostic solution |
| **ARM Templates** | Multi-cloud support | Azure native integration | Need cross-cloud deployment |
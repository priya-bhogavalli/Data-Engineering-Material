# Git All Features Reference

## 🎯 Overview
Comprehensive reference for Git version control system, including commands, workflows, branching strategies, and collaboration patterns.

## 📍 Legend

### Command Categories
- 🟢 **Essential** - Daily use commands
- 🟡 **Intermediate** - Regular use commands  
- 🔴 **Advanced** - Specialized use commands
- ⚫ **Dangerous** - Use with caution

### Git Areas
- **Working Directory** - Your local files
- **Staging Area** - Prepared changes
- **Local Repository** - Committed changes
- **Remote Repository** - Shared repository

## 🏗️ Core Git Architecture

| Component | Purpose | Scope | Persistence | Collaboration |
|-----------|---------|-------|-------------|---------------|
| **Working Directory** | File editing | Local | Temporary | Individual |
| **Staging Area (Index)** | Change preparation | Local | Session | Individual |
| **Local Repository** | Version history | Local | Permanent | Individual |
| **Remote Repository** | Shared history | Distributed | Permanent | Team |
| **Stash** | Temporary storage | Local | Temporary | Individual |

## 📊 Essential Commands Reference

### Repository Management
| Command | Purpose | Risk Level | Frequency | Example |
|---------|---------|------------|-----------|---------|
| **git init** | 🟢 Create repository | Safe | Once per project | `git init` |
| **git clone** | 🟢 Copy repository | Safe | Once per project | `git clone <url>` |
| **git status** | 🟢 Check status | Safe | Very High | `git status` |
| **git log** | 🟢 View history | Safe | High | `git log --oneline` |
| **git remote** | 🟡 Manage remotes | Safe | Low | `git remote -v` |

### File Operations
| Command | Purpose | Risk Level | Reversible | Example |
|---------|---------|------------|------------|---------|
| **git add** | 🟢 Stage changes | Safe | Yes | `git add file.txt` |
| **git commit** | 🟢 Save changes | Safe | Yes (with effort) | `git commit -m "message"` |
| **git rm** | 🟡 Remove files | Medium | Yes (if committed) | `git rm file.txt` |
| **git mv** | 🟡 Move/rename files | Safe | Yes | `git mv old.txt new.txt` |
| **git restore** | 🟡 Restore files | Medium | No (for unstaged) | `git restore file.txt` |

### Branch Operations
| Command | Purpose | Risk Level | Impact | Example |
|---------|---------|------------|--------|---------|
| **git branch** | 🟢 List/create branches | Safe | Local | `git branch feature` |
| **git checkout** | 🟢 Switch branches | Medium | Working directory | `git checkout main` |
| **git switch** | 🟢 Switch branches (new) | Medium | Working directory | `git switch feature` |
| **git merge** | 🟡 Combine branches | Medium | History | `git merge feature` |
| **git rebase** | 🔴 Rewrite history | High | History | `git rebase main` |

### Remote Operations
| Command | Purpose | Risk Level | Network Required | Example |
|---------|---------|------------|------------------|---------|
| **git fetch** | 🟢 Download changes | Safe | Yes | `git fetch origin` |
| **git pull** | 🟢 Fetch and merge | Medium | Yes | `git pull origin main` |
| **git push** | 🟢 Upload changes | Medium | Yes | `git push origin main` |
| **git push --force** | ⚫ Force upload | Very High | Yes | `git push --force-with-lease` |

## 🌿 Branching Strategies

### Git Flow
| Branch Type | Purpose | Lifetime | Merge Target | Naming Convention |
|-------------|---------|----------|--------------|-------------------|
| **main/master** | Production code | Permanent | N/A | `main` |
| **develop** | Integration branch | Permanent | main | `develop` |
| **feature** | New features | Temporary | develop | `feature/user-auth` |
| **release** | Release preparation | Temporary | main, develop | `release/v1.2.0` |
| **hotfix** | Critical fixes | Temporary | main, develop | `hotfix/security-patch` |

### GitHub Flow
| Branch Type | Purpose | Lifetime | Merge Target | Process |
|-------------|---------|----------|--------------|---------|
| **main** | Production code | Permanent | N/A | Direct deployment |
| **feature** | All changes | Temporary | main | Pull request → merge |

### GitLab Flow
| Branch Type | Purpose | Environment | Deployment | Use Cases |
|-------------|---------|-------------|------------|-----------|
| **main** | Development | Development | Automatic | Continuous integration |
| **pre-production** | Staging | Staging | Manual | Testing |
| **production** | Production | Production | Manual | Stable releases |

## 🔧 Advanced Git Operations

### History Manipulation
| Command | Purpose | Risk Level | Use Cases | Reversibility |
|---------|---------|------------|-----------|---------------|
| **git rebase -i** | 🔴 Interactive rebase | High | Clean history | Difficult |
| **git reset** | 🔴 Move HEAD | High | Undo commits | Partial |
| **git revert** | 🟡 Create inverse commit | Low | Safe undo | Easy |
| **git cherry-pick** | 🟡 Copy commits | Medium | Selective merging | Easy |
| **git reflog** | 🟡 Recovery tool | Safe | Find lost commits | N/A |

### Reset Options
| Option | Working Directory | Staging Area | Repository | Use Cases |
|--------|------------------|--------------|------------|-----------|
| **--soft** | Unchanged | Unchanged | Reset | Redo commit message |
| **--mixed** (default) | Unchanged | Reset | Reset | Unstage changes |
| **--hard** | Reset | Reset | Reset | Complete reset |

### Stash Operations
| Command | Purpose | Scope | Persistence | Example |
|---------|---------|-------|-------------|---------|
| **git stash** | Save work temporarily | Working dir + staging | Until applied | `git stash` |
| **git stash pop** | Apply and remove stash | Restore changes | Removes stash | `git stash pop` |
| **git stash apply** | Apply stash | Restore changes | Keeps stash | `git stash apply` |
| **git stash list** | List stashes | View all stashes | N/A | `git stash list` |
| **git stash drop** | Delete stash | Remove stash | Permanent | `git stash drop` |

## 🔍 Inspection & Comparison

### Log and History
| Command | Information | Format Options | Filtering | Example |
|---------|-------------|----------------|-----------|---------|
| **git log** | Commit history | --oneline, --graph | --since, --author | `git log --oneline --graph` |
| **git show** | Commit details | Patch format | Specific commit | `git show HEAD~1` |
| **git blame** | Line-by-line history | Author, date | File-specific | `git blame file.txt` |
| **git bisect** | Binary search bugs | Interactive | Commit range | `git bisect start` |

### Diff Operations
| Command | Comparison | Scope | Output Format | Use Cases |
|---------|------------|-------|---------------|-----------|
| **git diff** | Working vs staging | Changes | Unified diff | Review before staging |
| **git diff --staged** | Staging vs repository | Staged changes | Unified diff | Review before commit |
| **git diff HEAD** | Working vs repository | All changes | Unified diff | See all modifications |
| **git diff branch1..branch2** | Between branches | Branch comparison | Unified diff | Compare branches |

## 🔀 Merge Strategies

### Merge Types
| Strategy | History | Conflicts | Use Cases | Command |
|----------|---------|-----------|-----------|---------|
| **Fast-forward** | Linear | None | Simple updates | `git merge feature` |
| **Three-way merge** | Branched | Possible | Diverged branches | `git merge --no-ff feature` |
| **Squash merge** | Linear | Possible | Clean history | `git merge --squash feature` |
| **Rebase merge** | Linear | Possible | Clean history | `git rebase main` |

### Conflict Resolution
| Tool | Interface | Complexity | Features | Availability |
|------|-----------|------------|----------|--------------|
| **Manual editing** | Text editor | Low | Basic | Always |
| **git mergetool** | External tool | Medium | Visual | Configurable |
| **IDE integration** | IDE | Medium | Context-aware | IDE-dependent |
| **Web interface** | Browser | Low | Simple | Platform-dependent |

## 🌐 Remote Repository Management

### Remote Operations
| Command | Purpose | Direction | Safety | Example |
|---------|---------|-----------|--------|---------|
| **git remote add** | Add remote | N/A | Safe | `git remote add upstream <url>` |
| **git fetch** | Download refs | Remote → Local | Safe | `git fetch --all` |
| **git pull** | Fetch + merge | Remote → Local | Medium risk | `git pull --rebase` |
| **git push** | Upload changes | Local → Remote | Medium risk | `git push -u origin main` |
| **git push --tags** | Upload tags | Local → Remote | Safe | `git push --tags` |

### Tracking Branches
| Concept | Purpose | Setup | Behavior | Example |
|---------|---------|-------|----------|---------|
| **Upstream branch** | Default remote branch | Automatic/manual | Pull/push target | `git branch -u origin/main` |
| **Remote-tracking branch** | Local copy of remote | Automatic | Read-only | `origin/main` |
| **Local branch** | Working branch | Manual | Read-write | `main` |

## 🏷️ Tagging & Releases

### Tag Types
| Type | Storage | Metadata | Signing | Use Cases |
|------|---------|----------|---------|-----------|
| **Lightweight** | Reference only | Minimal | No | Quick markers |
| **Annotated** | Full object | Rich | Yes | Releases |

### Tagging Commands
| Command | Purpose | Type | Example | Best Practice |
|---------|---------|------|---------|---------------|
| **git tag** | List tags | N/A | `git tag` | Regular review |
| **git tag v1.0** | Create lightweight | Lightweight | `git tag v1.0` | Quick marking |
| **git tag -a v1.0** | Create annotated | Annotated | `git tag -a v1.0 -m "Release 1.0"` | Production releases |
| **git tag -d v1.0** | Delete tag | Both | `git tag -d v1.0` | Cleanup |
| **git push --tags** | Push tags | Both | `git push --tags` | Share releases |

## ⚙️ Configuration & Customization

### Configuration Levels
| Level | Scope | File Location | Priority | Use Cases |
|-------|-------|---------------|----------|-----------|
| **System** | All users | `/etc/gitconfig` | Lowest | System-wide settings |
| **Global** | Current user | `~/.gitconfig` | Medium | Personal preferences |
| **Local** | Current repository | `.git/config` | Highest | Project-specific |

### Essential Configuration
| Setting | Purpose | Example | Impact |
|---------|---------|---------|--------|
| **user.name** | Commit author | `git config --global user.name "John Doe"` | All commits |
| **user.email** | Commit email | `git config --global user.email "john@example.com"` | All commits |
| **core.editor** | Default editor | `git config --global core.editor "code --wait"` | Commit messages |
| **init.defaultBranch** | Default branch name | `git config --global init.defaultBranch main` | New repositories |
| **pull.rebase** | Pull behavior | `git config --global pull.rebase true` | Pull operations |

### Aliases
| Alias | Command | Purpose | Example |
|-------|---------|---------|---------|
| **co** | checkout | Quick switching | `git config --global alias.co checkout` |
| **br** | branch | Branch management | `git config --global alias.br branch` |
| **st** | status | Quick status | `git config --global alias.st status` |
| **unstage** | reset HEAD -- | Unstage files | `git config --global alias.unstage 'reset HEAD --'` |
| **last** | log -1 HEAD | Last commit | `git config --global alias.last 'log -1 HEAD'` |

## 🔒 Security & Best Practices

### Commit Signing
| Method | Security Level | Setup Complexity | Verification | Use Cases |
|--------|----------------|------------------|--------------|-----------|
| **GPG Signing** | High | High | Cryptographic | Open source projects |
| **SSH Signing** | High | Medium | SSH keys | Modern workflows |
| **No Signing** | None | None | None | Internal projects |

### Security Best Practices
| Practice | Risk Mitigation | Implementation | Verification |
|----------|-----------------|----------------|--------------|
| **Never commit secrets** | Data breaches | .gitignore, pre-commit hooks | Repository scanning |
| **Use signed commits** | Identity verification | GPG/SSH setup | Signature verification |
| **Protect main branch** | Accidental changes | Branch protection rules | Platform settings |
| **Regular backups** | Data loss | Multiple remotes | Backup verification |
| **Access control** | Unauthorized access | Platform permissions | Regular audits |

### .gitignore Patterns
| Pattern | Matches | Use Cases | Example |
|---------|---------|-----------|---------|
| **Exact filename** | Specific file | Known files | `config.json` |
| **Wildcard** | Pattern matching | File types | `*.log` |
| **Directory** | Entire directory | Build outputs | `node_modules/` |
| **Negation** | Exception to rule | Include specific files | `!important.log` |
| **Comments** | Documentation | Explanation | `# Build outputs` |

## 🚀 Workflow Optimization

### Commit Best Practices
| Practice | Benefit | Implementation | Example |
|----------|---------|----------------|---------|
| **Atomic commits** | Clear history | Single logical change | One feature per commit |
| **Descriptive messages** | Understanding | Clear, concise description | "Add user authentication" |
| **Conventional commits** | Automation | Structured format | "feat: add login endpoint" |
| **Frequent commits** | Safety | Regular checkpoints | Multiple commits per day |

### Branch Naming Conventions
| Type | Pattern | Example | Purpose |
|------|---------|---------|---------|
| **Feature** | feature/description | `feature/user-login` | New functionality |
| **Bugfix** | bugfix/description | `bugfix/login-error` | Bug fixes |
| **Hotfix** | hotfix/description | `hotfix/security-patch` | Critical fixes |
| **Release** | release/version | `release/v1.2.0` | Release preparation |
| **Experiment** | experiment/description | `experiment/new-ui` | Experimental work |

## 🔧 Git Hooks & Automation

### Client-side Hooks
| Hook | Trigger | Use Cases | Blocking | Example |
|------|---------|-----------|----------|---------|
| **pre-commit** | Before commit | Code quality checks | Yes | Linting, formatting |
| **prepare-commit-msg** | Commit message prep | Message templates | No | Issue number insertion |
| **commit-msg** | Commit message validation | Message format | Yes | Conventional commits |
| **pre-push** | Before push | Final validation | Yes | Test execution |

### Server-side Hooks
| Hook | Trigger | Use Cases | Environment | Example |
|------|---------|-----------|-------------|---------|
| **pre-receive** | Before push acceptance | Access control | Server | Permission checks |
| **update** | Before ref update | Branch policies | Server | Branch protection |
| **post-receive** | After push acceptance | Deployment | Server | CI/CD triggers |

## 📊 Performance & Optimization

### Repository Maintenance
| Command | Purpose | Frequency | Impact | Example |
|---------|---------|-----------|--------|---------|
| **git gc** | Garbage collection | Weekly | Performance | `git gc --aggressive` |
| **git prune** | Remove unreachable objects | Monthly | Storage | `git prune` |
| **git fsck** | File system check | Monthly | Integrity | `git fsck --full` |
| **git repack** | Optimize pack files | Rarely | Performance | `git repack -ad` |

### Large Repository Handling
| Technique | Use Cases | Implementation | Limitations |
|-----------|-----------|----------------|-------------|
| **Git LFS** | Large files | Extension | Additional setup |
| **Shallow clones** | CI/CD | `--depth` option | Limited history |
| **Sparse checkout** | Partial working directory | Configuration | Complex setup |
| **Submodules** | Code organization | Separate repositories | Management overhead |

## 🚨 Troubleshooting & Recovery

### Common Issues
| Issue | Symptoms | Causes | Solutions |
|-------|----------|--------|-----------|
| **Merge conflicts** | Conflict markers | Overlapping changes | Manual resolution |
| **Detached HEAD** | Warning messages | Checkout specific commit | Create branch or checkout branch |
| **Lost commits** | Missing work | Reset/rebase errors | Use reflog |
| **Large repository** | Slow operations | History/large files | Repository maintenance |
| **Authentication errors** | Push/pull failures | Credentials/permissions | Update credentials |

### Recovery Commands
| Command | Purpose | Risk Level | Use Cases |
|---------|---------|------------|-----------|
| **git reflog** | Find lost commits | Safe | Recovery |
| **git fsck --lost-found** | Find orphaned objects | Safe | Deep recovery |
| **git reset --hard ORIG_HEAD** | Undo last operation | High | Emergency reset |
| **git cherry-pick** | Recover specific commits | Medium | Selective recovery |

## 📚 Learning Resources & Tools

### Official Resources
| Resource | Type | Focus | Level | Cost |
|----------|------|-------|-------|------|
| **Pro Git Book** | Book | Comprehensive | All | Free |
| **Git Documentation** | Reference | Complete | All | Free |
| **Git Tutorial** | Interactive | Hands-on | Beginner | Free |

### GUI Tools
| Tool | Platform | Features | Cost | Use Cases |
|------|---------|----------|------|-----------|
| **GitKraken** | Cross-platform | Visual interface | Freemium | Complex workflows |
| **SourceTree** | Windows/Mac | Atlassian integration | Free | Bitbucket users |
| **GitHub Desktop** | Windows/Mac | GitHub integration | Free | GitHub users |
| **Git Extensions** | Windows | Comprehensive | Free | Windows users |

### Command Line Enhancements
| Tool | Purpose | Features | Installation |
|------|---------|----------|-------------|
| **Oh My Zsh** | Shell enhancement | Git aliases, themes | Package manager |
| **Git Bash** | Windows Git shell | Unix-like commands | Git installer |
| **Tig** | Text-mode interface | Interactive browsing | Package manager |
| **Delta** | Better diffs | Syntax highlighting | Package manager |

## 🆚 Git vs Alternatives

| Alternative | Git Advantage | Alternative Advantage | Best Choice When |
|-------------|---------------|----------------------|------------------|
| **Subversion (SVN)** | Distributed, branching | Centralized, simpler | Need distributed development |
| **Mercurial** | Larger ecosystem | Simpler interface | Need Git ecosystem |
| **Perforce** | Open source, flexibility | Enterprise features | Need cost-effective solution |
| **Bazaar** | Active development | Distributed | Need maintained system |
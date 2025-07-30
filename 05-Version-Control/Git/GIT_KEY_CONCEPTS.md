# Git Key Concepts

## 1. Git Fundamentals
**What is Git**: A distributed version control system for tracking changes in source code during software development.

**Key Concepts**:
- **Repository**: Project folder containing all files and version history
- **Commit**: Snapshot of changes with unique identifier (SHA)
- **Branch**: Independent line of development
- **Remote**: Repository hosted on external server (GitHub, GitLab)
- **Working Directory**: Current state of files you're editing
- **Staging Area**: Intermediate area for preparing commits

**Git Workflow**:
```
Working Directory → Staging Area → Local Repository → Remote Repository
     (edit)           (add)         (commit)         (push)
```

## 2. Repository Setup
**Initialize Repository**:
```bash
# Create new repository
git init
git init my-project

# Clone existing repository
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git

# Clone specific branch
git clone -b develop https://github.com/user/repo.git

# Clone with different name
git clone https://github.com/user/repo.git my-local-name
```

**Configuration**:
```bash
# Global configuration
git config --global user.name "John Doe"
git config --global user.email "john@example.com"
git config --global init.defaultBranch main

# Repository-specific configuration
git config user.name "Work User"
git config user.email "work@company.com"

# View configuration
git config --list
git config --global --list

# Editor configuration
git config --global core.editor "code --wait"
git config --global merge.tool vimdiff
```

## 3. Basic Operations
**Staging and Committing**:
```bash
# Check status
git status
git status -s  # Short format

# Add files to staging
git add file.txt
git add *.py
git add .  # Add all files
git add -A  # Add all including deleted files

# Remove from staging
git reset file.txt
git reset  # Unstage all files

# Commit changes
git commit -m "Add data processing module"
git commit -am "Fix bug in ETL pipeline"  # Add and commit

# Amend last commit
git commit --amend -m "Updated commit message"
git commit --amend --no-edit  # Keep same message
```

**Viewing History**:
```bash
# View commit history
git log
git log --oneline
git log --graph --oneline --all
git log --since="2 weeks ago"
git log --author="John Doe"

# View specific file history
git log -- file.txt
git log -p file.txt  # Show changes

# Show commit details
git show HEAD
git show abc1234
git show HEAD~2  # Two commits ago

# View changes
git diff  # Working directory vs staging
git diff --staged  # Staging vs last commit
git diff HEAD~1  # Compare with previous commit
```

## 4. Branching and Merging
**Branch Operations**:
```bash
# List branches
git branch
git branch -a  # Include remote branches
git branch -r  # Remote branches only

# Create branch
git branch feature/data-pipeline
git checkout -b feature/user-auth  # Create and switch
git switch -c feature/api-endpoints  # Modern syntax

# Switch branches
git checkout main
git switch develop  # Modern syntax

# Delete branch
git branch -d feature/completed
git branch -D feature/force-delete  # Force delete

# Rename branch
git branch -m old-name new-name
git branch -m new-name  # Rename current branch
```

**Merging Strategies**:
```bash
# Fast-forward merge (default when possible)
git checkout main
git merge feature/data-pipeline

# No fast-forward merge (always create merge commit)
git merge --no-ff feature/user-auth

# Squash merge (combine all commits into one)
git merge --squash feature/small-fixes
git commit -m "Add small fixes"

# Merge with custom message
git merge feature/api -m "Merge API endpoints feature"
```

**Rebasing**:
```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase (last 3 commits)
git rebase -i HEAD~3

# Rebase with conflict resolution
git rebase main
# Fix conflicts, then:
git add .
git rebase --continue

# Abort rebase
git rebase --abort

# Rebase onto different branch
git rebase --onto main develop feature
```

## 5. Remote Repositories
**Remote Management**:
```bash
# List remotes
git remote
git remote -v  # Show URLs

# Add remote
git remote add origin https://github.com/user/repo.git
git remote add upstream https://github.com/original/repo.git

# Change remote URL
git remote set-url origin git@github.com:user/repo.git

# Remove remote
git remote remove upstream
```

**Push and Pull**:
```bash
# Push to remote
git push origin main
git push -u origin feature/new-feature  # Set upstream
git push --all  # Push all branches

# Pull from remote
git pull origin main
git pull --rebase origin main  # Rebase instead of merge

# Fetch without merging
git fetch origin
git fetch --all

# Push tags
git push origin --tags
git push origin v1.0.0
```

## 6. Conflict Resolution
**Merge Conflicts**:
```bash
# When conflict occurs during merge
git status  # Shows conflicted files

# Edit conflicted files (remove conflict markers)
<<<<<<< HEAD
Current branch content
=======
Incoming branch content
>>>>>>> feature-branch

# After resolving conflicts
git add conflicted-file.txt
git commit  # Complete the merge

# Abort merge
git merge --abort
```

**Rebase Conflicts**:
```bash
# During rebase conflict
git status
# Edit files to resolve conflicts
git add resolved-file.txt
git rebase --continue

# Skip problematic commit
git rebase --skip

# Abort rebase
git rebase --abort
```

**Merge Tools**:
```bash
# Configure merge tool
git config --global merge.tool vimdiff
git config --global merge.tool vscode

# Use merge tool
git mergetool

# Custom merge tool command
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```

## 7. Stashing
**Stash Operations**:
```bash
# Stash current changes
git stash
git stash push -m "Work in progress on feature"

# Stash including untracked files
git stash -u
git stash --include-untracked

# List stashes
git stash list

# Apply stash
git stash apply  # Apply latest stash
git stash apply stash@{2}  # Apply specific stash
git stash pop  # Apply and remove from stash list

# Show stash contents
git stash show
git stash show -p stash@{1}

# Drop stash
git stash drop stash@{1}
git stash clear  # Remove all stashes
```

**Selective Stashing**:
```bash
# Stash specific files
git stash push -m "Stash config files" config/*.yml

# Interactive stashing
git stash -p  # Choose hunks to stash

# Create branch from stash
git stash branch feature/stashed-work stash@{1}
```

## 8. Tags and Releases
**Tagging**:
```bash
# Lightweight tag
git tag v1.0.0

# Annotated tag (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Tag specific commit
git tag -a v0.9.0 abc1234 -m "Beta release"

# List tags
git tag
git tag -l "v1.*"  # Pattern matching

# Show tag information
git show v1.0.0

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0  # Delete from remote
```

**Release Management**:
```bash
# Push tags to remote
git push origin v1.0.0
git push origin --tags

# Checkout specific tag
git checkout v1.0.0

# Create branch from tag
git checkout -b hotfix/v1.0.1 v1.0.0
```

## 9. Advanced Git Operations
**Cherry-picking**:
```bash
# Apply specific commit to current branch
git cherry-pick abc1234

# Cherry-pick multiple commits
git cherry-pick abc1234 def5678

# Cherry-pick without committing
git cherry-pick --no-commit abc1234

# Cherry-pick range of commits
git cherry-pick main~4..main~2
```

**Reset and Revert**:
```bash
# Soft reset (keep changes in staging)
git reset --soft HEAD~1

# Mixed reset (default, keep changes in working directory)
git reset HEAD~1
git reset --mixed HEAD~1

# Hard reset (discard all changes)
git reset --hard HEAD~1
git reset --hard origin/main

# Revert commit (create new commit that undoes changes)
git revert abc1234
git revert HEAD~2
```

**Reflog**:
```bash
# View reference log
git reflog
git reflog --all

# Recover lost commits
git reflog
git checkout abc1234  # From reflog output
git branch recovered-branch abc1234
```

## 10. Git Workflows and Best Practices
**Gitflow Workflow**:
```bash
# Initialize gitflow
git flow init

# Start feature
git flow feature start new-feature
# Work on feature...
git flow feature finish new-feature

# Start release
git flow release start 1.0.0
# Prepare release...
git flow release finish 1.0.0

# Hotfix
git flow hotfix start critical-fix
git flow hotfix finish critical-fix
```

**GitHub Flow**:
```bash
# 1. Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/user-authentication

# 2. Work and commit
git add .
git commit -m "Add user login functionality"
git push -u origin feature/user-authentication

# 3. Create pull request (via GitHub UI)
# 4. Review and merge
# 5. Delete feature branch
git checkout main
git pull origin main
git branch -d feature/user-authentication
```

**Commit Message Conventions**:
```bash
# Conventional Commits format
git commit -m "feat: add user authentication system"
git commit -m "fix: resolve database connection timeout"
git commit -m "docs: update API documentation"
git commit -m "refactor: optimize data processing pipeline"
git commit -m "test: add unit tests for user service"

# Types: feat, fix, docs, style, refactor, test, chore
```

**Git Hooks**:
```bash
# Pre-commit hook example (.git/hooks/pre-commit)
#!/bin/sh
# Run tests before commit
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi

# Make executable
chmod +x .git/hooks/pre-commit

# Pre-push hook example (.git/hooks/pre-push)
#!/bin/sh
# Run linting before push
flake8 .
if [ $? -ne 0 ]; then
    echo "Linting failed. Push aborted."
    exit 1
fi
```

**Useful Aliases**:
```bash
# Set up common aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
git config --global alias.lg "log --oneline --graph --all"

# Use aliases
git st  # Same as git status
git lg  # Pretty log output
```
# Version Control Quick Reference

## Basic Git Commands
```bash
# Repository setup
git init
git clone <url>
git remote add origin <url>

# Basic workflow
git add .
git add file.py
git commit -m "message"
git push origin main
git pull origin main

# Status and history
git status
git log --oneline
git diff
git show <commit-hash>
```

## Branching
```bash
# Create and switch branches
git branch feature-branch
git checkout feature-branch
git checkout -b feature-branch  # Create and switch

# List branches
git branch                      # Local branches
git branch -r                   # Remote branches
git branch -a                   # All branches

# Merge and delete
git checkout main
git merge feature-branch
git branch -d feature-branch    # Delete local
git push origin --delete feature-branch  # Delete remote
```

## Undoing Changes
```bash
# Unstage files
git reset HEAD file.py

# Discard working directory changes
git checkout -- file.py
git restore file.py

# Undo commits
git reset --soft HEAD~1         # Keep changes staged
git reset --hard HEAD~1         # Discard changes
git revert <commit-hash>        # Create new commit that undoes
```

## Remote Operations
```bash
# Remote repositories
git remote -v
git remote add upstream <url>
git fetch origin
git pull origin main
git push origin feature-branch

# Tags
git tag v1.0.0
git push origin --tags
git tag -d v1.0.0              # Delete local tag
```

## Stashing
```bash
# Save work temporarily
git stash
git stash save "work in progress"
git stash list
git stash pop                   # Apply and remove
git stash apply                 # Apply but keep
git stash drop                  # Delete stash
```

## Configuration
```bash
# User configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"

# Aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
```
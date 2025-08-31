# File Naming Standardization Report

## Summary
Fixed inconsistent file naming conventions throughout the Data Engineering repository to follow the established uppercase pattern.

## Issues Identified
1. **Mixed case files**: Some files used lowercase with hyphens while others used uppercase with underscores
2. **Duplicate content**: Renaming created duplicate files with similar content

## Changes Made

### Files Renamed
1. `Core-Data-Engineering/Data-Processing/Apache-Spark/concepts.md` → `KEY_CONCEPTS.md`
2. `Core-Data-Engineering/Programming-Languages/SQL/interview-questions.md` → `INTERVIEW_QUESTIONS.md`

### Duplicates Resolved
1. **Apache Spark**: Merged `KEY_CONCEPTS.md` content with existing `SPARK_KEY_CONCEPTS.md` and removed duplicate
2. **SQL**: Merged `INTERVIEW_QUESTIONS.md` content with existing `SQL_INTERVIEW_QUESTIONS.md` and removed duplicate

## Current Naming Convention
All files now follow the established pattern:
- **Technology-specific files**: `TECHNOLOGY_TYPE.md` (e.g., `SPARK_KEY_CONCEPTS.md`, `SQL_INTERVIEW_QUESTIONS.md`)
- **General files**: `CATEGORY_TYPE.md` (e.g., `DATA_ARCHITECTURE_BEST_PRACTICES.md`)
- **Code files**: Keep original naming (e.g., `.py`, `.sql`, `.scala` files)

## Verification
✅ All markdown files now follow consistent uppercase naming convention
✅ No duplicate files remain
✅ Content integrity maintained during merges
✅ Repository structure remains intact

## Scripts Created
1. `standardize_filenames.py` - Initial renaming script
2. `merge_duplicate_files.py` - Duplicate resolution script

## Next Steps
- Consider implementing a pre-commit hook to enforce naming conventions
- Update any documentation that references the old filenames
- Review internal links that might reference the renamed files

---
*Report generated on: $(date)*
*Total files processed: 2 renamed, 2 duplicates resolved*
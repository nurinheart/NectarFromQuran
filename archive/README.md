# Archive Directory

This directory contains all generated Quran verse images organized by date.

## Structure

```
archive/
├── YYYY/           # Year
│   ├── MM/         # Month
│   │   ├── *.png   # Generated images
│   │   └── log.txt # Archive log
```

## Purpose

- **Permanent Storage**: All generated images are archived here permanently
- **Version Control**: Tracked in git for complete history
- **Workflow Artifacts**: GitHub Actions also uploads to workflow artifacts (7-day retention)

## Archive Process

1. GitHub Actions runs twice daily (06:00 and 21:00 UTC)
2. Generates Quran verse carousel post
3. Posts to Instagram
4. Archives images to `archive/YYYY/MM/`
5. Commits and pushes to git

## Access

- **Git History**: Browse archived images in git commits
- **Workflow Artifacts**: Download from GitHub Actions (last 7 days only)
- **Local**: Images stored in date-based folders

---

*Automated by GitHub Actions*
*Last Updated: 2025-11-22*

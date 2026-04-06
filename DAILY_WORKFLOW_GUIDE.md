# Daily Voice Memo Workflow Guide

**Complete guide to using iMazing + daily cron automation with incremental transcription.**

---

## Overview

This system runs a complete workflow **every day**:

1. **Sync from iPhone** (via iMazing)
2. **Identify new memos** (incremental tracking)
3. **Transcribe only new files** (avoids re-processing)
4. **Analyze speech** (SLP pathology markers)
5. **Update searchable index**
6. **Backup to GitHub** (automatic)

All automated. You don't touch anything.

---

## Three Scenarios

### Scenario 1: First Time (100-200 Backlog)

**Goal:** Process all existing memos, THEN set up daily automation.

```bash
# 1. Do initial bulk export (one time)
# On iPhone: Voice Memos → Select All → Share → Save to Files
# Transfer to Mac via AirDrop

# 2. Copy to input folder
cp ~/Downloads/VoiceMemos/*.m4a input/

# 3. Transcribe all backlog (takes 1-2 hours for 100-200)
python scripts/batch_transcribe.py

# 4. Once done, set up daily cron
python scripts/setup_daily_cron.py
```

**What happens next:** Daily cron runs at 2 AM, only processes NEW memos from that day forward.

---

### Scenario 2: Ongoing Daily Automation

**Goal:** Every day, automatically sync + transcribe + backup.

```bash
# Set up once:
python scripts/setup_daily_cron.py

# Then do nothing. Every day at 2 AM:
# • iMazing syncs new memos from iPhone
# • Only NEW memos get transcribed
# • Results pushed to GitHub
```

**The daily workflow does this:**

```
[02:00 AM Daily]
├─ Sync iPhone → input/ (via iMazing)
├─ Check which memos are new
├─ Transcribe only new ones
├─ Update index
└─ Push to GitHub
```

---

### Scenario 3: Manual Override (Anytime)

**Goal:** Run the workflow immediately without waiting for cron.

```bash
# Full workflow now
python scripts/daily_workflow.py

# Skip iMazing sync (use files already in input/)
python scripts/daily_workflow.py --skip-imazing

# With GitHub backup
python scripts/daily_workflow.py \
  --repo libbynatico/voice-memo-transcription \
  --token ghp_YOUR_TOKEN
```

---

## Initial Setup (First Time Only)

### Step 1: Export Your Backlog

**On iPhone:**
1. Open Voice Memos app
2. Tap "Select" (top right)
3. Tap "Select All"
4. Tap "Share"
5. Choose "Save to Files"
6. Pick a folder (e.g., "VoiceMemos")

**On Mac:**
```bash
# Copy to input folder
cp ~/Downloads/VoiceMemos/*.m4a input/

# Verify they're there
ls input/*.m4a | wc -l
```

### Step 2: Process Backlog

```bash
# This transcribes ALL files in input/
python scripts/batch_transcribe.py

# Takes ~1-2 hours for 100-200 memos
# Progress shown in terminal
```

**What it creates:**
- `output/transcripts/` — All transcripts
- `output/analysis/` — Speech pathology findings
- `output/index.json` — Searchable index
- `.transcription_tracker.json` — Tracks what's done

### Step 3: Set Up Daily Cron

```bash
# Interactive setup
python scripts/setup_daily_cron.py

# It will ask:
# • What time daily? (default: 02:00)
# • GitHub repo? (optional, for backup)
# • GitHub token? (optional, for backup)
```

**Example:**
```
Setting up daily voice memo workflow...

What time should daily sync run?
Format: HH:MM (24-hour, e.g., 02:00 for 2 AM)
Time [02:00]: 02:00

GitHub Configuration (optional)
Skip if you don't want automatic GitHub backup
GitHub repo [skip]: libbynatico/voice-memo-transcription
GitHub token: ghp_...

✓ Daily cron job installed!
  Time: 02:00 (every day)
  Logs: /path/to/voice-memo-transcription/logs/cron.log
  GitHub: libbynatico/voice-memo-transcription
```

---

## How It Works Daily

### The iMazing Integration

iMazing allows automated export of iPhone data via command line.

**How it's used:**
```bash
/Applications/iMazing.app/Contents/MacOS/iMazing --exportVoiceMemos input/
```

This syncs **only new** Voice Memos from your iPhone to the `input/` folder.

**Your iPhone stays connected?** No. iMazing can work over USB or WiFi, but the sync is quick (~30 seconds).

### Incremental Tracking

The system tracks which memos have been processed using `.transcription_tracker.json`:

```json
{
  "processed_files": {
    "2026-04-06_osteopathy_visit.m4a": {
      "processed": "2026-04-06T14:30:00",
      "hash": "a1b2c3d4e5...",
      "mtime": 1712433000
    }
  }
}
```

**Result:** Each memo transcribed exactly once, even if cron runs multiple times.

### Daily Workflow Log

Every run logs to `logs/daily_workflow.log`:

```json
{"timestamp": "2026-04-07T02:00:15", "memos_processed": 3, "success": true}
{"timestamp": "2026-04-08T02:00:12", "memos_processed": 0, "success": true}
{"timestamp": "2026-04-09T02:00:18", "memos_processed": 2, "success": true}
```

**Check it anytime:**
```bash
cat logs/daily_workflow.log | tail -10
```

---

## Managing the Workflow

### Check Cron Status

```bash
# Show installed cron job
python scripts/setup_daily_cron.py --status

# Output:
# ✓ Daily cron job is installed:
#   0 2 * * * cd /path/to/... && python3 daily_workflow.py ...
```

### View Logs

```bash
# Last 20 runs
tail -20 logs/daily_workflow.log

# Last 50 lines of full cron output
tail -50 logs/cron.log

# Watch in real-time (if it's running)
tail -f logs/cron.log
```

### Disable Cron (Pause Automation)

```bash
python scripts/setup_daily_cron.py --disable

# Re-enable anytime
python scripts/setup_daily_cron.py
```

### Run Manually (Override Cron)

```bash
# Run now, skip iMazing (use files in input/)
python scripts/daily_workflow.py --skip-imazing

# Run with GitHub backup
python scripts/daily_workflow.py \
  --repo libbynatico/voice-memo-transcription \
  --token ghp_YOUR_TOKEN

# Dry-run (show what would happen, don't execute)
python scripts/daily_workflow.py --dry-run
```

---

## What Gets Backed Up to GitHub

After each daily run, if GitHub is configured, the system pushes:

```
output/
├── transcripts/          ← All .txt files with transcriptions
├── analysis/             ← All .json files with SLP analysis
├── metadata/             ← Speaker data and diarization
├── index.json            ← Master searchable index
└── [date]/               ← Timestamped runs
```

**GitHub is your permanent archive.** Every transcript and analysis is backed up automatically.

---

## Integration with Medical Files

### Using Transcripts in ODSP/OW Applications

1. **Evidence of communication ability**
   - Upload SLP analysis JSON
   - Shows intelligibility, clarity, cognition

2. **Functional impairment documentation**
   - Prosody and fatigue markers
   - Word-finding difficulties
   - Effort language

3. **Timeline documentation**
   - Every memo is date-stamped
   - Shows changes over time

### SLP Integration

The analysis JSON is clinical-grade:

```json
{
  "prosody": {
    "filled_pauses": 8,
    "word_repetitions": 3
  },
  "intelligibility": {
    "clarity_score": "high"
  },
  "fatigue_markers": {
    "effort_language": 2
  },
  "tbi_patterns": {
    "word_finding_pauses": 5,
    "topic_maintenance": "high"
  }
}
```

You can share this directly with:
- Your SLP
- Medical clinicians
- Disability assessment teams

---

## Troubleshooting

### iMazing Sync Failing

```bash
# List connected devices
python scripts/imazing_sync.py --list-devices

# Manual sync with specific device
python scripts/imazing_sync.py --device YOUR_DEVICE_ID
```

**If iMazing not found:**
1. Install iMazing: https://imazing.com/download
2. Or skip iMazing: `python scripts/daily_workflow.py --skip-imazing`

### No New Memos Found

```bash
# Check tracker
cat .transcription_tracker.json | python -m json.tool

# Reset tracker (reprocess everything)
python scripts/transcription_tracker.py --reset
```

### GitHub Push Failing

```bash
# Check repo is private
# https://github.com/libbynatico/voice-memo-transcription/settings

# Verify token is valid
# https://github.com/settings/tokens

# Retry push
python scripts/push_to_github.py \
  --repo libbynatico/voice-memo-transcription \
  --token ghp_YOUR_TOKEN
```

### Cron Not Running

```bash
# Check cron logs
tail logs/cron.log

# Verify cron is installed
python scripts/setup_daily_cron.py --status

# Test manually
python scripts/daily_workflow.py --skip-imazing
```

---

## File Locations Reference

```
voice-memo-transcription/
├── input/                      ← Drop .m4a files here (or iMazing syncs)
├── output/
│   ├── transcripts/            ← Generated transcript files
│   ├── analysis/               ← SLP analysis JSON
│   ├── metadata/               ← Speaker diarization
│   └── index.json              ← Master index (searchable)
├── logs/
│   ├── cron.log                ← Cron execution log
│   └── daily_workflow.log       ← Workflow run history
├── .transcription_tracker.json  ← Tracks processed files
├── scripts/
│   ├── daily_workflow.py       ← Main daily orchestration
│   ├── imazing_sync.py         ← iMazing integration
│   ├── batch_transcribe.py     ← Transcription engine
│   ├── slp_analyzer.py         ← Speech analysis
│   ├── transcription_tracker.py ← Incremental tracking
│   ├── push_to_github.py       ← GitHub backup
│   └── setup_daily_cron.py     ← Cron configuration
└── README.md, QUICKSTART.md, MANIFEST.json
```

---

## Complete Workflow Timeline

**Example 7-day cycle:**

```
Monday 12:00 PM
└─ Record new voice memo (osteopathy visit)
   (stays in Voice Memos app on iPhone)

Tuesday 2:00 AM [CRON RUNS]
├─ iMazing syncs → input/osteopathy_visit.m4a
├─ Transcripts + analyzes
├─ Updates index.json
└─ Pushes to GitHub
   ✓ Transcript in output/transcripts/
   ✓ Analysis in output/analysis/
   ✓ GitHub backup complete

Wednesday-Thursday
└─ No new memos, no cron action

Friday 3:00 PM
└─ Record two more memos (medical appointment, personal note)

Saturday 2:00 AM [CRON RUNS]
├─ iMazing syncs → input/medical_apt.m4a, personal_note.m4a
├─ Transcribes both (skips Monday's, already done)
├─ Updates index
└─ Pushes to GitHub
   ✓ 2 new transcripts added
   ✓ Index now shows 3 total memos

Check status anytime:
└─ cat logs/daily_workflow.log
└─ ls output/transcripts/ | wc -l
└─ cat output/index.json
```

---

## Questions?

See:
- **README.md** — Full system documentation
- **QUICKSTART.md** — Fast start guide
- **MANIFEST.json** — System inventory

---

**Built:** April 6, 2026  
**For:** Matthew Herbert  
**System:** Voice Memo Transcription + iMazing + Daily Cron + SLP Analysis


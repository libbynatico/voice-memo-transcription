# Voice Memo Transcription System

**Complete free workflow to transcribe 100-200+ iOS voice memos with speaker identification, SLP analysis, and GitHub integration.**

## What This Does

- **Batch transcribes** all your voice memos (Voice Memo app or Apple Notes audio)
- **Identifies speakers** (Matthew, Kellsie, Eric, etc.) automatically
- **Analyzes speech** pathology markers (prosody, intelligibility, fatigue, TBI patterns)
- **Organizes output** (indexed, searchable, clinical-ready)
- **Pushes to GitHub** automatically
- **Runs monthly** to capture new memos

## Cost

**$0** — Uses free Whisper AI + pyannote speaker diarization

## Setup (Mac)

### Step 1: Install Python Dependencies (5 minutes)

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and ffmpeg
brew install python@3.11 ffmpeg

# Clone/download this repo and install Python packages
cd voice-memo-transcription
pip install -r requirements.txt
```

### Step 2: Export Your Voice Memos (10 minutes)

1. On your iPhone:
   - Open Voice Memos app
   - Select all memos (swipe left, select)
   - Tap "Share" → "Save to Files" → choose a folder
   
2. Transfer to Mac:
   - Use AirDrop, iCloud Drive, or email them to yourself
   - Save all .m4a files to `/voice-memo-transcription/input/`

### Step 3: Run Transcription (depends on count, typically 30 min - 2 hours)

```bash
python scripts/batch_transcribe.py
```

This will:
- Transcribe all .m4a files
- Identify speakers
- Analyze speech patterns
- Create organized output folder

### Step 4: Review & Organize Output

```bash
ls output/
```

You'll see:
- `transcripts/` — All cleaned transcripts with speaker labels
- `analysis/` — SLP analysis (prosody, intelligibility, fatigue markers)
- `index.json` — Searchable index of all memos
- `metadata/` — Speaker summaries, clinical markers

### Step 5: Push to GitHub

```bash
# First time only: create GitHub repo (see setup instructions below)

# Then run automation:
python scripts/push_to_github.py --repo libbynatico/voice-memo-transcription --token YOUR_GITHUB_TOKEN
```

## GitHub Setup (First Time)

1. Go to: https://github.com/new
2. Create repo: `voice-memo-transcription`
3. Make it **Private** (for medical data)
4. Run: `python scripts/push_to_github.py --init`

## Ongoing (Monthly Updates)

```bash
# Set up monthly cron job (automatic):
python scripts/setup_cron.py

# Or run manually anytime:
python scripts/batch_transcribe.py
python scripts/push_to_github.py
```

## Output Structure

```
output/
├── transcripts/
│   ├── 2026-04-06_osteopathy_visit.txt
│   ├── 2026-03-15_personal_note.txt
│   └── ...
├── analysis/
│   ├── slp_analysis_batch.json
│   ├── speaker_profiles.json
│   └── clinical_markers.json
├── index.json
└── metadata/
    ├── speaker_diarization.json
    └── file_manifest.json
```

## What the SLP Analysis Captures

- **Prosody** — Rate, rhythm, intonation, phrasing
- **Intelligibility** — Speech clarity, articulation quality
- **Fatigue markers** — Voice changes, effort, breaks
- **TBI patterns** — Word retrieval, fluency, coherence
- **Cognitive markers** — Memory, processing speed, topic maintenance
- **Speaker identification** — Who's talking, turn-taking patterns

## GitHub Storage

All output syncs to private GitHub repo. Files include:
- Full transcripts (searchable)
- SLP analysis JSON (for future clinician review)
- Index with dates, speakers, clinical relevance
- Metadata for integration with medical records

## Troubleshooting

**"No module named 'whisper'"**
```bash
pip install openai-whisper
```

**"ffmpeg not found"**
```bash
brew install ffmpeg
```

**"Permission denied" on cron job**
```bash
chmod +x scripts/setup_cron.py
```

## Questions?

See `docs/FAQ.md` for full troubleshooting guide.

---

**Built for: Matthew Herbert**  
**System Version: 1.0**  
**Last Updated: April 6, 2026**

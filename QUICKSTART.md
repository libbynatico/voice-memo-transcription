# Voice Memo Transcription - QUICK START GUIDE

**Your system is ready. 5-minute setup:**

## 1. Get Python Dependencies (One-time, 5 min)

On your Mac, open Terminal and run:

```bash
# Copy this entire block and paste into Terminal
pip install openai-whisper pyannote.audio torch pydub requests PyGithub

# This installs all free transcription tools
```

Done! You now have:
- **Whisper** — Free speech-to-text (OpenAI's model, runs locally)
- **pyannote** — Free speaker identification (who's talking)
- **Python scripts** — Automated processing

## 2. Clone Your GitHub Repo

```bash
git clone https://github.com/libbynatico/voice-memo-transcription.git
cd voice-memo-transcription
```

This downloads the complete system to your Mac.

## 3. Export Your Voice Memos from iPhone

1. Open **Voice Memos** app on your iPhone
2. Long-press to select all memos
3. Tap **Share** → **Save to Files** → create folder or use existing
4. Transfer via:
   - **AirDrop** to Mac
   - **iCloud Drive** (iCloud.com/Files)
   - **Email to yourself**
5. Save all .m4a files to: `voice-memo-transcription/input/`

## 4. Run Transcription

```bash
cd voice-memo-transcription
python3 scripts/batch_transcribe.py
```

**What happens:**
- Whisper processes each memo (1-2 min per memo, runs in background)
- Identifies speakers (Matthew, Kellsie, Eric, etc.)
- Analyzes speech patterns (prosody, fatigue, TBI markers)
- Saves all transcripts to `output/transcripts/`
- Creates searchable index

**Time:** ~30 min - 2 hours (depends on number of memos + your Mac)

## 5. Review Output

When done, check your results:

```bash
ls output/transcripts/          # All transcripts
ls output/analysis/             # Clinical analysis
cat output/index.json           # Search index
```

Each transcript includes:
- Full transcription
- Speaker identification
- Speech analysis

## 6. Push to GitHub (Backup)

```bash
python3 scripts/push_to_github.py \
  --repo libbynatico/voice-memo-transcription \
  --token YOUR_GITHUB_TOKEN
```

(Replace YOUR_GITHUB_TOKEN with: `YOUR_GITHUB_TOKEN`)

**What this does:**
- Backs up all transcripts to private GitHub repo
- Creates searchable archive
- You can share with clinicians later

## 7. Ongoing (Monthly)

Set up automatic monthly transcription:

```bash
python3 scripts/setup_cron.py
```

This will automatically run transcription on the 1st of each month.

---

## If Something Breaks

**"No module named whisper"**
```bash
pip install openai-whisper
```

**"ffmpeg not found"**
```bash
brew install ffmpeg
```

**"Permission denied"**
```bash
chmod +x scripts/*.py
```

**"No audio files found"**
- Check your input folder: `voice-memo-transcription/input/`
- Make sure .m4a files are there
- Run again: `python3 scripts/batch_transcribe.py`

---

## What Happens to Your Data?

✓ **Stays on your Mac** — Transcription runs locally
✓ **Private GitHub repo** — Only you can see it
✓ **No cost** — Uses free Whisper AI
✗ **Not uploaded anywhere** except your GitHub

---

## Output Details

Each transcript will show:

```
File: 2026-04-06_osteopathy_visit
Processed: 2026-04-06T14:30:00

--- TRANSCRIPT ---
[Full transcription of what was said]

--- SPEAKER IDENTIFICATION ---
{
  "Speaker_1": [...], 
  "Speaker_2": [...]
}
```

And clinical analysis includes:
- Word retrieval patterns
- Fatigue markers
- Speech clarity
- TBI indicators
- Cognitive load assessment

---

## Next Steps

1. **Export your memos** to `input/` folder
2. **Run batch_transcribe.py**
3. **Review output**
4. **Push to GitHub** for backup
5. **Share transcripts with clinicians** as needed

**Questions?** See full README.md in repo

---

**Built for: Matthew Herbert**
**System: voice-memo-transcription**
**Cost: $0 (free tools only)**

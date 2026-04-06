# Quick Start Guide — Voice Memo Transcription System

**Start here if you want to run this NOW, not read documentation.**

---

## What You'll Do (5 Steps)

1. ✅ **Install Python packages** (1 minute)
2. ✅ **Export your voice memos from iPhone** (5 minutes)
3. ✅ **Run the transcription** (30 min to 2 hours, depending on memo count)
4. ✅ **Review output** (5 minutes)
5. ✅ **Push to GitHub** (2 minutes)

---

## Step 1: Install Python Packages

**On your Mac, open Terminal and run:**

```bash
# Navigate to the project folder
cd /path/to/voice-memo-transcription

# Install dependencies (one time)
pip install -r requirements.txt
```

**Takes ~2 minutes.** You'll see a bunch of text scrolling — that's normal.

If you get `pip: command not found`, install Homebrew first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.11
```

---

## Step 2: Export Voice Memos from iPhone

**On your iPhone:**

1. Open **Voice Memos** app
2. **Swipe left** on all memos to select them
3. Tap **Share** → **Save to Files**
4. Choose a folder (create one called "VoiceMemos")
5. Transfer folder to Mac via:
   - AirDrop (easiest)
   - Email (select all, share)
   - iCloud Drive sync

**On your Mac:**

```bash
# Copy all .m4a files into the input folder
cp ~/Downloads/VoiceMemos/*.m4a voice-memo-transcription/input/
```

---

## Step 3: Run Transcription

**In Terminal:**

```bash
cd /path/to/voice-memo-transcription
python scripts/batch_transcribe.py
```

**What happens:**
- Whisper transcribes each memo (~2-5 min per memo)
- Speaker diarization identifies who's talking
- SLP analysis checks speech patterns
- Output saved to `output/` folder

**Progress:** You'll see status like:
```
[1/150] Processing: 2026-04-06_osteopathy_visit
  Converting: input/osteo.m4a → wav
  Transcribing: input/osteo.wav
  Diarizing speakers: ...
  Analyzing speech patterns...
```

---

## Step 4: Review Output

**When done, check the results:**

```bash
# See all transcripts
ls output/transcripts/

# See analysis files
ls output/analysis/

# See searchable index
cat output/index.json
```

**Each memo gets:**
- `transcript.txt` — What was said (with speaker labels if available)
- `analysis.json` — SLP findings (prosody, fatigue, TBI markers, etc.)

---

## Step 5: Push to GitHub

**First time only:**

```bash
# Set up GitHub authentication
python scripts/push_to_github.py --init
```

This will show you how to create a GitHub token (takes 60 seconds).

**Then run:**

```bash
python scripts/push_to_github.py \
  --repo libbynatico/voice-memo-transcription \
  --token ghp_YOUR_TOKEN_HERE
```

(Replace `ghp_YOUR_TOKEN_HERE` with your actual token)

**What happens:**
- All transcripts & analysis pushed to your private GitHub repo
- You can access them anytime from any device
- Creates automatic backup of your medical data

---

## Future Runs (Monthly)

**After the first run, you can:**

**Option A: Run manually whenever**
```bash
python scripts/batch_transcribe.py
python scripts/push_to_github.py --repo libbynatico/voice-memo-transcription --token YOUR_TOKEN
```

**Option B: Set up automatic monthly updates**
```bash
python scripts/setup_cron.py
```

This runs transcription automatically on the **1st of each month at 2:00 AM**.

Check logs:
```bash
tail logs/cron.log
```

---

## Troubleshooting

**"command not found: python"**
```bash
python3 scripts/batch_transcribe.py
# OR
brew install python@3.11
```

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
# Try again
```

**Transcription is very slow**
- This is normal. Whisper processes 1-2 min of audio per minute of transcription.
- 100 memos = 1-2 hours total. Let it run.

**"ffmpeg not found"**
```bash
brew install ffmpeg
```

**Can't push to GitHub**
- Check your token is valid: https://github.com/settings/tokens
- Confirm repo exists: github.com/libbynatico/voice-memo-transcription
- Make it Private (Settings → Access)

---

## What's Next?

Once transcripts are in GitHub:

1. **SLP clinical review** — Send analysis.json to your speech pathologist
2. **Medical records integration** — Use transcripts in disability/medical filings
3. **Evidence archive** — All voice memos permanently backed up
4. **Search & retrieve** — index.json is searchable (grep, search tools)

---

## Questions?

See `README.md` for full documentation.


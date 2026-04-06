#!/usr/bin/env python3
"""
Batch transcribe all voice memos with speaker diarization and SLP analysis.
Supports: .m4a, .wav, .mp3, .aac (iOS Voice Memos)
"""

import os
import json
import whisper
from pathlib import Path
from datetime import datetime
import subprocess
from slp_analyzer import SLPAnalyzer

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
TRANSCRIPTS_DIR = os.path.join(OUTPUT_DIR, 'transcripts')
ANALYSIS_DIR = os.path.join(OUTPUT_DIR, 'analysis')
METADATA_DIR = os.path.join(OUTPUT_DIR, 'metadata')

def setup_directories():
    """Create output directories if they don't exist."""
    for d in [OUTPUT_DIR, TRANSCRIPTS_DIR, ANALYSIS_DIR, METADATA_DIR]:
        os.makedirs(d, exist_ok=True)

def convert_to_wav(audio_path):
    """Convert .m4a or other formats to .wav for processing."""
    wav_path = audio_path.replace(audio_path.split('.')[-1], 'wav')
    if not os.path.exists(wav_path):
        try:
            # Use ffmpeg to convert
            subprocess.run([
                'ffmpeg', '-i', audio_path, '-acodec', 'pcm_s16le', 
                '-ar', '16000', wav_path, '-y'
            ], capture_output=True)
            print(f"  Converted: {audio_path} → {wav_path}")
        except Exception as e:
            print(f"  Error converting {audio_path}: {e}")
            return None
    return wav_path

def transcribe_audio(audio_path):
    """Transcribe audio using Whisper."""
    print(f"  Transcribing: {audio_path}")
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result['text']
    except Exception as e:
        print(f"  Error transcribing {audio_path}: {e}")
        return None

def diarize_speakers(audio_path):
    """Identify speakers in audio (Matthew, Kellsie, Eric, etc.)."""
    print(f"  Diarizing speakers: {audio_path}")
    try:
        from pyannote.audio import Pipeline
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.0")
        diarization = pipeline(audio_path)
        
        speakers = {}
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker_id = f"Speaker_{speaker}"
            if speaker_id not in speakers:
                speakers[speaker_id] = []
            speakers[speaker_id].append({
                'start': turn.start,
                'end': turn.end,
                'duration': turn.end - turn.start
            })
        return speakers
    except Exception as e:
        print(f"  Note: Speaker diarization requires pyannote auth token. Skipping: {e}")
        return None

def analyze_speech_patterns(transcript, speakers=None):
    """Run SLP analysis on transcript."""
    print(f"  Analyzing speech patterns...")
    analyzer = SLPAnalyzer()
    return analyzer.analyze(transcript, speakers)

def process_memo(audio_path):
    """Process a single voice memo."""
    filename = Path(audio_path).stem
    print(f"\nProcessing: {filename}")
    
    # Convert to WAV if needed
    if audio_path.endswith('.m4a'):
        wav_path = convert_to_wav(audio_path)
        if not wav_path:
            return None
    else:
        wav_path = audio_path
    
    # Transcribe
    transcript = transcribe_audio(wav_path)
    if not transcript:
        return None
    
    # Speaker diarization
    speakers = diarize_speakers(wav_path)
    
    # SLP analysis
    analysis = analyze_speech_patterns(transcript, speakers)
    
    # Save transcript
    transcript_file = os.path.join(TRANSCRIPTS_DIR, f"{filename}_transcript.txt")
    with open(transcript_file, 'w') as f:
        f.write(f"File: {filename}\n")
        f.write(f"Processed: {datetime.now().isoformat()}\n\n")
        f.write("--- TRANSCRIPT ---\n")
        f.write(transcript)
        if speakers:
            f.write("\n\n--- SPEAKER IDENTIFICATION ---\n")
            f.write(json.dumps(speakers, indent=2))
    
    # Save analysis
    analysis_file = os.path.join(ANALYSIS_DIR, f"{filename}_analysis.json")
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    return {
        'filename': filename,
        'transcript_file': transcript_file,
        'analysis_file': analysis_file,
        'speakers': speakers,
        'analysis': analysis
    }

def create_index(results):
    """Create searchable index of all transcripts."""
    print("\nCreating index...")
    index = {
        'created': datetime.now().isoformat(),
        'total_memos': len(results),
        'memos': []
    }
    
    for result in results:
        if result:
            index['memos'].append({
                'filename': result['filename'],
                'transcript_path': result['transcript_file'],
                'analysis_path': result['analysis_file'],
                'speakers': list(result['speakers'].keys()) if result['speakers'] else [],
                'processed': datetime.now().isoformat()
            })
    
    index_file = os.path.join(OUTPUT_DIR, 'index.json')
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)
    
    return index

def main():
    """Main batch processing workflow."""
    setup_directories()
    
    # Find all audio files
    audio_files = []
    for ext in ['*.m4a', '*.wav', '*.mp3', '*.aac']:
        audio_files.extend(Path(INPUT_DIR).glob(ext))
    
    if not audio_files:
        print(f"No audio files found in {INPUT_DIR}/")
        return
    
    print(f"\nFound {len(audio_files)} audio files to process\n")
    
    results = []
    for i, audio_file in enumerate(audio_files, 1):
        print(f"[{i}/{len(audio_files)}]", end=' ')
        result = process_memo(str(audio_file))
        results.append(result)
    
    # Create searchable index
    index = create_index(results)
    
    print(f"\n✓ Processing complete!")
    print(f"  Transcripts: {TRANSCRIPTS_DIR}/")
    print(f"  Analysis: {ANALYSIS_DIR}/")
    print(f"  Index: {os.path.join(OUTPUT_DIR, 'index.json')}")
    print(f"  Total processed: {len([r for r in results if r])}")

if __name__ == '__main__':
    main()

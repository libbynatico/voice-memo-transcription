#!/usr/bin/env python3
"""
Track which voice memos have been transcribed to enable incremental processing.
Prevents re-transcribing the same memo multiple times.
"""

import json
import os
import hashlib
from pathlib import Path
from datetime import datetime

TRACKER_FILE = '.transcription_tracker.json'

class TranscriptionTracker:
    """Track processed memos to enable incremental transcription."""
    
    def __init__(self):
        self.data = self._load_tracker()
    
    def _load_tracker(self):
        """Load existing tracker data."""
        if os.path.exists(TRACKER_FILE):
            try:
                with open(TRACKER_FILE, 'r') as f:
                    return json.load(f)
            except:
                return self._create_empty_tracker()
        return self._create_empty_tracker()
    
    def _create_empty_tracker(self):
        """Create new tracker structure."""
        return {
            'version': '1.0',
            'created': datetime.now().isoformat(),
            'last_update': datetime.now().isoformat(),
            'processed_files': {},
            'stats': {
                'total_processed': 0,
                'total_new': 0,
                'last_run': None
            }
        }
    
    def _get_file_hash(self, filepath):
        """Create hash of file for change detection."""
        hash_md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _get_file_mtime(self, filepath):
        """Get file modification time."""
        return os.path.getmtime(filepath)
    
    def get_new_files(self, input_dir='input'):
        """Find files that haven't been transcribed yet."""
        new_files = []
        
        for audio_file in Path(input_dir).glob('*.m4a'):
            filepath = str(audio_file)
            filename = audio_file.name
            
            if filename not in self.data['processed_files']:
                new_files.append(filepath)
            else:
                # Check if file has changed
                stored_hash = self.data['processed_files'][filename].get('hash')
                current_hash = self._get_file_hash(filepath)
                
                if stored_hash != current_hash:
                    print(f"  File changed: {filename} (will re-transcribe)")
                    new_files.append(filepath)
        
        return new_files
    
    def mark_processed(self, filepath):
        """Mark a file as successfully transcribed."""
        filename = Path(filepath).name
        
        self.data['processed_files'][filename] = {
            'processed': datetime.now().isoformat(),
            'hash': self._get_file_hash(filepath),
            'mtime': self._get_file_mtime(filepath)
        }
        
        self.data['last_update'] = datetime.now().isoformat()
        self.data['stats']['total_processed'] += 1
        
        self._save_tracker()
    
    def get_stats(self):
        """Get processing statistics."""
        return {
            'total_processed': self.data['stats']['total_processed'],
            'files_processed': len(self.data['processed_files']),
            'last_update': self.data['last_update']
        }
    
    def reset(self):
        """Clear all tracking data (fresh start)."""
        self.data = self._create_empty_tracker()
        self._save_tracker()
        print("✓ Tracker reset")
    
    def _save_tracker(self):
        """Save tracker to file."""
        with open(TRACKER_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)


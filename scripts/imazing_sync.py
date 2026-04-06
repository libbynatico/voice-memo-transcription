#!/usr/bin/env python3
"""
iMazing integration for automatic voice memo export.
Syncs voice memos from iPhone to Mac via iMazing command-line.
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

IMAZING_PATH = "/Applications/iMazing.app/Contents/MacOS/iMazing"
OUTPUT_DIR = "input"
SYNC_LOG = ".imazing_sync_log.json"

def check_imazing_installed():
    """Verify iMazing is installed."""
    if not os.path.exists(IMAZING_PATH):
        print("❌ iMazing not found at /Applications/iMazing.app")
        print("\nTo use this script, install iMazing:")
        print("  https://imazing.com/download")
        return False
    return True

def get_connected_devices():
    """List connected iOS devices."""
    try:
        result = subprocess.run(
            [IMAZING_PATH, '--listDevices'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
    except Exception as e:
        print(f"Error listing devices: {e}")
    return []

def sync_voice_memos(device_id=None):
    """Export voice memos from iPhone using iMazing."""
    print("Syncing voice memos from iPhone...")
    
    if not check_imazing_installed():
        return False
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        # Build iMazing export command
        cmd = [
            IMAZING_PATH,
            '--exportVoiceMemos',
            OUTPUT_DIR
        ]
        
        if device_id:
            cmd.extend(['--device', device_id])
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Voice memos synced successfully")
            log_sync()
            return True
        else:
            print(f"❌ Sync failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during sync: {e}")
        return False

def log_sync():
    """Log successful sync for incremental tracking."""
    log_data = {
        'last_sync': datetime.now().isoformat(),
        'timestamp': datetime.now().timestamp()
    }
    
    with open(SYNC_LOG, 'w') as f:
        json.dump(log_data, f)
    
    print(f"Sync logged: {log_data['last_sync']}")

def get_new_memos():
    """Get list of new memos added since last sync."""
    try:
        if os.path.exists(SYNC_LOG):
            with open(SYNC_LOG, 'r') as f:
                log_data = json.load(f)
                last_sync = log_data['timestamp']
        else:
            last_sync = 0
    except:
        last_sync = 0
    
    new_memos = []
    for audio_file in Path(OUTPUT_DIR).glob('*.m4a'):
        if os.path.getmtime(audio_file) > last_sync:
            new_memos.append(str(audio_file))
    
    return new_memos

def main():
    """Main sync workflow."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sync voice memos via iMazing')
    parser.add_argument('--list-devices', action='store_true', help='Show connected devices')
    parser.add_argument('--device', help='Device ID to sync from')
    parser.add_argument('--auto', action='store_true', help='Sync and return count of new memos')
    
    args = parser.parse_args()
    
    if args.list_devices:
        devices = get_connected_devices()
        print("Connected devices:")
        for device in devices:
            print(f"  {device}")
        return
    
    if not check_imazing_installed():
        sys.exit(1)
    
    # Perform sync
    success = sync_voice_memos(args.device)
    
    if success and args.auto:
        new_memos = get_new_memos()
        print(f"\nNew memos: {len(new_memos)}")
        for memo in new_memos:
            print(f"  {memo}")
        sys.exit(0 if len(new_memos) > 0 else 1)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()


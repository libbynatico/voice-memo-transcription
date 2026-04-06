#!/usr/bin/env python3
"""
Set up monthly cron job to automatically transcribe new voice memos.
macOS only.
"""

import os
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = os.path.abspath('scripts/batch_transcribe.py')
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_PATH))

def setup_cron():
    """Add monthly cron job to transcribe new memos."""
    
    cron_command = f'''
cd {PROJECT_DIR} && /usr/bin/python3 {SCRIPT_PATH} >> logs/cron.log 2>&1
'''
    
    # Create logs directory
    os.makedirs(f'{PROJECT_DIR}/logs', exist_ok=True)
    
    # Create crontab entry (runs on first day of month at 2 AM)
    cron_entry = f"0 2 1 * * {cron_command}\n"
    
    try:
        # Get current crontab
        result = subprocess.run(
            'crontab -l',
            shell=True,
            capture_output=True,
            text=True
        )
        current_cron = result.stdout if result.returncode == 0 else ""
    except:
        current_cron = ""
    
    # Add new entry if not already present
    if SCRIPT_PATH not in current_cron:
        new_cron = current_cron + cron_entry
        
        # Write to temp file
        with open('/tmp/crontab_temp', 'w') as f:
            f.write(new_cron)
        
        # Install crontab
        subprocess.run('crontab /tmp/crontab_temp', shell=True)
        os.remove('/tmp/crontab_temp')
        
        print("✓ Monthly cron job installed")
        print(f"  Runs on: 1st day of each month at 2:00 AM")
        print(f"  Script: {SCRIPT_PATH}")
        print(f"  Logs: {PROJECT_DIR}/logs/cron.log")
    else:
        print("✓ Cron job already installed")

def disable_cron():
    """Remove the cron job."""
    try:
        result = subprocess.run(
            'crontab -l',
            shell=True,
            capture_output=True,
            text=True
        )
        current_cron = result.stdout
        
        # Remove lines containing our script
        new_cron = '\n'.join(
            line for line in current_cron.split('\n')
            if SCRIPT_PATH not in line
        )
        
        # Write back
        with open('/tmp/crontab_temp', 'w') as f:
            f.write(new_cron)
        
        subprocess.run('crontab /tmp/crontab_temp', shell=True)
        os.remove('/tmp/crontab_temp')
        
        print("✓ Cron job removed")
    except:
        print("Error removing cron job")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--disable':
        disable_cron()
    else:
        setup_cron()


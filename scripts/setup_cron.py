#!/usr/bin/env python3
"""
Set up monthly cron job for ongoing voice memo transcription.
Runs automatically on the 1st of each month.
"""

import os
import subprocess
import sys

def setup_cron(repo_path):
    """Create cron job for monthly transcription."""
    
    # Create cron command
    cron_command = f"""
# Voice Memo Transcription - Monthly Update (1st of each month at 8 AM)
0 8 1 * * cd {repo_path} && python3 scripts/batch_transcribe.py && python3 scripts/push_to_github.py
"""
    
    # Add to crontab
    print("Setting up monthly cron job...")
    print("This will run transcription on the 1st of each month at 8 AM")
    
    try:
        # Get current crontab
        result = subprocess.run('crontab -l', shell=True, capture_output=True, text=True)
        current_cron = result.stdout if result.returncode == 0 else ""
        
        # Add new cron job
        new_cron = current_cron + cron_command
        
        # Write back to crontab
        process = subprocess.Popen('crontab -', stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_cron)
        
        print("✓ Cron job configured")
        print(f"  Scheduled: Monthly on the 1st at 8 AM")
        print(f"  Run manually anytime: cd {repo_path} && python3 scripts/batch_transcribe.py")
    except Exception as e:
        print(f"Note: Could not set up cron automatically: {e}")
        print(f"Manual setup: crontab -e and add:")
        print(cron_command)

if __name__ == '__main__':
    repo_path = os.getcwd()
    setup_cron(repo_path)

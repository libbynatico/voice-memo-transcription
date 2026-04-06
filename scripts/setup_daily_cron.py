#!/usr/bin/env python3
"""
Set up daily automated workflow with cron.
Runs every day at specified time, syncs new memos, transcribes, and pushes to GitHub.
"""

import os
import subprocess
import sys
import getpass
from pathlib import Path

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_PATH = os.path.join(PROJECT_DIR, 'scripts', 'daily_workflow.py')

def get_cron_time():
    """Get time from user for daily cron job."""
    print("\nWhat time should daily sync run?")
    print("Format: HH:MM (24-hour, e.g., 02:00 for 2 AM)")
    
    while True:
        time_str = input("Time [02:00]: ").strip() or "02:00"
        try:
            hour, minute = map(int, time_str.split(':'))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return hour, minute
        except:
            pass
        print("Invalid format. Use HH:MM (e.g., 14:30)")

def get_github_credentials():
    """Get GitHub repo and token."""
    print("\nGitHub Configuration (optional)")
    print("Skip if you don't want automatic GitHub backup")
    
    repo = input("GitHub repo [skip]: ").strip() or None
    if repo:
        token = getpass.getpass("GitHub token: ")
        return repo, token
    return None, None

def setup_cron(hour, minute, repo=None, token=None):
    """Create cron job."""
    
    # Build command
    cmd = f'python3 {SCRIPT_PATH}'
    if repo and token:
        cmd += f' --repo {repo} --token {token}'
    
    cron_line = f'{minute} {hour} * * * cd {PROJECT_DIR} && {cmd} >> logs/cron.log 2>&1\n'
    
    # Get current crontab
    try:
        result = subprocess.run('crontab -l', shell=True, capture_output=True, text=True)
        current_cron = result.stdout if result.returncode == 0 else ""
    except:
        current_cron = ""
    
    # Check if already installed
    if SCRIPT_PATH in current_cron:
        print("✓ Daily cron job already installed")
        return True
    
    # Add new entry
    new_cron = current_cron + cron_line
    
    # Write to temp file and install
    try:
        with open('/tmp/crontab_new', 'w') as f:
            f.write(new_cron)
        
        subprocess.run('crontab /tmp/crontab_new', shell=True, check=True)
        os.remove('/tmp/crontab_new')
        
        print(f"\n✓ Daily cron job installed!")
        print(f"  Time: {hour:02d}:{minute:02d} (every day)")
        print(f"  Script: {SCRIPT_PATH}")
        print(f"  Logs: {PROJECT_DIR}/logs/cron.log")
        if repo:
            print(f"  GitHub: {repo}")
        
        return True
    except Exception as e:
        print(f"❌ Error installing cron: {e}")
        return False

def disable_cron():
    """Remove daily cron job."""
    try:
        result = subprocess.run('crontab -l', shell=True, capture_output=True, text=True)
        current_cron = result.stdout
        
        # Remove lines containing our script
        new_cron = '\n'.join(
            line for line in current_cron.split('\n')
            if SCRIPT_PATH not in line
        )
        
        with open('/tmp/crontab_new', 'w') as f:
            f.write(new_cron)
        
        subprocess.run('crontab /tmp/crontab_new', shell=True)
        os.remove('/tmp/crontab_new')
        
        print("✓ Daily cron job removed")
        return True
    except:
        print("❌ Error removing cron job")
        return False

def show_cron_status():
    """Show current cron job status."""
    try:
        result = subprocess.run('crontab -l', shell=True, capture_output=True, text=True)
        if SCRIPT_PATH in result.stdout:
            print("\n✓ Daily cron job is installed:")
            for line in result.stdout.split('\n'):
                if SCRIPT_PATH in line:
                    print(f"  {line}")
        else:
            print("\nℹ No daily cron job installed")
    except:
        print("\nℹ Unable to read cron status")

def main():
    """Setup or manage daily cron."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Set up daily voice memo workflow')
    parser.add_argument('--disable', action='store_true', help='Remove cron job')
    parser.add_argument('--status', action='store_true', help='Show cron status')
    parser.add_argument('--time', help='Cron time (HH:MM format)')
    parser.add_argument('--repo', help='GitHub repo')
    parser.add_argument('--token', help='GitHub token')
    
    args = parser.parse_args()
    
    if args.status:
        show_cron_status()
        return
    
    if args.disable:
        disable_cron()
        return
    
    # Setup new cron
    print("Setting up daily voice memo workflow...")
    
    # Get time
    if args.time:
        try:
            hour, minute = map(int, args.time.split(':'))
        except:
            print("Invalid time format")
            sys.exit(1)
    else:
        hour, minute = get_cron_time()
    
    # Get GitHub config
    if args.repo and args.token:
        repo, token = args.repo, args.token
    else:
        repo, token = get_github_credentials()
    
    # Create cron
    if setup_cron(hour, minute, repo, token):
        print("\n✓ Setup complete!")
        print("Your voice memos will be automatically transcribed daily.")
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()


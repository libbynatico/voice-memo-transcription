#!/usr/bin/env python3
"""
Complete daily workflow: iMazing sync → incremental transcription → GitHub push.
Called by cron job daily, or manually anytime.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from transcription_tracker import TranscriptionTracker
from batch_transcribe import process_memo, create_index, setup_directories

def run_command(cmd, description):
    """Run shell command with error handling."""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ⚠ {result.stderr[:200]}")
        return False
    print(f"  ✓ Complete")
    return True

def sync_imazing():
    """Step 1: Sync voice memos from iPhone via iMazing."""
    print("\n" + "="*60)
    print("STEP 1: SYNC WITH iMAZING")
    print("="*60)
    
    return run_command(
        'python scripts/imazing_sync.py --auto',
        'Syncing voice memos from iPhone'
    )

def get_new_memos():
    """Step 2: Identify new memos to transcribe."""
    print("\n" + "="*60)
    print("STEP 2: IDENTIFY NEW MEMOS")
    print("="*60)
    
    tracker = TranscriptionTracker()
    new_files = tracker.get_new_files()
    
    if not new_files:
        print("  ℹ No new memos to process")
        return []
    
    print(f"  Found {len(new_files)} new memo(s):")
    for f in new_files:
        print(f"    • {Path(f).name}")
    
    return new_files

def transcribe_memos(memo_files):
    """Step 3: Transcribe new memos."""
    if not memo_files:
        return []
    
    print("\n" + "="*60)
    print(f"STEP 3: TRANSCRIBE ({len(memo_files)} new memo(s))")
    print("="*60)
    
    setup_directories()
    tracker = TranscriptionTracker()
    results = []
    
    for i, memo_path in enumerate(memo_files, 1):
        filename = Path(memo_path).stem
        print(f"\n[{i}/{len(memo_files)}] {filename}")
        
        result = process_memo(memo_path)
        if result:
            results.append(result)
            tracker.mark_processed(memo_path)
            print(f"  ✓ Transcribed and tracked")
        else:
            print(f"  ❌ Failed to transcribe")
    
    if results:
        print(f"\n✓ Transcribed {len(results)}/{len(memo_files)} memos")
    
    return results

def update_index(results):
    """Step 4: Update searchable index."""
    if not results:
        return
    
    print("\n" + "="*60)
    print("STEP 4: UPDATE INDEX")
    print("="*60)
    
    create_index(results)
    print("  ✓ Index updated")

def push_to_github(repo_name, token):
    """Step 5: Push to GitHub."""
    print("\n" + "="*60)
    print("STEP 5: BACKUP TO GITHUB")
    print("="*60)
    
    if not token:
        print("  ℹ Skipping GitHub push (no token configured)")
        return False
    
    return run_command(
        f'python scripts/push_to_github.py --repo {repo_name} --token {token}',
        'Pushing to GitHub'
    )

def log_workflow(results_count, success):
    """Log workflow completion."""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'memos_processed': results_count,
        'success': success
    }
    
    log_file = 'logs/daily_workflow.log'
    os.makedirs('logs', exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    return log_entry

def main():
    """Execute complete daily workflow."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Daily voice memo workflow')
    parser.add_argument('--skip-imazing', action='store_true', help='Skip iMazing sync')
    parser.add_argument('--repo', help='GitHub repo (for push)')
    parser.add_argument('--token', help='GitHub token (for push)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would run, don\'t execute')
    
    args = parser.parse_args()
    
    print("\n" + "█"*60)
    print("  VOICE MEMO DAILY WORKFLOW")
    print("  " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("█"*60)
    
    # Step 1: iMazing sync
    if not args.skip_imazing:
        sync_imazing()
    else:
        print("\nℹ Skipping iMazing sync (--skip-imazing)")
    
    # Step 2: Identify new memos
    new_memos = get_new_memos()
    
    # Step 3: Transcribe
    results = transcribe_memos(new_memos)
    
    # Step 4: Update index
    update_index(results)
    
    # Step 5: Push to GitHub
    if args.repo and args.token:
        push_to_github(args.repo, args.token)
    elif args.token:
        print("\n⚠ GitHub token provided but no repo specified (--repo needed)")
    else:
        print("\nℹ GitHub push not configured (use --repo and --token)")
    
    # Finish
    print("\n" + "█"*60)
    if results:
        print(f"✓ SUCCESS: Processed {len(results)} memo(s)")
    else:
        print("✓ No new memos to process")
    print("█"*60 + "\n")
    
    # Log
    log_workflow(len(results), success=True)

if __name__ == '__main__':
    main()


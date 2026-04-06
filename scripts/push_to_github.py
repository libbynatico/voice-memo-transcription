#!/usr/bin/env python3
"""
Push transcripts and analysis to GitHub.
Maintains a private repo with all voice memo data.
"""

import os
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

def run_command(cmd, check=True):
    """Run shell command safely."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    return result.returncode == 0

def init_github_repo(repo_name, token):
    """Initialize connection to GitHub repo."""
    print(f"Setting up GitHub sync for {repo_name}...")
    
    # Configure git
    run_command(f'git config user.email "voice-memo@local"')
    run_command(f'git config user.name "Voice Memo System"')
    
    # Add remote
    remote_url = f"https://{token}@github.com/{repo_name}.git"
    run_command(f'git remote add origin {remote_url}')
    
    print(f"✓ GitHub sync configured")

def push_to_github(repo_name, token):
    """Push all output to GitHub."""
    print(f"\nPushing to GitHub: {repo_name}")
    
    # Add all files
    run_command('git add -A')
    
    # Create commit
    timestamp = datetime.now().isoformat()
    run_command(f'git commit -m "Voice memo transcription update: {timestamp}"')
    
    # Push to main (or master)
    if run_command('git branch -r | grep origin/main', check=False):
        run_command('git push -u origin main')
    else:
        run_command('git push -u origin master')
    
    print(f"✓ Pushed to GitHub: https://github.com/{repo_name}")

def create_gitignore():
    """Create .gitignore to exclude input files and cache."""
    gitignore = '''
# Input files (don't sync raw audio)
input/*.m4a
input/*.wav
input/*.mp3
input/*.aac

# Cache and temp
__pycache__/
*.pyc
.DS_Store
*.pth
.cache/

# Token files (never commit tokens)
.github_token
.env
'''
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore)
    print("✓ Created .gitignore")

def create_manifest():
    """Create manifest of what's in the repo."""
    manifest = {
        'system': 'Voice Memo Transcription',
        'created': datetime.now().isoformat(),
        'contents': {
            'scripts': 'Python automation scripts',
            'output': 'Generated transcripts and analysis',
            'docs': 'Documentation',
            'config': 'Configuration files'
        },
        'privacy': 'PRIVATE REPO - Medical data',
        'github_repo': 'Will be set by user'
    }
    
    with open('MANIFEST.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    print("✓ Created MANIFEST.json")

def main():
    parser = argparse.ArgumentParser(description='Push voice memo transcripts to GitHub')
    parser.add_argument('--repo', help='GitHub repo (user/repo-name)')
    parser.add_argument('--token', help='GitHub personal access token')
    parser.add_argument('--init', action='store_true', help='Initialize first time')
    
    args = parser.parse_args()
    
    # First time setup
    if args.init:
        print("First-time GitHub setup:")
        print("1. Create private repo on GitHub")
        print("2. Get your personal access token: https://github.com/settings/tokens")
        print("3. Run: python scripts/push_to_github.py --repo YOUR_USERNAME/voice-memo-transcription --token YOUR_TOKEN")
        return
    
    if not args.repo or not args.token:
        print("Usage:")
        print("  First time: python scripts/push_to_github.py --init")
        print("  Then: python scripts/push_to_github.py --repo USERNAME/REPO --token GITHUB_TOKEN")
        return
    
    # Setup
    create_gitignore()
    create_manifest()
    init_github_repo(args.repo, args.token)
    
    # Push
    push_to_github(args.repo, args.token)

if __name__ == '__main__':
    main()


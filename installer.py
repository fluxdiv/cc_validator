#!/usr/bin/env python3

import os
import stat
import subprocess
import sys
import urllib.request
from pathlib import Path


HOOK_URL = "https://raw.githubusercontent.com/fluxdiv/cc_validator/refs/heads/main/commit-msg"
HOOK_NAME = "commit-msg"
DEFAULT_HOOKS_DIR = ".githooks"


def run(cmd):
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


# Check that current directory is inside a Git repo
repo_check = run(["git", "rev-parse", "--show-toplevel"])

if repo_check.returncode != 0:
    print("Error: not inside a Git repository.", file=sys.stderr)
    sys.exit(1)

repo_root = Path(repo_check.stdout.strip())

# Check whether Git hooks are already configured
hooks_path_result = run(["git", "config", "--get", "core.hooksPath"])

if hooks_path_result.returncode == 0 and hooks_path_result.stdout.strip():
    hooks_dir = Path(hooks_path_result.stdout.strip())

    # core.hooksPath can be relative to the repo root
    if not hooks_dir.is_absolute():
        hooks_dir = repo_root / hooks_dir

    created_default_hooks_dir = False
else:
    hooks_dir = repo_root / DEFAULT_HOOKS_DIR
    created_default_hooks_dir = True


# Create the hooks directory if needed
hooks_dir.mkdir(parents=True, exist_ok=True)

# Download the commit-msg hook script
hook_path = hooks_dir / HOOK_NAME

try:
    with urllib.request.urlopen(HOOK_URL) as response:
        hook_contents = response.read()
except Exception as e:
    print(f"Error: failed to download hook from {HOOK_URL}", file=sys.stderr)
    print(e, file=sys.stderr)
    sys.exit(1)


# Write the hook to the selected hooks directory
hook_path.write_bytes(hook_contents)


# Make the hook executable
current_mode = hook_path.stat().st_mode
hook_path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


# If no hook path was already configured, configure .githooks
if created_default_hooks_dir:
    config_result = run(["git", "config", "core.hooksPath", DEFAULT_HOOKS_DIR])

    if config_result.returncode != 0:
        print("Error: failed to set git config core.hooksPath.", file=sys.stderr)
        print(config_result.stderr, file=sys.stderr)
        sys.exit(1)


print(f"Installed {HOOK_NAME} hook at: {hook_path}")

if created_default_hooks_dir:
    print(f"Configured git hooks path: {DEFAULT_HOOKS_DIR}")
else:
    print("Used existing git hooks path from core.hooksPath")

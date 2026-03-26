#!/usr/bin/env python3
"""
Sync Anthropic OAuth credentials from Claude CLI to OpenCode.

Reads credentials from ~/.claude/.credentials.json and updates the
anthropic section in ~/.local/share/opencode/auth.json.

Usage:
    python sync_anthropic_creds.py
"""

import json
import subprocess
import sys
from pathlib import Path


SOURCE_FILE = Path.home() / ".claude" / ".credentials.json"
TARGET_FILE = Path.home() / ".local" / "share" / "opencode" / "auth.json"


def run_claude_auth_status() -> bool:
    """Run claude auth status to verify credentials are valid.

    Returns:
        True if auth status is valid, False otherwise.
    """
    print("Checking Claude auth status...")
    try:
        result = subprocess.run(
            ["claude", "--no-session-persistence", "--model", "claude-haiku-4-5" "--print", "'.'"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print("✓ Claude auth status: valid")
            return True
        else:
            print(f"✗ Claude auth status check failed")
            if result.stderr:
                print(f"  Error: {result.stderr.strip()}")
            if result.stdout:
                print(f"  Output: {result.stdout.strip()}")
            return False
    except FileNotFoundError:
        print("✗ 'claude' command not found. Is Claude CLI installed?")
        return False
    except subprocess.TimeoutExpired:
        print("✗ Claude auth status check timed out")
        return False


def load_source_credentials() -> dict | None:
    """Load credentials from Claude CLI credentials file.

    Returns:
        Dictionary with claudeAiOauth data, or None on error.
    """
    print(f"Reading source file: {SOURCE_FILE}")

    if not SOURCE_FILE.exists():
        print(f"✗ Source file not found: {SOURCE_FILE}")
        return None

    try:
        with open(SOURCE_FILE, "r") as f:
            data = json.load(f)

        oauth = data.get("claudeAiOauth")
        if not oauth:
            print("✗ No claudeAiOauth section found in source file")
            return None

        required_fields = ["accessToken", "refreshToken", "expiresAt"]
        missing = [field for field in required_fields if field not in oauth]
        if missing:
            print(f"✗ Missing required fields: {', '.join(missing)}")
            return None

        print("✓ Source credentials loaded successfully")
        return oauth
    except json.JSONDecodeError as e:
        print(f"✗ Failed to parse source file: {e}")
        return None
    except OSError as e:
        print(f"✗ Failed to read source file: {e}")
        return None


def load_target_auth() -> dict | None:
    """Load existing OpenCode auth configuration.

    Returns:
        Dictionary with auth config, or None on error.
    """
    print(f"Reading target file: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"  Target file does not exist, will create new file")
        return {}

    try:
        with open(TARGET_FILE, "r") as f:
            data = json.load(f)
        print("✓ Target auth file loaded")
        return data
    except json.JSONDecodeError as e:
        print(f"✗ Failed to parse target file: {e}")
        return None
    except OSError as e:
        print(f"✗ Failed to read target file: {e}")
        return None


def update_anthropic_credentials(auth_data: dict, oauth: dict) -> dict:
    """Update the anthropic section in auth data.

    Args:
        auth_data: Existing auth configuration.
        oauth: Claude OAuth credentials.

    Returns:
        Updated auth configuration.
    """
    auth_data["anthropic"] = {
        "type": "oauth",
        "refresh": oauth["refreshToken"],
        "access": oauth["accessToken"],
        "expires": oauth["expiresAt"],
    }
    return auth_data


def save_target_auth(auth_data: dict) -> bool:
    """Save auth configuration to target file.

    Args:
        auth_data: Auth configuration to save.

    Returns:
        True on success, False on error.
    """
    print(f"Writing target file: {TARGET_FILE}")

    # Ensure parent directory exists
    TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(TARGET_FILE, "w") as f:
            json.dump(auth_data, f, indent=2)
            f.write("\n")  # Trailing newline
        print("✓ Target file updated successfully")
        return True
    except OSError as e:
        print(f"✗ Failed to write target file: {e}")
        return False


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    print("=" * 50)
    print("Syncing Anthropic credentials")
    print("=" * 50)
    print()

    # Step 1: Verify auth status
    if not run_claude_auth_status():
        return 1
    print()

    # Step 2: Load source credentials
    oauth = load_source_credentials()
    if oauth is None:
        return 1
    print()

    # Step 3: Load target auth
    auth_data = load_target_auth()
    if auth_data is None:
        return 1
    print()

    # Step 4: Update anthropic credentials
    print("Updating anthropic credentials...")
    auth_data = update_anthropic_credentials(auth_data, oauth)
    print("✓ Credentials mapped:")
    print(f"  access:  {oauth['accessToken'][:20]}...")
    print(f"  refresh: {oauth['refreshToken'][:20]}...")
    print(f"  expires: {oauth['expiresAt']}")
    print()

    # Step 5: Save target
    if not save_target_auth(auth_data):
        return 1
    print()

    print("=" * 50)
    print("✓ Sync complete!")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())

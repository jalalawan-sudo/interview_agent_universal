#!/usr/bin/env python3
"""
Interview Agent Universal — run.py
Single-command launcher. Handles dependencies, starts the server, opens your browser.
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path


MIN_PYTHON = (3, 9)


def check_python():
    if sys.version_info < MIN_PYTHON:
        print(f"✗ Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required. You have {sys.version}.")
        sys.exit(1)


def install_deps():
    req = Path("requirements.txt")
    if not req.exists():
        print("✗ requirements.txt not found. Are you in the right directory?")
        sys.exit(1)
    print("→ Checking dependencies...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"],
        capture_output=True,
    )
    if result.returncode != 0:
        print("✗ Dependency install failed:")
        print(result.stderr.decode()[:500])
        sys.exit(1)
    print("✓ Dependencies ready")


def has_api_key() -> bool:
    env_file = Path(".env")
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("ANTHROPIC_API_KEY=") and len(line) > 40:
                return True
    return bool(os.environ.get("ANTHROPIC_API_KEY", ""))


PORT = 5055


def free_port():
    """Kill any process already using our port so we always get a clean start."""
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{PORT}"],
            capture_output=True, text=True,
        )
        pids = result.stdout.strip().split()
        for pid in pids:
            if pid.isdigit():
                subprocess.run(["kill", "-9", pid], capture_output=True)
        if pids:
            time.sleep(0.5)
    except Exception:
        pass  # lsof not available on all platforms


def main():
    check_python()

    print("\n🎙️  Interview Agent Universal\n")

    # Install deps on first run (or if requirements changed)
    install_deps()

    # Free port 5055 if something else is already using it
    free_port()

    # Start Flask
    print(f"→ Starting server on http://localhost:{PORT} ...")
    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait for server to be ready
    import urllib.request
    server_up = False
    for _ in range(25):
        time.sleep(0.4)
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/check-setup", timeout=1)
            server_up = True
            break
        except Exception:
            continue

    if not server_up:
        print("✗ Server did not start. Check that no other app is using port 5055.")
        proc.terminate()
        sys.exit(1)

    # Open browser — setup page if no key, else main app
    if has_api_key():
        url = f"http://localhost:{PORT}"
        print("✓ Server ready → opening app")
    else:
        url = f"http://localhost:{PORT}/setup"
        print("✓ Server ready → opening setup (enter your Anthropic API key)")

    webbrowser.open(url)
    print(f"\n  Open manually if browser doesn't launch: {url}")
    print("  Press Ctrl+C to stop.\n")

    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n→ Shutting down...")
        proc.terminate()
        proc.wait()
        print("✓ Done.")


if __name__ == "__main__":
    main()

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


def main():
    check_python()

    print("\n🎙️  Interview Agent Universal\n")

    # Install deps on first run (or if requirements changed)
    install_deps()

    # Start Flask
    print("→ Starting server on http://localhost:5055 ...")
    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait for server to be ready
    import urllib.request
    for _ in range(20):
        time.sleep(0.4)
        try:
            urllib.request.urlopen("http://127.0.0.1:5055/check-setup", timeout=1)
            break
        except Exception:
            continue

    # Open browser — setup page if no key, else main app
    if has_api_key():
        url = "http://localhost:5055"
        print("✓ Server ready → opening app")
    else:
        url = "http://localhost:5055/setup"
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

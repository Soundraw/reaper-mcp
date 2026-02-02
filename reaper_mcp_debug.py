#!/usr/bin/env python3
"""
Debug wrapper for REAPER MCP Server

This script wraps the MCP server to capture any startup errors or issues
that might be causing Raycast to fail with "request cancelled" errors.

Usage:
    python reaper_mcp_debug.py
"""

import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

# Log file location
LOG_FILE = Path.home() / "reaper_mcp_debug.log"


def log(message: str):
    """Write a timestamped message to the log file."""
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def main():
    log("=" * 60)
    log("REAPER MCP Debug Wrapper Starting")
    log(f"Python: {sys.executable}")
    log(f"Python version: {sys.version}")
    log(f"Working directory: {os.getcwd()}")
    log(f"Script directory: {Path(__file__).parent}")

    # Log environment variables
    log("Environment variables:")
    for key in ["REAPER_BRIDGE_DIR", "REAPER_COMM_MODE", "REAPER_HOST", "REAPER_PORT"]:
        value = os.environ.get(key, "<not set>")
        log(f"  {key}={value}")

    # Check bridge directory
    bridge_dir = os.environ.get(
        "REAPER_BRIDGE_DIR",
        os.path.expanduser(
            "~/Library/Application Support/REAPER/Scripts/mcp_bridge_data"
        ),
    )
    log(f"Bridge directory: {bridge_dir}")
    log(f"Bridge directory exists: {Path(bridge_dir).exists()}")

    if Path(bridge_dir).exists():
        contents = list(Path(bridge_dir).iterdir())
        log(f"Bridge directory contents: {contents}")

    try:
        log("Importing mcp module...")
        from mcp.server.fastmcp import FastMCP

        log("Successfully imported FastMCP")

        log("Importing reaper_mcp_server...")
        # Add script directory to path
        script_dir = Path(__file__).parent
        sys.path.insert(0, str(script_dir))

        import reaper_mcp_server

        log(f"Successfully imported reaper_mcp_server")
        log(f"Server BRIDGE_DIR: {reaper_mcp_server.BRIDGE_DIR}")
        log(f"Server COMM_MODE: {reaper_mcp_server.COMM_MODE}")

        log("Starting MCP server...")
        reaper_mcp_server.main()

    except Exception as e:
        log(f"ERROR: {type(e).__name__}: {e}")
        log(f"Traceback:\n{traceback.format_exc()}")
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"Fatal error: {e}")
        sys.exit(1)

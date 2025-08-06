Eventin MCP Server - Quick Start Guide
======================================

This guide explains how to run the Eventin MCP server after cloning this repository.

Requirements:
-------------
- Python 3.13 or newer (see .python-version)
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Internet access (for API calls)
- Install dependencies listed in pyproject.toml

Setup Steps:
------------

1. Install Python 3.13 (if not already installed).

2. Install uv (if not already installed):
   pip install uv

3. Install dependencies:
   uv pip install -r requirements.txt
   OR
   uv pip install -e .

4. Run the Eventin MCP server:
   uv --directory . run eventin_mcp_server.py

   This will start the MCP server for Eventin bookings.

5. Logs:
   - Server logs are written to booking_server.log in this directory.

Troubleshooting:
----------------
- If you see missing dependency errors, check pyproject.toml and install required packages.
- Make sure your Python version matches .python-version.

Contact:
--------
For questions, open an issue or contact the repository maintainer.
Eventin MCP Server - Quick Start Guide
======================================

Setup Steps:
------------

1. Install Python 3.13 (if not already installed).

2. (Recommended) Create and activate a virtual environment:
   python -m venv .venv
   .\.venv\Scripts\activate

3. Install uv (if not already installed):
   pip install uv

4. Install dependencies:
   uv pip install -r requirements.txt
   OR
   uv pip install -e .

5. Start eventin locally, and check if it's running in the browser properly

6. Replace My base_url your yours

7. ![API TO CALL](image.png)

8. Run the Eventin MCP server:
   uv --directory . run eventin_mcp_server.py

   This will start the MCP server for Eventin bookings.

9. Logs:
   - Server logs are written to booking_server.log in this directory.

======================================

Steps to communicate with our MCP server using claude desktop:
------------

1. Download and install claude desktop
2. ![alt text](image-1.png)
3. ![alt text](image-2.png)
4. ![alt text](image-3.png)
5. you will find "claude_desktop_config.json", here just put following code
   {
      "mcpServers": {
         "eventin": {
            "command": "uv",
            "args": [
            "--directory",
            "D:\\machine_learning\\mcp-server-demo", //your directory may be different
            "run",
            "eventin_mcp_server.py"
            ]
         }
      }
   }
6. ![alt text](image-4.png)
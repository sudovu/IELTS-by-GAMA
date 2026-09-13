#!/usr/bin/env python
"""
IELTS by GAMA - Master Web Server Entrypoint
Run: python run_ui.py
Launches the local HTTP server serving both the REST API and the responsive single-page UI.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from ui.server import run_server

if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)

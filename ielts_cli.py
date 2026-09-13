#!/usr/bin/env python
"""
IELTS by GAMA - Master Command Line Entrypoint
Run: python ielts_cli.py
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from ui.cli import main

if __name__ == "__main__":
    main()

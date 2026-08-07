"""
Vercel entry point.

Vercel looks inside the /api folder for serverless functions. This file
simply imports the real Flask app from app.py (one level up) so Vercel
can run it. You don't need to edit this file.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app import app  # noqa: E402  (Vercel's Python runtime looks for "app")

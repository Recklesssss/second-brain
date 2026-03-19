#!/usr/bin/env python3
"""
Run script for the AI Second Brain Backend
"""

import uvicorn
import os
import sys
import uvicorn
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).parent.resolve()
    os.chdir(project_root)
    sys.path.insert(0, str(project_root))
    os.environ["PYTHONPATH"] = str(project_root)

    # Run the FastAPI server
    uvicorn.run(
        "second_brain_ai.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
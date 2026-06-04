"""
LeakRecon Test Configuration.

Adds the project root to sys.path so that imports like 'from config import Settings'
and 'from core.banner import ...' work correctly when running pytest from any directory.
"""
import sys
from pathlib import Path

# Ensure project root is on the path for imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

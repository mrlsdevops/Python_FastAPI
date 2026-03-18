import sys
from pathlib import Path

# Ensure `import app...` works even when test runner cwd is `app/`.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

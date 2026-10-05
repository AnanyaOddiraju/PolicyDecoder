import sys
from pathlib import Path

# Ensure project root (Pocky_Chatbot) is on sys.path so imports like `from src...` work
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

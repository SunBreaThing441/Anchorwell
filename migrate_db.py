"""
Run database migration and seed sample data:
python migrate_db.py
Or with reset:
python migrate_db.py --reset
"""
import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from psychbuddy.db_migrator import migrate_and_seed

if __name__ == '__main__':
    reset = "--reset" in sys.argv
    migrate_and_seed(drop_existing=reset, clear_existing=reset)

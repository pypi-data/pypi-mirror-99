from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent       # /whikoperator
CUR_DIR = os.path.dirname(os.path.abspath(__file__))    # /whikoperator/whikoperator
CONFIGS_DIR = os.path.join(CUR_DIR, 'configs')

DEF_COUNT_FILE = 'cam_count.cfg'
DEF_PICS_JOURNAL = 'fpath.cfg'
PICS_DIR_NAME = 'photos'

COUNT_FILE_PATH = os.path.join(CONFIGS_DIR, DEF_COUNT_FILE)
PICS_JOURNAL_PATH = os.path.join(CONFIGS_DIR, DEF_PICS_JOURNAL)
DEF_PICS_DIR = os.path.join(CUR_DIR, PICS_DIR_NAME)

from whikoperator import settings as s
import os


print('PICS_DIR_NAME', s.PICS_DIR_NAME)
print('PICS_JOURNAL', s.PICS_JOURNAL_PATH)
print('PICS_FOLDER', s.DEF_PICS_DIR)

os.listdir(s.DEF_PICS_DIR)
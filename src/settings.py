# GLOBAL SETTINGS
import os

DIR_SCHEMA_FOLDER = 'db_maps'
CHECK_SCHEMA = False

DB_CONNECTOR_PATTERN="^[a-z]*://[a-zA-Z0-9]*(:[a-zA-Z0-9]*)?@[a-zA-Z0-9\.]*([:0-9]*?)/[a-zA-Z0-9_]*$"

SEP = os.path.sep
BASE_DIR = os.path.abspath(os.path.dirname(__file__)).decode('utf-8')

ROOT_PATH = BASE_DIR + SEP
DB_MAP_FOLDER = ROOT_PATH + DIR_SCHEMA_FOLDER

SAFE_ROOT_PATH = ROOT_PATH.replace(' ', '\ ')
SAFE_DB_MAP_FOLDER = SAFE_ROOT_PATH + DIR_SCHEMA_FOLDER

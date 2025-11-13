"""Configuration settings for NLP to SQL converter"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
INPUT_DIR = DATA_DIR / 'input'
OUTPUT_DIR = DATA_DIR / 'output'

# Create directories if they don't exist
for dir_path in [DATA_DIR, INPUT_DIR, OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4')
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.0'))

# Cache Configuration
CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
SAVE_QUERIES = os.getenv('SAVE_QUERIES', 'false').lower() == 'true'
QUERY_LOG_FILE = OUTPUT_DIR / 'query_history.json'
SIMILARITY_THRESHOLD = 0.9

 
# Visualization Configuration
FIGURE_SIZE = (10, 6)
MAX_DISPLAY_ROWS = 15

# Text Processing
MAX_TEXT_LENGTH = 20000  # Characters
STOP_WORDS = 'english'

# Database Configuration
DB_TYPE = 'mysql'  # CHANGE THIS TO 'mysql'
DB_PATH = OUTPUT_DIR / 'generated_database.db'
IN_MEMORY_DB = False

# MySQL Configuration (if using MySQL)
MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'sample'
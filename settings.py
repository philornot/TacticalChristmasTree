import os
from pathlib import Path

from logger import NiceLogger

# Initialize logger
logger = NiceLogger(__name__).get_logger()

# Project information
PROJECT_NAME = "TacticalChristmasTree"
PROJECT_VERSION = "0.7.3"
AUTHOR = "philornot"
DESCRIPTION = "Deploy your own customizable ChristmasTree.png!"
GITHUB_REPO = "https://github.com/philornot/TacticalChristmasTree"

# Directory structure
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
USER_DATA_DIR = Path.home() / "Documents" / PROJECT_NAME
LOGS_DIR = USER_DATA_DIR / "logs"
TEMP_DIR = ROOT_DIR / "temp"
BUILD_DIR = ROOT_DIR / "build"
DIST_DIR = ROOT_DIR / "dist"

# Ensure directories exist
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Build settings
MAIN_SCRIPT = ROOT_DIR / "main.py"

# Icon paths
ICON_PATH = ROOT_DIR / "assets" / "icon.ico"
ICON_PNG_PATH = ROOT_DIR / "assets" / "icon.png"

# Ensure icon files exist
if not ICON_PATH.exists() or not ICON_PNG_PATH.exists():
    logger.warning("Icon files missing", extra={
        'metadata': {
            'ico_path': str(ICON_PATH),
            'png_path': str(ICON_PNG_PATH)
        }
    })

# Application settings
WINDOW_SIZE = "800x800"
DEFAULT_LANGUAGE = "en"

# Tree size settings
MIN_HEIGHT = 100
MAX_HEIGHT = 350
MIN_WIDTH = 100
MAX_WIDTH = 300
MIN_LAYERS = 3
MAX_LAYERS = 8
DEFAULT_COLOR = "#2E8B57"

# Decoration settings
MIN_ORNAMENTS = 0  # Minimum number of ornaments
MAX_ORNAMENTS = 15  # Maximum number of ornaments
DEFAULT_ORNAMENTS = 5  # Default number of ornaments

MIN_CHAINS = 0  # Minimum number of chains
MAX_CHAINS = 8  # Maximum number of chains
DEFAULT_CHAINS = 3  # Default number of chains

# Logging settings
LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5
LOG_CONSOLE_LEVEL = "INFO"
LOG_FILE_LEVEL = "DEBUG"

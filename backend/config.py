# backend/config.py
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.dirname(__file__)
# When running as an EXE, PyInstaller puts files in a temp folder accessed via sys._MEIPASS
import sys
if hasattr(sys, '_MEIPASS'):
    DIST_DIR = os.path.join(sys._MEIPASS, "frontend/dist")
else:
    DIST_DIR = os.path.join(BASE_DIR, "../frontend/dist")

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "hii")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

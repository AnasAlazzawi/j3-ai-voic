"""
Configuration file for Telegram Bot
ملف إعدادات البوت
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Configuration - Load from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Validate required environment variables
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN must be set in environment variables or .env file")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be set in environment variables or .env file")

# File paths
CONVERSATION_FILE = "conversations.json"
CONVERSATION_TIMEOUT = 24 * 60 * 60  # 24 hours in seconds

# Available TTS voices
TTS_VOICES = [
    'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', 
    'coral', 'verse', 'ballad', 'ash', 'sage', 'amuch', 'dan'
]

# Language detection regex patterns
ARABIC_CHARS_PATTERN = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
ENGLISH_CHARS_PATTERN = r'[a-zA-Z]'

# Speech recognition settings
SPEECH_RECOGNITION_SETTINGS = {
    'energy_threshold': 300,
    'dynamic_energy_threshold': True,
    'pause_threshold': 0.5,
    'ambient_noise_duration': 0.5
}

# AI Generation settings
AI_GENERATION_CONFIG = {
    'temperature': 0.7,
    'max_output_tokens': 1000,
    'top_p': 0.8,
    'top_k': 40
}

# TTS settings
TTS_MAX_LENGTH = 1000
TTS_CLIENT_URL = "NihalGazi/Text-To-Speech-Unlimited"

# Logging format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

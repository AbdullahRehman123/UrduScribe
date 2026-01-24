import os
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
import logging
#from dotenv import load_dotenv
import torch

# Load environment variables from .env (if present)
#load_dotenv()

# ─── PATHS ──────────────────────────────────────────────────────────────────────

# Folder where incoming urdu .wav/.mp3 files live
URDU_INPUT_FOLDER = Path(os.getenv("URDU_INPUT_FOLDER", "../urdu_audios"))

# Folder where incoming english .wav/.mp3 files live
ENGLISH_INPUT_FOLDER = Path(os.getenv("ENGLISH_INPUT_FOLDER", "../english_audios"))

# Folder where .txt transcripts will be written
OUTPUT_FOLDER = Path(os.getenv("OUTPUT_FOLDER", "../transcriptions"))

# Local WHISPER BASE Hugging Face model directory
ENGLISH_MODEL_PATH = Path(os.getenv("ENGLISH_MODEL_PATH", "../models/whisper-base"))

# Local URDU ASR Hugging Face model directory
URDU_MODEL_PATH = Path(os.getenv("MODEL_PATH", "../models/ns_finetune_urdu_asr_org"))

# Local DIARIZATION Hugging Face model directory
DIARIZATION_MODEL_CONFIG_PATH = Path(os.getenv("DIARIZATION_MODEL_CONFIG_PATH", "../models/speaker-diarization-3.1/pyannote_diarization_config.yaml"))

# Log file (rotated daily)
LOG_FILE = Path(os.getenv("LOG_FILE", "../logs/transcriber.log"))
print(LOG_FILE) #debug

# ─── AUDIO CHUNKING ─────────────────────────────────────────────────────────────
# How long (in seconds) each chunk should be
CHUNK_LENGTH_SECONDS = int(os.getenv("CHUNK_LENGTH_SECONDS", 30))

# ─── DEVICE CONFIG ─────────────────────────────────────────────────────────────
# Force CPU/GPU, or auto‐detect
DEVICE = os.getenv("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")

# ─── LOGGING SETTINGS ──────────────────────────────────────────────────────────
LOG_LEVEL  = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

def get_rotating_logger(name: str = "audio_transcriber") -> logging.Logger:
    """
    Returns a logger that writes to a daily-rotated file,
    keeping up to 7 days of history by default.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Prevent adding multiple handlers if called multiple times
    if not any(isinstance(h, TimedRotatingFileHandler) for h in logger.handlers):
        handler = TimedRotatingFileHandler(
            filename=str(LOG_FILE),
            when="midnight",
            interval=1,
            backupCount=int(os.getenv("LOG_BACKUP_COUNT", 7)),
            encoding="utf-8"
        )
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)

    return logger

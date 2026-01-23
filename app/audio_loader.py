from pathlib import Path
from typing import List, Tuple
import librosa
import numpy as np
from config import URDU_INPUT_FOLDER,ENGLISH_INPUT_FOLDER, CHUNK_LENGTH_SECONDS

def load_audio_files(input_dir: Path = ENGLISH_INPUT_FOLDER) -> List[Path]:
    """
    Returns a list of all .wav and .mp3 audio file paths in the input directory.
    """
    audio_files = []
    for ext in ("*.wav", "*.mp3"):
        audio_files.extend(input_dir.glob(ext))
    return audio_files

def load_and_preprocess_audio(file_path: Path) -> Tuple[np.ndarray, int]:
    """
    Loads an audio file, converts stereo to mono, and resamples to 16 kHz.
    Returns the audio time series (numpy array) and sample rate.
    """
    # Load audio using librosa (auto converts stereo to mono if needed)
    audio, sr = librosa.load(file_path, sr=16000, mono=True)
    return audio, sr

def chunk_audio(audio: np.ndarray, sr: int, chunk_duration_sec: int = CHUNK_LENGTH_SECONDS) -> List[np.ndarray]:
    """
    Splits the audio into fixed-duration chunks.
    Returns a list of audio chunks (numpy arrays).
    """
    total_samples = len(audio)
    chunk_length_samples = chunk_duration_sec * sr
    chunks = []

    for start in range(0, total_samples, chunk_length_samples):
        end = start + chunk_length_samples
        chunk = audio[start:end]
        chunks.append(chunk)

    return chunks

def process_audio_file(file_path: Path) -> List[np.ndarray]:
    """
    Complete pipeline for a single audio file:
    Loads, preprocesses, and chunks it.
    Returns a list of chunks ready for transcription.
    """
    audio, sr = load_and_preprocess_audio(file_path)
    chunks = chunk_audio(audio, sr)
    return chunks

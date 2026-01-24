from pathlib import Path
from pyannote.audio import Pipeline
from app.diarization_pipeline_loader import load_pipeline_from_pretrained
from app.config import DIARIZATION_MODEL_CONFIG_PATH, get_rotating_logger

logger = get_rotating_logger("Diarization")

# Load pipeline once at startup
config_uri = Path(DIARIZATION_MODEL_CONFIG_PATH).resolve()
pipeline = load_pipeline_from_pretrained(config_uri)

def diarize_audio(audio_file_path: str):
    """
    Run speaker diarization on the given audio file.
    Returns a list of segments with speaker labels.
    """
    logger.info(f"Diarizing file: {audio_file_path}")
    diarization_result = pipeline(audio_file_path,num_speakers=2)  # you can set num_speakers if known

    # Convert to structured list [(speaker, start_time, end_time)]
    segments = []
    for turn, _, speaker in diarization_result.itertracks(yield_label=True):
        segments.append((speaker, turn.start, turn.end))

    return segments
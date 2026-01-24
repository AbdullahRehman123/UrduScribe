import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import numpy as np
from typing import List
from app.config import URDU_MODEL_PATH, DEVICE
import warnings
from transformers.utils import logging as transformers_logging
from app.config import get_rotating_logger

# Initialize logger
logger = get_rotating_logger("main")

# Suppress transformers warnings for clean logs
warnings.filterwarnings("ignore")
transformers_logging.set_verbosity_error()

# Load processor and model once at module level (kept in memory)
processor = WhisperProcessor.from_pretrained(URDU_MODEL_PATH, local_files_only=True)
model = WhisperForConditionalGeneration.from_pretrained(URDU_MODEL_PATH, local_files_only=True).to(DEVICE)

# Forced decoder IDs for Urdu prompt (You may adjust these IDs if your model expects different ones)
#FORCED_DECODER_IDS = processor.get_decoder_prompt_ids(language="ur", task="transcribe")

model.generation_config.language = "ur"
model.generation_config.task = "transcribe"

def transcribe_chunks(audio_chunks: List[np.ndarray], sampling_rate: int = 16000) -> str:
    """
    Transcribes a list of audio chunks and returns the combined transcription as a single string.
    """
    full_transcription = []

    for idx, chunk in enumerate(audio_chunks):
        # Prepare input features
        input_features = processor(
            chunk, 
            sampling_rate=sampling_rate, 
            return_tensors="pt"
        ).input_features.to(DEVICE)

        # Disable gradient calculation for efficient inference
        with torch.no_grad():
            predicted_ids = model.generate(
                input_features
                #,forced_decoder_ids=FORCED_DECODER_IDS
            )

        # Decode token IDs to text
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0].strip()
        full_transcription.append(transcription)

    # Combine all chunk transcriptions into one final text

    logger.info(f"Chunks transcribed successfully")

    return ' '.join(full_transcription)
    
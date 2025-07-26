from config import MODEL_PATH, DEVICE
import os
from pathlib import Path
from transformers import WhisperProcessor

MODEL_PATH = str(
    Path(os.getenv("MODEL_PATH", "./models/ns_finetune_urdu_asr_org"))
    .resolve()
    .as_posix()
) + "/"

processor = WhisperProcessor.from_pretrained(MODEL_PATH, local_files_only=True)
print("✅ Processor loaded successfully from:", MODEL_PATH)
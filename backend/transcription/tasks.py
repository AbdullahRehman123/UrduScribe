from celery import shared_task
from pathlib import Path

@shared_task
def transcribe_audio_task(upload_path, language, num_speakers):
    """
    Background task to transcribe audio
    """
    from app.transcribe import transcribe
    
    transcription_text = transcribe(upload_path, language, num_speakers)
    return transcription_text
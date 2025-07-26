from pathlib import Path
from datetime import datetime
import time
from config import INPUT_FOLDER, OUTPUT_FOLDER, get_rotating_logger
from audio_loader import load_audio_files, process_audio_file
from transcription import transcribe_chunks

# Initialize logger
logger = get_rotating_logger("main")

def save_transcription(text: str, original_filename: str):
    """
    Saves the transcription text to OUTPUT_FOLDER with timestamped filename.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_name = Path(original_filename).stem
    output_filename = f"{base_name}_{timestamp}.txt"
    output_path = OUTPUT_FOLDER / output_filename

    # Ensure output folder exists
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return output_path

def main():
    logger.info("Starting Urdu Audio Transcription Microservice")

    audio_files = load_audio_files(INPUT_FOLDER)

    if not audio_files:
        logger.info("No audio files found in input folder.")
        return

    for audio_file in audio_files:
        logger.info(f"Processing file: {audio_file.name}")
        start_time = time.time()

        try:
            # Load, preprocess, and chunk audio
            chunks = process_audio_file(audio_file)
            logger.info(f"Chunking complete: {len(chunks)} chunks created.")

            # Transcribe all chunks
            transcription_text = transcribe_chunks(chunks)
            logger.info("Transcription completed successfully.")

            # Save to output file
            output_file_path = save_transcription(transcription_text, audio_file.name)
            duration = time.time() - start_time
            logger.info(f"File processed: {audio_file.name} | Duration: {duration:.2f}s | Output: {output_file_path.name} | Status: SUCCESS")

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"File processed: {audio_file.name} | Duration: {duration:.2f}s | Status: FAILED | Error: {str(e)}")

if __name__ == "__main__":
    main()
from pathlib import Path
from datetime import datetime
import time
from config import ENGLISH_INPUT_FOLDER, URDU_INPUT_FOLDER, OUTPUT_FOLDER, get_rotating_logger
from audio_loader import load_audio_files, load_and_preprocess_audio
from transcription_english import transcribe_chunks
from diarization import diarize_audio

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
    logger.info("Starting Audio Transcription Microservice")

    # Load audio files
    audio_files = load_audio_files(ENGLISH_INPUT_FOLDER)

    if not audio_files:
        logger.info("No audio files found in input folder.")
        return

    # Process each audio file
    for audio_file in audio_files:

        logger.info(f"Processing file: {audio_file.name}")
        start_time = time.time()

        try:
            # Load and preprocess audio
            audio_np, sr = load_and_preprocess_audio(audio_file)

             # Perform diarization
            speaker_segments = diarize_audio(str(audio_file))
            logger.info(f"Diarization completed: {len(speaker_segments)} speaker segments found.")

            lines = []
            min_len = int(0.25 * sr)  # skip <250 ms

            logger.info(f"Transcription started for each speaker segment.")
            # Segment audio by speaker
            for speaker, start, end in speaker_segments:
                s, e = int(start * sr), int(end * sr)
                seg_audio = audio_np[s:e]

                if len(seg_audio) < min_len:
                    continue

                # Transcribe audio segment
                text = transcribe_chunks([seg_audio], sampling_rate=sr)

                if text.strip():
                    lines.append(f"{speaker}: {text.strip()}")

            logger.info(f"Transcription completed for file: {audio_file.name}")

            # Save to output file
            output_file_path = save_transcription("\n".join(lines), audio_file.name)
            duration = time.time() - start_time
            logger.info(f"File processed: {audio_file.name} | Duration: {duration:.2f}s | Output: {output_file_path.name} | Status: SUCCESS")

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"File processed: {audio_file.name} | Duration: {duration:.2f}s | Status: FAILED | Error: {str(e)}")

if __name__ == "__main__":
    main()
# Urdu-Audio-Transcription-Microservice
A Python-based microservice that transcribes Urdu audio files (`.wav` or `.mp3`) using a **locally fine-tuned ASR model**. Supports batch processing, chunked transcription for long audios, and daily rotated logs.

## 📂 Project Structure
asr-microservice/  
├── app/  
│ ├── config.py  
│ ├── audio_loader.py  
│ ├── transcription.py  
│ └── main.py  
├── models/  
│ └── ns_finetune_urdu_asr_org/  
├── audios/ # Input folder for audio files (.wav/.mp3)  
├── transcriptions/ # Output folder for .txt transcriptions  
├── logs/ # Log files (rotated daily)  
├── requirements.txt  
├── .env  
└── README.md

## ⚙️ Prerequisites
- Python 3.9+
- pip or conda
- Sufficient disk space for ASR model
- CUDA-enabled GPU (optional, but recommended for performance)

### 1. Clone the Repository
```
git clone https://github.com/abdullah-rehman1/Urdu-Audio-Transcription-Microservice
cd audio_transcriber_microservice
```

### 2. Clone the Fine-Tuned Urdu ASR Model
```
git lfs install
git clone https://huggingface.co/sajadkawa/ns_finetune_urdu_asr_org
```

### 3. Create Virtual Environment & Install Dependencies
```
python -m venv env
# On Linux/macOS
source env/bin/activate
# On Windows
env\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure .env File
```
INPUT_FOLDER=../audios
OUTPUT_FOLDER=../transcriptions
MODEL_PATH=../models/ns_finetune_urdu_asr_org
LOG_FILE=../logs/transcriber.log
CHUNK_LENGTH_SECONDS=30
DEVICE=cpu
LOG_LEVEL=INFO
LOG_BACKUP_COUNT=14
```

### 5. Folder Structure Preparation
Ensure these folders exist:
```
mkdir -p audios transcriptions logs
```

## 🚀 Running the Service
1. Drop your .wav or .mp3 files into the /audios/ folder.
2. Run the transcription service:
```
python app/main.py
```

## 📤 Output
- Transcriptions will be saved as .txt files in /transcriptions/ with filenames like:
```
urduAudioFile_2025-07-24_15-30-00.txt
```
- Logs will appear in /logs/transcriber.log and rotate daily.

  
## 📝 Example Workflow
- Place urduMenu.wav in /audios/
- ```python app/main.py```
- Check /transcriptions/ for the output text file.
- Review /logs/ for process logs.
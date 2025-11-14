# AudioToText — Batch transcription (no summarization)

AudioToText converts audio files into text. The current version focuses on reliable batch transcription (place audio files in the `audio/` folder) and saves one `.txt` transcript per audio file. It uses Google Speech recognition (via the SpeechRecognition package) and FFmpeg (via pydub) for conversion and preprocessing.

This repository previously included automatic Gemini summarization; the codebase has since been refactored to remove automatic summarization and to provide a faster, more robust batch-transcription workflow.

## Why use this

- Great for course note-taking: drop lecture recordings in `audio/` and get clean transcripts
- Batch processing: transcribe multiple files without manual input
- Parallel chunk processing for speed (processes chunks of a file concurrently)
- Persian support (fa-IR) plus many other languages

## Key Features

- Batch-processing: put audio files into the `audio/` folder and run the script
- Parallel chunk transcription inside each file (configurable via `MAX_WORKERS`)
- Supports common audio formats: MP3, M4A, WAV, FLAC, OGG, WMA
- Language override via CLI or environment variable (see Usage)

## Supported Languages (examples)

- French (fr-FR)
- English (en-US)
- German (de-DE)
- Spanish (es-ES)
- Italian (it-IT)
- Japanese (ja-JP)
- Korean (ko-KR)
- Chinese Simplified (zh-CN)
- Persian (fa-IR)

## Prerequisites

1. Python 3.8+
2. FFmpeg installed and available in PATH
3. Python packages: SpeechRecognition, pydub

## Install

```powershell
# Create & activate venv (Windows PS)
python -m venv .venv
.venv\Scripts\Activate.ps1

pip install SpeechRecognition pydub
```

Install FFmpeg for your OS (winget/choco/brew/apt as appropriate).

## Usage

1. Put audio files into the `audio/` folder in the repository root.
2. Run the script. By default the tool uses French (`fr-FR`) unless you override the language.

One-off (select Persian):
```powershell
C:/Python312/python.exe .\audioToText.py --lang fa
```

Or set environment variable for the session (PowerShell):
```powershell
$env:AUDIO_LANG = 'fa'
C:/Python312/python.exe .\audioToText.py
```

Notes:
- Acceptable `--lang` values: `fa`, `fa-IR`, `persian`, `en`, `en-US`, `fr`, `fr-FR`, etc.
- The script saves transcripts as `audio_filename.txt` next to each audio file.

## Configuration

Open `audioToText.py` and change:

- `MAX_WORKERS` — number of parallel chunk workers (default 4)
- `CHUNK_LENGTH` — chunk size in milliseconds (default 300000 = 300s)
- `LANGUAGE_CODE` — default language code (e.g., `fr-FR`)

## Example

```powershell
# Transcribe Persian files in audio/ using 4 parallel chunk workers
C:/Python312/python.exe .\audioToText.py --lang fa
```

Output (example):

======================================================================
                  🎵 AUDIO TO TEXT BATCH PROCESSOR 🎵
======================================================================

📊 Found 2 file(s)
⚙️  Using 4 parallel workers per file
📝 Chunk size: 300s | Language: Persian (fa-IR)

[...] (progress lines and saved .txt files)

## Troubleshooting

- If FFmpeg is not found, install it and ensure it's on PATH.
- If recognition fails on some chunks, try lowering `CHUNK_LENGTH` or improving audio quality.

## Contributing

Contributions welcome — open a PR or an issue.

## License

MIT — see LICENSE

## Contact

- GitHub: https://github.com/Pooriadf

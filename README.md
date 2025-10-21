# AudioToText Transcription and Summarization Tool

A Python tool that transcribes audio files to text and generates summaries in multiple languages using Google Speech Recognition and Google's Gemini AI.

## Features

- Multi-language audio transcription
- Automatic audio format conversion (supports MP3, M4A, WAV, etc.)
- Smart audio preprocessing (normalization, mono conversion, resampling)
- Chunk-based processing for long audio files
- Language-native summarization
- Support for 8 different languages

## Supported Languages

- French (fr-FR)
- English (en-US)
- German (de-DE)
- Spanish (es-ES)
- Italian (it-IT)
- Japanese (ja-JP)
- Korean (ko-KR)
- Chinese Simplified (zh-CN)

## Prerequisites

1. Python 3.x
2. FFmpeg installed on your system
3. Google API Key for Gemini AI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Pooriadf/audiototext.git
cd audiototext
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. Install required packages:
```bash
pip install SpeechRecognition google-generativeai pydub
```

4. Install FFmpeg:
```bash
# Windows (using winget)
winget install -e --id Gyan.FFmpeg

# Windows (using chocolatey)
choco install ffmpeg

# Mac
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg
```

5. Set up your Google API Key:
```bash
# Windows PowerShell
$env:GOOGLE_API_KEY="your-api-key-here"

# Linux/Mac
export GOOGLE_API_KEY="your-api-key-here"
```

## Usage

1. Basic usage:
```bash
python audioToText.py path/to/your/audio.mp3
```

2. Follow the interactive prompts to:
   - Select your audio's language
   - View the transcription
   - Get the summary

## Examples

### Example 1: French Lecture Transcription

```bash
python audioToText.py lecture.mp3
```

Output:
```
Available languages:
1. French
2. English
3. German
[...]

Select the language of your audio (1-8): 1

Selected language: French
Loading audio file: lecture.mp3...
Converting audio to WAV format...
[...]

RÉSUMÉ:
[Your French summary appears here]

THÈMES PRINCIPAUX:
• Point 1
• Point 2
[...]
```

### Example 2: English Meeting Recording

```bash
python audioToText.py meeting.m4a
```

Output:
```
Select the language of your audio (1-8): 2

Selected language: English
[...]

SUMMARY:
[Your English summary appears here]

MAIN THEMES:
• Discussion point 1
• Action items
[...]
```

## Advanced Features

1. **Audio Preprocessing**:
   - Automatic audio normalization
   - Conversion to mono for better recognition
   - Resampling to 16kHz
   - Chunk-based processing for long files

2. **Format Support**:
   - WAV
   - MP3
   - M4A
   - And other formats supported by FFmpeg

## Troubleshooting

1. **FFmpeg not found error**:
   - Ensure FFmpeg is installed and in your system PATH
   - Windows users can install via: `winget install -e --id Gyan.FFmpeg`

2. **API Key Issues**:
   - Verify your Google API key is correctly set
   - Check if the key has proper permissions
   - Visit https://makersuite.google.com/app/apikey to manage keys

3. **Audio Not Recognized**:
   - Ensure clear audio quality
   - Check if the correct language is selected
   - Try with a shorter audio segment first

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Speech Recognition API
- Google Gemini AI
- FFmpeg project
- All contributors and users

## Contact

- GitHub: [@Pooriadf](https://github.com/Pooriadf)

# AI Agent Instructions for AudioToText Project

## Core Architecture

This project implements a dual-phase audio processing pipeline:

### Phase 1: Speech Recognition Layer
- **Input Handler**: Processes various audio formats (WAV, M4A, etc.)
- **Audio Preprocessor**:
  - Normalizes audio levels
  - Converts to mono channel
  - Resamples to 16kHz for optimal recognition
- **Chunking Engine**: Segments long audio into 10-second chunks
- **Speech Recognition Core**: 
  - Primary: Google Speech-to-Text API
  - Fallback: Sphinx (offline mode)
- **Language Support**: Multi-language capability with focus on French (`fr-FR`)

### Phase 2: Text Processing Layer
- **Text Aggregator**: Combines transcribed chunks
- **Summarization Engine**: Google Gemini AI
  - Model: `gemini-pro`
  - Cross-lingual capability (French → English)

## Critical Dependencies & Configuration

### External Services
1. **Google Speech Recognition**
   ```python
   # Language configuration
   r.recognize_google(audio, language='fr-FR')
   ```

2. **Google Gemini AI**
   ```python
   # Environment setup
   GOOGLE_API_KEY="your_api_key"  # Required
   ```

### Core Libraries
- `speech_recognition`: Speech-to-text conversion
- `google.generativeai`: Text summarization
- `pydub`: Audio preprocessing
- `ffmpeg`: Audio format conversion (system requirement)

## Error Handling Architecture

### Layered Error Management
1. **Audio Processing Layer**
   - File format validation
   - Conversion error handling
   - Chunk processing failures

2. **API Integration Layer**
   - Network connectivity issues
   - API rate limits
   - Service response validation

3. **Resource Management**
   - Temporary file cleanup
   - Memory management for large files
   - System resource allocation

## Performance Optimization

### Audio Processing
- Chunk size: 10 seconds (optimized for API limits)
- Audio normalization for improved recognition
- Mono channel conversion for reduced bandwidth

### Memory Management
- Streaming chunk processing
- Temporary file handling
- Resource cleanup protocols

## Development Workflow

### Setup Process
1. Environment Configuration:
   ```bash
   # Windows PowerShell
   $env:GOOGLE_API_KEY="your_api_key"
   ```

2. Dependencies Installation:
   ```bash
   pip install SpeechRecognition google-generativeai pydub
   ```

3. System Requirements:
   - FFmpeg installation
   - Python 3.x
   - Internet connectivity

### Testing Protocol
1. **Audio Format Testing**
   - Test with various formats (WAV, M4A)
   - Verify format conversion
   - Validate chunk processing

2. **Recognition Testing**
   - Online (Google) mode
   - Offline (Sphinx) mode
   - Multi-language support

3. **Error Scenario Testing**
   - Network failure handling
   - Invalid API key handling
   - Resource cleanup verification

## Integration Points

### External Services
1. **Google Speech API**
   - Rate limiting: Yes
   - Authentication: None required
   - Language support: Extensive

2. **Google Gemini API**
   - Rate limiting: Yes
   - Authentication: API key required
   - Cross-lingual support: Yes

### System Integration
- FFmpeg dependency
- File system access
- Environment variable management

## Best Practices

### Code Organization
- Modular function design
- Comprehensive error handling
- Clear logging and user feedback

### Resource Management
- Proper file cleanup
- Memory-efficient chunk processing
- API rate limit consideration

### Security
- Environment-based API key management
- Temporary file secure handling
- Resource access control

## Common Issues and Solutions

### Audio Processing
- Issue: FFmpeg not found
  Solution: Add to system PATH or use local installation

### API Integration
- Issue: API key not found
  Solution: Verify environment variable setup

### Performance
- Issue: Long audio files
  Solution: Chunked processing with progress tracking
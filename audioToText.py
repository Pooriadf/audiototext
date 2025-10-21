import speech_recognition as sr
import google.generativeai as genai
import os
from pydub import AudioSegment
import tempfile
import sys
from pathlib import Path

# Set FFmpeg path
FFMPEG_PATH = str(Path(__file__).parent / "tools")
if FFMPEG_PATH not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + FFMPEG_PATH

# --- Configuration ---
# You need to set your Gemini API key as an environment variable
# For Windows PowerShell: $env:GOOGLE_API_KEY="YOUR_API_KEY"
# For Linux/Mac: export GOOGLE_API_KEY="YOUR_API_KEY"
# Get your API key from: https://makersuite.google.com/app/apikey

def get_language_code():
    """
    Prompts the user to select the language of the audio file.
    
    Returns:
        str: The language code (e.g., 'fr-FR', 'en-US', etc.)
    """
    language_codes = {
        '1': ('fr-FR', 'French'),
        '2': ('en-US', 'English'),
        '3': ('de-DE', 'German'),
        '4': ('es-ES', 'Spanish'),
        '5': ('it-IT', 'Italian'),
        '6': ('ja-JP', 'Japanese'),
        '7': ('ko-KR', 'Korean'),
        '8': ('zh-CN', 'Chinese (Simplified)'),
    }
    
    print("\nAvailable languages:")
    for key, (code, name) in language_codes.items():
        print(f"{key}. {name}")
    
    while True:
        choice = input("\nSelect the language of your audio (1-8): ").strip()
        if choice in language_codes:
            code, name = language_codes[choice]
            print(f"\nSelected language: {name}")
            return code, name
        print("Invalid choice. Please try again.")

def transcribe_audio(audio_file_path, language_code):
    """
    Transcribes an audio file into text using the SpeechRecognition library.
    Handles long audio files by splitting them into smaller chunks.
    
    Args:
        audio_file_path (str): The path to the audio file (e.g., .wav, .mp3, .m4a).
        language_code (str): The language code for speech recognition.
        
    Returns:
        str: The transcribed text, or None if transcription fails.
    """
    r = sr.Recognizer()
    
    print(f"Loading audio file: {audio_file_path}...")
    try:
        # Convert audio file to WAV if it's not already
        if not audio_file_path.lower().endswith('.wav'):
            print("Converting audio to WAV format...")
            audio = AudioSegment.from_file(audio_file_path)
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                audio.export(temp_wav.name, format='wav')
                audio_file_path = temp_wav.name
                print("Conversion complete.")

        # Load the audio file
        full_text = []
        chunk_length = 300000  # 300 seconds
        audio_segment = AudioSegment.from_wav(audio_file_path)
        
        # Normalize audio (adjust volume to a standard level)
        audio_segment = audio_segment.normalize()
        
        # Convert to mono if stereo
        if audio_segment.channels > 1:
            audio_segment = audio_segment.set_channels(1)
        
        # Set sample rate to 16kHz (good for speech recognition)
        audio_segment = audio_segment.set_frame_rate(16000)
        
        # Calculate number of chunks
        total_chunks = len(audio_segment) // chunk_length + (1 if len(audio_segment) % chunk_length > 0 else 0)
        print(f"Processing audio in {total_chunks} chunks...")

        # Process each chunk
        for i, chunk_start in enumerate(range(0, len(audio_segment), chunk_length)):
            print(f"Processing chunk {i+1}/{total_chunks}...")
            chunk = audio_segment[chunk_start:chunk_start + chunk_length]
            
            # Export chunk to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_chunk:
                chunk.export(temp_chunk.name, format='wav')
                
                # Transcribe chunk
                with sr.AudioFile(temp_chunk.name) as source:
                    audio = r.record(source)
                    try:
                        text = r.recognize_google(audio, language=language_code)
                        full_text.append(text)
                        print(f"Chunk {i+1} transcribed successfully.")
                    except sr.UnknownValueError:
                        print(f"Chunk {i+1}: No speech detected.")
                    except sr.RequestError as e:
                        print(f"Chunk {i+1}: Error with the request; {e}")
                
            # Clean up temporary chunk file
            os.unlink(temp_chunk.name)

        # Clean up the temporary WAV file if we created one
        if not audio_file_path.lower().endswith('.wav'):
            os.unlink(audio_file_path)
            
        if full_text:
            print("Transcription successful.")
            return " ".join(full_text)
        else:
            print("No text was transcribed from any chunk.")
            return None
    
    except sr.WaitTimeoutError:
        print("Error: No speech detected in the audio.")
        return None
    except sr.UnknownValueError:
        print("Error: Google Speech Recognition could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Error: Could not request results from Google Speech Recognition service; {e}")
        return None
    except FileNotFoundError:
        print(f"Error: Audio file not found at {audio_file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during transcription: {e}")
        return None

def summarize_text_with_gemini(text_transcript, language_name):
    """
    Sends the transcribed text to the Gemini model for a summary.
    
    Args:
        text_transcript (str): The text to be summarized.
        language_name (str): The name of the language (e.g., 'French', 'English').
        
    Returns:
        str: The summary from the Gemini model, or None if an error occurs.
    """
    print("\nConnecting to Gemini...")
    try:
        # Configure the Gemini API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise Exception("GOOGLE_API_KEY environment variable is not set. Get your API key from https://makersuite.google.com/app/apikey")
        
        # Configure the API
        configuration = genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash', generation_config={
            "temperature": 0.7,
            "max_output_tokens": 2048,
        })
        
        # Define the prompt for summarization
        prompt = (
            f"Please provide a concise and comprehensive summary of the following {language_name} text. "
            f"The summary should be in {language_name}. Format the output as follows:\n"
            f"1. Start with 'RÉSUMÉ:' followed by a brief overview paragraph\n"
            f"2. Use 'THÈMES PRINCIPAUX:' as a section heading for main topics\n"
            f"3. Use 'DÉTAILS CLÉS:' as a section heading for key details\n"
            f"4. Use regular bullet points (•) for lists\n"
            f"5. Do not use any special formatting (no markdown, no **, no italics)\n"
            f"6. Use clear section breaks with newlines\n\n"
            f"The text is a transcript from a {language_name} audio recording:\n\n"
            f"--- TEXT START ---\n{text_transcript}\n--- TEXT END ---"
        )

        print("Generating summary...")
        
        # Call the Gemini API
        response = model.generate_content(prompt)
        
        print("Summary generation successful.")
        return response.text

    except Exception as e:
        print(f"An error occurred while communicating with the Gemini API: {e}")
        return None

# --- Main Execution Block ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Use the audio file path provided as command line argument
        AUDIO_FILE = sys.argv[1]
    else:
        print("Please provide the path to your audio file as a command line argument.")
        print("Example: python audioToText.py path/to/your/audio.m4a")
        sys.exit(1)
    
    # Convert the file path to absolute path
    AUDIO_FILE = str(Path(AUDIO_FILE).resolve())
    
    # Get the language from user input
    language_code, language_name = get_language_code()
    
    # 1. Transcribe the audio
    transcript = transcribe_audio(AUDIO_FILE, language_code)
    
    if transcript:
        print("\n--- FULL TRANSCRIPT ---")
        print(transcript)
        print("-----------------------")
        
        # 2. Summarize the transcript with Gemini
        summary = summarize_text_with_gemini(transcript, language_name)
        
        if summary:
            print("\n===========================================")
            print("                 RÉSUMÉ                    ")
            print("===========================================\n")
            print(summary)
        else:
            print("\nCould not generate a summary.")
    else:
        print("\nProcess stopped. Could not get a usable transcript.")
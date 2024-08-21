import sounddevice as sd
import numpy as np
import io
import speech_recognition as sr
import scipy.io.wavfile as wav


def record_audio(duration, fs, channels):
    """Record audio for a specified duration and sample rate."""
    print("Recording Audio...")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='float64')
        sd.wait()  # Wait until recording is finished
        print("Audio recording complete.")
        return recording
    except Exception as e:
        print(f"Recording error: {e}")
        return None


def audio_to_wav_bytes(audio, fs):
    """Convert recorded audio to WAV format in memory."""
    try:
        audio_int16 = np.int16(audio * 32767)
        buffer = io.BytesIO()
        wav.write(buffer, fs, audio_int16)
        buffer.seek(0)  # Rewind the buffer to the beginning
        return buffer
    except Exception as e:
        print(f"Conversion error: {e}")
        return None


def recognize_speech(audio_buffer):
    """Recognize speech from an audio buffer."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_buffer) as source:
            audio_data = recognizer.listen(source)
            text = recognizer.recognize_google(audio_data)
            print("Transcribing audio...")
            print(text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
    except Exception as e:
        print(f"Recognition error: {e}")


def main():
    fs = 44100  # Sample rate
    duration = 5  # Duration in seconds
    channels = 2  # Number of audio channels (stereo)

    # Record audio
    my_recording = record_audio(duration, fs, channels)
    if my_recording is None:
        return

    # Convert to WAV format in memory and recognize speech
    audio_buffer = audio_to_wav_bytes(my_recording, fs)
    if audio_buffer is None:
        return

    recognize_speech(audio_buffer)


if __name__ == "__main__":
    main()
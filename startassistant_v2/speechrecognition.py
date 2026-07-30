import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
import threading
import queue
import sys
import signal
import time

# Disable VOSK logs
SetLogLevel(-1)

class AudioProcessor:
    def __init__(self):
        print("Loading Vosk model...")
        self.model = Model(model_name="vosk-model-small-en-us-0.15")
        self.rec = KaldiRecognizer(self.model, 16000)
        print("Model loaded")

        self.audio_queue = queue.Queue(maxsize=2)
        self.sample_rate = 16000
        self.is_running = True
        self.partial_buffer = ""

    def input_callback(self, indata, frames, time_info, status):
        if self.is_running:
            try:
                self.audio_queue.put_nowait(bytes(indata))
            except queue.Full:
                print("QUEUE IS FULL")
                pass

    def process_audio(self):
        while self.is_running:
            try:
                data = self.audio_queue.get()
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "").strip()
                    if text:
                        # Clear the line and show final result
                        print(f"\r{' ' * len(self.partial_buffer)}", end='', flush=True)
                        print(f"\r{text}", flush=True)
                        self.partial_buffer = ""
                else:
                    partial = json.loads(self.rec.PartialResult())
                    text = partial.get("partial", "").strip()
                    if text and text != self.partial_buffer:
                        # Update buffer and show intermediate result
                        print(f"\r{' ' * len(self.partial_buffer)}", end='', flush=True)
                        print(f"\r{text}", end='', flush=True)
                        self.partial_buffer = text

            except queue.Empty:
                continue
            except Exception as e:
                print(f"\nError: {e}")

    def start_recording(self):
        print("\nStarting speech recognition")
        print("===========================")
        print("Speak into the microphone...")
        print("Ctrl+C to exit\n")

        process_thread = threading.Thread(target=self.process_audio)
        process_thread.daemon = True
        process_thread.start()

        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                #device=3,
                dtype='int16',
                channels=1,
                callback=self.input_callback
            ):
                while self.is_running:
                    time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nStopping recording...")
        finally:
            self.stop()
            process_thread.join(timeout=1.0)
            print("Recording stopped")

    def stop(self):
        self.is_running = False
        self.rec = None
        self.model = None

def main():
    processor = AudioProcessor()
    signal.signal(signal.SIGINT, lambda s, f: processor.stop())
    processor.start_recording()

if __name__ == "__main__":
    main()
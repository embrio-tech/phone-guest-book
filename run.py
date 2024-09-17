import RPi.GPIO as GPIO
import time
import pyaudio
import wave
import os
import logging
import signal
import threading

class Recorder:
    def __init__(self):
        # Set the GPIO mode to BCM
        GPIO.setmode(GPIO.BCM)

        # Define the GPIO pin you want to read
        self.PIN = 4  # Change this to the GPIO pin number you're using
        self.DEBOUNCE_TIME = 200  # Debounce time in milliseconds

        # Set up the pin as an input
        GPIO.setup(self.PIN, GPIO.IN)

        # PyAudio configuration
        self.CHUNK = 4096  # Increase from default 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 5

        # Instance variables
        self.recording = False
        self.frames = []
        self.audio = None
        self.stream = None

        # Set up logging
        logging.basicConfig(level=logging.DEBUG)

        self.intro_file = "intro.wav"
        self.playing_intro = False
        self.intro_thread = None

    def play_intro(self):
        self.playing_intro = True
        wf = wave.open(self.intro_file, 'rb')
        p = pyaudio.PyAudio()
        
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        output_device_index=1,
                        stream_callback=callback)

        stream.start_stream()

        while stream.is_active() and self.playing_intro:
            time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()
        self.playing_intro = False

    def start_recording(self):
        self.frames = []
        try:
            if self.audio is None:
                self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
                input_device_index=1,
            )
            logging.info("Audio stream successfully initialized")
            if not self.recording:
                self.recording = True
                print("Recording started")
        except Exception as e:
            logging.error(f"Failed to initialize audio stream: {e}")
            self.stream = None
            self.audio = None

    def state_change_callback(self, channel):
        state = GPIO.input(channel)
        if state:  # HIGH
            print("Telephone receiver picked up")
            self.intro_thread = threading.Thread(target=self.play_intro)
            self.intro_thread.start()
            self.intro_thread.join()  # Wait for intro to finish
            if GPIO.input(channel):  # Check if still HIGH after intro
                self.start_recording()
            else:
                print("Receiver hung up before recording could start")
        else:  # LOW
            print("Telephone receiver hung up")
            self.playing_intro = False  # Stop intro if it's still playing
            if self.intro_thread and self.intro_thread.is_alive():
                self.intro_thread.join()  # Wait for intro thread to finish
            self.stop_recording()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            print("Recording stopped")
            if self.audio is not None:
                self.save_recording()
            else:
                logging.error("Audio object is None. Unable to save recording.")

    def save_recording(self):
        if self.frames:
            try:
                if self.audio is None:
                    logging.error("Audio object is None. Unable to save recording.")
                    return

                filename = f"/home/wedding/Recordings/recording_{time.strftime('%Y%m%d-%H%M')}.wav"
                wf = wave.open(filename, "wb")
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b"".join(self.frames))
                wf.close()
                print(f"Recording saved as {filename}")
            except Exception as e:
                logging.error(f"Error saving recording: {e}")
            finally:
                # Reset audio and stream after saving
                if self.audio:
                    self.audio.terminate()
                self.audio = None
                self.stream = None
        else:
            logging.warning("No frames to save.")

    def cleanup(self, signum=None, frame=None):
        print("Cleaning up...")
        if self.recording:
            self.stop_recording()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        GPIO.cleanup()
        print("Cleanup complete.")
        exit(0)

    def run(self):
        try:
            print(f"Monitoring GPIO pin {self.PIN}. Press CTRL+C to exit.")
            # Set up event detection for both rising and falling edges
            GPIO.add_event_detect(
                self.PIN, GPIO.BOTH, callback=self.state_change_callback, bouncetime=self.DEBOUNCE_TIME
            )

            # Register the cleanup function for various signals
            signal.signal(signal.SIGINT, self.cleanup)
            signal.signal(signal.SIGTERM, self.cleanup)

            # Keep the script running
            while True:
                if self.recording:
                    try:
                        data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                        self.frames.append(data)
                    except OSError as e:
                        print(f"Error reading from stream: {e}")
                        self.stop_recording()
                time.sleep(0.01)

        except KeyboardInterrupt:
            print("Exiting...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cleanup()

if __name__ == "__main__":
    recorder = Recorder()
    recorder.run()

import pyaudio
import numpy as np
import math
import time
from gtts import gTTS
import os
import pygame
import threading

class SuddenAccelerationAlert:
    SAMPLE_RATE = 44100
    
    @staticmethod
    def calculate_arrival_time(speed, distance):
        """Calculate time to arrival in seconds based on speed (km/h) and distance (m)"""
        # Convert speed from km/h to m/s
        speed_ms = speed * (1000 / 3600)
        
        # Calculate time in seconds
        if speed_ms <= 0:
            return float('inf')  # Avoid division by zero
        
        time_to_arrival = distance / speed_ms
        return time_to_arrival
    
    @staticmethod
    def generate_sweep_tone(start_freq, end_freq, duration_ms, volume=1.0):
        """Generate a smooth frequency sweep from start_freq to end_freq"""
        samples = int(duration_ms * SuddenAccelerationAlert.SAMPLE_RATE / 1000)
        audio = np.zeros(samples, dtype=np.float32)
        
        for i in range(samples):
            # Linear interpolation between frequencies
            t = i / samples
            current_freq = start_freq + (end_freq - start_freq) * t
            
            # Generate sine wave at current frequency
            sample = math.sin(2 * math.pi * current_freq * i / SuddenAccelerationAlert.SAMPLE_RATE) * volume
            audio[i] = sample
            
        return audio
    
    @staticmethod
    def play_audio(audio):
        """Play audio data through PyAudio"""
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=SuddenAccelerationAlert.SAMPLE_RATE,
                        output=True)
        
        stream.write(audio.astype(np.float32).tobytes())
        
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    @staticmethod
    def play_approaching_alert(speed, distance):
        """Play alert for approaching vehicle - pulsing high-pitched beeps"""
        # Calculate parameters based on speed and distance
        volume = SuddenAccelerationAlert.get_volume(distance)
        frequency = 2000  # Higher frequency for approaching vehicle
        beep_duration = 100  # 0.1 second beep duration
        pulse_interval = 700  # 0.7 seconds between start of each beep
        num_beeps = 3  # Number of beeps to play
        
        # Generate and play multiple beeps with interval
        for i in range(num_beeps):
            beep = SuddenAccelerationAlert.generate_beep(frequency, beep_duration, volume)
            SuddenAccelerationAlert.play_audio(beep)
            
            # Don't wait after the last beep
            if i < num_beeps - 1:
                time.sleep(pulse_interval / 1000)  # Convert to seconds
    
    @staticmethod
    def play_departing_alert(speed, distance):
        """Play alert for departing vehicle - pulsing low-pitched beeps"""
        # Calculate parameters based on speed and distance
        volume = SuddenAccelerationAlert.get_volume(distance)
        frequency = 500  # Lower frequency for departing vehicle
        beep_duration = 100  # 0.1 second beep duration
        pulse_interval = 700  # 0.7 seconds between start of each beep
        num_beeps = 3  # Number of beeps to play
        
        # Generate and play multiple beeps with interval
        for i in range(num_beeps):
            beep = SuddenAccelerationAlert.generate_beep(frequency, beep_duration, volume)
            SuddenAccelerationAlert.play_audio(beep)
            
            # Don't wait after the last beep
            if i < num_beeps - 1:
                time.sleep(pulse_interval / 1000)  # Convert to seconds
        
    @staticmethod
    def generate_beep(frequency, duration_ms, volume=1.0):
        """Generate a simple beep tone at specified frequency"""
        samples = int(duration_ms * SuddenAccelerationAlert.SAMPLE_RATE / 1000)
        audio = np.zeros(samples, dtype=np.float32)
        
        for i in range(samples):
            # Generate sine wave at fixed frequency
            sample = math.sin(2 * math.pi * frequency * i / SuddenAccelerationAlert.SAMPLE_RATE) * volume
            audio[i] = sample
            
        return audio
    
    @staticmethod
    def get_volume(distance):
        """Calculate volume based on distance"""
        max_distance = 1000.0
        min_distance = 10.0
        volume_range = 1.0 - 0.1
        
        if distance <= min_distance:
            return 1.0
        elif distance >= max_distance:
            return 0.1
        else:
            return 1.0 - (distance - min_distance) * volume_range / (max_distance - min_distance)
    
    @staticmethod
    def countdown(seconds):
        """Count down from the given number of seconds"""
        # Round to nearest integer and ensure positive
        seconds = max(0, round(seconds))
        
        # Only countdown if we have at least 1 second
        if seconds >= 1:
            # Count down from seconds to 1
            for i in range(seconds, 0, -1):
                VoiceAlert.speak_countdown(i)
                # Wait exactly 1 second between counts
                if i > 1:  # Don't wait after the last number
                    time.sleep(1)
    
    @staticmethod
    def alert(speed, approaching, distance):
        """Main alert method that decides which alert to play"""
        # Calculate time to arrival if approaching
        if approaching:
            arrival_time = SuddenAccelerationAlert.calculate_arrival_time(speed, distance)
            
            # If vehicle will arrive within a reasonable time (<=10 seconds)
            # and is actually approaching (not stationary)
            if arrival_time <= 10 and arrival_time > 0:
                # Round to nearest second for countdown
                countdown_seconds = min(int(arrival_time), 10)
                print(f"Vehicle approaching! Arrival in approximately {countdown_seconds} seconds")
                
                # First play the approaching alert tones
                SuddenAccelerationAlert.play_approaching_alert(speed, distance)
                
                # Then play the danger alert
                VoiceAlert.speak_danger_alert()
                
                # Finally do the countdown if we have more than 1 second
                if countdown_seconds >= 1:
                    SuddenAccelerationAlert.countdown(countdown_seconds)
            else:
                # Just play approaching alert + danger for vehicles that are farther away
                SuddenAccelerationAlert.play_approaching_alert(speed, distance)
                VoiceAlert.speak_danger_alert()
        else:
            # For departing vehicles, play tones first then safety alert
            SuddenAccelerationAlert.play_departing_alert(speed, distance)
            VoiceAlert.speak_safety_alert()

class VoiceAlert:
    @staticmethod
    def speak_danger_alert():
        """Generate and play 'DANGER' voice alert"""
        # English native voice TTS generation
        tts = gTTS(text="Danger danger", lang='en', tld='com')
        
        # Save to temporary file
        alert_file = "danger_alert.mp3"
        tts.save(alert_file)
        
        try:
            # Play with pygame
            pygame.mixer.init()
            pygame.mixer.music.load(alert_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
        except Exception as e:
            print(f"Error playing danger alert: {e}")
            
        finally:
            # Give a small delay before trying to remove the file
            time.sleep(0.1)
            
            try:
                # Try to remove the file, but don't crash if it fails
                if os.path.exists(alert_file):
                    os.remove(alert_file)
            except Exception as e:
                print(f"Note: Could not remove temporary file {alert_file}. It will be cleaned up later.")
    
    @staticmethod
    def speak_safety_alert():
        """Generate and play 'SAFE' voice alert"""
        # English native voice TTS generation
        tts = gTTS(text="Safe safe", lang='en', tld='com')
        
        # Save to temporary file
        alert_file = "safe_alert.mp3"
        tts.save(alert_file)
        
        try:
            # Play with pygame
            pygame.mixer.init()
            pygame.mixer.music.load(alert_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
        except Exception as e:
            print(f"Error playing safety alert: {e}")
            
        finally:
            # Give a small delay before trying to remove the file
            time.sleep(0.1)
            
            try:
                # Try to remove the file, but don't crash if it fails
                if os.path.exists(alert_file):
                    os.remove(alert_file)
            except Exception as e:
                print(f"Note: Could not remove temporary file {alert_file}. It will be cleaned up later.")
    
    @staticmethod
    def speak_countdown(seconds):
        """Generate and play countdown voice (3, 2, 1, etc.)"""
        # English native voice TTS generation
        tts = gTTS(text=str(seconds), lang='en', tld='com')
        
        # Save to temporary file
        countdown_file = f"countdown_{seconds}.mp3"
        tts.save(countdown_file)
        
        try:
            # Play with pygame
            pygame.mixer.init()
            pygame.mixer.music.load(countdown_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
        except Exception as e:
            print(f"Error playing countdown: {e}")
            
        finally:
            # Give a small delay before trying to remove the file
            time.sleep(0.1)
            
            try:
                # Try to remove the file, but don't crash if it fails
                if os.path.exists(countdown_file):
                    os.remove(countdown_file)
            except Exception as e:
                print(f"Note: Could not remove temporary file {countdown_file}. It will be cleaned up later.")

if __name__ == "__main__":
    # Example 1: Speed 90 km/h, approaching vehicle, distance 100m (=4 seconds at 90km/h)
    print("Example 1: Approaching vehicle, 90km/h, 100m distance")
    SuddenAccelerationAlert.alert(90, True, 100)
    
    # Wait a few seconds between examples
    time.sleep(5)
    
    # Example 2: Speed 110 km/h, departing vehicle, distance 500m
    print("Example 2: Departing vehicle, 110km/h, 500m distance")
    SuddenAccelerationAlert.alert(110, False, 500)
    
    # Wait a few seconds between examples
    time.sleep(5)
    
    # Example 3: Fast approaching vehicle, 3-second arrival time
    print("Example 3: Fast approaching vehicle, 120km/h, 100m distance (3 seconds to arrival)")
    SuddenAccelerationAlert.alert(120, True, 100)
    
    # Wait a few seconds between examples
    time.sleep(5)
    
    # Example 4: Very close approaching vehicle, 1-second arrival time
    print("Example 4: Very close approaching vehicle, 108km/h, 30m distance (1 second to arrival)")
    SuddenAccelerationAlert.alert(108, True, 30)
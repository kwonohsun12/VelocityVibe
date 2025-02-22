import pyaudio
import numpy as np
import time

class SoundEffect:
    @staticmethod
    def play_acceleration_sound(duration=1.0, start_freq=220.0, end_freq=880.0):
        p = pyaudio.PyAudio()
        
        # 오디오 스트림 설정
        sample_rate = 44100  # 샘플링 레이트
        samples = int(duration * sample_rate)
        
        # 시간에 따라 주파수가 증가하는 사인파 생성
        t = np.linspace(0, duration, samples)
        frequency = np.exp(np.linspace(np.log(start_freq), np.log(end_freq), samples))
        
        # 부드러운 시작과 끝을 위한 페이드 인/아웃
        fade = 0.1  # 페이드 시간 (초)
        fade_length = int(fade * sample_rate)
        fade_in = np.linspace(0, 1, fade_length)
        fade_out = np.linspace(1, 0, fade_length)
        
        # 전체 볼륨 엔벨로프 생성
        envelope = np.ones(samples)
        envelope[:fade_length] = fade_in
        envelope[-fade_length:] = fade_out
        
        # 최종 사운드 생성
        tone = np.sin(2 * np.pi * frequency * t)
        tone = tone * envelope * 0.5  # 0.5는 볼륨을 조절하는 계수
        
        # 스테레오로 변환
        stereo_tone = np.vstack((tone, tone)).T
        
        # 오디오 스트림 열기 및 재생
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=2,
            rate=sample_rate,
            output=True
        )
        
        # float32로 변환하여 재생
        stream.write(stereo_tone.astype(np.float32).tobytes())
        
        # 스트림 정리
        stream.stop_stream()
        stream.close()
        p.terminate()

# 사용 예시:
# SoundEffect.play_acceleration_sound(duration=1.5, start_freq=220.0, end_freq=880.0)


# 가속 시작할 때
SoundEffect.play_acceleration_sound(
    duration=1.5,  # 소리 길이 (초)
    start_freq=220.0,  # 시작 주파수 (Hz)
    end_freq=880.0  # 종료 주파수 (Hz)
)
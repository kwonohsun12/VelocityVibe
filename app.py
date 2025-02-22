import numpy as np
import sounddevice as sd

# 오디오 매개변수 설정
duration = 5  # 재생 시간 (초)
frequency = 440  # 주파수 (Hz)
sample_rate = 44100  # 샘플링 레이트 (Hz)

# 사인파 생성
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio = np.sin(2 * np.pi * frequency * t)

# 소리 재생
sd.play(audio, sample_rate)
sd.wait()  # 재생이 완료될 때까지 대기
import math
import pyaudio

class SuddenAccelerationAlert:
    SAMPLE_RATE = 44100
    TONE_DURATION = 200

    @staticmethod
    def play_accel_sound(speed, approaching, distance):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=SuddenAccelerationAlert.SAMPLE_RATE,
                        output=True)

        frequency = SuddenAccelerationAlert.get_frequency(speed, approaching)
        volume = SuddenAccelerationAlert.get_volume(distance)

        for i in range(int(SuddenAccelerationAlert.TONE_DURATION * SuddenAccelerationAlert.SAMPLE_RATE / 1000)):
            angle = i / (SuddenAccelerationAlert.SAMPLE_RATE / frequency) * 2.0 * math.pi
            sample = math.sin(angle) * volume
            stream.write(sample.to_bytes(4, byteorder='little', signed=True))

        stream.stop_stream()
        stream.close()
        p.terminate()

    @staticmethod
    def get_frequency(speed, approaching):
        base_frequency = 500
        max_frequency = 2000
        frequency_range = max_frequency - base_frequency

        if speed >= 100:
            return max_frequency
        elif speed >= 80:
            if approaching:
                return base_frequency + (speed - 80) * frequency_range // 20
            else:
                return max_frequency - (speed - 80) * frequency_range // 20
        else:
            return base_frequency

    @staticmethod
    def get_volume(distance):
        max_distance = 1000.0
        min_distance = 10.0
        volume_range = 1.0 - 0.1

        if distance <= min_distance:
            return 1.0
        elif distance >= max_distance:
            return 0.1
        else:
            return 1.0 - (distance - min_distance) * volume_range / (max_distance - min_distance)


if __name__ == "__main__":
    # 예시: 속도 90 km/h, 다가오는 차량, 거리 100m
    SuddenAccelerationAlert.play_accel_sound(90, True, 100)

    # 예시: 속도 110 km/h, 멀어지는 차량, 거리 500m
    SuddenAccelerationAlert.play_accel_sound(110, False, 500)
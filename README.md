# VelocityVibe

This project aims to develop a system that detects sudden acceleration of vehicles and provides notifications to users. 
When a sudden acceleration event occurs in the radar system, relevant parameters are sent via an API. 
The system receives these parameters and plays an alert sound to notify the user. I will write python code by receiving parameters from the radar API.

이 프로젝트는 자동차의 급발진을 감지하고 사용자에게 알림을 제공하는 로직을 파이썬으로 구현하는 프로젝트입니다.
레이더 시스템에서 급발진 이벤트가 발생했을 때 관련 매개변수를 API를 통해 전송하면, 이를 받아 사용자에게 알림음을 재생하여 전달하는 기능입니다.

1. 1km미만 거리에서 자신에게 다가오는 차가 레이더에서 감지되는 경우, 80~100km/h 구간에서는 비프음이 낮은음에서 높은음으로 연속 비프알림음
2. 100km/h이상일 경우 더 높은음에서 연속 비프알림음 
3. 자신에게 멀어지는 경우의 알림은 상기의 역펄스 알림음으로 구현

# cmd
pip install sounddevice
pip install numpy
pip install pyaudio
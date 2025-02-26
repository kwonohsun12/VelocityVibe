# VelocityVibe: Rapid Acceleration Detection & Alert (2025.02.22~)

This project aims to develop a system that detects sudden acceleration of vehicles and provides notifications to users. 
When a sudden acceleration event occurs in the radar system, relevant parameters are sent via an API. 
The system receives these parameters and plays an alert sound to notify the user. I will write python code by receiving parameters from the radar API.

이 프로젝트는 자동차의 급발진을 감지하고 사용자에게 알림을 제공하는 로직을 파이썬으로 구현하는 프로젝트입니다.
레이더 시스템에서 급발진 이벤트가 발생했을 때 관련 매개변수를 API를 통해 전송하면, 이를 받아 사용자에게 알림음을 재생하여 전달하는 기능입니다.

I am currently developing through Claude AI and continuously improving notification patterns to effectively help users avoid dangerous situations.

claude ai를 통해 개발중이며 사용자에게 효과적으로 전달할 알림패턴을 지속적으로 개선중에 있습니다.

# Process

![Image](https://github.com/user-attachments/assets/2844f1f2-9917-4cec-aeb9-4c5f283587d0)

# Required Packages

| Package     | Version |
| ----------- | ------- |
| gTTS        | 2.5.4   |
| numpy       | 2.2.3   |
| PyAudio     | 0.2.14  |
| pyttsx3     | 2.98    |
| sounddevice | 0.5.1   |


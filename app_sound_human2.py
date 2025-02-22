from gtts import gTTS
import os
import pygame

class VoiceAlert:
    @staticmethod
    def speak_danger_alert():
        # 영어 원어민 목소리로 TTS 생성
        tts = gTTS(text="Danger danger", lang='en', tld='com')
        
        # 임시 파일로 저장
        tts.save("danger_alert.mp3")
        
        # pygame으로 재생
        pygame.mixer.init()
        pygame.mixer.music.load("danger_alert.mp3")
        pygame.mixer.music.play()
        
        # 재생이 끝날 때까지 대기
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # 임시 파일 삭제
        os.remove("danger_alert.mp3")
        
# 위험 상황 발생시
VoiceAlert.speak_danger_alert()
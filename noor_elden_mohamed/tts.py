import asyncio
import edge_tts
import pygame
import uuid
import os
import threading
import time

VOICE = "ar-EG-SalmaNeural"

pygame.mixer.init()


async def _generate_audio(text, filename):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate="+0%",
        volume="+0%"
    )
    await communicate.save(filename)


def _play_audio(filename):
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove(filename)

    except Exception as e:
        print("❌ خطأ في تشغيل الصوت:", e)


def speak(text):
    def run():
        filename = f"voice_{uuid.uuid4().hex}.mp3"

        asyncio.run(_generate_audio(text, filename))

        print(f"🔊 النضارة تقول: {text}")

        _play_audio(filename)

    threading.Thread(target=run, daemon=True).start()


# ✨ ميزة جديدة: إيقاف الصوت فوراً
def stop_speaking():
    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
    except:
        pass


if __name__ == "__main__":
    speak("مرحباً بك. النظام الصوتي يعمل الآن.")
    input("اضغط Enter للخروج")
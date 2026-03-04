# tts.py - نسخة احترافية محسنة
import asyncio
import edge_tts
import pygame
import uuid
import os
import threading
import time

VOICE = "ar-EG-SalmaNeural"

# تهيئة مشغل الصوت مرة واحدة فقط (تحسين أداء)
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

        # انتظار انتهاء الصوت
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()

        # حذف الملف بعد التشغيل
        os.remove(filename)

    except Exception as e:
        print("❌ خطأ أثناء تشغيل الصوت:", e)

def speak(text):
    def run():
        filename = f"voice_{uuid.uuid4().hex}.mp3"
        asyncio.run(_generate_audio(text, filename))
        print(f"🔊 النضارة تقول: {text}")
        _play_audio(filename)

    # تشغيل في Thread مستقل (تحسين أداء)
    threading.Thread(target=run, daemon=True).start()


if __name__ == "__main__":
    speak("أهلاً بك يا نور الدين. أنا مستعدة لمساعدة صديقنا الكفيف.")
    input("اضغط Enter للخروج...")
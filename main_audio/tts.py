import asyncio
import edge_tts
import pygame
import uuid
import os
import threading
import queue

VOICE = "ar-EG-SalmaNeural"
voice_queue = queue.Queue()

def init_mixer():
    if not pygame.mixer.get_init():
        pygame.mixer.init()

async def _generate_audio(text, filename):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate="-5%",
        volume="+10%"
    )
    await communicate.save(filename)

def _play_audio(filename):
    try:
        init_mixer()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(10)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        print("❌ خطأ أثناء تشغيل الصوت:", e)

def _audio_worker():
    while True:
        text, done_event = voice_queue.get()
        filename = f"voice_{uuid.uuid4().hex}.mp3"
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_generate_audio(text, filename))
            loop.close()
            print(f"🔊 النضارة تقول: {text}")
            _play_audio(filename)
        except Exception as e:
            print("❌ خطأ في TTS:", e)
        finally:
            voice_queue.task_done()
            if done_event:
                done_event.set()  # السماح للرسالة التالية بالبدء

# تشغيل Thread مرة واحدة عند استيراد الملف
audio_thread = threading.Thread(target=_audio_worker, daemon=True)
audio_thread.start()

def speak(text):
    """
    استدعاء الصوت بشكل blocking:
    تنتظر انتهاء الرسالة قبل السماح للرسالة التالية
    """
    done_event = threading.Event()
    voice_queue.put((text, done_event))
    done_event.wait()  # ← تنتظر انتهاء الصوت قبل العودة

if __name__ == "__main__":
    speak("أهلاً بك يا نور الدين")
    speak("تم تشغيل نظام النظارة الذكية")
    speak("تم اكتشاف شخص أمامك")

    input("اضغط Enter للخروج...")
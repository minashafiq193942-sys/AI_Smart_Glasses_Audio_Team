# stt.py - مينا شفيق

import speech_recognition as sr

def test_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(">>> المايك شغال.. اتكلم دلوقتي يا مينا!")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5)
            print(">>> جاري ترجمة كلامك...")
            text = recognizer.recognize_google(audio, language='ar-EG')
            print(f"✅ أنت قلت: {text}")
        except Exception as e:
            print(f"❌ حصل مشكلة: {e}")

if __name__ == "__main__":
    test_mic()
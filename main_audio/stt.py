import speech_recognition as sr

def listen_and_process():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n>>> أنا سامعك يا بطل.. قول أمرك (أنا فين / مين قدامي / اقرا)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='ar-EG')
            print(f"✅ أنت قلت: {text}")
            
            # منطق تحليل الأوامر (Command Logic)
            if "فين" in text:
                print("🚀 تنفيذ أمر: تحديد الموقع")
                return "LOCATION"
            elif "مين" in text or "شخص" in text:
                print("🚀 تنفيذ أمر: التعرف على الوجوه")
                return "FACE_ID"
            elif "اقرأ" in text or "كتاب" in text:
                print("🚀 تنفيذ أمر: القراءة الذكية")
                return "READING"
            else:
                print("🤔 أمر غير معروف، حاول تاني.")
                return None
                
        except Exception as e:
            print("❌ مسمعتش كويس، ممكن تعيد؟")
            return None

if __name__ == "__main__":
    while True:
        command = listen_and_process()
        if command:
            print(f"--- إرسال الإشارة للفريق المختص: {command} ---")
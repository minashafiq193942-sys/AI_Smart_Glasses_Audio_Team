import stt  # ملف مينا
import tts  # ملف نور
import time

def start_interaction():
    # 1. النضارة ترحب بالمستخدم أول ما تفتح
    tts.speak("أهلاً بك يا بطل، أنا نضارتك الذكية. أنا الآن أسمع أوامرك.")
    time.sleep(4) # وقت بسيط عشان تخلص الترحيب

    while True:
        # 2. مينا يبدأ يسمع
        command = stt.listen_and_process()
        
        if command == "LOCATION":
            tts.speak("جاري تحديد موقعك الآن، انتظر لحظة.")
        
        elif command == "FACE_ID":
            tts.speak("جاري التعرف على الشخص الموجود أمامك.")
        
        elif command == "READING":
            tts.speak("حسناً، وجه الكاميرا نحو النص وسأقوم بقراءته لك.")
            
        elif command is None:
            # لو مسمعتش حاجة أو فيه خطأ
            continue

if __name__ == "__main__":
    start_interaction()
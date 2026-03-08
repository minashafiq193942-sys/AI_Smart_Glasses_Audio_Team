# audio_logic.py - مهاب محمد

import sys
import os
import threading
import queue
import time

# --- 1. حل مشكلة المسارات (بخلي الملف يشوف الفولدر الكبير) ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- 2. استدعاء ملفات الفريق (مينا، نور، منة) ---
try:
    from noor_elden_mohamed import tts  # ملف نور
    from main_audio import stt         # ملف مينا
    from menna_sayed import sos        # ملف منة
except ImportError as e:
    print(f"⚠️ تنبيه: فيه ملف ناقص في الفريق أو الاسم غلط: {e}")

class AudioLogicManager:
    def __init__(self):
        # طابور الرسائل العادية (عشان الكلام ميداخلش في بعضه)
        self.msg_queue = queue.Queue()
        self.is_running = True
        
        # تشغيل "عامل" في الخلفية يعالج الطابور
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def _process_queue(self):
        """بتراقب الطابور وتشغل الرسائل بالترتيب"""
        while self.is_running:
            try:
                # بيسحب الرسالة اللي عليها الدور
                message = self.msg_queue.get(timeout=1)
                tts.speak(message)
                # انتظار بسيط عشان الجمل تكون واضحة
                time.sleep(0.5)
                self.msg_queue.task_done()
            except (queue.Empty, NameError):
                continue

    def speak_normal(self, text):
        """للرسائل العادية: وصف مكان، قراءة كتاب، ترحيب"""
        print(f"📢 [Normal]: {text}")
        self.msg_queue.put(text)

    def speak_urgent(self, text):
        """للرسائل الطارئة: خطر، عربية، حفرة (بتقطع أي حاجة ثانية)"""
        print(f"🚨 [URGENT]: {text}")
        # بننادي speak مباشرة بدون طابور عشان تطلع فوراً
        tts.speak(f"تنبيه هام! {text}")

    def run_voice_command_loop(self):
        """الدالة الأساسية اللي بتربط كلام مينا برد فعل النضارة"""
        self.speak_normal("النظام جاهز، أنا أسمعك الآن.")
        
        while True:
            # مينا بيبدأ يسمع ويحلل
            command = stt.listen_and_process()
            
            if command == "LOCATION":
                self.speak_normal("جاري تحديد موقعك الحالي...")
                location_info = sos.get_current_location()
                self.speak_normal(f"أنت الآن في {location_info}")
                
            elif command == "FACE_ID":
                self.speak_normal("بدأت عملية التعرف على الوجوه، وجه الكاميرا للأمام.")
                
            elif command == "READING":
                self.speak_normal("أنا جاهزة للقراءة، من فضلك ثبت الورقة أمام الكاميرا.")
            
            elif command is None:
                # لو مسمعش حاجة يرجع يسمع تاني
                continue
            
            # استراحة بسيطة قبل اللفة اللي جاية
            time.sleep(1)

# --- 3. تشغيل التجربة ---
if __name__ == "__main__":
    manager = AudioLogicManager()
    try:
        # ابدأي التجربة فوراً
        manager.run_voice_command_loop()
    except KeyboardInterrupt:
        print("\nإغلاق النظام...")
        manager.is_running = False
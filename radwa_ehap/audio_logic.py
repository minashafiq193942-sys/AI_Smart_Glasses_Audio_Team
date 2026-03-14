import sys
import os
import threading
import queue
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from noor_elden_mohamed import tts
from main_audio import stt
from menna_sayed import sos
from local_ai import ask_ai


class AudioLogicManager:

    def __init__(self):

        self.msg_queue = queue.Queue()
        self.is_running = True

        self.worker_thread = threading.Thread(
            target=self._process_queue,
            daemon=True
        )

        self.worker_thread.start()

    def _process_queue(self):

        while self.is_running:
            try:

                message = self.msg_queue.get(timeout=1)

                tts.speak(message)

                time.sleep(0.5)

                self.msg_queue.task_done()

            except queue.Empty:
                continue

    def speak(self, text):

        print(f"📢 {text}")
        self.msg_queue.put(text)

    def speak_urgent(self, text):

        print(f"🚨 {text}")
        tts.speak(f"تنبيه! {text}")

    # ---------------------------
    # فهم الأوامر بذكاء
    # ---------------------------

    def detect_command(self, text):

        text = text.lower()

        # الموقع
        if any(word in text for word in ["فين", "مكاني", "موقعي"]):
            return "location"

        # التعرف على الاشخاص
        if any(word in text for word in ["مين", "شخص", "قدامي"]):
            return "face"

        # قراءة نص
        if any(word in text for word in ["اقرا", "اقرأ", "قراءة"]):
            return "read"

        # استغاثة
        if any(word in text for word in ["استغاثة", "ساعدني", "نجدة"]):
            return "sos"

        return "chat"

    # ---------------------------
    # تنفيذ الأوامر
    # ---------------------------

    def execute_command(self, command, text):

        if command == "location":

            self.speak("جاري تحديد موقعك")

            location = sos.get_current_location()

            self.speak(f"أنت الآن في {location}")

        elif command == "face":

            self.speak(
                "بدأت التعرف على الوجوه، وجه الكاميرا للأمام"
            )

        elif command == "read":

            self.speak(
                "أنا جاهزة للقراءة، ضع النص أمام الكاميرا"
            )

        elif command == "sos":

            self.speak_urgent("جاري إرسال استغاثة")

            sos.send_emergency_signal()

        elif command == "chat":

            print("💬 سؤال عادي")

            answer = ask_ai(text)

            print("🤖 AI:", answer)

            self.speak(answer)

    # ---------------------------
    # الحلقة الرئيسية
    # ---------------------------

    def run_voice_command_loop(self):

        self.speak("النظام جاهز. أنا أسمعك الآن.")

        while True:

            text = stt.listen_and_process()

            if text is None:

                self.speak("لم أفهم كلامك، حاول مرة أخرى")
                continue

            print("✅ أنت قلت:", text)

            command = self.detect_command(text)

            print("🧠 نوع الطلب:", command)

            self.execute_command(command, text)

            time.sleep(1)


if __name__ == "__main__":

    manager = AudioLogicManager()

    try:

        manager.run_voice_command_loop()

    except KeyboardInterrupt:

        print("إغلاق النظام")

        manager.is_running = False
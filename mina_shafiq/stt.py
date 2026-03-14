import speech_recognition as sr

recognizer = sr.Recognizer()

# تحسينات المايك
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8


def listen_and_process():

    with sr.Microphone() as source:

        print("\n🎤 أنا سامعك يا بطل.. قول أمرك")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:

            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)

            text = recognizer.recognize_google(audio, language="ar-EG")

            text = text.strip().lower()

            print("✅ أنت قلت:", text)

            # ------------------------------
            # كلمات الأوامر
            # ------------------------------

            location_words = [
                "فين",
                "انا فين",
                "احنا فين",
                "مكاني",
                "موقعي",
                "المكان"
            ]

            face_words = [
                "مين",
                "مين قدامي",
                "الشخص",
                "شخص",
                "ده مين"
            ]

            read_words = [
                "اقرأ",
                "اقرا",
                "كتاب",
                "النص",
                "اقرالي"
            ]

            sos_words = [
                "ساعدني",
                "استغاثه",
                "نجده",
                "الحقني"
            ]

            # ------------------------------
            # تحليل الكلام
            # ------------------------------

            for word in location_words:
                if word in text:
                    return "LOCATION"

            for word in face_words:
                if word in text:
                    return "FACE_ID"

            for word in read_words:
                if word in text:
                    return "READING"

            for word in sos_words:
                if word in text:
                    return "SOS"

            return None

        except sr.WaitTimeoutError:

            print("⌛ لم يتم سماع صوت")

            return None

        except sr.UnknownValueError:

            print("❌ لم أفهم الكلام")

            return None

        except sr.RequestError:

            print("⚠️ مشكلة في الاتصال بالإنترنت")

            return None

        except Exception as e:

            print("⚠️ خطأ:", e)

            return None


if __name__ == "__main__":

    while True:

        command = listen_and_process()

        print("Command:", command)
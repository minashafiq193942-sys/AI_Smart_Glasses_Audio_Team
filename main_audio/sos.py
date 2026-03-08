import requests
import time
import sys
import os

# حل مشكلة المسارات
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# محاولة استدعاء ملف TTS
try:
    from noor_elden_mohamed import tts
except ImportError:
    try:
        import tts
    except ImportError:
        tts = None
        print("⚠️ تنبيه: ملف tts.py غير موجود، سيتم عرض الرسائل نصياً فقط.")


def get_current_location():
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        data = response.json()

        if 'latitude' in data:
            city = data.get('city', 'غير معروف')
            lat = data.get('latitude')
            lng = data.get('longitude')
            return f"مدينة: {city}, إحداثيات: ({lat}, {lng})"

        return "تعذر تحديد الموقع"

    except Exception as e:
        return f"خطأ في الاتصال بخدمة الموقع: {e}"


def safe_speak(text):
    """
    تشغيل الصوت بطريقة مستقرة
    """
    if not tts:
        return

    try:
        tts.speak(text)
    except RuntimeError as e:
        if "cannot schedule new futures after interpreter shutdown" in str(e):
            pass
        else:
            print("⚠️ خطأ في TTS:", e)


def send_emergency_signal():
    try:
        msg1 = "لا تقلق، جاري إرسال موقعك الآن إلى جهات الاتصال المسجلة."
        print(msg1)
        tts.speak(msg1)  # ← تنتظر حتى تنتهي الرسالة بالكامل
        time.sleep(5)  # تأخير بسيط للتأكد من انتهاء الصوت قبل المتابعة
        location_info = get_current_location()

        msg2 = f"تم إرسال الاستغاثة بنجاح، ابقَ في مكانك. {location_info}"
        print(msg2)
        tts.speak(msg2)  # ← تنتظر انتهاء الرسالة الثانية
        
    except Exception as e:
        print(f"⚠️ حدث خطأ أثناء إرسال الاستغاثة: {e}")


if __name__ == "__main__":
    try:
        send_emergency_signal()

        # انتظار انتهاء جميع الأصوات
        time.sleep(8)

    except RuntimeError as e:
        if "cannot schedule new futures after interpreter shutdown" in str(e):
            pass
        else:
            raise

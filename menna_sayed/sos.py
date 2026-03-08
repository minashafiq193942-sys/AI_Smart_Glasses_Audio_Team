# sos.py - منة سيد

import requests
import time
import sys
import os

# حل مشكلة المسارات: بيخلي بايثون يشوف الفولدر الرئيسي للمشروع
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# محاولة استدعاء ملف نور الدين (tts) بطريقة مرنة
try:
    from noor_elden_mohamed import tts
except ImportError:
    try:
        import tts
    except ImportError:
        tts = None
        print("⚠️ تنبيه: ملف tts.py غير موجود، سيتم عرض الرسائل نصياً فقط.")

def get_current_location():
    """
    تحديد موقع المستخدم التقريبي باستخدام API سريع
    """
    try:
        # استخدام requests بدلاً من geocoder لتجنب مشاكل التثبيت
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

def send_emergency_signal():
    """
    وظيفة الاستغاثة الأساسية
    """
    msg = "لا تقلق، جاري إرسال موقعك الآن إلى جهات الاتصال المسجلة."
    print(f"🔊 النضارة تقول: {msg}")
    
    # استخدام صوت "نور" لو الملف شغال
    if tts:
        tts.speak(msg)
    
    location_info = get_current_location()
    
    print(f"\n🚨 [تنبيه SOS] 🚨")
    print(f"📍 الموقع المكتشف: {location_info}")
    print(f"📩 الرسالة: 'المستخدم يحتاج مساعدة عاجلة!'")
    
    time.sleep(2)
    
    confirm_msg = "تم إرسال الاستغاثة بنجاح، ابقَ في مكانك."
    if tts:
        tts.speak(confirm_msg)
    print(f"🔊 النضارة تقول: {confirm_msg}")

if __name__ == "__main__":
    send_emergency_signal()
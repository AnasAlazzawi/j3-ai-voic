# 🤖 Telegram AI Voice Assistant Bot

مساعد ذكي متقدم للتليجرام مع إمكانيات الذكاء الاصطناعي والتعامل مع الصوت

## ✨ الميزات الرئيسية

- 🎤 **تحويل الكلام إلى نص** - دعم العربية والإنجليزية
- 🔊 **تحويل النص إلى كلام** - 13 صوت مختلف
- 🤖 **ذكاء اصطناعي** - مدعوم بـ Google Gemini 2.0 Flash
- 💾 **ذاكرة المحادثة** - تحتفظ بالمحادثات لمدة 24 ساعة
- 🌐 **دعم متعدد اللغات** - عربي وإنجليزي
- 📱 **واجهة تفاعلية** - أزرار وقوائم سهلة الاستخدام

## 📁 هيكل المشروع

```
📦 telegram-ai-voice-bot/
├── 📄 main.py                 # البوت الرئيسي
├── 📄 config.py               # الإعدادات والثوابت
├── 📄 conversation_manager.py # إدارة المحادثات
├── 📄 processors.py           # معالجات الذكاء الاصطناعي والصوت
├── 📄 requirements.txt        # متطلبات المشروع
├── 📄 README.md              # وثائق المشروع
├── 📄 run_app.bat            # تشغيل على ويندوز
├── 📄 run_app.ps1            # تشغيل بـ PowerShell
└── 📄 conversations.json     # ملف المحادثات (يُنشأ تلقائياً)
```

## 🚀 التثبيت والتشغيل

### 1. تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### 2. إعداد المفاتيح

قم بتعديل الملف `config.py` وأضف مفاتيح API الخاصة بك:

```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

### 3. تشغيل البوت

#### على ويندوز:
```bash
# باستخدام الملف المدمج
run_app.bat

# أو مباشرة
python main.py
```

#### على لينكس/ماك:
```bash
python main.py
```

## 🔧 الملفات والوظائف

### `main.py`
الملف الرئيسي للبوت، يحتوي على:
- فئة `TelegramBot` الأساسية
- معالجات الأوامر والرسائل
- واجهة المستخدم والأزرار
- منطق التشغيل الرئيسي

### `config.py`
إعدادات وثوابت البوت:
- مفاتيح API والتوكنات
- قائمة الأصوات المتاحة
- إعدادات التعرف على الكلام
- إعدادات الذكاء الاصطناعي

### `conversation_manager.py`
إدارة المحادثات:
- حفظ وتحميل المحادثات من JSON
- إدارة تفضيلات المستخدمين
- تنظيف المحادثات القديمة
- عمليات CRUD للمحادثات

### `processors.py`
معالجات الذكاء الاصطناعي والصوت:
- `AIAssistant` - تفاعل مع Gemini AI
- `SpeechProcessor` - تحويل الكلام إلى نص
- `TTSProcessor` - تحويل النص إلى كلام
- `detect_language` - كشف لغة النص

## 🎯 الأوامر المتاحة

- `/start` - بدء البوت وإظهار القائمة الرئيسية
- `/help` - عرض معلومات المساعدة
- `/voice` - تغيير تفضيل الصوت
- `/clear` - مسح تاريخ المحادثة
- `/status` - عرض حالة البوت والإحصائيات

## 🎵 الأصوات المتاحة

`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`, `coral`, `verse`, `ballad`, `ash`, `sage`, `amuch`, `dan`

## 📋 أنماط التفاعل

1. **💬 النمط النصي** - رد نصي فقط
2. **🔊 النمط الصوتي** - رد صوتي فقط
3. **💬🔊 النمط المختلط** - رد نصي وصوتي معاً

## 🔒 الأمان

- مفاتيح API محفوظة في ملف منفصل
- تشفير البيانات الحساسة
- تنظيف تلقائي للمحادثات القديمة
- معالجة الأخطاء الشاملة

## 🛠️ التطوير والصيانة

### إضافة ميزات جديدة:
1. أضف الإعدادات في `config.py`
2. أضف المعالجات في `processors.py`
3. أضف الأوامر في `main.py`
4. حديث التوثيق

### اختبار البوت:
```bash
python main.py
```

### مراقبة الأخطاء:
تحقق من سجلات النظام في وحدة التحكم

## 🤝 المساهمة

نرحب بمساهماتك! يرجى:
1. إنشاء فرع جديد للميزة
2. إضافة الاختبارات المناسبة
3. تحديث التوثيق
4. إرسال طلب دمج

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف LICENSE للتفاصيل.

## 🆘 الدعم

إذا واجهت أي مشاكل:
1. تحقق من سجلات الأخطاء
2. تأكد من صحة مفاتيح API
3. تحقق من الاتصال بالإنترنت
4. راجع التوثيق

---

**تم تطوير البوت بـ ❤️ لخدمة المجتمع العربي**

### Method 2: Run the simple example
```bash
python simple_example.py
```

This runs basic examples including Arabic text conversion.

### Method 3: Use as a module
```python
from text_to_speech import TextToSpeechClient

# Initialize client
tts = TextToSpeechClient()

# Convert text to speech
result = tts.text_to_speech(
    prompt="Hello world!",
    voice="alloy",
    emotion="friendly"
)
print(result)
```

## API Functions

### `/text_to_speech_app`
Main function for converting text to speech.

**Parameters:**
- `prompt` (str, required): The text to convert to speech
- `voice` (str, default: "alloy"): Voice type
- `emotion` (str, required): Emotion style
- `use_random_seed` (bool, default: True): Whether to use random seed
- `specific_seed` (float, default: 12345): Specific seed value

### `/toggle_seed_input`
Toggle seed input setting.

**Parameters:**
- `use_random_seed` (bool, default: True): Whether to use random seed

## Examples

### Basic Usage
```python
from gradio_client import Client

client = Client("NihalGazi/Text-To-Speech-Unlimited")
result = client.predict(
    prompt="Hello world!",
    voice="alloy",
    emotion="friendly",
    use_random_seed=True,
    specific_seed=12345,
    api_name="/text_to_speech_app"
)
print(result)
```

### Arabic Text
```python
result = client.predict(
    prompt="مرحبا بكم في نظام تحويل النص إلى كلام",
    voice="nova",
    emotion="welcoming",
    use_random_seed=True,
    specific_seed=12345,
    api_name="/text_to_speech_app"
)
```

## Notes

- The application connects to a remote Hugging Face Space
- Internet connection is required
- Processing time depends on text length and server load
- Results are returned as audio file paths or data

## Troubleshooting

1. **Connection Issues**: Ensure you have a stable internet connection
2. **Package Issues**: Make sure gradio_client is properly installed
3. **API Errors**: Check if the Hugging Face Space is available and running

## Requirements

- Python 3.7+
- gradio_client>=0.8.0
- Internet connection

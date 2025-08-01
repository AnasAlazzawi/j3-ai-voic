# إعداد متغيرات البيئة | Environment Setup

## العربية

### خطوات الإعداد:

1. **انسخ ملف البيئة النموذجي:**
   ```bash
   cp .env.example .env
   ```

2. **احصل على المفاتيح المطلوبة:**
   - **Telegram Bot Token**: اذهب إلى [@BotFather](https://t.me/botfather) على تليجرام واحصل على التوكن
   - **Gemini API Key**: اذهب إلى [Google AI Studio](https://makersuite.google.com/app/apikey) واحصل على المفتاح

3. **عدل ملف `.env`** وضع المفاتيح الحقيقية:
   ```env
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   GEMINI_API_KEY=your_actual_gemini_key_here
   ```

4. **تأكد من أن ملف `.env` محمي:**
   - الملف موجود في `.gitignore` لمنع رفعه للـ Git
   - لا تشارك هذا الملف مع أحد

### ⚠️ تحذير أمني:
- **لا ترفع ملف `.env` إلى Git أبداً**
- **لا تضع المفاتيح الحقيقية في `.env.example`**
- **غير المفاتيح فوراً إذا تم كشفها**

---

## English

### Setup Steps:

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Get the required API keys:**
   - **Telegram Bot Token**: Go to [@BotFather](https://t.me/botfather) on Telegram to get your token
   - **Gemini API Key**: Go to [Google AI Studio](https://makersuite.google.com/app/apikey) to get your key

3. **Edit the `.env` file** with your actual keys:
   ```env
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   GEMINI_API_KEY=your_actual_gemini_key_here
   ```

4. **Ensure `.env` file is protected:**
   - File is listed in `.gitignore` to prevent Git upload
   - Never share this file with anyone

### ⚠️ Security Warning:
- **Never commit `.env` file to Git**
- **Never put real keys in `.env.example`**
- **Rotate keys immediately if exposed**

## Required Dependencies

Make sure to install the required packages:
```bash
pip install -r requirements.txt
```

The `python-dotenv` package is included to load environment variables automatically.

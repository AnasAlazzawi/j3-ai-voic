# نشر البوت على Heroku | Deploy Bot to Heroku

## العربية

### متطلبات النشر:

1. **حساب Heroku**: [سجل هنا](https://signup.heroku.com/)
2. **Heroku CLI**: [حمل من هنا](https://devcenter.heroku.com/articles/heroku-cli)

### طريقة النشر:

#### الطريقة الأولى: عبر GitHub (الأسهل)

1. **اربط GitHub بـ Heroku:**
   - اذهب إلى [Heroku Dashboard](https://dashboard.heroku.com/)
   - انقر "New" > "Create new app"
   - اختر اسم التطبيق ومنطقة الخادم

2. **ربط المستودع:**
   - في تبويب "Deploy" اختر "GitHub"
   - ابحث عن `j3-ai-voic` واربطه
   - فعل "Automatic deploys" للنشر التلقائي

3. **إعداد متغيرات البيئة:**
   - اذهب إلى تبويب "Settings"
   - انقر "Reveal Config Vars"
   - أضف:
     ```
     TELEGRAM_BOT_TOKEN = your_bot_token_here
     GEMINI_API_KEY = your_gemini_key_here
     ```

4. **تشغيل البوت:**
   - في تبويب "Resources" فعل "worker" dyno
   - انقر "Deploy Branch" في تبويب "Deploy"

#### الطريقة الثانية: عبر Heroku CLI

```bash
# تسجيل الدخول
heroku login

# إنشاء تطبيق جديد
heroku create your-bot-name

# إضافة متغيرات البيئة
heroku config:set TELEGRAM_BOT_TOKEN="your_bot_token_here"
heroku config:set GEMINI_API_KEY="your_gemini_key_here"

# نشر الكود
git push heroku main

# تشغيل worker dyno
heroku ps:scale worker=1

# مراقبة اللوجات
heroku logs --tail
```

### ⚠️ ملاحظات مهمة:

- **استخدم eco dyno** (مجاني لـ 1000 ساعة/شهر)
- **أوقف البوت** عند عدم الحاجة لتوفير الساعات
- **راقب اللوجات** للتأكد من عمل البوت بشكل صحيح
- **احم المفاتيح**: لا تضعها في الكود أبداً

### إزالة النشر:

```bash
heroku apps:destroy your-bot-name --confirm your-bot-name
```

---

## English

### Deployment Requirements:

1. **Heroku Account**: [Sign up here](https://signup.heroku.com/)
2. **Heroku CLI**: [Download here](https://devcenter.heroku.com/articles/heroku-cli)

### Deployment Methods:

#### Method 1: Via GitHub (Easiest)

1. **Connect GitHub to Heroku:**
   - Go to [Heroku Dashboard](https://dashboard.heroku.com/)
   - Click "New" > "Create new app"
   - Choose app name and region

2. **Connect Repository:**
   - In "Deploy" tab, select "GitHub"
   - Search for `j3-ai-voic` and connect
   - Enable "Automatic deploys"

3. **Set Environment Variables:**
   - Go to "Settings" tab
   - Click "Reveal Config Vars"
   - Add:
     ```
     TELEGRAM_BOT_TOKEN = your_bot_token_here
     GEMINI_API_KEY = your_gemini_key_here
     ```

4. **Start the Bot:**
   - In "Resources" tab, enable "worker" dyno
   - Click "Deploy Branch" in "Deploy" tab

#### Method 2: Via Heroku CLI

```bash
# Login
heroku login

# Create new app
heroku create your-bot-name

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN="your_bot_token_here"
heroku config:set GEMINI_API_KEY="your_gemini_key_here"

# Deploy code
git push heroku main

# Scale worker dyno
heroku ps:scale worker=1

# Monitor logs
heroku logs --tail
```

### ⚠️ Important Notes:

- **Use eco dyno** (free for 1000 hours/month)
- **Stop bot** when not needed to save hours
- **Monitor logs** to ensure bot is working correctly
- **Protect keys**: Never put them in code

### Remove Deployment:

```bash
heroku apps:destroy your-bot-name --confirm your-bot-name
```

## Useful Commands:

```bash
# Check app status
heroku ps

# View config vars
heroku config

# Restart app
heroku restart

# View recent logs
heroku logs --tail -n 100
```

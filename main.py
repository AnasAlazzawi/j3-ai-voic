"""
Main Telegram Bot
البوت الرئيسي
"""

import os
import asyncio
import logging
import tempfile
from typing import Dict, List, Optional, Tuple

# Telegram bot imports
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Local imports
from config import TELEGRAM_BOT_TOKEN, TTS_VOICES, LOG_FORMAT
from conversation_manager import ConversationManager
from processors import AIAssistant, SpeechProcessor, TTSProcessor, detect_language

# Configure logging
logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """كلاس البوت الرئيسي"""
    
    def __init__(self):
        self.conversation_manager = ConversationManager()
        self.ai_assistant = AIAssistant()
        self.speech_processor = SpeechProcessor()
        self.tts_processor = TTSProcessor()
        
        # Initialize application
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """إعداد معالجات الأوامر والرسائل"""
        # Commands
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("voice", self.voice_command))
        self.application.add_handler(CommandHandler("clear", self.clear_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        
        # Callback queries (button presses)
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        self.application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, self.handle_audio))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"❌ خطأ في التحديث {update}: {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "آسف، حدث خطأ. يرجى المحاولة مرة أخرى لاحقاً."
            )
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show main menu for both commands and callback queries"""
        user_id = str(update.effective_user.id)
        username = update.effective_user.first_name or "المستخدم"
        
        # Check if user has sent any messages before to detect language preference
        user_lang = 'ar'  # Default to Arabic
        if user_id in self.conversation_manager.conversations:
            messages = self.conversation_manager.conversations[user_id]['messages']
            if messages:
                # Use the language of the last user message
                last_user_msg = next((msg for msg in reversed(messages) if msg['role'] == 'user'), None)
                if last_user_msg:
                    user_lang = detect_language(last_user_msg['content'])
        
        welcome_message = f"""
🤖 **مرحباً بك في المساعد الصوتي الذكي، {username}!**

أنا مساعدك الذكي مربوط بapi استطيع ان افهم الرسائل الصوتيه وارد باقل من ثانيه لكن عادتا الصوت يتئخر قليلا:

✨ **الميزات:**
• 🎤 الرسائل الصوتية (تحويل الكلام إلى نص)
• 💬 محادثات ذكية مع gemini 2.0
• 🔊 تحويل النص إلى كلام مع {len(TTS_VOICES)} صوت
• 💾 ذاكرة محادثة لمدة 24 ساعة
• 🌐 أجيب بنفس لغة رسالتك
• by anas firas

**اختر طريقة التفاعل:**
        """
        
        keyboard = [
            [
                InlineKeyboardButton("💬 نص فقط", callback_data="mode_text"),
                InlineKeyboardButton("🔊 صوت فقط", callback_data="mode_audio")
            ],
            [
                InlineKeyboardButton("💬🔊 نص + صوت", callback_data="mode_both")
            ],
            [
                InlineKeyboardButton("🎙️ إعدادات الصوت", callback_data="voice_settings"),
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Handle both callback queries and regular messages
        if update.callback_query:
            await update.callback_query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await self.show_main_menu(update, context)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **مساعدة البوت الصوتي الذكي**

**الأوامر:**
• `/start` - إظهار القائمة الرئيسية
• `/help` - إظهار هذه المساعدة
• `/voice` - تغيير تفضيل الصوت
• `/clear` - مسح تاريخ المحادثة
• `/status` - إظهار حالة البوت

**كيفية الاستخدام:**
1. اختر طريقة التفاعل المفضلة لديك
2. أرسل رسائل نصية أو صوتية
3. سأرد حسب الطريقة المختارة
4. محادثتك محفوظة لمدة 24 ساعة

**الأصوات المتاحة:**
`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`, `coral`, `verse`, `ballad`, `ash`, `sage`, `amuch`, `dan`

**الميزات:**
• 🎤 أرسل رسائل صوتية للتعرف على الكلام
• 💬 محادثات ذكية مع الذاكرة
• 🔊 تحويل نص إلى كلام عالي الجودة
• 🌐 دعم متعدد اللغات (عربي، إنجليزي)
• 🧠 ذاكرة محادثة لمدة 24 ساعة

**نصائح:**
• تكلم بوضوح للحصول على تعرف أفضل
• استخدم الأزرار للتبديل بين الأنماط
• جرب أصوات مختلفة لتجد المفضل لديك
• امسح التاريخ في أي وقت بـ `/clear`
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def voice_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /voice command"""
        await self.show_voice_settings(update, context)
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /clear command"""
        user_id = str(update.effective_user.id)
        success = await self.conversation_manager.clear_conversation(user_id)
        
        if success:
            await update.message.reply_text("✅ تم مسح تاريخ المحادثة!")
        else:
            await update.message.reply_text("لا يوجد تاريخ محادثة لمسحه.")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        user_id = str(update.effective_user.id)
        
        # إحصائيات المستخدم
        conversation_count = self.conversation_manager.get_conversation_count(user_id)
        voice_preference = await self.conversation_manager.get_voice_preference(user_id)
        
        current_mode = context.user_data.get('mode', 'غير محدد')
        
        status_text = f"""
📊 **حالة البوت**

**إعداداتك:**
• 🎙️ الصوت: `{voice_preference}`
• 💬 النمط: `{current_mode}`
• 📝 رسائل في التاريخ: `{conversation_count}`

**معلومات البوت:**
• 🤖 نموذج الذكاء الاصطناعي: جيميني 2.0 فلاش
• 🔊 تحويل النص إلى كلام: {len(TTS_VOICES)} صوت متاح
• 💾 الذاكرة: الاحتفاظ لمدة 24 ساعة
• 🌐 اللغات: العربية، الإنجليزية

**النظام:**
• 🟢 الحالة: متصل
• 📡 الاتصال: نشط
        """
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def show_voice_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show voice selection menu"""
        user_id = str(update.effective_user.id)
        current_voice = await self.conversation_manager.get_voice_preference(user_id)
        
        keyboard = []
        for i in range(0, len(TTS_VOICES), 2):
            row = []
            for j in range(2):
                if i + j < len(TTS_VOICES):
                    voice = TTS_VOICES[i + j]
                    emoji = "🎵" if voice != current_voice else "🎯"
                    row.append(InlineKeyboardButton(f"{emoji} {voice.title()}", callback_data=f"voice_{voice}"))
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"🎙️ **إعدادات الصوت**\n\nالصوت الحالي: `{current_voice}`\n\nاختر صوتك المفضل:"
        
        if update.callback_query:
            await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button presses"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(update.effective_user.id)
        data = query.data
        
        if data == "mode_text":
            context.user_data['mode'] = 'text'
            await query.edit_message_text("💬 **تم اختيار النمط النصي**\n\nأرسل لي رسائل نصية وسأرد بالنص فقط.", parse_mode='Markdown')
        
        elif data == "mode_audio":
            context.user_data['mode'] = 'audio'
            await query.edit_message_text("🔊 **تم اختيار النمط الصوتي**\n\nأرسل لي رسائل نصية أو صوتية وسأرد بالصوت فقط.", parse_mode='Markdown')
        
        elif data == "mode_both":
            context.user_data['mode'] = 'both'
            await query.edit_message_text("💬🔊 **تم اختيار النمط المختلط**\n\nأرسل لي رسائل نصية أو صوتية وسأرد بالنص والصوت معاً.", parse_mode='Markdown')
        
        elif data == "voice_settings":
            await self.show_voice_settings(update, context)
        
        elif data == "status":
            await self.status_command(update, context)
        
        elif data.startswith("voice_"):
            voice = data.replace("voice_", "")
            await self.conversation_manager.set_voice_preference(user_id, voice)
            
            # إظهار رسالة تأكيد ثم العودة للقائمة الرئيسية
            await query.edit_message_text(f"✅ **تم تحديث الصوت**\n\nتم تعيين صوتك المفضل إلى `{voice.title()}`\n\nالعودة للقائمة الرئيسية...", parse_mode='Markdown')
            
            # انتظار ثانية واحدة ثم العودة للقائمة الرئيسية
            await asyncio.sleep(1)
            await self.show_main_menu(update, context)
        
        elif data == "back_to_menu":
            await self.show_main_menu(update, context)
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user_id = str(update.effective_user.id)
        user_message = update.message.text
        mode = context.user_data.get('mode', 'text')
        
        # إضافة رسالة المستخدم للمحادثة
        await self.conversation_manager.add_message(user_id, 'user', user_message)
        
        # الحصول على تاريخ المحادثة
        conversation_history = await self.conversation_manager.get_conversation(user_id)
        
        # توليد رد الذكاء الاصطناعي
        typing_message = await update.message.reply_text("🤔 أفكر...")
        
        try:
            ai_response = await self.ai_assistant.generate_response(conversation_history, user_message)
            
            # إضافة رد الذكاء الاصطناعي للمحادثة
            await self.conversation_manager.add_message(user_id, 'assistant', ai_response)
            
            # حذف رسالة "أفكر..."
            await typing_message.delete()
            
            # إرسال الرد حسب النمط المختار
            if mode == 'text':
                await update.message.reply_text(ai_response)
            
            elif mode == 'audio':
                await self.send_audio_response(update, ai_response, user_id)
            
            elif mode == 'both':
                await update.message.reply_text(ai_response)
                await self.send_audio_response(update, ai_response, user_id)
            
        except Exception as e:
            await typing_message.delete()
            logger.error(f"❌ خطأ في معالجة الرسالة النصية: {e}")
            await update.message.reply_text("آسف، واجهت خطأ. يرجى المحاولة مرة أخرى.")
    
    async def handle_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice/audio messages"""
        user_id = str(update.effective_user.id)
        mode = context.user_data.get('mode', 'text')
        
        # تحميل الملف الصوتي
        processing_message = await update.message.reply_text("🎧 معالجة الصوت...")
        
        try:
            # الحصول على الملف الصوتي
            if update.message.voice:
                audio_file = await update.message.voice.get_file()
            else:
                audio_file = await update.message.audio.get_file()
            
            # تحميل إلى ملف مؤقت
            with tempfile.NamedTemporaryFile(suffix='.oga', delete=False) as temp_file:
                temp_path = temp_file.name
                await audio_file.download_to_drive(temp_path)
            
            # تحويل الكلام إلى نص
            user_message = await self.speech_processor.audio_to_text(temp_path)
            
            # تنظيف الملف المؤقت
            try:
                os.remove(temp_path)
            except:
                pass
            
            # حذف رسالة المعالجة
            await processing_message.delete()
            
            if "آسف، لم أتمكن" in user_message or "Sorry, I couldn't" in user_message:
                await update.message.reply_text(user_message)
                return
            
            # إضافة الرسالة المُفسرة
            await update.message.reply_text(f"🎤 **تم التعرف على:** {user_message}")
            
            # إضافة رسالة المستخدم للمحادثة
            await self.conversation_manager.add_message(user_id, 'user', user_message)
            
            # الحصول على تاريخ المحادثة
            conversation_history = await self.conversation_manager.get_conversation(user_id)
            
            # توليد رد الذكاء الاصطناعي
            thinking_message = await update.message.reply_text("🤔 أولد الرد...")
            
            ai_response = await self.ai_assistant.generate_response(conversation_history, user_message)
            
            # إضافة رد الذكاء الاصطناعي للمحادثة
            await self.conversation_manager.add_message(user_id, 'assistant', ai_response)
            
            # حذف رسالة "أولد الرد..."
            await thinking_message.delete()
            
            # إرسال الرد حسب النمط المختار
            if mode == 'text':
                await update.message.reply_text(ai_response)
            
            elif mode == 'audio':
                await self.send_audio_response(update, ai_response, user_id)
            
            elif mode == 'both':
                await update.message.reply_text(ai_response)
                await self.send_audio_response(update, ai_response, user_id)
        
        except Exception as e:
            await processing_message.delete()
            logger.error(f"❌ خطأ في معالجة الصوت: {e}")
            await update.message.reply_text("آسف، لم أتمكن من معالجة رسالتك الصوتية. يرجى المحاولة مرة أخرى.")
    
    async def send_audio_response(self, update: Update, text: str, user_id: str):
        """Send audio response using TTS"""
        try:
            # الحصول على تفضيل الصوت للمستخدم
            voice = await self.conversation_manager.get_voice_preference(user_id)
            
            # كشف لغة النص لإظهار الرسالة المناسبة
            detected_lang = detect_language(text)
            
            # توليد الصوت
            audio_message = await update.message.reply_text("🔊 أولد الصوت...")
            
            audio_path = await self.tts_processor.text_to_speech(text, voice)
            
            if audio_path and os.path.exists(audio_path):
                # إرسال الملف الصوتي
                with open(audio_path, 'rb') as audio_file:
                    await update.message.reply_voice(audio_file, caption=f"🎵 الصوت: {voice}")
                await audio_message.delete()
            else:
                await audio_message.edit_text("آسف، لم أتمكن من توليد الصوت لهذا الرد.")
        
        except Exception as e:
            logger.error(f"❌ خطأ في تحويل النص إلى كلام: {e}")
            await update.message.reply_text("آسف، لم أتمكن من توليد الصوت لهذا الرد.")
    
    async def cleanup_conversations(self, context: ContextTypes.DEFAULT_TYPE):
        """Periodic cleanup of old conversations"""
        await self.conversation_manager.cleanup_old_conversations()
        logger.info("🧹 تم تنظيف المحادثات القديمة")
    
    async def run(self):
        """Run the bot"""
        try:
            # تحميل المحادثات عند البدء
            await self.conversation_manager.load_conversations()
            
            # بدء تشغيل البوت
            logger.info("🚀 بدء تشغيل البوت...")
            await self.application.initialize()
            await self.application.start()
            
            # إعداد أوامر البوت
            commands = [
                BotCommand("start", "بدء البوت وإظهار القائمة الرئيسية"),
                BotCommand("help", "إظهار معلومات المساعدة"),
                BotCommand("voice", "تغيير تفضيل الصوت"),
                BotCommand("clear", "مسح تاريخ المحادثة"),
                BotCommand("status", "إظهار حالة البوت"),
            ]
            
            await self.application.bot.set_my_commands(commands)
            logger.info("✅ تم إعداد أوامر البوت بنجاح")
            
            # جدولة التنظيف الدوري (كل ساعة)
            job_queue = self.application.job_queue
            if job_queue:
                job_queue.run_repeating(self.cleanup_conversations, interval=3600, first=10)
            else:
                logger.warning("⚠️ JobQueue غير متاح - سيتم التنظيف اليدوي")
            
            # بدء الاستقبال
            await self.application.updater.start_polling(drop_pending_updates=True)
            
            logger.info("🤖 البوت يعمل الآن! اضغط Ctrl+C للإيقاف.")
            
            # الاستمرار في التشغيل
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("🛑 إيقاف البوت...")
            await self.application.stop()
        except Exception as e:
            logger.error(f"❌ فشل في تشغيل البوت: {e}")
            raise

# التشغيل الرئيسي
async def main():
    """Main function to run the bot"""
    try:
        bot = TelegramBot()
        await bot.run()
    except Exception as e:
        logger.error(f"❌ فشل في بدء البوت: {e}")
        raise

if __name__ == "__main__":
    print("🤖 بدء تشغيل البوت الذكي...")
    asyncio.run(main())

"""
Processors for AI, Speech, and TTS
معالجات الذكاء الاصطناعي والصوت
"""

import os
import re
import asyncio
import logging
import tempfile
from typing import Dict, List, Optional
from pathlib import Path

import google.generativeai as genai
import speech_recognition as sr
from pydub import AudioSegment
from gradio_client import Client

from config import (
    GEMINI_API_KEY, 
    ARABIC_CHARS_PATTERN, 
    ENGLISH_CHARS_PATTERN,
    SPEECH_RECOGNITION_SETTINGS,
    AI_GENERATION_CONFIG,
    TTS_MAX_LENGTH,
    TTS_CLIENT_URL
)

logger = logging.getLogger(__name__)

def detect_language(text: str) -> str:
    """Detect if text is Arabic or English"""
    # Remove punctuation and numbers
    clean_text = re.sub(r'[^\w\s]', '', text)
    clean_text = re.sub(r'\d+', '', clean_text)
    
    if not clean_text.strip():
        return 'en'  # Default to English if no text
    
    # Count Arabic and English characters
    arabic_chars = len(re.findall(ARABIC_CHARS_PATTERN, clean_text))
    english_chars = len(re.findall(ENGLISH_CHARS_PATTERN, clean_text))
    
    # If more than 60% Arabic characters, it's Arabic
    total_letters = arabic_chars + english_chars
    if total_letters > 0 and arabic_chars / total_letters > 0.6:
        return 'ar'
    else:
        return 'en'

class AIAssistant:
    """AI Assistant using Gemini 2.0 Flash"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    async def generate_response(self, conversation_history: List[Dict], user_message: str) -> str:
        """Generate AI response based on conversation history"""
        try:
            # Detect user's language
            user_language = detect_language(user_message)
            
            # Build conversation context based on detected language
            if user_language == 'ar':
                context = """أنت مساعد ذكي مفيد. أجب بالعربية فقط وبشكل طبيعي ومفيد.
لا تخلط بين العربية والإنجليزية. استخدم العربية الفصحى أو العامية حسب طبيعة السؤال.

سجل المحادثة:
"""
                user_prefix = "المستخدم"
                assistant_prefix = "المساعد"
                final_prompt = f"المستخدم: {user_message}\nالمساعد:"
            else:
                context = """You are a helpful AI assistant. Respond only in English in a natural and helpful way.
Don't mix Arabic and English. Use clear, natural English.

Conversation History:
"""
                user_prefix = "User"
                assistant_prefix = "Assistant"
                final_prompt = f"User: {user_message}\nAssistant:"
            
            # Add conversation history with appropriate language
            for msg in conversation_history[-8:]:  # Last 8 messages for context
                role = user_prefix if msg['role'] == 'user' else assistant_prefix
                context += f"{role}: {msg['content']}\n"
            
            context += f"\n{final_prompt}"
            
            # Generate response
            response = await asyncio.to_thread(
                self.model.generate_content,
                context,
                generation_config=genai.types.GenerationConfig(
                    temperature=AI_GENERATION_CONFIG['temperature'],
                    max_output_tokens=AI_GENERATION_CONFIG['max_output_tokens'],
                    top_p=AI_GENERATION_CONFIG['top_p'],
                    top_k=AI_GENERATION_CONFIG['top_k']
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"❌ خطأ في توليد رد الذكاء الاصطناعي: {e}")
            # Return error message in detected language
            if detect_language(user_message) == 'ar':
                return "أعتذر، أواجه مشكلة في تقديم رد الآن. يرجى المحاولة مرة أخرى."
            else:
                return "I apologize, but I'm having trouble generating a response right now. Please try again."

class SpeechProcessor:
    """Handles speech-to-text processing"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # تحسين إعدادات التعرف على الكلام
        self.recognizer.energy_threshold = SPEECH_RECOGNITION_SETTINGS['energy_threshold']
        self.recognizer.dynamic_energy_threshold = SPEECH_RECOGNITION_SETTINGS['dynamic_energy_threshold']
        self.recognizer.pause_threshold = SPEECH_RECOGNITION_SETTINGS['pause_threshold']
    
    async def audio_to_text(self, audio_file_path: str) -> str:
        """Convert audio file to text using speech recognition"""
        try:
            # Convert audio to WAV format if needed
            audio = AudioSegment.from_file(audio_file_path)
            
            # تحسين الصوت
            audio = audio.normalize()
            if audio.channels > 1:
                audio = audio.set_channels(1)
            audio = audio.set_frame_rate(16000)
            
            wav_path = audio_file_path.replace('.oga', '.wav').replace('.ogg', '.wav')
            audio.export(wav_path, format="wav")
            
            # Perform speech recognition
            with sr.AudioFile(wav_path) as source:
                self.recognizer.adjust_for_ambient_noise(
                    source, 
                    duration=SPEECH_RECOGNITION_SETTINGS['ambient_noise_duration']
                )
                audio_data = self.recognizer.record(source)
                
                # جرب التعرف باللغة الإنجليزية أولاً
                try:
                    text = await asyncio.to_thread(
                        self.recognizer.recognize_google,
                        audio_data,
                        language='en-US'
                    )
                    logger.info(f"🎤 تم التعرف على النص: {text}")
                    return text
                except sr.UnknownValueError:
                    # جرب التعرف باللغة العربية
                    try:
                        text = await asyncio.to_thread(
                            self.recognizer.recognize_google,
                            audio_data,
                            language='ar-SA'
                        )
                        logger.info(f"🎤 تم التعرف على النص بالعربية: {text}")
                        return text
                    except sr.UnknownValueError:
                        return "آسف، لم أتمكن من فهم الصوت. يرجى المحاولة مرة أخرى بوضوح أكبر."
            
        except sr.RequestError as e:
            logger.error(f"❌ خطأ في خدمة التعرف على الكلام: {e}")
            return "آسف، حدث خطأ في خدمة التعرف على الكلام."
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة الصوت: {e}")
            return "آسف، لم أتمكن من معالجة ملف الصوت."
        finally:
            # تنظيف الملفات المؤقتة
            try:
                if 'wav_path' in locals() and os.path.exists(wav_path):
                    os.remove(wav_path)
            except:
                pass

class TTSProcessor:
    """Handles text-to-speech processing"""
    
    def __init__(self):
        self.client = Client(TTS_CLIENT_URL)
    
    async def text_to_speech(self, text: str, voice: str = "alloy", emotion: str = "neutral") -> Optional[str]:
        """Convert text to speech and return audio file path"""
        try:
            # تحديد طول النص
            if len(text) > TTS_MAX_LENGTH:
                text = text[:TTS_MAX_LENGTH] + "..."
            
            logger.info(f"🔊 توليد صوت للنص: {text[:50]}... بصوت: {voice}")
            
            result = await asyncio.to_thread(
                self.client.predict,
                prompt=text,
                voice=voice,
                emotion=emotion,
                use_random_seed=True,
                specific_seed=12345,
                api_name="/text_to_speech_app"
            )
            
            if result and isinstance(result, tuple) and len(result) > 0:
                audio_path = result[0]
                if os.path.exists(audio_path):
                    logger.info(f"✅ تم توليد الصوت بنجاح: {audio_path}")
                    return audio_path
                else:
                    logger.error(f"❌ ملف الصوت غير موجود: {audio_path}")
                    return None
            
            return None
            
        except Exception as e:
            logger.error(f"❌ خطأ في تحويل النص إلى كلام: {e}")
            return None

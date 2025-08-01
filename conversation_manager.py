"""
Conversation Manager for Telegram Bot
إدارة المحادثات للبوت
"""

import os
import json
import asyncio
import aiofiles
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from config import CONVERSATION_FILE, CONVERSATION_TIMEOUT

logger = logging.getLogger(__name__)

class ConversationManager:
    """Manages user conversations with JSON storage and automatic cleanup"""
    
    def __init__(self, file_path: str = CONVERSATION_FILE):
        self.file_path = file_path
        self.conversations = {}
    
    async def load_conversations(self):
        """Load conversations from JSON file"""
        try:
            if os.path.exists(self.file_path):
                async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    if content.strip():
                        data = json.loads(content)
                        self.conversations = data
                        logger.info(f"✅ تم تحميل {len(self.conversations)} محادثة")
                    else:
                        self.conversations = {}
            else:
                self.conversations = {}
                logger.info("📁 ملف المحادثات غير موجود، سيتم إنشاؤه")
        except Exception as e:
            logger.error(f"❌ خطأ في تحميل المحادثات: {e}")
            self.conversations = {}
    
    async def save_conversations(self):
        """Save conversations to JSON file"""
        try:
            async with aiofiles.open(self.file_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(self.conversations, indent=2, ensure_ascii=False))
        except Exception as e:
            logger.error(f"❌ خطأ في حفظ المحادثات: {e}")
    
    async def get_conversation(self, user_id: str) -> List[Dict]:
        """Get conversation history for a user"""
        if user_id not in self.conversations:
            self.conversations[user_id] = {
                'messages': [],
                'last_activity': datetime.now().isoformat(),
                'voice_preference': 'alloy'
            }
        return self.conversations[user_id]['messages']
    
    async def add_message(self, user_id: str, role: str, content: str):
        """Add a message to user's conversation"""
        if user_id not in self.conversations:
            self.conversations[user_id] = {
                'messages': [],
                'last_activity': datetime.now().isoformat(),
                'voice_preference': 'alloy'
            }
        
        self.conversations[user_id]['messages'].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        self.conversations[user_id]['last_activity'] = datetime.now().isoformat()
        await self.save_conversations()
    
    async def set_voice_preference(self, user_id: str, voice: str):
        """Set user's voice preference"""
        if user_id not in self.conversations:
            self.conversations[user_id] = {
                'messages': [],
                'last_activity': datetime.now().isoformat(),
                'voice_preference': voice
            }
        else:
            self.conversations[user_id]['voice_preference'] = voice
        await self.save_conversations()
    
    async def get_voice_preference(self, user_id: str) -> str:
        """Get user's voice preference"""
        if user_id in self.conversations:
            return self.conversations[user_id].get('voice_preference', 'alloy')
        return 'alloy'
    
    async def clear_conversation(self, user_id: str):
        """Clear conversation history for a user"""
        if user_id in self.conversations:
            self.conversations[user_id]['messages'] = []
            await self.save_conversations()
            return True
        return False
    
    async def cleanup_old_conversations(self):
        """Remove conversations older than 24 hours"""
        current_time = datetime.now()
        users_to_remove = []
        
        for user_id, data in self.conversations.items():
            try:
                last_activity = datetime.fromisoformat(data['last_activity'])
                if current_time - last_activity > timedelta(seconds=CONVERSATION_TIMEOUT):
                    users_to_remove.append(user_id)
            except (ValueError, KeyError):
                users_to_remove.append(user_id)
        
        for user_id in users_to_remove:
            del self.conversations[user_id]
            logger.info(f"🗑️ تم حذف محادثة المستخدم {user_id}")
        
        if users_to_remove:
            await self.save_conversations()
    
    def get_conversation_count(self, user_id: str) -> int:
        """Get number of messages in user's conversation"""
        if user_id in self.conversations:
            return len(self.conversations[user_id]['messages'])
        return 0

"""
Генератор комментариев с использованием AI
"""
import asyncio
import logging
import random
from typing import Optional, Dict, Any
import openai
from openai import AsyncOpenAI

from app.config import settings
from app.ai.prompts import CommentPrompts, SPECIAL_PROMPTS

logger = logging.getLogger(__name__)


class CommentGenerator:
    """Генератор комментариев с использованием AI"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        
    async def generate_comment(self, content: str, media_type: str = "text", 
                             style: str = None, mood: str = None) -> Optional[str]:
        """Генерация комментария с использованием AI"""
        try:
            # Очищаем контент от лишних символов
            cleaned_content = self._clean_content(content)
            
            if not cleaned_content:
                logger.warning("Пустой контент для генерации комментария")
                return None
            
            # Выбираем стиль и настроение, если не указаны
            if not style:
                style = CommentPrompts.get_random_style()
            if not mood:
                mood = CommentPrompts.get_random_mood()
            
            # Получаем промпт
            prompt = CommentPrompts.get_prompt(cleaned_content, media_type, style, mood)
            
            # Генерируем комментарий
            comment = await self._generate_with_ai(prompt)
            
            if comment:
                # Проверяем и очищаем комментарий
                comment = self._clean_comment(comment)
                
                # Проверяем длину
                if len(comment) > settings.max_comment_length:
                    comment = comment[:settings.max_comment_length].rsplit(' ', 1)[0] + "..."
                
                logger.info(f"Сгенерирован комментарий: {comment[:50]}...")
                return comment
            else:
                logger.warning("Не удалось сгенерировать комментарий")
                return None
                
        except Exception as e:
            logger.error(f"Ошибка генерации комментария: {e}")
            return None
    
    async def generate_special_comment(self, content: str, special_type: str) -> Optional[str]:
        """Генерация специального комментария для определенного типа контента"""
        try:
            if special_type not in SPECIAL_PROMPTS:
                logger.warning(f"Неизвестный тип специального комментария: {special_type}")
                return await self.generate_comment(content)
            
            # Очищаем контент
            cleaned_content = self._clean_content(content)
            
            if not cleaned_content:
                return None
            
            # Получаем специальный промпт
            prompt = SPECIAL_PROMPTS[special_type].format(content=cleaned_content)
            
            # Генерируем комментарий
            comment = await self._generate_with_ai(prompt)
            
            if comment:
                comment = self._clean_comment(comment)
                if len(comment) > settings.max_comment_length:
                    comment = comment[:settings.max_comment_length].rsplit(' ', 1)[0] + "..."
                
                logger.info(f"Сгенерирован специальный комментарий ({special_type}): {comment[:50]}...")
                return comment
            else:
                return None
                
        except Exception as e:
            logger.error(f"Ошибка генерации специального комментария: {e}")
            return None
    
    async def _generate_with_ai(self, prompt: str) -> Optional[str]:
        """Генерация текста с использованием AI"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты - эксперт по созданию естественных комментариев в социальных сетях."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7,
                top_p=0.9
            )
            
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content.strip()
            else:
                logger.warning("Пустой ответ от AI")
                return None
                
        except Exception as e:
            logger.error(f"Ошибка обращения к AI: {e}")
            return None
    
    def _clean_content(self, content: str) -> str:
        """Очистка контента от лишних символов"""
        if not content:
            return ""
        
        # Удаляем лишние пробелы и переносы строк
        content = " ".join(content.split())
        
        # Ограничиваем длину контента для промпта
        if len(content) > 1000:
            content = content[:1000] + "..."
        
        return content
    
    def _clean_comment(self, comment: str) -> str:
        """Очистка сгенерированного комментария"""
        if not comment:
            return ""
        
        # Удаляем лишние пробелы
        comment = " ".join(comment.split())
        
        # Удаляем кавычки, если они есть
        comment = comment.strip('"\'')
        
        # Удаляем префиксы типа "Комментарий:" или "Ответ:"
        prefixes_to_remove = [
            "Комментарий:", "Ответ:", "Comment:", "Reply:",
            "Вот комментарий:", "Вот ответ:", "Мой комментарий:"
        ]
        
        for prefix in prefixes_to_remove:
            if comment.startswith(prefix):
                comment = comment[len(prefix):].strip()
        
        return comment
    
    async def generate_multiple_comments(self, content: str, media_type: str = "text", 
                                       count: int = 3) -> list[str]:
        """Генерация нескольких вариантов комментариев"""
        try:
            comments = []
            
            for i in range(count):
                # Используем разные стили и настроения
                style = CommentPrompts.get_random_style()
                mood = CommentPrompts.get_random_mood()
                
                comment = await self.generate_comment(content, media_type, style, mood)
                
                if comment and comment not in comments:
                    comments.append(comment)
                
                # Небольшая задержка между запросами
                await asyncio.sleep(0.5)
            
            return comments
            
        except Exception as e:
            logger.error(f"Ошибка генерации множественных комментариев: {e}")
            return []
    
    async def analyze_content_type(self, content: str) -> str:
        """Анализ типа контента для выбора подходящего промпта"""
        try:
            # Простой анализ ключевых слов
            content_lower = content.lower()
            
            # Криптовалюты
            crypto_keywords = ["биткоин", "bitcoin", "криптовалюта", "блокчейн", "эфириум", "ethereum"]
            if any(keyword in content_lower for keyword in crypto_keywords):
                return "crypto"
            
            # Технологии
            tech_keywords = ["программирование", "код", "разработка", "технология", "ai", "ии"]
            if any(keyword in content_lower for keyword in tech_keywords):
                return "tech"
            
            # Новости
            news_keywords = ["новости", "события", "происшествие", "политика", "экономика"]
            if any(keyword in content_lower for keyword in news_keywords):
                return "news"
            
            return "general"
            
        except Exception as e:
            logger.error(f"Ошибка анализа типа контента: {e}")
            return "general"
    
    async def generate_smart_comment(self, content: str, media_type: str = "text") -> Optional[str]:
        """Умная генерация комментария с анализом типа контента"""
        try:
            # Анализируем тип контента
            content_type = await self.analyze_content_type(content)
            
            # Генерируем специальный комментарий, если тип определен
            if content_type in SPECIAL_PROMPTS:
                comment = await self.generate_special_comment(content, content_type)
                if comment:
                    return comment
            
            # Иначе используем обычную генерацию
            return await self.generate_comment(content, media_type)
            
        except Exception as e:
            logger.error(f"Ошибка умной генерации комментария: {e}")
            return None

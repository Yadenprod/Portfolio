"""
Надежный параллельный чекер ГИБДД с системой валидации и повторных попыток
Автоматически определяет некачественные данные и перепроверяет их
"""

import time
import os
import json
import base64
import logging
import multiprocessing
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import hashlib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from ultimate_adaptive_solver import solve_captcha
from PIL import Image, ImageChops

# Настройка логирования
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class CheckType(Enum):
    """Типы проверок автомобиля"""
    REGISTRATION = "registration"  # Периоды регистрации
    ACCIDENTS = "accidents"        # ДТП
    WANTED = "wanted"             # Розыск
    RESTRICTIONS = "restrictions"  # Ограничения

@dataclass
class CheckResult:
    """Результат проверки"""
    check_type: CheckType
    success: bool
    data: List[Dict] = field(default=None)
    error: str = None
    captcha_solved: bool = False
    ad_waited: bool = False
    attempt_number: int = 1
    quality_score: float = 0.0  # Оценка качества данных
    validation_errors: List[str] = field(default=None)

class DataValidator:
    """Валидатор качества данных"""
    
    @staticmethod
    def validate_registration_data(data: List[Dict]) -> tuple[bool, float, List[str]]:
        """Валидация данных регистрации"""
        if not data:
            return False, 0.0, ["Нет данных о регистрации"]
        
        errors = []
        score = 0.0
        
        # Проверяем основные блоки
        has_checkResult = False
        has_ownership = False
        
        for block in data:
            block_type = block.get("block", "")
            text = block.get("text", "")
            
            if block_type == "checkResult":
                has_checkResult = True
                if len(text) > 50:  # Минимальная длина осмысленного текста
                    score += 40
                    
                    # Проверяем ключевые поля
                    if "Марка и(или) модель:" in text:
                        score += 20
                    if "Год выпуска:" in text:
                        score += 10
                    if "VIN" in text or "Номер кузова" in text:
                        score += 10
                    if "Цвет:" in text:
                        score += 5
                else:
                    errors.append("Слишком короткие данные в checkResult")
                    
            elif block_type == "ownershipPeriods":
                has_ownership = True
                if len(text) > 20:
                    score += 15
                else:
                    errors.append("Нет данных о периодах владения")
        
        if not has_checkResult:
            errors.append("Отсутствует основной блок данных")
        if not has_ownership:
            errors.append("Отсутствуют данные о владельцах")
        
        is_valid = score >= 60 and len(errors) == 0
        return is_valid, score, errors
    
    @staticmethod
    def validate_accidents_data(data: List[Dict]) -> tuple[bool, float, List[str]]:
        """Валидация данных ДТП"""
        if not data:
            return False, 0.0, ["Нет данных о ДТП"]
        
        errors = []
        score = 0.0
        screenshot_count = 0
        total_accidents = 1
        
        # Определяем общее количество ДТП
        for block in data:
            if "total_accidents" in block:
                total_accidents = block["total_accidents"]
                break
        
        for block in data:
            block_type = block.get("block", "")
            accident_num = block.get("accident_number", 1)
            
            if block_type == "checkResultScreenshot":
                screenshot_count += 1
                # Проверяем скриншот
                screenshot_path = block.get("screenshot_path", "")
                if screenshot_path and os.path.exists(screenshot_path):
                    file_size = os.path.getsize(screenshot_path)
                    if file_size > 1000:  # Минимальный размер скриншота
                        score += 40  # Снижаем базовый балл, так как теперь может быть несколько ДТП
                    else:
                        errors.append(f"Скриншот ДТП {accident_num} слишком маленький")
                else:
                    errors.append(f"Отсутствует скриншот ДТП {accident_num}")
                
                # Проверяем текст
                text = block.get("text", "")
                if len(text) > 10:
                    score += 20
                else:
                    score += 5  # Иногда ДТП действительно нет
                    
            elif block_type == "checkResult":
                # Текстовый блок вместо скриншота
                text = block.get("text", "")
                if "сведений о дорожно-транспортных происшествиях не найдено" in text.lower():
                    score += 80  # Корректное сообщение об отсутствии ДТП
                elif len(text) > 20:
                    score += 40  # Есть информация о ДТП
                else:
                    errors.append(f"Неполные данные о ДТП {accident_num}")
        
        # Бонусные баллы за полноту данных
        if screenshot_count >= total_accidents:
            score += 20  # Бонус за все скриншоты
        
        # Логика валидации: если получили данные о всех ДТП или корректное сообщение об их отсутствии
        is_valid = score >= 50
        
        # Если есть множественные ДТП, требуем более высокий балл
        if total_accidents > 1:
            is_valid = score >= 60 and screenshot_count >= total_accidents
            
        return is_valid, score, errors
    
    @staticmethod
    def validate_wanted_data(data: List[Dict]) -> tuple[bool, float, List[str]]:
        """Валидация данных розыска"""
        if not data:
            return False, 0.0, ["Нет данных о розыске"]
        
        errors = []
        score = 0.0
        
        for block in data:
            text = block.get("text", "")
            if len(text) > 10:
                if "сведений о розыске не найдено" in text.lower() or \
                   "информация отсутствует" in text.lower():
                    score += 80  # Корректное сообщение об отсутствии розыска
                elif "розыск" in text.lower() or "федеральный" in text.lower():
                    score += 70  # Есть информация о розыске
                else:
                    score += 40  # Есть какой-то текст
            else:
                errors.append("Слишком короткие данные о розыске")
        
        is_valid = score >= 60
        return is_valid, score, errors
    
    @staticmethod
    def validate_restrictions_data(data: List[Dict]) -> tuple[bool, float, List[str]]:
        """Валидация данных ограничений"""
        if not data:
            return False, 0.0, ["Нет данных об ограничениях"]
        
        errors = []
        score = 0.0
        
        for block in data:
            text = block.get("text", "")
            if len(text) > 10:
                if "сведений об ограничениях не найдено" in text.lower() or \
                   "информация отсутствует" in text.lower():
                    score += 80  # Корректное сообщение об отсутствии ограничений
                elif "ограничен" in text.lower() or "запрет" in text.lower():
                    score += 70  # Есть информация об ограничениях
                else:
                    score += 40  # Есть какой-то текст
            else:
                errors.append("Слишком короткие данные об ограничениях")
        
        is_valid = score >= 60
        return is_valid, score, errors
    
    @classmethod
    def validate_section_data(cls, check_type: CheckType, data: List[Dict]) -> tuple[bool, float, List[str]]:
        """Универсальная валидация данных секции"""
        if check_type == CheckType.REGISTRATION:
            return cls.validate_registration_data(data)
        elif check_type == CheckType.ACCIDENTS:
            return cls.validate_accidents_data(data)
        elif check_type == CheckType.WANTED:
            return cls.validate_wanted_data(data)
        elif check_type == CheckType.RESTRICTIONS:
            return cls.validate_restrictions_data(data)
        else:
            return False, 0.0, ["Неизвестный тип секции"]

class ReliableGibddChecker:
    """Надежный чекер с валидацией и повторными попытками"""
    
    def __init__(self, max_attempts: int = 3, min_quality_score: float = 60.0):
        self.url = "https://xn--90adear.xn--p1ai/check/auto"
        self.temp_files = []
        self.driver = None
        self.wait = None
        self.max_attempts = max_attempts
        self.min_quality_score = min_quality_score
        
    def cleanup_temp_files(self):
        """Очистка временных файлов"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                logger.error(f"❌ Ошибка удаления {temp_file}: {e}")
        self.temp_files.clear()

    def setup_driver(self):
        """Настройка веб-драйвера"""
        if self.driver:
            return
            
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        # Максимальное отключение звука
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--disable-audio-output")
        chrome_options.add_argument("--disable-sound")
        chrome_options.add_argument("--no-audio")
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        prefs = {
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.images": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
        except Exception as e:
            logger.error(f"❌ Ошибка создания драйвера: {e}")
            raise

    def input_vin(self, vin: str) -> bool:
        """Ввод VIN номера"""
        try:
            vin_input = self.wait.until(EC.presence_of_element_located((By.NAME, "vin")))
            vin_input.clear()
            vin_input.send_keys(vin)
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка ввода VIN: {e}")
            return False

    def wait_for_ad_completion(self, timeout: int = 90) -> bool:
        """Ожидание завершения рекламы"""
        try:
            start_time = time.time()
            ad_closed = False

            while time.time() - start_time < timeout:
                ad_modals = self.driver.find_elements(By.CSS_SELECTOR, ".modal, .fancybox-inner, .fancybox-container, .fancybox-bg, .fancybox-slide, .fancybox-content, .adds-modal")
                ad_modals = [m for m in ad_modals if m.is_displayed()]
                ad_modal = ad_modals[0] if ad_modals else None

                if not ad_modal:
                    ad_closed = True
                    break

                try:
                    close_btn = ad_modal.find_element(By.XPATH, ".//button[contains(@class, 'close') or contains(@class, 'fancybox-close') or contains(@class, 'close_modal_window') or contains(text(), 'Закрыть') or contains(text(), 'X')]")
                    if close_btn.is_displayed() and close_btn.is_enabled():
                        close_btn.click()
                        for _ in range(20):
                            time.sleep(0.5)
                            ad_modals = self.driver.find_elements(By.CSS_SELECTOR, ".modal, .fancybox-inner, .fancybox-container, .fancybox-bg, .fancybox-slide, .fancybox-content, .adds-modal")
                            ad_modals = [m for m in ad_modals if m.is_displayed()]
                            if not ad_modals:
                                ad_closed = True
                                break
                        if ad_closed:
                            break
                except Exception:
                    pass

                if ad_modal and ("img" in ad_modal.get_attribute("innerHTML") or ad_modal.find_elements(By.TAG_NAME, "img")):
                    if time.time() - start_time < 7:
                        time.sleep(1)
                        continue

                time.sleep(1)

            return ad_closed

        except Exception as e:
            logger.error(f"❌ Ошибка ожидания рекламы: {e}")
            return False

    def extract_results(self, check_type: CheckType) -> List[Dict]:
        """Извлечение результатов проверки"""
        try:
            time.sleep(3)
            
            if check_type == CheckType.REGISTRATION:
                results = []
                try:
                    check_result_div = self.driver.find_element(By.CSS_SELECTOR, "div.checkResult")
                    text = check_result_div.get_attribute("innerText")
                    results.append({
                        "block": "checkResult",
                        "text": text
                    })
                except Exception as e:
                    logger.error(f"❌ Не удалось найти div.checkResult: {e}")
                    
                try:
                    ownership_ul = self.driver.find_element(By.CSS_SELECTOR, "ul.ownershipPeriods")
                    text = ownership_ul.get_attribute("innerText")
                    results.append({
                        "block": "ownershipPeriods",
                        "text": text
                    })
                except Exception as e:
                    logger.error(f"❌ Не удалось найти ul.ownershipPeriods: {e}")
                    
                return results
                    
            elif check_type == CheckType.ACCIDENTS:
                try:
                    dtp_section = self.driver.find_element(By.CSS_SELECTOR, "div#checkAutoAiusdtp")
                    check_result_div = dtp_section.find_element(By.CSS_SELECTOR, "div.checkResult")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", check_result_div)
                    time.sleep(0.5)
                    
                    # Получаем весь текст для анализа
                    page_text = check_result_div.get_attribute("innerText")
                    
                    # Ищем все блоки "Информация о происшествии" для определения количества ДТП
                    import re
                    accident_patterns = [
                        r"Информация о происшествии №\d+",
                        r"Информация о происшествии\s*№\s*\d+",
                        r"Информация о происшествии"
                    ]
                    
                    total_accidents = 0
                    for pattern in accident_patterns:
                        matches = re.findall(pattern, page_text, re.IGNORECASE)
                        if matches:
                            total_accidents = len(matches)
                            logger.info(f"🔍 Найдено {total_accidents} ДТП по паттерну: '{pattern}'")
                            break
                    
                    if total_accidents == 0:
                        total_accidents = 1
                        logger.info(f"🔍 Не найдено паттернов ДТП, предполагаем 1 ДТП")
                    
                    # Альтернативная проверка по "X/Y"
                    if "из всего ТС в ДТП:" in page_text:
                        pattern = r"(\d+)/(\d+)"
                        match = re.search(pattern, page_text)
                        if match:
                            total_from_pattern = int(match.group(2))
                            total_accidents = max(total_accidents, total_from_pattern)
                            logger.info(f"🔍 Подтверждено из паттерна X/Y: всего {total_accidents} ДТП")
                    
                    results = []
                    
                    # Если ДТП одно, делаем один скриншот
                    if total_accidents == 1:
                        logger.info(f"📸 Делаем один скриншот для единственного ДТП")
                        
                        # Дополнительное ожидание полной загрузки контента
                        for wait_attempt in range(3):
                            size = check_result_div.size
                            logger.info(f"   📏 Попытка {wait_attempt + 1}: размеры элемента ДТП: {size}")
                            
                            if size['width'] > 0 and size['height'] > 16:
                                break
                            elif wait_attempt < 2:
                                logger.info(f"   ⏳ Ждем загрузки контента ДТП...")
                                time.sleep(2)
                                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", check_result_div)
                            else:
                                logger.warning(f"   ⚠️ Элемент ДТП остается невидимым после ожидания")
                        
                        timestamp = int(time.time())
                        screenshot_path = f"dtp_block_{timestamp}_{os.getpid()}_1.png"
                        
                        try:
                            check_result_div.screenshot(screenshot_path)
                            
                            # Обрезаем скриншот
                            try:
                                img = Image.open(screenshot_path)
                                bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
                                diff = ImageChops.difference(img, bg)
                                bbox = diff.getbbox()
                                if bbox:
                                    cropped = img.crop(bbox)
                                    cropped.save(screenshot_path)
                                    logger.info(f"   ✂️ Скриншот ДТП обрезан")
                            except Exception as crop_e:
                                logger.error(f"❌ Не удалось обрезать скриншот: {crop_e}")
                            
                            text = check_result_div.get_attribute("innerText").strip()
                            
                            results.append({
                                "block": "checkResultScreenshot",
                                "screenshot_path": screenshot_path,
                                "text": text,
                                "total_accidents": total_accidents,
                                "accident_number": 1
                            })
                            
                            logger.info(f"✅ Скриншот единственного ДТП сохранен: {screenshot_path}")
                            
                        except Exception as screenshot_e:
                            logger.error(f"❌ Не удалось сделать скриншот ДТП: {screenshot_e}")
                            text = check_result_div.get_attribute("innerText").strip()
                            if text:
                                results.append({
                                    "block": "checkResult",
                                    "text": text,
                                    "total_accidents": total_accidents,
                                    "error": f"Ошибка скриншота: {screenshot_e}"
                                })
                    
                    else:
                        # Если ДТП несколько, ищем каждое отдельно
                        logger.info(f"📸 Ищем {total_accidents} отдельных блоков ДТП для скриншотов")
                        
                        # Ищем все элементы, содержащие "Информация о происшествии"
                        try:
                            # Ищем LI блоки ДТП в контейнере
                            accident_elements = []
                            
                            # Сначала ищем все LI элементы в контейнере
                            li_elements = check_result_div.find_elements(By.TAG_NAME, "li")
                            logger.info(f"🔍 Найдено {len(li_elements)} LI элементов в контейнере ДТП")
                            
                            # Фильтруем только валидные LI с содержимым ДТП
                            for i, li in enumerate(li_elements):
                                try:
                                    text = li.get_attribute("innerText").strip()
                                    size = li.size
                                    
                                    logger.info(f"   🔍 LI элемент {i+1}: размер={size}, текст={len(text)} символов")
                                    logger.info(f"      Начало текста: {text[:100]}...")
                                    
                                    # Проверяем что это блок ДТП (содержит ключевые слова)
                                    has_accident_info = (
                                        "Информация о происшествии" in text or
                                        "происшествия" in text.lower() or
                                        "Дата и время происшествия" in text or
                                        "Тип происшествия" in text or
                                        "Регион происшествия" in text
                                    )
                                    
                                    has_sufficient_content = len(text) > 100 and size['height'] > 50
                                    
                                    if has_accident_info and has_sufficient_content:
                                        accident_elements.append(li)
                                        logger.info(f"      ✅ Валидный LI блок ДТП #{len(accident_elements)} добавлен")
                                    else:
                                        logger.info(f"      ❌ LI блок не подходит: инфо_ДТП={has_accident_info}, контент={has_sufficient_content}")
                                        
                                except Exception as li_e:
                                    logger.debug(f"   ❌ Ошибка проверки LI {i+1}: {li_e}")
                                    continue
                            
                            # Определяем что делать с найденными LI блоками
                            logger.info(f"🔍 Найдено {len(accident_elements)} LI блоков ДТП")
                            
                            if len(accident_elements) > 0:
                                # Нашли LI блоки - делаем скриншот каждого
                                logger.info(f"✅ Используем найденные LI блоки: {len(accident_elements)} ДТП")
                                
                                for i, accident_element in enumerate(accident_elements, 1):
                                    try:
                                        logger.info(f"📸 Делаем скриншот LI блока ДТП {i}/{len(accident_elements)}")
                                        
                                        # Прокручиваем к элементу
                                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", accident_element)
                                        time.sleep(1)
                                        
                                        # Проверяем размеры элемента
                                        size = accident_element.size
                                        logger.info(f"   📏 Размеры LI элемента {i}: {size}")
                                        
                                        if size['width'] > 0 and size['height'] > 16:
                                            timestamp = int(time.time())
                                            # Добавляем небольшую задержку для уникального timestamp
                                            time.sleep(0.3)
                                            screenshot_path = f"dtp_block_{timestamp}_{os.getpid()}_{i}.png"
                                            
                                            # Добавляем границу для лучшей видимости
                                            self.driver.execute_script("arguments[0].style.border = '3px solid red';", accident_element)
                                            time.sleep(0.5)
                                            
                                            accident_element.screenshot(screenshot_path)
                                            
                                            # Убираем границу
                                            self.driver.execute_script("arguments[0].style.border = '';", accident_element)
                                            
                                            text = accident_element.get_attribute("innerText").strip()
                                            
                                            results.append({
                                                "block": "checkResultScreenshot",
                                                "screenshot_path": screenshot_path,
                                                "text": text,
                                                "total_accidents": len(accident_elements),  # Используем реальное количество
                                                "accident_number": i
                                            })
                                            
                                            logger.info(f"✅ Скриншот LI блока ДТП {i} сохранен: {screenshot_path}")
                                        else:
                                            logger.warning(f"⚠️ LI элемент ДТП {i} имеет нулевые размеры: {size}")
                                            
                                    except Exception as acc_e:
                                        logger.error(f"❌ Ошибка скриншота LI блока ДТП {i}: {acc_e}")
                                        continue
                            
                            elif total_accidents > 1:
                                # LI блоки не найдены, но ожидается несколько ДТП - используем fallback прокрутки
                                logger.info(f"⚠️ LI блоки не найдены, но ожидается {total_accidents} ДТП. Используем fallback метод прокрутки")
                                
                                # Получаем размеры контейнера
                                container_height = check_result_div.size['height']
                                section_height = container_height // total_accidents if container_height > 0 else 200
                                
                                logger.info(f"📏 Высота контейнера: {container_height}px, на секцию: {section_height}px")
                                
                                for i in range(total_accidents):
                                    try:
                                        logger.info(f"📸 Делаем fallback скриншот ДТП {i+1}/{total_accidents}")
                                        
                                        # Прокручиваем к нужной позиции
                                        scroll_position = i * section_height
                                        logger.info(f"   🔄 Прокручиваем к позиции: {scroll_position}px")
                                        
                                        # Прокрутка с помощью JavaScript
                                        self.driver.execute_script(f"""
                                            var element = arguments[0];
                                            element.scrollTop = {scroll_position};
                                            window.scrollTo(0, window.scrollY + {scroll_position});
                                        """, check_result_div)
                                        time.sleep(1.5)  # Ждем загрузки контента
                                        
                                        timestamp = int(time.time())
                                        time.sleep(0.3)  # Задержка для уникального timestamp
                                        screenshot_path = f"dtp_block_{timestamp}_{os.getpid()}_{i+1}.png"
                                        
                                        # Добавляем границу для видимости
                                        self.driver.execute_script("arguments[0].style.border = '3px solid blue';", check_result_div)
                                        time.sleep(0.3)
                                        
                                        # Делаем скриншот всего контейнера
                                        check_result_div.screenshot(screenshot_path)
                                        
                                        # Убираем границу
                                        self.driver.execute_script("arguments[0].style.border = '';", check_result_div)
                                        
                                        # Обрезаем скриншот (оставляем только нужную часть)
                                        try:
                                            img = Image.open(screenshot_path)
                                            width, height = img.size
                                            
                                            # Вычисляем координаты для обрезки
                                            top = max(0, (height // total_accidents) * i)
                                            bottom = min(height, (height // total_accidents) * (i + 1))
                                            
                                            logger.info(f"   ✂️ Обрезаем fallback: top={top}, bottom={bottom} из {height}")
                                            
                                            if bottom > top:
                                                cropped = img.crop((0, top, width, bottom))
                                                cropped.save(screenshot_path)
                                                logger.info(f"   ✂️ Fallback скриншот ДТП {i+1} обрезан до {width}x{bottom-top}")
                                        except Exception as crop_e:
                                            logger.error(f"❌ Не удалось обрезать fallback скриншот ДТП {i+1}: {crop_e}")
                                        
                                        # Получаем текст для этой части
                                        full_text = check_result_div.get_attribute("innerText")
                                        text_lines = full_text.split('\n')
                                        lines_per_section = max(1, len(text_lines) // total_accidents)
                                        
                                        start_line = i * lines_per_section
                                        end_line = min((i + 1) * lines_per_section, len(text_lines))
                                        section_text = '\n'.join(text_lines[start_line:end_line])
                                        
                                        results.append({
                                            "block": "checkResultScreenshot",
                                            "screenshot_path": screenshot_path,
                                            "text": section_text.strip(),
                                            "total_accidents": total_accidents,
                                            "accident_number": i + 1
                                        })
                                        
                                        logger.info(f"✅ Fallback скриншот ДТП {i+1} сохранен: {screenshot_path}")
                                        
                                    except Exception as scroll_e:
                                        logger.error(f"❌ Ошибка fallback скриншота ДТП {i+1}: {scroll_e}")
                                        continue
                            
                            else:
                                # Одно ДТП или LI блоки не найдены - делаем общий скриншот
                                logger.info(f"📸 Делаем общий скриншот (одно ДТП или LI блоки не найдены)")
                                
                                timestamp = int(time.time())
                                screenshot_path = f"dtp_block_{timestamp}_{os.getpid()}_1.png"
                                
                                check_result_div.screenshot(screenshot_path)
                                text = check_result_div.get_attribute("innerText").strip()
                                
                                results.append({
                                    "block": "checkResultScreenshot",
                                    "screenshot_path": screenshot_path,
                                    "text": text,
                                    "total_accidents": 1,
                                    "accident_number": 1
                                })
                                
                                logger.info(f"✅ Общий скриншот ДТП сохранен: {screenshot_path}")
                        
                        except Exception as search_e:
                            logger.error(f"❌ Ошибка поиска элементов ДТП: {search_e}")
                            # Fallback - общий скриншот
                            timestamp = int(time.time())
                            screenshot_path = f"dtp_block_{timestamp}_{os.getpid()}_fallback.png"
                            
                            check_result_div.screenshot(screenshot_path)
                            text = check_result_div.get_attribute("innerText").strip()
                            
                            results.append({
                                "block": "checkResultScreenshot",
                                "screenshot_path": screenshot_path,
                                "text": text,
                                "total_accidents": total_accidents,
                                "accident_number": 1,
                                "error": f"Fallback скриншот: {search_e}"
                            })
                    
                    if results:
                        logger.info(f"✅ Получено {len(results)} скриншотов ДТП")
                        return results
                    else:
                        logger.warning("⚠️ Не удалось получить скриншоты ни одного ДТП")
                        return []
                        
                except Exception as e:
                    logger.error(f"❌ Ошибка извлечения результатов ДТП: {e}")
                    return []
                    
            else:  # WANTED или RESTRICTIONS
                section_ids = {
                    CheckType.WANTED: "checkAutoWanted",
                    CheckType.RESTRICTIONS: "checkAutoRestricted"
                }
                section_id = section_ids.get(check_type)
                if section_id:
                    try:
                        section = self.driver.find_element(By.CSS_SELECTOR, f"div#{section_id}")
                        try:
                            check_result_div = section.find_element(By.CSS_SELECTOR, "div.checkResult")
                            text = check_result_div.get_attribute("innerText").strip()
                        except Exception:
                            text = ""
                            
                        if not text:
                            ps = section.find_elements(By.TAG_NAME, "p")
                            ps_text = [p.get_attribute("innerText").strip() for p in ps 
                                     if p.get_attribute("innerText").strip() and 
                                     "description" not in p.get_attribute("class")]
                            text = "\n".join(ps_text)
                            
                        # Очищаем текст
                        text = text.replace("Выполняется запрос, ждите...", "")
                        text = text.replace("запросить сведения о\n            розыске", "")
                        text = text.replace("запросить сведения\n            об ограничениях", "")
                        text = text.replace("\n", " ").strip()
                        while "  " in text:
                            text = text.replace("  ", " ")
                            
                        return [{
                            "block": "checkResult",
                            "text": text
                        }]
                    except Exception as e:
                        logger.error(f"❌ Ошибка извлечения результатов {check_type.value}: {e}")
                        return []
                        
            return []
             
        except Exception as e:
            logger.error(f"❌ Ошибка извлечения результатов: {e}")
            return []

    def check_section_with_validation(self, vin: str, check_type: CheckType) -> CheckResult:
        """Проверка одной секции с валидацией и повторными попытками"""
        best_result = None
        best_score = 0.0
        
        for attempt in range(1, self.max_attempts + 1):
            logger.info(f"🔄 Попытка {attempt}/{self.max_attempts} для {check_type.value}")
            
            try:
                # Новый драйвер для каждой попытки
                if self.driver:
                    self.driver.quit()
                    self.driver = None
                
                self.setup_driver()
                self.driver.get(self.url)
                
                if not self.input_vin(vin):
                    continue

                # Прокручиваем к нужной секции
                section_ids = {
                    CheckType.REGISTRATION: "checkAutoHistory",
                    CheckType.ACCIDENTS: "checkAutoAiusdtp",
                    CheckType.WANTED: "checkAutoWanted",
                    CheckType.RESTRICTIONS: "checkAutoRestricted"
                }
                section_id = section_ids.get(check_type)
                if section_id:
                    section = self.driver.find_element(By.CSS_SELECTOR, f"div#{section_id}")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", section)
                    time.sleep(0.5)

                # Находим и кликаем кнопку
                button_selectors = {
                    CheckType.REGISTRATION: "a.checker[data-type='history']",
                    CheckType.ACCIDENTS: "a.checker[data-type='aiusdtp']",
                    CheckType.WANTED: "a.checker[data-type='wanted']",
                    CheckType.RESTRICTIONS: "a.checker[data-type='restricted']"
                }
                selector = button_selectors.get(check_type)
                if not selector:
                    continue

                # Решаем капчу и получаем результаты
                captcha_attempts = 10
                for captcha_attempt in range(1, captcha_attempts + 1):
                    try:
                        button = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        button.click()
                    except Exception as e:
                        logger.error(f"❌ Ошибка нажатия кнопки: {e}")
                        break

                    # Решаем капчу
                    try:
                        modal = self.wait.until(
                            EC.visibility_of_element_located((By.ID, "captchaDialog"))
                        )
                        captcha_img, captcha_input = None, None
                        loader_src = None
                        for i in range(30):
                            try:
                                captcha_img = modal.find_element(By.CSS_SELECTOR, "#captchaPic img")
                                captcha_input = modal.find_element(By.CSS_SELECTOR, "input[name='captcha_num']")
                                src = captcha_img.get_attribute("src")
                                if i == 0:
                                    loader_src = src
                                if src and "base64" in src and len(src) > 1000 and src != loader_src:
                                    break
                            except Exception:
                                pass
                            time.sleep(0.5)
                        else:
                            continue

                        # Создаем временный файл с уникальным именем
                        timestamp = int(time.time())
                        temp_captcha_path = f"temp_captcha_{timestamp}_{os.getpid()}.png"
                        self.temp_files.append(temp_captcha_path)
                        
                        src = captcha_img.get_attribute("src")
                        if src and src.startswith("data:image"):
                            b64data = src.split(",", 1)[1]
                            with open(temp_captcha_path, "wb") as f:
                                f.write(base64.b64decode(b64data))
                        else:
                            captcha_screenshot = captcha_img.screenshot_as_png
                            with open(temp_captcha_path, "wb") as f:
                                f.write(captcha_screenshot)

                        result = solve_captcha(temp_captcha_path)
                        if result:
                            captcha_input.clear()
                            captcha_input.send_keys(result)
                            captcha_solved = True
                            self.wait.until(EC.invisibility_of_element_located((By.ID, "captchaDialog")))
                        else:
                            continue
                    except Exception as e:
                        logger.error(f"❌ Ошибка решения CAPTCHA: {e}")
                        continue

                    # Ждем завершения рекламы
                    ad_waited = self.wait_for_ad_completion()

                    # Извлекаем результаты
                    results = self.extract_results(check_type)

                    # Проверяем наличие ошибки капчи
                    try:
                        error_elements = self.driver.find_elements(By.CSS_SELECTOR, "p.check-space.check-message")
                        captcha_error = False
                        for el in error_elements:
                            if "Проверка CAPTCHA не была пройдена" in el.text:
                                captcha_error = True
                                break
                        if captcha_error:
                            if captcha_attempt < captcha_attempts:
                                time.sleep(1)
                                continue
                            else:
                                break
                    except Exception:
                        pass

                    if results:
                        # Валидируем результаты
                        is_valid, quality_score, validation_errors = DataValidator.validate_section_data(
                            check_type, results
                        )
                        
                        current_result = CheckResult(
                            check_type=check_type,
                            success=True,
                            data=results,
                            captcha_solved=True,
                            ad_waited=ad_waited,
                            attempt_number=attempt,
                            quality_score=quality_score,
                            validation_errors=validation_errors
                        )
                        
                        logger.info(f"✅ Попытка {attempt}: качество {quality_score:.1f}%, валидация: {is_valid}")
                        
                        # Сохраняем лучший результат
                        if quality_score > best_score:
                            best_result = current_result
                            best_score = quality_score
                        
                        # Если качество достаточно высокое, возвращаем результат
                        if is_valid and quality_score >= self.min_quality_score:
                            logger.info(f"🎯 Качественные данные получены с попытки {attempt}")
                            return current_result
                        else:
                            logger.warning(f"⚠️ Низкое качество данных: {quality_score:.1f}%, ошибки: {validation_errors}")
                    
                    break  # Выходим из цикла капчи если получили результаты
                    
            except Exception as e:
                logger.error(f"❌ Ошибка в попытке {attempt}: {e}")
                
            finally:
                self.cleanup_temp_files()
                if self.driver:
                    self.driver.quit()
                    self.driver = None
            
            # Пауза между попытками
            if attempt < self.max_attempts:
                time.sleep(2)
        
        # Возвращаем лучший результат или ошибку
        if best_result:
            logger.info(f"📊 Возвращаем лучший результат: качество {best_score:.1f}%")
            return best_result
        else:
            return CheckResult(
                check_type=check_type, 
                success=False, 
                error="Не удалось получить качественные данные после всех попыток"
            )

def check_section_wrapper_reliable(args):
    """Обертка для надежной проверки секции в отдельном процессе"""
    try:
        vin, section, max_attempts, min_quality_score = args
        checker = ReliableGibddChecker(max_attempts=max_attempts, min_quality_score=min_quality_score)
        result = checker.check_section_with_validation(vin, section)
        return result
    except Exception as e:
        logger.error(f"❌ Ошибка в процессе: {str(e)}")
        return CheckResult(section, False, error=str(e))

def check_vin_reliable(vin: str, max_attempts: int = 3, min_quality_score: float = 60.0) -> Dict[str, Any]:
    """Надежная параллельная проверка всех секций с валидацией"""
    try:
        sections = [CheckType.REGISTRATION, CheckType.ACCIDENTS, CheckType.WANTED, CheckType.RESTRICTIONS]
        
        logger.info(f"🚀 Запуск надежной проверки VIN: {vin}")
        logger.info(f"🎯 Параметры: макс. попыток={max_attempts}, мин. качество={min_quality_score}%")
        
        # Создаем пул процессов
        with multiprocessing.Pool(processes=4) as pool:
            # Подготавливаем аргументы для каждого процесса
            args = [(vin, section, max_attempts, min_quality_score) for section in sections]
            
            # Запускаем проверки параллельно
            results = pool.map(check_section_wrapper_reliable, args)
            
            # Проверяем результаты
            if not results or len(results) != 4:
                logger.error(f"❌ Неожиданное количество результатов: {len(results) if results else 0}")
                return {
                    "vin": vin,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "error": "Получено неожиданное количество результатов",
                    "results": []
                }
            
            # Формируем итоговый результат
            total_quality = 0
            quality_count = 0
            
            formatted_results = []
            for result in results:
                if not isinstance(result, CheckResult):
                    logger.error(f"❌ Некорректный тип результата: {type(result)}")
                    continue
                
                formatted_result = {
                    "type": result.check_type.value,
                    "success": result.success,
                    "data": result.data or [],
                    "error": result.error,
                    "captcha_solved": result.captcha_solved,
                    "ad_waited": result.ad_waited,
                    "attempt_number": result.attempt_number,
                    "quality_score": result.quality_score,
                    "validation_errors": result.validation_errors or []
                }
                formatted_results.append(formatted_result)
                
                if result.success and result.quality_score > 0:
                    total_quality += result.quality_score
                    quality_count += 1
        
            avg_quality = total_quality / quality_count if quality_count > 0 else 0
            successful_sections = sum(1 for r in formatted_results if r["success"])
            
            final_result = {
                "vin": vin,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "results": formatted_results,
                "summary": {
                    "successful_sections": successful_sections,
                    "total_sections": len(formatted_results),
                    "average_quality_score": avg_quality,
                    "high_quality_sections": sum(1 for r in formatted_results 
                                                if r["success"] and r["quality_score"] >= min_quality_score)
                }
            }
            
            logger.info(f"✅ Проверка завершена: {successful_sections}/4 секций, средн. качество: {avg_quality:.1f}%")
            return final_result
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка при надежной проверке: {str(e)}")
        return {
            "vin": vin,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error": str(e),
            "results": []
        }

def main():
    """Тестирование надежного чекера"""
    vin = "Z94K241CBLR147119"  # Тестовый VIN
    result = check_vin_reliable(vin, max_attempts=2, min_quality_score=65.0)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 
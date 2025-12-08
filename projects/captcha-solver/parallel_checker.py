import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import logging
import os
import tempfile
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import base64
from PIL import Image, ImageChops
from ultimate_adaptive_solver import solve_captcha

# Настройка логирования (уменьшаем количество логов)
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
    data: Dict = None
    error: str = None
    captcha_solved: bool = False
    ad_waited: bool = False

class ParallelGibddChecker:
    """Параллельный чекер ГИБДД"""
    
    def __init__(self):
        self.url = "https://xn--90adear.xn--p1ai/check/auto"
        self.driver = None
        self.wait = None
        self.temp_files = []  # Список временных файлов для очистки
        
    def cleanup_temp_files(self):
        """Очистка временных файлов"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass
        self.temp_files.clear()
        
    def setup_driver(self):
        """Настройка веб-драйвера в headless режиме"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # Отключаем звук полностью
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--disable-audio-output")
        chrome_options.add_argument("--disable-sound")
        chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
        
        # Отключаем изображения и медиа для ускорения (кроме капч)
        prefs = {
            "profile.managed_default_content_settings.images": 1,  # Оставляем изображения для капч
            "profile.managed_default_content_settings.media_stream": 2,
            "profile.default_content_settings.popups": 0,
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        
    def input_vin(self, vin: str) -> bool:
        """Ввод VIN-номера"""
        try:
            vin_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "vin"))
            )
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
            
    def extract_results(self, check_type: CheckType) -> Dict:
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
                        "text": text,
                        "html": check_result_div.get_attribute("outerHTML")
                    })
                except Exception as e:
                    logger.error(f"❌ Не удалось найти div.checkResult: {e}")
                    
                try:
                    ownership_ul = self.driver.find_element(By.CSS_SELECTOR, "ul.ownershipPeriods")
                    text = ownership_ul.get_attribute("innerText")
                    results.append({
                        "block": "ownershipPeriods",
                        "text": text,
                        "html": ownership_ul.get_attribute("outerHTML")
                    })
                except Exception as e:
                    logger.error(f"❌ Не удалось найти ul.ownershipPeriods: {e}")
                    
                if results:
                    return {
                        "type": check_type.value,
                        "data": results,
                        "timestamp": time.time()
                    }
                    
            elif check_type == CheckType.ACCIDENTS:
                try:
                    results = []
                    dtp_section = self.driver.find_element(By.CSS_SELECTOR, "div#checkAutoAiusdtp")
                    
                    # Определяем общее количество ДТП из текста "Номер ТС/из всего ТС в ДТП: X/Y"
                    total_accidents = 1  # По умолчанию предполагаем одно ДТП
                    current_accident = 1
                    
                    try:
                        # Ищем текст с информацией о количестве ДТП
                        page_text = dtp_section.get_attribute("innerText")
                        if "из всего ТС в ДТП:" in page_text:
                            import re
                            # Паттерн для поиска "X/Y" где Y - общее количество ДТП
                            pattern = r"Номер ТС/из всего ТС в ДТП:\s*(\d+)/(\d+)"
                            match = re.search(pattern, page_text)
                            if match:
                                current_accident = int(match.group(1))
                                total_accidents = int(match.group(2))
                                logger.info(f"🔍 Найдено ДТП: {current_accident}/{total_accidents}")
                            else:
                                # Альтернативный паттерн для поиска простого "X/Y"
                                pattern2 = r"(\d+)/(\d+)"
                                match2 = re.search(pattern2, page_text)
                                if match2:
                                    current_accident = int(match2.group(1))
                                    total_accidents = int(match2.group(2))
                                    logger.info(f"🔍 Найдено ДТП (альт. поиск): {current_accident}/{total_accidents}")
                    except Exception as e:
                        logger.warning(f"⚠️ Не удалось определить количество ДТП: {e}")
                    
                    # Делаем скриншоты всех ДТП
                    for accident_num in range(1, total_accidents + 1):
                        try:
                            logger.info(f"📸 Обрабатываем ДТП {accident_num}/{total_accidents}")
                            
                            # Если это не первое ДТП, пытаемся найти навигационные кнопки
                            if accident_num > current_accident:
                                # Ищем кнопку "следующее" или аналогичную для навигации
                                navigation_attempted = False
                                for nav_selector in [
                                    "button[onclick*='next']", "a[onclick*='next']",
                                    "button[onclick*='следующ']", "a[onclick*='следующ']",
                                    ".pagination-next", ".next-button", 
                                    "button:contains('>')", "a:contains('>')",
                                    "[data-action='next']"
                                ]:
                                    try:
                                        nav_button = dtp_section.find_element(By.CSS_SELECTOR, nav_selector)
                                        if nav_button.is_displayed() and nav_button.is_enabled():
                                            self.driver.execute_script("arguments[0].click();", nav_button)
                                            time.sleep(1)  # Ждем загрузки нового ДТП
                                            navigation_attempted = True
                                            logger.info(f"✅ Переключились на ДТП {accident_num}")
                                            break
                                    except Exception:
                                        continue
                                
                                if not navigation_attempted:
                                    logger.warning(f"⚠️ Не удалось найти навигацию для ДТП {accident_num}")
                                    break
                            
                            elif accident_num < current_accident:
                                # Ищем кнопку "предыдущее" или аналогичную для навигации назад
                                navigation_attempted = False
                                for nav_selector in [
                                    "button[onclick*='prev']", "a[onclick*='prev']",
                                    "button[onclick*='предыдущ']", "a[onclick*='предыдущ']",
                                    ".pagination-prev", ".prev-button",
                                    "button:contains('<')", "a:contains('<')",
                                    "[data-action='prev']"
                                ]:
                                    try:
                                        nav_button = dtp_section.find_element(By.CSS_SELECTOR, nav_selector)
                                        if nav_button.is_displayed() and nav_button.is_enabled():
                                            self.driver.execute_script("arguments[0].click();", nav_button)
                                            time.sleep(1)  # Ждем загрузки нового ДТП
                                            navigation_attempted = True
                                            logger.info(f"✅ Переключились на ДТП {accident_num}")
                                            break
                                    except Exception:
                                        continue
                                
                                if not navigation_attempted:
                                    logger.warning(f"⚠️ Не удалось найти навигацию для ДТП {accident_num}")
                                    break
                            
                            # Теперь делаем скриншот текущего ДТП
                            try:
                                check_result_div = dtp_section.find_element(By.CSS_SELECTOR, "div.checkResult")
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", check_result_div)
                                time.sleep(0.5)
                                
                                # Проверяем размеры элемента перед скриншотом
                                size = check_result_div.size
                                if size['width'] == 0 or size['height'] == 0:
                                    logger.error(f"❌ Элемент ДТП {accident_num} имеет нулевые размеры: {size}")
                                    # Пытаемся получить текст вместо скриншота
                                    try:
                                        text = check_result_div.get_attribute("innerText").strip()
                                        if text:
                                            results.append({
                                                "block": "checkResult",
                                                "text": text,
                                                "accident_number": accident_num
                                            })
                                    except Exception:
                                        pass
                                    continue
                                
                                # Создаем уникальное имя файла со временем для каждого ДТП
                                timestamp = int(time.time())
                                screenshot_path = f"dtp_block_{timestamp}_{os.getpid()}_{accident_num}.png"
                                
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
                                    except Exception as crop_e:
                                        logger.error(f"❌ Не удалось обрезать скриншот ДТП {accident_num}: {crop_e}")
                                    
                                    # Получаем также текст для резерва
                                    text = check_result_div.get_attribute("innerText").strip()
                                    
                                    results.append({
                                        "block": "checkResultScreenshot",
                                        "screenshot_path": screenshot_path,
                                        "text": text,
                                        "accident_number": accident_num,
                                        "total_accidents": total_accidents
                                    })
                                    
                                    logger.info(f"✅ Скриншот ДТП {accident_num} сохранен: {screenshot_path}")
                                    
                                except Exception as screenshot_e:
                                    logger.error(f"❌ Не удалось сделать скриншот ДТП {accident_num}: {screenshot_e}")
                                    # Возвращаем только текст
                                    try:
                                        text = check_result_div.get_attribute("innerText").strip()
                                        if text:
                                            results.append({
                                                "block": "checkResult",
                                                "text": text,
                                                "accident_number": accident_num
                                            })
                                    except Exception:
                                        pass
                                        
                            except Exception as e:
                                logger.error(f"❌ Ошибка обработки ДТП {accident_num}: {e}")
                                continue
                                
                        except Exception as e:
                            logger.error(f"❌ Ошибка в цикле для ДТП {accident_num}: {e}")
                            continue
                    
                    if results:
                        logger.info(f"✅ Обработано {len(results)} ДТП из {total_accidents}")
                        return {
                            "type": check_type.value,
                            "data": results
                        }
                    else:
                        logger.warning("⚠️ Не удалось получить данные ни одного ДТП")
                        return {"type": check_type.value, "data": []}
                        
                except Exception as e:
                    logger.error(f"❌ Ошибка извлечения результатов ДТП: {e}")
                    return {"type": check_type.value, "data": []}
                    
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
                            
                        # Очищаем текст от служебных строк
                        text = text.replace("Выполняется запрос, ждите...", "")
                        text = text.replace("запросить сведения о\n            розыске", "")
                        text = text.replace("запросить сведения\n            об ограничениях", "")
                        text = text.replace("\n", " ").strip()
                        while "  " in text:
                            text = text.replace("  ", " ")
                            
                        return {
                            "type": check_type.value,
                            "data": [{
                                "block": "checkResult",
                                "text": text
                            }]
                        }
                    except Exception as e:
                        logger.error(f"❌ Ошибка извлечения результатов {check_type.value}: {e}")
                        return {"type": check_type.value, "data": []}
                        
            return {"type": check_type.value, "data": []}
             
        except Exception as e:
            logger.error(f"❌ Ошибка извлечения результатов: {e}")
            return {"type": check_type.value, "data": []}
            
    def check_section(self, vin: str, check_type: CheckType) -> CheckResult:
        """Проверка одной секции"""
        try:
            self.setup_driver()
            self.driver.get(self.url)
            
            if not self.input_vin(vin):
                return CheckResult(check_type, False, error="Ошибка ввода VIN")

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
                return CheckResult(check_type, False, error="Неизвестный тип проверки")

            max_attempts = 10
            for attempt in range(1, max_attempts + 1):
                try:
                    button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    button.click()
                except Exception as e:
                    logger.error(f"❌ Ошибка поиска/нажатия кнопки: {e}")
                    return CheckResult(check_type, False, error="Кнопка проверки не найдена")

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
                        logger.error("❌ Не удалось дождаться загрузки капчи")
                        return CheckResult(check_type, False, error="Не удалось дождаться загрузки капчи")

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
                        return CheckResult(check_type, False, error="Не удалось решить CAPTCHA")
                except Exception as e:
                    logger.error(f"❌ Ошибка решения/отправки CAPTCHA: {e}")
                    return CheckResult(check_type, False, error="Не удалось решить/отправить CAPTCHA")

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
                        if attempt < max_attempts:
                            time.sleep(1)
                            continue
                        else:
                            return CheckResult(check_type, False, error="Капча не пройдена после нескольких попыток")
                except Exception:
                    pass

                if results and isinstance(results, dict) and results.get("data"):
                    return CheckResult(
                        check_type=check_type,
                        success=True,
                        data=results["data"],  # Используем только данные
                        captcha_solved=True,
                        ad_waited=ad_waited
                    )
                else:
                    return CheckResult(check_type, False, error="Не удалось извлечь результаты")

            return CheckResult(check_type, False, error="Не удалось пройти капчу после нескольких попыток")
            
        except Exception as e:
            logger.error(f"❌ Ошибка проверки {check_type.value}: {e}")
            return CheckResult(check_type, False, error=str(e))
        finally:
            self.cleanup_temp_files()  # Очищаем временные файлы
            if self.driver:
                self.driver.quit()

def check_section_wrapper(args):
    """Обертка для проверки секции в отдельном процессе"""
    try:
        checker, vin, section = args
        result = checker.check_section(vin, section)
        return result
    except Exception as e:
        logger.error(f"❌ Ошибка в процессе: {str(e)}")
        return CheckResult(section, False, error=str(e))

def check_vin_parallel(vin: str) -> Dict[str, Any]:
    """Параллельная проверка всех секций"""
    try:
        sections = [CheckType.REGISTRATION, CheckType.ACCIDENTS, CheckType.WANTED, CheckType.RESTRICTIONS]
        
        # Создаем пул процессов - ограничиваем количество одновременных процессов для экономии ресурсов
        # Будем использовать 4 процесса для 4 секций, но в контролируемом пуле
        with multiprocessing.Pool(processes=min(4, len(sections))) as pool:
            # Создаем экземпляр ParallelGibddChecker для каждой секции
            checkers = [ParallelGibddChecker() for _ in sections]
            
            # Подготавливаем аргументы для каждого процесса
            args = [(checker, vin, section) for checker, section in zip(checkers, sections)]
            
            # Запускаем проверки параллельно
            results = pool.map(check_section_wrapper, args)
            
            # Проверяем что все результаты корректные
            if not results or len(results) != len(sections):
                logger.error(f"❌ Неожиданное количество результатов: {len(results) if results else 0} из {len(sections)}")
                return {
                    "vin": vin,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "error": f"Получено неожиданное количество результатов: {len(results) if results else 0} из {len(sections)}",
                    "results": []
                }
            
            # Проверяем типы результатов
            for i, result in enumerate(results):
                if not isinstance(result, CheckResult):
                    logger.error(f"❌ Результат {i} не является CheckResult: {type(result)}")
                    return {
                        "vin": vin,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "error": f"Некорректный тип результата #{i}: {type(result)}",
                        "results": []
                    }
        
        # Формируем итоговый результат
        result = {
            "vin": vin,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": [
                {
                    "type": result.check_type.value,
                    "success": result.success,
                    "data": result.data,
                    "error": result.error,
                    "captcha_solved": result.captcha_solved,
                    "ad_waited": result.ad_waited
                }
                for result in results
            ]
        }
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка при параллельной проверке: {str(e)}")
        return {
            "vin": vin,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error": str(e),
            "results": []
        }

def main():
    """Тестирование параллельного чекера"""
    vin = "WBAJC31010B050810"  # Пример VIN
    result = check_vin_parallel(vin)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 
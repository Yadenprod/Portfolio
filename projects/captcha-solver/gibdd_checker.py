import asyncio
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import base64
import io
from PIL import Image, ImageChops
import ddddocr
from ultimate_adaptive_solver import solve_captcha
import json
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
import numpy as np

# Настройка логирования
logging.basicConfig(level=logging.INFO)
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
    data: Optional[Dict] = None
    error: Optional[str] = None
    captcha_solved: bool = False
    ad_waited: bool = False

class GIBDDChecker:
    """Автоматизированный чекер ГИБДД"""
    
    def __init__(self, headless: bool = True):
        self.base_url = "https://гибдд.рф/check/auto"
        self.headless = headless
        self.driver = None
        self.captcha_solver = None
        self.wait = None
        
    def _setup_driver(self):
        """Настройка веб-драйвера"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # Отключаем изображения и медиа для ускорения (кроме капч)
        prefs = {
            "profile.managed_default_content_settings.images": 1,  # Оставляем изображения для капч
            "profile.managed_default_content_settings.media_stream": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        
    def _setup_captcha_solver(self):
        """Инициализация решателя капч"""
        logger.info("🚀 Инициализация CAPTCHA-солвера...")
        # Используем наш проверенный солвер
        self.captcha_solver = True
        logger.info("✅ CAPTCHA-солвер готов!")
        
    async def initialize(self):
        """Инициализация чекера"""
        logger.info("🔧 Инициализация ГИБДД-чекера...")
        self._setup_driver()
        self._setup_captcha_solver()
        logger.info("✅ ГИБДД-чекер готов!")
        
    async def close(self):
        """Закрытие чекера"""
        if self.driver:
            self.driver.quit()
            
    def _input_vin(self, vin: str) -> bool:
        """Ввод VIN-номера"""
        try:
            logger.info(f"📝 Ввод VIN: {vin}")
            
            # Находим поле ввода VIN
            vin_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "vin"))
            )
            
            # Очищаем и вводим VIN
            vin_input.clear()
            vin_input.send_keys(vin)
            
            logger.info("✅ VIN введен успешно")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка ввода VIN: {e}")
            return False
            
    def _solve_captcha_element(self, captcha_img_element) -> Optional[str]:
        """Решение капчи"""
        try:
            logger.info("🔍 Обнаружена CAPTCHA, решаем...")
            
            # Получаем скриншот капчи
            captcha_screenshot = captcha_img_element.screenshot_as_png
            
            # Сохраняем временно для решения
            temp_captcha_path = "temp_captcha.png"
            with open(temp_captcha_path, "wb") as f:
                f.write(captcha_screenshot)
                
            # Решаем капчу нашим солвером
            result = solve_captcha(temp_captcha_path)
            
            if result:
                logger.info(f"✅ CAPTCHA решена: {result}")
                return result
            else:
                logger.error("❌ Не удалось решить CAPTCHA")
                return None
                
        except Exception as e:
            logger.error(f"❌ Ошибка решения CAPTCHA: {e}")
            return None
            
    def _wait_for_ad_completion(self, timeout: int = 90) -> bool:
        try:
            logger.info("📺 Ожидание завершения рекламы...")
            start_time = time.time()
            ad_closed = False

            while time.time() - start_time < timeout:
                # Ищем все видимые модальные окна рекламы
                ad_modals = self.driver.find_elements(By.CSS_SELECTOR, ".modal, .fancybox-inner, .fancybox-container, .fancybox-bg, .fancybox-slide, .fancybox-content, .adds-modal")
                ad_modals = [m for m in ad_modals if m.is_displayed()]
                ad_modal = ad_modals[0] if ad_modals else None

                # Если модалка исчезла — реклама завершена
                if not ad_modal:
                    logger.info("✅ Реклама завершена (модалка исчезла)")
                    ad_closed = True
                    break

                # Пробуем найти и кликнуть по кнопке закрытия
                try:
                    close_btn = ad_modal.find_element(By.XPATH, ".//button[contains(@class, 'close') or contains(@class, 'fancybox-close') or contains(@class, 'close_modal_window') or contains(text(), 'Закрыть') or contains(text(), 'X')]")
                    if close_btn.is_displayed() and close_btn.is_enabled():
                        close_btn.click()
                        logger.info("✅ Кнопка закрытия рекламы нажата")
                        # Ждем исчезновения модалки
                        for _ in range(20):
                            time.sleep(0.5)
                            ad_modals = self.driver.find_elements(By.CSS_SELECTOR, ".modal, .fancybox-inner, .fancybox-container, .fancybox-bg, .fancybox-slide, .fancybox-content, .adds-modal")
                            ad_modals = [m for m in ad_modals if m.is_displayed()]
                            if not ad_modals:
                                ad_closed = True
                                logger.info("✅ Реклама закрыта и модалка исчезла")
                                break
                        if ad_closed:
                            break
                except Exception:
                    pass

                # Если это изображение — ждем не менее 7 секунд, затем проверяем исчезновение
                if ad_modal and ("img" in ad_modal.get_attribute("innerHTML") or ad_modal.find_elements(By.TAG_NAME, "img")):
                    if time.time() - start_time < 7:
                        time.sleep(1)
                        continue

                # Если это видео — ждем появления кнопки "X" или исчезновения модалки
                if ad_modal and (ad_modal.find_elements(By.TAG_NAME, "video") or "video" in ad_modal.get_attribute("innerHTML")):
                    # Просто ждем появления кнопки или исчезновения модалки
                    pass

                time.sleep(1)

            if not ad_closed:
                logger.warning("⚠️ Превышен таймаут ожидания рекламы")
            return ad_closed

        except Exception as e:
            logger.error(f"❌ Ошибка ожидания рекламы: {e}")
            return False
            
    def _extract_results(self, check_type: CheckType) -> Optional[Dict]:
        """Извлечение результатов проверки"""
        try:
            logger.info(f"📊 Извлечение результатов: {check_type.value}")
            
            # Ждем загрузки результатов
            time.sleep(3)
            
            # Для типа registration извлекаем только нужный блок
            if check_type == CheckType.REGISTRATION:
                try:
                    results = []
                    # 1. div.checkResult (основной блок)
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
                    # 2. ul.ownershipPeriods (периоды владения)
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
                        logger.info("✅ Извлечены оба блока: checkResult и ownershipPeriods")
                        return {
                            "type": check_type.value,
                            "data": results,
                            "timestamp": time.time()
                        }
                    else:
                        logger.warning("⚠️ Не удалось найти ни один из нужных блоков")
                        return None
                except Exception as e:
                    logger.error(f"❌ Не удалось извлечь оба блока: {e}")
                    return None

            # Для типа ACCIDENTS извлекаем нужные блоки
            if check_type == CheckType.ACCIDENTS:
                try:
                    results = []
                    # Прокручиваем к div.checkResult внутри div#checkAutoAiusdtp и делаем скриншот
                    try:
                        dtp_section = self.driver.find_element(By.CSS_SELECTOR, "div#checkAutoAiusdtp")
                        check_result_div = dtp_section.find_element(By.CSS_SELECTOR, "div.checkResult")
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", check_result_div)
                        time.sleep(0.5)
                        screenshot_path = "dtp_block.png"
                        check_result_div.screenshot(screenshot_path)
                        # Обрезаем пустые поля по краям
                        try:
                            img = Image.open(screenshot_path)
                            bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
                            diff = ImageChops.difference(img, bg)
                            bbox = diff.getbbox()
                            if bbox:
                                cropped = img.crop(bbox)
                                cropped.save(screenshot_path)
                        except Exception as crop_e:
                            logger.error(f"❌ Не удалось обрезать скриншот: {crop_e}")
                        results.append({
                            "block": "checkResultScreenshot",
                            "screenshot_path": screenshot_path
                        })
                    except Exception as e:
                        logger.error(f"❌ Не удалось сделать скриншот div.checkResult внутри div#checkAutoAiusdtp: {e}")
                    return results
                except Exception as e:
                    logger.error(f"❌ Ошибка извлечения результатов ДТП: {e}")
                    return []

            # Для типа WANTED извлекаем текст из div.checkResult внутри div#checkAutoWanted
            if check_type == CheckType.WANTED:
                try:
                    results = []
                    try:
                        wanted_section = self.driver.find_element(By.CSS_SELECTOR, "div#checkAutoWanted")
                        # Пробуем найти div.checkResult
                        try:
                            check_result_div = wanted_section.find_element(By.CSS_SELECTOR, "div.checkResult")
                            text = check_result_div.get_attribute("innerText").strip()
                        except Exception:
                            text = ""
                        # Если текст пустой — ищем все <p> и собираем их текст (кроме .description)
                        if not text:
                            ps = wanted_section.find_elements(By.TAG_NAME, "p")
                            ps_text = [p.get_attribute("innerText").strip() for p in ps if p.get_attribute("innerText").strip() and "description" not in p.get_attribute("class")]
                            text = "\n".join(ps_text)
                        results.append({
                            "block": "checkResult",
                            "text": text
                        })
                    except Exception as e:
                        logger.error(f"❌ Не удалось извлечь текст из div.checkResult или <p> внутри div#checkAutoWanted: {e}")
                    return results
                except Exception as e:
                    logger.error(f"❌ Ошибка извлечения результатов розыска: {e}")
                    return []

            # Для типа RESTRICTIONS извлекаем текст из div.checkResult внутри div#checkAutoRestricted
            if check_type == CheckType.RESTRICTIONS:
                try:
                    results = []
                    try:
                        restricted_section = self.driver.find_element(By.CSS_SELECTOR, "div#checkAutoRestricted")
                        # Пробуем найти div.checkResult
                        try:
                            check_result_div = restricted_section.find_element(By.CSS_SELECTOR, "div.checkResult")
                            text = check_result_div.get_attribute("innerText").strip()
                        except Exception:
                            text = ""
                        # Если текст пустой — ищем все <p> и собираем их текст (кроме .description)
                        if not text:
                            ps = restricted_section.find_elements(By.TAG_NAME, "p")
                            ps_text = [p.get_attribute("innerText").strip() for p in ps if p.get_attribute("innerText").strip() and "description" not in p.get_attribute("class")]
                            text = "\n".join(ps_text)
                        results.append({
                            "block": "checkResult",
                            "text": text
                        })
                    except Exception as e:
                        logger.error(f"❌ Не удалось извлечь текст из div.checkResult или <p> внутри div#checkAutoRestricted: {e}")
                    return results
                except Exception as e:
                    logger.error(f"❌ Ошибка извлечения результатов ограничений: {e}")
                    return []

            # Для остальных типов — прежняя логика
            result_selectors = {
                CheckType.ACCIDENTS: [
                    ".accidents-info",
                    ".dtp-table",
                    ".accident-data"
                ],
                CheckType.WANTED: [
                    ".wanted-info",
                    ".search-data"
                ],
                CheckType.RESTRICTIONS: [
                    ".restrictions-info",
                    ".pledge-data"
                ]
            }
            
            # Пробуем найти результаты
            for selector in result_selectors.get(check_type, []):
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        # Извлекаем текст результатов
                        results = []
                        for element in elements:
                            if element.is_displayed():
                                results.append({
                                    "text": element.text,
                                    "html": element.get_attribute("innerHTML")
                                })
                        
                        if results:
                            logger.info("✅ Результаты извлечены")
                            return {
                                "type": check_type.value,
                                "data": results,
                                "timestamp": time.time()
                            }
                except:
                    continue
                    
            # Если специфичные селекторы не сработали, берем общий контент
            try:
                page_content = self.driver.find_element(By.TAG_NAME, "body").text
                return {
                    "type": check_type.value,
                    "data": [{"text": page_content}],
                    "timestamp": time.time()
                }
            except:
                pass
                
            logger.warning("⚠️ Результаты не найдены")
            return None
            
        except Exception as e:
            logger.error(f"❌ Ошибка извлечения результатов: {e}")
            return None
            
    async def perform_check(self, vin: str, check_type: CheckType, reload_page: bool = True) -> CheckResult:
        """Выполнение одной проверки"""
        try:
            logger.info(f"🔍 Начало проверки: {check_type.value} для VIN: {vin}")
            if reload_page:
                self.driver.get(self.base_url)
                if not self._input_vin(vin):
                    return CheckResult(check_type, False, error="Ошибка ввода VIN")

            # Прокручиваем к нужной секции перед поиском кнопки
            try:
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
            except Exception as e:
                logger.warning(f"⚠️ Не удалось прокрутить к секции {check_type.value}: {e}")

            # Используем CSS-селекторы для разных типов проверок
            button_selectors = {
                CheckType.REGISTRATION: "a.checker[data-type='history']",
                CheckType.ACCIDENTS: "a.checker[data-type='aiusdtp']",
                CheckType.WANTED: "a.checker[data-type='wanted']",
                CheckType.RESTRICTIONS: "a.checker[data-type='restricted']"
            }
            selector = button_selectors.get(check_type)
            if not selector:
                return CheckResult(check_type, False, error="Неизвестный тип проверки (селектор)")

            max_attempts = 10
            for attempt in range(1, max_attempts + 1):
                try:
                    button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    button.click()
                    logger.info(f"✅ Нажата кнопка: {selector} (попытка {attempt})")
                except Exception as e:
                    logger.error(f"❌ Ошибка поиска/нажатия кнопки: {e}")
                    return CheckResult(check_type, False, error="Кнопка проверки не найдена")

                # Ждем появления модального окна с капчей
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
                        logger.error("❌ Не удалось дождаться загрузки капчи (src не изменился)")
                        return CheckResult(check_type, False, error="Не удалось дождаться загрузки капчи (src не изменился)")
                    temp_captcha_path = "temp_captcha.png"
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
                        logger.info(f"✅ CAPTCHA решена: {result}")
                        captcha_input.clear()
                        captcha_input.send_keys(result)
                        captcha_solved = True
                        self.wait.until(EC.invisibility_of_element_located((By.ID, "captchaDialog")))
                        logger.info("✅ CAPTCHA решена и окно закрыто")
                    else:
                        return CheckResult(check_type, False, error="Не удалось решить CAPTCHA")
                except Exception as e:
                    logger.error(f"❌ Ошибка решения/отправки CAPTCHA: {e}")
                    return CheckResult(check_type, False, error="Не удалось решить/отправить CAPTCHA")

                # Ждем завершения рекламы
                ad_waited = self._wait_for_ad_completion()

                # Извлекаем результаты
                results = self._extract_results(check_type)

                # Проверяем наличие ошибки капчи на странице
                try:
                    error_elements = self.driver.find_elements(By.CSS_SELECTOR, "p.check-space.check-message")
                    captcha_error = False
                    for el in error_elements:
                        if "Проверка CAPTCHA не была пройдена" in el.text:
                            captcha_error = True
                            logger.warning(f"❌ Капча не пройдена (попытка {attempt})")
                            break
                    if captcha_error:
                        if attempt < max_attempts:
                            time.sleep(1)
                            continue  # Пробуем еще раз
                        else:
                            return CheckResult(check_type, False, error="Капча не пройдена после нескольких попыток")
                except Exception:
                    pass

                if results:
                    return CheckResult(
                        check_type=check_type,
                        success=True,
                        data=results,
                        captcha_solved=True,
                        ad_waited=ad_waited
                    )
                else:
                    return CheckResult(check_type, False, error="Не удалось извлечь результаты")

            return CheckResult(check_type, False, error="Не удалось пройти капчу после нескольких попыток")
        except Exception as e:
            logger.error(f"❌ Ошибка проверки {check_type.value}: {e}")
            return CheckResult(check_type, False, error=str(e))
            
    async def check_vehicle(self, vin: str, check_types: List[CheckType] = None) -> List[CheckResult]:
        """Полная проверка автомобиля"""
        if check_types is None:
            check_types = [CheckType.REGISTRATION, CheckType.ACCIDENTS]
        logger.info(f"🚗 Начало полной проверки VIN: {vin}")
        results = []
        for idx, check_type in enumerate(check_types):
            try:
                reload_page = (idx == 0)
                result = await self.perform_check(vin, check_type, reload_page=reload_page)
                results.append(result)
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"❌ Ошибка проверки {check_type.value}: {e}")
                results.append(CheckResult(check_type, False, error=str(e)))
        logger.info(f"✅ Проверка завершена. Успешно: {sum(1 for r in results if r.success)}/{len(results)}")
        return results

# Пример использования
async def main():
    """Тестирование чекера"""
    checker = GIBDDChecker(headless=False)  # Для отладки показываем браузер
    
    try:
        await checker.initialize()
        
        # Тестовый VIN (замените на реальный)
        test_vin = "WVWZZZ1JZYW386752"
        
        # Выполняем проверки
        results = await checker.check_vehicle(
            test_vin, 
            [CheckType.REGISTRATION, CheckType.ACCIDENTS]
        )
        
        # Выводим результаты
        for result in results:
            print(f"\n{'='*50}")
            print(f"Тип проверки: {result.check_type.value}")
            print(f"Успех: {result.success}")
            if result.success:
                print(f"CAPTCHA решена: {result.captcha_solved}")
                print(f"Реклама пройдена: {result.ad_waited}")
                print(f"Данные: {result.data}")
            else:
                print(f"Ошибка: {result.error}")
                
    finally:
        await checker.close()

if __name__ == "__main__":
    asyncio.run(main()) 
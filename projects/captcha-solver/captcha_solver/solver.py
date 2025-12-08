import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from PIL import Image
import os
import tempfile

# Внешние библиотеки OCR
try:
    import paddleocr
    PADDLE_AVAILABLE = True
except ImportError:
    PADDLE_AVAILABLE = False
    
try:
    import easyocr
    EASY_OCR_AVAILABLE = True
except ImportError:
    EASY_OCR_AVAILABLE = False

try:
    import ddddocr
    DDDDOCR_AVAILABLE = True
except ImportError:
    DDDDOCR_AVAILABLE = False

from .preprocessor import CaptchaPreprocessor
from .models import CaptchaModel

logger = logging.getLogger(__name__)

class CaptchaSolver:
    """
    Мощный решатель капчи, использующий множественные подходы:
    1. Собственная CNN+LSTM модель
    2. PaddleOCR
    3. EasyOCR  
    4. Классификация отдельных символов
    
    Комбинирует результаты для максимальной точности
    """
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        self.preprocessor = CaptchaPreprocessor()
        
        # Инициализация OCR движков
        self.easyocr_reader = None
        self.paddleocr_reader = None
        self.ddddocr_det = None
        self.ddddocr_ocr = None
        
        # Инициализация моделей
        self.captcha_model = None
        
        # Статистика
        self.stats = {
            'total_solved': 0,
            'success_rate': 0.0,
            'avg_confidence': 0.0,
            'method_performance': {}
        }
        
        self._init_ocr_engines()
        self._init_models()
        
    def _init_ocr_engines(self):
        """Инициализация OCR движков"""
        if EASY_OCR_AVAILABLE:
            try:
                # Более мягкие настройки для лучшего распознавания
                self.easyocr_reader = easyocr.Reader(
                    ['en'], 
                    gpu=False,
                    verbose=False,
                    download_enabled=True
                )
                logger.info("EasyOCR инициализирован")
            except Exception as e:
                logger.warning(f"Ошибка инициализации EasyOCR: {e}")
                
        if PADDLE_AVAILABLE:
            try:
                self.paddleocr_reader = paddleocr.PaddleOCR(
                    use_angle_cls=True, 
                    lang='en',
                    show_log=False
                )
                logger.info("PaddleOCR инициализирован")
            except Exception as e:
                logger.warning(f"Ошибка инициализации PaddleOCR: {e}")
                
        if DDDDOCR_AVAILABLE:
            try:
                # ddddocr специально для капч
                self.ddddocr_det = ddddocr.DdddOcr(det=True, show_ad=False)
                self.ddddocr_ocr = ddddocr.DdddOcr(show_ad=False)
                logger.info("DDDDOCR инициализирован")
            except Exception as e:
                logger.warning(f"Ошибка инициализации DDDDOCR: {e}")
    
    def _init_models(self):
        """Инициализация собственных моделей"""
        try:
            os.makedirs(self.models_dir, exist_ok=True)
            self.captcha_model = CaptchaModel()
            logger.info("Модели скомпилированы для обучения")
        except Exception as e:
            logger.warning(f"Ошибка инициализации моделей: {e}")
    
    def solve(self, image_path: str, save_debug: bool = True) -> Dict:
        """
        Решение капчи с использованием всех доступных методов
        
        Args:
            image_path: путь к изображению капчи
            save_debug: сохранять ли промежуточные изображения для отладки
            
        Returns:
            Словарь с результатами распознавания
        """
        logger.info(f"Начинаем решение капчи: {image_path}")
        
        results = {
            'success': False,
            'text': '',
            'confidence': 0.0,
            'methods': {},
            'processing_time': 0.0,
            'debug_info': {}
        }
        
        import time
        start_time = time.time()
        
        try:
            # 1. Создаем множественные варианты обработки
            if save_debug:
                debug_dir = "debug_images"
                os.makedirs(debug_dir, exist_ok=True)
            
            # 2. Пробуем лучшие готовые решения в порядке эффективности
            methods_results = {}
            
            # DDDDOCR - лучший для сложных капч
            if self.ddddocr_det and self.ddddocr_ocr:
                dddd_result = self._solve_with_ddddocr(image_path)
                methods_results['ddddocr'] = dddd_result
                logger.info(f"ddddocr: {dddd_result.get('text', '')}")
            
            # EasyOCR на оригинале
            if self.easyocr_reader:
                original_result = self._solve_with_easyocr_image(image_path)
                methods_results['easyocr_original'] = original_result
                logger.info(f"easyocr_original: {original_result.get('text', '')}")
            
            # Если нужно, пробуем варианты предобработки
            if not any(result.get('text') for result in methods_results.values()):
                preprocessing_variants = self.preprocessor.create_multiple_variants(image_path)
                
                # Пробуем EasyOCR на всех вариантах предобработки
                for variant_name, processed_image in preprocessing_variants:
                    if self.easyocr_reader and save_debug:
                        temp_path = f"{debug_dir}/variant_{variant_name}.png"
                        cv2.imwrite(temp_path, processed_image)
                        
                        variant_result = self._solve_with_easyocr_image(temp_path)
                        methods_results[f'easyocr_{variant_name}'] = variant_result
                        logger.info(f"easyocr_{variant_name}: {variant_result.get('text', '')}")
                
                # PaddleOCR на лучшем варианте
                if self.paddleocr_reader and len(preprocessing_variants) > 1:
                    best_variant = preprocessing_variants[1][1] 
                    methods_results['paddleocr'] = self._solve_with_paddleocr(best_variant)
            
            results['methods'] = methods_results
            
            # 3. Консенсус результатов
            consensus_result = self._get_consensus(methods_results)
            results.update(consensus_result)
            
            results['processing_time'] = time.time() - start_time
            
            # Обновляем статистику
            self._update_stats(results)
            
            # Конвертируем все в JSON-совместимые типы
            results = self._convert_to_json_compatible(results)
            
            logger.info(f"Решение завершено: {results['text']} (уверенность: {results['confidence']:.2f})")
            
        except Exception as e:
            logger.error(f"Ошибка при решении капчи: {e}")
            results['error'] = str(e)
            
        return results
    
    def _solve_with_ddddocr(self, image_path: str) -> Dict:
        """Решение с помощью DDDDOCR - лучшая библиотека для капч"""
        try:
            with open(image_path, 'rb') as f:
                img_bytes = f.read()
            
            # Сначала определяем области текста
            bboxes = self.ddddocr_det.detection(img_bytes)
            
            if bboxes:
                # Сортируем по позиции слева направо
                bboxes = sorted(bboxes, key=lambda x: x[0])
                
                # Загружаем изображение для вырезания областей
                img = cv2.imread(image_path)
                all_text = ""
                total_confidence = 0
                
                for bbox in bboxes:
                    x1, y1, x2, y2 = map(int, bbox)
                    
                    # Вырезаем область
                    roi = img[y1:y2, x1:x2]
                    
                    # Преобразуем в байты
                    _, buffer = cv2.imencode('.png', roi)
                    roi_bytes = buffer.tobytes()
                    
                    # Распознаем
                    text = self.ddddocr_ocr.classification(roi_bytes)
                    
                    # Фильтруем только цифры
                    clean_text = ''.join(c for c in text if c.isdigit())
                    if clean_text:
                        all_text += clean_text
                        total_confidence += 0.9  # Высокая уверенность для ddddocr
                
                if all_text:
                    avg_confidence = total_confidence / len(bboxes) if bboxes else 0
                    return {
                        'text': all_text,
                        'confidence': float(min(avg_confidence, 1.0)),
                        'raw_result': bboxes
                    }
            
            # Если детекция не сработала, пробуем напрямую
            result = self.ddddocr_ocr.classification(img_bytes)
            clean_text = ''.join(c for c in result if c.isdigit())
            
            return {
                'text': clean_text,
                'confidence': 0.8 if clean_text else 0.0,
                'raw_result': result
            }
            
        except Exception as e:
            logger.error(f"Ошибка DDDDOCR: {e}")
            return {'text': '', 'confidence': 0.0, 'error': str(e)}
    
    def _solve_with_easyocr_image(self, image_path: str) -> Dict:
        """Решение с помощью EasyOCR для файла изображения"""
        try:
            # Специальные настройки для капчи с цифрами
            result = self.easyocr_reader.readtext(
                image_path,
                detail=1,
                paragraph=False,
                width_ths=0.4,      # Более низкий порог для склеивания по ширине
                height_ths=0.4,     # Более низкий порог для склеивания по высоте  
                text_threshold=0.3, # Понижаем порог уверенности для текста
                low_text=0.2,       # Еще ниже для слабого текста
                link_threshold=0.2, # Низкий порог для связывания
                allowlist='0123456789', # Только цифры
                decoder='greedy'    # Жадный декодер для лучшей работы с цифрами
            )
            
            if result:
                # Собираем все найденные символы
                all_text = ''
                total_confidence = 0
                
                for detection in result:
                    bbox, text, confidence = detection
                    
                    # Фильтруем только цифры
                    clean_text = ''.join(c for c in text if c.isdigit())
                    if clean_text:
                        all_text += clean_text
                        total_confidence += confidence
                
                if all_text:
                    avg_confidence = total_confidence / len(result)
                    return {
                        'text': all_text,
                        'confidence': float(avg_confidence),
                        'raw_result': result
                    }
            
            return {'text': '', 'confidence': 0.0, 'raw_result': result if 'result' in locals() else []}
                
        except Exception as e:
            logger.error(f"Ошибка EasyOCR: {e}")
            return {'text': '', 'confidence': 0.0, 'error': str(e)}
    
    def _solve_with_paddleocr(self, image: np.ndarray) -> Dict:
        """Решение с помощью PaddleOCR"""
        try:
            result = self.paddleocr_reader.ocr(image, cls=True)
            
            if result and result[0]:
                # Обрабатываем результат PaddleOCR
                texts = []
                confidences = []
                
                for line in result[0]:
                    if len(line) >= 2:
                        text = line[1][0]
                        confidence = line[1][1]
                        texts.append(text)
                        confidences.append(confidence)
                
                if texts:
                    full_text = ''.join(texts)
                    avg_confidence = sum(confidences) / len(confidences)
                    
                    # Фильтруем только цифры и буквы
                    clean_text = ''.join(c for c in full_text if c.isalnum())
                    
                    return {
                        'text': clean_text,
                        'confidence': avg_confidence,
                        'raw_result': result
                    }
            
            return {'text': '', 'confidence': 0.0, 'raw_result': result}
            
        except Exception as e:
            logger.error(f"Ошибка PaddleOCR: {e}")
            return {'text': '', 'confidence': 0.0, 'error': str(e)}
    
    def _solve_with_custom_model(self, image: np.ndarray) -> Dict:
        """Решение с помощью собственной модели"""
        try:
            # Здесь будет логика для собственной модели
            # Пока возвращаем пустой результат
            return {'text': '', 'confidence': 0.0, 'note': 'Custom model not trained yet'}
        except Exception as e:
            logger.error(f"Ошибка custom model: {e}")
            return {'text': '', 'confidence': 0.0, 'error': str(e)}
    
    def _get_consensus(self, methods_results: Dict) -> Dict:
        """Получение консенсуса из результатов разных методов"""
        valid_results = []
        
        for method, result in methods_results.items():
            if result.get('text') and result.get('confidence', 0) > 0.1:
                valid_results.append((result['text'], result['confidence'], method))
        
        if not valid_results:
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'consensus_method': 'none'
            }
        
        # Сортируем по уверенности
        valid_results.sort(key=lambda x: x[1], reverse=True)
        
        # Берем лучший результат
        best_text, best_confidence, best_method = valid_results[0]
        
        # Проверяем согласованность (если есть несколько результатов)
        if len(valid_results) > 1:
            # Ищем наиболее частый результат
            text_counts = {}
            for text, conf, method in valid_results:
                if text in text_counts:
                    text_counts[text] += conf
                else:
                    text_counts[text] = conf
            
            # Берем результат с наибольшей суммарной уверенностью
            consensus_text = max(text_counts.keys(), key=lambda k: text_counts[k])
            consensus_confidence = text_counts[consensus_text] / len([r for r in valid_results if r[0] == consensus_text])
            
            return {
                'success': True,
                'text': consensus_text,
                'confidence': float(min(consensus_confidence, 1.0)),
                'consensus_method': 'weighted_voting'
            }
        else:
            return {
                'success': True,
                'text': best_text,
                'confidence': float(best_confidence),
                'consensus_method': best_method
            }
    
    def _update_stats(self, result: Dict):
        """Обновление статистики"""
        self.stats['total_solved'] += 1
        
        if result['success']:
            confidence = float(result['confidence'])  # Конвертируем в float
            self.stats['avg_confidence'] = (
                (self.stats['avg_confidence'] * (self.stats['total_solved'] - 1) + confidence) 
                / self.stats['total_solved']
            )
        
        # Обновляем статистику успешности  
        self.stats['success_rate'] = float(result['confidence']) if result['success'] else 0.0
    
    def _convert_to_json_compatible(self, obj):
        """Конвертирует объект в JSON-совместимый формат"""
        if isinstance(obj, dict):
            return {key: self._convert_to_json_compatible(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_json_compatible(item) for item in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    def get_stats(self) -> Dict:
        """Получение статистики работы"""
        return self._convert_to_json_compatible(self.stats.copy())
    
    def train_custom_model(self, training_data_dir: str, epochs: int = 50):
        """Обучение собственной модели на данных"""
        # Реализация обучения будет добавлена позже
        pass

    def _solve_parallel(self, original_path: str, processed_path: str, 
                       processed_image: np.ndarray) -> Dict[str, str]:
        """Параллельное выполнение всех методов распознавания"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Запускаем все методы
            futures = {}
            
            # Собственная CNN+LSTM модель
            if self.captcha_model:
                futures['cnn_lstm'] = executor.submit(
                    self._solve_cnn_lstm, processed_image
                )
                
            # PaddleOCR
            if self.paddleocr_reader:
                futures['paddle_ocr'] = executor.submit(
                    self._solve_paddle_ocr, processed_path
                )
                
            # EasyOCR
            if self.easyocr_reader:
                futures['easy_ocr'] = executor.submit(
                    self._solve_easy_ocr, processed_path
                )
                
            # Классификация символов
            if self.char_classifier:
                futures['character_classification'] = executor.submit(
                    self._solve_character_classification, processed_image
                )
                
            # Собираем результаты
            for method, future in futures.items():
                try:
                    result = future.result(timeout=30)  # 30 секунд таймаут
                    results[method] = result
                    logger.info(f"{method}: {result}")
                except Exception as e:
                    logger.error(f"Ошибка в методе {method}: {e}")
                    results[method] = ""
                    
        return results
        
    def _solve_cnn_lstm(self, image: np.ndarray) -> str:
        """Решение с помощью CNN+LSTM модели"""
        try:
            result = self.captcha_model.predict_sequence(image)
            return self._clean_result(result)
        except Exception as e:
            logger.error(f"Ошибка CNN+LSTM: {e}")
            return ""
            
    def _solve_paddle_ocr(self, image_path: str) -> str:
        """Решение с помощью PaddleOCR"""
        try:
            result = self.paddleocr_reader.ocr(image_path, cls=True)
            if result and result[0]:
                text = ''.join([item[1][0] for item in result[0]])
                return self._clean_result(text)
            return ""
        except Exception as e:
            logger.error(f"Ошибка PaddleOCR: {e}")
            return ""
            
    def _solve_easy_ocr(self, image_path: str) -> str:
        """Решение с помощью EasyOCR"""
        try:
            result = self.easyocr_reader.readtext(image_path, detail=0)
            if result:
                text = ''.join(result)
                return self._clean_result(text)
            return ""
        except Exception as e:
            logger.error(f"Ошибка EasyOCR: {e}")
            return ""
            
    def _solve_character_classification(self, image: np.ndarray) -> str:
        """Решение через классификацию отдельных символов"""
        try:
            characters = self.preprocessor.extract_characters(image)
            if characters:
                result = self.char_classifier.predict(characters)
                return self._clean_result(result)
            return ""
        except Exception as e:
            logger.error(f"Ошибка классификации символов: {e}")
            return ""
            
    def _clean_result(self, text: str) -> str:
        """Очистка результата - оставляем только цифры"""
        if not text:
            return ""
        # Оставляем только цифры
        cleaned = ''.join(c for c in text if c.isdigit())
        return cleaned
        
    def _get_consensus_result(self, results: Dict[str, str]) -> str:
        """Определение результата на основе консенсуса"""
        valid_results = [r for r in results.values() if r and len(r) >= 3]
        
        if not valid_results:
            return ""
            
        # Если только один результат
        if len(valid_results) == 1:
            return valid_results[0]
            
        # Подсчет голосов
        vote_count = {}
        for result in valid_results:
            vote_count[result] = vote_count.get(result, 0) + 1
            
        # Результат с максимальным количеством голосов
        best_result = max(vote_count.items(), key=lambda x: x[1])
        
        # Если есть явный победитель (больше половины голосов)
        if best_result[1] > len(valid_results) / 2:
            return best_result[0]
            
        # Если нет консенсуса, используем приоритеты
        return self._get_best_result(results)
        
    def _get_best_result(self, results: Dict[str, str]) -> str:
        """Выбор лучшего результата по приоритету"""
        # Приоритет методов (от высшего к низшему)
        priority = ['cnn_lstm', 'character_classification', 'paddle_ocr', 'easy_ocr']
        
        for method in priority:
            if method in results and results[method] and len(results[method]) >= 3:
                return results[method]
                
        # Если ничего не найдено, возвращаем любой непустой результат
        for result in results.values():
            if result:
                return result
                
        return ""
        
    def _update_stats(self, results: Dict[str, str], final_result: str):
        """Обновление статистики"""
        self.stats['total_solved'] += 1
        
        if final_result:
            for method, result in results.items():
                if result == final_result:
                    self.stats[f"{method}_success"] += 1
                    
        # Если результат получен консенсусом
        if len([r for r in results.values() if r == final_result]) > 1:
            self.stats['consensus_success'] += 1
            
    def get_stats(self) -> Dict:
        """Получение статистики работы"""
        if self.stats['total_solved'] == 0:
            return self.stats
            
        stats_with_percentage = self.stats.copy()
        total = self.stats['total_solved']
        
        for key in stats_with_percentage:
            if key != 'total_solved':
                percentage = (stats_with_percentage[key] / total) * 100
                stats_with_percentage[f"{key}_percentage"] = round(percentage, 2)
                
        return stats_with_percentage
        
    def train_custom_model(self, dataset_path: Optional[str] = None, 
                          epochs: int = 50, use_synthetic: bool = True):
        """Обучение собственной модели"""
        logger.info("Начинаем обучение собственной модели")
        
        if use_synthetic:
            # Генерируем синтетические данные
            X_train, y_train = self.captcha_model.generate_synthetic_data(5000)
            
            # Конвертируем метки для CTC
            y_train_encoded = []
            for label in y_train:
                encoded = [self.captcha_model.char_to_num[c] for c in label]
                y_train_encoded.append(encoded)
                
            # Дополняем до максимальной длины
            max_len = max(len(seq) for seq in y_train_encoded)
            y_train_padded = []
            for seq in y_train_encoded:
                padded = seq + [len(self.captcha_model.characters)] * (max_len - len(seq))
                y_train_padded.append(padded)
                
            y_train_array = np.array(y_train_padded)
            
            # Подготавливаем изображения
            X_train_normalized = X_train.astype(np.float32) / 255.0
            X_train_normalized = np.expand_dims(X_train_normalized, axis=-1)
            
            # Обучение
            self.captcha_model.model.fit(
                X_train_normalized, y_train_array,
                batch_size=32,
                epochs=epochs,
                validation_split=0.2,
                verbose=1
            )
            
            logger.info("Обучение завершено")
            
        # Сохраняем модель
        if self.models_dir:
            self.captcha_model.save_models(self.models_dir)
            
    def benchmark(self, test_images: List[str], expected_results: List[str]) -> Dict:
        """Бенчмарк точности на тестовых данных"""
        correct = 0
        total = len(test_images)
        method_accuracy = {}
        
        for img_path, expected in zip(test_images, expected_results):
            result = self.solve(img_path, show_steps=False)
            
            if result['final_result'] == expected:
                correct += 1
                
            # Точность по методам
            for method, pred in result['all_results'].items():
                if method not in method_accuracy:
                    method_accuracy[method] = {'correct': 0, 'total': 0}
                method_accuracy[method]['total'] += 1
                if pred == expected:
                    method_accuracy[method]['correct'] += 1
                    
        overall_accuracy = (correct / total) * 100
        
        # Вычисляем точность по методам
        for method in method_accuracy:
            acc = method_accuracy[method]
            acc['accuracy'] = (acc['correct'] / acc['total']) * 100
            
        return {
            'overall_accuracy': overall_accuracy,
            'correct': correct,
            'total': total,
            'method_accuracy': method_accuracy
        } 
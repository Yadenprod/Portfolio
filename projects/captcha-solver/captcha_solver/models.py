try:
    import tensorflow as tf
    from tensorflow.keras import layers, Model
    TF_AVAILABLE = True
except ImportError:
    print("⚠️  TensorFlow не найден, CNN+LSTM модель будет недоступна")
    TF_AVAILABLE = False
    tf = None
    layers = None
    Model = None

import numpy as np
import cv2
from typing import List, Tuple, Optional
import pickle
import os
import logging

logger = logging.getLogger(__name__)

class CaptchaModel:
    """
    Мощная модель для распознавания капчи
    Использует CNN+LSTM архитектуру для последовательного распознавания символов
    """
    
    def __init__(self, img_width: int = 150, img_height: int = 50, 
                 max_length: int = 5, characters: str = "0123456789"):
        self.img_width = img_width
        self.img_height = img_height
        self.max_length = max_length
        self.characters = characters
        self.char_to_num = {char: idx for idx, char in enumerate(characters)}
        self.num_to_char = {idx: char for idx, char in enumerate(characters)}
        
        self.model = None
        self.character_model = None
        
    def create_cnn_lstm_model(self):
        """Создание CNN+LSTM модели для распознавания последовательности"""
        
        if not TF_AVAILABLE:
            logger.warning("TensorFlow недоступен, CNN+LSTM модель не может быть создана")
            return None
        
        # Входной слой
        input_img = layers.Input(shape=(self.img_width, self.img_height, 1), name='image')
        
        # CNN блоки для извлечения признаков
        x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        
        x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        
        x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        
        x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        
        # Подготовка для RNN
        new_shape = ((self.img_width // 16), (self.img_height // 16) * 256)
        x = layers.Reshape(target_shape=new_shape, name='reshape')(x)
        x = layers.Dense(128, activation='relu', name='dense1')(x)
        x = layers.Dropout(0.25)(x)
        
        # RNN слои для последовательного распознавания
        x = layers.Bidirectional(layers.LSTM(256, return_sequences=True, dropout=0.25))(x)
        x = layers.Bidirectional(layers.LSTM(128, return_sequences=True, dropout=0.25))(x)
        
        # Выходной слой
        x = layers.Dense(len(self.characters) + 1, activation='softmax', name='dense2')(x)
        
        # Создаем модель
        model = Model(inputs=input_img, outputs=x, name='captcha_cnn_lstm')
        
        return model
        
    def create_character_classifier(self):
        """Создание классификатора отдельных символов"""
        
        if not TF_AVAILABLE:
            logger.warning("TensorFlow недоступен, классификатор символов не может быть создан")
            return None
        
        input_img = layers.Input(shape=(32, 32, 1), name='character')
        
        # CNN для классификации символов
        x = layers.Conv2D(32, (3, 3), activation='relu')(input_img)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Conv2D(64, (3, 3), activation='relu')(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Conv2D(128, (3, 3), activation='relu')(x)
        
        # Глобальный пулинг
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(len(self.characters), activation='softmax')(x)
        
        model = Model(inputs=input_img, outputs=x, name='character_classifier')
        
        return model
        
    def compile_models(self):
        """Компиляция моделей"""
        if not TF_AVAILABLE:
            logger.warning("TensorFlow недоступен, модели не могут быть скомпилированы")
            return
            
        if self.model is None:
            self.model = self.create_cnn_lstm_model()
            
        if self.character_model is None:
            self.character_model = self.create_character_classifier()
        
        if self.model is not None:
            # Компиляция основной модели
            self.model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                loss=self.ctc_loss_func,
                metrics=['accuracy']
            )
        
        if self.character_model is not None:
            # Компиляция модели символов
            self.character_model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )
        
        logger.info("Модели скомпилированы успешно")
        
    def ctc_loss_func(self, y_true, y_pred):
        """CTC Loss функция для обучения последовательностей"""
        if not TF_AVAILABLE:
            return None
            
        batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
        input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
        label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")

        input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
        label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")

        loss = tf.keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)
        return loss
        
    def decode_predictions(self, pred):
        """Декодирование предсказаний CTC"""
        if not TF_AVAILABLE:
            return [""]
            
        input_len = np.ones(pred.shape[0]) * pred.shape[1]
        
        # Используем жадный декодер
        results = tf.keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0]
        
        # Конвертируем в текст
        output_text = []
        for res in results:
            text = ''.join([self.num_to_char.get(int(num), '') for num in res if int(num) < len(self.characters)])
            output_text.append(text)
            
        return output_text
        
    def predict_sequence(self, image: np.ndarray) -> str:
        """Предсказание всей последовательности символов"""
        if not TF_AVAILABLE or self.model is None:
            logger.warning("CNN+LSTM модель недоступна")
            return ""
            
        # Подготовка изображения
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
        # Изменение размера
        image = cv2.resize(image, (self.img_width, self.img_height))
        
        # Нормализация
        image = image.astype(np.float32) / 255.0
        image = np.expand_dims(image, axis=-1)
        image = np.expand_dims(image, axis=0)
        
        # Предсказание
        prediction = self.model.predict(image, verbose=0)
        
        # Декодирование
        decoded = self.decode_predictions(prediction)
        
        return decoded[0] if decoded else ""
        
    def predict_characters(self, characters: List[np.ndarray]) -> str:
        """Предсказание отдельных символов"""
        if not TF_AVAILABLE or self.character_model is None:
            logger.warning("Модель классификации символов недоступна")
            return ""
            
        if not characters:
            return ""
            
        result = ""
        for char_img in characters:
            # Нормализация
            if len(char_img.shape) == 3:
                char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)
                
            char_img = char_img.astype(np.float32) / 255.0
            char_img = np.expand_dims(char_img, axis=-1)
            char_img = np.expand_dims(char_img, axis=0)
            
            # Предсказание
            prediction = self.character_model.predict(char_img, verbose=0)
            predicted_class = np.argmax(prediction[0])
            
            if predicted_class < len(self.characters):
                result += self.characters[predicted_class]
                
        return result
        
    def save_models(self, base_path: str):
        """Сохранение обученных моделей"""
        if self.model is not None:
            self.model.save(f"{base_path}_sequence.h5")
            logger.info(f"Модель последовательности сохранена: {base_path}_sequence.h5")
            
        if self.character_model is not None:
            self.character_model.save(f"{base_path}_character.h5")
            logger.info(f"Модель символов сохранена: {base_path}_character.h5")
            
        # Сохранение параметров
        params = {
            'img_width': self.img_width,
            'img_height': self.img_height,
            'max_length': self.max_length,
            'characters': self.characters,
            'char_to_num': self.char_to_num,
            'num_to_char': self.num_to_char
        }
        
        with open(f"{base_path}_params.pkl", 'wb') as f:
            pickle.dump(params, f)
            
        logger.info(f"Параметры сохранены: {base_path}_params.pkl")
        
    def load_models(self, base_path: str):
        """Загрузка обученных моделей"""
        if not TF_AVAILABLE:
            logger.warning("TensorFlow недоступен, модели не могут быть загружены")
            return False
            
        try:
            # Загрузка параметров
            with open(f"{base_path}_params.pkl", 'rb') as f:
                params = pickle.load(f)
                
            self.img_width = params['img_width']
            self.img_height = params['img_height']
            self.max_length = params['max_length']
            self.characters = params['characters']
            self.char_to_num = params['char_to_num']
            self.num_to_char = params['num_to_char']
            
            # Загрузка моделей
            if os.path.exists(f"{base_path}_sequence.h5"):
                self.model = tf.keras.models.load_model(
                    f"{base_path}_sequence.h5", 
                    custom_objects={'ctc_loss_func': self.ctc_loss_func}
                )
                logger.info("Модель последовательности загружена")
                
            if os.path.exists(f"{base_path}_character.h5"):
                self.character_model = tf.keras.models.load_model(f"{base_path}_character.h5")
                logger.info("Модель символов загружена")
                
            return True
            
        except Exception as e:
            logger.error(f"Ошибка загрузки моделей: {e}")
            return False
            
    def generate_synthetic_data(self, num_samples: int = 1000) -> Tuple[np.ndarray, List[str]]:
        """Генерация синтетических данных для обучения"""
        logger.info(f"Генерируем {num_samples} синтетических образцов")
        
        images = []
        labels = []
        
        for _ in range(num_samples):
            # Генерируем случайную строку из цифр
            length = np.random.randint(3, self.max_length + 1)
            text = ''.join(np.random.choice(list(self.characters), length))
            
            # Создаем изображение с текстом
            img = self._create_text_image(text)
            
            # Добавляем шум и искажения
            img = self._add_noise_and_distortions(img)
            
            images.append(img)
            labels.append(text)
            
        return np.array(images), labels
        
    def _create_text_image(self, text: str) -> np.ndarray:
        """Создание изображения с текстом"""
        # Создаем белое изображение
        img = np.ones((self.img_height, self.img_width), dtype=np.uint8) * 255
        
        # Параметры текста
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0
        thickness = 2
        
        # Размер текста
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        
        # Позиция для центрирования
        x = (self.img_width - text_width) // 2
        y = (self.img_height + text_height) // 2
        
        # Рисуем текст
        cv2.putText(img, text, (x, y), font, font_scale, 0, thickness)
        
        return img
        
    def _add_noise_and_distortions(self, img: np.ndarray) -> np.ndarray:
        """Добавление шума и искажений к изображению"""
        # Добавляем случайные линии
        num_lines = np.random.randint(5, 15)
        for _ in range(num_lines):
            x1, y1 = np.random.randint(0, img.shape[1]), np.random.randint(0, img.shape[0])
            x2, y2 = np.random.randint(0, img.shape[1]), np.random.randint(0, img.shape[0])
            color = np.random.randint(0, 256)
            cv2.line(img, (x1, y1), (x2, y2), color, 1)
            
        # Добавляем шум
        noise = np.random.normal(0, 25, img.shape).astype(np.uint8)
        img = cv2.add(img, noise)
        
        # Размытие
        if np.random.random() > 0.5:
            img = cv2.GaussianBlur(img, (3, 3), 0)
            
        # Морфологические операции
        if np.random.random() > 0.5:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
            img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
            
        return img 
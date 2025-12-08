"""
Пример конфигурационного файла
Скопируйте в config.py и настройте под себя
"""

# Настройки захвата экрана
SCREEN_CAPTURE = {
    'monitor': None,  # None = весь экран, или {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
    'fps': 1,  # Кадров в секунду для обработки
}

# Настройки обработки изображений
VISION = {
    'tesseract_path': r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    'min_confidence': 0.7,  # Минимальная уверенность в распознавании
}

# Настройки управления
CONTROLLER = {
    'key_delay': 0.1,  # Задержка между нажатиями клавиш
    'mouse_sensitivity': 1.0,  # Чувствительность мыши
}

# Настройки AI
AI = {
    'decision_threshold': 0.5,  # Порог для принятия решений
    'learning_rate': 0.01,  # Скорость обучения (если используется ML)
}

# Горячие клавиши
HOTKEYS = {
    'toggle': 'f9',  # Запуск/остановка
    'exit': 'f10',  # Выход
}


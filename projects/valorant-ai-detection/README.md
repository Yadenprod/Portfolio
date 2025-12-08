# 🎯 Valorant Object Detection - AI Triggerbot

<div align="center">

![Status](https://img.shields.io/badge/Status-Advanced%20Prototype-brightgreen)
![Tech Stack](https://img.shields.io/badge/Stack-Go%20%7C%20Python%20%7C%20YOLO-blue)
![ML](https://img.shields.io/badge/ML-YOLOv8%20%7C%20Object%20Detection-orange)
![Complexity](https://img.shields.io/badge/Complexity-⭐⭐⭐⭐⭐-red)

**AI triggerbot для Valorant с использованием YOLO для детекции врагов**

[Go Client](./VLProd/ai_triggerbot/go_client.go) | [Python Server](./VLProd/ai_triggerbot/py_server.py) | [Model](./model/)

</div>

---

## 📋 Описание проекта

Valorant Object Detection - это интеллектуальный triggerbot для игры Valorant, который использует YOLO (YOLOv8n) для детекции врагов на экране и автоматической эмуляции нажатий. Система построена на гибридной архитектуре Go + Python для максимальной производительности.

### 🎯 Основная концепция

Система работает в два этапа:
1. **Go клиент** - Захватывает область экрана и отправляет в Python сервер
2. **Python сервер** - Использует YOLO для детекции врагов и возвращает результат
3. **Go клиент** - Эмулирует нажатие кнопки при обнаружении врага

---

## 🏗️ Архитектура

### Основные компоненты

#### 1. **Go Client** (`VLProd/ai_triggerbot/go_client.go`)
- **Захват экрана:** `robotgo.CaptureScreen()` с областью 1280x960 в центре экрана
- **Обработка изображений:** Конвертация в PNG через `bytes.Buffer` и `png.Encode()`
- **HTTP коммуникация:** Multipart form-data отправка через `createMultipart()`
- **Низкоуровневая эмуляция:** CGO вызовы `pressEqualDown()`/`pressEqualUp()` для нажатия клавиши `=`
- **Защита от конфликтов:** Проверка физического нажатия мыши через `C.isMouseDown()` перед эмуляцией
- **Обработка ошибок:** Автоматическое отпускание кнопки при потере связи с сервером
- **Real-time loop:** Бесконечный цикл без задержек для максимальной скорости

#### 2. **Python Server** (`VLProd/ai_triggerbot/py_server.py`)
- **Flask API:** `/predict` endpoint с multipart file upload
- **YOLO модель:** Загрузка кастомной модели `best.pt` через Ultralytics
- **Детекция:** Проверка классов 0 и 1 (головы врагов) с confidence threshold 0.05
- **Центральная зона:** Проверка детекций в центре экрана (cx, cy) с tolerance 15 пикселей
- **Оптимизация:** Обработка только релевантных детекций для минимальной задержки

#### 3. **YOLO Model** (`model/`)
- YOLOv8n модель для детекции голов врагов
- Обучение на скриншотах игры
- Оптимизация для real-time обработки

---

## 🔑 Ключевые особенности

### 1. **YOLO Detection**
- YOLOv8n для детекции
- Детекция голов врагов
- Высокая точность
- Real-time обработка

### 2. **Hybrid Architecture**
- Go для производительности
- Python для ML
- HTTP/gRPC коммуникация
- Низкая задержка

### 3. **Real-time Processing**
- Захват экрана в реальном времени
- Быстрая обработка
- Минимальная задержка

### 4. **Customizable**
- Настройка области захвата
- Настройка задержек
- Настройка порога детекции

---

## 🚀 Технологический стек

### Core
- **Go 1.18+** - Клиент для захвата экрана
- **Python 3.8+** - ML сервер
- **YOLOv8** - Детекция объектов
- **Ultralytics** - YOLO библиотека

### Communication
- **HTTP/gRPC** - Коммуникация между Go и Python
- **Flask/FastAPI** - Python сервер

### Computer Vision
- **OpenCV** - Обработка изображений
- **NumPy** - Математические операции

---

## 📊 Возможности

- ✅ Детекция врагов с помощью YOLO
- ✅ Автоматическая эмуляция нажатий
- ✅ Real-time обработка
- ✅ Настраиваемые параметры
- ✅ Высокая точность детекции
- ✅ Низкая задержка

---

## 🔧 Установка и запуск

### Требования

- Go 1.18+
- Python 3.8+
- YOLOv8 модель
- Ultralytics, OpenCV, NumPy

### Установка

```bash
# Python зависимости
pip install ultralytics opencv-python numpy flask

# Go зависимости
go mod download
```

### Запуск

```bash
# 1. Запустите Python сервер
python VLProd/ai_triggerbot/py_server.py

# 2. Запустите Go клиент
go run VLProd/ai_triggerbot/go_client.go
```

---

## 📁 Структура проекта

```
VLProd/
├── VLProd/
│   └── ai_triggerbot/
│       ├── go_client.go         # Go клиент
│       └── py_server.py         # Python сервер
├── model/                        # YOLO модель
└── README.md                     # Документация
```

---

## 💡 Особенности реализации

1. **Hybrid Architecture:**
   - Go для производительности
   - Python для ML
   - Оптимальное разделение

2. **YOLO Detection:**
   - State-of-the-art детекция
   - Высокая точность
   - Real-time обработка

3. **Low Latency:**
   - Минимальная задержка
   - Оптимизированная обработка
   - Эффективная коммуникация

---

## 📝 Примечания

- Проект разработан с использованием **Cursor AI** и современных практик ML разработки
- Используется YOLOv8 для детекции
- Гибридная архитектура Go + Python
- Модель может быть обучена на собственных данных

---

**Разработчик:** Дмитрий  
**Дата:** Декабрь 2025  
**Статус:** Advanced Prototype


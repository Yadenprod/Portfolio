# 🎯 Sports Prediction Model - ML Betting System

<div align="center">

![Status](https://img.shields.io/badge/Status-Production--ready-brightgreen)
![Tech Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Scikit-learn%20%7C%20Streamlit-blue)
![ML](https://img.shields.io/badge/ML-Random%20Forest%20%7C%20Logistic%20Regression-orange)
![Complexity](https://img.shields.io/badge/Complexity-⭐⭐⭐⭐-orange)

**Персональная система спортивных ставок с машинным обучением и управлением банкроллом**

[Model](./prediction_model.py) | [Bankroll](./bankroll_manager.py) | [App](./app.py)

</div>

---

## 📋 Описание проекта

Sports Prediction Model - это комплексная система для анализа спортивных матчей и управления банкроллом с использованием машинного обучения. Система предсказывает исходы матчей, рассчитывает оптимальные размеры ставок и управляет банкроллом с помощью различных стратегий.

### 🎯 Основная концепция

Система включает:
1. **ML модель** - Предсказание исходов матчей (Random Forest)
2. **Bankroll Manager** - Управление банкроллом (5 стратегий)
3. **Data Collector** - Сбор данных о матчах
4. **Streamlit UI** - Веб-интерфейс с графиками
5. **Value Betting** - Поиск ценных ставок

---

## 🏗️ Архитектура

### Основные компоненты

#### 1. **SportsPredictionModel** (`prediction_model.py`)
- **Random Forest Classifier:** 100 деревьев (`n_estimators=100`), `random_state=42`
- **Feature Engineering:** 13 фичей:
  - `home_goals_scored`, `home_goals_conceded` - статистика домашней команды
  - `away_goals_scored`, `away_goals_conceded` - статистика гостевой команды
  - `home_goal_diff`, `away_goal_diff` - рассчитанная разница голов
  - `home_wins_last_5`, `away_wins_last_5` - форма команд (последние 5 матчей)
  - `h2h_home_wins`, `h2h_away_wins` - head-to-head статистика
  - `odds_home`, `odds_away` - коэффициенты букмекеров
  - `home_percentage` - рыночные данные (процент ставок)
- **Data Generation:** Симуляция 1000+ матчей с логичной генерацией исходов
- **Training:** Train/test split 80/20, accuracy метрика
- **Prediction:** `predict_proba()` для получения вероятностей всех исходов

#### 2. **BankrollManager** (`bankroll_manager.py`)
- **5 стратегий управления банкроллом:**
  - **FLAT:** Фиксированная ставка 2% от текущего банка, минимум 1000 руб
  - **MARTINGALE:** Удвоение после проигрыша, максимум 5 удвоений, лимит 20% от банка
  - **FIBONACCI:** Динамическая последовательность Фибоначчи, лимит 15% от банка
  - **KELLY:** Критерий Келли с формулой `f = (bp - q) / b`, где `b = odds - 1`, `p = confidence`, `q = 1 - p`
    - Консервативный подход: максимум 10%, минимум 1% от банка
    - Проверка выгодности ставки: `p > q/b`
  - **DALEMBERT:** +1 единица после проигрыша, лимит 10% от банка
- **Bet History:** Полная история ставок с timestamp, размерами, коэффициентами
- **Statistics:** ROI, win rate, profit/loss, consecutive losses tracking
- **Risk Management:** Автоматическая защита от превышения банка

#### 3. **Data Collector** (`data_collector.py`)
- Сбор данных о матчах
- Интеграция с API (Football Data, Odds API, HLTV)
- Парсинг данных
- Обработка статистики

#### 4. **Advanced Features:**
- `advanced_prediction_model.py` - Продвинутая модель
- `smart_bankroll_manager.py` - Умный банкролл менеджер
- `advanced_bet_analyzer.py` - Анализ ставок
- `hltv_parser.py` - Парсер HLTV для CS2
- `csgo_prediction_model.py` - Модель для CS2
- `fonbet_api.py` - Интеграция с Fonbet API

#### 5. **Streamlit UI** (`app.py`)
- Веб-интерфейс
- Графики и статистика
- Управление банкроллом
- Анализ матчей
- История ставок

---

## 🔑 Ключевые особенности

### 1. **Machine Learning**
- Random Forest для предсказаний
- 13 фичей для анализа
- Генерация тренировочных данных
- Обучение на исторических данных

### 2. **Bankroll Management**
- 5 стратегий управления
- Критерий Келли для оптимизации
- Защита от больших потерь
- Адаптивное управление

### 3. **Value Betting**
- Поиск ценных ставок
- Расчет Expected Value (EV)
- Учет уверенности модели
- Рекомендации на основе EV

### 4. **Data Integration**
- Football Data API
- Odds API
- HLTV для CS2
- Fonbet API

### 5. **Analytics**
- Статистика ставок
- ROI и win rate
- Графики производительности
- Анализ по стратегиям

---

## 🚀 Технологический стек

### Core
- **Python 3.8+** - Основной язык
- **Scikit-learn** - ML библиотека
- **Pandas** - Обработка данных
- **NumPy** - Математические операции

### UI
- **Streamlit** - Веб-интерфейс
- **Matplotlib** - Графики
- **Plotly** - Интерактивные графики

### Data
- **Requests** - HTTP запросы
- **BeautifulSoup** - Парсинг HTML
- **JSON** - Обработка данных

---

## 📊 Возможности

- ✅ Предсказание исходов матчей
- ✅ 5 стратегий управления банкроллом
- ✅ Value betting поиск
- ✅ Веб-интерфейс с графиками
- ✅ Интеграция с API
- ✅ Статистика и аналитика
- ✅ Поддержка футбола и CS2
- ✅ История ставок

---

## 🔧 Установка и запуск

### Требования

- Python 3.8+
- Scikit-learn, Pandas, NumPy
- Streamlit

### Установка

```bash
pip install -r requirements.txt
```

### Запуск

```bash
# Веб-интерфейс
streamlit run app.py

# Консольная версия
python main.py
```

---

## 📁 Структура проекта

```
ProjectFor/
├── prediction_model.py          # ML модель
├── bankroll_manager.py          # Управление банкроллом
├── data_collector.py            # Сбор данных
├── app.py                       # Streamlit UI
├── main.py                      # Основная логика
├── advanced_prediction_model.py # Продвинутая модель
├── smart_bankroll_manager.py    # Умный банкролл
├── hltv_parser.py               # Парсер HLTV
├── csgo_prediction_model.py     # Модель для CS2
└── requirements.txt             # Зависимости
```

---

## 💡 Особенности реализации

1. **ML Model:**
   - Random Forest с 100 деревьями
   - 13 фичей для анализа
   - Высокая точность предсказаний

2. **Bankroll Management:**
   - 5 различных стратегий
   - Критерий Келли для оптимизации
   - Защита от рисков

3. **Value Betting:**
   - Поиск положительного EV
   - Учет уверенности модели
   - Оптимизация прибыли

4. **Analytics:**
   - Детальная статистика
   - Графики производительности
   - Анализ эффективности

---

## 📝 Примечания

- Проект разработан с использованием **Cursor AI** и современных практик ML разработки
- Система предназначена для обучения и анализа
- Поддерживается обучение на собственных данных
- Интеграция с множественными API

---

**Разработчик:** Дмитрий  
**Дата:** Декабрь 2025  
**Статус:** Production-ready

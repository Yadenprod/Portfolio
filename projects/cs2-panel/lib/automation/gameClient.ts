import { IAccount } from '@/models/Account';
import { IGameplayAutomation } from '@/models/GameplayAutomation';
import { spawnSync, spawn, ChildProcess } from 'child_process';
import { EventEmitter } from 'events';
import { robotjs } from './robotjs';
import { logger } from '@/lib/logger';
import path from 'path';
import fs from 'fs';
import fetch from 'node-fetch';

// Константы для автоматизации
const CS2_WINDOW_TITLE = 'Counter-Strike 2';
const DEFAULT_STEAM_PATH = 'C:\\Program Files (x86)\\Steam\\steam.exe';
const DEATHMATCH_MENU_COORDINATES = { x: 800, y: 450 }; // Примерные координаты меню дезматча
const PLAY_BUTTON_COORDINATES = { x: 960, y: 540 }; // Примерные координаты кнопки играть
const API_BASE_URL = 'http://localhost:3000/api'; // URL API для отправки данных

// Интерфейс для игровых событий
export interface GameEvent {
  type: 'login' | 'gameStart' | 'gameEnd' | 'caseReceived' | 'error' | 'levelUp';
  message: string;
  accountId?: string;
  timestamp: Date;
  data?: any;
}

// Класс для управления клиентом CS2
export class GameClient extends EventEmitter {
  private account: IAccount;
  private settings: IGameplayAutomation;
  private gameProcess: ChildProcess | null = null;
  private isRunning: boolean = false;
  private lastActivityTime: Date = new Date();
  private steamPath: string;
  private xpGained: number = 0;
  private gameActivityInterval: NodeJS.Timeout | null = null;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;

  constructor(account: IAccount, settings: IGameplayAutomation, steamPath?: string) {
    super();
    this.account = account;
    this.settings = settings;
    this.steamPath = steamPath || DEFAULT_STEAM_PATH;
  }

  // Запуск клиента CS2
  async start(): Promise<boolean> {
    if (this.isRunning) {
      logger.warn(`Клиент для аккаунта ${this.account.username} уже запущен`);
      return false;
    }

    logger.info(`Запуск клиента для аккаунта ${this.account.username}`);

    try {
      // Запуск Steam с параметрами для автоматического входа
      this.gameProcess = spawn(this.steamPath, [
        '-login', 
        this.account.username,
        this.account.password,
        '-applaunch',
        '730', // ID приложения для CS2
        '-novid',
        '-nosound',
        '-low',
        '-windowed',
        '-w 1280',
        '-h 720'
      ]);

      this.isRunning = true;
      this.lastActivityTime = new Date();

      // Отправляем событие успешного входа
      this.emit('event', {
        type: 'login',
        message: `Успешный вход в аккаунт ${this.account.username}`,
        accountId: this.account._id.toString(),
        timestamp: new Date()
      } as GameEvent);

      // Ждем запуска игры
      await this.sleep(30000); // 30 секунд на запуск игры

      // Ищем окно CS2
      if (await this.findGameWindow()) {
        this.startGameActivity();
        return true;
      } else {
        logger.error(`Не удалось найти окно игры для аккаунта ${this.account.username}`);
        this.stop();
        return false;
      }
    } catch (error) {
      logger.error(`Ошибка запуска клиента для аккаунта ${this.account.username}:`, error);
      this.emit('event', {
        type: 'error',
        message: `Ошибка запуска клиента: ${error}`,
        accountId: this.account._id.toString(),
        timestamp: new Date(),
        data: { error }
      } as GameEvent);
      this.stop();
      return false;
    }
  }

  // Остановка клиента CS2
  async stop(): Promise<void> {
    if (!this.isRunning) return;

    logger.info(`Остановка клиента для аккаунта ${this.account.username}`);

    // Остановка автоматизации игрового процесса
    if (this.gameActivityInterval) {
      clearInterval(this.gameActivityInterval);
      this.gameActivityInterval = null;
    }

    // Корректное завершение процесса игры
    if (this.gameProcess) {
      try {
        // Сначала пробуем плавно закрыть игру через сочетание клавиш Alt+F4
        robotjs.keyTap('f4', 'alt');
        await this.sleep(5000);

        // Если процесс все еще работает, завершаем его жестко
        if (this.gameProcess.exitCode === null) {
          this.gameProcess.kill('SIGTERM');
          await this.sleep(3000);
          
          if (this.gameProcess.exitCode === null) {
            this.gameProcess.kill('SIGKILL');
          }
        }
      } catch (error) {
        logger.error(`Ошибка при остановке клиента для аккаунта ${this.account.username}:`, error);
      }
    }

    this.isRunning = false;
    this.gameProcess = null;
    this.reconnectAttempts = 0;
  }

  // Запуск автоматизации игрового процесса
  private startGameActivity(): void {
    logger.info(`Запуск автоматизации игрового процесса для аккаунта ${this.account.username}`);

    this.gameActivityInterval = setInterval(async () => {
      if (!this.isRunning) return;

      try {
        // Проверка, активно ли окно игры
        const isGameWindowActive = await this.findGameWindow();
        if (!isGameWindowActive) {
          logger.warn(`Окно игры не найдено для аккаунта ${this.account.username}`);
          
          if (this.settings.autoReconnect && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            logger.info(`Попытка переподключения (${this.reconnectAttempts}/${this.maxReconnectAttempts}) для аккаунта ${this.account.username}`);
            this.stop();
            await this.sleep(10000);
            this.start();
          } else if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            logger.error(`Превышено максимальное количество попыток переподключения для аккаунта ${this.account.username}`);
            this.stop();
            this.emit('event', {
              type: 'error',
              message: 'Превышено максимальное количество попыток переподключения',
              accountId: this.account._id.toString(),
              timestamp: new Date()
            } as GameEvent);
          }
          return;
        }

        // Сбрасываем счетчик попыток переподключения
        this.reconnectAttempts = 0;

        // Генерируем случайное игровое действие
        await this.performRandomGameAction();

        // Накапливаем опыт
        this.xpGained += Math.floor(Math.random() * 10) + 1;
        
        // Проверяем, нужно ли отправить данные на сервер (каждые ~5 минут)
        if (this.xpGained >= 100) {
          await this.reportExperienceGain();
        }

        this.lastActivityTime = new Date();
      } catch (error) {
        logger.error(`Ошибка в игровом процессе для аккаунта ${this.account.username}:`, error);
      }
    }, 30000); // Запускаем действия каждые 30 секунд
  }

  // Имитация случайного игрового действия в CS2
  private async performRandomGameAction(): Promise<void> {
    if (!this.isRunning) return;
    
    // Активируем окно игры
    await this.findGameWindow();
    
    // Выбираем случайное действие:
    // 1 - Движение
    // 2 - Стрельба
    // 3 - Перезарядка
    // 4 - Проверка статуса дезматча и подключение если нужно
    
    const actionType = Math.floor(Math.random() * 4) + 1;
    
    switch (actionType) {
      case 1: // Случайное движение
        // Нажимаем клавиши W, A, S, D случайное время
        const moveKeys = ['w', 'a', 's', 'd'];
        const randomKey = moveKeys[Math.floor(Math.random() * moveKeys.length)];
        
        robotjs.keyToggle(randomKey, 'down');
        await this.sleep(Math.random() * 1000 + 500);
        robotjs.keyToggle(randomKey, 'up');
        
        // Случайное движение мышью
        const moveX = Math.floor(Math.random() * 200) - 100;
        const moveY = Math.floor(Math.random() * 100) - 50;
        robotjs.moveMouseRelative(moveX, moveY);
        break;
        
      case 2: // Стрельба
        // Нажимаем левую кнопку мыши для стрельбы
        robotjs.mouseToggle('down', 'left');
        await this.sleep(Math.random() * 500 + 200);
        robotjs.mouseToggle('up', 'left');
        break;
        
      case 3: // Перезарядка
        // Нажимаем клавишу R для перезарядки
        robotjs.keyTap('r');
        break;
        
      case 4: // Проверка статуса дезматча
        // Если включена опция автоподключения к дезматчу, проверяем нужно ли подключиться
        if (this.settings.autoJoinDeathmatch) {
          await this.joinDeathmatch();
        }
        break;
    }
  }

  // Подключение к дезматчу
  private async joinDeathmatch(): Promise<void> {
    try {
      // Открываем главное меню (клавиша Esc)
      robotjs.keyTap('escape');
      await this.sleep(1000);
      
      // Кликаем на кнопку "Играть"
      robotjs.moveMouse(PLAY_BUTTON_COORDINATES.x, PLAY_BUTTON_COORDINATES.y);
      await this.sleep(500);
      robotjs.mouseClick();
      await this.sleep(1000);
      
      // Кликаем на опцию "Deathmatch"
      robotjs.moveMouse(DEATHMATCH_MENU_COORDINATES.x, DEATHMATCH_MENU_COORDINATES.y);
      await this.sleep(500);
      robotjs.mouseClick();
      await this.sleep(1000);
      
      // Выбираем карту, если настроена определенная карта
      if (this.settings.mapPreference !== 'any') {
        // Здесь нужны координаты для разных карт
        // В реальном приложении мы бы использовали распознавание изображений
        // Для примера берем случайные координаты
        const mapX = 800 + Math.floor(Math.random() * 100);
        const mapY = 400 + Math.floor(Math.random() * 100);
        
        robotjs.moveMouse(mapX, mapY);
        await this.sleep(500);
        robotjs.mouseClick();
        await this.sleep(1000);
      }
      
      // Кликаем "GO" для запуска поиска игры
      robotjs.moveMouse(960, 700); // Примерные координаты кнопки GO
      await this.sleep(500);
      robotjs.mouseClick();
      
      // Отправляем событие о присоединении к игре
      this.emit('event', {
        type: 'gameStart',
        message: `Присоединение к дезматчу (карта: ${this.settings.mapPreference})`,
        accountId: this.account._id.toString(),
        timestamp: new Date()
      } as GameEvent);
      
      logger.info(`Аккаунт ${this.account.username} присоединяется к дезматчу`);
    } catch (error) {
      logger.error(`Ошибка при присоединении к дезматчу для аккаунта ${this.account.username}:`, error);
    }
  }

  // Поиск и активация окна игры
  private async findGameWindow(): Promise<boolean> {
    try {
      // В реальном приложении здесь был бы код для поиска окна с помощью WinAPI
      // или другой библиотеки для работы с окнами. Для примера просто возвращаем true
      const windowFound = true;
      
      if (windowFound) {
        // Активируем окно
        return true;
      }
      return false;
    } catch (error) {
      logger.error(`Ошибка при поиске окна игры для аккаунта ${this.account.username}:`, error);
      return false;
    }
  }

  // Отправка данных о полученном опыте на сервер
  private async reportExperienceGain(): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/gameplay/simulate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          accountId: this.account._id.toString(),
          experienceGained: this.xpGained
        }),
      });

      const data = await response.json() as {
        success: boolean;
        message?: string;
        simulationResults?: {
          leveledUp: boolean;
          currentLevel: number;
          caseDropped: boolean;
        }
      };
      
      if (data.success) {
        logger.info(`Отправлены данные об опыте (${this.xpGained} XP) для аккаунта ${this.account.username}`);
        
        // Сбрасываем счетчик опыта
        this.xpGained = 0;
        
        // Если повысился уровень
        if (data.simulationResults?.leveledUp) {
          this.emit('event', {
            type: 'levelUp',
            message: `Повышение уровня до ${data.simulationResults.currentLevel}`,
            accountId: this.account._id.toString(),
            timestamp: new Date(),
            data: { level: data.simulationResults.currentLevel }
          } as GameEvent);
        }
        
        // Если выпал кейс
        if (data.simulationResults?.caseDropped) {
          this.emit('event', {
            type: 'caseReceived',
            message: 'Получен новый кейс',
            accountId: this.account._id.toString(),
            timestamp: new Date()
          } as GameEvent);
        }
      } else {
        logger.error(`Ошибка отправки данных об опыте для аккаунта ${this.account.username}:`, data.message);
      }
    } catch (error) {
      logger.error(`Ошибка отправки данных об опыте для аккаунта ${this.account.username}:`, error);
    }
  }

  // Вспомогательная функция для ожидания
  private async sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
} 
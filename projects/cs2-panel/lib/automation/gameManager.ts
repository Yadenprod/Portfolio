import { IAccount } from '@/models/Account';
import { IGameplayAutomation } from '@/models/GameplayAutomation';
import { GameClient, GameEvent } from './gameClient';
import { logger } from '@/lib/logger';

/**
 * Менеджер для управления всеми игровыми клиентами
 */
export class GameManager {
  private clients: Map<string, GameClient> = new Map();
  private eventListeners: ((event: GameEvent) => void)[] = [];
  private maxConcurrentClients: number;
  private steamPath?: string;

  /**
   * Конструктор GameManager
   * @param maxConcurrentClients - Максимальное количество одновременно запущенных клиентов
   * @param steamPath - Путь к исполняемому файлу Steam
   */
  constructor(maxConcurrentClients: number = 3, steamPath?: string) {
    this.maxConcurrentClients = maxConcurrentClients;
    this.steamPath = steamPath;
    logger.info(`GameManager инициализирован с ограничением ${maxConcurrentClients} одновременных клиентов`);
  }

  /**
   * Добавляет обработчик событий от игровых клиентов
   * @param listener - Функция-обработчик события
   */
  onEvent(listener: (event: GameEvent) => void): void {
    this.eventListeners.push(listener);
  }

  /**
   * Внутренний метод для вызова всех обработчиков событий
   * @param event - Игровое событие
   */
  private emitEvent(event: GameEvent): void {
    for (const listener of this.eventListeners) {
      try {
        listener(event);
      } catch (error) {
        logger.error('Ошибка в обработчике события:', error);
      }
    }
  }

  /**
   * Запускает клиент для указанного аккаунта с настройками
   * @param account - Аккаунт для запуска
   * @param settings - Настройки автоматизации
   * @returns true, если запуск успешен
   */
  async startClient(account: IAccount, settings: IGameplayAutomation): Promise<boolean> {
    const accountId = account._id.toString();
    
    // Проверяем, не запущен ли уже клиент для этого аккаунта
    if (this.clients.has(accountId)) {
      logger.warn(`Клиент для аккаунта ${account.username} уже запущен`);
      return false;
    }
    
    // Проверяем ограничение на количество клиентов
    if (this.clients.size >= this.maxConcurrentClients) {
      logger.warn(`Достигнуто максимальное количество одновременных клиентов: ${this.maxConcurrentClients}`);
      return false;
    }
    
    // Создаем и запускаем клиент
    const client = new GameClient(account, settings, this.steamPath);
    
    // Подписываемся на события от клиента
    client.on('event', (event: GameEvent) => {
      logger.debug(`Получено событие от клиента ${account.username}:`, event);
      this.emitEvent(event);
    });
    
    // Запускаем клиент
    const success = await client.start();
    
    if (success) {
      this.clients.set(accountId, client);
      logger.info(`Клиент для аккаунта ${account.username} успешно запущен`);
    } else {
      logger.error(`Не удалось запустить клиент для аккаунта ${account.username}`);
    }
    
    return success;
  }

  /**
   * Останавливает клиент для указанного аккаунта
   * @param accountId - ID аккаунта
   * @returns true, если остановка успешна
   */
  async stopClient(accountId: string): Promise<boolean> {
    const client = this.clients.get(accountId);
    
    if (!client) {
      logger.warn(`Клиент для аккаунта с ID ${accountId} не найден`);
      return false;
    }
    
    try {
      await client.stop();
      this.clients.delete(accountId);
      logger.info(`Клиент для аккаунта с ID ${accountId} успешно остановлен`);
      return true;
    } catch (error) {
      logger.error(`Ошибка при остановке клиента для аккаунта с ID ${accountId}:`, error);
      return false;
    }
  }

  /**
   * Останавливает все запущенные клиенты
   */
  async stopAllClients(): Promise<void> {
    const clientIds = Array.from(this.clients.keys());
    
    logger.info(`Останавливаем все ${clientIds.length} клиентов...`);
    
    for (const id of clientIds) {
      await this.stopClient(id);
    }
    
    logger.info('Все клиенты остановлены');
  }

  /**
   * Получает список всех запущенных клиентов
   * @returns Массив ID аккаунтов с запущенными клиентами
   */
  getActiveClientIds(): string[] {
    return Array.from(this.clients.keys());
  }

  /**
   * Проверяет, запущен ли клиент для указанного аккаунта
   * @param accountId - ID аккаунта
   * @returns true, если клиент запущен
   */
  isClientActive(accountId: string): boolean {
    return this.clients.has(accountId);
  }

  /**
   * Получает количество запущенных клиентов
   * @returns Количество активных клиентов
   */
  getActiveClientCount(): number {
    return this.clients.size;
  }

  /**
   * Устанавливает максимальное количество одновременных клиентов
   * @param count - Максимальное количество клиентов
   */
  setMaxConcurrentClients(count: number): void {
    this.maxConcurrentClients = count;
    logger.info(`Установлено новое ограничение на количество клиентов: ${count}`);
  }

  /**
   * Устанавливает путь к исполняемому файлу Steam
   * @param path - Путь к Steam.exe
   */
  setSteamPath(path: string): void {
    this.steamPath = path;
    logger.info(`Установлен новый путь к Steam: ${path}`);
  }
} 
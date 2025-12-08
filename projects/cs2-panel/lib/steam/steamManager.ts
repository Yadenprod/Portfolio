import { SteamAPI, SteamLoginOptions, SteamUserStatus } from './steamAPI';
import { IAccount } from '@/models/Account';
import { logger } from '@/lib/logger';

export interface LoginOptions {
  twoFactorCode?: string;
  waitForMobileConfirmation?: boolean;
}

/**
 * Менеджер для управления несколькими Steam клиентами
 */
export class SteamManager {
  private clients: Map<string, SteamAPI> = new Map();
  private maxConcurrentClients: number;
  private timers: Map<string, NodeJS.Timeout> = new Map();
  private loginAttempts: Map<string, number> = new Map();
  private rateLimit: Map<string, number> = new Map();
  private mobilePendingAccounts: Map<string, boolean> = new Map();

  /**
   * Конструктор
   * @param maxConcurrentClients Максимальное количество одновременных подключений
   */
  constructor(maxConcurrentClients = 3) {
    this.maxConcurrentClients = maxConcurrentClients;
    logger.info(`SteamManager инициализирован с ограничением ${maxConcurrentClients} одновременных клиентов`);
  }

  /**
   * Создание и вход в Steam клиент для указанного аккаунта
   * @param account Аккаунт для входа
   * @param options Дополнительные параметры входа
   */
  async loginAccount(account: IAccount, options?: LoginOptions): Promise<SteamUserStatus> {
    const accountId = account._id.toString();

    // Проверяем, не превышено ли максимальное количество клиентов
    if (this.clients.size >= this.maxConcurrentClients) {
      const error = `Достигнуто максимальное количество одновременных клиентов (${this.maxConcurrentClients})`;
      logger.warn(error);
      throw new Error(error);
    }

    // Проверяем, не находится ли аккаунт в Rate Limit
    const rateLimitTime = this.rateLimit.get(accountId);
    if (rateLimitTime && Date.now() < rateLimitTime) {
      const remainingTime = Math.round((rateLimitTime - Date.now()) / 1000 / 60);
      const error = `Аккаунт ${account.username} в режиме ограничения от Steam. Подождите еще ${remainingTime} минут, используйте мобильное подтверждение или нажмите "Сбросить ограничение"`;
      logger.warn(error);
      throw new Error(error);
    }

    // Проверяем, не запущен ли уже клиент для этого аккаунта
    if (this.clients.has(accountId)) {
      const client = this.clients.get(accountId)!;
      
      // Проверяем, не выполняется ли уже вход
      if (client.isLogonInProgress()) {
        logger.warn(`Вход в аккаунт ${account.username} уже выполняется`);
        throw new Error('Вход уже выполняется, дождитесь завершения');
      }
      
      // Проверяем, не ожидается ли мобильное подтверждение
      if (client.isWaitingForMobileConfirmation()) {
        logger.info(`Аккаунт ${account.username} ожидает мобильного подтверждения`);
        return {
          isLoggedIn: false,
          requiresMobileConfirmation: true,
          error: 'Ожидается подтверждение через мобильное приложение'
        };
      }
      
      const status = client.getStatus();
      
      // Если уже авторизован, просто возвращаем статус
      if (status.isLoggedIn) {
        logger.info(`Клиент для аккаунта ${account.username} уже авторизован, возвращаем текущий статус`);
        return status;
      }
      
      // Если не авторизован, удаляем клиент и создаем новый
      logger.info(`Клиент для аккаунта ${account.username} существует, но не авторизован. Создаем новый`);
      this.clients.delete(accountId);
      
      // Добавляем небольшую задержку перед созданием нового клиента
      await new Promise(resolve => setTimeout(resolve, 2000));
    }

    // Увеличиваем счетчик попыток входа
    const attempts = (this.loginAttempts.get(accountId) || 0) + 1;
    this.loginAttempts.set(accountId, attempts);
    
    // Если не используется мобильное подтверждение и было много попыток, добавляем задержку
    if (!options?.waitForMobileConfirmation && attempts > 3) {
      // Если было больше 3 попыток, добавляем задержку между попытками
      const delay = Math.min(attempts * 5000, 30000); // Максимальная задержка 30 секунд
      logger.info(`Слишком много попыток входа для аккаунта ${account.username}. Добавляем задержку ${delay/1000} секунд`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }

    // Создаем новый клиент
    const steamClient = new SteamAPI();
    this.clients.set(accountId, steamClient);

    // Регистрируем обработчик события мобильного подтверждения
    if (options?.waitForMobileConfirmation) {
      this.mobilePendingAccounts.set(accountId, true);
      steamClient.on('mobileConfirmationRequired', (data) => {
        logger.info(`Требуется мобильное подтверждение для аккаунта ${data.username}`);
      });
    }

    try {
      // Настраиваем параметры входа
      const loginOptions: SteamLoginOptions = {
        username: account.username,
        password: account.password,
        waitForMobileConfirmation: options?.waitForMobileConfirmation
      };

      // Добавляем код Steam Guard, если доступен
      if (account.sharedSecret) {
        loginOptions.sharedSecret = account.sharedSecret;
      } else if (options?.twoFactorCode) {
        loginOptions.twoFactorCode = options.twoFactorCode;
        logger.info(`Используем предоставленный код Steam Guard: ${options.twoFactorCode}`);
      } else if (account.steamGuardCode) {
        loginOptions.twoFactorCode = account.steamGuardCode;
        logger.info(`Используем код Steam Guard из базы данных: ${account.steamGuardCode}`);
      }

      // Настраиваем обработчик для запроса Steam Guard
      let steamGuardHandled = false;
      
      steamClient.on('steamGuard', async (params) => {
        logger.warn(`Запрошен Steam Guard для аккаунта ${account.username}`);
        
        if (steamGuardHandled) {
          logger.warn(`Повторный запрос Steam Guard для ${account.username}, игнорируем`);
          return;
        }
        
        steamGuardHandled = true;
        
        // Если есть код в параметрах запроса или в аккаунте, используем его
        if (options?.twoFactorCode) {
          logger.info(`Отправляем код Steam Guard из параметров: ${options.twoFactorCode}`);
          params.callback(options.twoFactorCode);
        } else if (account.steamGuardCode) {
          logger.info(`Отправляем код Steam Guard из базы данных: ${account.steamGuardCode}`);
          params.callback(account.steamGuardCode);
        } else {
          logger.warn(`Нет доступного кода Steam Guard для аккаунта ${account.username}`);
          
          // Если используем мобильное подтверждение, ничего не делаем
          // обработчик выше уже настроен для этого случая
          if (!options?.waitForMobileConfirmation) {
            params.callback(''); // Отправляем пустой код, чтобы прервать процесс
          }
        }
      });
      
      // Обработчик ошибок
      steamClient.on('error', (err) => {
        logger.error(`Ошибка Steam клиента для аккаунта ${account.username}: ${err.message}`);
        if (options?.waitForMobileConfirmation) {
          this.mobilePendingAccounts.delete(accountId);
        }
      });

      // Выполняем вход
      const status = await steamClient.login(loginOptions);
      logger.info(`Успешный вход в Steam для аккаунта ${account.username}, статус: ${JSON.stringify(status)}`);
      
      // Сбрасываем счетчик попыток входа при успешном входе
      this.loginAttempts.set(accountId, 0);
      this.mobilePendingAccounts.delete(accountId);
      
      // Обновляем время последнего входа в базе данных
      try {
        const Account = (await import('@/models/Account')).default;
        const dbConnect = (await import('@/lib/dbConnect')).default;
        
        await dbConnect();
        await Account.findByIdAndUpdate(accountId, { 
          lastLogin: new Date(),
          steamGuardCode: '' // Очищаем код Steam Guard после успешного входа
        });
        logger.info(`Обновлено время последнего входа для аккаунта ${account.username}`);
      } catch (dbError: any) {
        logger.error(`Ошибка при обновлении времени последнего входа: ${dbError.message}`);
      }

      return status;
    } catch (error: any) {
      // Удаляем клиент в случае ошибки, кроме случая ожидания мобильного подтверждения
      if (!options?.waitForMobileConfirmation || !error.message.includes('ожидания')) {
        this.clients.delete(accountId);
        this.mobilePendingAccounts.delete(accountId);
      }
      
      if (error.message.includes('RateLimitExceeded') || error.message.includes('Превышен лимит запросов')) {
        // Устанавливаем ограничение на 15 минут при превышении лимита запросов
        // Если не используется мобильное подтверждение
        if (!options?.waitForMobileConfirmation) {
          const limitTime = Date.now() + 15 * 60 * 1000; // 15 минут
          this.rateLimit.set(accountId, limitTime);
          
          logger.warn(`Превышен лимит запросов Steam для аккаунта ${account.username}. Установлено ограничение на 15 минут`);
          throw new Error(`Превышен лимит запросов Steam. Подождите 15 минут перед новой попыткой для аккаунта ${account.username}, используйте мобильное подтверждение или нажмите "Сбросить ограничение"`);
        } else {
          // В случае мобильного подтверждения просто передаем ошибку дальше
          throw error;
        }
      } else if (error.message.includes('мобильное') || error.message.includes('подтверждение')) {
        // Если ошибка связана с мобильным подтверждением, но мы не в режиме ожидания - предлагаем его использовать
        if (!options?.waitForMobileConfirmation) {
          throw new Error(`Для аккаунта ${account.username} может потребоваться мобильное подтверждение. Попробуйте включить эту опцию.`);
        }
        // Иначе просто передаем ошибку дальше
        throw error;
      }
      
      logger.error(`Ошибка при входе в Steam для аккаунта ${account.username}: ${error.message}`);
      throw error;
    }
  }

  /**
   * Выход из Steam клиента для указанного аккаунта
   * @param accountId ID аккаунта
   */
  async logoutAccount(accountId: string): Promise<boolean> {
    const client = this.clients.get(accountId);
    if (!client) {
      logger.warn(`Попытка выхода из несуществующего клиента для аккаунта ${accountId}`);
      return false;
    }

    try {
      // Останавливаем таймер фарминга кейсов
      const timerId = this.timers.get(accountId);
      if (timerId) {
        clearInterval(timerId);
        this.timers.delete(accountId);
        logger.info(`Таймер фарминга кейсов для аккаунта ${accountId} остановлен`);
      }
      
      // Удаляем из списка ожидающих мобильного подтверждения
      this.mobilePendingAccounts.delete(accountId);
      
      await client.logout();
      this.clients.delete(accountId);
      logger.info(`Выход из Steam клиента для аккаунта ${accountId} выполнен успешно`);
      return true;
    } catch (error: any) {
      logger.error(`Ошибка при выходе из Steam клиента для аккаунта ${accountId}: ${error.message}`);
      return false;
    }
  }

  /**
   * Запуск CS2 для указанного аккаунта
   * @param accountId ID аккаунта
   */
  async startGame(accountId: string): Promise<boolean> {
    // Получаем клиент или возвращаем ошибку
    const client = this.clients.get(accountId);
    if (!client) {
      logger.warn(`Попытка запуска CS2 для несуществующего клиента аккаунта ${accountId}`);
      return false;
    }

    try {
      logger.info(`Запускаем CS2 для аккаунта ${accountId}`);
      
      // Проверяем текущий статус
      const status = client.getStatus();
      logger.info(`Текущий статус аккаунта: ${JSON.stringify(status)}`);
      
      // Если пользователь не авторизован, пробуем автоматически войти
      if (!status.isLoggedIn) {
        logger.warn(`Аккаунт ${accountId} не авторизован в Steam. Пробуем автоматический вход...`);
        
        try {
          // Находим аккаунт в базе данных
          const Account = (await import('@/models/Account')).default;
          const dbConnect = (await import('@/lib/dbConnect')).default;
          
          await dbConnect();
          const account = await Account.findById(accountId);
          
          if (!account) {
            logger.error(`Аккаунт ${accountId} не найден в базе данных`);
            return false;
          }
          
          // Выполняем автоматический вход
          logger.info(`Выполняем автоматический вход для аккаунта ${account.username}`);
          await this.loginAccount(account);
          
          // Проверяем статус после входа
          const newStatus = client.getStatus();
          if (!newStatus.isLoggedIn) {
            logger.error(`Не удалось автоматически войти в аккаунт ${accountId}`);
            return false;
          }
          
          logger.info(`Автоматический вход в аккаунт ${account.username} выполнен успешно`);
        } catch (loginError: any) {
          logger.error(`Ошибка при автоматическом входе: ${loginError.message}`);
          return false;
        }
      }
      
      // Запускаем игру
      logger.info(`Запускаем CS2 для аккаунта ${accountId} после проверки авторизации`);
      const result = await client.startGame();
      
      if (result) {
        logger.info(`CS2 запущен для аккаунта ${accountId}`);
        
        // Запускаем таймер для эмуляции получения кейсов
        this.setupCaseFarmingTimer(accountId);
        
        return true;
      } else {
        logger.warn(`Не удалось запустить CS2 для аккаунта ${accountId}`);
        return false;
      }
    } catch (error: any) {
      logger.error(`Ошибка при запуске CS2 для аккаунта ${accountId}: ${error.message}`);
      return false;
    }
  }

  /**
   * Остановка CS2 для указанного аккаунта
   * @param accountId ID аккаунта
   */
  async stopGame(accountId: string): Promise<boolean> {
    const client = this.clients.get(accountId);
    if (!client) {
      logger.warn(`Попытка остановки CS2 для несуществующего клиента аккаунта ${accountId}`);
      return false;
    }

    try {
      // Останавливаем таймер фарминга кейсов
      const timerId = this.timers.get(accountId);
      if (timerId) {
        clearInterval(timerId);
        this.timers.delete(accountId);
        logger.info(`Таймер фарминга кейсов для аккаунта ${accountId} остановлен`);
      }
      
      const result = await client.stopGame();
      if (result) {
        logger.info(`CS2 остановлен для аккаунта ${accountId}`);
      } else {
        logger.warn(`Не удалось остановить CS2 для аккаунта ${accountId}`);
      }
      return result;
    } catch (error: any) {
      logger.error(`Ошибка при остановке CS2 для аккаунта ${accountId}: ${error.message}`);
      return false;
    }
  }

  /**
   * Получение статуса клиента для указанного аккаунта
   * @param accountId ID аккаунта
   */
  getClientStatus(accountId: string): SteamUserStatus | null {
    const client = this.clients.get(accountId);
    if (!client) {
      // Проверяем, ожидает ли аккаунт мобильного подтверждения
      if (this.mobilePendingAccounts.get(accountId)) {
        return {
          isLoggedIn: false,
          requiresMobileConfirmation: true,
          error: 'Ожидается подтверждение через мобильное приложение'
        };
      }
      return null;
    }
    return client.getStatus();
  }

  /**
   * Проверка, активен ли клиент для указанного аккаунта
   * @param accountId ID аккаунта
   */
  isClientActive(accountId: string): boolean {
    return this.clients.has(accountId);
  }

  /**
   * Проверка, ожидает ли клиент мобильного подтверждения
   * @param accountId ID аккаунта
   */
  isWaitingForMobileConfirmation(accountId: string): boolean {
    const client = this.clients.get(accountId);
    if (client && client.isWaitingForMobileConfirmation()) {
      return true;
    }
    return this.mobilePendingAccounts.get(accountId) || false;
  }

  /**
   * Получение количества активных клиентов
   */
  getActiveClientCount(): number {
    return this.clients.size;
  }

  /**
   * Получение списка ID аккаунтов с активными клиентами
   */
  getActiveClientIds(): string[] {
    return Array.from(this.clients.keys());
  }

  /**
   * Проверка, находится ли аккаунт в режиме ограничения скорости запросов
   * @param accountId ID аккаунта
   */
  isRateLimited(accountId: string): boolean {
    const rateLimitTime = this.rateLimit.get(accountId);
    return rateLimitTime !== undefined && Date.now() < rateLimitTime;
  }

  /**
   * Получение времени ожидания до снятия ограничения
   * @param accountId ID аккаунта
   * @returns Время в минутах или null, если ограничения нет
   */
  getRateLimitWaitTime(accountId: string): number | null {
    const rateLimitTime = this.rateLimit.get(accountId);
    if (!rateLimitTime || Date.now() >= rateLimitTime) {
      return null;
    }
    return Math.ceil((rateLimitTime - Date.now()) / 1000 / 60);
  }

  /**
   * Установка максимального количества одновременных клиентов
   * @param count Максимальное количество клиентов
   */
  setMaxConcurrentClients(count: number): void {
    this.maxConcurrentClients = count;
    logger.info(`Установлено новое ограничение на количество Steam клиентов: ${count}`);
  }

  /**
   * Очистка ограничения скорости для аккаунта
   * @param accountId ID аккаунта
   */
  clearRateLimit(accountId: string): void {
    if (this.rateLimit.has(accountId)) {
      this.rateLimit.delete(accountId);
      logger.info(`Ограничение скорости для аккаунта ${accountId} сброшено`);
      return;
    }
    logger.info(`Для аккаунта ${accountId} не было установлено ограничение`);
  }

  /**
   * Проверка наличия и сброс ограничения для всех аккаунтов пользователя
   * @param userId ID пользователя
   */
  async clearRateLimitsForUser(userId: string): Promise<{cleared: number}> {
    try {
      const Account = (await import('@/models/Account')).default;
      const dbConnect = (await import('@/lib/dbConnect')).default;
      
      await dbConnect();
      const accounts = await Account.find({ user: userId });
      
      let clearedCount = 0;
      for (const account of accounts) {
        const accountId = account._id.toString();
        if (this.rateLimit.has(accountId)) {
          this.rateLimit.delete(accountId);
          clearedCount++;
        }
      }
      
      logger.info(`Сброшены ограничения для ${clearedCount} аккаунтов пользователя ${userId}`);
      return { cleared: clearedCount };
    } catch (error: any) {
      logger.error(`Ошибка при сбросе ограничений: ${error.message}`);
      throw error;
    }
  }

  /**
   * Выход из всех активных клиентов
   */
  async logoutAllClients(): Promise<void> {
    const clientIds = this.getActiveClientIds();
    logger.info(`Выход из всех Steam клиентов (${clientIds.length})...`);

    for (const id of clientIds) {
      await this.logoutAccount(id);
    }

    // Очищаем список ожидающих мобильного подтверждения
    this.mobilePendingAccounts.clear();

    logger.info('Выход из всех Steam клиентов выполнен успешно');
  }

  /**
   * Настройка таймера для эмуляции получения кейсов
   * @param accountId ID аккаунта
   */
  private setupCaseFarmingTimer(accountId: string): void {
    // Очищаем существующий таймер, если есть
    const existingTimerId = this.timers.get(accountId);
    if (existingTimerId) {
      clearInterval(existingTimerId);
    }
    
    // Настраиваем новый таймер
    const timerId = setInterval(async () => {
      try {
        // Проверяем, активен ли клиент
        if (!this.isClientActive(accountId)) {
          clearInterval(timerId);
          return;
        }
        
        // Проверяем статус
        const status = this.getClientStatus(accountId);
        if (!status?.isPlayingCS2) {
          clearInterval(timerId);
          return;
        }
        
        // Находим аккаунт в базе данных
        const Account = (await import('@/models/Account')).default;
        const dbConnect = (await import('@/lib/dbConnect')).default;
        
        await dbConnect();
        const account = await Account.findById(accountId);
        
        if (!account) {
          logger.warn(`Аккаунт ${accountId} не найден в базе данных`);
          return;
        }
        
        // Увеличиваем счетчик кейсов
        account.casesCollected += 1;
        await account.save();
        
        logger.info(`Получен кейс для аккаунта ${accountId}. Всего кейсов: ${account.casesCollected}`);
      } catch (error: any) {
        logger.error(`Ошибка при обработке фарма кейсов для ${accountId}: ${error.message}`);
      }
    }, 10 * 60 * 1000); // Каждые 10 минут
    
    // Сохраняем ID таймера
    this.timers.set(accountId, timerId);
    logger.info(`Настроен таймер фарминга кейсов для аккаунта ${accountId}`);
  }
} 
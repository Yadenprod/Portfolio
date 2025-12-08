import SteamUser from 'steam-user';
import SteamTotp from 'steam-totp';
import { EventEmitter } from 'events';
import { logger } from '@/lib/logger';

export interface SteamLoginOptions {
  username: string;
  password: string;
  sharedSecret?: string;
  twoFactorCode?: string;
  waitForMobileConfirmation?: boolean;
}

export interface SteamUserStatus {
  isLoggedIn: boolean;
  steamId?: string;
  error?: string;
  lastLogin?: Date;
  isPlayingCS2?: boolean;
  requiresMobileConfirmation?: boolean;
}

/**
 * Класс для работы с Steam API
 */
export class SteamAPI extends EventEmitter {
  private steamClient: SteamUser;
  private status: SteamUserStatus = {
    isLoggedIn: false
  };
  private isLoggingIn: boolean = false;
  private waitingForMobileConfirmation: boolean = false;
  private mobileConfirmationTimeout: NodeJS.Timeout | null = null;

  constructor() {
    super();
    this.steamClient = new SteamUser({
      promptSteamGuardCode: false,
      httpTimeout: 30000,
      autoRelogin: false
    });
    this.setupEventHandlers();
  }

  /**
   * Настройка обработчиков событий Steam клиента
   */
  private setupEventHandlers(): void {
    // Обработка успешного входа
    this.steamClient.on('loggedOn', (details) => {
      this.status.isLoggedIn = true;
      this.status.steamId = this.steamClient.steamID?.toString();
      this.status.lastLogin = new Date();
      this.status.error = undefined;
      this.isLoggingIn = false;
      this.waitingForMobileConfirmation = false;
      
      if (this.mobileConfirmationTimeout) {
        clearTimeout(this.mobileConfirmationTimeout);
        this.mobileConfirmationTimeout = null;
      }

      logger.info(`Steam клиент успешно вошел в аккаунт ${this.steamClient.steamID?.toString()}`);
      this.emit('loggedOn', { ...this.status });
    });

    // Обработка отключения от Steam
    this.steamClient.on('disconnected', (eresult, msg) => {
      this.status.isLoggedIn = false;
      this.isLoggingIn = false;
      this.waitingForMobileConfirmation = false;
      
      if (this.mobileConfirmationTimeout) {
        clearTimeout(this.mobileConfirmationTimeout);
        this.mobileConfirmationTimeout = null;
      }
      
      logger.info(`Steam клиент отключен: ${msg}`);
      this.emit('disconnected', { eresult, msg });
    });

    // Обработка ошибок
    this.steamClient.on('error', (err) => {
      this.status.error = err.message;
      this.isLoggingIn = false;
      this.waitingForMobileConfirmation = false;
      
      if (this.mobileConfirmationTimeout) {
        clearTimeout(this.mobileConfirmationTimeout);
        this.mobileConfirmationTimeout = null;
      }
      
      logger.error(`Ошибка Steam клиента: ${err.message}`);
      this.emit('error', err);
    });

    // Обработка запроса двухфакторной аутентификации
    this.steamClient.on('steamGuard', (domain, callback, lastCodeWrong) => {
      logger.info(`Запрошен код Steam Guard${domain ? ` для домена ${domain}` : ''}`);
      this.emit('steamGuard', { domain, lastCodeWrong, callback });
    });
  }

  /**
   * Вход в Steam аккаунт
   */
  async login(options: SteamLoginOptions): Promise<SteamUserStatus> {
    // Проверка, не выполняется ли уже вход
    if (this.isLoggingIn) {
      logger.warn(`Попытка повторного входа в аккаунт ${options.username} во время выполнения предыдущего запроса`);
      throw new Error('Вход уже выполняется, дождитесь завершения');
    }

    try {
      this.isLoggingIn = true;
      logger.info(`Попытка входа в аккаунт Steam: ${options.username}`);

      // Подготавливаем параметры входа
      const loginOptions: any = {
        accountName: options.username,
        password: options.password,
        rememberPassword: true,
        logonID: Math.floor(Math.random() * 1000000),
        useLoginKey: false
      };

      // Генерируем код Steam Guard, если есть shared secret
      if (options.sharedSecret) {
        try {
          loginOptions.twoFactorCode = SteamTotp.generateAuthCode(options.sharedSecret);
          logger.info(`Сгенерирован код Steam Guard для аккаунта ${options.username}`);
        } catch (error: any) {
          logger.error(`Ошибка генерации кода Steam Guard: ${error.message}`);
        }
      } else if (options.twoFactorCode) {
        // Используем предоставленный код двухфакторной аутентификации
        loginOptions.twoFactorCode = options.twoFactorCode;
        logger.info(`Используем предоставленный код Steam Guard: ${options.twoFactorCode}`);
      }

      // Если выбран режим ожидания мобильного подтверждения
      const waitForMobile = options.waitForMobileConfirmation === true;
      
      // Выполняем вход в аккаунт
      return new Promise((resolve, reject) => {
        let steamGuardPromise: Promise<void> | null = null;
        let timeoutId: NodeJS.Timeout | null = null;
        
        // Устанавливаем обработчик события успешного входа
        const onLoggedOn = () => {
          if (timeoutId) clearTimeout(timeoutId);
          this.steamClient.removeListener('error', onError);
          this.steamClient.removeListener('steamGuard', onSteamGuard);
          
          // Явно устанавливаем флаг входа в систему
          this.status.isLoggedIn = true;
          this.status.steamId = this.steamClient.steamID?.toString();
          this.status.lastLogin = new Date();
          this.status.error = undefined;
          this.isLoggingIn = false;
          this.waitingForMobileConfirmation = false;
          
          if (this.mobileConfirmationTimeout) {
            clearTimeout(this.mobileConfirmationTimeout);
            this.mobileConfirmationTimeout = null;
          }
          
          logger.info(`Пользователь ${options.username} успешно вошел в Steam. SteamID: ${this.status.steamId}`);
          
          // Возвращаем успешный статус
          resolve({ ...this.status });
        };

        // Устанавливаем обработчик ошибок
        const onError = (err: Error) => {
          if (timeoutId) clearTimeout(timeoutId);
          this.steamClient.removeListener('loggedOn', onLoggedOn);
          this.steamClient.removeListener('steamGuard', onSteamGuard);
          
          this.status.isLoggedIn = false;
          this.status.error = err.message;
          this.isLoggingIn = false;
          this.waitingForMobileConfirmation = false;
          
          if (this.mobileConfirmationTimeout) {
            clearTimeout(this.mobileConfirmationTimeout);
            this.mobileConfirmationTimeout = null;
          }
          
          logger.error(`Ошибка при входе в Steam: ${err.message}`);
          
          if (err.message === 'RateLimitExceeded') {
            reject(new Error('Превышен лимит запросов к Steam. Рекомендуется: 1) Подождите 15-30 минут 2) Попробуйте использовать мобильное подтверждение 3) Проверьте правильность данных.'));
          } else if (err.message.includes('InvalidPassword') || err.message.includes('password')) {
            reject(new Error('Неверный пароль для аккаунта Steam. Проверьте правильность введенных данных.'));
          } else if (err.message.includes('InvalidLoginAuthCode') || err.message.includes('TwoFactorCodeMismatch')) {
            reject(new Error('Неверный код Steam Guard. Пожалуйста, проверьте код и попробуйте снова.'));
          } else {
            reject(err);
          }
        };
        
        // Обработчик запроса Steam Guard
        const onSteamGuard = (domain: string, callback: (code: string) => void, lastCodeWrong: boolean) => {
          logger.info(`Запрошен код Steam Guard${domain ? ` для домена ${domain}` : ''}`);
          
          // Если код неверный, сообщаем об этом
          if (lastCodeWrong) {
            logger.warn(`Предыдущий код Steam Guard был неверным для аккаунта ${options.username}`);
          }
          
          // Если выбран режим мобильного подтверждения
          if (waitForMobile) {
            this.waitingForMobileConfirmation = true;
            logger.info(`Ожидаем подтверждение входа через мобильное приложение для ${options.username}`);
            
            // Информируем, что требуется мобильное подтверждение
            this.status.requiresMobileConfirmation = true;
            this.emit('mobileConfirmationRequired', { username: options.username });
            
            // Устанавливаем таймаут для мобильного подтверждения (3 минуты)
            this.mobileConfirmationTimeout = setTimeout(() => {
              logger.warn(`Истекло время ожидания мобильного подтверждения для ${options.username}`);
              this.waitingForMobileConfirmation = false;
              callback(''); // Отправляем пустой код, чтобы прервать процесс
              reject(new Error('Время ожидания мобильного подтверждения истекло'));
            }, 180000); // 3 минуты
            
            return;
          }
          
          // Если есть twoFactorCode в опциях, используем его сразу
          if (options.twoFactorCode) {
            logger.info(`Автоматически отправляем код Steam Guard: ${options.twoFactorCode}`);
            callback(options.twoFactorCode);
            return;
          }
          
          // Если обработчик Steam Guard уже установлен через внешний emit, не перезаписываем его
          if (!steamGuardPromise) {
            steamGuardPromise = new Promise<void>((resolveGuard) => {
              this.emit('steamGuard', { 
                domain, 
                lastCodeWrong, 
                callback: (code: string) => {
                  logger.info(`Получен код Steam Guard: ${code}`);
                  callback(code);
                  resolveGuard();
                } 
              });
            });
          }
        };

        // Добавляем временные обработчики
        this.steamClient.once('loggedOn', onLoggedOn);
        this.steamClient.once('error', onError);
        this.steamClient.on('steamGuard', onSteamGuard);

        // Выполняем вход
        try {
          this.steamClient.logOn(loginOptions);
        } catch (err: any) {
          this.isLoggingIn = false;
          logger.error(`Ошибка при вызове logOn: ${err.message}`);
          reject(err);
          return;
        }
        
        // Добавляем таймаут, чтобы не ждать ответа вечно
        // Увеличиваем таймаут до 180 секунд для учета процесса Steam Guard
        timeoutId = setTimeout(() => {
          this.steamClient.removeListener('loggedOn', onLoggedOn);
          this.steamClient.removeListener('error', onError);
          this.steamClient.removeListener('steamGuard', onSteamGuard);
          
          this.isLoggingIn = false;
          this.waitingForMobileConfirmation = false;
          
          if (this.mobileConfirmationTimeout) {
            clearTimeout(this.mobileConfirmationTimeout);
            this.mobileConfirmationTimeout = null;
          }
          
          logger.error(`Таймаут авторизации для аккаунта ${options.username} (180 секунд)`);
          reject(new Error('Таймаут авторизации в Steam. Возможно, Steam не отвечает или требуется подтверждение входа.'));
        }, 180000); // 180 секунд таймаут
      });
    } catch (error: any) {
      this.isLoggingIn = false;
      this.waitingForMobileConfirmation = false;
      this.status.error = error.message;
      logger.error(`Ошибка при входе в Steam: ${error.message}`);
      return Promise.reject(error);
    }
  }

  /**
   * Выход из аккаунта Steam
   */
  async logout(): Promise<void> {
    return new Promise((resolve) => {
      if (!this.status.isLoggedIn) {
        resolve();
        return;
      }

      this.steamClient.once('disconnected', () => {
        this.status.isLoggedIn = false;
        this.status.steamId = undefined;
        this.waitingForMobileConfirmation = false;
        
        if (this.mobileConfirmationTimeout) {
          clearTimeout(this.mobileConfirmationTimeout);
          this.mobileConfirmationTimeout = null;
        }
        
        logger.info('Выход из аккаунта Steam выполнен');
        resolve();
      });

      this.steamClient.logOff();
    });
  }

  /**
   * Получение текущего статуса
   */
  getStatus(): SteamUserStatus {
    // Проверяем, действительно ли клиент авторизован по наличию steamID
    const actuallyLoggedIn = this.steamClient.steamID !== null;
    
    // Если статусы не совпадают, исправляем
    if (this.status.isLoggedIn !== actuallyLoggedIn) {
      logger.warn(`Несоответствие статуса аккаунта: status.isLoggedIn=${this.status.isLoggedIn}, actuallyLoggedIn=${actuallyLoggedIn}`);
      this.status.isLoggedIn = actuallyLoggedIn;
    }
    
    // Если ожидаем мобильного подтверждения, добавляем это в статус
    if (this.waitingForMobileConfirmation) {
      this.status.requiresMobileConfirmation = true;
    }
    
    return { ...this.status };
  }

  /**
   * Проверка, выполняется ли сейчас вход
   */
  isLogonInProgress(): boolean {
    return this.isLoggingIn;
  }

  /**
   * Проверка, ожидается ли подтверждение через мобильное приложение
   */
  isWaitingForMobileConfirmation(): boolean {
    return this.waitingForMobileConfirmation;
  }

  /**
   * Проверка, запущен ли CS2 для данного аккаунта
   */
  async isGameRunning(): Promise<boolean> {
    if (!this.status.isLoggedIn) {
      return false;
    }

    try {
      const appInfo = await this.steamClient.getProductInfo([730], [], true);
      return !!appInfo;
    } catch (error) {
      logger.error('Ошибка при проверке статуса игры:', error);
      return false;
    }
  }

  /**
   * Запуск CS2
   */
  async startGame(): Promise<boolean> {
    if (!this.status.isLoggedIn) {
      logger.error('Попытка запустить CS2, когда пользователь не авторизован в Steam');
      return false;
    }

    try {
      logger.info(`Попытка запуска CS2 (AppID 730) для пользователя ${this.status.steamId}`);
      
      // Устанавливаем обработчики событий для отслеживания состояния игры
      this.steamClient.on('appLaunched', (appid) => {
        logger.info(`Приложение ${appid} запущено`);
      });

      this.steamClient.on('playingState', (blocked, playingApp) => {
        logger.info(`Изменение состояния игры: blocked=${blocked}, playingApp=${playingApp}`);
      });

      // Запускаем игру
      this.steamClient.gamesPlayed(730);
      
      // Обновляем статус
      this.status.isPlayingCS2 = true;
      
      logger.info('CS2 запущен успешно');
      return true;
    } catch (error: any) {
      logger.error(`Ошибка при запуске CS2: ${error.message || 'Неизвестная ошибка'}`);
      logger.error(`Стек вызовов: ${error.stack || 'Недоступен'}`);
      return false;
    }
  }

  /**
   * Остановка CS2
   */
  async stopGame(): Promise<boolean> {
    if (!this.status.isLoggedIn) {
      logger.warn('Попытка остановить CS2, когда пользователь не авторизован в Steam');
      return false;
    }

    try {
      logger.info(`Останавливаем CS2 для пользователя ${this.status.steamId}`);
      this.steamClient.gamesPlayed([]);
      
      // Обновляем статус
      this.status.isPlayingCS2 = false;
      
      logger.info('CS2 остановлен успешно');
      return true;
    } catch (error: any) {
      logger.error(`Ошибка при остановке CS2: ${error.message || 'Неизвестная ошибка'}`);
      return false;
    }
  }
} 
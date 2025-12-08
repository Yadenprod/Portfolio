/**
 * Простой логгер для приложения
 */

// Типы уровней логирования
export type LogLevel = 'error' | 'warn' | 'info' | 'debug';

// Определение интерфейса логгера
export interface Logger {
  error(message: string, ...args: any[]): void;
  warn(message: string, ...args: any[]): void;
  info(message: string, ...args: any[]): void;
  debug(message: string, ...args: any[]): void;
  setLevel(level: LogLevel): void;
}

// Числовые значения для уровней логирования
const LOG_LEVELS: Record<LogLevel, number> = {
  error: 0,
  warn: 1,
  info: 2,
  debug: 3
};

/**
 * Создание класса логгера
 */
class LoggerImplementation implements Logger {
  private level: LogLevel = 'info';

  /**
   * Установка уровня логирования
   * @param level - Уровень логирования
   */
  setLevel(level: LogLevel): void {
    this.level = level;
  }

  /**
   * Проверяет, нужно ли логировать сообщение данного уровня
   * @param msgLevel - Уровень сообщения
   * @returns true, если нужно логировать
   */
  private shouldLog(msgLevel: LogLevel): boolean {
    return LOG_LEVELS[msgLevel] <= LOG_LEVELS[this.level];
  }

  /**
   * Форматирование времени для лога
   * @returns Отформатированное время
   */
  private getFormattedTime(): string {
    const now = new Date();
    return now.toISOString();
  }

  /**
   * Вывод сообщения в лог
   * @param level - Уровень сообщения
   * @param message - Текст сообщения
   * @param args - Дополнительные аргументы
   */
  private log(level: LogLevel, message: string, ...args: any[]): void {
    if (!this.shouldLog(level)) return;

    const time = this.getFormattedTime();
    const prefix = `[${time}] [${level.toUpperCase()}]`;

    if (args.length > 0) {
      console[level === 'error' ? 'error' : level === 'warn' ? 'warn' : 'log'](
        `${prefix} ${message}`, ...args
      );
    } else {
      console[level === 'error' ? 'error' : level === 'warn' ? 'warn' : 'log'](
        `${prefix} ${message}`
      );
    }

    // В реальном приложении здесь может быть сохранение лога в файл
    // или отправка в систему мониторинга
  }

  /**
   * Логирование сообщения уровня error
   * @param message - Текст сообщения
   * @param args - Дополнительные аргументы
   */
  error(message: string, ...args: any[]): void {
    this.log('error', message, ...args);
  }

  /**
   * Логирование сообщения уровня warn
   * @param message - Текст сообщения
   * @param args - Дополнительные аргументы
   */
  warn(message: string, ...args: any[]): void {
    this.log('warn', message, ...args);
  }

  /**
   * Логирование сообщения уровня info
   * @param message - Текст сообщения
   * @param args - Дополнительные аргументы
   */
  info(message: string, ...args: any[]): void {
    this.log('info', message, ...args);
  }

  /**
   * Логирование сообщения уровня debug
   * @param message - Текст сообщения
   * @param args - Дополнительные аргументы
   */
  debug(message: string, ...args: any[]): void {
    this.log('debug', message, ...args);
  }
}

// Создание и экспорт singleton-экземпляра логгера
export const logger: Logger = new LoggerImplementation(); 
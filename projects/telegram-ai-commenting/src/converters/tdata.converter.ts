import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';
import { Logger } from '../utils/logger';

export interface TelegramSession {
  sessionString: string;
  apiId: number;
  apiHash: string;
  phoneNumber?: string;
  userId?: number;
}

export interface TDataAccount {
  accountId: string;
  sessionData: TelegramSession;
  isActive: boolean;
  lastUsed?: Date;
}

export class TDataConverter {
  private logger: Logger;
  private encryptionKey: string;

  constructor(logger: Logger) {
    this.logger = logger;
    this.encryptionKey = process.env.ENCRYPTION_KEY || this.generateEncryptionKey();
  }

  /**
   * Конвертирует папку tdata в session файлы
   * @param tdataPath Путь к папке tdata
   * @param outputPath Путь для сохранения session файлов
   */
  async convertTDataToSessions(tdataPath: string, outputPath: string): Promise<TDataAccount[]> {
    try {
      this.logger.info(`Converting tdata from ${tdataPath} to sessions in ${outputPath}`);

      if (!fs.existsSync(tdataPath)) {
        throw new Error(`TData folder not found: ${tdataPath}`);
      }

      // Создаем выходную папку если не существует
      if (!fs.existsSync(outputPath)) {
        fs.mkdirSync(outputPath, { recursive: true });
      }

      const accounts: TDataAccount[] = [];
      const tdataFiles = this.getTDataFiles(tdataPath);

      for (const file of tdataFiles) {
        try {
          const sessionData = await this.parseTDataFile(file);
          if (sessionData) {
            const accountId = this.generateAccountId(sessionData);
            const encryptedSession = this.encryptSession(sessionData);
            
            // Сохраняем зашифрованную сессию
            const sessionPath = path.join(outputPath, `${accountId}.session`);
            fs.writeFileSync(sessionPath, encryptedSession);

            accounts.push({
              accountId,
              sessionData,
              isActive: true,
              lastUsed: new Date()
            });

            this.logger.info(`Converted session for account: ${accountId}`);
          }
        } catch (error) {
          this.logger.error(`Failed to convert tdata file ${file}:`, error);
        }
      }

      this.logger.info(`Successfully converted ${accounts.length} accounts`);
      return accounts;
    } catch (error) {
      this.logger.error('Failed to convert tdata to sessions:', error);
      throw error;
    }
  }

  /**
   * Парсит файл tdata и извлекает данные сессии
   */
  private async parseTDataFile(filePath: string): Promise<TelegramSession | null> {
    try {
      const fileData = fs.readFileSync(filePath);
      
      // TData файлы обычно содержат бинарные данные
      // Здесь нужно реализовать специфичную логику парсинга
      // в зависимости от версии Telegram Desktop
      
      const sessionData = this.parseTDataBinary(fileData);
      return sessionData;
    } catch (error) {
      this.logger.error(`Failed to parse tdata file ${filePath}:`, error);
      return null;
    }
  }

  /**
   * Парсит бинарные данные tdata файла
   */
  private parseTDataBinary(data: Buffer): TelegramSession | null {
    try {
      // Это упрощенная реализация
      // В реальном проекте нужна более сложная логика парсинга
      // в зависимости от структуры tdata файлов
      
      // Извлекаем основные данные сессии
      const sessionString = this.extractSessionString(data);
      const apiId = parseInt(process.env.TELEGRAM_API_ID || '0');
      const apiHash = process.env.TELEGRAM_API_HASH || '';

      if (!sessionString || !apiId || !apiHash) {
        return null;
      }

      return {
        sessionString,
        apiId,
        apiHash
      };
    } catch (error) {
      this.logger.error('Failed to parse tdata binary data:', error);
      return null;
    }
  }

  /**
   * Извлекает строку сессии из бинарных данных
   */
  private extractSessionString(data: Buffer): string {
    // Упрощенная реализация - в реальности нужен более сложный парсинг
    try {
      // Ищем паттерны сессии в бинарных данных
      const sessionPattern = /[A-Za-z0-9+/]{40,}/;
      const match = data.toString('utf8').match(sessionPattern);
      return match ? match[0] : '';
    } catch (error) {
      this.logger.error('Failed to extract session string:', error);
      return '';
    }
  }

  /**
   * Получает список файлов tdata
   */
  private getTDataFiles(tdataPath: string): string[] {
    const files: string[] = [];
    
    try {
      const items = fs.readdirSync(tdataPath);
      
      for (const item of items) {
        const itemPath = path.join(tdataPath, item);
        const stat = fs.statSync(itemPath);
        
        if (stat.isFile() && this.isTDataFile(item)) {
          files.push(itemPath);
        }
      }
    } catch (error) {
      this.logger.error('Failed to read tdata directory:', error);
    }
    
    return files;
  }

  /**
   * Проверяет, является ли файл tdata файлом
   */
  private isTDataFile(filename: string): boolean {
    const tdataExtensions = ['.tdata', '.session', '.key'];
    return tdataExtensions.some(ext => filename.endsWith(ext));
  }

  /**
   * Шифрует данные сессии
   */
  private encryptSession(session: TelegramSession): string {
    try {
      const algorithm = 'aes-256-gcm';
      const iv = crypto.randomBytes(16);
      const cipher = crypto.createCipher(algorithm, this.encryptionKey);
      
      let encrypted = cipher.update(JSON.stringify(session), 'utf8', 'hex');
      encrypted += cipher.final('hex');
      
      return JSON.stringify({
        iv: iv.toString('hex'),
        encrypted,
        algorithm
      });
    } catch (error) {
      this.logger.error('Failed to encrypt session:', error);
      throw error;
    }
  }

  /**
   * Расшифровывает данные сессии
   */
  decryptSession(encryptedData: string): TelegramSession {
    try {
      const data = JSON.parse(encryptedData);
      const algorithm = data.algorithm;
      const iv = Buffer.from(data.iv, 'hex');
      const decipher = crypto.createDecipher(algorithm, this.encryptionKey);
      
      let decrypted = decipher.update(data.encrypted, 'hex', 'utf8');
      decrypted += decipher.final('utf8');
      
      return JSON.parse(decrypted);
    } catch (error) {
      this.logger.error('Failed to decrypt session:', error);
      throw error;
    }
  }

  /**
   * Генерирует уникальный ID аккаунта
   */
  private generateAccountId(session: TelegramSession): string {
    const data = `${session.apiId}-${session.apiHash}-${Date.now()}`;
    return crypto.createHash('sha256').update(data).digest('hex').substring(0, 16);
  }

  /**
   * Генерирует ключ шифрования если не задан
   */
  private generateEncryptionKey(): string {
    return crypto.randomBytes(32).toString('hex');
  }

  /**
   * Проверяет валидность tdata папки
   */
  validateTDataFolder(tdataPath: string): boolean {
    try {
      if (!fs.existsSync(tdataPath)) {
        return false;
      }

      const files = fs.readdirSync(tdataPath);
      return files.some(file => this.isTDataFile(file));
    } catch (error) {
      this.logger.error('Failed to validate tdata folder:', error);
      return false;
    }
  }

  /**
   * Получает информацию о аккаунтах в tdata папке
   */
  async getTDataAccountsInfo(tdataPath: string): Promise<{ count: number; files: string[] }> {
    try {
      if (!this.validateTDataFolder(tdataPath)) {
        return { count: 0, files: [] };
      }

      const files = this.getTDataFiles(tdataPath);
      return {
        count: files.length,
        files: files.map(f => path.basename(f))
      };
    } catch (error) {
      this.logger.error('Failed to get tdata accounts info:', error);
      return { count: 0, files: [] };
    }
  }
}


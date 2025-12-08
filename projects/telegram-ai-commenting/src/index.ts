import { TelegramQRAuth } from './auth';
import { TelegramCommenter, CommentConfig } from './commenting';
import { TelegramApi } from 'gramjs';
import { StringSession } from 'gramjs/sessions';
import * as fs from 'fs';

class TelegramNeuroCommenting {
    private auth: TelegramQRAuth;
    private api: TelegramApi | null = null;
    private commenter: TelegramCommenter | null = null;

    constructor() {
        this.auth = new TelegramQRAuth(14369082, 'b221b4f79223104634a800ecd4a9c3e5', 'session.txt');
    }

    /**
     * Инициализирует систему
     */
    async initialize(): Promise<boolean> {
        try {
            console.log('🤖 Telegram Neuro Commenting System');
            console.log('=====================================\n');

            // Пытаемся загрузить существующую сессию
            const loadResult = await this.auth.loadSession();
            
            if (loadResult.success) {
                console.log('✅ Using existing session');
                this.api = this.auth.getApi();
                
                // Проверяем, что сессия работает
                const isAuth = await this.auth.isAuthenticated();
                if (!isAuth) {
                    console.log('⚠️  Session is invalid, need to re-authenticate');
                    return await this.authenticate();
                }
                
                return true;
            } else {
                console.log('🔄 No valid session found, starting authentication...');
                return await this.authenticate();
            }
        } catch (error: any) {
            console.error('❌ Initialization failed:', error.message);
            return false;
        }
    }

    /**
     * Выполняет аутентификацию
     */
    private async authenticate(): Promise<boolean> {
        const authResult = await this.auth.authenticateWithQR();
        
        if (authResult.success) {
            console.log('✅ Authentication successful!');
            this.api = this.auth.getApi();
            return true;
        } else {
            console.error('❌ Authentication failed:', authResult.error);
            return false;
        }
    }

    /**
     * Настраивает систему комментирования
     */
    setupCommenting(config: CommentConfig): void {
        if (!this.api) {
            throw new Error('Not authenticated');
        }

        this.commenter = new TelegramCommenter(this.api, config);
        console.log('✅ Commenting system configured');
    }

    /**
     * Запускает мониторинг и комментирование
     */
    async startCommenting(): Promise<void> {
        if (!this.commenter) {
            throw new Error('Commenting system not configured');
        }

        console.log('🚀 Starting commenting system...');
        await this.commenter.startMonitoring();
    }

    /**
     * Получает статистику
     */
    getStats(): any {
        if (!this.commenter) {
            return { error: 'Commenting system not configured' };
        }

        return this.commenter.getStats();
    }

    /**
     * Отключается
     */
    async disconnect(): Promise<void> {
        if (this.api) {
            await this.api.disconnect();
            console.log('🔌 Disconnected from Telegram');
        }
    }
}

// Пример использования
async function main() {
    const system = new TelegramNeuroCommenting();

    try {
        // Инициализируем систему
        const initialized = await system.initialize();
        if (!initialized) {
            console.log('❌ Failed to initialize system');
            return;
        }

        // Настраиваем комментирование
        const config: CommentConfig = {
            targetChannels: [
                'cryptonews',    // Замените на реальные каналы
                'technews',
                'startupnews'
            ],
            commentTemplates: [
                'Интересная мысль! {keywords} действительно важная тема.',
                'Согласен с автором по поводу {topic}. {keywords} - это актуально.',
                'Хорошая статья! Особенно про {keywords}.',
                'Спасибо за информацию о {topic}!',
                'Полезный пост про {keywords}. Рекомендую!'
            ],
            minDelay: 30000,    // 30 секунд
            maxDelay: 120000,   // 2 минуты
            maxCommentsPerDay: 10
        };

        system.setupCommenting(config);

        // Показываем статистику
        const stats = system.getStats();
        console.log('\n📊 Current Statistics:');
        console.log(`📝 Comments today: ${stats.commentsToday}`);
        console.log(`🎯 Max per day: ${stats.maxCommentsPerDay}`);
        console.log(`⏳ Remaining: ${stats.remainingComments}`);

        // Запускаем комментирование
        await system.startCommenting();

    } catch (error: any) {
        console.error('❌ Error:', error.message);
    } finally {
        await system.disconnect();
    }
}

// Запускаем только если файл выполняется напрямую
if (require.main === module) {
    main().catch(console.error);
}

export { TelegramNeuroCommenting };
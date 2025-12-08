import { TelegramApi } from 'gramjs';
import { StringSession } from 'gramjs/sessions';
import * as qrcode from 'qrcode-terminal';
import * as fs from 'fs';
import * as path from 'path';

class TelegramQRAuth {
    private apiId: number;
    private apiHash: string;
    private api: TelegramApi | null = null;
    private sessionFile: string;

    constructor(apiId: number, apiHash: string, sessionFile: string = 'session.txt') {
        this.apiId = apiId;
        this.apiHash = apiHash;
        this.sessionFile = sessionFile;
    }

    /**
     * Аутентификация через QR-код
     */
    async authenticateWithQR(): Promise<{ success: boolean; session?: string; user?: any; error?: string }> {
        try {
            console.log('🚀 Starting QR authentication...');
            console.log(`📱 API ID: ${this.apiId}`);
            console.log(`🔑 API Hash: ${this.apiHash.substring(0, 8)}...`);
            
            // Создаем новую сессию
            const session = new StringSession('');
            this.api = new TelegramApi(session, this.apiId, this.apiHash);
            
            // Подключаемся к Telegram
            console.log('🔌 Connecting to Telegram...');
            await this.api.start();
            
            // Получаем QR-код для авторизации
            console.log('📱 Generating QR code...');
            const qrResult = await this.api.call('auth.exportLoginToken', {
                apiId: this.apiId,
                apiHash: this.apiHash,
                exceptIds: []
            });
            
            // Показываем QR-код в консоли
            console.log('\n' + '='.repeat(50));
            console.log('📱 SCAN THIS QR CODE WITH YOUR TELEGRAM APP');
            console.log('(Make sure you\'re logged into the same account)');
            console.log('='.repeat(50));
            console.log('');
            
            qrcode.generate(qrResult.token, { 
                small: true,
                width: 40
            });
            
            console.log('\n' + '='.repeat(50));
            console.log('⏳ Waiting for QR scan... (60 seconds timeout)');
            console.log('='.repeat(50));
            
            // Ждем сканирования QR-кода
            const loginResult = await this.api.call('auth.importLoginToken', {
                token: qrResult.token
            });
            
            if (loginResult.user) {
                console.log('\n✅ Authentication successful!');
                console.log(`👤 User: ${loginResult.user.firstName} ${loginResult.user.lastName || ''}`);
                console.log(`📞 Phone: ${loginResult.user.phone || 'Not available'}`);
                console.log(`🆔 User ID: ${loginResult.user.id}`);
                
                // Сохраняем сессию
                const sessionString = this.api.session.save();
                await this.saveSession(sessionString);
                
                console.log('💾 Session saved successfully!');
                console.log(`📁 Session file: ${this.sessionFile}`);
                
                return {
                    success: true,
                    session: sessionString,
                    user: loginResult.user
                };
            } else {
                throw new Error('Authentication failed - no user data received');
            }
            
        } catch (error: any) {
            console.error('\n❌ Authentication error:', error.message);
            
            if (error.message.includes('timeout')) {
                console.log('⏰ QR code expired. Please try again.');
            } else if (error.message.includes('network')) {
                console.log('🌐 Network error. Check your internet connection.');
            } else if (error.message.includes('API_ID')) {
                console.log('🔑 Invalid API credentials. Check your API_ID and API_HASH.');
            }
            
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Загружает существующую сессию
     */
    async loadSession(): Promise<{ success: boolean; session?: string; error?: string }> {
        try {
            if (!fs.existsSync(this.sessionFile)) {
                return {
                    success: false,
                    error: 'Session file not found'
                };
            }

            const sessionString = fs.readFileSync(this.sessionFile, 'utf8').trim();
            
            if (!sessionString) {
                return {
                    success: false,
                    error: 'Session file is empty'
                };
            }

            console.log('📁 Loading existing session...');
            
            // Создаем API с существующей сессией
            const session = new StringSession(sessionString);
            this.api = new TelegramApi(session, this.apiId, this.apiHash);
            
            // Проверяем валидность сессии
            await this.api.start();
            
            console.log('✅ Session loaded successfully!');
            
            return {
                success: true,
                session: sessionString
            };
            
        } catch (error: any) {
            console.error('❌ Failed to load session:', error.message);
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Сохраняет сессию в файл
     */
    private async saveSession(sessionString: string): Promise<void> {
        try {
            fs.writeFileSync(this.sessionFile, sessionString);
            console.log(`💾 Session saved to: ${path.resolve(this.sessionFile)}`);
        } catch (error: any) {
            console.error('❌ Failed to save session:', error.message);
            throw error;
        }
    }

    /**
     * Получает API объект для дальнейшего использования
     */
    getApi(): TelegramApi | null {
        return this.api;
    }

    /**
     * Проверяет, авторизован ли пользователь
     */
    async isAuthenticated(): Promise<boolean> {
        try {
            if (!this.api) {
                return false;
            }
            
            await this.api.getMe();
            return true;
        } catch (error) {
            return false;
        }
    }

    /**
     * Получает информацию о текущем пользователе
     */
    async getCurrentUser(): Promise<any> {
        try {
            if (!this.api) {
                throw new Error('Not authenticated');
            }
            
            return await this.api.getMe();
        } catch (error: any) {
            throw new Error(`Failed to get user info: ${error.message}`);
        }
    }

    /**
     * Отключается от Telegram
     */
    async disconnect(): Promise<void> {
        try {
            if (this.api) {
                await this.api.disconnect();
                this.api = null;
                console.log('🔌 Disconnected from Telegram');
            }
        } catch (error: any) {
            console.error('❌ Error during disconnect:', error.message);
        }
    }
}

// Основная функция для запуска аутентификации
async function main() {
    const API_ID = 14369082;
    const API_HASH = 'b221b4f79223104634a800ecd4a9c3e5';
    const SESSION_FILE = 'session.txt';

    console.log('🤖 Telegram QR Authentication Tool');
    console.log('=====================================\n');

    const auth = new TelegramQRAuth(API_ID, API_HASH, SESSION_FILE);

    try {
        // Сначала пытаемся загрузить существующую сессию
        console.log('🔍 Checking for existing session...');
        const loadResult = await auth.loadSession();
        
        if (loadResult.success) {
            console.log('✅ Using existing session');
            
            // Проверяем, что сессия работает
            const isAuth = await auth.isAuthenticated();
            if (isAuth) {
                const user = await auth.getCurrentUser();
                console.log(`👤 Logged in as: ${user.firstName} ${user.lastName || ''}`);
                console.log('🎉 Ready to use! You can now use this session for commenting.');
                return;
            } else {
                console.log('⚠️  Existing session is invalid, starting fresh authentication...');
            }
        }

        // Если нет валидной сессии, запускаем QR аутентификацию
        console.log('🔄 Starting fresh authentication...');
        const authResult = await auth.authenticateWithQR();
        
        if (authResult.success) {
            console.log('\n🎉 Authentication completed successfully!');
            console.log('✅ You can now use this session for Telegram operations.');
            console.log(`📁 Session saved to: ${SESSION_FILE}`);
        } else {
            console.log('\n❌ Authentication failed:', authResult.error);
            process.exit(1);
        }

    } catch (error: any) {
        console.error('\n💥 Unexpected error:', error.message);
        process.exit(1);
    } finally {
        // Отключаемся
        await auth.disconnect();
    }
}

// Запускаем только если файл выполняется напрямую
if (require.main === module) {
    main().catch(console.error);
}

export { TelegramQRAuth };


import { TelegramApi } from 'gramjs';
import { StringSession } from 'gramjs/sessions';
import * as fs from 'fs';

async function testSession() {
    try {
        console.log('🧪 Testing Telegram session...\n');

        // Проверяем наличие файла сессии
        if (!fs.existsSync('session.txt')) {
            console.log('❌ Session file not found!');
            console.log('💡 Run "npm run auth" to authenticate first');
            return;
        }

        // Загружаем сессию
        const sessionString = fs.readFileSync('session.txt', 'utf8').trim();
        
        if (!sessionString) {
            console.log('❌ Session file is empty!');
            console.log('💡 Run "npm run auth" to authenticate first');
            return;
        }

        console.log('📁 Loading session...');
        
        // Создаем API с сессией
        const session = new StringSession(sessionString);
        const api = new TelegramApi(session, 14369082, 'b221b4f79223104634a800ecd4a9c3e5');
        
        // Подключаемся
        console.log('🔌 Connecting to Telegram...');
        await api.start();
        
        // Получаем информацию о пользователе
        console.log('👤 Getting user info...');
        const user = await api.getMe();
        
        console.log('\n✅ Session is valid!');
        console.log(`👤 User: ${user.firstName} ${user.lastName || ''}`);
        console.log(`📞 Phone: ${user.phone || 'Not available'}`);
        console.log(`🆔 User ID: ${user.id}`);
        console.log(`🌐 Username: @${user.username || 'Not set'}`);
        
        // Тестируем получение диалогов
        console.log('\n📋 Getting recent chats...');
        const dialogs = await api.getDialogs({ limit: 5 });
        
        console.log(`📊 Found ${dialogs.length} recent chats:`);
        dialogs.forEach((dialog, index) => {
            const title = dialog.title || 'Unknown';
            console.log(`  ${index + 1}. ${title}`);
        });
        
        console.log('\n🎉 Session test completed successfully!');
        console.log('✅ You can now use this session for commenting');
        
        // Отключаемся
        await api.disconnect();
        console.log('🔌 Disconnected from Telegram');
        
    } catch (error: any) {
        console.error('\n❌ Session test failed:', error.message);
        
        if (error.message.includes('AUTH_KEY_UNREGISTERED')) {
            console.log('💡 Session is invalid. Run "npm run auth" to re-authenticate');
        } else if (error.message.includes('network')) {
            console.log('🌐 Network error. Check your internet connection');
        } else if (error.message.includes('API_ID')) {
            console.log('🔑 API credentials error. Check your API_ID and API_HASH');
        }
    }
}

// Запускаем тест
testSession().catch(console.error);


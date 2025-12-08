import { TelegramApi } from 'gramjs';
import { StringSession } from 'gramjs/sessions';
import * as fs from 'fs';

interface CommentConfig {
    targetChannels: string[];
    commentTemplates: string[];
    minDelay: number;
    maxDelay: number;
    maxCommentsPerDay: number;
}

class TelegramCommenter {
    private api: TelegramApi;
    private config: CommentConfig;
    private commentsToday: number = 0;
    private lastCommentDate: string = '';

    constructor(api: TelegramApi, config: CommentConfig) {
        this.api = api;
        this.config = config;
        this.loadCommentStats();
    }

    /**
     * Загружает статистику комментариев
     */
    private loadCommentStats(): void {
        try {
            if (fs.existsSync('comment_stats.json')) {
                const stats = JSON.parse(fs.readFileSync('comment_stats.json', 'utf8'));
                this.commentsToday = stats.commentsToday || 0;
                this.lastCommentDate = stats.lastCommentDate || '';
                
                // Сбрасываем счетчик если новый день
                const today = new Date().toDateString();
                if (this.lastCommentDate !== today) {
                    this.commentsToday = 0;
                    this.lastCommentDate = today;
                }
            }
        } catch (error) {
            console.log('📊 No previous comment stats found, starting fresh');
        }
    }

    /**
     * Сохраняет статистику комментариев
     */
    private saveCommentStats(): void {
        try {
            const stats = {
                commentsToday: this.commentsToday,
                lastCommentDate: this.lastCommentDate
            };
            fs.writeFileSync('comment_stats.json', JSON.stringify(stats, null, 2));
        } catch (error) {
            console.error('❌ Failed to save comment stats:', error);
        }
    }

    /**
     * Проверяет, можно ли оставить комментарий
     */
    private canComment(): boolean {
        const today = new Date().toDateString();
        
        // Сбрасываем счетчик если новый день
        if (this.lastCommentDate !== today) {
            this.commentsToday = 0;
            this.lastCommentDate = today;
        }
        
        return this.commentsToday < this.config.maxCommentsPerDay;
    }

    /**
     * Получает случайную задержку между комментариями
     */
    private getRandomDelay(): number {
        return Math.floor(Math.random() * (this.config.maxDelay - this.config.minDelay + 1)) + this.config.minDelay;
    }

    /**
     * Получает случайный шаблон комментария
     */
    private getRandomCommentTemplate(): string {
        const templates = this.config.commentTemplates;
        return templates[Math.floor(Math.random() * templates.length)];
    }

    /**
     * Генерирует комментарий на основе поста
     */
    private generateComment(postText: string, template: string): string {
        // Простая логика генерации комментария
        // В реальном проекте здесь можно интегрировать AI
        
        const keywords = this.extractKeywords(postText);
        let comment = template;
        
        // Заменяем плейсхолдеры
        comment = comment.replace('{keywords}', keywords.join(', '));
        comment = comment.replace('{topic}', this.detectTopic(postText));
        
        return comment;
    }

    /**
     * Извлекает ключевые слова из текста поста
     */
    private extractKeywords(text: string): string[] {
        const words = text.toLowerCase()
            .replace(/[^\w\s]/g, '')
            .split(/\s+/)
            .filter(word => word.length > 3);
        
        // Простая фильтрация стоп-слов
        const stopWords = ['это', 'что', 'как', 'для', 'или', 'но', 'если', 'когда', 'где', 'почему'];
        return words.filter(word => !stopWords.includes(word)).slice(0, 5);
    }

    /**
     * Определяет тему поста
     */
    private detectTopic(text: string): string {
        const lowerText = text.toLowerCase();
        
        if (lowerText.includes('крипт') || lowerText.includes('биткоин')) return 'криптовалюты';
        if (lowerText.includes('технолог') || lowerText.includes('программ')) return 'технологии';
        if (lowerText.includes('бизнес') || lowerText.includes('стартап')) return 'бизнес';
        if (lowerText.includes('новост') || lowerText.includes('событ')) return 'новости';
        
        return 'общее';
    }

    /**
     * Получает последние посты из канала
     */
    async getChannelPosts(channelUsername: string, limit: number = 10): Promise<any[]> {
        try {
            console.log(`📡 Getting posts from @${channelUsername}...`);
            
            const channel = await this.api.getEntity(channelUsername);
            const posts = await this.api.getMessages(channel, { limit });
            
            console.log(`📰 Found ${posts.length} posts in @${channelUsername}`);
            return posts;
        } catch (error: any) {
            console.error(`❌ Failed to get posts from @${channelUsername}:`, error.message);
            return [];
        }
    }

    /**
     * Проверяет, есть ли у поста комментарии
     */
    private hasComments(post: any): boolean {
        return post.replies && post.replies.replies > 0;
    }

    /**
     /**
     * Оставляет комментарий под постом
     */
    async commentOnPost(post: any, comment: string): Promise<boolean> {
        try {
            if (!this.canComment()) {
                console.log('⏰ Daily comment limit reached');
                return false;
            }

            console.log(`💬 Posting comment: "${comment}"`);
            
            // Отправляем комментарий как ответ на пост
            await this.api.sendMessage(post.chatId, {
                message: comment,
                replyTo: post.id
            });

            // Обновляем статистику
            this.commentsToday++;
            this.saveCommentStats();
            
            console.log(`✅ Comment posted successfully! (${this.commentsToday}/${this.config.maxCommentsPerDay} today)`);
            
            return true;
        } catch (error: any) {
            console.error('❌ Failed to post comment:', error.message);
            return false;
        }
    }

    /**
     * Мониторит каналы и оставляет комментарии
     */
    async startMonitoring(): Promise<void> {
        console.log('🚀 Starting channel monitoring...');
        console.log(`📊 Max comments per day: ${this.config.maxCommentsPerDay}`);
        console.log(`⏰ Current comments today: ${this.commentsToday}`);
        
        for (const channelUsername of this.config.targetChannels) {
            try {
                console.log(`\n🔍 Checking @${channelUsername}...`);
                
                const posts = await this.getChannelPosts(channelUsername, 5);
                
                for (const post of posts) {
                    // Проверяем, есть ли комментарии и можем ли мы комментировать
                    if (this.hasComments(post) && this.canComment()) {
                        const template = this.getRandomCommentTemplate();
                        const comment = this.generateComment(post.message || '', template);
                        
                        console.log(`\n📝 Post: ${(post.message || '').substring(0, 100)}...`);
                        console.log(`💭 Generated comment: ${comment}`);
                        
                        const success = await this.commentOnPost(post, comment);
                        
                        if (success) {
                            // Задержка между комментариями
                            const delay = this.getRandomDelay();
                            console.log(`⏳ Waiting ${delay}ms before next comment...`);
                            await new Promise(resolve => setTimeout(resolve, delay));
                        }
                    }
                }
                
            } catch (error: any) {
                console.error(`❌ Error monitoring @${channelUsername}:`, error.message);
            }
        }
        
        console.log('\n✅ Monitoring cycle completed');
    }

    /**
     * Получает статистику комментариев
     */
    getStats(): { commentsToday: number; maxCommentsPerDay: number; remainingComments: number } {
        return {
            commentsToday: this.commentsToday,
            maxCommentsPerDay: this.config.maxCommentsPerDay,
            remainingComments: this.config.maxCommentsPerDay - this.commentsToday
        };
    }
}

// Пример использования
async function main() {
    try {
        // Загружаем сессию
        const sessionString = fs.readFileSync('session.txt', 'utf8').trim();
        const session = new StringSession(sessionString);
        const api = new TelegramApi(session, 14369082, 'b221b4f79223104634a800ecd4a9c3e5');
        
        await api.start();
        console.log('✅ Connected to Telegram');

        // Конфигурация для комментирования
        const config: CommentConfig = {
            targetChannels: [
                'cryptonews',  // Замените на реальные каналы
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

        const commenter = new TelegramCommenter(api, config);
        
        // Показываем статистику
        const stats = commenter.getStats();
        console.log('\n📊 Comment Statistics:');
        console.log(`📝 Comments today: ${stats.commentsToday}`);
        console.log(`🎯 Max per day: ${stats.maxCommentsPerDay}`);
        console.log(`⏳ Remaining: ${stats.remainingComments}`);

        // Запускаем мониторинг
        await commenter.startMonitoring();

    } catch (error: any) {
        console.error('❌ Error:', error.message);
    }
}

// Запускаем только если файл выполняется напрямую
if (require.main === module) {
    main().catch(console.error);
}

export { TelegramCommenter, CommentConfig };


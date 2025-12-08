import { Api } from 'gramjs';
import { TelegramService } from '../services/telegram.service';
import { Logger } from '../utils/logger';

export interface ChannelInfo {
  id: string;
  username: string;
  title: string;
  description?: string;
  participantsCount: number;
  hasComments: boolean;
  isActive: boolean;
  lastPostDate?: Date;
  commentTopics: string[];
}

export interface PostInfo {
  id: string;
  channelId: string;
  text: string;
  date: Date;
  views?: number;
  hasComments: boolean;
  commentCount?: number;
  mediaType?: 'text' | 'photo' | 'video' | 'document' | 'voice' | 'sticker';
  mediaUrl?: string;
}

export interface CommentTopic {
  topic: string;
  keywords: string[];
  priority: number;
  isActive: boolean;
}

export class ChannelParser {
  private telegramService: TelegramService;
  private logger: Logger;
  private monitoredChannels: Map<string, ChannelInfo> = new Map();
  private commentTopics: CommentTopic[] = [];

  constructor(telegramService: TelegramService, logger: Logger) {
    this.telegramService = telegramService;
    this.logger = logger;
    this.initializeCommentTopics();
  }

  /**
   * Инициализирует темы для комментариев
   */
  private initializeCommentTopics(): void {
    this.commentTopics = [
      {
        topic: 'technology',
        keywords: ['технологии', 'IT', 'программирование', 'разработка', 'код', 'software'],
        priority: 1,
        isActive: true
      },
      {
        topic: 'business',
        keywords: ['бизнес', 'стартап', 'инвестиции', 'финансы', 'маркетинг'],
        priority: 2,
        isActive: true
      },
      {
        topic: 'crypto',
        keywords: ['криптовалюта', 'биткоин', 'блокчейн', 'NFT', 'DeFi'],
        priority: 3,
        isActive: true
      },
      {
        topic: 'general',
        keywords: ['новости', 'события', 'обсуждение', 'мнение'],
        priority: 4,
        isActive: true
      }
    ];
  }

  /**
   * Находит каналы с открытыми комментариями
   */
  async findChannelsWithComments(searchQuery: string, limit: number = 50): Promise<ChannelInfo[]> {
    try {
      this.logger.info(`Searching for channels with comments: ${searchQuery}`);

      const channels: ChannelInfo[] = [];
      
      // Поиск каналов по запросу
      const searchResults = await this.telegramService.searchChannels(searchQuery, limit);
      
      for (const channel of searchResults) {
        try {
          const channelInfo = await this.analyzeChannel(channel);
          if (channelInfo.hasComments) {
            channels.push(channelInfo);
            this.logger.info(`Found channel with comments: ${channelInfo.title} (@${channelInfo.username})`);
          }
        } catch (error) {
          this.logger.error(`Failed to analyze channel ${channel.id}:`, error);
        }
      }

      this.logger.info(`Found ${channels.length} channels with open comments`);
      return channels;
    } catch (error) {
      this.logger.error('Failed to find channels with comments:', error);
      throw error;
    }
  }

  /**
   * Анализирует канал на наличие открытых комментариев
   */
  private async analyzeChannel(channel: any): Promise<ChannelInfo> {
    try {
      // Получаем информацию о канале
      const fullInfo = await this.telegramService.getChannelInfo(channel.id);
      
      // Проверяем последние посты на наличие комментариев
      const recentPosts = await this.telegramService.getRecentPosts(channel.id, 10);
      let hasComments = false;
      let commentTopics: string[] = [];

      for (const post of recentPosts) {
        if (post.hasComments) {
          hasComments = true;
          
          // Определяем темы комментариев
          const topics = this.identifyCommentTopics(post.text);
          commentTopics.push(...topics);
        }
      }

      // Убираем дубликаты тем
      commentTopics = [...new Set(commentTopics)];

      return {
        id: channel.id.toString(),
        username: channel.username || '',
        title: fullInfo.title || '',
        description: fullInfo.about || '',
        participantsCount: fullInfo.participantsCount || 0,
        hasComments,
        isActive: true,
        lastPostDate: recentPosts[0]?.date,
        commentTopics
      };
    } catch (error) {
      this.logger.error(`Failed to analyze channel ${channel.id}:`, error);
      throw error;
    }
  }

  /**
   * Определяет темы комментариев на основе текста поста
   */
  private identifyCommentTopics(text: string): string[] {
    const topics: string[] = [];
    const lowerText = text.toLowerCase();

    for (const topic of this.commentTopics) {
      if (!topic.isActive) continue;

      const hasKeyword = topic.keywords.some(keyword => 
        lowerText.includes(keyword.toLowerCase())
      );

      if (hasKeyword) {
        topics.push(topic.topic);
      }
    }

    return topics;
  }

  /**
   * Получает новые посты из мониторимых каналов
   */
  async getNewPosts(channelId: string, since?: Date): Promise<PostInfo[]> {
    try {
      this.logger.info(`Getting new posts from channel: ${channelId}`);

      const posts = await this.telegramService.getChannelPosts(channelId, since);
      const postInfos: PostInfo[] = [];

      for (const post of posts) {
        const postInfo: PostInfo = {
          id: post.id.toString(),
          channelId,
          text: post.message || '',
          date: post.date,
          views: post.views,
          hasComments: post.replies?.replies > 0,
          commentCount: post.replies?.replies,
          mediaType: this.detectMediaType(post),
          mediaUrl: this.extractMediaUrl(post)
        };

        postInfos.push(postInfo);
      }

      this.logger.info(`Found ${postInfos.length} new posts in channel ${channelId}`);
      return postInfos;
    } catch (error) {
      this.logger.error(`Failed to get new posts from channel ${channelId}:`, error);
      throw error;
    }
  }

  /**
   * Определяет тип медиа в посте
   */
  private detectMediaType(post: any): 'text' | 'photo' | 'video' | 'document' | 'voice' | 'sticker' {
    if (post.photo) return 'photo';
    if (post.video) return 'video';
    if (post.document) return 'document';
    if (post.voice) return 'voice';
    if (post.sticker) return 'sticker';
    return 'text';
  }

  /**
   * Извлекает URL медиа файла
   */
  private extractMediaUrl(post: any): string | undefined {
    // Упрощенная реализация - в реальности нужна более сложная логика
    if (post.photo) {
      return `photo_${post.photo.id}`;
    }
    if (post.video) {
      return `video_${post.video.id}`;
    }
    return undefined;
  }

  /**
   * Добавляет канал в мониторинг
   */
  async addChannelToMonitoring(channelInfo: ChannelInfo): Promise<void> {
    try {
      this.monitoredChannels.set(channelInfo.id, channelInfo);
      this.logger.info(`Added channel to monitoring: ${channelInfo.title}`);
    } catch (error) {
      this.logger.error(`Failed to add channel to monitoring:`, error);
      throw error;
    }
  }

  /**
   * Удаляет канал из мониторинга
   */
  async removeChannelFromMonitoring(channelId: string): Promise<void> {
    try {
      this.monitoredChannels.delete(channelId);
      this.logger.info(`Removed channel from monitoring: ${channelId}`);
    } catch (error) {
      this.logger.error(`Failed to remove channel from monitoring:`, error);
      throw error;
    }
  }

  /**
   * Получает список мониторимых каналов
   */
  getMonitoredChannels(): ChannelInfo[] {
    return Array.from(this.monitoredChannels.values());
  }

  /**
   * Запускает мониторинг каналов
   */
  startMonitoring(): void {
    this.logger.info('Starting channel monitoring...');
    
    // Запускаем периодическую проверку новых постов
    setInterval(async () => {
      await this.checkForNewPosts();
    }, 30000); // Проверяем каждые 30 секунд
  }

  /**
   * Проверяет новые посты во всех мониторимых каналах
   */
  private async checkForNewPosts(): Promise<void> {
    try {
      for (const [channelId, channelInfo] of this.monitoredChannels) {
        if (!channelInfo.isActive) continue;

        try {
          const newPosts = await this.getNewPosts(channelId);
          
          for (const post of newPosts) {
            if (post.hasComments) {
              // Отправляем пост в очередь для обработки
              await this.queueNewPost(post);
            }
          }
        } catch (error) {
          this.logger.error(`Failed to check new posts for channel ${channelId}:`, error);
        }
      }
    } catch (error) {
      this.logger.error('Failed to check for new posts:', error);
    }
  }

  /**
   * Отправляет новый пост в очередь для обработки
   */
  private async queueNewPost(post: PostInfo): Promise<void> {
    try {
      // Здесь будет интеграция с системой очередей
      this.logger.info(`Queued new post for processing: ${post.id} from channel ${post.channelId}`);
    } catch (error) {
      this.logger.error('Failed to queue new post:', error);
    }
  }

  /**
   * Обновляет темы комментариев
   */
  updateCommentTopics(topics: CommentTopic[]): void {
    this.commentTopics = topics;
    this.logger.info(`Updated comment topics: ${topics.length} topics`);
  }

  /**
   * Получает статистику мониторинга
   */
  getMonitoringStats(): {
    totalChannels: number;
    activeChannels: number;
    totalTopics: number;
  } {
    const totalChannels = this.monitoredChannels.size;
    const activeChannels = Array.from(this.monitoredChannels.values())
      .filter(channel => channel.isActive).length;
    const totalTopics = this.commentTopics.length;

    return {
      totalChannels,
      activeChannels,
      totalTopics
    };
  }
}


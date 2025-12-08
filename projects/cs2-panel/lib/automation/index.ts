import { GameManager } from './gameManager';
import { GameEvent } from './gameClient';
import { logger } from '@/lib/logger';

// Создаем единственный экземпляр GameManager для всего приложения
const gameManager = new GameManager();

// Подписываемся на события от клиентов
gameManager.onEvent((event: GameEvent) => {
  // Здесь можно добавить дополнительную обработку событий
  // Например, отправку уведомлений, запись в БД и т.д.
  
  if (event.type === 'caseReceived') {
    logger.info(`Получен кейс для аккаунта ${event.accountId}`);
    // В реальном приложении здесь можно было бы отправить уведомление пользователю
  }
});

// Экспортируем GameManager
export { gameManager, GameManager };
export type { GameEvent };

// Экспортируем тип GameClient для использования в других модулях
export { GameClient } from './gameClient'; 
import type { NextApiRequest, NextApiResponse } from 'next';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '../auth/[...nextauth]';
import { steamManager } from '@/lib/steam';
import { logger } from '@/lib/logger';

type Data = {
  success: boolean;
  message?: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  // Разрешаем только POST запросы
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Метод не разрешен' });
  }

  // Проверяем аутентификацию
  const session = await getServerSession(req, res, authOptions);
  if (!session) {
    return res.status(401).json({ success: false, message: 'Не авторизован' });
  }

  try {
    // Получаем данные из запроса
    const { accountId } = req.body;

    if (!accountId) {
      return res.status(400).json({ success: false, message: 'Не указан ID аккаунта' });
    }

    // Проверяем, находится ли аккаунт в режиме ограничения
    const isRateLimited = steamManager.isRateLimited(accountId);
    
    // Проверяем, активен ли клиент для этого аккаунта
    const isClientActive = steamManager.isClientActive(accountId);
    
    // Если клиент не активен, но есть ограничение скорости, сбрасываем его
    if (!isClientActive && isRateLimited) {
      steamManager.clearRateLimit(accountId);
      logger.info(`Сброшено ограничение скорости для неактивного аккаунта ${accountId}`);
      return res.status(200).json({
        success: true,
        message: 'Ограничение скорости сброшено'
      });
    }
    
    // Если клиент не активен, возвращаем ошибку
    if (!isClientActive) {
      return res.status(400).json({ 
        success: false, 
        message: 'Клиент для этого аккаунта не активен' 
      });
    }

    // Выполняем выход из Steam
    const result = await steamManager.logoutAccount(accountId);

    if (result) {
      // При успешном выходе сбрасываем ограничение скорости
      steamManager.clearRateLimit(accountId);
      
      logger.info(`Успешный выход из Steam для аккаунта ${accountId}`);
      return res.status(200).json({
        success: true,
        message: 'Успешный выход из Steam'
      });
    } else {
      return res.status(500).json({
        success: false,
        message: 'Не удалось выйти из Steam'
      });
    }
  } catch (error: any) {
    logger.error(`Ошибка при выходе из Steam: ${error.message}`);
    return res.status(500).json({
      success: false,
      message: `Ошибка при выходе из Steam: ${error.message}`
    });
  }
} 
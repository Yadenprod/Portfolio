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

    // Проверяем, активен ли клиент для этого аккаунта
    if (!steamManager.isClientActive(accountId)) {
      return res.status(400).json({ 
        success: false, 
        message: 'Необходимо сначала войти в Steam для этого аккаунта' 
      });
    }

    // Запускаем CS2
    const result = await steamManager.startGame(accountId);

    if (result) {
      logger.info(`CS2 успешно запущен для аккаунта ${accountId}`);
      return res.status(200).json({
        success: true,
        message: 'CS2 успешно запущен'
      });
    } else {
      return res.status(500).json({
        success: false,
        message: 'Не удалось запустить CS2'
      });
    }
  } catch (error: any) {
    logger.error(`Ошибка при запуске CS2: ${error.message}`);
    return res.status(500).json({
      success: false,
      message: `Ошибка при запуске CS2: ${error.message}`
    });
  }
} 
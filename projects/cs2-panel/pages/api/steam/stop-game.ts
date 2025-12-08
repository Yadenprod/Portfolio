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
        message: 'Клиент для этого аккаунта не активен' 
      });
    }

    // Останавливаем CS2
    const result = await steamManager.stopGame(accountId);

    if (result) {
      logger.info(`CS2 успешно остановлен для аккаунта ${accountId}`);
      return res.status(200).json({
        success: true,
        message: 'CS2 успешно остановлен'
      });
    } else {
      return res.status(500).json({
        success: false,
        message: 'Не удалось остановить CS2'
      });
    }
  } catch (error: any) {
    logger.error(`Ошибка при остановке CS2: ${error.message}`);
    return res.status(500).json({
      success: false,
      message: `Ошибка при остановке CS2: ${error.message}`
    });
  }
} 
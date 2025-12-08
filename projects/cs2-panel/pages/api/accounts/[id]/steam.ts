import type { NextApiRequest, NextApiResponse } from 'next';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '../../auth/[...nextauth]';
import dbConnect from '@/lib/dbConnect';
import Account from '@/models/Account';
import { steamManager } from '@/lib/steam';
import { logger } from '@/lib/logger';

type Data = {
  success: boolean;
  message?: string;
  data?: any;
  rateLimited?: boolean;
  waitTime?: number;
  requiresSteamGuard?: boolean;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const session = await getServerSession(req, res, authOptions);
  
  // Проверка авторизации
  if (!session) {
    return res.status(401).json({ success: false, message: 'Не авторизован' });
  }

  await dbConnect();
  
  // Получаем ID аккаунта из URL
  const { id } = req.query;
  
  if (!id || Array.isArray(id)) {
    return res.status(400).json({ success: false, message: 'Неверный ID аккаунта' });
  }

  // Находим аккаунт в базе данных
  const account = await Account.findById(id);
  if (!account) {
    return res.status(404).json({ success: false, message: 'Аккаунт не найден' });
  }

  // Обработка GET запроса - получение статуса Steam
  if (req.method === 'GET') {
    const status = steamManager.getClientStatus(id);
    
    // Проверяем, находится ли аккаунт в режиме ограничения
    const isRateLimited = steamManager.isRateLimited(id);
    let rateLimitData = {};
    
    if (isRateLimited) {
      const waitTimeValue = steamManager.getRateLimitWaitTime(id);
      const waitTime = waitTimeValue !== null ? waitTimeValue : 15; // Если null, используем 15 минут по умолчанию
      rateLimitData = {
        rateLimited: true,
        waitTime
      };
    }
    
    return res.status(200).json({
      success: true,
      data: {
        isConnected: !!status,
        status: status || { isLoggedIn: false },
        ...rateLimitData
      }
    });
  }
  
  // Обработка POST запроса - разные действия (login, logout, startGame, stopGame)
  else if (req.method === 'POST') {
    const { action, steamGuardCode } = req.body;
    
    if (!action) {
      return res.status(400).json({ success: false, message: 'Не указано действие' });
    }
    
    // Проверяем, находится ли аккаунт в режиме ограничения
    if (action === 'login' && steamManager.isRateLimited(id)) {
      const waitTimeValue = steamManager.getRateLimitWaitTime(id);
      const waitTime = waitTimeValue !== null ? waitTimeValue : 15; // Если null, используем 15 минут по умолчанию
      return res.status(429).json({
        success: false,
        rateLimited: true,
        waitTime,
        message: `Превышен лимит запросов к Steam. Подождите ${waitTime} минут перед новой попыткой.`
      });
    }
    
    try {
      switch (action) {
        case 'login':
          const loginStatus = await steamManager.loginAccount(account, steamGuardCode);
          
          // Обновляем данные аккаунта
          account.lastLogin = new Date();
          await account.save();
          
          return res.status(200).json({
            success: true,
            message: 'Выполнен вход в Steam',
            data: loginStatus
          });
          
        case 'logout':
          const logoutResult = await steamManager.logoutAccount(id);
          
          if (logoutResult) {
            // При успешном выходе сбрасываем ограничения на скорость запросов
            steamManager.clearRateLimit(id);
          }
          
          return res.status(200).json({
            success: logoutResult,
            message: logoutResult ? 'Выполнен выход из Steam' : 'Ошибка при выходе из Steam'
          });
          
        case 'startGame':
          if (!steamManager.isClientActive(id)) {
            return res.status(400).json({ 
              success: false,
              message: 'Сначала необходимо войти в Steam' 
            });
          }
          
          const startResult = await steamManager.startGame(id);
          
          return res.status(200).json({
            success: startResult,
            message: startResult ? 'CS2 запущен' : 'Ошибка при запуске CS2'
          });
          
        case 'stopGame':
          if (!steamManager.isClientActive(id)) {
            return res.status(400).json({ 
              success: false,
              message: 'Клиент не активен' 
            });
          }
          
          const stopResult = await steamManager.stopGame(id);
          
          return res.status(200).json({
            success: stopResult,
            message: stopResult ? 'CS2 остановлен' : 'Ошибка при остановке CS2'
          });
          
        default:
          return res.status(400).json({ 
            success: false,
            message: `Неизвестное действие: ${action}` 
          });
      }
    } catch (error: any) {
      logger.error(`Ошибка при выполнении действия ${action} для аккаунта ${id}: ${error.message}`);
      
      // Обрабатываем различные типы ошибок
      if (error.message.includes('RateLimitExceeded') || error.message.includes('Превышен лимит запросов')) {
        return res.status(429).json({
          success: false,
          rateLimited: true,
          waitTime: 15,
          message: 'Превышен лимит запросов к Steam. Подождите 15 минут перед новой попыткой.'
        });
      } else if (error.message.includes('режиме ограничения')) {
        const waitTimeValue = steamManager.getRateLimitWaitTime(id);
        const waitTime = waitTimeValue !== null ? waitTimeValue : 15;
        return res.status(429).json({
          success: false,
          rateLimited: true,
          waitTime,
          message: error.message
        });
      } else if (error.message.includes('Вход уже выполняется')) {
        return res.status(409).json({
          success: false,
          message: 'Вход уже выполняется, дождитесь завершения предыдущего запроса'
        });
      } else if (error.message.includes('Steam Guard')) {
        return res.status(200).json({
          success: false,
          requiresSteamGuard: true,
          message: 'Требуется код Steam Guard'
        });
      }
      
      return res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
  
  // Неподдерживаемый метод
  else {
    res.setHeader('Allow', ['GET', 'POST']);
    return res.status(405).json({ success: false, message: `Метод ${req.method} не разрешен` });
  }
} 
import { NextApiRequest, NextApiResponse } from 'next';
import { unstable_getServerSession } from 'next-auth/next';
import { authOptions } from '../auth/[...nextauth]';
import dbConnect from '@/lib/dbConnect';
import Account from '@/models/Account';
import { logger } from '@/lib/logger';
import { steamManager } from '@/lib/steam';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Проверяем, что метод запроса - POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Метод не разрешен' });
  }

  try {
    // Проверяем авторизацию пользователя
    const session = await unstable_getServerSession(req, res, authOptions);
    if (!session) {
      return res.status(401).json({ error: 'Необходимо авторизоваться' });
    }

    await dbConnect();

    // Получаем ID аккаунта из тела запроса
    const { accountId, steamGuardCode } = req.body;

    if (!accountId) {
      return res.status(400).json({ error: 'ID аккаунта не указан' });
    }

    // Находим аккаунт в базе данных
    const account = await Account.findOne({
      _id: accountId,
      user: session.user.id, // Проверяем, что аккаунт принадлежит текущему пользователю
    });

    if (!account) {
      return res.status(404).json({ error: 'Аккаунт не найден' });
    }

    // Проверяем, находится ли аккаунт в режиме ограничения
    if (steamManager.isRateLimited(accountId)) {
      const waitTime = steamManager.getRateLimitWaitTime(accountId);
      return res.status(429).json({
        success: false,
        rateLimited: true,
        message: `Превышен лимит запросов к Steam. Подождите ${waitTime} минут перед новой попыткой.`,
        waitTime
      });
    }

    // Если передан код Steam Guard, сохраняем его в базе данных
    if (steamGuardCode) {
      logger.info(`Получен код Steam Guard для аккаунта ${account.username}: ${steamGuardCode}`);
      account.steamGuardCode = steamGuardCode;
      await account.save();
    }

    // Выполняем вход в Steam
    try {
      const status = await steamManager.loginAccount(account, steamGuardCode);
      
      // Если авторизация успешна
      if (status.isLoggedIn) {
        // Обновляем статус аккаунта
        await Account.findByIdAndUpdate(accountId, {
          status: 'active',
          lastLogin: new Date()
        });
        
        return res.status(200).json({
          success: true,
          message: `Успешный вход в аккаунт ${account.username}`,
          status
        });
      } else if (status.error && status.error.includes('Steam Guard')) {
        // Если требуется Steam Guard (определяем по сообщению об ошибке)
        return res.status(200).json({
          success: false,
          requiresSteamGuard: true,
          message: 'Требуется код Steam Guard',
          status
        });
      } else {
        // Если авторизация не удалась по другим причинам
        return res.status(200).json({
          success: false,
          message: 'Не удалось войти в аккаунт Steam',
          status
        });
      }
    } catch (error: any) {
      logger.error(`Ошибка при входе в Steam для аккаунта ${account.username}: ${error.message}`);
      
      // Проверяем различные типы ошибок
      if (error.message && error.message.includes('Steam Guard')) {
        await Account.findByIdAndUpdate(accountId, {
          status: 'steam_guard_required'
        });
        
        return res.status(200).json({
          success: false,
          requiresSteamGuard: true,
          message: 'Требуется код Steam Guard'
        });
      } else if (error.message && error.message.includes('RateLimitExceeded') || error.message.includes('Превышен лимит запросов')) {
        return res.status(429).json({
          success: false,
          rateLimited: true,
          message: 'Превышен лимит запросов к Steam. Подождите 15 минут перед новой попыткой.'
        });
      } else if (error.message && error.message.includes('Вход уже выполняется')) {
        return res.status(409).json({
          success: false,
          message: 'Вход уже выполняется, дождитесь завершения предыдущего запроса'
        });
      } else if (error.message && error.message.includes('режиме ограничения')) {
        const waitTime = steamManager.getRateLimitWaitTime(accountId);
        return res.status(429).json({
          success: false,
          rateLimited: true,
          message: error.message,
          waitTime
        });
      }
      
      return res.status(500).json({
        success: false,
        error: `Ошибка при входе в Steam: ${error.message}`
      });
    }
  } catch (error: any) {
    logger.error(`Ошибка API при входе в Steam: ${error.message}`);
    return res.status(500).json({
      success: false,
      error: `Внутренняя ошибка сервера: ${error.message}`
    });
  }
} 
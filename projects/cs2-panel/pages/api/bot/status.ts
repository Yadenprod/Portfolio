import { NextApiRequest, NextApiResponse } from 'next';
import { unstable_getServerSession } from 'next-auth/next';
import { authOptions } from '../auth/[...nextauth]';
import dbConnect from '@/lib/dbConnect';
import Account from '@/models/Account';
import { logger } from '@/lib/logger';

// Хранилище для статистики ботов
const botStats: { [accountId: string]: any } = {};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Для GET запросов - возвращаем статистику
  if (req.method === 'GET') {
    return await getStats(req, res);
  }
  
  // Для POST запросов - обновляем статистику (от Python бота)
  if (req.method === 'POST') {
    return await updateStats(req, res);
  }
  
  return res.status(405).json({ error: 'Метод не разрешен' });
}

/**
 * Обработчик GET запросов - возвращает статистику бота
 */
async function getStats(req: NextApiRequest, res: NextApiResponse) {
  try {
    // Проверяем авторизацию пользователя
    const session = await unstable_getServerSession(req, res, authOptions);
    if (!session) {
      return res.status(401).json({ error: 'Необходимо авторизоваться' });
    }

    await dbConnect();
    
    // Получаем ID аккаунта из запроса
    const { accountId } = req.query;
    
    if (!accountId || Array.isArray(accountId)) {
      return res.status(400).json({ error: 'Некорректный ID аккаунта' });
    }

    // Находим аккаунт в базе данных
    const account = await Account.findOne({
      _id: accountId,
      user: session.user.id, // Проверяем, что аккаунт принадлежит текущему пользователю
    });

    if (!account) {
      return res.status(404).json({ error: 'Аккаунт не найден' });
    }
    
    // Получаем статистику из хранилища или возвращаем пустой объект
    const stats = botStats[accountId] || { 
      moves: 0,
      shots: 0,
      deaths: 0,
      reconnects: 0,
      session_start: null,
      session_duration: 0,
      last_update: null
    };
    
    return res.status(200).json({ 
      success: true,
      stats,
      account: {
        id: account._id,
        username: account.username,
        botStatus: account.botStatus || 'inactive',
        casesCollected: account.casesCollected || 0,
        lastBotStart: account.lastBotStart,
        lastBotStop: account.lastBotStop
      }
    });
  } catch (error: any) {
    logger.error(`Ошибка при получении статистики бота: ${error.message}`);
    return res.status(500).json({
      success: false,
      error: `Внутренняя ошибка сервера: ${error.message}`
    });
  }
}

/**
 * Обработчик POST запросов - обновляет статистику бота
 * Этот эндпоинт вызывается Python ботом
 */
async function updateStats(req: NextApiRequest, res: NextApiResponse) {
  try {
    const { account_id, stats, timestamp } = req.body;
    
    if (!account_id || !stats) {
      return res.status(400).json({ error: 'Некорректные данные статистики' });
    }
    
    // Проверяем существование аккаунта
    await dbConnect();
    const account = await Account.findById(account_id);
    
    if (!account) {
      return res.status(404).json({ error: 'Аккаунт не найден' });
    }
    
    // Обновляем статистику в хранилище
    botStats[account_id] = {
      ...stats,
      last_update: timestamp || new Date().toISOString()
    };
    
    logger.info(`Обновлена статистика для аккаунта ${account_id}: ${JSON.stringify(stats)}`);
    
    // Если бот долго работает, увеличиваем количество собранных кейсов
    // Проверяем, прошло ли минимум 10 минут с начала сессии
    if (stats.session_duration && stats.session_duration >= 600) {
      // Расчет количества кейсов: 1 кейс каждые 10 минут работы
      const casesForThisSession = Math.floor(stats.session_duration / 600);
      const previousCases = account.casesCollected || 0;
      
      // Сохраняем только если есть новые кейсы
      if (casesForThisSession > 0) {
        account.casesCollected = previousCases + 1; // Добавляем только 1 кейс за обновление
        await account.save();
        
        logger.info(`Добавлен кейс для аккаунта ${account_id}. Всего кейсов: ${account.casesCollected}`);
      }
    }
    
    return res.status(200).json({ 
      success: true,
      message: 'Статистика успешно обновлена'
    });
  } catch (error: any) {
    logger.error(`Ошибка при обновлении статистики бота: ${error.message}`);
    return res.status(500).json({
      success: false,
      error: `Внутренняя ошибка сервера: ${error.message}`
    });
  }
} 
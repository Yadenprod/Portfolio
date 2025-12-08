import type { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '../../../lib/dbConnect';
import Account from '@/models/Account';

type Stats = {
  activeAccounts: number;
  totalAccounts: number;
  totalCases: number;
  banRisk: number;
  casesCollectedToday: number;
  casesCollectedThisWeek: number;
  bannedAccounts: number;
  inactiveAccounts: number;
}

type Data = {
  success: boolean;
  message?: string;
  stats?: Stats;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  // Разрешаем только GET-запросы
  if (req.method !== 'GET') {
    return res.status(405).json({ success: false, message: 'Метод не разрешен' });
  }

  try {
    await dbConnect();
    
    // Получаем все аккаунты
    const accounts = await Account.find({});
    
    // Считаем статистику
    const activeAccounts = accounts.filter(acc => acc.status === 'active').length;
    const bannedAccounts = accounts.filter(acc => acc.status === 'banned').length;
    const inactiveAccounts = accounts.filter(acc => acc.status === 'inactive').length;
    const totalAccounts = accounts.length;
    
    // Подсчитываем общее количество собранных кейсов
    const totalCases = accounts.reduce((sum, acc) => sum + acc.casesCollected, 0);
    
    // Расчет риска бана (просто пример - в реальном приложении тут была бы сложная логика)
    const banRisk = Math.round((bannedAccounts / totalAccounts) * 100) || 0;
    
    // Данные за сегодня и за неделю (тут просто заглушки)
    // В реальном приложении тут был бы запрос с фильтрацией по дате
    const casesCollectedToday = 3; // заглушка
    const casesCollectedThisWeek = 15; // заглушка
    
    const stats: Stats = {
      activeAccounts,
      totalAccounts,
      totalCases,
      banRisk,
      casesCollectedToday,
      casesCollectedThisWeek,
      bannedAccounts,
      inactiveAccounts,
    };
    
    return res.status(200).json({
      success: true,
      stats
    });
  } catch (error: any) {
    console.error('Ошибка получения статистики:', error);
    return res.status(500).json({
      success: false,
      message: 'Ошибка сервера при получении статистики',
    });
  }
} 
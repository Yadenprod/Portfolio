import type { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '../../../lib/dbConnect';
import Account from '@/models/Account';

// Тип для элемента активности
type ActivityItem = {
  type: 'case' | 'login' | 'error';
  message: string;
  account: string;
  time: string;
  timestamp: Date;
};

type Data = {
  success: boolean;
  message?: string;
  activity?: ActivityItem[];
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
    
    // Получаем все аккаунты для имен
    const accounts = await Account.find({}, 'username');
    const usernameMap = accounts.reduce((map, acc) => {
      map[acc._id.toString()] = acc.username;
      return map;
    }, {} as Record<string, string>);
    
    // Создаем моковые данные активности
    const mockActivity: ActivityItem[] = [
      {
        type: 'case',
        message: 'Получен кейс «Призма»',
        account: usernameMap[accounts[0]?._id.toString()] || 'unknown',
        time: '2 часа назад',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000)
      },
      {
        type: 'login',
        message: 'Успешный вход в аккаунт',
        account: usernameMap[accounts[0]?._id.toString()] || 'unknown',
        time: '5 часов назад',
        timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000)
      },
      {
        type: 'error',
        message: 'Ошибка подключения',
        account: usernameMap[accounts[1]?._id.toString()] || 'unknown',
        time: '8 часов назад',
        timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000)
      },
      {
        type: 'case',
        message: 'Получен кейс «Хрома 3»',
        account: usernameMap[accounts[0]?._id.toString()] || 'unknown',
        time: '1 день назад',
        timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000)
      },
      {
        type: 'login',
        message: 'Успешный вход в аккаунт',
        account: usernameMap[accounts[2]?._id.toString()] || 'unknown',
        time: '1 день назад',
        timestamp: new Date(Date.now() - 26 * 60 * 60 * 1000)
      }
    ];
    
    // Сортируем по времени (сначала новые)
    const sortedActivity = mockActivity.sort((a, b) => 
      b.timestamp.getTime() - a.timestamp.getTime()
    );
    
    return res.status(200).json({
      success: true,
      activity: sortedActivity
    });
  } catch (error: any) {
    console.error('Ошибка получения активности:', error);
    return res.status(500).json({
      success: false,
      message: 'Ошибка сервера при получении активности',
    });
  }
} 
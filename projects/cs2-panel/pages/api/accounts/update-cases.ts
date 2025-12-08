import { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '@/lib/dbConnect';
import Account from '@/models/Account';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Разрешаем только POST запросы
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  try {
    // Подключаемся к базе данных
    await dbConnect();

    // Получаем параметры из запроса
    const { accountId, casesCollected, apiKey } = req.body;

    // Проверяем наличие API ключа
    if (!apiKey || apiKey !== process.env.BOT_API_KEY) {
      return res.status(401).json({ success: false, message: 'Unauthorized' });
    }

    // Проверяем наличие обязательных параметров
    if (!accountId) {
      return res.status(400).json({ success: false, message: 'Account ID is required' });
    }

    if (casesCollected === undefined || isNaN(Number(casesCollected))) {
      return res.status(400).json({ success: false, message: 'Valid cases count is required' });
    }

    // Находим аккаунт
    const account = await Account.findById(accountId);
    if (!account) {
      return res.status(404).json({ success: false, message: 'Account not found' });
    }

    // Обновляем количество кейсов
    account.casesCollected = Number(casesCollected);
    await account.save();

    // Возвращаем успешный ответ
    return res.status(200).json({
      success: true,
      message: 'Cases count updated successfully',
      data: {
        accountId: account._id,
        casesCollected: account.casesCollected
      }
    });
  } catch (error: any) {
    console.error('Error updating cases count:', error);
    return res.status(500).json({ success: false, message: `Server error: ${error.message}` });
  }
} 
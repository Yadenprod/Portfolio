import type { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '../../../lib/dbConnect';
import Account from '@/models/Account';

type Data = {
  success: boolean;
  message?: string;
  farmStatus?: {
    accountId: string;
    isActive: boolean;
  };
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  // Разрешаем только POST-запросы
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Метод не разрешен' });
  }

  try {
    await dbConnect();
    
    const { accountId, action } = req.body;
    
    if (!accountId || !action) {
      return res.status(400).json({ 
        success: false, 
        message: 'Необходимо указать ID аккаунта и действие (start/stop)' 
      });
    }
    
    // Проверяем существование аккаунта
    const account = await Account.findById(accountId);
    if (!account) {
      return res.status(404).json({ 
        success: false, 
        message: 'Аккаунт не найден' 
      });
    }
    
    // Проверяем статус аккаунта
    if (account.status === 'banned') {
      return res.status(400).json({ 
        success: false, 
        message: 'Нельзя запустить фарм на заблокированном аккаунте' 
      });
    }
    
    // Обработка действий
    let isActive = false;
    
    if (action === 'start') {
      // Логика запуска фарма
      // В реальном приложении здесь бы был запуск внешних процессов или обновление статуса
      
      // Обновляем статус аккаунта
      account.status = 'active';
      await account.save();
      
      isActive = true;
    } else if (action === 'stop') {
      // Логика остановки фарма
      // В реальном приложении здесь бы была остановка внешних процессов
      
      // Обновляем статус аккаунта, если нужно
      if (account.status === 'active') {
        account.status = 'inactive';
        await account.save();
      }
      
      isActive = false;
    } else {
      return res.status(400).json({ 
        success: false, 
        message: 'Неизвестное действие. Доступные действия: start, stop' 
      });
    }
    
    return res.status(200).json({
      success: true,
      message: `Фарм кейсов ${isActive ? 'запущен' : 'остановлен'} для аккаунта ${account.username}`,
      farmStatus: {
        accountId: account._id.toString(),
        isActive,
      }
    });
  } catch (error: any) {
    console.error('Ошибка фарма кейсов:', error);
    return res.status(500).json({
      success: false,
      message: 'Ошибка сервера при управлении фармом кейсов',
    });
  }
} 
import type { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '../../../lib/dbConnect';
import Account from '@/models/Account';
import GameplayAutomation from '@/models/GameplayAutomation';
import { gameManager } from '@/lib/automation';

type Data = {
  success: boolean;
  message?: string;
  data?: any;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  // Разрешаем только POST-запросы
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Метод не разрешен' });
  }

  await dbConnect();

  try {
    const { automationId, accountId } = req.body;

    // Проверяем, что указан либо automationId, либо accountId
    if (!automationId && !accountId) {
      return res.status(400).json({ 
        success: false, 
        message: 'Необходимо указать ID настроек автоматизации или ID аккаунта' 
      });
    }

    let automation;
    let account;

    if (automationId) {
      // Находим настройки автоматизации по ID и получаем связанный аккаунт
      automation = await GameplayAutomation.findById(automationId);
      
      if (!automation) {
        return res.status(404).json({ 
          success: false, 
          message: 'Настройки автоматизации не найдены' 
        });
      }
      
      account = await Account.findById(automation.accountId);
    } else {
      // Находим аккаунт по ID и связанные настройки автоматизации
      account = await Account.findById(accountId);
      
      if (!account) {
        return res.status(404).json({ 
          success: false, 
          message: 'Аккаунт не найден' 
        });
      }
      
      automation = await GameplayAutomation.findOne({ accountId });
      
      if (!automation) {
        return res.status(404).json({ 
          success: false, 
          message: 'Настройки автоматизации для данного аккаунта не найдены' 
        });
      }
    }

    // Проверяем, что аккаунт найден
    if (!account) {
      return res.status(404).json({ 
        success: false, 
        message: 'Аккаунт не найден' 
      });
    }

    // Проверяем, что аккаунт активен
    if (account.status !== 'active') {
      return res.status(400).json({ 
        success: false, 
        message: 'Аккаунт не активен, автоматизация невозможна' 
      });
    }

    // Проверяем, не запущена ли уже автоматизация для этого аккаунта
    if (gameManager.isClientActive(account._id.toString())) {
      return res.status(400).json({ 
        success: false, 
        message: 'Автоматизация для этого аккаунта уже запущена' 
      });
    }

    // Активируем настройки автоматизации
    automation.isActive = true;
    await automation.save();

    // Запускаем автоматизацию
    const success = await gameManager.startClient(account, automation);

    if (success) {
      return res.status(200).json({ 
        success: true, 
        message: 'Автоматизация успешно запущена',
        data: { accountId: account._id, automationId: automation._id }
      });
    } else {
      // Если не удалось запустить, сбрасываем флаг активности
      automation.isActive = false;
      await automation.save();
      
      return res.status(500).json({ 
        success: false, 
        message: 'Не удалось запустить автоматизацию' 
      });
    }
  } catch (error: any) {
    return res.status(500).json({ 
      success: false, 
      message: `Ошибка при запуске автоматизации: ${error.message}` 
    });
  }
} 
import type { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '../../../lib/dbConnect';
import GameplayAutomation from '@/models/GameplayAutomation';
import { gameManager } from '@/lib/automation';

type Data = {
  success: boolean;
  message?: string;
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

    if (automationId) {
      // Находим настройки автоматизации по ID
      automation = await GameplayAutomation.findById(automationId);
      
      if (!automation) {
        return res.status(404).json({ 
          success: false, 
          message: 'Настройки автоматизации не найдены' 
        });
      }
    } else {
      // Находим настройки автоматизации по ID аккаунта
      automation = await GameplayAutomation.findOne({ accountId });
      
      if (!automation) {
        return res.status(404).json({ 
          success: false, 
          message: 'Настройки автоматизации не найдены' 
        });
      }
    }

    // Проверяем, активна ли автоматизация
    if (!automation.isActive) {
      return res.status(400).json({ 
        success: false, 
        message: 'Автоматизация уже остановлена' 
      });
    }

    // Проверяем, запущен ли клиент
    const clientActive = gameManager.isClientActive(automation.accountId.toString());

    // Останавливаем автоматизацию, если клиент запущен
    if (clientActive) {
      await gameManager.stopClient(automation.accountId.toString());
    }

    // Обновляем статус автоматизации
    automation.isActive = false;
    await automation.save();

    return res.status(200).json({ 
      success: true, 
      message: 'Автоматизация успешно остановлена' 
    });
  } catch (error: any) {
    return res.status(500).json({ 
      success: false, 
      message: `Ошибка при остановке автоматизации: ${error.message}` 
    });
  }
} 
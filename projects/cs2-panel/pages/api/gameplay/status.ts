import type { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '../../../lib/dbConnect';
import Account from '@/models/Account';
import GameplayAutomation from '@/models/GameplayAutomation';
import { gameManager } from '@/lib/automation';

type Data = {
  success: boolean;
  message?: string;
  data?: {
    isActive: boolean;
    clientRunning: boolean;
    stats?: {
      activeClients: number;
      totalClients: number;
    };
    automationSettings?: any;
  };
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  // Разрешаем только GET-запросы
  if (req.method !== 'GET') {
    return res.status(405).json({ success: false, message: 'Метод не разрешен' });
  }

  await dbConnect();

  try {
    const { automationId, accountId } = req.query;

    // Если не указаны automationId и accountId, возвращаем общую статистику
    if (!automationId && !accountId) {
      const activeClients = gameManager.getActiveClientCount();
      const totalAutomations = await GameplayAutomation.countDocuments({ isActive: true });
      
      return res.status(200).json({
        success: true,
        data: {
          isActive: false,
          clientRunning: false,
          stats: {
            activeClients,
            totalClients: totalAutomations
          }
        }
      });
    }

    let automation;
    let account;

    if (automationId) {
      // Находим настройки автоматизации по ID
      automation = await GameplayAutomation.findById(automationId);
      
      if (!automation) {
        return res.status(404).json({ 
          success: false, 
          message: 'Настройки автоматизации не найдены' 
        });
      }
      
      // Получаем связанный аккаунт для дополнительной информации
      account = await Account.findById(automation.accountId);
    } else if (accountId) {
      // Находим настройки автоматизации по ID аккаунта
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

    if (!automation) {
      return res.status(404).json({ 
        success: false, 
        message: 'Настройки автоматизации не найдены' 
      });
    }

    // Проверяем, запущен ли клиент
    const clientRunning = gameManager.isClientActive(automation.accountId.toString());

    // Если в базе данных указано, что автоматизация активна, но клиент не запущен,
    // исправляем несоответствие
    if (automation.isActive && !clientRunning) {
      automation.isActive = false;
      await automation.save();
    }

    return res.status(200).json({
      success: true,
      data: {
        isActive: automation.isActive,
        clientRunning,
        automationSettings: {
          _id: automation._id,
          accountId: automation.accountId,
          username: account?.username,
          mapPreference: automation.mapPreference,
          autoJoinDeathmatch: automation.autoJoinDeathmatch,
          farmingHoursPerDay: automation.farmingHoursPerDay,
          autoReconnect: automation.autoReconnect,
          experienceGained: automation.experienceGained,
          currentLevel: automation.currentLevel,
          nextCaseDropEstimate: automation.nextCaseDropEstimate,
          lastGameActivity: automation.lastGameActivity
        }
      }
    });
  } catch (error: any) {
    return res.status(500).json({ 
      success: false, 
      message: `Ошибка при получении статуса автоматизации: ${error.message}` 
    });
  }
} 
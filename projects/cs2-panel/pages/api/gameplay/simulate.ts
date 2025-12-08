import type { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '@/lib/dbConnect';
import Account from '@/models/Account';
import GameplayAutomation from '@/models/GameplayAutomation';
import { logger } from '@/lib/logger';

// Тип для ответа API
type SimulationResponse = {
  success: boolean;
  message?: string;
  simulationResults?: {
    experienceGained: number;
    currentLevel: number;
    previousLevel: number;
    leveledUp: boolean;
    caseDropped: boolean;
    totalCases: number;
    totalXP: number;
  };
};

// Константы для симуляции
const XP_PER_LEVEL = 5000; // XP для перехода на следующий уровень
const CASE_DROP_CHANCE = 0.15; // 15% шанс выпадения кейса после игры

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<SimulationResponse>
) {
  // Только POST запросы
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  await dbConnect();

  const { accountId, experienceGained } = req.body;

  // Проверка необходимых параметров
  if (!accountId) {
    return res.status(400).json({ success: false, message: 'Account ID is required' });
  }

  if (!experienceGained || typeof experienceGained !== 'number' || experienceGained <= 0) {
    return res.status(400).json({ 
      success: false, 
      message: 'Valid experience gained value is required' 
    });
  }

  try {
    // Получаем аккаунт и настройки автоматизации
    const account = await Account.findById(accountId);
    
    if (!account) {
      return res.status(404).json({ success: false, message: 'Account not found' });
    }

    const automation = await GameplayAutomation.findOne({ account: accountId });
    
    if (!automation) {
      return res.status(404).json({ 
        success: false, 
        message: 'Gameplay automation settings not found for this account' 
      });
    }

    // Проверяем, активна ли автоматизация
    if (!automation.isActive) {
      return res.status(400).json({ 
        success: false, 
        message: 'Gameplay automation is not active for this account' 
      });
    }

    // Получаем текущий опыт и уровень
    const previousXP = account.statistics.totalXP || 0;
    const previousLevel = account.statistics.currentLevel || 1;
    
    // Добавляем полученный опыт
    const totalXP = previousXP + experienceGained;
    const currentLevel = Math.floor(totalXP / XP_PER_LEVEL) + 1;
    const leveledUp = currentLevel > previousLevel;

    // Проверяем выпадение кейса
    const caseDropped = Math.random() < CASE_DROP_CHANCE;
    const totalCases = account.statistics.totalCases || 0;
    const newTotalCases = caseDropped ? totalCases + 1 : totalCases;

    // Обновляем статистику аккаунта
    account.statistics.totalXP = totalXP;
    account.statistics.currentLevel = currentLevel;
    account.statistics.totalCases = newTotalCases;
    account.statistics.lastActivity = new Date();
    
    // Если выпал кейс, добавляем запись в историю
    if (caseDropped) {
      account.caseHistory.push({
        date: new Date(),
        type: 'weekly', // Предполагаем, что это еженедельный кейс
        source: 'gameplay',
        isOpened: false
      });

      logger.info(`Кейс выпал для аккаунта ${account.username} (ID: ${accountId})`);
    }

    // Если повысился уровень, записываем в историю
    if (leveledUp) {
      logger.info(`Аккаунт ${account.username} (ID: ${accountId}) повысил уровень с ${previousLevel} до ${currentLevel}`);
    }

    // Сохраняем изменения в аккаунте
    await account.save();

    // Возвращаем результаты симуляции
    return res.status(200).json({
      success: true,
      simulationResults: {
        experienceGained,
        currentLevel,
        previousLevel,
        leveledUp,
        caseDropped,
        totalCases: newTotalCases,
        totalXP
      }
    });

  } catch (error) {
    logger.error(`Ошибка при симуляции игрового процесса: ${error}`);
    return res.status(500).json({ 
      success: false, 
      message: `Error processing gameplay simulation: ${error}` 
    });
  }
} 
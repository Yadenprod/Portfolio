import type { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '../../../lib/dbConnect';
import GameplayAutomation from '@/models/GameplayAutomation';
import Account from '@/models/Account';

type Data = {
  success: boolean;
  message?: string;
  automationSettings?: any[];
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  await dbConnect();

  // Получение всех настроек автоматизации игрового процесса (GET)
  if (req.method === 'GET') {
    try {
      const automationSettings = await GameplayAutomation.find({})
        .populate('accountId', 'username status')
        .sort({ createdAt: -1 });
      
      return res.status(200).json({ success: true, automationSettings });
    } catch (error: any) {
      return res.status(500).json({ success: false, message: error.message });
    }
  }

  // Создание новых настроек автоматизации (POST)
  if (req.method === 'POST') {
    try {
      const { accountId } = req.body;
      
      // Проверка, существует ли аккаунт
      const account = await Account.findById(accountId);
      if (!account) {
        return res.status(404).json({ success: false, message: 'Аккаунт не найден' });
      }
      
      // Проверка, есть ли уже настройки для этого аккаунта
      const existingSettings = await GameplayAutomation.findOne({ accountId });
      if (existingSettings) {
        return res.status(400).json({ 
          success: false, 
          message: 'Настройки автоматизации для этого аккаунта уже существуют' 
        });
      }
      
      // Установка даты следующего ожидаемого дропа кейса (через 7 дней)
      const nextCaseDropDate = new Date();
      nextCaseDropDate.setDate(nextCaseDropDate.getDate() + 7);
      
      const automationSettings = await GameplayAutomation.create({
        ...req.body,
        nextCaseDropEstimate: nextCaseDropDate
      });
      
      return res.status(201).json({ 
        success: true, 
        automationSettings: [automationSettings] 
      });
    } catch (error: any) {
      return res.status(400).json({ success: false, message: error.message });
    }
  }

  // Метод не разрешен
  return res.status(405).json({ success: false, message: 'Метод не разрешен' });
} 
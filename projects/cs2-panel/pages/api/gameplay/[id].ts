import type { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '../../../lib/dbConnect';
import GameplayAutomation from '@/models/GameplayAutomation';

type Data = {
  success: boolean;
  message?: string;
  automationSettings?: any;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const { id } = req.query;
  await dbConnect();

  // Получение настроек автоматизации по ID (GET)
  if (req.method === 'GET') {
    try {
      const automationSettings = await GameplayAutomation.findById(id)
        .populate('accountId', 'username status');
      
      if (!automationSettings) {
        return res.status(404).json({ 
          success: false, 
          message: 'Настройки автоматизации не найдены' 
        });
      }
      
      return res.status(200).json({ success: true, automationSettings });
    } catch (error: any) {
      return res.status(500).json({ success: false, message: error.message });
    }
  }

  // Обновление настроек автоматизации (PUT)
  if (req.method === 'PUT') {
    try {
      const automationSettings = await GameplayAutomation.findByIdAndUpdate(id, req.body, {
        new: true,
        runValidators: true
      }).populate('accountId', 'username status');
      
      if (!automationSettings) {
        return res.status(404).json({ 
          success: false, 
          message: 'Настройки автоматизации не найдены' 
        });
      }
      
      return res.status(200).json({ success: true, automationSettings });
    } catch (error: any) {
      return res.status(400).json({ success: false, message: error.message });
    }
  }

  // Удаление настроек автоматизации (DELETE)
  if (req.method === 'DELETE') {
    try {
      const deletedSettings = await GameplayAutomation.findByIdAndDelete(id);
      
      if (!deletedSettings) {
        return res.status(404).json({ 
          success: false, 
          message: 'Настройки автоматизации не найдены' 
        });
      }
      
      return res.status(200).json({ 
        success: true, 
        message: 'Настройки автоматизации успешно удалены' 
      });
    } catch (error: any) {
      return res.status(500).json({ success: false, message: error.message });
    }
  }

  // Метод не разрешен
  return res.status(405).json({ success: false, message: 'Метод не разрешен' });
} 
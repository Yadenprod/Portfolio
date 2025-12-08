import type { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '../../../lib/dbConnect';
import User from '@/models/User';

type Settings = {
  generalSettings?: {
    autoLogin?: boolean;
    proxiesEnabled?: boolean;
    caseCollectionEnabled?: boolean;
    useCustomSteamPath?: boolean;
    customSteamPath?: string;
    maxConcurrentAccounts?: number;
    logLevel?: string;
  };
  notificationSettings?: {
    emailNotifications?: boolean;
    telegramNotifications?: boolean;
    telegramBotToken?: string;
    telegramChatId?: string;
    notifyOnCaseCollected?: boolean;
    notifyOnBan?: boolean;
    notifyOnLogin?: boolean;
  };
};

type Data = {
  success: boolean;
  message?: string;
  settings?: Settings;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  await dbConnect();

  // Получение настроек (GET)
  if (req.method === 'GET') {
    try {
      // В реальном приложении тут был бы запрос настроек для конкретного пользователя
      // по ID из сессии или JWT токена
      
      // Для демонстрации возвращаем настройки по умолчанию
      const defaultSettings: Settings = {
        generalSettings: {
          autoLogin: true,
          proxiesEnabled: false,
          caseCollectionEnabled: true,
          useCustomSteamPath: false,
          customSteamPath: 'C:\\Program Files (x86)\\Steam\\steam.exe',
          maxConcurrentAccounts: 5,
          logLevel: 'info',
        },
        notificationSettings: {
          emailNotifications: true,
          telegramNotifications: false,
          telegramBotToken: '',
          telegramChatId: '',
          notifyOnCaseCollected: true,
          notifyOnBan: true,
          notifyOnLogin: false,
        }
      };
      
      return res.status(200).json({ success: true, settings: defaultSettings });
    } catch (error: any) {
      return res.status(500).json({ success: false, message: error.message });
    }
  }

  // Сохранение настроек (POST)
  if (req.method === 'POST') {
    try {
      const { generalSettings, notificationSettings } = req.body;
      
      // Валидация настроек
      if (!generalSettings && !notificationSettings) {
        return res.status(400).json({ 
          success: false, 
          message: 'Не указаны настройки для сохранения' 
        });
      }
      
      // В реальном приложении тут был бы поиск и обновление настроек пользователя
      // Например:
      // const userId = // получение ID пользователя из сессии или JWT
      // await User.findByIdAndUpdate(userId, { 
      //   'settings.generalSettings': generalSettings,
      //   'settings.notificationSettings': notificationSettings
      // });
      
      // Для демонстрации просто возвращаем полученные настройки
      const savedSettings: Settings = {
        generalSettings,
        notificationSettings
      };
      
      return res.status(200).json({ 
        success: true, 
        message: 'Настройки успешно сохранены',
        settings: savedSettings
      });
    } catch (error: any) {
      return res.status(400).json({ success: false, message: error.message });
    }
  }

  // Метод не разрешен
  return res.status(405).json({ success: false, message: 'Метод не разрешен' });
} 
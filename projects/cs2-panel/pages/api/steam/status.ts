import type { NextApiRequest, NextApiResponse } from 'next';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '../auth/[...nextauth]';
import dbConnect from '@/lib/dbConnect';
import Account from '@/models/Account';
import { steamManager } from '@/lib/steam';

type Data = {
  success: boolean;
  message?: string;
  status?: any;
  activeClients?: number;
  activeClientIds?: string[];
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  // Разрешаем только GET запросы
  if (req.method !== 'GET') {
    return res.status(405).json({ success: false, message: 'Метод не разрешен' });
  }

  // Проверяем аутентификацию
  const session = await getServerSession(req, res, authOptions);
  if (!session) {
    return res.status(401).json({ success: false, message: 'Не авторизован' });
  }

  await dbConnect();

  try {
    const { accountId } = req.query;

    // Если не указан ID аккаунта, возвращаем общую информацию о клиентах
    if (!accountId) {
      return res.status(200).json({
        success: true,
        activeClients: steamManager.getActiveClientCount(),
        activeClientIds: steamManager.getActiveClientIds()
      });
    }

    // Проверяем, существует ли аккаунт
    const account = await Account.findById(accountId);
    if (!account) {
      return res.status(404).json({ success: false, message: 'Аккаунт не найден' });
    }

    // Получаем статус клиента
    const status = steamManager.getClientStatus(accountId as string);
    
    if (!status) {
      return res.status(200).json({
        success: true,
        message: 'Клиент не активен',
        status: { isLoggedIn: false }
      });
    }

    return res.status(200).json({
      success: true,
      status
    });
  } catch (error: any) {
    return res.status(500).json({
      success: false,
      message: `Ошибка при получении статуса Steam: ${error.message}`
    });
  }
} 
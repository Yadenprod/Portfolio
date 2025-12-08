import { NextApiRequest, NextApiResponse } from 'next';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '../auth/[...nextauth]';
import dbConnect from '../../../lib/dbConnect';
import AccountModel from '../../../models/Account';
import { Account } from '../../../types/account';

type ApiResponse = {
  success: boolean;
  message?: string;
  account?: Account;
  error?: any;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ApiResponse>
) {
  // Проверяем авторизацию пользователя
  const session = await getServerSession(req, res, authOptions);
  
  if (!session) {
    return res.status(401).json({
      success: false,
      message: 'Не авторизован'
    });
  }

  // Получаем ID аккаунта из URL
  const { id } = req.query;
  
  if (!id || typeof id !== 'string') {
    return res.status(400).json({
      success: false,
      message: 'ID аккаунта отсутствует или недействителен'
    });
  }

  console.log(`Запрос ${req.method} к аккаунту с ID ${id}`);

  // Подключаемся к базе данных
  try {
    await dbConnect();
    console.log('Подключение к MongoDB успешно');
  } catch (error) {
    console.error('Ошибка подключения к MongoDB:', error);
    return res.status(500).json({
      success: false,
      message: 'Ошибка подключения к базе данных',
      error: error
    });
  }
  
  // Находим аккаунт, проверяя, что он принадлежит текущему пользователю
  let account;
  try {
    account = await AccountModel.findOne({
      _id: id,
      user: session.user.id
    });
  } catch (error: any) {
    console.error(`Ошибка при поиске аккаунта ${id}:`, error);
    return res.status(500).json({
      success: false,
      message: `Ошибка при поиске аккаунта: ${error.message}`,
      error: error
    });
  }
  
  if (!account) {
    return res.status(404).json({
      success: false,
      message: 'Аккаунт не найден или у вас нет прав доступа'
    });
  }
  
  // Обрабатываем разные типы запросов
  switch (req.method) {
    case 'GET':
      return res.status(200).json({
        success: true,
        account
      });
      
    case 'PUT':
      try {
        // Получаем данные для обновления
        const { username, password, steamGuardCode, sharedSecret, status, notes, proxySetting } = req.body;
        
        console.log(`Обновление аккаунта ${id}:`, {
          username,
          password: password ? '********' : undefined,
          steamGuardCode,
          sharedSecret,
          status,
          notes,
          proxySetting
        });
        
        // Обновляем только поля, которые переданы в запросе
        if (username) account.username = username;
        if (password) account.password = password;
        if (steamGuardCode !== undefined) account.steamGuardCode = steamGuardCode;
        if (sharedSecret !== undefined) account.sharedSecret = sharedSecret;
        if (status) account.status = status;
        if (notes !== undefined) account.notes = notes;
        if (proxySetting !== undefined) account.proxySetting = proxySetting;
        
        // Сохраняем изменения
        await account.save();
        console.log(`Аккаунт ${id} успешно обновлен`);
        
        return res.status(200).json({
          success: true,
          message: 'Аккаунт успешно обновлен',
          account
        });
      } catch (error: any) {
        console.error(`Ошибка при обновлении аккаунта ${id}:`, error);
        
        // Проверяем, является ли ошибка ошибкой дубликата (уникальности)
        if (error.code === 11000) {
          return res.status(400).json({
            success: false,
            message: 'Аккаунт с таким именем пользователя уже существует',
            error: error
          });
        }
        
        return res.status(500).json({
          success: false,
          message: `Ошибка при обновлении аккаунта: ${error.message}`,
          error: error
        });
      }
      
    case 'DELETE':
      try {
        // Удаляем аккаунт
        await AccountModel.deleteOne({ _id: id });
        console.log(`Аккаунт ${id} успешно удален`);
        
        return res.status(200).json({
          success: true,
          message: 'Аккаунт успешно удален'
        });
      } catch (error: any) {
        console.error(`Ошибка при удалении аккаунта ${id}:`, error);
        return res.status(500).json({
          success: false,
          message: `Ошибка при удалении аккаунта: ${error.message}`,
          error: error
        });
      }
      
    default:
      return res.status(405).json({
        success: false,
        message: `Метод ${req.method} не поддерживается`
      });
  }
} 
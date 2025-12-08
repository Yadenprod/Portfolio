import { NextApiRequest, NextApiResponse } from 'next';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '../auth/[...nextauth]';
import dbConnect from '../../../lib/dbConnect';
import AccountModel from '../../../models/Account';
import { Account } from '../../../types/account';

type ApiResponse = {
  success: boolean;
  message?: string;
  accounts?: Account[];
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
  
  // Обрабатываем разные типы запросов
  switch (req.method) {
    case 'GET':
      try {
        // Получаем аккаунты для текущего пользователя
        const accounts = await AccountModel.find({
          user: session.user.id
        }).sort({ createdAt: -1 });
        
        return res.status(200).json({
          success: true,
          accounts
        });
      } catch (error: any) {
        console.error('Ошибка при получении аккаунтов:', error);
        return res.status(500).json({
          success: false,
          message: `Ошибка при получении аккаунтов: ${error.message}`,
          error: error
        });
      }
      
    case 'POST':
      try {
        // Создаем новый аккаунт
        const { username, password, steamGuardCode, sharedSecret, status, notes, proxySetting } = req.body;
        
        console.log('Создание аккаунта, полученные данные:', { 
          username, 
          password: password ? '********' : undefined, 
          steamGuardCode, 
          sharedSecret, 
          status, 
          notes, 
          proxySetting,
          userId: session.user.id
        });

        // Проверяем наличие обязательных полей
        if (!username || !password) {
          return res.status(400).json({
            success: false,
            message: 'Имя пользователя и пароль обязательны'
          });
        }
        
        // Создаем новый аккаунт и связываем его с пользователем
        const accountData = {
          username,
          password,
          steamGuardCode: steamGuardCode || '',
          sharedSecret: sharedSecret || '',
          status: status || 'inactive',
          notes: notes || '',
          proxySetting: proxySetting || '',
          casesCollected: 0,
          lastLogin: null,
          user: session.user.id
        };

        console.log('Создаем аккаунт с данными:', {
          ...accountData,
          password: '********'
        });

        const accounts = await AccountModel.create([accountData]);
        
        console.log('Аккаунт успешно создан:', accounts[0]._id);
        
        return res.status(201).json({
          success: true,
          message: 'Аккаунт успешно создан',
          accounts
        });
      } catch (error: any) {
        console.error('Ошибка при создании аккаунта:', error);
        
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
          message: `Ошибка при создании аккаунта: ${error.message}`,
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
import { NextApiRequest, NextApiResponse } from 'next';
import mongoose from 'mongoose';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    // Проверяем текущее соединение без подключения к базе
    if (mongoose.connection.readyState === 1) {
      return res.status(200).json({ 
        status: 'OK',
        mongoStatus: 'connected',
        message: 'Подключение к базе данных установлено' 
      });
    } else {
      // Если нет соединения, возвращаем информацию
      return res.status(200).json({ 
        status: 'WARNING',
        mongoStatus: 'disconnected',
        readyState: mongoose.connection.readyState,
        message: 'Соединение с базой данных не установлено' 
      });
    }
  } catch (error: any) {
    console.error('Ошибка при проверке статуса базы данных:', error);
    return res.status(500).json({
      status: 'ERROR',
      message: 'Ошибка при проверке статуса базы данных',
      error: error.message
    });
  }
} 
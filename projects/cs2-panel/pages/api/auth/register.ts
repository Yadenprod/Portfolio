import type { NextApiRequest, NextApiResponse } from 'next';
import bcrypt from 'bcryptjs';
import dbConnect from '../../../lib/dbConnect';
import User from '@/models/User';

type Data = {
  success: boolean;
  message?: string;
  user?: {
    id: string;
    name: string;
    email: string;
  };
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  // Разрешаем только POST-запросы
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Метод не разрешен' });
  }

  try {
    // Подключаемся к базе данных
    await dbConnect();

    const { name, email, password } = req.body;

    // Проверяем, существует ли уже пользователь с таким email
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ 
        success: false, 
        message: 'Пользователь с таким email уже существует' 
      });
    }

    // Создаем нового пользователя
    const user = await User.create({
      name,
      email,
      password,
      role: 'user', // По умолчанию все новые пользователи имеют роль "user"
    });

    // Возвращаем успешный ответ без пароля
    return res.status(201).json({
      success: true,
      user: {
        id: user._id.toString(),
        name: user.name,
        email: user.email,
      },
    });
  } catch (error: any) {
    console.error('Ошибка регистрации:', error);
    return res.status(500).json({
      success: false,
      message: 'Ошибка сервера при регистрации',
    });
  }
} 
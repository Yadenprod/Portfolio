import { NextApiRequest, NextApiResponse } from 'next';
import { getServerSession } from 'next-auth';
import { authOptions } from '../auth/[...nextauth]';
import dbConnect from '@/lib/dbConnect';
import Account from '@/models/Account';
import * as fs from 'fs';
import * as path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// Допустимые действия для бота
type BotAction = 'start' | 'stop' | 'status';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Проверяем метод запроса
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  try {
    // Проверяем авторизацию
    const session = await getServerSession(req, res, authOptions);
    if (!session || !session.user) {
      return res.status(401).json({ success: false, message: 'Not authenticated' });
    }

    // Проверяем id пользователя
    if (!session.user.id) {
      console.error('API error: session.user.id is undefined', session.user);
      return res.status(401).json({ success: false, message: 'User ID not found in session' });
    }

    // Подключаемся к базе данных
    await dbConnect();

    // Получаем параметры из запроса
    const { accountId, action } = req.body;

    // Проверяем наличие обязательных параметров
    if (!accountId) {
      return res.status(400).json({ success: false, message: 'Account ID is required' });
    }

    if (!action || !['start', 'stop', 'status'].includes(action)) {
      return res.status(400).json({ success: false, message: 'Valid action is required (start, stop, status)' });
    }

    // Находим аккаунт в базе данных
    const account = await Account.findById(accountId);
    if (!account) {
      return res.status(404).json({ success: false, message: 'Account not found' });
    }

    // Проверяем наличие userId в аккаунте
    if (!account.user) {
      console.error('API error: account.user is undefined', account);
      return res.status(500).json({ success: false, message: 'Account user reference is missing' });
    }

    // Преобразуем ObjectId в строку безопасным способом
    const accountUserId = account.user.toString();
    const sessionUserId = session.user.id.toString();

    // Проверяем, принадлежит ли аккаунт текущему пользователю
    if (accountUserId !== sessionUserId) {
      console.error(`API error: User ${sessionUserId} tried to access account ${accountId} belonging to ${accountUserId}`);
      return res.status(403).json({ success: false, message: 'Not authorized to manage this account' });
    }

    // Путь к скрипту бота
    const botScriptPath = path.join(process.cwd(), 'scripts', 'cs2_bot.py');
    
    console.log(`Путь к скрипту бота: ${botScriptPath}`);

    // Проверяем существование скрипта
    if (!fs.existsSync(botScriptPath)) {
      console.error(`API error: Bot script not found at path: ${botScriptPath}`);
      return res.status(500).json({ success: false, message: 'Bot script not found' });
    }

    // Обрабатываем действие
    switch (action as BotAction) {
      case 'start':
        // Проверяем, не запущен ли бот уже
        if (account.botStatus === 'active') {
          return res.status(400).json({ success: false, message: 'Bot is already running for this account' });
        }

        try {
          // Формируем команду для запуска бота
          const pythonCommand = `python "${botScriptPath}" --account_id "${accountId}" --username "${account.username}"`;
          
          console.log(`Запуск бота с командой: ${pythonCommand}`);
          
          // Запускаем процесс в фоновом режиме
          if (process.platform === 'win32') {
            // Windows
            exec(`start /B cmd /c ${pythonCommand} > bot_${accountId}.log 2>&1`);
          } else {
            // Unix (Linux/Mac)
            exec(`nohup ${pythonCommand} > bot_${accountId}.log 2>&1 &`);
          }

          // Обновляем статус в базе данных
          account.botStatus = 'active';
          account.lastBotStart = new Date();
          await account.save();

          return res.status(200).json({ 
            success: true, 
            message: 'Bot started successfully', 
            data: { 
              status: account.botStatus, 
              lastStart: account.lastBotStart 
            } 
          });
        } catch (error: any) {
          console.error('Error starting bot:', error);
          return res.status(500).json({ success: false, message: `Error starting bot: ${error.message}` });
        }

      case 'stop':
        // Проверяем, запущен ли бот
        if (account.botStatus !== 'active') {
          return res.status(400).json({ success: false, message: 'Bot is not running for this account' });
        }

        try {
          // Останавливаем процесс бота
          if (process.platform === 'win32') {
            // Windows - ищем процесс по заголовку окна
            await execAsync(`taskkill /FI "WINDOWTITLE eq CS2Bot-${accountId}" /F`);
          } else {
            // Unix - ищем процесс по содержимому командной строки
            await execAsync(`pkill -f "python.*--account_id ${accountId}"`);
          }

          // Обновляем статус в базе данных
          account.botStatus = 'inactive';
          account.lastBotStop = new Date();
          await account.save();

          return res.status(200).json({ 
            success: true, 
            message: 'Bot stopped successfully', 
            data: { 
              status: account.botStatus, 
              lastStop: account.lastBotStop 
            } 
          });
        } catch (error: any) {
          console.error('Error stopping bot:', error);
          return res.status(500).json({ success: false, message: `Error stopping bot: ${error.message}` });
        }

      case 'status':
        // Возвращаем текущий статус бота
        return res.status(200).json({
          success: true,
          data: {
            status: account.botStatus || 'inactive',
            lastStart: account.lastBotStart,
            lastStop: account.lastBotStop,
            casesCollected: account.casesCollected
          }
        });

      default:
        return res.status(400).json({ success: false, message: 'Invalid action' });
    }
  } catch (error: any) {
    console.error('API error:', error);
    return res.status(500).json({ success: false, message: `Server error: ${error.message}` });
  }
} 
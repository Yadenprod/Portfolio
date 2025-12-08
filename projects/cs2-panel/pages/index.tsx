import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import axios from 'axios';

export default function Home() {
  const [showLogin, setShowLogin] = useState(false);
  const [dbStatus, setDbStatus] = useState<'connected' | 'disconnected' | 'error' | 'loading'>('loading');
  const [message, setMessage] = useState<string>('Проверка соединения с базой данных...');

  // Функция для проверки подключения к базе данных
  const checkDbConnection = async () => {
    try {
      const response = await axios.get('/api/health');
      if (response.data.status === 'OK') {
        setDbStatus('connected');
        setMessage('Успешное подключение к MongoDB');
      } else {
        setDbStatus('disconnected');
        setMessage('Отключено');
      }
    } catch (error) {
      console.error('Ошибка при проверке подключения к базе данных:', error);
      setDbStatus('error');
      setMessage('Ошибка подключения к базе данных');
    }
  };

  useEffect(() => {
    checkDbConnection();
    // Проверяем каждые 30 секунд
    const interval = setInterval(checkDbConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <Head>
        <title>CS2 Панель управления | Главная</title>
        <meta name="description" content="Панель управления аккаунтами CS2" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="bg-cs-dark border-b border-gray-800 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-cs-orange">
            CS2 Панель
          </Link>
          <nav>
            <Link href="/login" className="text-gray-300 hover:text-white">
              Войти
            </Link>
          </nav>
        </div>
      </header>

      <main className="flex-grow container mx-auto p-4 flex flex-col items-center justify-center">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-4">
            Управление аккаунтами <span className="text-cs-orange">CS2</span>
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Автоматизируйте сбор кейсов, управляйте множеством аккаунтов и отслеживайте их статус в одном месте.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <Link href="/login" className="cs-button text-center px-8 py-3">
            Войти в систему
          </Link>
          <Link href="/register" className="cs-button-outline text-center px-8 py-3">
            Зарегистрироваться
          </Link>
        </div>

        <div className="cs-card max-w-2xl w-full">
          <h2 className="text-xl font-bold mb-4">Основные возможности</h2>
          
          <div className="space-y-4">
            <div className="flex">
              <div className="text-cs-orange text-2xl mr-4">🎮</div>
              <div>
                <h3 className="font-medium mb-1">Управление аккаунтами</h3>
                <p className="text-gray-400">Добавляйте, редактируйте и контролируйте аккаунты CS2</p>
              </div>
            </div>
            
            <div className="flex">
              <div className="text-cs-orange text-2xl mr-4">📦</div>
              <div>
                <h3 className="font-medium mb-1">Фарм кейсов</h3>
                <p className="text-gray-400">Автоматизируйте сбор кейсов на нескольких аккаунтах одновременно</p>
              </div>
            </div>
            
            <div className="flex">
              <div className="text-cs-orange text-2xl mr-4">📊</div>
              <div>
                <h3 className="font-medium mb-1">Статистика и отчеты</h3>
                <p className="text-gray-400">Отслеживайте эффективность каждого аккаунта и общие результаты</p>
              </div>
            </div>
          </div>
        </div>

        {/* Статус подключения к базе данных */}
        <div className="mt-8 text-center">
          <p className="text-sm">
            Статус подключения к базе данных:{' '}
            {dbStatus === 'loading' ? (
              <span className="text-yellow-500">Проверка...</span>
            ) : dbStatus === 'connected' ? (
              <span className="text-green-500">Подключено</span>
            ) : dbStatus === 'disconnected' ? (
              <span className="text-yellow-500">Отключено</span>
            ) : (
              <span className="text-red-500">Ошибка</span>
            )}
          </p>
        </div>
      </main>

      {showLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
          <div className="cs-card w-full max-w-md">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Вход в панель</h2>
              <button
                onClick={() => setShowLogin(false)}
                className="text-gray-400 hover:text-white"
              >
                ✕
              </button>
            </div>
            
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Email</label>
                <input
                  type="email"
                  className="cs-input w-full"
                  placeholder="your@email.com"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Пароль</label>
                <input
                  type="password"
                  className="cs-input w-full"
                  placeholder="********"
                  required
                />
              </div>
              
              <button
                type="submit"
                className="cs-button w-full"
              >
                Войти
              </button>
              
              <div className="text-center text-sm text-gray-400 mt-4">
                Нет аккаунта?{' '}
                <Link href="/register" className="text-cs-orange hover:underline">
                  Зарегистрироваться
                </Link>
              </div>
            </form>
          </div>
        </div>
      )}

      <footer className="bg-cs-dark border-t border-gray-800 p-4 text-center text-gray-400">
        <div className="container mx-auto">
          <p>© {new Date().getFullYear()} CS2 Панель управления. Все права защищены.</p>
        </div>
      </footer>
    </div>
  );
} 
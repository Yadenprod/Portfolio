import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';

// Компонент для отображения активного фарма кейсов
const ActiveFarm = ({ 
  account, 
  onStop 
}: { 
  account: any, 
  onStop: (id: string) => void 
}) => {
  const [progress, setProgress] = useState(0);
  const [lastCase, setLastCase] = useState<string | null>(null);
  const [timeRemaining, setTimeRemaining] = useState<number>(0);
  
  // Имитация прогресса фарма кейсов
  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = Math.min(prev + Math.random() * 5, 100);
        if (newProgress === 100) {
          clearInterval(interval);
          // Имитация обнаружения кейса
          const cases = ["Кейс «Хрома 3»", "Кейс «Призма»", "Кейс «Разлом»", "Кейс «Опасная зона»"];
          setLastCase(cases[Math.floor(Math.random() * cases.length)]);
          
          // Сбросить прогресс после имитации получения кейса
          setTimeout(() => {
            setProgress(0);
            setLastCase(null);
            // Новый случайный таймер для следующего кейса (3-8 часов в миллисекундах)
            const nextTime = Math.floor(Math.random() * (8 - 3) + 3) * 60 * 60;
            setTimeRemaining(nextTime);
          }, 3000);
        }
        return newProgress;
      });
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);
  
  // Преобразование секунд в формат "чч:мм:сс"
  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };
  
  // Уменьшение таймера оставшегося времени
  useEffect(() => {
    if (timeRemaining <= 0) return;
    
    const timer = setInterval(() => {
      setTimeRemaining(prev => prev - 1);
    }, 1000);
    
    return () => clearInterval(timer);
  }, [timeRemaining]);
  
  return (
    <div className="cs-card">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-bold">{account.username}</h3>
          <p className="text-sm text-gray-400">Всего собрано: {account.casesCollected} кейсов</p>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs bg-green-900 text-green-300`}>
          Активен
        </span>
      </div>
      
      <div className="mb-4">
        <div className="flex justify-between text-sm mb-1">
          <span>Прогресс фарма:</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-2.5 mb-3">
          <div 
            className="bg-cs-orange h-2.5 rounded-full transition-all duration-500" 
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        
        {lastCase && (
          <div className="my-3 p-2 bg-green-900 bg-opacity-30 border border-green-800 rounded text-sm">
            <span className="font-medium text-green-300">Получен новый кейс: </span>
            {lastCase}
          </div>
        )}
        
        {timeRemaining > 0 && (
          <div className="text-sm text-gray-300 mb-3">
            <span>Ожидание до следующего кейса: </span>
            <span className="font-medium">{formatTime(timeRemaining)}</span>
          </div>
        )}
      </div>
      
      <div className="flex space-x-2">
        <button 
          onClick={() => onStop(account._id)} 
          className="flex-1 py-1.5 bg-red-900 hover:bg-opacity-80 rounded text-sm"
        >
          Остановить фарм
        </button>
      </div>
    </div>
  );
};

// Основной компонент страницы
export default function Cases() {
  const [accounts, setAccounts] = useState<any[]>([]);
  const [activeAccounts, setActiveAccounts] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showSelector, setShowSelector] = useState(false);
  
  // Имитация загрузки данных о аккаунтах
  useEffect(() => {
    // Тестовые данные
    const mockAccounts = [
      {
        _id: '1',
        username: 'cs2user1',
        casesCollected: 15,
        status: 'active',
      },
      {
        _id: '2',
        username: 'cs2user2',
        casesCollected: 8,
        status: 'inactive',
      },
      {
        _id: '3',
        username: 'cs2user3',
        casesCollected: 3,
        status: 'banned',
      },
      {
        _id: '4',
        username: 'cs2user4',
        casesCollected: 22,
        status: 'active',
      }
    ];
    
    // Имитация активных аккаунтов
    const mockActiveAccounts = [
      {
        _id: '1',
        username: 'cs2user1',
        casesCollected: 15,
        status: 'active',
      }
    ];
    
    setTimeout(() => {
      setAccounts(mockAccounts);
      setActiveAccounts(mockActiveAccounts);
      setIsLoading(false);
    }, 800);
  }, []);
  
  // Функция для старта фарма на выбранном аккаунте
  const startFarming = (accountId: string) => {
    const accountToStart = accounts.find(acc => acc._id === accountId);
    if (accountToStart && !activeAccounts.some(acc => acc._id === accountId)) {
      setActiveAccounts([...activeAccounts, accountToStart]);
    }
    setShowSelector(false);
  };
  
  // Функция для остановки фарма
  const stopFarming = (accountId: string) => {
    setActiveAccounts(activeAccounts.filter(acc => acc._id !== accountId));
  };
  
  // Фильтрация аккаунтов для селектора (только активные и не запущенные)
  const getAvailableAccounts = () => {
    return accounts.filter(
      acc => acc.status === 'active' && !activeAccounts.some(active => active._id === acc._id)
    );
  };
  
  return (
    <div className="min-h-screen flex flex-col">
      <Head>
        <title>Фарм кейсов | CS2 Панель</title>
        <meta name="description" content="Фарм кейсов CS2" />
      </Head>

      <header className="bg-cs-dark border-b border-gray-800 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <Link href="/dashboard" className="text-2xl font-bold text-cs-orange">
            CS2 Панель
          </Link>
          <nav>
            <ul className="flex space-x-6">
              <li>
                <Link href="/dashboard" className="text-gray-300 hover:text-white">
                  Обзор
                </Link>
              </li>
              <li>
                <Link href="/dashboard/accounts" className="text-gray-300 hover:text-white">
                  Аккаунты
                </Link>
              </li>
              <li>
                <Link href="/dashboard/cases" className="text-cs-orange font-medium">
                  Кейсы
                </Link>
              </li>
              <li>
                <Link href="/dashboard/gameplay" className="text-gray-300 hover:text-white">
                  Геймплей
                </Link>
              </li>
              <li>
                <Link href="/dashboard/settings" className="text-gray-300 hover:text-white">
                  Настройки
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      <main className="flex-grow container mx-auto p-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Фарм кейсов</h1>
          
          {!showSelector && getAvailableAccounts().length > 0 && (
            <button
              onClick={() => setShowSelector(true)}
              className="cs-button flex items-center"
            >
              <span className="mr-1">+</span> Запустить фарм
            </button>
          )}
        </div>

        {isLoading ? (
          <div className="text-center py-10">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-cs-orange mb-2"></div>
            <p>Загрузка данных...</p>
          </div>
        ) : showSelector ? (
          <div className="cs-card mb-6">
            <h2 className="text-xl font-bold mb-4">Выберите аккаунт для фарма</h2>
            
            {getAvailableAccounts().length > 0 ? (
              <div className="space-y-3">
                {getAvailableAccounts().map(account => (
                  <div 
                    key={account._id}
                    className="flex justify-between items-center p-3 border border-gray-700 rounded-md hover:border-cs-orange cursor-pointer"
                    onClick={() => startFarming(account._id)}
                  >
                    <div>
                      <h3 className="font-medium">{account.username}</h3>
                      <p className="text-sm text-gray-400">Собрано кейсов: {account.casesCollected}</p>
                    </div>
                    <span className="text-cs-orange">Выбрать</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-400">Нет доступных аккаунтов для фарма</p>
            )}
            
            <div className="mt-4">
              <button
                onClick={() => setShowSelector(false)}
                className="px-4 py-2 bg-gray-800 text-gray-300 rounded-md hover:bg-gray-700"
              >
                Отмена
              </button>
            </div>
          </div>
        ) : null}

        <div className="mb-6">
          <h2 className="text-xl font-bold mb-4">Активный фарм</h2>
          
          {activeAccounts.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {activeAccounts.map(account => (
                <ActiveFarm 
                  key={account._id}
                  account={account}
                  onStop={stopFarming}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-8 cs-card">
              <p className="text-gray-400 mb-4">У вас нет аккаунтов, активно собирающих кейсы</p>
              {getAvailableAccounts().length > 0 && (
                <button
                  onClick={() => setShowSelector(true)}
                  className="cs-button"
                >
                  Запустить фарм
                </button>
              )}
            </div>
          )}
        </div>
        
        <div>
          <h2 className="text-xl font-bold mb-4">Статистика</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="cs-card">
              <h3 className="text-lg font-medium mb-1">Всего кейсов</h3>
              <p className="text-3xl font-bold text-cs-orange">
                {accounts.reduce((sum, acc) => sum + acc.casesCollected, 0)}
              </p>
            </div>
            <div className="cs-card">
              <h3 className="text-lg font-medium mb-1">Активных аккаунтов</h3>
              <p className="text-3xl font-bold text-cs-orange">
                {activeAccounts.length}
              </p>
            </div>
            <div className="cs-card">
              <h3 className="text-lg font-medium mb-1">Кейсов за сегодня</h3>
              <p className="text-3xl font-bold text-cs-orange">
                {Math.floor(Math.random() * 5)}
              </p>
            </div>
            <div className="cs-card">
              <h3 className="text-lg font-medium mb-1">Кейсов за неделю</h3>
              <p className="text-3xl font-bold text-cs-orange">
                {Math.floor(Math.random() * 25)}
              </p>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-cs-dark border-t border-gray-800 p-4 text-center text-gray-400">
        <div className="container mx-auto">
          <p>© {new Date().getFullYear()} CS2 Панель управления. Все права защищены.</p>
        </div>
      </footer>
    </div>
  );
} 
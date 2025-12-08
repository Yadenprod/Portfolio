import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/router';

// Компонент статистической карточки
const StatCard = ({ 
  title, 
  value, 
  icon, 
  change 
}: { 
  title: string, 
  value: string | number, 
  icon: string, 
  change?: { value: number, positive: boolean } 
}) => {
  return (
    <div className="cs-card">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-gray-400 text-sm">{title}</h3>
          <p className="text-2xl font-bold">{value}</p>
          
          {change && (
            <div className={`text-xs flex items-center mt-1 ${change.positive ? 'text-green-400' : 'text-red-400'}`}>
              <span>{change.positive ? '↑' : '↓'}</span>
              <span className="ml-1">{change.value}%</span>
              <span className="ml-1">за неделю</span>
            </div>
          )}
        </div>
        <div className="text-cs-orange text-3xl">{icon}</div>
      </div>
    </div>
  );
};

// Компонент для отображения последних действий
const RecentActivity = ({ activity }: { activity: any[] }) => {
  return (
    <div className="cs-card">
      <h2 className="text-xl font-bold mb-4">Последние действия</h2>
      {activity.length === 0 ? (
        <p className="text-gray-400">Нет недавних действий</p>
      ) : (
        <div className="space-y-3">
          {activity.map((item, index) => (
            <div key={index} className="flex items-start pb-3 border-b border-gray-800 last:border-b-0 last:pb-0">
              <div className={`p-2 rounded-full mr-3 ${item.type === 'case' ? 'bg-green-900 bg-opacity-30 text-green-300' : item.type === 'login' ? 'bg-blue-900 bg-opacity-30 text-blue-300' : 'bg-red-900 bg-opacity-30 text-red-300'}`}>
                {item.type === 'case' ? '📦' : item.type === 'login' ? '🔑' : '⚠️'}
              </div>
              <div>
                <p className="font-medium">{item.message}</p>
                <div className="flex justify-between mt-1 text-sm">
                  <span className="text-gray-400">{item.account}</span>
                  <span className="text-gray-500">{item.time}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// Основной компонент страницы
export default function Dashboard() {
  const { data: session, status } = useSession();
  const router = useRouter();
  
  const [stats, setStats] = useState({
    activeAccounts: 0,
    totalAccounts: 0,
    totalCases: 0,
    banRisk: 0,
  });
  
  const [accountsData, setAccountsData] = useState<any[]>([]);
  const [recentActivity, setRecentActivity] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Проверка аутентификации
  useEffect(() => {
    if (status === 'unauthenticated') {
      router.replace('/login?callbackUrl=/dashboard');
    }
  }, [status, router]);
  
  // Имитация загрузки данных с сервера
  useEffect(() => {
    // Не загружаем данные, если не аутентифицированы
    if (status !== 'authenticated') return;
    
    // Тестовые данные
    const mockStats = {
      activeAccounts: 3,
      totalAccounts: 7,
      totalCases: 48,
      banRisk: 15,
    };
    
    const mockAccounts = [
      { username: 'cs2user1', casesCollected: 15, status: 'active', lastLogin: '2023-12-25', risk: 'low' },
      { username: 'cs2user2', casesCollected: 8, status: 'inactive', lastLogin: '2023-12-20', risk: 'medium' },
      { username: 'cs2user3', casesCollected: 3, status: 'banned', lastLogin: '2023-11-05', risk: 'high' },
      { username: 'cs2user4', casesCollected: 22, status: 'active', lastLogin: '2023-12-28', risk: 'low' },
    ];
    
    const mockActivity = [
      { type: 'case', message: 'Получен кейс «Призма»', account: 'cs2user4', time: '2 часа назад' },
      { type: 'login', message: 'Успешный вход в аккаунт', account: 'cs2user1', time: '5 часов назад' },
      { type: 'error', message: 'Ошибка подключения', account: 'cs2user2', time: '8 часов назад' },
      { type: 'case', message: 'Получен кейс «Хрома 3»', account: 'cs2user1', time: '1 день назад' },
      { type: 'login', message: 'Успешный вход в аккаунт', account: 'cs2user4', time: '1 день назад' },
    ];
    
    setTimeout(() => {
      setStats(mockStats);
      setAccountsData(mockAccounts);
      setRecentActivity(mockActivity);
      setIsLoading(false);
    }, 800);
  }, [status]);
  
  // Показываем загрузку, пока проверяем сессию
  if (status === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-cs-orange mb-2"></div>
        <span className="ml-2">Загрузка...</span>
      </div>
    );
  }
  
  return (
    <div className="min-h-screen flex flex-col">
      <Head>
        <title>Панель управления | CS2 Панель</title>
        <meta name="description" content="Панель управления CS2" />
      </Head>

      <header className="bg-cs-dark border-b border-gray-800 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <Link href="/dashboard" className="text-2xl font-bold text-cs-orange">
            CS2 Панель
          </Link>
          <nav className="flex items-center">
            <ul className="flex space-x-6 mr-6">
              <li>
                <Link href="/dashboard" className="text-cs-orange font-medium">
                  Обзор
                </Link>
              </li>
              <li>
                <Link href="/dashboard/accounts" className="text-gray-300 hover:text-white">
                  Аккаунты
                </Link>
              </li>
              <li>
                <Link href="/dashboard/cases" className="text-gray-300 hover:text-white">
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
            
            {session?.user && (
              <div className="text-sm">
                <span className="text-gray-400 mr-2">{session.user.name}</span>
                <Link href="/logout" className="text-cs-orange hover:underline">
                  Выйти
                </Link>
              </div>
            )}
          </nav>
        </div>
      </header>

      <main className="flex-grow container mx-auto p-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Обзор панели</h1>
          <div className="flex space-x-2">
            <Link href="/dashboard/accounts" className="cs-button">
              Управление аккаунтами
            </Link>
          </div>
        </div>

        {isLoading ? (
          <div className="text-center py-10">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-cs-orange mb-2"></div>
            <p>Загрузка данных...</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <StatCard 
                title="Активные аккаунты" 
                value={stats.activeAccounts} 
                icon="👤" 
                change={{ value: 20, positive: true }}
              />
              <StatCard 
                title="Всего аккаунтов" 
                value={stats.totalAccounts} 
                icon="👥"
              />
              <StatCard 
                title="Собрано кейсов" 
                value={stats.totalCases} 
                icon="📦" 
                change={{ value: 15, positive: true }}
              />
              <StatCard 
                title="Риск бана" 
                value={`${stats.banRisk}%`} 
                icon="⚠️" 
                change={{ value: 5, positive: false }}
              />
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <div className="cs-card">
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-bold">Аккаунты</h2>
                    <Link href="/dashboard/accounts" className="text-cs-orange text-sm hover:underline">
                      Посмотреть все
                    </Link>
                  </div>
                  
                  <div className="overflow-x-auto">
                    <table className="min-w-full">
                      <thead>
                        <tr className="text-left text-gray-400 text-sm border-b border-gray-800">
                          <th className="pb-3">Имя пользователя</th>
                          <th className="pb-3">Статус</th>
                          <th className="pb-3">Кейсы</th>
                          <th className="pb-3">Посл. вход</th>
                          <th className="pb-3">Риск</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-800">
                        {accountsData.map((account, index) => (
                          <tr key={index} className="text-sm">
                            <td className="py-3 font-medium">{account.username}</td>
                            <td className="py-3">
                              <span 
                                className={`px-2 py-1 rounded-full text-xs ${
                                  account.status === 'active' 
                                    ? 'bg-green-900 text-green-300' 
                                    : account.status === 'banned' 
                                      ? 'bg-red-900 text-red-300' 
                                      : 'bg-gray-700 text-gray-300'
                                }`}
                              >
                                {account.status === 'active' 
                                  ? 'Активен' 
                                  : account.status === 'banned' 
                                    ? 'Заблокирован' 
                                    : 'Неактивен'}
                              </span>
                            </td>
                            <td className="py-3 font-medium text-cs-orange">{account.casesCollected}</td>
                            <td className="py-3 text-gray-400">{account.lastLogin}</td>
                            <td className="py-3">
                              <span className={`px-2 py-1 rounded-full text-xs ${
                                account.risk === 'high' 
                                  ? 'bg-red-900 text-red-300' 
                                  : account.risk === 'medium' 
                                    ? 'bg-yellow-900 text-yellow-300' 
                                    : 'bg-green-900 text-green-300'
                              }`}>
                                {account.risk === 'high' 
                                  ? 'Высокий' 
                                  : account.risk === 'medium' 
                                    ? 'Средний' 
                                    : 'Низкий'}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              
              <div>
                <RecentActivity activity={recentActivity} />
              </div>
            </div>

            {/* Статистика кейсов */}
            <div className="cs-section mb-8">
              <h2 className="cs-section-title">Статистика кейсов</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <StatCard 
                  title="Активных аккаунтов" 
                  value={stats.activeAccounts} 
                  icon="👤" 
                  change={{ value: 20, positive: true }}
                />
                <StatCard 
                  title="Всего аккаунтов" 
                  value={stats.totalAccounts} 
                  icon="👥"
                />
                <StatCard 
                  title="Собрано кейсов" 
                  value={stats.totalCases} 
                  icon="📦" 
                  change={{ value: 15, positive: true }}
                />
                <StatCard 
                  title="Риск бана" 
                  value={`${stats.banRisk}%`} 
                  icon="⚠️" 
                  change={{ value: 5, positive: false }}
                />
              </div>
            </div>

            {/* Автоматизация геймплея */}
            <div className="cs-section mb-8">
              <div className="flex justify-between items-center mb-4">
                <h2 className="cs-section-title">Автоматизация геймплея</h2>
                <Link href="/dashboard/gameplay" className="text-cs-orange hover:text-cs-orange-light text-sm">
                  Подробнее →
                </Link>
              </div>
              
              <div className="bg-cs-dark-2 rounded-lg mb-4 p-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                  <div className="p-3 bg-cs-dark-3 rounded-md">
                    <p className="text-sm text-gray-400 mb-1">Активных аккаунтов</p>
                    <p className="text-xl font-bold text-cs-orange">1</p>
                  </div>
                  <div className="p-3 bg-cs-dark-3 rounded-md">
                    <p className="text-sm text-gray-400 mb-1">Общий опыт</p>
                    <p className="text-xl font-bold text-cs-orange">12,450 XP</p>
                  </div>
                  <div className="p-3 bg-cs-dark-3 rounded-md">
                    <p className="text-sm text-gray-400 mb-1">Ср. уровень</p>
                    <p className="text-xl font-bold text-cs-orange">3.0</p>
                  </div>
                  <div className="p-3 bg-cs-dark-3 rounded-md">
                    <p className="text-sm text-gray-400 mb-1">След. кейс через</p>
                    <p className="text-xl font-bold text-cs-orange">3 дня</p>
                  </div>
                </div>
                
                <div className="flex justify-between">
                  <div>
                    <p className="text-sm font-semibold">cs2user1</p>
                    <p className="text-xs text-gray-400">Играет на dust2</p>
                  </div>
                  <Link href="/dashboard/gameplay" className="text-xs text-cs-orange bg-cs-dark-3 px-2 py-1 rounded">
                    Управление
                  </Link>
                </div>
              </div>
              
              <Link href="/dashboard/gameplay" className="cs-card flex items-center justify-center py-3 hover:bg-cs-dark-2">
                <span className="text-cs-orange mr-2">+</span> Настроить автоматизацию геймплея
              </Link>
            </div>
          </>
        )}
      </main>

      <footer className="bg-cs-dark border-t border-gray-800 p-4 text-center text-gray-400">
        <div className="container mx-auto">
          <p>© {new Date().getFullYear()} CS2 Панель управления. Все права защищены.</p>
        </div>
      </footer>
    </div>
  );
} 
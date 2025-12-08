import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { GetServerSideProps } from 'next';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '../api/auth/[...nextauth]';
import axios from 'axios';
import Head from 'next/head';
import { Toaster, toast } from 'react-hot-toast';
import SteamLogin from '@/components/SteamLogin';
import CS2Bot from '@/components/CS2Bot';

interface AccountProps {
  account: {
    _id: string;
    username: string;
    status: string;
    casesCollected: number;
    lastLogin?: string;
    notes?: string;
    proxySetting?: string;
    steamGuardCode?: string;
    sharedSecret?: string;
    botStatus?: string;
    lastStart?: string;
    lastStop?: string;
  } | null;
}

export default function AccountPage({ account }: AccountProps) {
  const router = useRouter();
  const [steamStatus, setSteamStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Загрузка статуса Steam
  const fetchSteamStatus = async () => {
    if (!account) return;
    
    try {
      setLoading(true);
      const response = await axios.get(`/api/accounts/${account._id}/steam`);
      if (response.data.success) {
        setSteamStatus(response.data.data.status);
      }
    } catch (error) {
      console.error('Ошибка при получении статуса Steam:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSteamStatus();
    // Настройка интервала обновления
    const intervalId = setInterval(fetchSteamStatus, 30000);
    return () => clearInterval(intervalId);
  }, [account]);

  // Обработчик для успешного входа в Steam
  const handleSteamLoginSuccess = (status: any) => {
    setSteamStatus(status);
    fetchSteamStatus(); // Обновляем статус после входа
  };

  // Управление игрой CS2
  const handleStartGame = async () => {
    if (!account) return;
    
    try {
      setLoading(true);
      const response = await axios.post(`/api/accounts/${account._id}/steam`, {
        action: 'startGame'
      });
      
      if (response.data.success) {
        toast.success('CS2 запущен');
        fetchSteamStatus();
      } else {
        toast.error(response.data.message);
      }
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Ошибка при запуске CS2');
    } finally {
      setLoading(false);
    }
  };

  const handleStopGame = async () => {
    if (!account) return;
    
    try {
      setLoading(true);
      const response = await axios.post(`/api/accounts/${account._id}/steam`, {
        action: 'stopGame'
      });
      
      if (response.data.success) {
        toast.success('CS2 остановлен');
        fetchSteamStatus();
      } else {
        toast.error(response.data.message);
      }
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Ошибка при остановке CS2');
    } finally {
      setLoading(false);
    }
  };

  if (!account) {
    return <div className="p-4">Аккаунт не найден</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <Head>
        <title>Управление аккаунтом | {account.username}</title>
      </Head>
      
      <Toaster position="top-right" />
      
      <div className="mb-4">
        <button
          onClick={() => router.back()}
          className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
        >
          &larr; Назад
        </button>
      </div>
      
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-2xl font-bold mb-4">{account.username}</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Основная информация */}
          <div className="space-y-4">
            <div>
              <h2 className="text-xl font-semibold mb-2">Информация об аккаунте</h2>
              <div className="grid grid-cols-2 gap-2">
                <div className="font-medium">Статус:</div>
                <div>
                  <span className={`px-2 py-1 rounded text-sm ${
                    account.status === 'active' ? 'bg-green-100 text-green-800' :
                    account.status === 'banned' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {account.status === 'active' ? 'Активен' : 
                     account.status === 'banned' ? 'Заблокирован' : 'Неактивен'}
                  </span>
                </div>
                
                <div className="font-medium">Собрано кейсов:</div>
                <div>{account.casesCollected}</div>
                
                {account.lastLogin && (
                  <>
                    <div className="font-medium">Последний вход:</div>
                    <div>{new Date(account.lastLogin).toLocaleString()}</div>
                  </>
                )}
                
                {account.proxySetting && (
                  <>
                    <div className="font-medium">Прокси:</div>
                    <div>{account.proxySetting}</div>
                  </>
                )}
              </div>
            </div>
            
            {account.notes && (
              <div>
                <h3 className="font-medium mb-1">Заметки:</h3>
                <p className="text-gray-700 bg-gray-50 p-3 rounded">{account.notes}</p>
              </div>
            )}
          </div>
          
          {/* Steam интеграция */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold mb-2">Управление Steam</h2>
            
            {/* Статус Steam */}
            <div className="bg-gray-50 p-4 rounded">
              <h3 className="font-medium mb-2">Статус соединения:</h3>
              {loading ? (
                <div className="text-gray-500">Загрузка...</div>
              ) : steamStatus ? (
                <div>
                  <div className="flex items-center mb-2">
                    <div className={`w-3 h-3 rounded-full mr-2 ${steamStatus.isLoggedIn ? 'bg-green-500' : 'bg-gray-400'}`}></div>
                    <div>{steamStatus.isLoggedIn ? 'Подключено к Steam' : 'Не подключено к Steam'}</div>
                  </div>
                  
                  {steamStatus.steamId && (
                    <div className="text-sm text-gray-600">Steam ID: {steamStatus.steamId}</div>
                  )}
                  
                  {steamStatus.error && (
                    <div className="text-sm text-red-500 mt-1">Ошибка: {steamStatus.error}</div>
                  )}
                </div>
              ) : (
                <div className="text-gray-500">Нет данных о статусе Steam</div>
              )}
            </div>
            
            {/* Компонент для входа в Steam */}
            <SteamLogin 
              accountId={account._id} 
              onLoginSuccess={handleSteamLoginSuccess}
            />
            
            {/* Управление CS2 */}
            {steamStatus?.isLoggedIn && (
              <div className="mt-4">
                <h3 className="font-medium mb-2">Управление CS2:</h3>
                <div className="flex space-x-2">
                  <button
                    onClick={handleStartGame}
                    disabled={loading}
                    className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
                  >
                    Запустить CS2
                  </button>
                  
                  <button
                    onClick={handleStopGame}
                    disabled={loading}
                    className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50"
                  >
                    Остановить CS2
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
        
        {/* Компонент CS2Bot для управления ботом */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4">Фарм кейсов в CS2</h2>
          
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
            <p className="text-yellow-700">
              <strong>Внимание!</strong> Бот автоматически запустит CS2, присоединится к игре на карте Dust 2 и начнет имитировать игровой процесс для фарма кейсов. 
              Во время работы бота ваш компьютер будет занят, т.к. бот управляет клавиатурой и мышью.
            </p>
          </div>
          
          {/* Компонент CS2Bot */}
          <CS2Bot accountId={account._id} status={account.botStatus} />
          
          <div className="mt-4 text-sm text-gray-600">
            <p className="mb-2">Бот автоматически:</p>
            <ul className="list-disc pl-5 space-y-1">
              <li>Запускает CS2 и входит в игру на карте Dust 2 в режиме Deathmatch</li>
              <li>Имитирует движение и стрельбу для фарма кейсов</li>
              <li>Каждые 10 минут активной игры добавляет новый кейс</li>
            </ul>
            <p className="mt-2 text-red-500">
              <strong>Важно:</strong> Использование ботов может привести к блокировке аккаунта. Используйте на свой страх и риск.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  const session = await getServerSession(context.req, context.res, authOptions);
  
  // Проверка авторизации
  if (!session) {
    return {
      redirect: {
        destination: '/auth/login',
        permanent: false,
      },
    };
  }
  
  const { id } = context.params || {};
  
  try {
    // Получаем данные аккаунта
    const response = await axios.get(`${process.env.NEXTAUTH_URL}/api/accounts/${id}`, {
      headers: {
        Cookie: context.req.headers.cookie || '',
      },
    });
    
    if (response.data.success) {
      return {
        props: {
          account: response.data.account,
        },
      };
    } else {
      return {
        props: {
          account: null,
        },
      };
    }
  } catch (error) {
    console.error('Ошибка при получении данных аккаунта:', error);
    return {
      props: {
        account: null,
      },
    };
  }
}; 
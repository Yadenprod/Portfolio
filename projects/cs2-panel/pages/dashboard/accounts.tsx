import { useState, useEffect, ReactNode, Fragment } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import axios from 'axios';
import { toast } from 'react-hot-toast';
import { useSession } from 'next-auth/react';
import { Account } from '../../types/account';

// Компонент для карточки аккаунта
interface AccountCardProps {
  account: Account;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  onSteamLogin: (id: string) => void;
  onStartGame: (id: string) => void;
  onStopGame: (id: string) => void;
  onStartBot: (id: string) => void;
  onStopBot: (id: string) => void;
  isLogging?: boolean;
  isBusy?: boolean;
  isBotRunning?: boolean;
  key?: string; // Добавляем key как опциональное свойство
}

const AccountCard = ({ 
  account, 
  onEdit, 
  onDelete,
  onSteamLogin,
  onStartGame,
  onStopGame,
  onStartBot,
  onStopBot,
  isLogging = false,
  isBusy = false,
  isBotRunning = false
}: AccountCardProps) => {
  return (
    <div className="cs-card flex flex-col">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-bold">{account.username}</h3>
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
      </div>

      <div className="space-y-2 mb-4 text-sm text-gray-300">
        <div className="flex justify-between">
          <span>Собрано кейсов:</span>
          <span className="font-medium text-cs-orange">{account.casesCollected}</span>
        </div>
        <div className="flex justify-between">
          <span>Посл. вход:</span>
          <span>{account.lastLogin ? new Date(account.lastLogin).toLocaleDateString() : 'Никогда'}</span>
        </div>
        {account.notes && (
          <div className="pt-2 border-t border-gray-700">
            <p className="text-gray-400 italic">{account.notes}</p>
          </div>
        )}
      </div>

      <div className="grid grid-cols-2 gap-2 mb-2">
        <button 
          onClick={() => onSteamLogin(account._id)}
          disabled={isLogging || isBusy || account.status !== 'active'}
          className={`py-1.5 rounded text-sm flex items-center justify-center ${
            isLogging 
              ? 'bg-gray-700 text-gray-400' 
              : 'bg-cs-blue hover:bg-opacity-80'
          } ${account.status !== 'active' ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isLogging ? (
            <Fragment>
              <span className="animate-spin h-3 w-3 border-t-2 border-b-2 border-white rounded-full mr-1"></span> Вход...
            </Fragment>
          ) : (
            'Войти в Steam'
          )}
        </button>
        <button 
          onClick={() => onStartGame(account._id)}
          disabled={isLogging || isBusy || account.status !== 'active'}
          className={`py-1.5 rounded text-sm ${
            isBusy 
              ? 'bg-orange-700 hover:bg-orange-600' 
              : 'bg-green-700 hover:bg-green-600'
          } ${account.status !== 'active' ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isBusy ? 'Играет' : 'Запустить CS2'}
        </button>
        <button 
          onClick={() => onEdit(account._id)} 
          className="py-1.5 bg-cs-blue hover:bg-opacity-80 rounded text-sm"
        >
          Редактировать
        </button>
        <button 
          onClick={() => onDelete(account._id)} 
          className="py-1.5 bg-red-900 hover:bg-opacity-80 rounded text-sm"
        >
          Удалить
        </button>
        {isBusy && (
          <button 
            onClick={() => onStopGame(account._id)}
            className="py-1.5 bg-red-700 hover:bg-red-600 rounded text-sm col-span-2"
          >
            Остановить CS2
          </button>
        )}
        
        {/* Секция для управления ботом */}
        <div className="col-span-2 mt-3 pt-3 border-t border-gray-700">
          <h4 className="text-sm font-semibold mb-2 flex items-center">
            <svg className="w-4 h-4 mr-1 text-cs-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            Фарм кейсов (Бот CS2)
          </h4>
          
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={() => onStartBot(account._id)}
              disabled={isLogging || !isBusy || isBotRunning || account.status !== 'active'}
              className={`py-1.5 rounded text-sm ${
                isBotRunning ? 'bg-purple-700 cursor-not-allowed' : 'bg-purple-800 hover:bg-purple-700'
              } ${(isLogging || !isBusy || account.status !== 'active') ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {isBotRunning ? 'Бот запущен' : 'Запустить бота'}
            </button>
            
            <button
              onClick={() => onStopBot(account._id)}
              disabled={!isBotRunning}
              className={`py-1.5 rounded text-sm ${
                !isBotRunning ? 'bg-gray-700 cursor-not-allowed' : 'bg-red-800 hover:bg-red-700'
              }`}
            >
              Остановить бота
            </button>
          </div>
          
          <p className="text-xs text-gray-400 mt-2">
            {isBotRunning 
              ? 'Бот активен: фармит кейсы в CS2' 
              : 'Сначала войдите в Steam и запустите CS2, затем активируйте бота для фарма кейсов'}
          </p>
        </div>
      </div>
    </div>
  );
};

// Типы для формы аккаунта
interface AccountFormProps {
  account?: Account | null;
  onSave: (data: Partial<Account>) => void;
  onCancel: () => void;
}

interface AccountFormData {
  username: string;
  password: string;
  steamGuardCode: string;
  sharedSecret: string;
  status: 'active' | 'inactive' | 'banned';
  notes: string;
  proxySetting: string;
}

// Компонент формы для добавления/редактирования аккаунта
const AccountForm = ({ 
  account = null, 
  onSave, 
  onCancel 
}: AccountFormProps) => {
  const [formData, setFormData] = useState<AccountFormData>({
    username: account?.username || '',
    password: account?.password || '',
    steamGuardCode: account?.steamGuardCode || '',
    sharedSecret: account?.sharedSecret || '',
    status: account?.status || 'inactive',
    notes: account?.notes || '',
    proxySetting: account?.proxySetting || '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError(null); // Сбрасываем ошибку при изменении данных
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    onSave({
      ...formData,
      _id: account?._id,
    });
  };

  return (
    <div className="cs-card">
      <h2 className="text-xl font-bold mb-4">
        {account ? 'Редактировать аккаунт' : 'Добавить новый аккаунт'}
      </h2>
      
      {error && (
        <div className="bg-red-900 text-red-200 p-3 rounded-md mb-4">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Имя пользователя</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="cs-input w-full"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Пароль</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="cs-input w-full"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Код Steam Guard</label>
            <input
              type="text"
              name="steamGuardCode"
              value={formData.steamGuardCode}
              onChange={handleChange}
              className="cs-input w-full"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Shared Secret</label>
            <input
              type="text"
              name="sharedSecret"
              value={formData.sharedSecret}
              onChange={handleChange}
              className="cs-input w-full"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Статус</label>
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="cs-input w-full"
            >
              <option value="active">Активен</option>
              <option value="inactive">Неактивен</option>
              <option value="banned">Заблокирован</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Настройки прокси</label>
            <input
              type="text"
              name="proxySetting"
              value={formData.proxySetting}
              onChange={handleChange}
              className="cs-input w-full"
              placeholder="ip:port:login:password"
            />
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-1">Заметки</label>
          <textarea
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            className="cs-input w-full h-24 resize-none"
          />
        </div>
        
        <div className="flex space-x-4">
          <button
            type="submit"
            className="cs-button flex-1 flex items-center justify-center"
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <>
                <div className="animate-spin h-4 w-4 border-t-2 border-b-2 border-white rounded-full mr-2"></div>
                Сохранение...
              </>
            ) : (
              'Сохранить'
            )}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-800 text-gray-300 rounded-md flex-1 hover:bg-gray-700"
            disabled={isSubmitting}
          >
            Отмена
          </button>
        </div>
      </form>
    </div>
  );
};

// Основной компонент страницы
export default function Accounts() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAccountForm, setShowAccountForm] = useState(false);
  const [editingAccount, setEditingAccount] = useState<Account | null>(null);
  const [deletingAccountId, setDeletingAccountId] = useState<string | null>(null);
  const [showConfirmDelete, setShowConfirmDelete] = useState(false);
  const [loggingAccounts, setLoggingAccounts] = useState<string[]>([]);
  const [busyAccounts, setBusyAccounts] = useState<string[]>([]);
  const [botRunningAccounts, setBotRunningAccounts] = useState<string[]>([]);
  
  // Перенаправляем на страницу входа, только если статус явно unauthenticated
  // и не во время загрузки сессии
  useEffect(() => {
    if (status === 'unauthenticated') {
      router.replace('/login?callbackUrl=/dashboard/accounts');
    }
  }, [status, router]);

  // Функция получения списка аккаунтов
  const fetchAccounts = async () => {
    // Не делаем запрос, если статус загружается или пользователь не аутентифицирован
    if (status !== 'authenticated') return;

    try {
      setLoading(true);
      // Добавляем withCredentials: true для передачи cookies с сессией
      const response = await axios.get('/api/accounts', { withCredentials: true });
      
      if (response.data.success) {
        setAccounts(response.data.accounts || []);
      } else {
        toast.error(response.data.message || 'Ошибка при загрузке аккаунтов');
      }
    } catch (error) {
      console.error('Ошибка при загрузке аккаунтов:', error);
      toast.error('Не удалось загрузить список аккаунтов');
    } finally {
      setLoading(false);
    }
  };
  
  // Загрузка списка аккаунтов только когда сессия точно загружена и аутентифицирована
  useEffect(() => {
    fetchAccounts();
  }, [status]);

  const handleAddAccount = () => {
    setEditingAccount(null);
    setShowAccountForm(true);
  };

  const handleEditAccount = (id: string) => {
    const account = accounts.find(acc => acc._id === id);
    if (account) {
      setEditingAccount(account);
      setShowAccountForm(true);
    }
  };

  const handleDeleteAccount = (id: string) => {
    setDeletingAccountId(id);
    setShowConfirmDelete(true);
  };

  const confirmDeleteAccount = async () => {
    if (!deletingAccountId) return;
    
    try {
      const response = await axios.delete(`/api/accounts/${deletingAccountId}`, { withCredentials: true });
      
      if (response.data.success) {
        setAccounts(accounts.filter(acc => acc._id !== deletingAccountId));
        toast.success('Аккаунт успешно удален');
      } else {
        toast.error(response.data.message || 'Ошибка при удалении аккаунта');
      }
    } catch (error) {
      console.error('Ошибка при удалении аккаунта:', error);
      toast.error('Не удалось удалить аккаунт');
    } finally {
      setDeletingAccountId(null);
      setShowConfirmDelete(false);
    }
  };

  const handleSaveAccount = async (accountData: Partial<Account>) => {
    try {
      if (accountData._id) {
        // Обновляем существующий аккаунт
        console.log('Обновляем аккаунт:', accountData);
        const response = await axios.put(`/api/accounts/${accountData._id}`, accountData, { withCredentials: true });
        
        if (response.data.success) {
          setAccounts(accounts.map(acc => 
            acc._id === accountData._id ? { ...acc, ...response.data.account } : acc
          ));
          toast.success('Аккаунт успешно обновлен');
          setShowAccountForm(false);
          setEditingAccount(null);
        } else {
          console.error('Ошибка при обновлении аккаунта:', response.data);
          toast.error(response.data.message || 'Ошибка при обновлении аккаунта');
        }
      } else {
        // Добавляем новый аккаунт
        console.log('Добавляем новый аккаунт:', accountData);
        const response = await axios.post('/api/accounts', accountData, { withCredentials: true });
        
        if (response.data.success) {
          setAccounts([...accounts, response.data.accounts[0]]);
          toast.success('Аккаунт успешно добавлен');
          setShowAccountForm(false);
          setEditingAccount(null);
        } else {
          console.error('Ошибка при добавлении аккаунта:', response.data);
          toast.error(response.data.message || 'Ошибка при добавлении аккаунта');
        }
      }
    } catch (error: any) {
      console.error('Детали ошибки при сохранении аккаунта:', error);
      
      // Более детальная информация об ошибке
      if (error.response) {
        // Ответ получен, но статус не 2xx
        console.error('Данные ответа:', error.response.data);
        console.error('Статус:', error.response.status);
        console.error('Заголовки:', error.response.headers);
        toast.error(`Ошибка ${error.response.status}: ${error.response.data.message || 'Не удалось сохранить аккаунт'}`);
      } else if (error.request) {
        // Запрос был сделан, но ответ не получен
        console.error('Запрос без ответа:', error.request);
        toast.error('Сервер не отвечает. Проверьте соединение');
      } else {
        // Что-то другое вызвало ошибку
        console.error('Сообщение об ошибке:', error.message);
        toast.error(`Ошибка: ${error.message}`);
      }
    }
  };

  // Функция входа в Steam
  const handleSteamLogin = async (id: string) => {
    try {
      setLoggingAccounts(prev => [...prev, id]);
      const response = await axios.post(`/api/accounts/${id}/steam`, {
        action: 'login'
      }, { withCredentials: true });
      
      if (response.data.success) {
        toast.success('Вход в Steam выполнен');
        // Обновляем список аккаунтов, чтобы показать последнее время входа
        fetchAccounts();
      } else {
        toast.error(response.data.message || 'Ошибка при входе в Steam');
      }
    } catch (error: any) {
      console.error('Ошибка при входе в Steam:', error);
      toast.error(error.response?.data?.message || 'Не удалось войти в Steam');
    } finally {
      setLoggingAccounts(prev => prev.filter(accountId => accountId !== id));
    }
  };

  // Функция запуска CS2
  const handleStartGame = async (id: string) => {
    try {
      const response = await axios.post(`/api/accounts/${id}/steam`, {
        action: 'startGame'
      }, { withCredentials: true });
      
      if (response.data.success) {
        toast.success('CS2 запущен');
        setBusyAccounts(prev => [...prev, id]);
      } else {
        toast.error(response.data.message || 'Ошибка при запуске CS2');
      }
    } catch (error: any) {
      console.error('Ошибка при запуске CS2:', error);
      toast.error(error.response?.data?.message || 'Не удалось запустить CS2');
    }
  };

  // Функция остановки CS2
  const handleStopGame = async (id: string) => {
    try {
      const response = await axios.post(`/api/accounts/${id}/steam`, {
        action: 'stopGame'
      }, { withCredentials: true });
      
      if (response.data.success) {
        toast.success('CS2 остановлен');
        setBusyAccounts(prev => prev.filter(accountId => accountId !== id));
      } else {
        toast.error(response.data.message || 'Ошибка при остановке CS2');
      }
    } catch (error: any) {
      console.error('Ошибка при остановке CS2:', error);
      toast.error(error.response?.data?.message || 'Не удалось остановить CS2');
    }
  };

  const handleStartBot = async (id: string) => {
    try {
      // Проверяем, что аккаунт существует и не занят уже
      if (!busyAccounts.includes(id) || botRunningAccounts.includes(id)) {
        toast.error('Перед запуском бота необходимо запустить CS2');
        return;
      }

      console.log(`Запуск бота для аккаунта: ${id}`);
      
      const response = await axios.post('/api/bot', {
        accountId: id,
        action: 'start'
      });

      if (response.data.success) {
        setBotRunningAccounts(prev => [...prev, id]);
        toast.success('Бот запущен успешно');
        console.log('Ответ сервера:', response.data);
      } else {
        toast.error(response.data.message || 'Не удалось запустить бота');
        console.error('Ошибка запуска бота:', response.data);
      }
    } catch (error: any) {
      console.error('Ошибка при запуске бота:', error);
      const errorMessage = error.response?.data?.message || 'Не удалось запустить бота';
      console.error('Детали ошибки:', errorMessage);
      toast.error(errorMessage);
    }
  };

  const handleStopBot = async (id: string) => {
    try {
      if (!botRunningAccounts.includes(id)) {
        toast.error('Бот не запущен');
        return;
      }

      const response = await axios.post('/api/bot', {
        accountId: id,
        action: 'stop'
      });

      if (response.data.success) {
        setBotRunningAccounts(prev => prev.filter(accId => accId !== id));
        toast.success('Бот остановлен');
      } else {
        toast.error(response.data.message || 'Не удалось остановить бота');
      }
    } catch (error: any) {
      console.error('Ошибка при остановке бота:', error);
      toast.error(error.response?.data?.message || 'Не удалось остановить бота');
    }
  };

  const checkBotsStatus = async () => {
    try {
      // Проверяем статус ботов, только если есть запущенные боты
      if (botRunningAccounts.length === 0) return;

      for (const accountId of botRunningAccounts) {
        const response = await axios.post('/api/bot', {
          accountId,
          action: 'status'
        });

        // Если бот не запущен (статус не running), удаляем из списка запущенных
        if (response.data.success && response.data.data.status !== 'running') {
          setBotRunningAccounts(prev => prev.filter(id => id !== accountId));
        }
      }
    } catch (error) {
      console.error('Ошибка при проверке статуса ботов:', error);
    }
  };

  // Дополняем метод проверки статуса аккаунтов
  const checkAccountsStatus = async () => {
    // Существующая проверка статуса игры
    try {
      for (const accountId of busyAccounts) {
        const response = await axios.get(`/api/accounts/${accountId}/steam`);
        if (response.data.success && !response.data.data.status.isPlayingCS2) {
          setBusyAccounts(prev => prev.filter(id => id !== accountId));
        }
      }
      
      // Добавляем проверку ботов
      await checkBotsStatus();
    } catch (error) {
      console.error('Ошибка при проверке статуса аккаунтов:', error);
    }
  };

  // Загрузка аккаунтов при монтировании компонента
  useEffect(() => {
    fetchAccounts();
    const interval = setInterval(checkAccountsStatus, 30000); // Проверяем статус каждые 30 секунд
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <Head>
        <title>Управление аккаунтами | CS2 Панель</title>
        <meta name="description" content="Управление аккаунтами CS2" />
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
                <Link href="/dashboard/accounts" className="text-cs-orange font-medium">
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
          </nav>
        </div>
      </header>

      <main className="flex-grow container mx-auto p-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Управление аккаунтами</h1>
          
          {!showAccountForm && (
            <button
              onClick={handleAddAccount}
              className="cs-button flex items-center"
            >
              <span className="mr-1">+</span> Добавить аккаунт
            </button>
          )}
        </div>

        {loading ? (
          <div className="cs-card flex items-center justify-center p-8">
            <div className="animate-spin h-8 w-8 border-t-2 border-b-2 border-cs-orange rounded-full"></div>
            <span className="ml-3">Загрузка аккаунтов...</span>
          </div>
        ) : showAccountForm ? (
          <AccountForm 
            account={editingAccount} 
            onSave={handleSaveAccount} 
            onCancel={() => {
              setShowAccountForm(false);
              setEditingAccount(null);
            }} 
          />
        ) : accounts.length === 0 ? (
          <div className="cs-card p-6 text-center">
            <p className="text-gray-400 mb-4">У вас пока нет добавленных аккаунтов</p>
            <button 
              onClick={handleAddAccount}
              className="cs-button"
            >
              Добавить первый аккаунт
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {accounts.map(account => (
              <AccountCard
                key={account._id}
                account={account}
                onEdit={handleEditAccount}
                onDelete={handleDeleteAccount}
                onSteamLogin={handleSteamLogin}
                onStartGame={handleStartGame}
                onStopGame={handleStopGame}
                onStartBot={handleStartBot}
                onStopBot={handleStopBot}
                isLogging={loggingAccounts.includes(account._id)}
                isBusy={busyAccounts.includes(account._id)}
                isBotRunning={botRunningAccounts.includes(account._id)}
              />
            ))}
          </div>
        )}
      </main>

      {showConfirmDelete && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
          <div className="bg-cs-dark-blue border border-gray-700 rounded-lg p-6 max-w-md w-full">
            <h3 className="text-lg font-semibold mb-4">Подтверждение удаления</h3>
            <p className="mb-6">Вы уверены, что хотите удалить этот аккаунт? Это действие нельзя отменить.</p>
            <div className="flex justify-end space-x-3">
              <button 
                onClick={() => setShowConfirmDelete(false)}
                className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded"
              >
                Отмена
              </button>
              <button 
                onClick={confirmDeleteAccount}
                className="px-4 py-2 bg-red-700 hover:bg-red-600 rounded"
              >
                Удалить
              </button>
            </div>
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
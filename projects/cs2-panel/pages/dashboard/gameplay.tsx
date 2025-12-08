import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { FaPlay, FaStop, FaCog, FaGamepad } from 'react-icons/fa';

// Компонент активной автоматизации
const ActiveGameplay = ({ 
  account,
  automationSettings,
  onStop
}: { 
  account: any,
  automationSettings: any,
  onStop: (id: string) => void
}) => {
  const [status, setStatus] = useState('playing');
  const [currentMap, setCurrentMap] = useState<string>('dust2');
  const [playTime, setPlayTime] = useState<number>(0);
  const [experienceGained, setExperienceGained] = useState<number>(0);
  
  // Имитация игрового процесса
  useEffect(() => {
    if (!automationSettings.isActive) return;
    
    const interval = setInterval(() => {
      // Имитация статусов игры: поиск игры -> игра -> поиск новой игры
      if (status === 'searching') {
        setStatus('playing');
        // Выбор случайной карты из предпочтений
        const maps = ['dust2', 'mirage', 'inferno', 'nuke', 'overpass', 'vertigo', 'ancient', 'anubis'];
        const preferredMap = automationSettings.mapPreference === 'any' 
          ? maps[Math.floor(Math.random() * maps.length)]
          : automationSettings.mapPreference;
        setCurrentMap(preferredMap);
      } else if (Math.random() < 0.05) { // 5% шанс завершения игры
        setStatus('searching');
      }
      
      // Увеличение времени игры и опыта
      setPlayTime(prev => prev + 10);
      const xpGain = Math.floor(Math.random() * 10) + 1;
      setExperienceGained(prev => prev + xpGain);
    }, 2000);
    
    return () => clearInterval(interval);
  }, [status, automationSettings.isActive, automationSettings.mapPreference]);
  
  // Форматирование времени в часы:минуты:секунды
  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };
  
  // Форматирование даты до следующего кейса
  const formatNextCase = (date: string) => {
    const dropDate = new Date(date);
    const now = new Date();
    const diffTime = Math.abs(dropDate.getTime() - now.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return `${diffDays} ${diffDays === 1 ? 'день' : diffDays < 5 ? 'дня' : 'дней'}`;
  };
  
  return (
    <div className="cs-card">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-bold">{account.username}</h3>
          <p className="text-sm text-gray-400">Уровень: {automationSettings.currentLevel}</p>
        </div>
        <span className="px-2 py-1 rounded-full text-xs bg-green-900 text-green-300">
          Активен
        </span>
      </div>
      
      <div className="mb-4 space-y-3">
        <div className="bg-cs-dark-2 p-3 rounded-md">
          <div className="flex justify-between text-sm mb-1">
            <span>Статус:</span>
            <span className="font-medium text-cs-orange">
              {status === 'playing' ? 'Играет на ' + currentMap : 'Поиск игры...'}
            </span>
          </div>
          
          <div className="flex justify-between text-sm mb-1">
            <span>Время игры:</span>
            <span>{formatTime(playTime)}</span>
          </div>
          
          <div className="flex justify-between text-sm mb-1">
            <span>Опыт за сессию:</span>
            <span>+{experienceGained} XP</span>
          </div>
          
          <div className="flex justify-between text-sm">
            <span>Следующий кейс через:</span>
            <span>{formatNextCase(automationSettings.nextCaseDropEstimate)}</span>
          </div>
        </div>
        
        <div className="flex justify-between text-sm">
          <span>Всего опыта:</span>
          <span className="font-medium text-cs-orange">
            {automationSettings.experienceGained} XP
          </span>
        </div>
        
        <div className="flex justify-between text-sm">
          <span>Предпочитаемая карта:</span>
          <span>
            {automationSettings.mapPreference === 'any' ? 'Любая' : automationSettings.mapPreference}
          </span>
        </div>
        
        <div className="flex justify-between text-sm">
          <span>Часов фарма в день:</span>
          <span>{automationSettings.farmingHoursPerDay}</span>
        </div>
      </div>
      
      <div className="flex space-x-2">
        <button 
          onClick={() => onStop(automationSettings._id)} 
          className="flex-1 py-1.5 bg-red-900 hover:bg-opacity-80 rounded text-sm flex items-center justify-center"
        >
          <FaStop className="mr-1" /> Остановить
        </button>
      </div>
    </div>
  );
};

// Компонент формы настроек автоматизации
const GameplaySettings = ({ 
  account, 
  automationSettings = null,
  onSave, 
  onCancel 
}: { 
  account: any, 
  automationSettings?: any,
  onSave: (data: any) => void, 
  onCancel: () => void 
}) => {
  const [formData, setFormData] = useState({
    mapPreference: automationSettings?.mapPreference || 'any',
    autoJoinDeathmatch: automationSettings?.autoJoinDeathmatch ?? true,
    farmingHoursPerDay: automationSettings?.farmingHoursPerDay || 6,
    autoReconnect: automationSettings?.autoReconnect ?? true,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const newValue = type === 'checkbox' 
      ? (e.target as HTMLInputElement).checked 
      : name === 'farmingHoursPerDay' 
        ? parseInt(value) 
        : value;
        
    setFormData(prev => ({ ...prev, [name]: newValue }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({
      accountId: account._id,
      ...formData,
      isActive: true
    });
  };

  return (
    <div className="cs-card">
      <h2 className="text-xl font-bold mb-4">
        Настройки автоматизации для {account.username}
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Предпочитаемая карта</label>
          <select
            name="mapPreference"
            value={formData.mapPreference}
            onChange={handleChange}
            className="cs-input w-full"
          >
            <option value="any">Любая</option>
            <option value="dust2">Dust II</option>
            <option value="mirage">Mirage</option>
            <option value="inferno">Inferno</option>
            <option value="nuke">Nuke</option>
            <option value="overpass">Overpass</option>
            <option value="vertigo">Vertigo</option>
            <option value="ancient">Ancient</option>
            <option value="anubis">Anubis</option>
          </select>
        </div>
        
        <div className="flex items-center">
          <input
            type="checkbox"
            id="autoJoinDeathmatch"
            name="autoJoinDeathmatch"
            checked={formData.autoJoinDeathmatch}
            onChange={handleChange}
            className="rounded text-cs-orange"
          />
          <label htmlFor="autoJoinDeathmatch" className="ml-2 text-sm">
            Автоматически присоединяться к дезматчу
          </label>
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-1">
            Часов фарма в день (1-24)
          </label>
          <input
            type="number"
            name="farmingHoursPerDay"
            value={formData.farmingHoursPerDay}
            onChange={handleChange}
            min="1"
            max="24"
            className="cs-input w-full"
          />
        </div>
        
        <div className="flex items-center">
          <input
            type="checkbox"
            id="autoReconnect"
            name="autoReconnect"
            checked={formData.autoReconnect}
            onChange={handleChange}
            className="rounded text-cs-orange"
          />
          <label htmlFor="autoReconnect" className="ml-2 text-sm">
            Автоматически переподключаться при разрыве соединения
          </label>
        </div>
        
        <div className="flex space-x-4">
          <button
            type="submit"
            className="cs-button flex-1 flex items-center justify-center"
          >
            <FaPlay className="mr-1" /> Запустить автоматизацию
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-800 text-gray-300 rounded-md flex-1 hover:bg-gray-700"
          >
            Отмена
          </button>
        </div>
      </form>
    </div>
  );
};

// Основной компонент страницы
export default function Gameplay() {
  const [accounts, setAccounts] = useState<any[]>([]);
  const [automationSettings, setAutomationSettings] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showSelector, setShowSelector] = useState(false);
  const [selectedAccount, setSelectedAccount] = useState<any>(null);
  
  // Имитация загрузки данных
  useEffect(() => {
    // Тестовые данные аккаунтов
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
        status: 'active',
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
    
    // Тестовые данные настроек автоматизации
    const mockAutomation = [
      {
        _id: 'a1',
        accountId: '1',
        isActive: true,
        mapPreference: 'dust2',
        autoJoinDeathmatch: true,
        farmingHoursPerDay: 8,
        autoReconnect: true,
        lastGameActivity: new Date(),
        experienceGained: 12450,
        currentLevel: 3,
        nextCaseDropEstimate: new Date(new Date().setDate(new Date().getDate() + 3))
      }
    ];
    
    setTimeout(() => {
      setAccounts(mockAccounts);
      setAutomationSettings(mockAutomation);
      setIsLoading(false);
    }, 800);
  }, []);
  
  // Получение аккаунтов без активной автоматизации
  const getAvailableAccounts = () => {
    const activeAccountIds = automationSettings
      .filter(setting => setting.isActive)
      .map(setting => setting.accountId);
    
    return accounts.filter(acc => 
      acc.status === 'active' && !activeAccountIds.includes(acc._id)
    );
  };
  
  // Получение аккаунтов с активной автоматизацией
  const getActiveAutomationAccounts = () => {
    const result = [];
    
    for (const setting of automationSettings.filter(s => s.isActive)) {
      const account = accounts.find(acc => acc._id === setting.accountId);
      if (account) {
        result.push({
          account,
          automationSettings: setting
        });
      }
    }
    
    return result;
  };
  
  const handleStartSetup = (account: any) => {
    setSelectedAccount(account);
    setShowSelector(false);
  };
  
  const handleSaveSettings = (data: any) => {
    // В реальном приложении здесь был бы API-запрос
    const newSettings = {
      _id: `a${Date.now()}`,
      ...data,
      lastGameActivity: new Date(),
      experienceGained: 0,
      currentLevel: 1,
      nextCaseDropEstimate: new Date(new Date().setDate(new Date().getDate() + 7))
    };
    
    setAutomationSettings([...automationSettings, newSettings]);
    setSelectedAccount(null);
  };
  
  const handleStopAutomation = (id: string) => {
    // В реальном приложении здесь был бы API-запрос
    setAutomationSettings(automationSettings.map(setting =>
      setting._id === id ? { ...setting, isActive: false } : setting
    ));
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Head>
        <title>Автоматизация геймплея | CS2 Панель</title>
        <meta name="description" content="Автоматизация геймплея CS2" />
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
                <Link href="/dashboard/cases" className="text-gray-300 hover:text-white">
                  Кейсы
                </Link>
              </li>
              <li>
                <Link href="/dashboard/gameplay" className="text-cs-orange font-medium">
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
          <h1 className="text-2xl font-bold">Автоматизация геймплея</h1>
          
          {!showSelector && !selectedAccount && getAvailableAccounts().length > 0 && (
            <button
              onClick={() => setShowSelector(true)}
              className="cs-button flex items-center"
            >
              <FaPlay className="mr-1" /> Запустить автоматизацию
            </button>
          )}
        </div>
        
        <div className="mb-6">
          <div className="bg-yellow-900 bg-opacity-30 border border-yellow-800 text-yellow-200 p-4 rounded-md mb-6">
            <h3 className="font-bold mb-1">Информация о функции</h3>
            <p className="text-sm">
              Эта функция позволяет автоматически запускать аккаунты CS2 в режим дезматч 
              для накопления опыта и получения еженедельных кейсов. Система будет 
              автоматически подключаться к играм, играть на выбранных картах и 
              получать опыт, который приводит к повышению уровня и выпадению кейсов.
            </p>
          </div>
        </div>

        {isLoading ? (
          <div className="text-center py-10">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-cs-orange mb-2"></div>
            <p>Загрузка данных...</p>
          </div>
        ) : selectedAccount ? (
          <GameplaySettings 
            account={selectedAccount}
            onSave={handleSaveSettings}
            onCancel={() => setSelectedAccount(null)}
          />
        ) : showSelector ? (
          <div className="cs-card mb-6">
            <h2 className="text-xl font-bold mb-4">Выберите аккаунт для автоматизации</h2>
            
            {getAvailableAccounts().length > 0 ? (
              <div className="space-y-3">
                {getAvailableAccounts().map(account => (
                  <div 
                    key={account._id}
                    className="flex justify-between items-center p-3 border border-gray-700 rounded-md hover:border-cs-orange cursor-pointer"
                    onClick={() => handleStartSetup(account)}
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
              <p className="text-gray-400">Нет доступных аккаунтов для автоматизации</p>
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
          <h2 className="text-xl font-bold mb-4">Активная автоматизация</h2>
          
          {getActiveAutomationAccounts().length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {getActiveAutomationAccounts().map(({ account, automationSettings }) => (
                <ActiveGameplay
                  key={automationSettings._id}
                  account={account}
                  automationSettings={automationSettings}
                  onStop={handleStopAutomation}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-8 cs-card">
              <p className="text-gray-400 mb-4">У вас нет аккаунтов с активной автоматизацией геймплея</p>
              {getAvailableAccounts().length > 0 && (
                <button
                  onClick={() => setShowSelector(true)}
                  className="cs-button flex items-center justify-center"
                >
                  <FaPlay className="mr-1" /> Запустить автоматизацию
                </button>
              )}
            </div>
          )}
        </div>
        
        <div>
          <h2 className="text-xl font-bold mb-4">Статистика автоматизации</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="cs-card">
              <h3 className="text-lg font-medium mb-1">Активных аккаунтов</h3>
              <p className="text-3xl font-bold text-cs-orange">
                {getActiveAutomationAccounts().length}
              </p>
            </div>
            <div className="cs-card">
              <h3 className="text-lg font-medium mb-1">Всего опыта</h3>
              <p className="text-3xl font-bold text-cs-orange">
                {automationSettings.reduce((sum, setting) => sum + setting.experienceGained, 0)} XP
              </p>
            </div>
            <div className="cs-card">
              <h3 className="text-lg font-medium mb-1">Собрано кейсов</h3>
              <p className="text-3xl font-bold text-cs-orange">
                {accounts.reduce((sum, acc) => sum + acc.casesCollected, 0)}
              </p>
            </div>
            <div className="cs-card">
              <h3 className="text-lg font-medium mb-1">Ожидается кейсов</h3>
              <p className="text-3xl font-bold text-cs-orange">
                {getActiveAutomationAccounts().length}
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
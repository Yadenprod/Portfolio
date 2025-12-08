import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';

export default function Settings() {
  const [generalSettings, setGeneralSettings] = useState({
    autoLogin: true,
    proxiesEnabled: false,
    caseCollectionEnabled: true,
    useCustomSteamPath: false,
    customSteamPath: 'C:\\Program Files (x86)\\Steam\\steam.exe',
    maxConcurrentAccounts: 5,
    logLevel: 'info',
  });
  
  const [notificationSettings, setNotificationSettings] = useState({
    emailNotifications: true,
    telegramNotifications: false,
    telegramBotToken: '',
    telegramChatId: '',
    notifyOnCaseCollected: true,
    notifyOnBan: true,
    notifyOnLogin: false,
  });
  
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  
  const handleGeneralChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target as HTMLInputElement;
    
    setGeneralSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : 
              type === 'number' ? parseInt(value) : value
    }));
  };
  
  const handleNotificationChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    
    setNotificationSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };
  
  const handleSaveSettings = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    
    // Имитация сохранения настроек
    setTimeout(() => {
      setIsSaving(false);
      setSaveSuccess(true);
      
      // Скрыть сообщение об успехе через 3 секунды
      setTimeout(() => setSaveSuccess(false), 3000);
    }, 800);
  };
  
  const resetSettings = () => {
    if (confirm('Вы уверены, что хотите сбросить все настройки до значений по умолчанию?')) {
      setGeneralSettings({
        autoLogin: true,
        proxiesEnabled: false,
        caseCollectionEnabled: true,
        useCustomSteamPath: false,
        customSteamPath: 'C:\\Program Files (x86)\\Steam\\steam.exe',
        maxConcurrentAccounts: 5,
        logLevel: 'info',
      });
      
      setNotificationSettings({
        emailNotifications: true,
        telegramNotifications: false,
        telegramBotToken: '',
        telegramChatId: '',
        notifyOnCaseCollected: true,
        notifyOnBan: true,
        notifyOnLogin: false,
      });
    }
  };
  
  return (
    <div className="min-h-screen flex flex-col">
      <Head>
        <title>Настройки | CS2 Панель</title>
        <meta name="description" content="Настройки CS2 панели управления" />
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
                <Link href="/dashboard/gameplay" className="text-gray-300 hover:text-white">
                  Геймплей
                </Link>
              </li>
              <li>
                <Link href="/dashboard/settings" className="text-cs-orange font-medium">
                  Настройки
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      <main className="flex-grow container mx-auto p-4">
        <div className="mb-6">
          <h1 className="text-2xl font-bold">Настройки панели</h1>
          <p className="text-gray-400">Настройте параметры работы панели управления CS2</p>
        </div>
        
        {saveSuccess && (
          <div className="bg-green-900 bg-opacity-50 border border-green-800 rounded-md p-3 mb-6 flex justify-between items-center">
            <p className="text-green-300">Настройки успешно сохранены</p>
            <button 
              onClick={() => setSaveSuccess(false)}
              className="text-green-300 hover:text-white"
            >
              ✕
            </button>
          </div>
        )}

        <form onSubmit={handleSaveSettings} className="space-y-8">
          <div className="cs-card">
            <h2 className="text-xl font-bold mb-4">Общие настройки</h2>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <label htmlFor="autoLogin" className="block font-medium">Автоматический вход</label>
                  <p className="text-sm text-gray-400">Автоматически входить в аккаунты при запуске фарма</p>
                </div>
                <div className="relative inline-block w-12 h-6">
                  <input
                    type="checkbox"
                    id="autoLogin"
                    name="autoLogin"
                    className="absolute w-0 h-0 opacity-0"
                    checked={generalSettings.autoLogin}
                    onChange={handleGeneralChange}
                  />
                  <label
                    htmlFor="autoLogin"
                    className={`block overflow-hidden h-6 rounded-full cursor-pointer transition-colors duration-200 ${
                      generalSettings.autoLogin ? 'bg-cs-orange' : 'bg-gray-700'
                    }`}
                  >
                    <span
                      className={`block h-6 w-6 rounded-full bg-white transform transition-transform duration-200 ${
                        generalSettings.autoLogin ? 'translate-x-6' : 'translate-x-0'
                      }`}
                    ></span>
                  </label>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <label htmlFor="proxiesEnabled" className="block font-medium">Использовать прокси</label>
                  <p className="text-sm text-gray-400">Использовать прокси для каждого аккаунта</p>
                </div>
                <div className="relative inline-block w-12 h-6">
                  <input
                    type="checkbox"
                    id="proxiesEnabled"
                    name="proxiesEnabled"
                    className="absolute w-0 h-0 opacity-0"
                    checked={generalSettings.proxiesEnabled}
                    onChange={handleGeneralChange}
                  />
                  <label
                    htmlFor="proxiesEnabled"
                    className={`block overflow-hidden h-6 rounded-full cursor-pointer transition-colors duration-200 ${
                      generalSettings.proxiesEnabled ? 'bg-cs-orange' : 'bg-gray-700'
                    }`}
                  >
                    <span
                      className={`block h-6 w-6 rounded-full bg-white transform transition-transform duration-200 ${
                        generalSettings.proxiesEnabled ? 'translate-x-6' : 'translate-x-0'
                      }`}
                    ></span>
                  </label>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <label htmlFor="caseCollectionEnabled" className="block font-medium">Сбор кейсов</label>
                  <p className="text-sm text-gray-400">Включить автоматический сбор кейсов</p>
                </div>
                <div className="relative inline-block w-12 h-6">
                  <input
                    type="checkbox"
                    id="caseCollectionEnabled"
                    name="caseCollectionEnabled"
                    className="absolute w-0 h-0 opacity-0"
                    checked={generalSettings.caseCollectionEnabled}
                    onChange={handleGeneralChange}
                  />
                  <label
                    htmlFor="caseCollectionEnabled"
                    className={`block overflow-hidden h-6 rounded-full cursor-pointer transition-colors duration-200 ${
                      generalSettings.caseCollectionEnabled ? 'bg-cs-orange' : 'bg-gray-700'
                    }`}
                  >
                    <span
                      className={`block h-6 w-6 rounded-full bg-white transform transition-transform duration-200 ${
                        generalSettings.caseCollectionEnabled ? 'translate-x-6' : 'translate-x-0'
                      }`}
                    ></span>
                  </label>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <label htmlFor="useCustomSteamPath" className="block font-medium">Пользовательский путь Steam</label>
                  <p className="text-sm text-gray-400">Использовать нестандартный путь к Steam.exe</p>
                </div>
                <div className="relative inline-block w-12 h-6">
                  <input
                    type="checkbox"
                    id="useCustomSteamPath"
                    name="useCustomSteamPath"
                    className="absolute w-0 h-0 opacity-0"
                    checked={generalSettings.useCustomSteamPath}
                    onChange={handleGeneralChange}
                  />
                  <label
                    htmlFor="useCustomSteamPath"
                    className={`block overflow-hidden h-6 rounded-full cursor-pointer transition-colors duration-200 ${
                      generalSettings.useCustomSteamPath ? 'bg-cs-orange' : 'bg-gray-700'
                    }`}
                  >
                    <span
                      className={`block h-6 w-6 rounded-full bg-white transform transition-transform duration-200 ${
                        generalSettings.useCustomSteamPath ? 'translate-x-6' : 'translate-x-0'
                      }`}
                    ></span>
                  </label>
                </div>
              </div>
              
              {generalSettings.useCustomSteamPath && (
                <div>
                  <label htmlFor="customSteamPath" className="block text-sm font-medium mb-1">Путь к Steam</label>
                  <input
                    type="text"
                    id="customSteamPath"
                    name="customSteamPath"
                    value={generalSettings.customSteamPath}
                    onChange={handleGeneralChange}
                    className="cs-input w-full"
                  />
                </div>
              )}
              
              <div>
                <label htmlFor="maxConcurrentAccounts" className="block text-sm font-medium mb-1">
                  Максимум одновременных аккаунтов
                </label>
                <input
                  type="number"
                  id="maxConcurrentAccounts"
                  name="maxConcurrentAccounts"
                  value={generalSettings.maxConcurrentAccounts}
                  onChange={handleGeneralChange}
                  min="1"
                  max="20"
                  className="cs-input w-full max-w-xs"
                />
              </div>
              
              <div>
                <label htmlFor="logLevel" className="block text-sm font-medium mb-1">Уровень логирования</label>
                <select
                  id="logLevel"
                  name="logLevel"
                  value={generalSettings.logLevel}
                  onChange={handleGeneralChange}
                  className="cs-input w-full max-w-xs"
                >
                  <option value="error">Только ошибки</option>
                  <option value="warn">Предупреждения</option>
                  <option value="info">Информационный</option>
                  <option value="debug">Отладка</option>
                </select>
              </div>
            </div>
          </div>
          
          <div className="cs-card">
            <h2 className="text-xl font-bold mb-4">Уведомления</h2>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <label htmlFor="emailNotifications" className="block font-medium">Email уведомления</label>
                  <p className="text-sm text-gray-400">Получать уведомления на email</p>
                </div>
                <div className="relative inline-block w-12 h-6">
                  <input
                    type="checkbox"
                    id="emailNotifications"
                    name="emailNotifications"
                    className="absolute w-0 h-0 opacity-0"
                    checked={notificationSettings.emailNotifications}
                    onChange={handleNotificationChange}
                  />
                  <label
                    htmlFor="emailNotifications"
                    className={`block overflow-hidden h-6 rounded-full cursor-pointer transition-colors duration-200 ${
                      notificationSettings.emailNotifications ? 'bg-cs-orange' : 'bg-gray-700'
                    }`}
                  >
                    <span
                      className={`block h-6 w-6 rounded-full bg-white transform transition-transform duration-200 ${
                        notificationSettings.emailNotifications ? 'translate-x-6' : 'translate-x-0'
                      }`}
                    ></span>
                  </label>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <label htmlFor="telegramNotifications" className="block font-medium">Telegram уведомления</label>
                  <p className="text-sm text-gray-400">Получать уведомления в Telegram</p>
                </div>
                <div className="relative inline-block w-12 h-6">
                  <input
                    type="checkbox"
                    id="telegramNotifications"
                    name="telegramNotifications"
                    className="absolute w-0 h-0 opacity-0"
                    checked={notificationSettings.telegramNotifications}
                    onChange={handleNotificationChange}
                  />
                  <label
                    htmlFor="telegramNotifications"
                    className={`block overflow-hidden h-6 rounded-full cursor-pointer transition-colors duration-200 ${
                      notificationSettings.telegramNotifications ? 'bg-cs-orange' : 'bg-gray-700'
                    }`}
                  >
                    <span
                      className={`block h-6 w-6 rounded-full bg-white transform transition-transform duration-200 ${
                        notificationSettings.telegramNotifications ? 'translate-x-6' : 'translate-x-0'
                      }`}
                    ></span>
                  </label>
                </div>
              </div>
              
              {notificationSettings.telegramNotifications && (
                <div className="space-y-3">
                  <div>
                    <label htmlFor="telegramBotToken" className="block text-sm font-medium mb-1">Токен Telegram бота</label>
                    <input
                      type="text"
                      id="telegramBotToken"
                      name="telegramBotToken"
                      value={notificationSettings.telegramBotToken}
                      onChange={handleNotificationChange}
                      className="cs-input w-full"
                      placeholder="1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    />
                  </div>
                  <div>
                    <label htmlFor="telegramChatId" className="block text-sm font-medium mb-1">ID чата Telegram</label>
                    <input
                      type="text"
                      id="telegramChatId"
                      name="telegramChatId"
                      value={notificationSettings.telegramChatId}
                      onChange={handleNotificationChange}
                      className="cs-input w-full"
                      placeholder="12345678"
                    />
                  </div>
                </div>
              )}
              
              <div className="pt-3 border-t border-gray-700">
                <p className="font-medium mb-2">Типы уведомлений</p>
                
                <div className="space-y-2">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="notifyOnCaseCollected"
                      name="notifyOnCaseCollected"
                      checked={notificationSettings.notifyOnCaseCollected}
                      onChange={handleNotificationChange}
                      className="mr-2 h-4 w-4 rounded border-gray-600 bg-gray-800 text-cs-orange focus:ring-0 focus:ring-offset-0"
                    />
                    <label htmlFor="notifyOnCaseCollected">Уведомлять при получении кейса</label>
                  </div>
                  
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="notifyOnBan"
                      name="notifyOnBan"
                      checked={notificationSettings.notifyOnBan}
                      onChange={handleNotificationChange}
                      className="mr-2 h-4 w-4 rounded border-gray-600 bg-gray-800 text-cs-orange focus:ring-0 focus:ring-offset-0"
                    />
                    <label htmlFor="notifyOnBan">Уведомлять при бане аккаунта</label>
                  </div>
                  
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="notifyOnLogin"
                      name="notifyOnLogin"
                      checked={notificationSettings.notifyOnLogin}
                      onChange={handleNotificationChange}
                      className="mr-2 h-4 w-4 rounded border-gray-600 bg-gray-800 text-cs-orange focus:ring-0 focus:ring-offset-0"
                    />
                    <label htmlFor="notifyOnLogin">Уведомлять при входе в аккаунт</label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="flex justify-between">
            <button
              type="button"
              onClick={resetSettings}
              className="px-4 py-2 bg-gray-800 text-gray-300 rounded-md hover:bg-gray-700"
            >
              Сбросить настройки
            </button>
            
            <button
              type="submit"
              className="cs-button px-8"
              disabled={isSaving}
            >
              {isSaving ? 'Сохранение...' : 'Сохранить настройки'}
            </button>
          </div>
        </form>
      </main>

      <footer className="bg-cs-dark border-t border-gray-800 p-4 text-center text-gray-400 mt-8">
        <div className="container mx-auto">
          <p>© {new Date().getFullYear()} CS2 Панель управления. Все права защищены.</p>
        </div>
      </footer>
    </div>
  );
} 
import React, { useState } from 'react';
import { 
  Settings, 
  Shield, 
  Camera, 
  Bell, 
  Database,
  Save,
  RefreshCw,
  Download,
  Upload
} from 'lucide-react';

const SettingsPanel: React.FC = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [settings, setSettings] = useState({
    general: {
      systemName: 'ProSity Security',
      timezone: 'Europe/Moscow',
      language: 'ru',
      autoBackup: true,
      notifications: true
    },
    detection: {
      suspiciousBehaviorThreshold: 70,
      packageOpeningThreshold: 80,
      exitMovementThreshold: 60,
      confidenceThreshold: 75,
      maxConcurrentDetections: 10
    },
    cameras: {
      fps: 30,
      resolution: '1920x1080',
      quality: 'high',
      recordingEnabled: true,
      storageDays: 30
    },
    notifications: {
      emailEnabled: true,
      smsEnabled: false,
      pushEnabled: true,
      alertLevels: ['high', 'medium'],
      quietHours: { start: '22:00', end: '08:00' }
    },
    security: {
      sessionTimeout: 30,
      passwordPolicy: 'strong',
      twoFactorAuth: false,
      ipWhitelist: [],
      auditLog: true
    }
  });

  const tabs = [
    { id: 'general', name: 'Общие', icon: Settings },
    { id: 'detection', name: 'Детекция', icon: Shield },
    { id: 'cameras', name: 'Камеры', icon: Camera },
    { id: 'notifications', name: 'Уведомления', icon: Bell },
    { id: 'security', name: 'Безопасность', icon: Shield },
    { id: 'database', name: 'База данных', icon: Database }
  ];

  const handleSettingChange = (category: string, key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category as keyof typeof prev],
        [key]: value
      }
    }));
  };

  const handleSave = () => {
    // Здесь будет логика сохранения настроек
    console.log('Настройки сохранены:', settings);
  };

  const renderGeneralSettings = () => (
    <div className="space-y-6">
      <div className="form-group">
        <label className="form-label">Название системы</label>
        <input 
          type="text" 
          className="form-input"
          value={settings.general.systemName}
          onChange={(e) => handleSettingChange('general', 'systemName', e.target.value)}
        />
      </div>
      
      <div className="form-group">
        <label className="form-label">Часовой пояс</label>
        <select 
          className="form-select"
          value={settings.general.timezone}
          onChange={(e) => handleSettingChange('general', 'timezone', e.target.value)}
        >
          <option value="Europe/Moscow">Москва (UTC+3)</option>
          <option value="Europe/London">Лондон (UTC+0)</option>
          <option value="America/New_York">Нью-Йорк (UTC-5)</option>
        </select>
      </div>

      <div className="form-group">
        <label className="form-label">Язык интерфейса</label>
        <select 
          className="form-select"
          value={settings.general.language}
          onChange={(e) => handleSettingChange('general', 'language', e.target.value)}
        >
          <option value="ru">Русский</option>
          <option value="en">English</option>
        </select>
      </div>

      <div className="form-group">
        <label className="flex items-center gap-2">
          <input 
            type="checkbox" 
            checked={settings.general.autoBackup}
            onChange={(e) => handleSettingChange('general', 'autoBackup', e.target.checked)}
          />
          Автоматическое резервное копирование
        </label>
      </div>

      <div className="form-group">
        <label className="flex items-center gap-2">
          <input 
            type="checkbox" 
            checked={settings.general.notifications}
            onChange={(e) => handleSettingChange('general', 'notifications', e.target.checked)}
          />
          Системные уведомления
        </label>
      </div>
    </div>
  );

  const renderDetectionSettings = () => (
    <div className="space-y-6">
      <div className="form-group">
        <label className="form-label">
          Порог подозрительного поведения: {settings.detection.suspiciousBehaviorThreshold}%
        </label>
        <input 
          type="range" 
          min="0" 
          max="100" 
          value={settings.detection.suspiciousBehaviorThreshold}
          onChange={(e) => handleSettingChange('detection', 'suspiciousBehaviorThreshold', parseInt(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="form-group">
        <label className="form-label">
          Порог детекции вскрытия упаковок: {settings.detection.packageOpeningThreshold}%
        </label>
        <input 
          type="range" 
          min="0" 
          max="100" 
          value={settings.detection.packageOpeningThreshold}
          onChange={(e) => handleSettingChange('detection', 'packageOpeningThreshold', parseInt(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="form-group">
        <label className="form-label">
          Порог движения к выходам: {settings.detection.exitMovementThreshold}%
        </label>
        <input 
          type="range" 
          min="0" 
          max="100" 
          value={settings.detection.exitMovementThreshold}
          onChange={(e) => handleSettingChange('detection', 'exitMovementThreshold', parseInt(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="form-group">
        <label className="form-label">
          Минимальная уверенность: {settings.detection.confidenceThreshold}%
        </label>
        <input 
          type="range" 
          min="0" 
          max="100" 
          value={settings.detection.confidenceThreshold}
          onChange={(e) => handleSettingChange('detection', 'confidenceThreshold', parseInt(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="form-group">
        <label className="form-label">Максимум одновременных детекций</label>
        <input 
          type="number" 
          className="form-input"
          value={settings.detection.maxConcurrentDetections}
          onChange={(e) => handleSettingChange('detection', 'maxConcurrentDetections', parseInt(e.target.value))}
          min="1"
          max="50"
        />
      </div>
    </div>
  );

  const renderCameraSettings = () => (
    <div className="space-y-6">
      <div className="form-group">
        <label className="form-label">Частота кадров (FPS)</label>
        <select 
          className="form-select"
          value={settings.cameras.fps}
          onChange={(e) => handleSettingChange('cameras', 'fps', parseInt(e.target.value))}
        >
          <option value={15}>15 FPS</option>
          <option value={30}>30 FPS</option>
          <option value={60}>60 FPS</option>
        </select>
      </div>

      <div className="form-group">
        <label className="form-label">Разрешение</label>
        <select 
          className="form-select"
          value={settings.cameras.resolution}
          onChange={(e) => handleSettingChange('cameras', 'resolution', e.target.value)}
        >
          <option value="1280x720">HD (1280x720)</option>
          <option value="1920x1080">Full HD (1920x1080)</option>
          <option value="2560x1440">2K (2560x1440)</option>
          <option value="3840x2160">4K (3840x2160)</option>
        </select>
      </div>

      <div className="form-group">
        <label className="form-label">Качество записи</label>
        <select 
          className="form-select"
          value={settings.cameras.quality}
          onChange={(e) => handleSettingChange('cameras', 'quality', e.target.value)}
        >
          <option value="low">Низкое</option>
          <option value="medium">Среднее</option>
          <option value="high">Высокое</option>
        </select>
      </div>

      <div className="form-group">
        <label className="flex items-center gap-2">
          <input 
            type="checkbox" 
            checked={settings.cameras.recordingEnabled}
            onChange={(e) => handleSettingChange('cameras', 'recordingEnabled', e.target.checked)}
          />
          Включить запись видео
        </label>
      </div>

      <div className="form-group">
        <label className="form-label">Дни хранения записей</label>
        <input 
          type="number" 
          className="form-input"
          value={settings.cameras.storageDays}
          onChange={(e) => handleSettingChange('cameras', 'storageDays', parseInt(e.target.value))}
          min="1"
          max="365"
        />
      </div>
    </div>
  );

  const renderNotificationSettings = () => (
    <div className="space-y-6">
      <div className="form-group">
        <label className="flex items-center gap-2">
          <input 
            type="checkbox" 
            checked={settings.notifications.emailEnabled}
            onChange={(e) => handleSettingChange('notifications', 'emailEnabled', e.target.checked)}
          />
          Email уведомления
        </label>
      </div>

      <div className="form-group">
        <label className="flex items-center gap-2">
          <input 
            type="checkbox" 
            checked={settings.notifications.smsEnabled}
            onChange={(e) => handleSettingChange('notifications', 'smsEnabled', e.target.checked)}
          />
          SMS уведомления
        </label>
      </div>

      <div className="form-group">
        <label className="flex items-center gap-2">
          <input 
            type="checkbox" 
            checked={settings.notifications.pushEnabled}
            onChange={(e) => handleSettingChange('notifications', 'pushEnabled', e.target.checked)}
          />
          Push уведомления
        </label>
      </div>

      <div className="form-group">
        <label className="form-label">Уровни уведомлений</label>
        <div className="space-y-2">
          {['low', 'medium', 'high'].map(level => (
            <label key={level} className="flex items-center gap-2">
              <input 
                type="checkbox" 
                checked={settings.notifications.alertLevels.includes(level)}
                onChange={(e) => {
                  const newLevels = e.target.checked 
                    ? [...settings.notifications.alertLevels, level]
                    : settings.notifications.alertLevels.filter(l => l !== level);
                  handleSettingChange('notifications', 'alertLevels', newLevels);
                }}
              />
              {level === 'low' ? 'Низкий' : level === 'medium' ? 'Средний' : 'Высокий'}
            </label>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="form-group">
          <label className="form-label">Начало тихих часов</label>
          <input 
            type="time" 
            className="form-input"
            value={settings.notifications.quietHours.start}
            onChange={(e) => handleSettingChange('notifications', 'quietHours', {
              ...settings.notifications.quietHours,
              start: e.target.value
            })}
          />
        </div>
        <div className="form-group">
          <label className="form-label">Конец тихих часов</label>
          <input 
            type="time" 
            className="form-input"
            value={settings.notifications.quietHours.end}
            onChange={(e) => handleSettingChange('notifications', 'quietHours', {
              ...settings.notifications.quietHours,
              end: e.target.value
            })}
          />
        </div>
      </div>
    </div>
  );

  const renderSecuritySettings = () => (
    <div className="space-y-6">
      <div className="form-group">
        <label className="form-label">Таймаут сессии (минуты)</label>
        <input 
          type="number" 
          className="form-input"
          value={settings.security.sessionTimeout}
          onChange={(e) => handleSettingChange('security', 'sessionTimeout', parseInt(e.target.value))}
          min="5"
          max="480"
        />
      </div>

      <div className="form-group">
        <label className="form-label">Политика паролей</label>
        <select 
          className="form-select"
          value={settings.security.passwordPolicy}
          onChange={(e) => handleSettingChange('security', 'passwordPolicy', e.target.value)}
        >
          <option value="weak">Слабая</option>
          <option value="medium">Средняя</option>
          <option value="strong">Сильная</option>
        </select>
      </div>

      <div className="form-group">
        <label className="flex items-center gap-2">
          <input 
            type="checkbox" 
            checked={settings.security.twoFactorAuth}
            onChange={(e) => handleSettingChange('security', 'twoFactorAuth', e.target.checked)}
          />
          Двухфакторная аутентификация
        </label>
      </div>

      <div className="form-group">
        <label className="flex items-center gap-2">
          <input 
            type="checkbox" 
            checked={settings.security.auditLog}
            onChange={(e) => handleSettingChange('security', 'auditLog', e.target.checked)}
          />
          Ведение журнала аудита
        </label>
      </div>

      <div className="form-group">
        <label className="form-label">IP белый список (по одному на строку)</label>
        <textarea 
          className="form-input"
          rows={4}
          placeholder="192.168.1.1&#10;10.0.0.1"
          value={settings.security.ipWhitelist.join('\n')}
          onChange={(e) => handleSettingChange('security', 'ipWhitelist', e.target.value.split('\n').filter(ip => ip.trim()))}
        />
      </div>
    </div>
  );

  const renderDatabaseSettings = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Резервное копирование</h3>
          </div>
          <div className="space-y-4">
            <button className="btn btn-primary w-full">
              <Download size={16} />
              Создать резервную копию
            </button>
            <button className="btn btn-secondary w-full">
              <Upload size={16} />
              Восстановить из копии
            </button>
            <button className="btn btn-warning w-full">
              <RefreshCw size={16} />
              Автоматическая синхронизация
            </button>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Статистика базы данных</h3>
          </div>
          <div className="space-y-4">
            <div className="flex justify-between">
              <span>Размер базы данных:</span>
              <span className="font-medium">2.4 GB</span>
            </div>
            <div className="flex justify-between">
              <span>Записей уведомлений:</span>
              <span className="font-medium">15,432</span>
            </div>
            <div className="flex justify-between">
              <span>Событий детекции:</span>
              <span className="font-medium">8,765</span>
            </div>
            <div className="flex justify-between">
              <span>Последнее обновление:</span>
              <span className="font-medium">2 мин назад</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'general': return renderGeneralSettings();
      case 'detection': return renderDetectionSettings();
      case 'cameras': return renderCameraSettings();
      case 'notifications': return renderNotificationSettings();
      case 'security': return renderSecuritySettings();
      case 'database': return renderDatabaseSettings();
      default: return renderGeneralSettings();
    }
  };

  return (
    <div className="settings-panel">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Настройки системы
        </h1>
        <p className="text-gray-600">
          Конфигурация параметров системы детекции краж
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Боковая панель с вкладками */}
        <div className="lg:col-span-1">
          <div className="card">
            <nav className="space-y-2">
              {tabs.map(tab => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    className={`w-full flex items-center gap-3 px-4 py-3 text-left rounded-lg transition-colors ${
                      activeTab === tab.id 
                        ? 'bg-blue-100 text-blue-700' 
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                    onClick={() => setActiveTab(tab.id)}
                  >
                    <Icon size={20} />
                    {tab.name}
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Основной контент */}
        <div className="lg:col-span-3">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">
                {tabs.find(tab => tab.id === activeTab)?.name}
              </h3>
              <button 
                className="btn btn-primary"
                onClick={handleSave}
              >
                <Save size={16} />
                Сохранить настройки
              </button>
            </div>
            <div className="p-6">
              {renderTabContent()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPanel;

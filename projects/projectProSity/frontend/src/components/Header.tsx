import React from 'react';
import { Menu, Bell, User, Settings } from 'lucide-react';

interface SystemStatus {
  status: 'online' | 'offline' | 'maintenance';
  activeCameras: number;
  totalAlerts: number;
  preventionRate: number;
}

interface HeaderProps {
  systemStatus: SystemStatus;
  activeAlerts: number;
  onSidebarToggle: () => void;
}

const Header: React.FC<HeaderProps> = ({ systemStatus, activeAlerts, onSidebarToggle }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return '#10b981';
      case 'offline': return '#ef4444';
      case 'maintenance': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'online': return 'Онлайн';
      case 'offline': return 'Офлайн';
      case 'maintenance': return 'Обслуживание';
      default: return 'Неизвестно';
    }
  };

  return (
    <header className="header">
      <div className="header-left">
        <button
          className="sidebar-toggle lg:hidden"
          onClick={onSidebarToggle}
        >
          <Menu size={24} />
        </button>
        
        <div>
          <h1 className="header-title">ProSity Security</h1>
          <p className="text-sm text-gray-500">
            Система детекции краж в торговых центрах
          </p>
        </div>
      </div>

      <div className="header-right">
        {/* Статус системы */}
        <div 
          className="status-indicator"
          style={{ 
            backgroundColor: getStatusColor(systemStatus.status) + '20',
            color: getStatusColor(systemStatus.status)
          }}
        >
          <div 
            className="status-dot"
            style={{ backgroundColor: getStatusColor(systemStatus.status) }}
          />
          {getStatusText(systemStatus.status)}
        </div>

        {/* Уведомления */}
        <button className="relative p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
          <Bell size={20} />
          {activeAlerts > 0 && (
            <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
              {activeAlerts > 99 ? '99+' : activeAlerts}
            </span>
          )}
        </button>

        {/* Пользователь */}
        <div className="flex items-center gap-2">
          <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
            <Settings size={20} />
          </button>
          <button className="flex items-center gap-2 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
            <User size={20} />
            <span className="hidden md:block text-sm font-medium">
              Администратор
            </span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield, Menu, X } from 'lucide-react';

interface MenuItem {
  id: string;
  title: string;
  icon: React.ComponentType<any>;
  path: string;
  description: string;
  badge?: number;
}

interface SystemStatus {
  status: 'online' | 'offline' | 'maintenance';
  activeCameras: number;
  totalAlerts: number;
  preventionRate: number;
}

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  menuItems: MenuItem[];
  systemStatus: SystemStatus;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onToggle, menuItems, systemStatus }) => {
  const location = useLocation();

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
    <>
      {/* Мобильная кнопка */}
      <button
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-lg"
        onClick={onToggle}
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Боковая панель */}
      <div className={`sidebar ${isOpen ? 'open' : 'collapsed'} lg:block`}>
        {/* Заголовок */}
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <Shield size={32} />
            <span className={isOpen ? 'block' : 'hidden'}>ProSity</span>
          </div>
        </div>

        {/* Статус системы */}
        <div className={`mb-6 p-4 bg-white bg-opacity-10 rounded-lg ${isOpen ? 'block' : 'hidden'}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">Статус системы</span>
            <div 
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: getStatusColor(systemStatus.status) }}
            />
          </div>
          <div className="text-lg font-bold">{getStatusText(systemStatus.status)}</div>
          <div className="text-sm opacity-75">
            {systemStatus.activeCameras} камер активны
          </div>
        </div>

        {/* Меню */}
        <nav className="sidebar-menu">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <div key={item.id} className="sidebar-menu-item">
                <Link
                  to={item.path}
                  className={`sidebar-menu-link ${isActive ? 'active' : ''}`}
                  title={isOpen ? '' : item.description}
                >
                  <Icon size={20} />
                  <span className={isOpen ? 'block' : 'hidden'}>
                    {item.title}
                  </span>
                  {item.badge && item.badge > 0 && (
                    <span className="menu-badge">
                      {item.badge > 99 ? '99+' : item.badge}
                    </span>
                  )}
                </Link>
              </div>
            );
          })}
        </nav>

        {/* Нижняя секция */}
        <div className={`mt-auto pt-6 border-t border-white border-opacity-10 ${isOpen ? 'block' : 'hidden'}`}>
          <div className="text-sm opacity-75 mb-2">Процент предотвращения</div>
          <div className="text-2xl font-bold mb-2">{systemStatus.preventionRate}%</div>
          <div className="w-full bg-white bg-opacity-20 rounded-full h-2">
            <div 
              className="bg-white h-2 rounded-full transition-all duration-300"
              style={{ width: `${systemStatus.preventionRate}%` }}
            />
          </div>
        </div>
      </div>

      {/* Затемнение для мобильных устройств */}
      {isOpen && (
        <div 
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={onToggle}
        />
      )}
    </>
  );
};

export default Sidebar;

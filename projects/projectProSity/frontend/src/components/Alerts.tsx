import React, { useState } from 'react';
import { 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  Eye,
  Filter,
  Search,
  Bell
} from 'lucide-react';

const Alerts: React.FC = () => {
  const [selectedSeverity, setSelectedSeverity] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');

  const alerts = [
    {
      id: 1,
      type: 'suspicious_behavior',
      severity: 'high',
      status: 'active',
      location: 'Электроника - Камера 2',
      time: '2 минуты назад',
      description: 'Обнаружено подозрительное поведение: человек долго смотрит на товар и прячет руки',
      confidence: 87,
      camera: 'cam_2',
      actionRequired: true
    },
    {
      id: 2,
      type: 'package_opening',
      severity: 'medium',
      status: 'acknowledged',
      location: 'Одежда - Камера 5',
      time: '5 минут назад',
      description: 'Возможное вскрытие упаковки товара',
      confidence: 73,
      camera: 'cam_5',
      actionRequired: false
    },
    {
      id: 3,
      type: 'exit_movement',
      severity: 'low',
      status: 'resolved',
      location: 'Главный выход',
      time: '8 минут назад',
      description: 'Движение к выходу без оплаты товара',
      confidence: 65,
      camera: 'cam_1',
      actionRequired: false
    },
    {
      id: 4,
      type: 'suspicious_behavior',
      severity: 'high',
      status: 'active',
      location: 'Косметика - Камера 9',
      time: '12 минут назад',
      description: 'Подозрительные движения: человек избегает камер',
      confidence: 82,
      camera: 'cam_9',
      actionRequired: true
    },
    {
      id: 5,
      type: 'package_opening',
      severity: 'medium',
      status: 'acknowledged',
      location: 'Электроника - Камера 3',
      time: '15 минут назад',
      description: 'Попытка вскрытия упаковки смартфона',
      confidence: 78,
      camera: 'cam_3',
      actionRequired: false
    }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high': return <AlertTriangle size={16} />;
      case 'medium': return <Clock size={16} />;
      case 'low': return <Eye size={16} />;
      default: return <Bell size={16} />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return '#ef4444';
      case 'acknowledged': return '#f59e0b';
      case 'resolved': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Активно';
      case 'acknowledged': return 'Подтверждено';
      case 'resolved': return 'Разрешено';
      default: return 'Неизвестно';
    }
  };

  const filteredAlerts = alerts.filter(alert => {
    if (selectedSeverity !== 'all' && alert.severity !== selectedSeverity) return false;
    if (selectedStatus !== 'all' && alert.status !== selectedStatus) return false;
    return true;
  });

  return (
    <div className="alerts">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Уведомления системы
        </h1>
        <p className="text-gray-600">
          Мониторинг и управление уведомлениями о подозрительной активности
        </p>
      </div>

      {/* Фильтры и статистика */}
      <div className="card mb-6">
        <div className="card-header">
          <h3 className="card-title">Фильтры и поиск</h3>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Filter size={16} />
              <select 
                className="form-select w-auto"
                value={selectedSeverity}
                onChange={(e) => setSelectedSeverity(e.target.value)}
              >
                <option value="all">Все уровни</option>
                <option value="high">Высокий</option>
                <option value="medium">Средний</option>
                <option value="low">Низкий</option>
              </select>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle size={16} />
              <select 
                className="form-select w-auto"
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
              >
                <option value="all">Все статусы</option>
                <option value="active">Активные</option>
                <option value="acknowledged">Подтвержденные</option>
                <option value="resolved">Разрешенные</option>
              </select>
            </div>
            <div className="flex items-center gap-2">
              <Search size={16} />
              <input 
                type="text" 
                placeholder="Поиск по описанию..."
                className="form-input w-64"
              />
            </div>
          </div>
        </div>

        {/* Статистика уведомлений */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600">
              {alerts.filter(a => a.status === 'active').length}
            </div>
            <div className="text-sm text-gray-600">Активные</div>
          </div>
          <div className="text-center p-4 bg-yellow-50 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600">
              {alerts.filter(a => a.status === 'acknowledged').length}
            </div>
            <div className="text-sm text-gray-600">Подтвержденные</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">
              {alerts.filter(a => a.status === 'resolved').length}
            </div>
            <div className="text-sm text-gray-600">Разрешенные</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">
              {alerts.filter(a => a.actionRequired).length}
            </div>
            <div className="text-sm text-gray-600">Требуют действий</div>
          </div>
        </div>
      </div>

      {/* Список уведомлений */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Уведомления ({filteredAlerts.length})</h3>
          <button className="btn btn-primary btn-sm">
            Отметить все как прочитанные
          </button>
        </div>
        <div className="space-y-4">
          {filteredAlerts.map(alert => (
            <div 
              key={alert.id}
              className={`p-4 border rounded-lg ${
                alert.status === 'active' ? 'border-red-200 bg-red-50' :
                alert.status === 'acknowledged' ? 'border-yellow-200 bg-yellow-50' :
                'border-green-200 bg-green-50'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4 flex-1">
                  <div 
                    className="p-2 rounded-full"
                    style={{ backgroundColor: getSeverityColor(alert.severity) + '20' }}
                  >
                    {getSeverityIcon(alert.severity)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h4 className="font-medium text-gray-900">{alert.description}</h4>
                      {alert.actionRequired && (
                        <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">
                          Требует действий
                        </span>
                      )}
                    </div>
                    <div className="text-sm text-gray-600 mb-2">
                      {alert.location} • {alert.time}
                    </div>
                    <div className="flex items-center gap-4 text-sm">
                      <span 
                        className="px-2 py-1 rounded-full"
                        style={{ 
                          backgroundColor: getSeverityColor(alert.severity) + '20',
                          color: getSeverityColor(alert.severity)
                        }}
                      >
                        Уверенность: {alert.confidence}%
                      </span>
                      <span 
                        className="px-2 py-1 rounded-full"
                        style={{ 
                          backgroundColor: getStatusColor(alert.status) + '20',
                          color: getStatusColor(alert.status)
                        }}
                      >
                        {getStatusText(alert.status)}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button className="btn btn-secondary btn-sm">
                    <Eye size={14} />
                    Просмотр
                  </button>
                  {alert.status === 'active' && (
                    <button className="btn btn-warning btn-sm">
                      <CheckCircle size={14} />
                      Подтвердить
                    </button>
                  )}
                  {alert.status === 'acknowledged' && (
                    <button className="btn btn-success btn-sm">
                      <CheckCircle size={14} />
                      Разрешить
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredAlerts.length === 0 && (
          <div className="text-center py-8">
            <Bell size={48} className="text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Уведомлений не найдено
            </h3>
            <p className="text-gray-500">
              Попробуйте изменить фильтры или поисковый запрос
            </p>
          </div>
        )}
      </div>

      {/* Быстрые действия */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <button className="btn btn-primary btn-lg w-full">
          <AlertTriangle size={20} />
          Создать уведомление
        </button>
        <button className="btn btn-success btn-lg w-full">
          <CheckCircle size={20} />
          Разрешить все активные
        </button>
        <button className="btn btn-warning btn-lg w-full">
          <Eye size={20} />
          Экспорт уведомлений
        </button>
      </div>
    </div>
  );
};

export default Alerts;

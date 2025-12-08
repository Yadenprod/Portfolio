import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  Camera, 
  AlertTriangle, 
  TrendingUp, 
  Users, 
  DollarSign,
  Eye,
  Clock,
  CheckCircle,
  XCircle,
  Settings
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface SystemStatus {
  status: 'online' | 'offline' | 'maintenance';
  activeCameras: number;
  totalAlerts: number;
  preventionRate: number;
}

interface DashboardProps {
  systemStatus: SystemStatus;
}

const Dashboard: React.FC<DashboardProps> = ({ systemStatus }) => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [recentAlerts, setRecentAlerts] = useState([
    {
      id: 1,
      type: 'suspicious_behavior',
      location: 'Электроника - Камера 2',
      severity: 'high',
      time: '2 минуты назад',
      description: 'Обнаружено подозрительное поведение'
    },
    {
      id: 2,
      type: 'package_opening',
      location: 'Одежда - Камера 5',
      severity: 'medium',
      time: '5 минут назад',
      description: 'Возможное вскрытие упаковки'
    },
    {
      id: 3,
      type: 'exit_movement',
      location: 'Главный выход',
      severity: 'low',
      time: '8 минут назад',
      description: 'Движение к выходу без оплаты'
    }
  ]);

  // Данные для графиков
  const theftData = [
    { month: 'Янв', prevented: 12, total: 15 },
    { month: 'Фев', prevented: 15, total: 18 },
    { month: 'Мар', prevented: 18, total: 22 },
    { month: 'Апр', prevented: 22, total: 25 },
    { month: 'Май', prevented: 25, total: 28 },
    { month: 'Июн', prevented: 28, total: 30 }
  ];

  const categoryData = [
    { name: 'Электроника', value: 45, color: '#ef4444' },
    { name: 'Одежда', value: 30, color: '#f59e0b' },
    { name: 'Косметика', value: 15, color: '#3b82f6' },
    { name: 'Другое', value: 10, color: '#10b981' }
  ];

  const performanceData = [
    { time: '00:00', accuracy: 87, alerts: 2 },
    { time: '04:00', accuracy: 85, alerts: 1 },
    { time: '08:00', accuracy: 89, alerts: 3 },
    { time: '12:00', accuracy: 92, alerts: 5 },
    { time: '16:00', accuracy: 88, alerts: 4 },
    { time: '20:00', accuracy: 90, alerts: 6 }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

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
      case 'low': return <CheckCircle size={16} />;
      default: return <Eye size={16} />;
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Панель управления ProSity Security
          </h1>
          <p className="text-gray-600">
            Система детекции краж в торговых центрах
          </p>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-500">
            {currentTime.toLocaleDateString('ru-RU', { 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </div>
          <div className="text-lg font-semibold text-gray-900">
            {currentTime.toLocaleTimeString('ru-RU')}
          </div>
        </div>
      </div>

      {/* Основная статистика */}
      <div className="stats-grid">
        <div className="stat-card success">
          <div className="flex items-center justify-between">
            <div>
              <div className="stat-value">{systemStatus.preventionRate}%</div>
              <div className="stat-label">Процент предотвращения</div>
              <div className="stat-change positive">
                <TrendingUp size={16} />
                +2.5% за месяц
              </div>
            </div>
            <Shield size={48} className="text-green-500" />
          </div>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between">
            <div>
              <div className="stat-value">{systemStatus.activeCameras}</div>
              <div className="stat-label">Активные камеры</div>
              <div className="stat-change positive">
                <CheckCircle size={16} />
                Все работают
              </div>
            </div>
            <Camera size={48} className="text-blue-500" />
          </div>
        </div>

        <div className="stat-card warning">
          <div className="flex items-center justify-between">
            <div>
              <div className="stat-value">{systemStatus.totalAlerts}</div>
              <div className="stat-label">Активные уведомления</div>
              <div className="stat-change negative">
                <AlertTriangle size={16} />
                +3 за час
              </div>
            </div>
            <AlertTriangle size={48} className="text-orange-500" />
          </div>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between">
            <div>
              <div className="stat-value">₽2.4M</div>
              <div className="stat-label">Экономия за месяц</div>
              <div className="stat-change positive">
                <DollarSign size={16} />
                +15% к прошлому месяцу
              </div>
            </div>
            <DollarSign size={48} className="text-green-600" />
          </div>
        </div>
      </div>

      {/* Графики и аналитика */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* График предотвращения краж */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Динамика предотвращения краж</h3>
            <span className="text-sm text-gray-500">За 6 месяцев</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={theftData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="prevented" 
                stroke="#10b981" 
                strokeWidth={3}
                name="Предотвращено"
              />
              <Line 
                type="monotone" 
                dataKey="total" 
                stroke="#ef4444" 
                strokeWidth={2}
                name="Всего попыток"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Круговая диаграмма по категориям */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Кражи по категориям товаров</h3>
            <span className="text-sm text-gray-500">Текущий месяц</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Производительность системы */}
      <div className="card mb-8">
        <div className="card-header">
          <h3 className="card-title">Производительность системы</h3>
          <span className="text-sm text-gray-500">За последние 24 часа</span>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={performanceData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis yAxisId="left" />
            <YAxis yAxisId="right" orientation="right" />
            <Tooltip />
            <Line 
              yAxisId="left"
              type="monotone" 
              dataKey="accuracy" 
              stroke="#3b82f6" 
              strokeWidth={3}
              name="Точность (%)"
            />
            <Line 
              yAxisId="right"
              type="monotone" 
              dataKey="alerts" 
              stroke="#f59e0b" 
              strokeWidth={2}
              name="Уведомления"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Последние уведомления */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Последние уведомления</h3>
          <button className="btn btn-primary btn-sm">
            Просмотреть все
          </button>
        </div>
        <div className="space-y-4">
          {recentAlerts.map((alert) => (
            <div 
              key={alert.id} 
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center gap-4">
                <div 
                  className="p-2 rounded-full"
                  style={{ backgroundColor: getSeverityColor(alert.severity) + '20' }}
                >
                  {getSeverityIcon(alert.severity)}
                </div>
                <div>
                  <div className="font-medium text-gray-900">
                    {alert.description}
                  </div>
                  <div className="text-sm text-gray-500">
                    {alert.location} • {alert.time}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span 
                  className="px-2 py-1 text-xs font-medium rounded-full"
                  style={{ 
                    backgroundColor: getSeverityColor(alert.severity) + '20',
                    color: getSeverityColor(alert.severity)
                  }}
                >
                  {alert.severity.toUpperCase()}
                </span>
                <button className="btn btn-secondary btn-sm">
                  Действие
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Быстрые действия */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <button className="btn btn-primary btn-lg w-full">
          <Camera size={20} />
          Запустить детекцию
        </button>
        <button className="btn btn-success btn-lg w-full">
          <TrendingUp size={20} />
          Сгенерировать отчет
        </button>
        <button className="btn btn-warning btn-lg w-full">
          <Settings size={20} />
          Настройки системы
        </button>
      </div>
    </div>
  );
};

export default Dashboard;

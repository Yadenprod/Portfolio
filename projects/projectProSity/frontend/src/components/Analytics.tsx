import React, { useState } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  DollarSign, 
  Shield,
  Download,
  Calendar
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  PieChart, 
  Pie, 
  Cell 
} from 'recharts';

const Analytics: React.FC = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('month');

  // Данные для графиков
  const roiData = [
    { month: 'Янв', investment: 300000, savings: 180000, roi: -40 },
    { month: 'Фев', investment: 300000, savings: 220000, roi: -27 },
    { month: 'Мар', investment: 300000, savings: 280000, roi: -7 },
    { month: 'Апр', investment: 300000, savings: 320000, roi: 7 },
    { month: 'Май', investment: 300000, savings: 380000, roi: 27 },
    { month: 'Июн', investment: 300000, savings: 420000, roi: 40 }
  ];

  const theftByCategory = [
    { category: 'Электроника', prevented: 45, total: 53, percentage: 85 },
    { category: 'Одежда', prevented: 30, total: 40, percentage: 75 },
    { category: 'Косметика', prevented: 15, total: 23, percentage: 65 },
    { category: 'Другое', prevented: 10, total: 15, percentage: 67 }
  ];

  const performanceMetrics = [
    { metric: 'Точность детекции', value: 87, target: 90, status: 'good' },
    { metric: 'Ложные срабатывания', value: 3.2, target: 2.0, status: 'warning' },
    { metric: 'Время отклика', value: 2.3, target: 3.0, status: 'excellent' },
    { metric: 'Покрытие зон', value: 90.6, target: 95, status: 'good' }
  ];

  const monthlySavings = [
    { month: 'Янв', savings: 180000 },
    { month: 'Фев', savings: 220000 },
    { month: 'Мар', savings: 280000 },
    { month: 'Апр', savings: 320000 },
    { month: 'Май', savings: 380000 },
    { month: 'Июн', savings: 420000 }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'excellent': return '#10b981';
      case 'good': return '#3b82f6';
      case 'warning': return '#f59e0b';
      case 'poor': return '#ef4444';
      default: return '#6b7280';
    }
  };

  return (
    <div className="analytics">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Аналитика и ROI
        </h1>
        <p className="text-gray-600">
          Анализ эффективности системы и расчет возврата инвестиций
        </p>
      </div>

      {/* Период анализа */}
      <div className="card mb-6">
        <div className="card-header">
          <h3 className="card-title">Период анализа</h3>
          <div className="flex items-center gap-2">
            <Calendar size={16} />
            <select 
              className="form-select w-auto"
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
            >
              <option value="week">Неделя</option>
              <option value="month">Месяц</option>
              <option value="quarter">Квартал</option>
              <option value="year">Год</option>
            </select>
          </div>
        </div>
      </div>

      {/* ROI анализ */}
      <div className="card mb-6">
        <div className="card-header">
          <h3 className="card-title">Анализ ROI</h3>
          <button className="btn btn-primary btn-sm">
            <Download size={16} />
            Экспорт отчета
          </button>
        </div>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={roiData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Line 
              type="monotone" 
              dataKey="savings" 
              stroke="#10b981" 
              strokeWidth={3}
              name="Экономия (₽)"
            />
            <Line 
              type="monotone" 
              dataKey="investment" 
              stroke="#ef4444" 
              strokeWidth={2}
              name="Инвестиции (₽)"
            />
          </LineChart>
        </ResponsiveContainer>
        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">₽2.4M</div>
            <div className="text-sm text-gray-600">Общая экономия за 6 месяцев</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">40%</div>
            <div className="text-sm text-gray-600">ROI за 6 месяцев</div>
          </div>
          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <div className="text-2xl font-bold text-orange-600">4.5 мес</div>
            <div className="text-sm text-gray-600">Время окупаемости</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Эффективность по категориям */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Эффективность по категориям</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={theftByCategory}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="prevented" fill="#10b981" name="Предотвращено" />
              <Bar dataKey="total" fill="#ef4444" name="Всего попыток" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Ежемесячная экономия */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Ежемесячная экономия</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={monthlySavings}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="savings" fill="#3b82f6" name="Экономия (₽)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Метрики производительности */}
      <div className="card mb-6">
        <div className="card-header">
          <h3 className="card-title">Метрики производительности</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {performanceMetrics.map((metric, index) => (
            <div key={index} className="p-4 border rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-600">{metric.metric}</span>
                <div 
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: getStatusColor(metric.status) }}
                />
              </div>
              <div className="text-2xl font-bold text-gray-900">{metric.value}</div>
              <div className="text-sm text-gray-500">Цель: {metric.target}</div>
              <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="h-2 rounded-full transition-all duration-300"
                  style={{ 
                    width: `${(metric.value / metric.target) * 100}%`,
                    backgroundColor: getStatusColor(metric.status)
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Детальный анализ */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Статистика по магазинам */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Статистика по магазинам</h3>
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
              <div>
                <div className="font-medium">Электроника</div>
                <div className="text-sm text-gray-500">Очень высокий риск</div>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-red-600">₽150K</div>
                <div className="text-sm text-gray-500">месячные потери</div>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
              <div>
                <div className="font-medium">Одежда</div>
                <div className="text-sm text-gray-500">Высокий риск</div>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-orange-600">₽80K</div>
                <div className="text-sm text-gray-500">месячные потери</div>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div>
                <div className="font-medium">Косметика</div>
                <div className="text-sm text-gray-500">Средний риск</div>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-blue-600">₽40K</div>
                <div className="text-sm text-gray-500">месячные потери</div>
              </div>
            </div>
          </div>
        </div>

        {/* Прогнозы */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Прогнозы на 12 месяцев</h3>
          </div>
          <div className="space-y-4">
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">₽5.2M</div>
              <div className="text-sm text-gray-600">Ожидаемая экономия</div>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">73%</div>
              <div className="text-sm text-gray-600">Ожидаемый ROI</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">92%</div>
              <div className="text-sm text-gray-600">Ожидаемая точность</div>
            </div>
          </div>
        </div>

        {/* Рекомендации */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Рекомендации</h3>
          </div>
          <div className="space-y-3">
            <div className="flex items-start gap-3 p-3 bg-yellow-50 rounded-lg">
              <Shield size={16} className="text-yellow-600 mt-1" />
              <div>
                <div className="font-medium text-yellow-800">Увеличить камеры</div>
                <div className="text-sm text-yellow-700">Добавить 2 камеры в зону электроники</div>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
              <TrendingUp size={16} className="text-blue-600 mt-1" />
              <div>
                <div className="font-medium text-blue-800">Оптимизировать алгоритмы</div>
                <div className="text-sm text-blue-700">Снизить ложные срабатывания на 15%</div>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 bg-green-50 rounded-lg">
              <DollarSign size={16} className="text-green-600 mt-1" />
              <div>
                <div className="font-medium text-green-800">Расширить зону покрытия</div>
                <div className="text-sm text-green-700">Добавить мониторинг парковки</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;

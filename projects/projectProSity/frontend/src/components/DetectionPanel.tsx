import React, { useState, useEffect } from 'react';
import { 
  Camera, 
  Play, 
  Pause, 
  Settings, 
  AlertTriangle,
  Eye,
  Shield,
  Activity
} from 'lucide-react';

const DetectionPanel: React.FC = () => {
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [selectedCamera, setSelectedCamera] = useState('all');
  const [detectionStats, setDetectionStats] = useState({
    activeDetections: 0,
    suspiciousEvents: 0,
    packageOpenings: 0,
    exitMovements: 0
  });

  const cameras = [
    { id: 'cam_1', name: 'Камера 1 - Вход', location: 'Электроника', status: 'active' },
    { id: 'cam_2', name: 'Камера 2 - Витрина', location: 'Электроника', status: 'active' },
    { id: 'cam_3', name: 'Камера 3 - Касса', location: 'Электроника', status: 'active' },
    { id: 'cam_4', name: 'Камера 4 - Склад', location: 'Электроника', status: 'active' },
    { id: 'cam_5', name: 'Камера 5 - Вход', location: 'Одежда', status: 'active' },
    { id: 'cam_6', name: 'Камера 6 - Примерочные', location: 'Одежда', status: 'active' },
    { id: 'cam_7', name: 'Камера 7 - Касса', location: 'Одежда', status: 'active' },
    { id: 'cam_8', name: 'Камера 8 - Вход', location: 'Косметика', status: 'active' },
    { id: 'cam_9', name: 'Камера 9 - Парфюм', location: 'Косметика', status: 'active' },
    { id: 'cam_10', name: 'Камера 10 - Касса', location: 'Косметика', status: 'active' }
  ];

  const recentEvents = [
    {
      id: 1,
      camera: 'cam_2',
      type: 'suspicious_behavior',
      severity: 'high',
      time: '2 минуты назад',
      description: 'Подозрительные движения рук',
      confidence: 87
    },
    {
      id: 2,
      camera: 'cam_5',
      type: 'package_opening',
      severity: 'medium',
      time: '5 минут назад',
      description: 'Возможное вскрытие упаковки',
      confidence: 73
    },
    {
      id: 3,
      camera: 'cam_1',
      type: 'exit_movement',
      severity: 'low',
      time: '8 минут назад',
      description: 'Движение к выходу',
      confidence: 65
    }
  ];

  useEffect(() => {
    if (isMonitoring) {
      const interval = setInterval(() => {
        setDetectionStats(prev => ({
          activeDetections: prev.activeDetections + Math.floor(Math.random() * 3),
          suspiciousEvents: prev.suspiciousEvents + Math.floor(Math.random() * 2),
          packageOpenings: prev.packageOpenings + Math.floor(Math.random() * 1),
          exitMovements: prev.exitMovements + Math.floor(Math.random() * 2)
        }));
      }, 3000);

      return () => clearInterval(interval);
    }
  }, [isMonitoring]);

  const getEventTypeIcon = (type: string) => {
    switch (type) {
      case 'suspicious_behavior': return <AlertTriangle size={16} />;
      case 'package_opening': return <Eye size={16} />;
      case 'exit_movement': return <Activity size={16} />;
      default: return <Camera size={16} />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  return (
    <div className="detection-panel">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Панель детекции
        </h1>
        <p className="text-gray-600">
          Мониторинг в реальном времени и управление системой детекции
        </p>
      </div>

      {/* Управление системой */}
      <div className="card mb-6">
        <div className="card-header">
          <h3 className="card-title">Управление системой</h3>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${isMonitoring ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="text-sm">
                {isMonitoring ? 'Мониторинг активен' : 'Мониторинг остановлен'}
              </span>
            </div>
            <button
              className={`btn ${isMonitoring ? 'btn-danger' : 'btn-success'}`}
              onClick={() => setIsMonitoring(!isMonitoring)}
            >
              {isMonitoring ? (
                <>
                  <Pause size={16} />
                  Остановить
                </>
              ) : (
                <>
                  <Play size={16} />
                  Запустить
                </>
              )}
            </button>
          </div>
        </div>

        {/* Статистика детекции */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">{detectionStats.activeDetections}</div>
            <div className="text-sm text-gray-600">Активные детекции</div>
          </div>
          <div className="text-center p-4 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600">{detectionStats.suspiciousEvents}</div>
            <div className="text-sm text-gray-600">Подозрительные события</div>
          </div>
          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <div className="text-2xl font-bold text-orange-600">{detectionStats.packageOpenings}</div>
            <div className="text-sm text-gray-600">Вскрытия упаковок</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">{detectionStats.exitMovements}</div>
            <div className="text-sm text-gray-600">Движения к выходам</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Список камер */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Камеры наблюдения</h3>
            <select 
              className="form-select w-auto"
              value={selectedCamera}
              onChange={(e) => setSelectedCamera(e.target.value)}
            >
              <option value="all">Все камеры</option>
              <option value="electronics">Электроника</option>
              <option value="clothing">Одежда</option>
              <option value="cosmetics">Косметика</option>
            </select>
          </div>
          <div className="space-y-3">
            {cameras
              .filter(camera => selectedCamera === 'all' || camera.location.toLowerCase().includes(selectedCamera))
              .map(camera => (
                <div 
                  key={camera.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${camera.status === 'active' ? 'bg-green-500' : 'bg-red-500'}`} />
                    <div>
                      <div className="font-medium">{camera.name}</div>
                      <div className="text-sm text-gray-500">{camera.location}</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button className="btn btn-secondary btn-sm">
                      <Settings size={14} />
                    </button>
                    <button className="btn btn-primary btn-sm">
                      <Eye size={14} />
                    </button>
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* Последние события */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Последние события</h3>
            <button className="btn btn-primary btn-sm">
              Просмотреть все
            </button>
          </div>
          <div className="space-y-3">
            {recentEvents.map(event => (
              <div 
                key={event.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <div 
                    className="p-2 rounded-full"
                    style={{ backgroundColor: getSeverityColor(event.severity) + '20' }}
                  >
                    {getEventTypeIcon(event.type)}
                  </div>
                  <div>
                    <div className="font-medium">{event.description}</div>
                    <div className="text-sm text-gray-500">
                      {cameras.find(c => c.id === event.camera)?.name} • {event.time}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span 
                    className="px-2 py-1 text-xs font-medium rounded-full"
                    style={{ 
                      backgroundColor: getSeverityColor(event.severity) + '20',
                      color: getSeverityColor(event.severity)
                    }}
                  >
                    {event.confidence}%
                  </span>
                  <span 
                    className="px-2 py-1 text-xs font-medium rounded-full"
                    style={{ 
                      backgroundColor: getSeverityColor(event.severity) + '20',
                      color: getSeverityColor(event.severity)
                    }}
                  >
                    {event.severity.toUpperCase()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Настройки детекции */}
      <div className="card mt-6">
        <div className="card-header">
          <h3 className="card-title">Настройки детекции</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="form-label">Порог подозрительного поведения</label>
            <input 
              type="range" 
              min="0" 
              max="100" 
              defaultValue="70" 
              className="w-full"
            />
            <div className="text-sm text-gray-500 mt-1">70%</div>
          </div>
          <div>
            <label className="form-label">Порог детекции вскрытия упаковок</label>
            <input 
              type="range" 
              min="0" 
              max="100" 
              defaultValue="80" 
              className="w-full"
            />
            <div className="text-sm text-gray-500 mt-1">80%</div>
          </div>
          <div>
            <label className="form-label">Порог движения к выходам</label>
            <input 
              type="range" 
              min="0" 
              max="100" 
              defaultValue="60" 
              className="w-full"
            />
            <div className="text-sm text-gray-500 mt-1">60%</div>
          </div>
        </div>
        <div className="mt-4 flex justify-end">
          <button className="btn btn-primary">
            <Shield size={16} />
            Сохранить настройки
          </button>
        </div>
      </div>
    </div>
  );
};

export default DetectionPanel;

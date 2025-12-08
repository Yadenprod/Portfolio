import { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-hot-toast';

interface CS2BotProps {
  accountId: string;
  status?: string;
  onStatusChange?: (status: any) => void;
}

export default function CS2Bot({ accountId, status: initialStatus, onStatusChange }: CS2BotProps) {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<{
    status?: string;
    lastStart?: string;
    lastStop?: string;
    casesCollected?: number;
  }>({
    status: initialStatus
  });

  // Загрузка статуса бота
  const fetchBotStatus = async () => {
    if (!accountId) return;
    
    try {
      setLoading(true);
      const response = await axios.post('/api/bot', {
        accountId,
        action: 'status'
      });
      
      if (response.data.success) {
        setStatus(response.data.data);
        if (onStatusChange) {
          onStatusChange(response.data.data);
        }
      }
    } catch (error: any) {
      console.error('Ошибка при получении статуса бота:', error);
      toast.error(error.response?.data?.message || 'Ошибка при получении статуса бота');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBotStatus();
    // Обновление статуса каждые 30 секунд
    const intervalId = setInterval(fetchBotStatus, 30000);
    return () => clearInterval(intervalId);
  }, [accountId]);

  // Запуск бота
  const handleStartBot = async () => {
    try {
      setLoading(true);
      const response = await axios.post('/api/bot', {
        accountId,
        action: 'start'
      });
      
      if (response.data.success) {
        toast.success('Бот успешно запущен');
        fetchBotStatus();
      } else {
        toast.error(response.data.message || 'Ошибка при запуске бота');
      }
    } catch (error: any) {
      console.error('Ошибка при запуске бота:', error);
      toast.error(error.response?.data?.message || 'Ошибка при запуске бота');
    } finally {
      setLoading(false);
    }
  };

  // Остановка бота
  const handleStopBot = async () => {
    try {
      setLoading(true);
      const response = await axios.post('/api/bot', {
        accountId,
        action: 'stop'
      });
      
      if (response.data.success) {
        toast.success('Бот успешно остановлен');
        fetchBotStatus();
      } else {
        toast.error(response.data.message || 'Ошибка при остановке бота');
      }
    } catch (error: any) {
      console.error('Ошибка при остановке бота:', error);
      toast.error(error.response?.data?.message || 'Ошибка при остановке бота');
    } finally {
      setLoading(false);
    }
  };

  // Форматирование даты
  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Нет данных';
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h3 className="text-lg font-semibold mb-3">CS2 Бот</h3>
      
      <div className="mb-4">
        <div className="grid grid-cols-2 gap-2 text-sm mb-4">
          <div className="font-medium">Статус:</div>
          <div>
            {loading ? (
              <span className="text-gray-500">Загрузка...</span>
            ) : (
              <span className={`px-2 py-1 rounded text-xs font-medium ${
                status.status === 'running' ? 'bg-green-100 text-green-800' :
                status.status === 'error' ? 'bg-red-100 text-red-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {status.status === 'running' ? 'Запущен' :
                 status.status === 'error' ? 'Ошибка' :
                 status.status === 'idle' ? 'Остановлен' : 'Не запускался'}
              </span>
            )}
          </div>
          
          <div className="font-medium">Последний запуск:</div>
          <div>{formatDate(status.lastStart)}</div>
          
          <div className="font-medium">Последняя остановка:</div>
          <div>{formatDate(status.lastStop)}</div>
          
          <div className="font-medium">Собрано кейсов:</div>
          <div>{status.casesCollected || 0}</div>
        </div>
      </div>
      
      <div className="flex space-x-2">
        <button
          onClick={handleStartBot}
          disabled={loading || status.status === 'running'}
          className={`px-3 py-1.5 rounded text-white ${
            loading || status.status === 'running' 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-green-600 hover:bg-green-700'
          }`}
        >
          {loading ? 'Загрузка...' : 'Запустить бота'}
        </button>
        
        <button
          onClick={handleStopBot}
          disabled={loading || status.status !== 'running'}
          className={`px-3 py-1.5 rounded text-white ${
            loading || status.status !== 'running'
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-red-600 hover:bg-red-700'
          }`}
        >
          {loading ? 'Загрузка...' : 'Остановить бота'}
        </button>
      </div>
      
      <div className="mt-4 text-xs text-gray-500">
        <p>
          Бот автоматически запускает CS2, подключается к игре и имитирует игровой процесс для 
          фарма кейсов. Во время работы бота ваш компьютер будет занят, так как бот управляет 
          клавиатурой и мышью.
        </p>
      </div>
    </div>
  );
} 
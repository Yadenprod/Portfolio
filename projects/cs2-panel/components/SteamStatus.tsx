import { useState, useEffect } from 'react';
import axios from 'axios';

interface SteamStatusProps {
  accountId: string;
  refreshInterval?: number; // Интервал обновления в миллисекундах
}

interface SteamStatus {
  isLoggedIn: boolean;
  steamId?: string;
  error?: string;
  lastLogin?: string;
}

export default function SteamStatus({ accountId, refreshInterval = 30000 }: SteamStatusProps) {
  const [status, setStatus] = useState<SteamStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.get(`/api/steam/status?accountId=${accountId}`);
      
      if (response.data.success) {
        setStatus(response.data.status);
      } else {
        setError(response.data.message || 'Ошибка при получении статуса');
      }
    } catch (error: any) {
      setError(error.response?.data?.message || 'Ошибка при получении статуса');
    } finally {
      setLoading(false);
    }
  };

  // Инициализация и настройка интервала обновления
  useEffect(() => {
    fetchStatus();

    // Настройка интервала обновления
    const intervalId = setInterval(fetchStatus, refreshInterval);
    
    // Очистка интервала при размонтировании компонента
    return () => clearInterval(intervalId);
  }, [accountId, refreshInterval]);

  if (loading && !status) {
    return <div className="text-gray-500">Загрузка статуса...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  if (!status) {
    return <div className="text-gray-500">Статус недоступен</div>;
  }

  return (
    <div className="space-y-2">
      <h3 className="text-lg font-medium">Статус Steam</h3>
      
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div className="font-medium">Состояние:</div>
        <div>
          {status.isLoggedIn ? (
            <span className="text-green-500">В сети</span>
          ) : (
            <span className="text-gray-500">Не в сети</span>
          )}
        </div>
        
        {status.steamId && (
          <>
            <div className="font-medium">Steam ID:</div>
            <div>{status.steamId}</div>
          </>
        )}
        
        {status.lastLogin && (
          <>
            <div className="font-medium">Последний вход:</div>
            <div>{new Date(status.lastLogin).toLocaleString()}</div>
          </>
        )}
        
        {status.error && (
          <>
            <div className="font-medium">Ошибка:</div>
            <div className="text-red-500">{status.error}</div>
          </>
        )}
      </div>
    </div>
  );
} 
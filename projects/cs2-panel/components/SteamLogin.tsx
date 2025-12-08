import { useState, ChangeEvent } from 'react';
import axios from 'axios';
import { toast } from 'react-hot-toast';

interface SteamLoginProps {
  accountId: string;
  onLoginSuccess?: (status: any) => void;
  onLoginError?: (error: string) => void;
}

export default function SteamLogin({ accountId, onLoginSuccess, onLoginError }: SteamLoginProps) {
  const [loading, setLoading] = useState(false);
  const [steamGuardCode, setSteamGuardCode] = useState('');
  const [showSteamGuard, setShowSteamGuard] = useState(false);
  const [rateLimited, setRateLimited] = useState<{limited: boolean, waitTime?: number}>({ limited: false });
  const [useMobileConfirmation, setUseMobileConfirmation] = useState(false);
  const [waitingForMobile, setWaitingForMobile] = useState(false);
  const [clearingLimit, setClearingLimit] = useState(false);

  const handleLogin = async () => {
    try {
      setLoading(true);
      
      // If using mobile confirmation, use the dedicated endpoint
      const endpoint = useMobileConfirmation ? '/api/steam/login-with-mobile' : '/api/steam/login';
      
      const response = await axios.post(endpoint, {
        accountId,
        steamGuardCode: steamGuardCode || undefined,
      });
      
      if (response.data.success) {
        toast.success('Успешный вход в Steam');
        setShowSteamGuard(false);
        setSteamGuardCode('');
        setRateLimited({ limited: false });
        setWaitingForMobile(false);
        if (onLoginSuccess) {
          onLoginSuccess(response.data.status);
        }
      } else if (response.data.requiresMobileConfirmation || response.data.requiresConfirmation) {
        // Если требуется мобильное подтверждение
        setWaitingForMobile(true);
        toast.success('Подтвердите вход через мобильное приложение Steam');
        // Запускаем проверку статуса каждые 5 секунд
        checkLoginStatus();
      } else if (response.data.requiresSteamGuard) {
        // If Steam Guard is required
        setShowSteamGuard(true);
        toast.error('Требуется код Steam Guard');
      }
    } catch (error: any) {
      const errorResponse = error.response?.data;
      const errorMessage = errorResponse?.message || errorResponse?.error || 'Ошибка при входе в Steam';
      
      // Обработка разных типов ошибок
      if (error.response?.status === 429 && errorResponse?.rateLimited) {
        // Превышение лимита запросов
        setRateLimited({ 
          limited: true, 
          waitTime: errorResponse.waitTime || 15 
        });
        toast.error(`Превышен лимит запросов. Подождите ${errorResponse.waitTime || 15} минут или используйте мобильную аутентификацию`);
      } else if (error.response?.status === 409) {
        // Конфликт - вход уже выполняется
        toast.error('Вход уже выполняется, дождитесь завершения');
      } else if (errorMessage.includes('мобильное') || errorMessage.includes('подтверждение')) {
        // Рекомендация использовать мобильное подтверждение
        setUseMobileConfirmation(true);
        toast.success('Рекомендуется использовать подтверждение через мобильное приложение Steam');
      } else if (errorMessage.includes('Steam Guard') || errorMessage.includes('two-factor')) {
        // Требуется Steam Guard
        setShowSteamGuard(true);
        toast.error('Требуется код Steam Guard');
      } else {
        toast.error(errorMessage);
      }
      
      if (onLoginError) {
        onLoginError(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  // Function to clear rate limits
  const handleClearRateLimit = async () => {
    try {
      setClearingLimit(true);
      
      const response = await axios.post('/api/steam/clear-rate-limit', {
        accountId
      });
      
      if (response.data.success) {
        setRateLimited({ limited: false });
        toast.success(response.data.message || 'Ограничение сброшено');
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Ошибка при сбросе ограничения';
      toast.error(errorMessage);
    } finally {
      setClearingLimit(false);
    }
  };

  // Функция для проверки статуса логина при ожидании мобильного подтверждения
  const checkLoginStatus = async () => {
    if (!waitingForMobile) return;
    
    try {
      const response = await axios.get(`/api/accounts/${accountId}/steam`);
      
      if (response.data.success) {
        const status = response.data.data.status;
        
        if (status.isLoggedIn) {
          // Успешный вход
          toast.success('Вход выполнен успешно через мобильное приложение');
          setWaitingForMobile(false);
          if (onLoginSuccess) {
            onLoginSuccess(status);
          }
          return;
        } else if (!status.requiresMobileConfirmation) {
          // Если мобильное подтверждение больше не требуется, но мы не авторизованы - что-то пошло не так
          setWaitingForMobile(false);
          toast.error('Не удалось войти через мобильное приложение');
          return;
        }
      }
      
      // Продолжаем проверять каждые 5 секунд
      setTimeout(checkLoginStatus, 5000);
    } catch (error) {
      // При ошибке продолжаем проверять
      setTimeout(checkLoginStatus, 5000);
    }
  };

  const handleLogout = async () => {
    try {
      setLoading(true);
      
      const response = await axios.post('/api/steam/logout', {
        accountId
      });
      
      if (response.data.success) {
        toast.success('Выход из Steam выполнен успешно');
        setRateLimited({ limited: false });
        setWaitingForMobile(false);
        if (onLoginSuccess) {
          onLoginSuccess({ isLoggedIn: false });
        }
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Ошибка при выходе из Steam';
      toast.error(errorMessage);
      
      if (onLoginError) {
        onLoginError(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  // Переключатель для опции мобильного подтверждения
  const toggleMobileConfirmation = () => {
    setUseMobileConfirmation(!useMobileConfirmation);
  };

  return (
    <div className="mt-4 space-y-4">
      {showSteamGuard && (
        <div className="space-y-2">
          <label className="block text-sm font-medium">Код Steam Guard</label>
          <input
            type="text"
            value={steamGuardCode}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setSteamGuardCode(e.target.value)}
            maxLength={5}
            placeholder="XXXXX"
            className="px-3 py-2 border rounded-md w-full"
          />
          <p className="text-xs text-gray-500">
            Введите код, который был отправлен на вашу почту или в мобильное приложение Steam.
          </p>
        </div>
      )}

      {rateLimited.limited && (
        <div className="bg-red-100 text-red-800 p-3 rounded-md">
          <p>Превышен лимит запросов к Steam. Подождите {rateLimited.waitTime} минут перед новой попыткой или попробуйте использовать подтверждение через приложение Steam.</p>
          <button
            onClick={handleClearRateLimit}
            disabled={clearingLimit}
            className="mt-2 px-3 py-1 bg-white text-red-800 border border-red-300 rounded-md hover:bg-red-50 disabled:opacity-50"
          >
            {clearingLimit ? 'Сброс...' : 'Сбросить ограничение'}
          </button>
        </div>
      )}

      {waitingForMobile && (
        <div className="bg-blue-100 text-blue-800 p-3 rounded-md">
          <div className="flex items-center">
            <div className="animate-spin mr-2 h-4 w-4 border-t-2 border-b-2 border-blue-800 rounded-full"></div>
            <p>Ожидание подтверждения через мобильное приложение Steam...</p>
          </div>
          <p className="text-xs mt-1">Откройте приложение Steam и подтвердите вход.</p>
        </div>
      )}

      <div className="flex items-center space-x-2">
        <input
          type="checkbox"
          id="mobileConfirmation"
          checked={useMobileConfirmation}
          onChange={toggleMobileConfirmation}
          className="h-4 w-4 text-blue-600"
        />
        <label htmlFor="mobileConfirmation" className="text-sm">
          Использовать подтверждение через мобильное приложение
        </label>
      </div>

      <div className="flex space-x-2">
        <button
          onClick={handleLogin}
          disabled={loading || waitingForMobile}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Загрузка...' : waitingForMobile ? 'Ожидание...' : 'Войти в Steam'}
        </button>
        
        <button
          onClick={handleLogout}
          disabled={loading}
          className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 disabled:opacity-50"
        >
          Выйти из Steam
        </button>
      </div>
    </div>
  );
} 
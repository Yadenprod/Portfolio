const http = require('http');

console.log('🔍 Проверка состояния сервера...\n');

// Функции для проверки разных сервисов
function checkAPI() {
  return new Promise((resolve) => {
    const req = http.request('http://localhost:3000/api/health', { method: 'GET' }, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          resolve({ status: '✅', service: 'API Server', details: response });
        } catch (e) {
          resolve({ status: '❌', service: 'API Server', error: 'Invalid JSON response' });
        }
      });
    });

    req.on('error', (err) => {
      resolve({ status: '❌', service: 'API Server', error: err.message });
    });

    req.setTimeout(5000, () => {
      req.destroy();
      resolve({ status: '❌', service: 'API Server', error: 'Timeout' });
    });

    req.end();
  });
}

function checkWebSocket() {
  return new Promise((resolve) => {
    const WebSocket = require('ws');

    try {
      const ws = new WebSocket('ws://localhost:3000/ws');

      const timeout = setTimeout(() => {
        ws.terminate();
        resolve({ status: '❌', service: 'WebSocket', error: 'Connection timeout' });
      }, 5000);

      ws.on('open', () => {
        clearTimeout(timeout);
        ws.close();
        resolve({ status: '✅', service: 'WebSocket', details: 'Connected successfully' });
      });

      ws.on('error', (error) => {
        clearTimeout(timeout);
        resolve({ status: '❌', service: 'WebSocket', error: error.message });
      });

    } catch (error) {
      resolve({ status: '❌', service: 'WebSocket', error: error.message });
    }
  });
}

function checkCORSProxy() {
  return new Promise((resolve) => {
    // Проверяем CORS proxy с тестовым запросом
    const testUrl = 'http://httpbin.org/get';
    const req = http.request(`http://localhost:3000/api/proxy/${testUrl}`, { method: 'GET' }, (res) => {
      if (res.statusCode === 200) {
        resolve({ status: '✅', service: 'CORS Proxy', details: 'Working' });
      } else {
        resolve({ status: '❌', service: 'CORS Proxy', error: `Status ${res.statusCode}` });
      }
    });

    req.on('error', (err) => {
      resolve({ status: '❌', service: 'CORS Proxy', error: err.message });
    });

    req.setTimeout(5000, () => {
      req.destroy();
      resolve({ status: '❌', service: 'CORS Proxy', error: 'Timeout' });
    });

    req.end();
  });
}

async function checkAllServices() {
  console.log('🖥️  Проверка сервисов...\n');

  const results = await Promise.all([
    checkAPI(),
    checkWebSocket(),
    checkCORSProxy()
  ]);

  console.log('📊 Результаты проверки:\n');

  results.forEach(result => {
    console.log(`${result.status} ${result.service}`);
    if (result.error) {
      console.log(`   Ошибка: ${result.error}`);
    }
    if (result.details) {
      if (typeof result.details === 'object') {
        console.log(`   Детали: ${JSON.stringify(result.details, null, 2)}`);
      } else {
        console.log(`   Детали: ${result.details}`);
      }
    }
    console.log('');
  });

  const allWorking = results.every(r => r.status === '✅');

  if (allWorking) {
    console.log('🎉 Все сервисы работают корректно!');
    console.log('\n🌐 Доступные URL:');
    console.log('   Vue Client: http://localhost:5173');
    console.log('   API Server: http://localhost:3000');
    console.log('   WebSocket: ws://localhost:3000/ws');
    console.log('   Health Check: http://localhost:3000/api/health');
  } else {
    console.log('⚠️  Некоторые сервисы не работают.');
    console.log('\n🔧 Возможные решения:');
    console.log('   1. Убедитесь, что сервер запущен: npm run server');
    console.log('   2. Проверьте, что порт 3000 свободен');
    console.log('   3. Перезапустите сервер');
  }
}

// Запуск проверки
checkAllServices().catch(console.error);

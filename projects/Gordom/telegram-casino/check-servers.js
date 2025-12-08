#!/usr/bin/env node

// Скрипт для проверки состояния серверов Telegram Casino

const axios = require('axios')

async function checkServers() {
  console.log('🔍 Проверка состояния серверов...\n')

  const servers = [
    {
      name: 'Laravel Backend',
      url: 'http://localhost:8000',
      endpoint: '/api/health'
    },
    {
      name: 'Node.js WebSocket',
      url: 'http://localhost:8443',
      endpoint: '/health'
    },
    {
      name: 'Telegram Web App',
      url: 'http://localhost:3000',
      endpoint: '/'
    }
  ]

  for (const server of servers) {
    try {
      console.log(`📡 Проверка ${server.name}...`)

      const response = await axios.get(server.url + server.endpoint, {
        timeout: 5000,
        validateStatus: function (status) {
          return status < 500 // Принимаем все статусы кроме 5xx ошибок сервера
        }
      })

      console.log(`✅ ${server.name}: Доступен (статус: ${response.status})`)
      console.log(`   URL: ${server.url}\n`)

    } catch (error) {
      console.log(`❌ ${server.name}: Недоступен`)
      console.log(`   Ошибка: ${error.code || error.message}\n`)

      if (server.name === 'Laravel Backend') {
        console.log('💡 Возможные решения:')
        console.log('   1. Убедитесь, что запущен: php artisan serve --host=0.0.0.0 --port=8000')
        console.log('   2. Проверьте .env файл на корректность')
        console.log('   3. Убедитесь, что база данных SQLite существует')
        console.log('')
      }

      if (server.name === 'Node.js WebSocket') {
        console.log('💡 Возможные решения:')
        console.log('   1. Убедитесь, что запущен: node app.js в папке server/')
        console.log('   2. Проверьте, что порт 8443 не занят')
        console.log('')
      }

      if (server.name === 'Telegram Web App') {
        console.log('💡 Возможные решения:')
        console.log('   1. Убедитесь, что запущен: npm run dev в папке telegram-casino/')
        console.log('   2. Проверьте, что порт 3000 не занят')
        console.log('')
      }
    }
  }

  console.log('🎯 Инструкции по запуску:')
  console.log('')
  console.log('1. Laravel Backend:')
  console.log('   cd E:\\Gordom')
  console.log('   php artisan serve --host=0.0.0.0 --port=8000')
  console.log('')
  console.log('2. Node.js WebSocket:')
  console.log('   cd E:\\Gordom\\server')
  console.log('   node app.js')
  console.log('')
  console.log('3. Telegram Web App:')
  console.log('   cd telegram-casino')
  console.log('   npm run dev')
  console.log('')
  console.log('🌐 После запуска откройте: http://localhost:3000')
}

// Запуск проверки
checkServers().catch(console.error)

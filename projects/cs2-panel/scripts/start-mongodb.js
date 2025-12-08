const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Директория для данных MongoDB
const dbPath = path.join(__dirname, '..', 'data', 'db');
const logPath = path.join(__dirname, '..', 'data', 'logs');

// Создаем директории, если они не существуют
if (!fs.existsSync(dbPath)) {
  fs.mkdirSync(dbPath, { recursive: true });
  console.log(`Создана директория для базы данных: ${dbPath}`);
}

if (!fs.existsSync(logPath)) {
  fs.mkdirSync(logPath, { recursive: true });
  console.log(`Создана директория для логов: ${logPath}`);
}

// Настройки сервера MongoDB
const mongodbPort = 27017;
const logFile = path.join(logPath, 'mongodb.log');

// Проверка, запущен ли уже MongoDB на этом порту
const netstat = spawn('netstat', ['-an']);
let isPortInUse = false;

netstat.stdout.on('data', (data) => {
  const output = data.toString();
  if (output.includes(`:${mongodbPort}`)) {
    isPortInUse = true;
  }
});

netstat.on('close', () => {
  if (isPortInUse) {
    console.log(`MongoDB уже запущен на порту ${mongodbPort}.`);
    console.log('Используйте существующий сервер MongoDB.');
    return;
  }

  // Запускаем MongoDB с указанной конфигурацией
  console.log('Запуск MongoDB...');
  
  // Команда запуска зависит от платформы и способа установки MongoDB
  // Этот пример предполагает использование mongod из системного пути
  const mongod = spawn('mongod', [
    '--dbpath', dbPath,
    '--port', mongodbPort.toString(),
    '--logpath', logFile,
    '--logappend'
  ]);

  mongod.stdout.on('data', (data) => {
    console.log(`MongoDB: ${data.toString()}`);
  });

  mongod.stderr.on('data', (data) => {
    console.error(`MongoDB ошибка: ${data.toString()}`);
  });

  mongod.on('close', (code) => {
    if (code !== 0) {
      console.log(`MongoDB завершил работу с кодом ${code}`);
    }
  });

  console.log(`MongoDB запущен на порту ${mongodbPort}`);
  console.log(`Данные хранятся в: ${dbPath}`);
  console.log(`Логи записываются в: ${logFile}`);
  console.log('Нажмите Ctrl+C для остановки сервера.');
  
  // Обрабатываем завершение процесса
  process.on('SIGINT', () => {
    console.log('Останавливаем MongoDB...');
    mongod.kill('SIGINT');
    process.exit();
  });
}); 
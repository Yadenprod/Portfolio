const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Цвета для вывода в консоль
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
};

console.log(`${colors.blue}Начинаем установку CS2 Панели управления...${colors.reset}\n`);

// Проверяем наличие Node.js и npm
try {
  const nodeVersion = execSync('node -v').toString().trim();
  const npmVersion = execSync('npm -v').toString().trim();
  
  console.log(`${colors.green}✓ Node.js: ${nodeVersion}${colors.reset}`);
  console.log(`${colors.green}✓ npm: ${npmVersion}${colors.reset}\n`);
} catch (error) {
  console.error(`${colors.red}✗ Ошибка: Node.js или npm не установлены.${colors.reset}`);
  console.error(`${colors.yellow}Пожалуйста, установите Node.js с сайта: https://nodejs.org/${colors.reset}`);
  process.exit(1);
}

// Устанавливаем зависимости
console.log(`${colors.blue}Устанавливаем зависимости...${colors.reset}`);
try {
  execSync('npm install', { stdio: 'inherit' });
  console.log(`${colors.green}✓ Зависимости установлены успешно${colors.reset}\n`);
} catch (error) {
  console.error(`${colors.red}✗ Ошибка при установке зависимостей${colors.reset}`);
  process.exit(1);
}

// Проверяем наличие .env.local, если нет - создаем из примера
const envPath = path.join(process.cwd(), '.env.local');
const envExamplePath = path.join(process.cwd(), '.env.example');

if (!fs.existsSync(envPath) && fs.existsSync(envExamplePath)) {
  console.log(`${colors.yellow}Файл .env.local не найден. Создаем из примера...${colors.reset}`);
  
  try {
    fs.copyFileSync(envExamplePath, envPath);
    console.log(`${colors.green}✓ Файл .env.local создан${colors.reset}`);
    console.log(`${colors.yellow}⚠ Не забудьте отредактировать .env.local с вашими настройками!${colors.reset}\n`);
  } catch (error) {
    console.error(`${colors.red}✗ Ошибка при создании .env.local${colors.reset}`);
  }
} else {
  console.log(`${colors.green}✓ Файл .env.local найден${colors.reset}\n`);
}

// Запускаем приложение
console.log(`${colors.blue}Запускаем приложение...${colors.reset}`);
console.log(`${colors.green}CS2 Panel будет доступен по адресу: http://localhost:3000${colors.reset}\n`);

try {
  execSync('npm run dev', { stdio: 'inherit' });
} catch (error) {
  console.error(`${colors.red}✗ Ошибка при запуске приложения${colors.reset}`);
  process.exit(1);
} 
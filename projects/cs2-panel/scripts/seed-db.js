const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

// URI подключения к MongoDB из переменных окружения
const MONGODB_URI = process.env.MONGODB_URI || "mongodb://localhost:27017/cspanel";

// Определяем схему пользователя для скрипта
const UserSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  role: { 
    type: String, 
    enum: ['admin', 'user'], 
    default: 'user' 
  }
}, 
{ timestamps: true });

// Определяем схему аккаунта для скрипта
const AccountSchema = new mongoose.Schema({
  username: { type: String, required: true },
  password: { type: String, required: true },
  steamGuardCode: { type: String, default: '' },
  sharedSecret: { type: String, default: '' },
  casesCollected: { type: Number, default: 0 },
  lastLogin: { type: Date, default: null },
  status: { 
    type: String, 
    enum: ['active', 'banned', 'inactive'], 
    default: 'inactive' 
  },
  notes: { type: String, default: '' },
  proxySetting: { type: String, default: '' },
  user: { 
    type: mongoose.Schema.Types.ObjectId, 
    ref: 'User',
    required: true
  }
}, 
{ timestamps: true });

// Создаем индекс по комбинации пользователя и имени пользователя Steam
AccountSchema.index({ user: 1, username: 1 }, { unique: true });

// Создаем модели
const User = mongoose.model('User', UserSchema);
const Account = mongoose.model('Account', AccountSchema);

async function seedDatabase() {
  try {
    // Подключаемся к базе данных
    await mongoose.connect(MONGODB_URI);
    console.log('Подключение к MongoDB установлено');

    // Очищаем существующие коллекции
    await User.deleteMany({});
    await Account.deleteMany({});
    console.log('Существующие данные очищены');

    // Создаем администратора
    const adminPassword = await bcrypt.hash('admin123', 10);
    const admin = await User.create({
      name: 'Администратор',
      email: 'admin@example.com',
      password: adminPassword,
      role: 'admin'
    });
    console.log('Создан администратор:', admin.email);

    // Создаем обычного пользователя
    const userPassword = await bcrypt.hash('user123', 10);
    const user = await User.create({
      name: 'Пользователь',
      email: 'user@example.com',
      password: userPassword,
      role: 'user'
    });
    console.log('Создан пользователь:', user.email);

    // Создаем тестовые аккаунты для администратора
    const adminAccounts = [
      {
        username: 'admin_account1',
        password: 'pass123',
        steamGuardCode: '',
        sharedSecret: '',
        casesCollected: 12,
        lastLogin: new Date(),
        status: 'active',
        notes: 'Тестовый аккаунт администратора 1',
        proxySetting: '',
        user: admin._id
      },
      {
        username: 'admin_account2',
        password: 'pass456',
        steamGuardCode: '',
        sharedSecret: '',
        casesCollected: 5,
        lastLogin: new Date(),
        status: 'inactive',
        notes: 'Тестовый аккаунт администратора 2',
        proxySetting: '',
        user: admin._id
      }
    ];

    await Account.insertMany(adminAccounts);
    console.log(`Создано ${adminAccounts.length} аккаунтов для администратора`);

    // Создаем тестовые аккаунты для обычного пользователя
    const userAccounts = [
      {
        username: 'user_account1',
        password: 'pass789',
        steamGuardCode: '',
        sharedSecret: '',
        casesCollected: 3,
        lastLogin: new Date(),
        status: 'active',
        notes: 'Тестовый аккаунт пользователя',
        proxySetting: '',
        user: user._id
      }
    ];

    await Account.insertMany(userAccounts);
    console.log(`Создано ${userAccounts.length} аккаунтов для пользователя`);

    console.log('База данных успешно заполнена');
  } catch (error) {
    console.error('Ошибка при заполнении базы данных:', error);
  } finally {
    // Закрываем соединение с базой данных
    await mongoose.connection.close();
    console.log('Соединение с базой данных закрыто');
  }
}

// Запускаем заполнение базы данных
seedDatabase(); 
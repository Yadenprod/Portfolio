import mongoose from 'mongoose';
import path from 'path';

// Получаем путь к сертификату X509
const X509_CERT_PATH = path.resolve(process.cwd(), 'X509-cert-7070748032059209805.pem');

// Напрямую задаем строку подключения
const MONGODB_URI = "mongodb+srv://cluster0.twpmlgr.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=Cluster0";

// Опции подключения с сертификатом X509
const options: mongoose.ConnectOptions = {
  tls: true,
  tlsCertificateKeyFile: X509_CERT_PATH,
  authMechanism: 'MONGODB-X509' as any,
  authSource: '$external'
};

// Интерфейс для глобальной переменной
interface GlobalMongo {
  conn: mongoose.Connection | null;
  promise: Promise<mongoose.Connection> | null;
}

// Объявление глобальной переменной
declare global {
  var mongooseConnection: GlobalMongo | undefined;
}

// Инициализация глобальной переменной
if (!global.mongooseConnection) {
  global.mongooseConnection = { conn: null, promise: null };
}

/**
 * Функция подключения к базе данных
 */
async function dbConnect(): Promise<mongoose.Connection> {
  if (global.mongooseConnection!.conn) {
    return global.mongooseConnection!.conn;
  }

  if (!global.mongooseConnection!.promise) {
    // Создаем соединение
    global.mongooseConnection!.promise = mongoose.connect(MONGODB_URI, options)
      .then((mongoose) => {
        console.log('MongoDB подключена успешно с использованием X509 сертификата');
        return mongoose.connection;
      });
  }

  try {
    const conn = await global.mongooseConnection!.promise;
    global.mongooseConnection!.conn = conn;
    return conn;
  } catch (error) {
    console.error('Ошибка подключения к MongoDB:', error);
    throw error;
  }
}

export default dbConnect; 
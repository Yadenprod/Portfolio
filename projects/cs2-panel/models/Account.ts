import mongoose, { Schema, Document } from 'mongoose';

export interface IAccount extends Document {
  _id: mongoose.Types.ObjectId;
  username: string;
  password: string;
  steamGuardCode?: string;
  sharedSecret?: string;
  casesCollected: number;
  lastLogin: Date | null;
  status: 'active' | 'banned' | 'inactive';
  botStatus?: 'active' | 'inactive';
  lastBotStart?: Date;
  lastBotStop?: Date;
  notes?: string;
  proxySetting?: string;
  user: mongoose.Types.ObjectId;
  createdAt: Date;
  updatedAt: Date;
}

const AccountSchema: Schema = new Schema(
  {
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
    botStatus: {
      type: String,
      enum: ['active', 'inactive'],
      default: 'inactive'
    },
    lastBotStart: { type: Date, default: null },
    lastBotStop: { type: Date, default: null },
    notes: { type: String, default: '' },
    proxySetting: { type: String, default: '' },
    user: { 
      type: mongoose.Schema.Types.ObjectId, 
      ref: 'User',
      required: true
    },
  },
  { timestamps: true }
);

// Создаем индекс по комбинации пользователя и имени пользователя Steam
// для обеспечения уникальности в рамках одного пользователя
AccountSchema.index({ user: 1, username: 1 }, { unique: true });

// Добавляем логгирование при сохранении аккаунта
AccountSchema.pre('save', function(next) {
  console.log(`Сохранение аккаунта ${this._id ? 'существующего' : 'нового'}: ${this.username}`);
  next();
});

// Обработчик ошибок для MongoDB
AccountSchema.post('save', function(error: any, doc: any, next: any) {
  if (error.name === 'MongoServerError' && error.code === 11000) {
    console.error('Ошибка дубликата индекса:', error);
    next(new Error('Аккаунт с таким именем пользователя уже существует'));
  } else {
    next(error);
  }
});

const AccountModel = mongoose.models.Account || mongoose.model<IAccount>('Account', AccountSchema);
export default AccountModel; 
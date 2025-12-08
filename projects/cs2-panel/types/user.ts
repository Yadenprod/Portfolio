import { Account } from './account';

export interface User {
  _id: string;
  name: string;
  email: string;
  password?: string;
  role: 'admin' | 'user';
  accounts?: Account[];
  createdAt?: Date;
  updatedAt?: Date;
}

export interface Session {
  user: {
    id: string;
    name: string;
    email: string;
    role: 'admin' | 'user';
  };
  expires: string;
} 
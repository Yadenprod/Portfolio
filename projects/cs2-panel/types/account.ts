export interface Account {
  _id: string;
  username: string;
  password: string;
  steamGuardCode?: string;
  sharedSecret?: string;
  casesCollected: number;
  lastLogin?: Date | null;
  status: 'active' | 'inactive' | 'banned';
  notes?: string;
  proxySetting?: string;
  createdAt?: Date;
  updatedAt?: Date;
} 
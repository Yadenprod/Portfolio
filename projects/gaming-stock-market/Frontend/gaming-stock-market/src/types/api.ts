export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  expiration: string;
  refreshToken: string;
}

export interface RefreshTokenRequest {
  refreshToken: string;
}

export interface VerifyEmailRequest {
  token: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  newPassword: string;
}

export interface PlayerResponse {
  id: number;
  name: string;
  game: string;
  team?: string;
  currentPrice: number;
  rating?: number;
  popularityScore: number;
}

export interface TeamResponse {
  id: number;
  name: string;
  game: string;
  currentPrice: number;
  ranking?: number;
}

export type OrderType = 'Buy' | 'Sell';
export type OrderStatus = 'Pending' | 'PartiallyFilled' | 'Filled' | 'Cancelled';

export interface PlaceOrderRequest {
  playerId?: number;
  teamId?: number;
  type: OrderType;
  shares: number;
  price: number;
}

export interface OrderResponse {
  orderId: number;
  status: OrderStatus;
  filledShares: number;
}

export interface OrderBookResponse {
  playerId?: number;
  teamId?: number;
  buyOrders: Order[];
  sellOrders: Order[];
}

export interface Order {
  id: number;
  userId: number;
  playerId?: number;
  teamId?: number;
  type: OrderType;
  shares: number;
  price: number;
  status: OrderStatus;
  filledShares: number;
  createdAt: string;
  updatedAt: string;
}

export interface UserPortfolio {
  id: number;
  userId: number;
  playerId?: number;
  teamId?: number;
  shares: number;
  averagePrice: number;
  createdAt: string;
  updatedAt: string;
  player?: PlayerResponse; // Optional: include player details
  team?: TeamResponse;   // Optional: include team details
}

export interface PortfolioResponse {
  userId: number;
  balance: number;
  holdings: UserPortfolio[];
  totalValue: number;
}

export interface Trade {
  id: number;
  buyOrderId: number;
  sellOrderId: number;
  playerId?: number;
  teamId?: number;
  shares: number;
  price: number;
  commission: number;
  createdAt: string;
}

export interface NotificationResponse {
  id: number;
  type: string;
  message: string;
  isRead: boolean;
  createdAt: string;
}

export interface AchievementResponse {
  id: number;
  name: string;
  description: string;
  achievedAt: string | null;
  rewardAmount: number;
  type: string;
}

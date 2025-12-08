import { createSlice, type PayloadAction } from '@reduxjs/toolkit';
import type { OrderResponse, PlayerResponse, TeamResponse } from 'types/api'; // Updated path

export interface Order {
  id: number;
  type: 'Buy' | 'Sell';
  shares: number;
  price: number;
  status: string;
}

export interface Trade {
  id: number;
  buyOrderId: number; // Keep buyOrderId
  sellOrderId: number; // Keep sellOrderId
  playerId?: number; // Added from types/api.ts
  teamId?: number;   // Added from types/api.ts
  shares: number;
  price: number;
  commission: number;
  createdAt: string;
}

export interface UserPortfolio {
  playerId?: number;
  teamId?: number;
  shares: number;
  averagePrice: number;
  player?: PlayerResponse; // Added from types/api.ts
  team?: TeamResponse;   // Added from types/api.ts
}

interface TradingState {
  openOrders: Order[];
  tradeHistory: Trade[];
  userPortfolio: UserPortfolio[];
  loading: boolean;
  error: string | null;
}

const initialState: TradingState = {
  openOrders: [],
  tradeHistory: [],
  userPortfolio: [],
  loading: false,
  error: null,
};

const tradingSlice = createSlice({
  name: 'trading',
  initialState,
  reducers: {
    fetchOrdersStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchOrdersSuccess: (state, action: PayloadAction<Order[]>) => {
      state.openOrders = action.payload;
      state.loading = false;
    },
    fetchOrdersFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    placeOrderStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    placeOrderSuccess: (state, action: PayloadAction<OrderResponse>) => {
      // For simplicity, we'll add a dummy order based on OrderResponse
      const newOrder: Order = {
        id: action.payload.orderId,
        type: 'Buy', // This should ideally come from the original request or API response
        shares: action.payload.filledShares, // Assuming filledShares is initially what was ordered
        price: 0, // Price is not directly in OrderResponse, need to refine API or infer
        status: action.payload.status,
      };
      state.openOrders.push(newOrder);
      state.loading = false;
    },
    placeOrderFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    cancelOrderStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    cancelOrderSuccess: (state, action: PayloadAction<number>) => {
      state.openOrders = state.openOrders.filter(order => order.id !== action.payload);
      state.loading = false;
    },
    cancelOrderFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    fetchTradeHistoryStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchTradeHistorySuccess: (state, action: PayloadAction<Trade[]>) => {
      state.tradeHistory = action.payload;
      state.loading = false;
    },
    fetchTradeHistoryFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    fetchUserPortfolioStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchUserPortfolioSuccess: (state, action: PayloadAction<UserPortfolio[]>) => {
      state.userPortfolio = action.payload;
      state.loading = false;
    },
    fetchUserPortfolioFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
  },
});

export const { 
  fetchOrdersStart, fetchOrdersSuccess, fetchOrdersFailure, 
  placeOrderStart, placeOrderSuccess, placeOrderFailure, 
  cancelOrderStart, cancelOrderSuccess, cancelOrderFailure,
  fetchTradeHistoryStart, fetchTradeHistorySuccess, fetchTradeHistoryFailure,
  fetchUserPortfolioStart, fetchUserPortfolioSuccess, fetchUserPortfolioFailure,
} = tradingSlice.actions;

export default tradingSlice.reducer;

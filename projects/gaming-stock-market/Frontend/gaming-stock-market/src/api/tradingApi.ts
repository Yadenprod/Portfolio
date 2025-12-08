import api from 'api/api';
import type { PlaceOrderRequest, OrderResponse, OrderBookResponse, PortfolioResponse, Trade } from 'types/api';

export const tradingApi = {
  placeOrder: (data: PlaceOrderRequest) => api.post<OrderResponse>('/Trading/place-order', data),
  cancelOrder: (orderId: number) => api.post(`/Trading/cancel-order/${orderId}`),
  getOrderBook: (playerId?: number, teamId?: number) => 
    api.get<OrderBookResponse>('/Trading/order-book', { params: { playerId, teamId } }),
  getPortfolio: () => api.get<PortfolioResponse>('/Trading/portfolio'),
  getTradeHistory: (pageNumber?: number, pageSize?: number) => 
    api.get<Trade[]>('/Trading/trade-history', { params: { pageNumber, pageSize } }),
};

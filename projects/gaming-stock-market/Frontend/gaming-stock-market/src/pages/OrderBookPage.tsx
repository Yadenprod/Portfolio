import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from 'store'; // Updated path
import { fetchOrdersStart, fetchOrdersSuccess, fetchOrdersFailure, placeOrderStart, placeOrderSuccess, placeOrderFailure, cancelOrderStart, cancelOrderSuccess, cancelOrderFailure } from 'slices/tradingSlice'; // Updated path
import { tradingApi } from 'api/tradingApi'; // Updated path
import type { PlaceOrderRequest, OrderType } from 'types/api'; // Updated path
import type { Order } from 'slices/tradingSlice'; // Updated path
import LoadingSpinner from 'components/LoadingSpinner'; // Updated path
import Input from 'components/Input'; // Updated path
import Button from 'components/Button'; // Updated path
import Modal from 'components/Modal'; // Updated path

const OrderBookPage: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const { openOrders, loading, error } = useSelector((state: RootState) => state.trading);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [orderType, setOrderType] = useState<OrderType>('Buy');
  const [assetId, setAssetId] = useState<string>('');
  const [shares, setShares] = useState<number>(1);
  const [price, setPrice] = useState<number>(0.01);

  useEffect(() => {
    const getOrderBook = async () => {
      dispatch(fetchOrdersStart());
      try {
        const response = await tradingApi.getOrderBook();
        // The API returns OrderBookResponse, which contains buyOrders and sellOrders
        // We'll combine them for simplicity here, or display separately in UI
        const allOrders = [...response.data.buyOrders, ...response.data.sellOrders];
        dispatch(fetchOrdersSuccess(allOrders));
      } catch (err: any) {
        dispatch(fetchOrdersFailure(err.response?.data?.message || 'Failed to fetch order book.'));
      }
    };
    getOrderBook();
  }, [dispatch]);

  const handlePlaceOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    dispatch(placeOrderStart());
    try {
      const request: PlaceOrderRequest = {
        type: orderType,
        shares,
        price,
        // Assuming assetId can be either playerId or teamId based on context
        // For simplicity, let's assume it's a playerId for now.
        playerId: parseInt(assetId) // Needs proper handling for player vs team
      };
      const response = await tradingApi.placeOrder(request);
      dispatch(placeOrderSuccess(response.data)); // Now expects OrderResponse
      setIsModalOpen(false);
      // Refresh order book after placing order
      const refreshResponse = await tradingApi.getOrderBook();
      const allOrders = [...refreshResponse.data.buyOrders, ...refreshResponse.data.sellOrders];
      dispatch(fetchOrdersSuccess(allOrders));
    } catch (err: any) {
      dispatch(placeOrderFailure(err.response?.data?.message || 'Failed to place order.'));
    }
  };

  const handleCancelOrder = async (orderId: number) => {
    dispatch(cancelOrderStart());
    try {
      await tradingApi.cancelOrder(orderId);
      dispatch(cancelOrderSuccess(orderId));
      // Refresh order book after cancelling order
      const refreshResponse = await tradingApi.getOrderBook();
      const allOrders = [...refreshResponse.data.buyOrders, ...refreshResponse.data.sellOrders];
      dispatch(fetchOrdersSuccess(allOrders));
    } catch (err: any) {
      dispatch(cancelOrderFailure(err.response?.data?.message || 'Failed to cancel order.'));
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500 text-center mt-8">Error: {error}</div>;

  const buyOrders = openOrders.filter((order: Order) => order.type === 'Buy').sort((a: Order, b: Order) => b.price - a.price);
  const sellOrders = openOrders.filter((order: Order) => order.type === 'Sell').sort((a: Order, b: Order) => a.price - b.price);

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-white mb-6">Order Book</h1>
      <Button onClick={() => setIsModalOpen(true)} className="mb-4">Place New Order</Button>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Buy Orders */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-4">Buy Orders</h2>
          {buyOrders.length === 0 ? (
            <p className="text-gray-400">No buy orders currently.</p>
          ) : (
            <ul className="space-y-2">
              {buyOrders.map((order: Order) => (
                <li key={order.id} className="flex justify-between items-center bg-gray-700 p-3 rounded">
                  <span>{order.shares} shares @ ${order.price.toFixed(2)}</span>
                  <Button variant="danger" size="sm" onClick={() => handleCancelOrder(order.id)}>Cancel</Button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Sell Orders */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-4">Sell Orders</h2>
          {sellOrders.length === 0 ? (
            <p className="text-gray-400">No sell orders currently.</p>
          ) : (
            <ul className="space-y-2">
              {sellOrders.map((order: Order) => (
                <li key={order.id} className="flex justify-between items-center bg-gray-700 p-3 rounded">
                  <span>{order.shares} shares @ ${order.price.toFixed(2)}</span>
                  <Button variant="danger" size="sm" onClick={() => handleCancelOrder(order.id)}>Cancel</Button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Place New Order">
        <form onSubmit={handlePlaceOrder}>
          <div className="mb-4">
            <label htmlFor="orderType" className="block text-gray-300 text-sm font-bold mb-2">Order Type</label>
            <select 
              id="orderType" 
              className="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 border-gray-600 text-white"
              value={orderType}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setOrderType(e.target.value as OrderType)}
            >
              <option value="Buy">Buy</option>
              <option value="Sell">Sell</option>
            </select>
          </div>
          <Input
            label="Asset ID (Player/Team ID)"
            id="assetId"
            type="number"
            value={assetId}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setAssetId(e.target.value)}
            required
            className="bg-gray-700 border-gray-600 text-white"
          />
          <Input
            label="Shares"
            id="shares"
            type="number"
            value={shares}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setShares(parseInt(e.target.value))}
            required
            min="1"
            className="bg-gray-700 border-gray-600 text-white"
          />
          <Input
            label="Price"
            id="price"
            type="number"
            step="0.01"
            value={price}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPrice(parseFloat(e.target.value))}
            required
            min="0.01"
            className="bg-gray-700 border-gray-600 text-white"
          />
          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
          <div className="flex justify-end space-x-2 mt-4">
            <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
            <Button type="submit" loading={loading}>Place Order</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default OrderBookPage;

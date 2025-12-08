import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Order {
  id: number;
  userId: number;
  username: string; // Assuming we can fetch username
  assetType: 'Player' | 'Team';
  assetName: string; // Assuming we can fetch asset name
  type: 'Buy' | 'Sell';
  shares: number;
  price: number;
  status: string;
  createdAt: string;
}

const OrderManagement: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const response = await axios.get<Order[]>('http://localhost:5000/api/admin/orders'); // Adjust API endpoint
      setOrders(response.data);
    } catch (err) {
      setError('Failed to fetch orders.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelOrder = async (orderId: number) => {
    if (window.confirm('Are you sure you want to cancel this order?')) {
      try {
        await axios.put(`http://localhost:5000/api/admin/orders/${orderId}/cancel`); // Adjust API endpoint
        fetchOrders();
      } catch (err) {
        setError('Failed to cancel order.');
        console.error(err);
      }
    }
  };

  if (loading) return <div className="text-center text-white">Loading orders...</div>;
  if (error) return <div className="text-center text-red-500">Error: {error}</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6 text-indigo-400">Order Management</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-gray-800 rounded-lg shadow-md">
          <thead>
            <tr className="bg-gray-700">
              <th className="py-3 px-4 text-left">ID</th>
              <th className="py-3 px-4 text-left">User</th>
              <th className="py-3 px-4 text-left">Asset Type</th>
              <th className="py-3 px-4 text-left">Asset Name</th>
              <th className="py-3 px-4 text-left">Type</th>
              <th className="py-3 px-4 text-left">Shares</th>
              <th className="py-3 px-4 text-left">Price</th>
              <th className="py-3 px-4 text-left">Status</th>
              <th className="py-3 px-4 text-left">Created At</th>
              <th className="py-3 px-4 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id} className="border-b border-gray-700 last:border-b-0">
                <td className="py-3 px-4">{order.id}</td>
                <td className="py-3 px-4">{order.username} (ID: {order.userId})</td>
                <td className="py-3 px-4">{order.assetType}</td>
                <td className="py-3 px-4">{order.assetName}</td>
                <td className="py-3 px-4">{order.type}</td>
                <td className="py-3 px-4">{order.shares}</td>
                <td className="py-3 px-4">{order.price.toFixed(2)}</td>
                <td className="py-3 px-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                    order.status === 'Pending' ? 'bg-yellow-500' :
                    order.status === 'Filled' ? 'bg-green-500' :
                    'bg-red-500'
                  }`}>
                    {order.status}
                  </span>
                </td>
                <td className="py-3 px-4">{new Date(order.createdAt).toLocaleDateString()}</td>
                <td className="py-3 px-4">
                  {order.status === 'Pending' && (
                    <button
                      onClick={() => handleCancelOrder(order.id)}
                      className="px-4 py-2 rounded-md text-white bg-red-600 hover:bg-red-700"
                    >
                      Cancel
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default OrderManagement;

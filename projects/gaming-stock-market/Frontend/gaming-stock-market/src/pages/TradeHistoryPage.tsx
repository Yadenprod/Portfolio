import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from 'store'; // Updated path
import { fetchTradeHistoryStart, fetchTradeHistorySuccess, fetchTradeHistoryFailure } from 'slices/tradingSlice'; // Updated path
import { tradingApi } from 'api/tradingApi'; // Updated path
import LoadingSpinner from 'components/LoadingSpinner'; // Updated path
import type { Trade } from 'slices/tradingSlice'; // Updated path

const TradeHistoryPage: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const { tradeHistory, loading, error } = useSelector((state: RootState) => state.trading);

  useEffect(() => {
    const getTradeHistory = async () => {
      dispatch(fetchTradeHistoryStart());
      try {
        const response = await tradingApi.getTradeHistory();
        dispatch(fetchTradeHistorySuccess(response.data));
      } catch (err: any) {
        dispatch(fetchTradeHistoryFailure(err.response?.data?.message || 'Failed to fetch trade history.'));
      }
    };
    getTradeHistory();
  }, [dispatch]);

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500 text-center mt-8">Error: {error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-white mb-6">Trade History</h1>
      {tradeHistory.length === 0 ? (
        <p className="text-gray-400 text-center">No trade history available.</p>
      ) : (
        <div className="overflow-x-auto bg-gray-800 rounded-lg shadow-lg p-4">
          <table className="min-w-full divide-y divide-gray-700">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Trade ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Asset ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Shares</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Price</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Commission</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {tradeHistory.map((trade: Trade) => (
                <tr key={trade.id} className="hover:bg-gray-700">
                  <td className="px-6 py-4 whitespace-nowrap text-white">{trade.id}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-white">{trade.playerId || trade.teamId}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-white">{trade.shares}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-white">${trade.price.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-white">${trade.commission.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-white">{new Date(trade.createdAt).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default TradeHistoryPage;

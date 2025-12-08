import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from 'store'; // Updated path
import { fetchUserPortfolioStart, fetchUserPortfolioSuccess, fetchUserPortfolioFailure } from 'slices/tradingSlice'; // Updated path
import { tradingApi } from 'api/tradingApi'; // Updated path
import LoadingSpinner from 'components/LoadingSpinner'; // Updated path
import type { UserPortfolio } from 'slices/tradingSlice'; // Updated path

const PortfolioPage: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const { userPortfolio, loading, error } = useSelector((state: RootState) => state.trading);

  useEffect(() => {
    const getPortfolio = async () => {
      dispatch(fetchUserPortfolioStart());
      try {
        const response = await tradingApi.getPortfolio();
        // The API response for getPortfolio is PortfolioResponse which has holdings array
        dispatch(fetchUserPortfolioSuccess(response.data.holdings));
      } catch (err: any) {
        dispatch(fetchUserPortfolioFailure(err.response?.data?.message || 'Failed to fetch portfolio.'));
      }
    };
    getPortfolio();
  }, [dispatch]);

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500 text-center mt-8">Error: {error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-white mb-6">My Portfolio</h1>
      {userPortfolio.length === 0 ? (
        <p className="text-gray-400 text-center">Your portfolio is empty. Start trading!</p>
      ) : (
        <div className="overflow-x-auto bg-gray-800 rounded-lg shadow-lg p-4">
          <table className="min-w-full divide-y divide-gray-700">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Asset</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Shares</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Average Price</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Current Price</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Total Value</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Profit/Loss</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {userPortfolio.map((holding: UserPortfolio) => (
                <tr key={holding.playerId || holding.teamId} className="hover:bg-gray-700">
                  <td className="px-6 py-4 whitespace-nowrap text-white">
                    {holding.playerId ? holding.player?.name : holding.team?.name} 
                    <span className="text-gray-500 text-sm">({holding.playerId ? 'Player' : 'Team'})</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-white">{holding.shares}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-white">${holding.averagePrice.toFixed(2)}</td>
                  {/* Assuming current price is not directly in holding, would fetch from player/team state or API */}
                  <td className="px-6 py-4 whitespace-nowrap text-white">--</td> 
                  <td className="px-6 py-4 whitespace-nowrap text-white">--</td>
                  <td className="px-6 py-4 whitespace-nowrap text-white">--</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default PortfolioPage;

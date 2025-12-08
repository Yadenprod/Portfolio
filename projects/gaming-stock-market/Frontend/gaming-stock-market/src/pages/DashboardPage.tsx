import React from 'react';

const DashboardPage: React.FC = () => {
  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-white mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Example Dashboard Widgets */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-4">Total Portfolio Value</h2>
          <p className="text-green-400 text-4xl font-bold">$12,345.67</p>
        </div>

        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-4">Recent Trades</h2>
          <ul className="text-gray-300">
            <li className="mb-2">Bought PlayerX - $100.00</li>
            <li className="mb-2">Sold TeamY - $250.00</li>
            <li>Bought PlayerZ - $50.00</li>
          </ul>
        </div>

        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-4">Notifications</h2>
          <ul className="text-gray-300">
            <li className="mb-2">New achievement unlocked!</li>
            <li className="mb-2">Price alert for PlayerA.</li>
            <li>Your order for TeamB was filled.</li>
          </ul>
        </div>
      </div>
      {/* Further sections like charts, market movers etc. */}
    </div>
  );
};

export default DashboardPage;

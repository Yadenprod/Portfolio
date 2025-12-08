import React from 'react';

const AdminPage: React.FC = () => {
  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-white mb-6">Admin Panel</h1>
      <p className="text-gray-300">Welcome to the Admin Panel. Here you can manage users, players, teams, orders, and view analytics.</p>
      {/* TODO: Add links to different admin sections */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-3">User Management</h2>
          <ul className="text-gray-300">
            <li><a href="#" className="text-blue-500 hover:underline">View All Users</a></li>
            <li><a href="#" className="text-blue-500 hover:underline">Manage User Roles</a></li>
          </ul>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-3">Asset Management</h2>
          <ul className="text-gray-300">
            <li><a href="#" className="text-blue-500 hover:underline">Add New Player</a></li>
            <li><a href="#" className="text-blue-500 hover:underline">Manage Players</a></li>
            <li><a href="#" className="text-blue-500 hover:underline">Add New Team</a></li>
            <li><a href="#" className="text-blue-500 hover:underline">Manage Teams</a></li>
          </ul>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-3">Trading & Transactions</h2>
          <ul className="text-gray-300">
            <li><a href="#" className="text-blue-500 hover:underline">View All Orders</a></li>
            <li><a href="#" className="text-blue-500 hover:underline">View All Trades</a></li>
            <li><a href="#" className="text-blue-500 hover:underline">View All Transactions</a></li>
          </ul>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-3">Analytics & Logs</h2>
          <ul className="text-gray-300">
            <li><a href="#" className="text-blue-500 hover:underline">View Analytics</a></li>
            <li><a href="#" className="text-blue-500 hover:underline">View Audit Logs</a></li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AdminPage;

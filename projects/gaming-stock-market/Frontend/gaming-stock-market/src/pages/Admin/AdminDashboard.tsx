import React from 'react';
import { Link } from 'react-router-dom';

const AdminDashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-4xl font-bold mb-8 text-center text-indigo-400">Admin Dashboard</h1>
      <nav className="flex flex-col items-center space-y-4">
        <Link to="/admin/users" className="w-full max-w-xs p-4 bg-gray-800 hover:bg-gray-700 rounded-lg shadow-lg text-center text-xl font-semibold transition duration-300">
          User Management
        </Link>
        <Link to="/admin/players" className="w-full max-w-xs p-4 bg-gray-800 hover:bg-gray-700 rounded-lg shadow-lg text-center text-xl font-semibold transition duration-300">
          Player Management
        </Link>
        <Link to="/admin/teams" className="w-full max-w-xs p-4 bg-gray-800 hover:bg-gray-700 rounded-lg shadow-lg text-center text-xl font-semibold transition duration-300">
          Team Management
        </Link>
        <Link to="/admin/orders" className="w-full max-w-xs p-4 bg-gray-800 hover:bg-gray-700 rounded-lg shadow-lg text-center text-xl font-semibold transition duration-300">
          Order Management
        </Link>
        <Link to="/admin/transactions" className="w-full max-w-xs p-4 bg-gray-800 hover:bg-gray-700 rounded-lg shadow-lg text-center text-xl font-semibold transition duration-300">
          Transaction Management
        </Link>
        {/* Add more admin links as needed */}
      </nav>
    </div>
  );
};

export default AdminDashboard;

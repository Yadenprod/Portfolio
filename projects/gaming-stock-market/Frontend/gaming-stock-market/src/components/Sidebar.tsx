import React from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import type { RootState } from 'store'; // Updated path

const Sidebar: React.FC = () => {
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);

  if (!isAuthenticated) {
    return null; // Don't render sidebar if not authenticated
  }

  return (
    <aside className="w-64 bg-gray-900 text-gray-100 p-4 min-h-screen">
      <nav>
        <ul>
          <li className="mb-2">
            <Link to="/dashboard" className="block hover:bg-gray-700 p-2 rounded">Dashboard</Link>
          </li>
          <li className="mb-2">
            <Link to="/portfolio" className="block hover:bg-gray-700 p-2 rounded">Portfolio</Link>
          </li>
          <li className="mb-2">
            <Link to="/orders" className="block hover:bg-gray-700 p-2 rounded">My Orders</Link>
          </li>
          <li className="mb-2">
            <Link to="/trade-history" className="block hover:bg-gray-700 p-2 rounded">Trade History</Link>
          </li>
          <li className="mb-2">
            <Link to="/settings" className="block hover:bg-gray-700 p-2 rounded">Settings</Link>
          </li>
          <li className="mb-2">
            <Link to="/notifications" className="block hover:bg-gray-700 p-2 rounded">Notifications</Link>
          </li>
          <li className="mb-2">
            <Link to="/achievements" className="block hover:bg-gray-700 p-2 rounded">Achievements</Link>
          </li>
          {/* Admin link - would be conditionally rendered based on user role */}
          {/* Example: <li className="mb-2"><Link to="/admin" className="block hover:bg-gray-700 p-2 rounded">Admin Panel</Link></li> */}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;

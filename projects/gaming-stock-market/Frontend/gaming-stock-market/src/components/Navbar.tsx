import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import type { RootState } from 'store'; // Updated path
import { logout } from 'slices/authSlice'; // Updated path

const Navbar: React.FC = () => {
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  return (
    <nav className="bg-gray-800 p-4 text-white">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">Gaming Stock Market</Link>
        <div>
          <Link to="/players" className="mr-4 hover:text-gray-300">Players</Link>
          <Link to="/teams" className="mr-4 hover:text-gray-300">Teams</Link>
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="mr-4 hover:text-gray-300">Dashboard</Link>
              <Link to="/portfolio" className="mr-4 hover:text-gray-300">Portfolio</Link>
              <button onClick={handleLogout} className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="mr-4 hover:text-gray-300">Login</Link>
              <Link to="/register" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

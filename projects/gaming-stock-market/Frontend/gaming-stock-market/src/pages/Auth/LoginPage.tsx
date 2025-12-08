import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from 'store'; // Updated path
import { loginStart, loginSuccess, loginFailure } from 'slices/authSlice'; // Updated path
import { authApi } from 'api/authApi'; // Updated path
import Input from 'components/Input'; // Updated path
import Button from 'components/Button'; // Updated path

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const dispatch: AppDispatch = useDispatch();
  const { loading, error } = useSelector((state: RootState) => state.auth);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    dispatch(loginStart());
    try {
      const response = await authApi.login({ username, password });
      dispatch(loginSuccess(response.data));
      navigate('/dashboard');
    } catch (err: any) {
      dispatch(loginFailure(err.response?.data?.message || 'Login failed.'));
    }
  };

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-160px)]">
      <div className="bg-gray-800 p-8 rounded-lg shadow-xl w-full max-w-md">
        <h2 className="text-3xl font-bold text-white mb-6 text-center">Login</h2>
        <form onSubmit={handleSubmit}>
          <Input
            label="Username"
            id="username"
            type="text"
            value={username}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUsername(e.target.value)}
            required
            className="bg-gray-700 border-gray-600 text-white"
          />
          <Input
            label="Password"
            id="password"
            type="password"
            value={password}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
            required
            className="bg-gray-700 border-gray-600 text-white"
          />
          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
          <Button type="submit" loading={loading} className="w-full bg-blue-600 hover:bg-blue-700">
            Login
          </Button>
        </form>
        <p className="text-center text-gray-400 mt-4">
          Don't have an account? <Link to="/register" className="text-blue-500 hover:underline">Register here</Link>
        </p>
        <p className="text-center text-gray-400 mt-2">
          <Link to="/forgot-password" className="text-blue-500 hover:underline">Forgot Password?</Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;

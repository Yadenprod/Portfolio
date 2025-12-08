import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface AnalyticsResponse {
  totalUsers: number;
  activeUsers: number;
  totalTradingVolume: number;
  dailyTradingVolume: DailyMetric[];
  dailyNewUsers: DailyMetric[];
}

interface DailyMetric {
  date: string;
  value: number;
}

const AnalyticsDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [daysFilter, setDaysFilter] = useState<number>(7);

  useEffect(() => {
    fetchAnalytics();
  }, [daysFilter]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const [overallResponse, tradingVolumeResponse, newUsersResponse] = await Promise.all([
        axios.get<AnalyticsResponse>('http://localhost:5000/api/analytics/overall'),
        axios.get<DailyMetric[]>(`http://localhost:5000/api/analytics/daily-trading-volume?days=${daysFilter}`),
        axios.get<DailyMetric[]>(`http://localhost:5000/api/analytics/daily-new-users?days=${daysFilter}`)
      ]);

      setAnalytics({
        ...overallResponse.data,
        dailyTradingVolume: tradingVolumeResponse.data,
        dailyNewUsers: newUsersResponse.data,
      });
    } catch (err) {
      setError('Failed to fetch analytics data.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const tradingVolumeData = {
    labels: analytics?.dailyTradingVolume.map(d => new Date(d.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Daily Trading Volume',
        data: analytics?.dailyTradingVolume.map(d => d.value),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
    ],
  };

  const newUsersData = {
    labels: analytics?.dailyNewUsers.map(d => new Date(d.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Daily New Users',
        data: analytics?.dailyNewUsers.map(d => d.value),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  };

  if (loading) return <div className="text-center text-white">Loading analytics...</div>;
  if (error) return <div className="text-center text-red-500">Error: {error}</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-4xl font-bold mb-8 text-center text-indigo-400">Analytics Dashboard</h1>

      <div className="mb-6 text-center">
        <label htmlFor="daysFilter" className="mr-2 text-lg">Show data for last:</label>
        <select
          id="daysFilter"
          value={daysFilter}
          onChange={(e) => setDaysFilter(Number(e.target.value))}
          className="bg-gray-700 border border-gray-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option value={7}>7 Days</option>
          <option value={30}>30 Days</option>
          <option value={90}>90 Days</option>
        </select>
      </div>

      {analytics && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
            <h2 className="text-xl font-semibold text-indigo-300">Total Users</h2>
            <p className="text-3xl font-bold mt-2">{analytics.totalUsers}</p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
            <h2 className="text-xl font-semibold text-indigo-300">Active Users (30 Days)</h2>
            <p className="text-3xl font-bold mt-2">{analytics.activeUsers}</p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
            <h2 className="text-xl font-semibold text-indigo-300">Total Trading Volume</h2>
            <p className="text-3xl font-bold mt-2">${analytics.totalTradingVolume.toFixed(2)}</p>
          </div>
        </div>
      )}

      {analytics && (analytics.dailyTradingVolume.length > 0) && (
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg mb-8">
          <h2 className="text-2xl font-bold mb-4 text-indigo-300">Daily Trading Volume</h2>
          <Line data={tradingVolumeData} />
        </div>
      )}

      {analytics && (analytics.dailyNewUsers.length > 0) && (
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg mb-8">
          <h2 className="text-2xl font-bold mb-4 text-indigo-300">Daily New Users</h2>
          <Line data={newUsersData} />
        </div>
      )}
    </div>
  );
};

export default AnalyticsDashboard;

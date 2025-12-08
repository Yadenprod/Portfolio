import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useSelector } from 'react-redux';
import type { RootState } from 'store'; // Updated path

// Layout Components
import Navbar from 'components/Navbar'; // Updated path
import Footer from 'components/Footer'; // Updated path
import Sidebar from 'components/Sidebar'; // Updated path
import ErrorBoundary from 'components/ErrorBoundary'; // Updated path

// Public Pages
import HomePage from 'pages/HomePage'; // Updated path
import LoginPage from 'pages/Auth/LoginPage'; // Updated path
import RegisterPage from 'pages/Auth/RegisterPage'; // Updated path
import NotFoundPage from 'pages/NotFoundPage'; // Updated path

// Authenticated Pages
import DashboardPage from 'pages/DashboardPage'; // Updated path
import PlayersPage from 'pages/Players/PlayersPage'; // Updated path
import PlayerDetailsPage from 'pages/Players/PlayerDetailsPage'; // Updated path
import TeamsPage from 'pages/Teams/TeamsPage'; // Updated path
import TeamDetailsPage from 'pages/Teams/TeamDetailsPage'; // Updated path
import PortfolioPage from 'pages/PortfolioPage'; // Updated path
import OrderBookPage from 'pages/OrderBookPage'; // Updated path
import TradeHistoryPage from 'pages/TradeHistoryPage'; // Updated path
import SettingsPage from 'pages/SettingsPage'; // Updated path
import NotificationsPage from 'pages/NotificationsPage'; // Updated path
import AchievementsPage from 'pages/AchievementsPage'; // Updated path

// Admin Pages
import AdminDashboard from 'pages/Admin/AdminDashboard'; // Updated path
import UserManagement from 'pages/Admin/UserManagement'; // Updated path
import PlayerManagement from 'pages/Admin/PlayerManagement'; // Updated path
import TeamManagement from 'pages/Admin/TeamManagement'; // Updated path
import OrderManagement from 'pages/Admin/OrderManagement'; // Updated path
import TransactionManagement from 'pages/Admin/TransactionManagement'; // Updated path
import AnalyticsDashboard from 'pages/Admin/AnalyticsDashboard'; // Updated path
import AdminRoute from 'components/Admin/AdminRoute'; // Updated path

// Private Route Component
const PrivateRoute: React.FC<{ children: JSX.Element }> = ({ children }) => {
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);
  return isAuthenticated ? children : <LoginPage />;
};

const AppRouter: React.FC = () => {
  return (
    <Router>
      <ErrorBoundary>
        <div className="flex flex-col min-h-screen bg-gray-900 text-gray-100">
          <Navbar />
          <div className="flex flex-grow">
            <Sidebar />
            <main className="flex-grow p-4">
              <Routes>
                {/* Public Routes */}
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/players" element={<PlayersPage />} />
                <Route path="/players/:id" element={<PlayerDetailsPage />} />
                <Route path="/teams" element={<TeamsPage />} />
                <Route path="/teams/:id" element={<TeamDetailsPage />} />

                {/* Authenticated Routes */}
                <Route path="/dashboard" element={<PrivateRoute><DashboardPage /></PrivateRoute>} />
                <Route path="/portfolio" element={<PrivateRoute><PortfolioPage /></PrivateRoute>} />
                <Route path="/orders" element={<PrivateRoute><OrderBookPage /></PrivateRoute>} />
                <Route path="/trade-history" element={<PrivateRoute><TradeHistoryPage /></PrivateRoute>} />
                <Route path="/settings" element={<PrivateRoute><SettingsPage /></PrivateRoute>} />
                <Route path="/notifications" element={<PrivateRoute><NotificationsPage /></PrivateRoute>} />
                <Route path="/achievements" element={<PrivateRoute><AchievementsPage /></PrivateRoute>} />

                {/* Admin Routes */}
                <Route path="/admin" element={<AdminRoute />}>
                  <Route index element={<AdminDashboard />} />
                  <Route path="users" element={<UserManagement />} />
                  <Route path="players" element={<PlayerManagement />} />
                  <Route path="teams" element={<TeamManagement />} />
                  <Route path="orders" element={<OrderManagement />} />
                  <Route path="transactions" element={<TransactionManagement />} />
                  <Route path="analytics" element={<AnalyticsDashboard />} />
                </Route>

                {/* Catch-all for 404 */}
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </main>
          </div>
          <Footer />
        </div>
      </ErrorBoundary>
    </Router>
  );
};

export default AppRouter;

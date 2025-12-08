import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Shield, 
  BarChart3, 
  Camera, 
  Settings, 
  AlertTriangle,
  Home,
  Users,
  FileText
} from 'lucide-react';

// Компоненты
import Dashboard from './components/Dashboard';
import DetectionPanel from './components/DetectionPanel';
import Analytics from './components/Analytics';
import Alerts from './components/Alerts';
import SettingsPanel from './components/SettingsPanel';
import Sidebar from './components/Sidebar';
import Header from './components/Header';

// Стили
import './App.css';

interface SystemStatus {
  status: 'online' | 'offline' | 'maintenance';
  activeCameras: number;
  totalAlerts: number;
  preventionRate: number;
}

function App() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    status: 'online',
    activeCameras: 12,
    totalAlerts: 8,
    preventionRate: 87.5
  });

  const [activeAlerts, setActiveAlerts] = useState(0);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // Симуляция real-time обновлений
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveAlerts(prev => {
        const newValue = Math.max(0, prev + (Math.random() > 0.5 ? 1 : -1));
        return newValue;
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const menuItems = [
    {
      id: 'dashboard',
      title: 'Панель управления',
      icon: Home,
      path: '/',
      description: 'Общий обзор системы'
    },
    {
      id: 'detection',
      title: 'Детекция',
      icon: Camera,
      path: '/detection',
      description: 'Мониторинг в реальном времени'
    },
    {
      id: 'analytics',
      title: 'Аналитика',
      icon: BarChart3,
      path: '/analytics',
      description: 'Статистика и отчеты'
    },
    {
      id: 'alerts',
      title: 'Уведомления',
      icon: AlertTriangle,
      path: '/alerts',
      description: 'Активные уведомления',
      badge: activeAlerts
    },
    {
      id: 'reports',
      title: 'Отчеты',
      icon: FileText,
      path: '/reports',
      description: 'Генерация отчетов'
    },
    {
      id: 'users',
      title: 'Пользователи',
      icon: Users,
      path: '/users',
      description: 'Управление пользователями'
    },
    {
      id: 'settings',
      title: 'Настройки',
      icon: Settings,
      path: '/settings',
      description: 'Конфигурация системы'
    }
  ];

  return (
    <Router>
      <div className="app">
        <Sidebar 
          isOpen={isSidebarOpen} 
          onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
          menuItems={menuItems}
          systemStatus={systemStatus}
        />
        
        <div className={`main-content ${isSidebarOpen ? 'sidebar-open' : ''}`}>
          <Header 
            systemStatus={systemStatus}
            activeAlerts={activeAlerts}
            onSidebarToggle={() => setIsSidebarOpen(!isSidebarOpen)}
          />
          
          <main className="content">
            <AnimatePresence mode="wait">
              <Routes>
                <Route 
                  path="/" 
                  element={
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Dashboard systemStatus={systemStatus} />
                    </motion.div>
                  } 
                />
                <Route 
                  path="/detection" 
                  element={
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <DetectionPanel />
                    </motion.div>
                  } 
                />
                <Route 
                  path="/analytics" 
                  element={
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Analytics />
                    </motion.div>
                  } 
                />
                <Route 
                  path="/alerts" 
                  element={
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Alerts />
                    </motion.div>
                  } 
                />
                <Route 
                  path="/reports" 
                  element={
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <div className="reports-page">
                        <h1>Отчеты</h1>
                        <p>Страница отчетов в разработке...</p>
                      </div>
                    </motion.div>
                  } 
                />
                <Route 
                  path="/users" 
                  element={
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <div className="users-page">
                        <h1>Пользователи</h1>
                        <p>Страница пользователей в разработке...</p>
                      </div>
                    </motion.div>
                  } 
                />
                <Route 
                  path="/settings" 
                  element={
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <SettingsPanel />
                    </motion.div>
                  } 
                />
              </Routes>
            </AnimatePresence>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;

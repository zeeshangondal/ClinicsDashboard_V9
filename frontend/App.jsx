import { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import CallData from './components/CallData';
import WhatsAppLog from './components/WhatsAppLog';
import SMSInbox from './components/SMSInbox';
import Telegram from './components/Telegram';
import Appointments from './components/Appointments';

import WhatsAppConfig from './components/WhatsAppConfig';
import SuperAdmin from './components/SuperAdmin';
import Login from './components/Login';
import Header from './components/Header';
import authService from './lib/auth';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentPath, setCurrentPath] = useState('/dashboard');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [user, setUser] = useState(null);
  const [clinic, setClinic] = useState(null);

  useEffect(() => {
    // Check if user is already authenticated
    const checkAuth = async () => {
      try {
        const userData = authService.getCurrentUser();
        const clinicData = authService.getCurrentClinic();
        
        if (userData && clinicData) {
          setUser(userData);
          setClinic(clinicData);
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Authentication check failed:', error);
        setIsAuthenticated(false);
      }
    };
    
    checkAuth();
  }, []);

  const handleLogin = (data) => {
    setUser(data.user);
    setClinic(data.clinic);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUser(null);
    setClinic(null);
    setCurrentPath('/dashboard');
  };

  const handleNavigate = (path) => {
    setCurrentPath(path);
  };

  const handleSidebarToggle = (collapsed) => {
    setIsSidebarCollapsed(collapsed);
  };

  const getPageTitle = (path) => {
    const titles = {
      '/dashboard': 'Dashboard',
      '/calls': 'Call Data',
      '/whatsapp': 'WhatsApp',
      '/inbox': 'SMS Inbox',
      '/telegram': 'Telegram',
      '/appointments': 'Appointments',
      '/whatsapp-config': 'WhatsApp Config',
      '/admin/clinics': 'Admin - Clinics',
      '/admin/logs': 'Admin - Logs',
      '/admin/metrics': 'Admin - Metrics'
    };
    return titles[path] || 'Dashboard';
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  const renderContent = () => {
    switch (currentPath) {
      case '/dashboard':
        return <Dashboard />;
      case '/calls':
        return <CallData />;
      case '/whatsapp':
        return <WhatsAppLog />;
      case '/inbox':
        return <SMSInbox />;
      case '/telegram':
        return <Telegram />;
      case '/appointments':
        return <Appointments />;
     case '/whatsapp-config':
        return <WhatsAppConfig />;
      case '/admin/clinics':
      case '/admin/logs':
      case '/admin/metrics':
        return <SuperAdmin section={currentPath.split('/').pop()} />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="app-container">
      <div className="sidebar-container">
        <Sidebar 
          currentPath={currentPath} 
          onNavigate={handleNavigate} 
          onLogout={handleLogout}
          onToggle={handleSidebarToggle}
        />
      </div>
      <div className={`content-container ${isSidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
        <Header title={getPageTitle(currentPath)} />
        {renderContent()}
      </div>
    </div>
  );
}

export default App;


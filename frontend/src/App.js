import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import VideoUpload from './pages/VideoUpload';
import DetectionResults from './pages/DetectionResults';
import UserManagement from './pages/UserManagement';
import LogManagement from './pages/LogManagement';
import SideNav from './layouts/SideNav';
import MainLayout from './layouts/MainLayout';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('user_id'));

  useEffect(() => {
    const handleStorage = () => setIsLoggedIn(!!localStorage.getItem('user_id'));
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={
            isLoggedIn ? <Navigate to="/upload" /> : <Login onLogin={() => setIsLoggedIn(true)} />
          }
        />
        <Route
          path="/*"
          element={
            isLoggedIn ? <MainLayout /> : <Navigate to="/login" />
          }
        />
      </Routes>
    </Router>
  );
};

export default App; 
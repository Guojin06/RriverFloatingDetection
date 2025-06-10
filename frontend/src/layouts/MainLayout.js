import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import SideNav from './SideNav';
import DetectionResults from '../pages/DetectionResults';
import UserManagement from '../pages/UserManagement';
import LogManagement from '../pages/LogManagement';
import ImageDetect from '../pages/ImageDetect';

const MainLayout = () => {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'transparent' }}>
      <SideNav />
      <div style={{
        flex: 1,
        marginLeft: 280,
        padding: '48px 32px 0 32px',
        maxWidth: 1200,
        marginRight: 'auto',
        marginLeft: 320,
        background: 'rgba(34,40,49,0.82)',
        borderRadius: 28,
        minHeight: '92vh',
        boxShadow: '0 8px 32px 0 rgba(54,209,196,0.10)',
        marginTop: 32
      }}>
        <Routes>
          <Route path="/image-detect" element={<ImageDetect />} />
          <Route path="/results" element={<DetectionResults />} />
          <Route path="/users" element={<UserManagement />} />
          <Route path="/logs" element={<LogManagement />} />
          <Route path="*" element={<Navigate to="/image-detect" />} />
        </Routes>
      </div>
    </div>
  );
};

export default MainLayout; 
import React from 'react';
import { Card } from 'antd';

const CenterCardLayout = ({ children, width = 400 }) => (
  <div style={{
    minHeight: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
  }}>
    <Card
      style={{
        width,
        background: 'rgba(255,255,255,0.25)',
        borderRadius: 24,
        boxShadow: '0 8px 32px rgba(0,0,0,0.25)',
        padding: 32,
        backdropFilter: 'blur(12px)',
        border: '1px solid rgba(255,255,255,0.18)'
      }}
      bodyStyle={{ padding: 32 }}
    >
      {children}
    </Card>
  </div>
);

export default CenterCardLayout;

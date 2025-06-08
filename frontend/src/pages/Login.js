import React, { useState } from 'react';
import { Form, Input, Button, Typography, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';

const { Title } = Typography;
const API_BASE = process.env.REACT_APP_API_BASE;

const inputStyle = {
  borderRadius: 18,
  background: 'rgba(34,40,49,0.28)',
  color: '#fff',
  border: 'none',
  boxShadow: '0 2px 8px rgba(54,209,196,0.10)',
  textAlign: 'center',
  fontSize: 18,
  fontWeight: 500,
  width: '80%',
  margin: '0 auto',
  display: 'block',
  paddingLeft: 40,
  paddingRight: 16,
};

const Login = ({ onLogin }) => {
  const [loading, setLoading] = useState(false);

  const handleFinish = async (values) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', values.username);
      formData.append('password', values.password);
      const response = await fetch(`${API_BASE}/api/login`, {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('登录失败');
      const data = await response.json();
      localStorage.setItem('user_id', data.user_id);
      message.success('登录成功！');
      onLogin && onLogin();
    } catch (e) {
      message.error('登录失败，请检查用户名和密码！');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      width: '100vw',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: `linear-gradient(135deg, #232526 0%, #414345 100%), url('https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1500&q=80') center/cover no-repeat`,
      backgroundBlendMode: 'overlay',
    }}>
      <div style={{
        width: 420,
        padding: '48px 40px 40px 40px',
        borderRadius: 28,
        background: 'rgba(34, 40, 49, 0.82)',
        boxShadow: '0 8px 32px 0 rgba(54,209,196,0.18)',
        backdropFilter: 'blur(8px)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 36, color: '#36d1c4', fontWeight: 700, letterSpacing: 2, fontFamily: 'Roboto, sans-serif', textShadow: '0 2px 8px #0004' }}>河流漂浮物检测系统</Title>
        <Form onFinish={handleFinish} style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }} layout="vertical">
          <Form.Item name="username" rules={[{ required: true, message: '请输入用户名！' }]} style={{ marginBottom: 28, width: '100%' }}>
            <Input prefix={<UserOutlined style={{ marginRight: 8, color: '#36d1c4' }} />} placeholder="用户名" size="large" style={inputStyle}
              autoComplete="username"
              allowClear={false}
              bordered={false}
            />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true, message: '请输入密码！' }]} style={{ marginBottom: 32, width: '100%' }}>
            <Input.Password prefix={<LockOutlined style={{ marginRight: 8, color: '#36d1c4' }} />} placeholder="密码" size="large" style={inputStyle}
              autoComplete="current-password"
              allowClear={false}
              bordered={false}
            />
          </Form.Item>
          <Form.Item style={{ marginBottom: 0, width: '100%', display: 'flex', justifyContent: 'center' }}>
            <Button type="primary" htmlType="submit" size="large" loading={loading}
              style={{
                borderRadius: 24,
                background: 'linear-gradient(90deg, #36d1c4 0%, #5b86e5 100%)',
                border: 'none',
                fontWeight: 'bold',
                fontSize: 22,
                letterSpacing: 2,
                boxShadow: '0 4px 24px 0 #36d1c4cc, 0 0 16px 2px #5b86e5cc',
                width: 180,
                transition: 'box-shadow 0.2s',
                textAlign: 'center',
                display: 'block',
                margin: '0 auto',
                filter: loading ? 'brightness(0.8)' : 'none',
              }}
              onMouseOver={e => e.currentTarget.style.boxShadow = '0 0 32px 4px #36d1c4cc, 0 0 32px 8px #5b86e5cc'}
              onMouseOut={e => e.currentTarget.style.boxShadow = '0 4px 24px 0 #36d1c4cc, 0 0 16px 2px #5b86e5cc'}
            >
              登 录
            </Button>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};

export default Login; 
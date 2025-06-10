import React, { useState } from 'react';
import { Form, Input, Button, Typography, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import './Login.css';

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
        width: 340,
        padding: '32px 28px 28px 28px',
        borderRadius: 18,
        background: 'rgba(34, 40, 49, 0.82)',
        boxShadow: '0 8px 32px 0 rgba(54,209,196,0.18)',
        backdropFilter: 'blur(8px)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 24, color: '#36d1c4', fontWeight: 700, letterSpacing: 2, fontFamily: 'Roboto, sans-serif', textShadow: '0 2px 8px #0004', fontSize: 22 }}>河流漂浮物检测系统</Title>
        <Form
          onFinish={handleFinish}
          className="login-form-center"
          style={{ width: '100%', maxWidth: 280, margin: '0 auto' }}
          layout="vertical"
        >
          <Form.Item name="username" rules={[{ required: true, message: '请输入用户名！' }]} style={{ width: '100%', marginBottom: 20 }}>
            <Input
              prefix={<UserOutlined style={{ color: '#36d1c4', fontSize: 20 }} />}
              placeholder="用户名"
              size="large"
              style={{
                background: 'rgba(255,255,255,0.85)',
                borderRadius: 12,
                border: 'none',
                color: '#232526',
                fontSize: 16,
                boxShadow: 'none',
                height: 40,
                width: '100%',
                paddingLeft: 36,
                paddingRight: 12,
                marginBottom: 0
              }}
              autoComplete="username"
              allowClear={false}
              bordered={false}
            />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true, message: '请输入密码！' }]} style={{ width: '100%', marginBottom: 22 }}>
            <Input.Password
              prefix={<LockOutlined style={{ color: '#36d1c4', fontSize: 20 }} />}
              placeholder="密码"
              size="large"
              style={{
                background: 'rgba(255,255,255,0.85)',
                borderRadius: 12,
                border: 'none',
                color: '#232526',
                fontSize: 16,
                boxShadow: 'none',
                height: 40,
                width: '100%',
                paddingLeft: 36,
                paddingRight: 12,
                marginBottom: 0
              }}
              autoComplete="current-password"
              allowClear={false}
              bordered={false}
            />
          </Form.Item>
          <Form.Item style={{ width: '100%', marginBottom: 0 }}>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              className="login-btn"
              style={{
                width: '100%',
                borderRadius: 12,
                background: 'linear-gradient(90deg, #36d1c4 0%, #5b86e5 100%)',
                border: 'none',
                fontWeight: 700,
                fontSize: 16,
                height: 40,
                boxShadow: '0 2px 8px rgba(54,209,196,0.12)',
                marginTop: 8
              }}
            >登 录</Button>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};

export default Login; 
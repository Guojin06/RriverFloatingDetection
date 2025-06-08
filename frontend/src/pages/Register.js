import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE;

const Register = () => {
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      // 使用 FormData 以表单格式提交，兼容 FastAPI Form 参数
      const formData = new FormData();
      formData.append('username', values.username);
      formData.append('password', values.password);
      const response = await axios.post(`${API_BASE}/api/register`, formData);
      message.success('注册成功！');
      // 跳转到登录页面
    } catch (error) {
      message.error('注册失败，请检查输入信息！');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 300, margin: '0 auto', padding: '50px 0' }}>
      <h2>注册</h2>
      <Form onFinish={onFinish}>
        <Form.Item name="username" rules={[{ required: true, message: '请输入用户名！' }]}>
          <Input placeholder="用户名" />
        </Form.Item>
        <Form.Item name="password" rules={[{ required: true, message: '请输入密码！' }]}>
          <Input.Password placeholder="密码" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} block>
            注册
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default Register; 
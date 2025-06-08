import React, { useState, useEffect } from 'react';
import { Table, message, Typography, Card } from 'antd';
import axios from 'axios';

const { Title } = Typography;
const API_BASE = process.env.REACT_APP_API_BASE;

const LogManagement = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const userId = localStorage.getItem('user_id');
      const response = await axios.get(`${API_BASE}/api/logs/user/${userId}`);
      setLogs(response.data);
    } catch (error) {
      message.error('获取日志信息失败！');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { title: '日志ID', dataIndex: 'id', key: 'id', align: 'center' },
    { title: '用户ID', dataIndex: 'user_id', key: 'user_id', align: 'center', render: v => v ?? '-' },
    { title: '操作', dataIndex: 'action', key: 'action', align: 'center' },
    { title: '操作时间', dataIndex: 'action_time', key: 'action_time', align: 'center' }
  ];

  // 横向分页符号
  const itemRender = (current, type, originalElement) => {
    if (type === 'prev') {
      return <a style={{ fontSize: 22, color: '#36d1c4' }}>‹</a>;
    }
    if (type === 'next') {
      return <a style={{ fontSize: 22, color: '#36d1c4' }}>›</a>;
    }
    return originalElement;
  };

  return (
    <Card style={{ borderRadius: 22, boxShadow: '0 4px 32px rgba(54,209,196,0.10)', background: 'rgba(30,34,54,0.92)', margin: '32px auto', maxWidth: 900 }}>
      <Title level={2} style={{ textAlign: 'center', color: '#36d1c4', fontWeight: 700, marginBottom: 32 }}>日志管理</Title>
      <Table columns={columns} dataSource={logs} loading={loading} rowKey="id" pagination={{ pageSize: 8, itemRender }} bordered />
    </Card>
  );
};

export default LogManagement; 
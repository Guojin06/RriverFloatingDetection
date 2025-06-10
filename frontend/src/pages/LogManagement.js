import React, { useState, useEffect } from 'react';
import { Table, message, Typography, Card } from 'antd';
import axios from 'axios';
import './LogManagement.css';

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
    { title: '日志ID', dataIndex: 'id', key: 'id', align: 'center', width: 80 },
    { title: '用户ID', dataIndex: 'user_id', key: 'user_id', align: 'center', width: 100 },
    { title: '操作', dataIndex: 'action', key: 'action', align: 'center', width: 180 },
    { title: '操作时间', dataIndex: 'action_time', key: 'action_time', align: 'center', width: 180 }
  ];

  return (
    <Card style={{ borderRadius: 22, boxShadow: '0 4px 32px rgba(54,209,196,0.10)', background: 'rgba(30,34,54,0.92)', margin: '32px auto', maxWidth: 900 }}>
      <Title level={2} style={{ textAlign: 'center', color: '#36d1c4', fontWeight: 700, marginBottom: 32 }}>日志管理</Title>
      <div className="custom-pagination-wrapper">
        <Table
          columns={columns}
          dataSource={logs}
          loading={loading}
          rowKey="id"
          bordered
          scroll={{ x: 600 }}
          pagination={{
            pageSize: 8,
            showSizeChanger: false,
            showQuickJumper: false,
            showLessItems: false,
            simple: true,
            style: { display: 'flex', justifyContent: 'center', marginTop: 24 },
          }}
          style={{ background: 'rgba(30,34,54,0.92)' }}
        />
      </div>
    </Card>
  );
};

export default LogManagement; 
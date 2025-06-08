import React, { useState, useEffect } from 'react';
import { Table, Button, message, Typography, Card } from 'antd';
import axios from 'axios';

const { Title } = Typography;
const API_BASE = process.env.REACT_APP_API_BASE;

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const userId = localStorage.getItem('user_id');
      const response = await axios.get(`${API_BASE}/api/users/${userId}`);
      setUsers([response.data]);
    } catch (error) {
      message.error('获取用户信息失败！');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (userId) => {
    try {
      await axios.delete(`${API_BASE}/api/users/${userId}`);
      message.success('用户删除成功！');
      fetchUsers();
    } catch (error) {
      message.error('用户删除失败！');
    }
  };

  const columns = [
    { title: '用户ID', dataIndex: 'user_id', key: 'user_id', align: 'center' },
    { title: '用户名', dataIndex: 'username', key: 'username', align: 'center' },
    { title: '角色', dataIndex: 'role', key: 'role', align: 'center' },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at', align: 'center' },
    {
      title: '操作',
      key: 'action',
      align: 'center',
      render: (_, record) => (
        <Button type="primary" danger onClick={() => handleDelete(record.user_id)}>
          删除
        </Button>
      )
    }
  ];

  return (
    <Card style={{ borderRadius: 22, boxShadow: '0 4px 32px rgba(54,209,196,0.10)', background: 'rgba(30,34,54,0.92)', margin: '32px auto', maxWidth: 900, minWidth: 700 }}>
      <Title level={2} style={{ textAlign: 'center', color: '#36d1c4', fontWeight: 700, marginBottom: 32 }}>用户管理</Title>
      <Table columns={columns} dataSource={users} loading={loading} rowKey="user_id" pagination={false} bordered scroll={{ x: 900 }} />
    </Card>
  );
};

export default UserManagement; 
import React, { useState, useEffect } from 'react';
import { Table, message, Typography, Card } from 'antd';
import axios from 'axios';

const { Title } = Typography;
const API_BASE = process.env.REACT_APP_API_BASE;

const DetectionResults = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    setLoading(true);
    try {
      const userId = localStorage.getItem('user_id');
      const response = await axios.get(`${API_BASE}/api/detection_results/video/${userId}`);
      setResults(response.data);
    } catch (error) {
      message.error('获取检测结果失败！');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { title: '结果ID', dataIndex: 'result_id', key: 'result_id', align: 'center' },
    { title: '视频ID', dataIndex: 'video_id', key: 'video_id', align: 'center', render: v => v ?? '-' },
    { title: '检测时间', dataIndex: 'detected_at', key: 'detected_at', align: 'center' },
    { title: '结果JSON', dataIndex: 'result_json', key: 'result_json', align: 'center' }
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
      <Title level={2} style={{ textAlign: 'center', color: '#36d1c4', fontWeight: 700, marginBottom: 32 }}>检测结果</Title>
      <Table columns={columns} dataSource={results} loading={loading} rowKey="result_id" pagination={{ pageSize: 8, itemRender }} bordered />
    </Card>
  );
};

export default DetectionResults; 
import React, { useState, useEffect } from 'react';
import { Table, message, Typography, Card } from 'antd';
import axios from 'axios';
import './DetectionResults.css';

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
      // 获取该用户所有图片
      const imagesRes = await axios.get(`${API_BASE}/api/images/user/${userId}`);
      const images = imagesRes.data;
      let allResults = [];
      for (const img of images) {
        const res = await axios.get(`${API_BASE}/api/detection_results/image/${img.image_id}`);
        if (Array.isArray(res.data)) {
          allResults = allResults.concat(res.data.map(r => ({...r, image_path: img.image_path})));
        } else if (res.data) {
          allResults.push({...res.data, image_path: img.image_path});
        }
      }
      setResults(allResults);
    } catch (error) {
      message.error('获取检测结果失败！');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { title: '结果ID', dataIndex: 'result_id', key: 'result_id', align: 'center', width: 80 },
    { title: '图片ID', dataIndex: 'image_id', key: 'image_id', align: 'center', width: 100 },
    {
      title: '图片文件',
      dataIndex: 'image_path',
      key: 'image_path',
      align: 'center',
      width: 180,
      render: (text) => (
        <a
          href={`http://localhost:9000/images/${text}`}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            color: '#36d1c4',
            textDecoration: 'underline',
            cursor: 'pointer',
            fontSize: 16,
            padding: 0,
            margin: 0
          }}
        >
          {text}
        </a>
      )
    },
    { title: '检测时间', dataIndex: 'detected_at', key: 'detected_at', align: 'center', width: 180 },
    {
      title: '检测详情',
      dataIndex: 'result_json',
      key: 'result_json',
      align: 'center',
      width: 400,
      render: (text) => {
        let arr = [];
        try {
          arr = typeof text === 'string' ? JSON.parse(text.replace(/'/g, '"')) : text;
        } catch {
          return <span style={{ color: '#888' }}>无</span>;
        }
        if (!Array.isArray(arr) || arr.length === 0) return <span style={{ color: '#888' }}>无</span>;
        return (
          <table style={{ width: '100%', fontSize: 14, background: 'none', color: '#fff', borderCollapse: 'collapse', border: '1px solid #36d1c4', tableLayout: 'fixed' }}>
            <thead>
              <tr style={{ background: 'rgba(54,209,196,0.10)' }}>
                <th style={{ padding: '6px 0', border: '1px solid #36d1c4', width: '33%', textAlign: 'center' }}>类别</th>
                <th style={{ padding: '6px 0', border: '1px solid #36d1c4', width: '33%', textAlign: 'center' }}>置信度</th>
                <th style={{ padding: '6px 0', border: '1px solid #36d1c4', width: '33%', textAlign: 'center' }}>坐标</th>
              </tr>
            </thead>
            <tbody>
              {arr.map((det, idx) => (
                <tr key={idx}>
                  <td style={{ padding: '6px 0', border: '1px solid #36d1c4', width: '33%', textAlign: 'center' }}>{det.class_name}</td>
                  <td style={{ padding: '6px 0', border: '1px solid #36d1c4', width: '33%', textAlign: 'center' }}>{(det.confidence * 100).toFixed(1)}%</td>
                  <td style={{ padding: '6px 0', border: '1px solid #36d1c4', width: '33%', textAlign: 'center' }}>{det.box.join(', ')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        );
      }
    }
  ];

  return (
    <Card style={{ borderRadius: 22, boxShadow: '0 4px 32px rgba(54,209,196,0.10)', background: 'rgba(30,34,54,0.92)', margin: '32px auto', maxWidth: 1200 }}>
      <Title level={2} style={{ textAlign: 'center', color: '#36d1c4', fontWeight: 700, marginBottom: 32 }}>图片检测结果</Title>
      <div className="custom-pagination-wrapper">
        <Table
          columns={columns}
          dataSource={results}
          loading={loading}
          rowKey="result_id"
          bordered
          scroll={{ x: 1200 }}
          pagination={{
            pageSize: 8,
            showSizeChanger: false,
            showQuickJumper: false,
            showLessItems: false,
            simple: true,
            style: { display: 'flex', justifyContent: 'center', marginTop: 24, color: '#36d1c4', fontSize: 18, fontFamily: 'Roboto, Arial, sans-serif' },
          }}
          style={{ background: 'rgba(30,34,54,0.92)' }}
        />
      </div>
    </Card>
  );
};

export default DetectionResults; 
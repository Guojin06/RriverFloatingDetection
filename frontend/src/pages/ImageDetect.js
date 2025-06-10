import React, { useState } from 'react';
import { Upload, Button, Card, Typography, message, Spin, Result } from 'antd';
import { UploadOutlined, CheckCircleTwoTone } from '@ant-design/icons';
import axios from 'axios';

const { Title, Paragraph } = Typography;
const API_BASE = process.env.REACT_APP_API_BASE;

const ImageDetect = () => {
  const [loading, setLoading] = useState(false);
  const [detectResult, setDetectResult] = useState(null);

  // 先上传图片，拿到image_id后再检测
  const handleUpload = async (file) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    const userId = localStorage.getItem('user_id');
    formData.append('user_id', userId);
    try {
      // 1. 上传图片，获取image_id
      const uploadRes = await axios.post(`${API_BASE}/api/images/upload`, formData);
      const imageId = uploadRes.data.image_id;
      if (!imageId) throw new Error('图片上传失败');
      // 2. 检测图片，传image_id和file
      const detectForm = new FormData();
      detectForm.append('file', file);
      detectForm.append('image_id', imageId);
      detectForm.append('user_id', userId);
      const res = await axios.post(`${API_BASE}/api/detect/image`, detectForm);
      setDetectResult(res.data);
      message.success('检测完成！');
    } catch (e) {
      message.error('图片上传或检测失败！');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '80vh', display: 'flex', justifyContent: 'center', alignItems: 'center', background: 'transparent' }}>
      <Card style={{ width: 540, boxShadow: '0 8px 32px 0 rgba(54,209,196,0.18)', borderRadius: 24, background: 'rgba(34,40,49,0.92)', padding: '40px 32px' }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 32, color: '#36d1c4', fontWeight: 700, letterSpacing: 2 }}>图片检测</Title>
        <Paragraph style={{ textAlign: 'center', color: '#b2f7ef', marginBottom: 32, fontSize: 16 }}>
          上传图片，系统将自动检测并返回检测结果。
        </Paragraph>
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 32 }}>
          <Upload beforeUpload={handleUpload} showUploadList={false} accept="image/*">
            <Button icon={<UploadOutlined />} loading={loading} size="large" type="primary" style={{ borderRadius: 12, width: 200, fontWeight: 600, fontSize: 18 }}>
              {loading ? '处理中...' : '选择图片'}
            </Button>
          </Upload>
        </div>
        {loading && (
          <div style={{ textAlign: 'center', marginBottom: 24 }}>
            <Spin size="large" tip="正在检测..." />
          </div>
        )}
        {detectResult && (
          <div style={{ marginTop: 32 }}>
            <Result
              icon={<CheckCircleTwoTone twoToneColor="#36d1c4" style={{ fontSize: 48 }} />}
              title={<span style={{ color: '#36d1c4' }}>检测完成！</span>}
              subTitle={<span style={{ color: '#36d1c4' }}>{`检测时间：${detectResult.detected_at || ''}`}</span>}
            />
            <Card
              type="inner"
              title={<span style={{ color: '#36d1c4' }}>检测结果详情</span>}
              style={{ marginTop: 16, background: 'rgba(255,255,255,0.96)', borderColor: '#36d1c4', color: '#222' }}
            >
              {Array.isArray(detectResult.detections) && detectResult.detections.length > 0 ? (
                <table style={{ width: '100%', color: '#222', background: 'none', fontSize: 16, borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ background: 'rgba(54,209,196,0.10)' }}>
                      <th style={{ padding: '8px 12px' }}>类别</th>
                      <th style={{ padding: '8px 12px' }}>置信度</th>
                      <th style={{ padding: '8px 12px' }}>坐标 [x1, y1, x2, y2]</th>
                    </tr>
                  </thead>
                  <tbody>
                    {detectResult.detections.map((det, idx) => (
                      <tr key={idx}>
                        <td style={{ padding: '8px 12px' }}>{det.class_name}</td>
                        <td style={{ padding: '8px 12px' }}>{(det.confidence * 100).toFixed(1)}%</td>
                        <td style={{ padding: '8px 12px' }}>{det.box.join(', ')}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <div style={{ color: '#888', fontSize: 16 }}>未检测到目标</div>
              )}
            </Card>
          </div>
        )}
      </Card>
    </div>
  );
};

export default ImageDetect; 
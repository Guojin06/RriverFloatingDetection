import React, { useState } from 'react';
import { Upload, Button, message, Card, Typography, Result, Spin } from 'antd';
import { UploadOutlined, CheckCircleTwoTone } from '@ant-design/icons';
import axios from 'axios';

const { Title, Paragraph } = Typography;
const API_BASE = process.env.REACT_APP_API_BASE;

const VideoUpload = () => {
  const [loading, setLoading] = useState(false);
  const [detectResult, setDetectResult] = useState(null);

  const handleUpload = async (file) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    const userId = localStorage.getItem('user_id');
    formData.append('user_id', userId);

    try {
      // 1. 上传视频
      const uploadRes = await axios.post(`${API_BASE}/api/videos/upload`, formData);
      message.success('视频上传成功，开始检测...');
      const videoId = uploadRes.data.video_id;

      // 2. 调用检测接口
      const detectRes = await axios.post(`${API_BASE}/api/detect/video`, null, {
        params: { video_id: videoId }
      });
      message.success('检测完成！');

      // 3. 拉取检测结果详情
      const resultId = detectRes.data.result_id;
      const resultRes = await axios.get(`${API_BASE}/api/detection_results/${resultId}`);
      setDetectResult(resultRes.data);
    } catch (error) {
      message.error('视频上传或检测失败，请重试！');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '80vh', display: 'flex', justifyContent: 'center', alignItems: 'center', background: 'transparent' }}>
      <Card style={{ width: 540, boxShadow: '0 8px 32px 0 rgba(54,209,196,0.18)', borderRadius: 24, background: 'rgba(34,40,49,0.92)', padding: '40px 32px' }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 32, color: '#36d1c4', fontWeight: 700, letterSpacing: 2 }}>河流漂浮物视频检测</Title>
        <Paragraph style={{ textAlign: 'center', color: '#b2f7ef', marginBottom: 32, fontSize: 16 }}>
          上传河流监控视频，系统将自动检测并返回检测结果。
        </Paragraph>
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 32 }}>
          <Upload beforeUpload={handleUpload} showUploadList={false} accept="video/*">
            <Button icon={<UploadOutlined />} loading={loading} size="large" type="primary" style={{ borderRadius: 12, width: 200, fontWeight: 600, fontSize: 18 }}>
              {loading ? '处理中...' : '选择视频'}
            </Button>
          </Upload>
        </div>
        {loading && (
          <div style={{ textAlign: 'center', marginBottom: 24 }}>
            <Spin size="large" tip="正在上传和检测，请稍候..." />
          </div>
        )}
        {detectResult && (
          <Result
            icon={<CheckCircleTwoTone twoToneColor="#36d1c4" style={{ fontSize: 48 }} />}
            title={<span style={{ color: '#36d1c4' }}>检测完成！</span>}
            subTitle={<span style={{ color: '#fff' }}>{`检测时间：${detectResult.detected_at}`}</span>}
            extra={
              <Card type="inner" title={<span style={{ color: '#36d1c4' }}>检测结果详情</span>} style={{ marginTop: 16, background: 'rgba(54,209,196,0.08)', borderColor: '#36d1c4', color: '#fff' }}>
                <pre style={{ background: 'none', color: '#333', fontSize: 15, margin: 0, padding: 0, border: 'none' }}>
                  {JSON.stringify(detectResult.result_json, null, 2)}
                </pre>
              </Card>
            }
          />
        )}
      </Card>
    </div>
  );
};

export default VideoUpload; 
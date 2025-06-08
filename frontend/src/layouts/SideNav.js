import React from 'react';
import { Menu } from 'antd';
import { UserOutlined, VideoCameraOutlined, FileTextOutlined, LogoutOutlined, BarsOutlined } from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import './SideNav.css';

const menuItems = [
  { key: '/upload', icon: <VideoCameraOutlined />, label: '视频上传' },
  { key: '/results', icon: <FileTextOutlined />, label: '检测结果' },
  { key: '/users', icon: <UserOutlined />, label: '用户管理' },
  { key: '/logs', icon: <BarsOutlined />, label: '日志管理' },
  { key: 'logout', icon: <LogoutOutlined />, label: '退出登录' },
];

const SideNav = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleClick = (e) => {
    if (e.key === 'logout') {
      localStorage.removeItem('user_id');
      window.location.href = '/login';
    } else {
      navigate(e.key);
    }
  };

  return (
    <div className="side-nav-tech">
      <div className="logo-tech">河流漂浮物检测</div>
      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={[location.pathname]}
        onClick={handleClick}
        items={menuItems}
        style={{
          background: 'transparent',
          border: 'none',
          fontSize: 18,
          fontWeight: 500,
          color: '#fff',
          marginTop: 24
        }}
      />
    </div>
  );
};

export default SideNav;

import React from 'react';
import { Menu } from 'antd';
import { UserOutlined, FileTextOutlined, LogoutOutlined, BarsOutlined, UploadOutlined } from '@ant-design/icons';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import './SideNav.css';

const menuItems = [
  { key: '/image-detect', icon: <UploadOutlined />, label: <Link to="/image-detect">图片检测</Link> },
  { key: '/results', icon: <FileTextOutlined />, label: <Link to="/results">检测结果</Link> },
  { key: '/users', icon: <UserOutlined />, label: <Link to="/users">用户管理</Link> },
  { key: '/logs', icon: <BarsOutlined />, label: <Link to="/logs">日志管理</Link> },
];

const SideNav = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const selectedKey = menuItems.find(item => location.pathname.startsWith(item.key))?.key || '/image-detect';

  return (
    <div className="side-nav-tech">
      <div className="logo-tech">河流检测</div>
      <Menu
        mode="inline"
        theme="dark"
        selectedKeys={[selectedKey]}
        style={{ width: '100%', background: 'transparent', border: 'none', flex: 1 }}
        items={menuItems}
        onClick={({ key }) => navigate(key)}
      />
      <Menu
        mode="inline"
        theme="dark"
        style={{ width: '100%', background: 'transparent', border: 'none', marginTop: 'auto' }}
        items={[
          { key: 'logout', icon: <LogoutOutlined />, label: '退出登录' }
        ]}
        onClick={({ key }) => {
          if (key === 'logout') {
            localStorage.removeItem('user_id');
            window.location.reload();
          }
        }}
      />
    </div>
  );
};

export default SideNav;

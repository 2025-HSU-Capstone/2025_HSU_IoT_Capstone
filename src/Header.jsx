// src/Header.jsx
import React from 'react';

const Header = () => {
  const scrollToSection = (id) => {
    const section = document.getElementById(id);
    section?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <header style={{
      position: 'sticky', top: 0, background: '#fff', zIndex: 100,
      padding: '16px 24px', borderBottom: '1px solid #ddd'
    }}>
      <nav style={{ display: 'flex', gap: '24px', justifyContent: 'center' }}>
        <button onClick={() => scrollToSection('auto-diary')}>📘 자동일기</button>
        <button onClick={() => scrollToSection('growth-chart')}>🌿 키 변화</button>
        <button onClick={() => scrollToSection('timelapse')}>📸 타임랩스</button>
      </nav>
    </header>
  );
};

export default Header;

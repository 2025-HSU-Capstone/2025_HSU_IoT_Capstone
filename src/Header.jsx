// src/Header.jsx
// Header.jsx
import React from 'react';
import { LeafHeaderWrapper, LeafTab } from './styles/styledComponents';

const Header = () => {
  const scrollToSection = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <LeafHeaderWrapper>
      <LeafTab onClick={() => scrollToSection('auto-diary')}>📘 자동일기</LeafTab>
      <LeafTab onClick={() => scrollToSection('growth-chart')}>🌿 키 변화</LeafTab>
      <LeafTab onClick={() => scrollToSection('timelapse')}>📸 타임랩스</LeafTab>
    </LeafHeaderWrapper>
  );
};

export default Header;

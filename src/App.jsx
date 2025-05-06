import React from 'react';
import { Container, HeaderText, ContentWrapper, LayoutWrapper } from './styles/styledComponents';
import Header from './Header';
import AutoDiarySection from './AutoDiary';
import GrowthChart from './GrowthChart';
import TimelapseViewer from './TimelapseViewer';

function App() {
  return (
    <LayoutWrapper>
      {/* 📌 상단 탭 */}
      <Header />

      {/* 📌 프로젝트 제목 */}
      <Container>
        <HeaderText>야 너도 키울 수 있어</HeaderText>
      </Container>

      {/* 📘 자동 식물 일기 */}
      <ContentWrapper>
        <section id="auto-diary" className="mb-12">
          <AutoDiarySection />
        </section>
      </ContentWrapper>

      {/* 📈 키 변화 그래프 */}
      <ContentWrapper>
        <section id="growth-chart" className="mb-12">
          <h2 className="text-2xl font-bold text-green-600 mb-4">🌿 키 변화 그래프</h2>
          <GrowthChart />
        </section>
      </ContentWrapper>

      {/* 📸 타임랩스 */}
      <ContentWrapper>
        <section id="timelapse" className="mb-12">
          <h2 className="text-2xl font-bold text-blue-600 mb-4">📸 타임랩스 보기</h2>
          <TimelapseViewer />
        </section>
      </ContentWrapper>

      <footer className="text-center text-gray-500 text-sm py-6">
        Made with 💚 by Your Team
      </footer>
    </LayoutWrapper>
  );
}

export default App;

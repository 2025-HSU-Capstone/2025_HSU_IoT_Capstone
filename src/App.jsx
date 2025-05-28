import React from 'react';
import { useState } from 'react';
import axios from 'axios';
import { WoodenTitleBox, Container, HeaderText, ContentWrapper, LayoutWrapper, FloatingPlantForm } from './styles/styledComponents';
import Header from './Header';
import AutoDiarySection from './AutoDiary';
import GrowthChart from './GrowthChart';
import TimelapseViewer from './TimelapseViewer';
import PlantSetter from "./PlantSetter"; 
import {
  HangingSignWrapper,
  SignImage,
  SignText,
} from './styles/styledComponents';

function App() {
  const [plantName, setPlantName] = useState("");

  const handlePlantSubmit = async () => {
    try {
      const res = await axios.post("/plant/env-recommendation", { name: plantName });
      alert(res.data.message);
      setPlantName("");
    } catch (err) {
      alert(err.response?.data?.detail || "에러 발생");
    }
  };

  return (
    <LayoutWrapper>
      {/* 📌 상단 탭 */}
      <Header />
      {/* 📌 프로젝트 제목 */}
      <Container>
        <HangingSignWrapper>
          <SignImage src="/assets/wooden_board.jpg" alt="나무간판" />
          <SignText>야 너도 키울 수 있어</SignText>
        </HangingSignWrapper>
      </Container>

      {/* ✅ 제목 아래, 독립된 말풍선 위치 */}
        <PlantSetter />
    <div style={{ paddingTop: '80px' }}>
      {/* 📘 자동 식물 일기 */}
      <ContentWrapper>
        <section id="auto-diary" className="mb-12">
          <WoodenTitleBox>자동식물일기</WoodenTitleBox>
          <AutoDiarySection />
        </section>
      </ContentWrapper>

      {/* 📈 키 변화 그래프 */}
      <ContentWrapper>
        <section id="growth-chart" className="mb-12">
         <WoodenTitleBox>키 변화 그래프</WoodenTitleBox>
          <GrowthChart />
        </section>
      </ContentWrapper>

      {/* 📸 타임랩스 */}
      <ContentWrapper>
        <section id="timelapse" className="mb-12">
          <WoodenTitleBox>타임랩스</WoodenTitleBox>
          <TimelapseViewer />
        </section>
      </ContentWrapper>
    </div>
      
      {/* ❌ text-align 없음 */}
      {/* 즉, LayoutWrapper에 기본적으로 text-align: left 상태
        → footer는 className="text-center"로 되어 있어도 CSS 상속의 우선순위나 적용 누락으로 인해 무시될 수 있음 */}
      <footer 
        className="text-center text-gray-500 text-sm py-6"
        style={{ textAlign: 'center' }}
      >
        Made with 💚 by 허현준,이나은,이현승
      </footer>
    </LayoutWrapper>
  );
}

export default App;

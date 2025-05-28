// styledComponents.jsx
// styledComponents.jsx
import styled, {keyframes} from 'styled-components';

export const LayoutWrapper = styled.div`
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  box-sizing: border-box;
  overflow: visible;
`;

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: visible;
`;

export const HeaderText = styled.h1`
  font-size: 2rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 20px;
  color: #213547;

  @media (max-width: 600px) {
    font-size: 1.5rem;
  }
`;

export const ContentWrapper = styled.div`
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;

  @media (max-width: 768px) {
    padding: 15px;
  }
  @media (max-width: 480px) {
    padding: 10px;
  }
`;

export const EnvCard = styled.div`
  background-color: #ffffff;
  border-radius: 4px;                   // ⛔ 둥글지 않게
  padding: 32px;
  margin-top: 40px;
  width: 90%;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 8px rgba(0,0,0,0.15); // 종이 그림자
  display: flex;
  flex-direction: column;
  gap: 20px;
  text-align: left;
  border: 1px solid #ccc;
`;

export const infoStyle = {
  background: '#f6fff6',
  borderRadius: '8px',
  padding: '12px 16px',
  fontSize: '0.95rem',
  boxShadow: 'inset 0 1px 2px rgba(0,0,0,0.05)',
  lineHeight: 1.5
};

// ✅ 자동일기 전용 카드 스타일
export const DiaryCard = styled.div`
  background-color: #ffffff;
  border-radius: 16px;
  padding: 24px;
  margin-top: 24px;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
`;

export const DateContainer = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 40px;
`;

export const DateText = styled.div`
 font-size: 1.75rem;
  font-weight: bold;
  color: #1f2937;
  text-align: left;
  white-space: nowrap;
`;

export const SmallPhoto = styled.img`
   width: 140px;
  height: 140px;
  border-radius: 12px;
  object-fit: cover;
`;

export const SensorList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

export const SensorItem = styled.li`
  font-size: 0.95rem;
  margin: 4px 0;
`;

export const DiaryText = styled.p`
  font-size: 1rem;
  line-height: 1.6;
  white-space: pre-line;
  color: #333;
`;


export const FloatingPlantForm = styled.div`
  position: relative;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
  margin: 10px 20px 30px auto;
  padding: 8px 12px;
  background-color: #e6fbe8;
  border-radius: 16px;
  font-size: 0.85rem;
  color: #2e7d32;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  width: fit-content;

  &::after {
    content: "";
    position: absolute;
    right: 12px;
    top: 100%;
    border-width: 8px 8px 0 8px;
    border-style: solid;
    border-color: #e6fbe8 transparent transparent transparent;
  }
`;


const swing = keyframes`
  0%   { transform: rotate(1.2deg); }
  50%  { transform: rotate(-1.2deg); }
  100% { transform: rotate(1.2deg); }
`;

export const HangingSignWrapper = styled.div`
  position: relative;
  display: inline-block;
  margin-top: 0px;             /* ✅ 탭에 딱 붙게 */
  animation: ${swing} 3s ease-in-out infinite;
  transform-origin: top center;
`;

export const SignImage = styled.img`
  width: 260px;
  display: block;
  border-radius: 8px;
`;

export const SignText = styled.div`
  font-family: 'Gamja Flower', sans-serif;
  font-weight: normal;
  position: absolute;
  top: 60%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fffbe6;
  font-weight: 700;
  font-size: 1.3rem;
  white-space: nowrap;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);
`;

export const LeafHeaderWrapper = styled.div`
  position: fixed;              // 💡 상단 고정
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;                // ✅ 다른 요소 위에 오게
  display: flex;
  justify-content: center;
  gap: 16px;
  padding: 16px 0;
  background-color: #f4fff5;
  border-bottom: 1px solid #cceacc;
`;

export const LeafTab = styled.button`
  background: linear-gradient(135deg, #a6e6a3, #d2f5d0);
  color: #2e7d32;
  border: none;
  border-radius: 30% 70% 70% 30% / 40% 30% 70% 60%; /* 🍃 나뭇잎형 */
  padding: 12px 24px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s ease;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  }

  &.active {
    background: linear-gradient(135deg, #6fcf97, #a1e6a5);
    color: white;
  }
`;

// 말풍선 공통
export const ChatBubble = styled.div`
  max-width: 75%;
  padding: 12px 18px;
  border-radius: 16px;
  font-size: 1rem;
  position: relative;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  margin: 16px 0;
  line-height: 1.5;
  word-break: keep-all;

  
  overflow: visible;
`;

// 왼쪽 말풍선 (식물)
export const ChatLeft = styled(ChatBubble)`
  background-color:rgb(213, 247, 182);
  margin-right: auto;
  overflow: visible;
  

  &::after {
  content: "";
  position: absolute;
  top: 16px; /* 말풍선 안쪽 상단에서 약간 내려온 위치 */
  left: -12px; /* 바깥으로 밀어냄 */
  width: 0;
  height: 0;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  border-right: 12px solid rgb(213, 247, 182); /* 말풍선 배경색과 맞춰야 함 */
}

`;

// 오른쪽 말풍선 (사용자)
export const ChatRight = styled(ChatBubble)`
  background-color:rgb(220, 249, 255); /* 어두운 파란 계열 */
  color: white;
  margin-left: auto;

  &::after {
    content: "";
    position: absolute;
    top: 16px;
    right: -12px;
    width: 0;
    height: 0;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
    border-left: 12px solid rgb(220, 249, 255); /* ✅ 말풍선 배경색과 일치 */
  }
`;


// 캐릭터+말풍선용 래퍼 추가
export const ChatRowLeft = styled.div`
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin: 16px 0;
`;

export const PlantEmoji = styled.div`
  font-size: 1.5rem;
  margin-top: 6px;
`;
// 말풍선 아이콘 + 왼쪽 말풍선 묶는 래퍼
export const PlantSpeech = ({ children }) => (
  <ChatRowLeft>
    <PlantEmoji>🪴</PlantEmoji>
    <ChatLeft>{children}</ChatLeft>
  </ChatRowLeft>
);

// styledComponents.jsx 내부
export const WoodenTitleBox = styled.div`
  position: relative;
  background-image: url('https://www.transparenttextures.com/patterns/wood-pattern.png');
  background-color: #8b5e3c;
  background-size: cover;
  color: #eee2c2;
  font-size: 1.4rem;
  font-weight: 600;
  font-family: 'Gamja Flower', sans-serif;
  padding: 18px 32px;
  width: fit-content;
  max-width: 90%;
  text-align: center;
  margin: 40px 0 24px 0;
  clip-path: polygon(0% 0%, 90% 0%, 100% 50%, 90% 100%, 0% 100%);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  border-radius: 0;
  line-height: 1.4;

  /* ✅ 텍스트 음각 효과 */
  text-shadow:
    -2px -2px 2px rgba(0, 0, 0, 0.5);
     0 1px 0 rgba(0, 0, 0, 0.1);
  /* ✅ 안쪽 입체 그림자 */
  &::before {
    content: '';
    position: absolute;
    inset: 0;
    box-shadow:
      inset 0 1px 2px rgba(255, 255, 255, 0.3),
      inset 0 -2px 2px rgba(0, 0, 0, 0.4);
    z-index: 0;
  }

  /* ✅ 왼쪽 못 도트 */
  &::after {
    content: '';
    position: absolute;
    top: 6px;
    left: 10px;
    width: 8px;
    height: 8px;
    background-color: #333;
    border-radius: 50%;
    box-shadow: inset 1px 1px 2px rgba(255,255,255,0.3);
    z-index: 2;
  }

  /* ✅ 오른쪽 못 도트 (두 번째 가상 요소는 직접 span 추가 필요) */
  span.nail {
    position: absolute;
    top: 6px;
    right: 30px;
    width: 8px;
    height: 8px;
    background-color: #333;
    border-radius: 50%;
    box-shadow: inset 1px 1px 2px rgba(255,255,255,0.3);
    z-index: 2;
  }
`;


// 각 제목 나무화살표표
// export const WoodenTitleBox = styled.div`
//   position: relative;
//   background-image: url('https://www.transparenttextures.com/patterns/wood-pattern.png');
//   background-color: #8b5e3c; /* 나무색 배경과 패턴 조화 */
//   background-size: auto;
//   padding: 24px 32px;
//   margin: 40px 0 24px 0;
//   border-radius: 8px;
//   color: #fffbe6;
//   font-size: 1.5rem;
//   font-weight: 700;
//   font-family: 'Gamja Flower', sans-serif;
//   text-align: center;
//   width: fit-content;
//   max-width: 90%;
//   box-shadow: 0 4px 8px rgba(0,0,0,0.3);
//   text-shadow: 1px 1px 3px rgba(0,0,0,0.6);

//   &::after {
//     content: "";
//     position: absolute;
//     right: -20px;
//     top: 50%;
//     transform: translateY(-50%);
//     width: 0;
//     height: 0;
//     border-top: 16px solid transparent;
//     border-bottom: 16px solid transparent;
//     border-left: 20px solid #5a3d28;
//   }
// `;

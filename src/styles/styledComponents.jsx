// styledComponents.jsx
import styled from 'styled-components';

export const LayoutWrapper = styled.div`
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  box-sizing: border-box;
`;

// DateContainer 스타일 정의
export const DateContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px;
  margin-top: 20px;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

export const DateText = styled.div`
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
`;

export const SmallPhoto = styled.img`
  width: 100px;
  height: 100px;
  border-radius: 10px;
  object-fit: cover;
`;

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
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

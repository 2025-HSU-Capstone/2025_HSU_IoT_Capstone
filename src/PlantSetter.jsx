import { useState, useEffect } from "react";
import axios from "axios";
import { ChatLeft, ChatRowLeft, PlantEmoji } from "./styles/styledComponents"; // ✅ 말풍선 스타일 가져오기
import { EnvCard, infoStyle, HeaderText, SensorList, SensorItem } from "./styles/styledComponents";

// localStorage.getItem("plantName")
// 예: "상추"

function PlantSetter() {
  const [plantName, setPlantName] = useState("");
  const [envProfile, setEnvProfile] = useState(null);

  useEffect(() => {
    const savedName = localStorage.getItem("plantName");
    if (savedName) fetchEnvProfile(savedName);
  }, []);

  const fetchEnvProfile = async (name) => {
    try {
      const res = await axios.get(`http://localhost:8000/plant/env-profile/${name}`);
      setEnvProfile(res.data);
      localStorage.setItem("plantName", name);
    } catch (err) {
      if (err.response?.status === 404) {
        const recommendRes = await recommendEnv(name);
        if (recommendRes) {
          localStorage.setItem("plantName", name);
        }
      } else {
        alert("환경 정보 조회 실패");
      }
    }
  };

  const recommendEnv = async (name) => {
    try {
      const res = await axios.post(`http://localhost:8000/plant/env-recommendation`, { name });
      alert(res.data.message);
      await fetchEnvProfile(name);
      return true;
    } catch (err) {
      alert(err.response?.data?.detail || "추천 요청 실패");
      return false;
    }
  };

  const handleSubmit = () => {
    const trimmed = plantName.trim();
    if (!trimmed) return alert("식물 이름을 입력해 주세요.");
    fetchEnvProfile(trimmed);
    setPlantName("");
  };

  return (
    <>
      {/* 오른쪽 상단 입력 + 말풍선만 따로 */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-end',
        width: 'fit-content',
        marginLeft: 'auto',
        marginRight: '32px',
        marginTop: '40px',
        background: '#e6fbe8',
        padding: '16px',
        borderRadius: '16px'
      }}>
        {/* 입력창 */}
        <div style={{ marginBottom: '8px' }}>
          <input
            type="text"
            placeholder="키울 식물 이름쓰기 예:상추"
            value={plantName}
            onChange={(e) => setPlantName(e.target.value)}
            style={{
              padding: "4px 8px",
              borderRadius: "10px",
              border: "1px solid #ccc",
              marginRight: "6px",
            }}
          />
          <button
            onClick={handleSubmit}
            style={{
              background: "#4caf50",
              color: "#fff",
              border: "none",
              padding: "4px 10px",
              borderRadius: "10px",
            }}
          >
            버튼
          </button>
        </div>

        {/* 말풍선 */}
        {envProfile && (
          <ChatRowLeft>
            <PlantEmoji>🪴</PlantEmoji>
            <ChatLeft>
              <strong>{envProfile.plant_name}</strong>의 환경 기준을 불러왔어요!
            </ChatLeft>
          </ChatRowLeft>
        )}
      </div>

      {/* ⬇️ 말풍선 밖, 중앙 카드 */}
      {envProfile && (
        <EnvCard>
          <div style={{
            fontSize: '1.25rem',
            fontWeight: '600',
            color: '#2e7d32',
            marginBottom: '8px'
          }}>
            🌿 {envProfile.plant_name}의 환경 기준
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '16px',
          }}>
            <div style={infoStyle}>🌡️ 온도<br /><span>{envProfile.temperature}°C</span></div>
            <div style={infoStyle}>💧 습도<br /><span>{envProfile.humidity}%</span></div>
            <div style={infoStyle}>🫧 CO₂<br /><span>{envProfile.co2} ppm</span></div>
            <div style={infoStyle}>💡 조도<br /><span>{envProfile.light} lux</span></div>
            <div style={infoStyle}>🌱 토양 수분<br /><span>{envProfile.soil_moisture}%</span></div>
          </div>
        </EnvCard>
      )}

    </>
  );
}

export default PlantSetter;

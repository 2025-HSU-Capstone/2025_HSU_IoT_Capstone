import { useState, useEffect } from "react";
import axios from "axios";
import { ChatLeft, ChatRowLeft, PlantEmoji } from "./styles/styledComponents"; // ✅ 말풍선 스타일 가져오기

// localStorage.getItem("plantName")
// 예: "상추"

function PlantSetter() {
  const [plantName, setPlantName] = useState("");
  const [envProfile, setEnvProfile] = useState(null);

  useEffect(() => {
    const savedName = localStorage.getItem("plantName");
    if (savedName) fetchEnvProfile(savedName);
  }, []);

  useEffect(() => {
    if (envProfile) {
      console.log("🌱 envProfile (updated):", envProfile);
    }
  }, [envProfile]);

  const fetchEnvProfile = async (name) => {
    try {
      const res = await axios.get(`http://localhost:8000/plant/env-profile/${name}`);
      console.log("✅ 받은 환경 프로필:", res.data);
      setEnvProfile(res.data);
      localStorage.setItem("plantName", name);
    } catch (err) {
      if (err.response?.status === 404) {
        console.log("DB에 없음 → 추천 시도");
        const recommendRes = await recommendEnv(name);
        if (recommendRes) {
        localStorage.setItem("plantName", name); // ✅ 여기서만 저장
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
      return true; // ✅ 성공 시 true
    } catch (err) {
      alert(err.response?.data?.detail || "추천 요청 실패");
      return false; // ❌ 실패 시 false
    }
  };

  const handleSubmit = () => {
    const trimmed = plantName.trim();
    if (!trimmed) return alert("식물 이름을 입력해 주세요.");
    fetchEnvProfile(trimmed);
    setPlantName("");
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
      <div>
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

      {envProfile && (
        <ChatRowLeft>
          <PlantEmoji>🪴</PlantEmoji>
          <ChatLeft>
            <strong>{envProfile.plant_name}</strong>의 환경 기준<br />
            🌡️ {envProfile.temperature}°C / 💧 {envProfile.humidity}%<br />
            🫧 CO₂ {envProfile.co2}ppm / 💡 {envProfile.light}lux / 🌱 수분 {envProfile.soil_moisture}%
          </ChatLeft>
        </ChatRowLeft>
      )}
    </div>
  );
}

export default PlantSetter;

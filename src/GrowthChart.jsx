// GrowthChart.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { PlantSpeech, ChatRight } from './styles/styledComponents';

const GrowthChart = () => {
  const [chartData, setChartData] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [isReady, setIsReady] = useState(false);
  const [hasQueried, setHasQueried] = useState(false);

  const fetchGrowthData = async () => {
    if (!startDate || !endDate) return;

    try {
      const res = await axios.get(`http://localhost:8000/growth/chart`, {
        params: { start_date: startDate, end_date: endDate },
      });

      // 👉 날짜 포맷 수정
      const formatted = res.data.map(item => ({
        ...item,
        date: item.date.split('T')[0], // "2025-04-01T00:00:00" → "2025-04-01"
      }));

      console.log("raw data", res.data);
      
      setChartData(formatted);
      setHasQueried(true);
    } catch (err) {
      console.error("📉 그래프 데이터 로드 실패:", err);
      console.log("formatted", formatted);
      alert('그래프 불러오기 실패!');
    }
  };

  useEffect(() => {
    const fetchDateRange = async () => {
      try {
        const res = await axios.get("http://localhost:8000/growth/date-range");
        const { start_date, end_date } = res.data;
        setStartDate(start_date);
        setEndDate(end_date);
        setChartData([]);
        setIsReady(true);
      } catch (err) {
        console.error("날짜 범위 불러오기 실패", err);
      }
    };

    fetchDateRange();
  }, []);

  return (
    <div style={{ marginTop: 40 }}>
      <PlantSpeech>
        날짜를 입력하면 키 성장 추이를 보여줄게!
      </PlantSpeech>


      {isReady && (
        <ChatRight>
          <label htmlFor="start-date">시작 날짜:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
          <label htmlFor="end-date" style={{ marginLeft: '8px' }}>종료 날짜:</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
          <button
            onClick={fetchGrowthData}>
            조회
          </button>
        </ChatRight>
      )}

      {hasQueried && chartData.length > 0 && (
        <PlantSpeech>
          <div
            style={{
              display: 'block',             // ✅ 인라인-block이 아님을 보장
              width: '100%',
              maxWidth: '600px',
              height: '300px',
              minHeight: '300px',
              minWidth: '300px',            // ✅ 최소 너비 명시
              overflow: 'visible',
              background: '#fff',           // 디버깅 시 확인용 (선택)
              border: '1px dashed #ccc'     // 디버깅 시 확인용 (선택)
            }}
          >
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis label={{ value: '키(cm)', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Line type="monotone" dataKey="height" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </PlantSpeech>

      )}

      {hasQueried && chartData.length === 0 && (
        <PlantSpeech>
          📭 해당 날짜 범위에 키 변화 데이터가 없어!
        </PlantSpeech>
      )}
    </div>
  );
};

export default GrowthChart;

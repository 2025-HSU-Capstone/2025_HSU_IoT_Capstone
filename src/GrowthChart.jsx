// GrowthChart.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

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
      setChartData(res.data);
      setHasQueried(true);
    } catch (err) {
      console.error("📉 그래프 데이터 로드 실패:", err);
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
      <h1>🌿 키 변화 그래프</h1>

      {isReady && (
        <div style={{ marginBottom: 20 }}>
          <label htmlFor="start-date">시작 날짜:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            style={{
              padding: '8px',
              border: '1px solid #ccc',
              borderRadius: '8px',
              marginRight: '8px'
            }}
          />
          <label htmlFor="end-date" style={{ marginLeft: '8px' }}>종료 날짜:</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            style={{
              padding: '8px',
              border: '1px solid #ccc',
              borderRadius: '8px',
              marginRight: '8px'
            }}
          />
          <button
            onClick={fetchGrowthData}
            style={{
              padding: '8px 16px',
              backgroundColor: '#fff',
              border: '1px solid #ccc',
              borderRadius: '8px',
              cursor: 'pointer'
            }}
          >
            조회
          </button>
        </div>
      )}

      {hasQueried && chartData.length > 0 && (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis label={{ value: '키(cm)', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Line type="monotone" dataKey="height" stroke="#82ca9d" />
          </LineChart>
        </ResponsiveContainer>
      )}

      {hasQueried && chartData.length === 0 && (
        <p style={{ marginTop: 20 }}>📭 해당 날짜 범위에 키 변화 데이터가 없습니다.</p>
      )}
    </div>
  );
};

export default GrowthChart;

// AutoDiary.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { DateContainer, DateText, SmallPhoto } from './styles/styledComponents';  // 스타일 불러오기

const AutoDiarySection = () => {
  const [date, setDate] = useState(null);
  const [availableDates, setAvailableDates] = useState([]);
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchDates = async () => {
      try {
        const res = await axios.get('http://localhost:8000/diary/available-dates');
        const validDates = res.data.map(d => new Date(d));
        setAvailableDates(validDates);

        const latest = await axios.get('http://localhost:8000/diary/latest-date');
        setDate(new Date(latest.data.latest_date));
      } catch (err) {
        console.error("날짜 불러오기 실패", err);
      }
    };

    fetchDates();
  }, []);

  const fetchDiary = async () => {
    if (!date) return;
    const formatted = date.toISOString().split('T')[0];
    try {
      const res = await axios.get(`http://localhost:8000/diary/auto/${formatted}`);
      setData(res.data);
    } catch (err) {
      setData(null);
      alert("일기 데이터가 없습니다.");
    }
  };

  return (
    <div style={{ marginTop: 40 }}>
      <h1>📘 자동 식물 일기</h1>

      <DatePicker
        selected={date}
        onChange={(d) => setDate(d)}
        includeDates={availableDates}
        dateFormat="yyyy-MM-dd"
        placeholderText="자동일기 있는 날짜만 선택 가능"
        className="custom-datepicker"
      />
      <button onClick={fetchDiary} disabled={!date}>조회</button>

      {data && (
        <div style={{ marginTop: 20 }}>
          <DateContainer>
            <DateText>{data.date} ({data.day})</DateText>
            <SmallPhoto
              src={`http://localhost:8000${data.photo_path}`}
              alt="식물 사진"
            />
          </DateContainer>

          <h3>🌱 센서 정보</h3>
          <ul>
            <li>📏 오늘 키: {data.sensor_data.height_today}</li>
            <li>📏 어제 키: {data.sensor_data.height_yesterday}</li>
            <li>💧 토양 습도: {data.sensor_data.soil_moisture}</li>
            <li>💡 조도: {data.sensor_data.light}</li>
            <li>🌡️ 온도: {data.sensor_data.temperature}℃</li>
            <li>💦 습도: {data.sensor_data.humidity}%</li>
            <li>🫁 CO₂: {data.sensor_data.co2}ppm</li>
          </ul>

          <p><b>일기:</b> {data.diary}</p>
        </div>
      )}
    </div>
  );
};

export default AutoDiarySection;

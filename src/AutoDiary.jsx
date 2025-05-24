// AutoDiary.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

import {
  DateContainer,
  DateText,
  SmallPhoto,
  DiaryCard,
  SensorList,
  SensorItem,
  DiaryText,
  ChatLeft,
  ChatRight,
  ChatRowLeft, 
  PlantEmoji,
  PlantSpeech
} from './styles/styledComponents';

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
      {/* 왼쪽 말풍선: 제목 */}
        <PlantSpeech>
          내 일기를 보고싶으면 날짜를 입력해
        </PlantSpeech>

      {/* 오른쪽 말풍선: 날짜 선택 + 버튼 */}
      <ChatRight>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          <DatePicker
            selected={date}
            onChange={(d) => setDate(d)}
            includeDates={availableDates}
            dateFormat="yyyy-MM-dd"
            placeholderText="날짜를 골라주세요"
            className="custom-datepicker"
          />
          <button onClick={fetchDiary} disabled={!date}>go</button>
        </div>
      </ChatRight>

      {/* 결과 일기 카드 */}
      {data && (
        <PlantSpeech>
          <DiaryCard style={{ boxShadow: 'none', marginTop: 0, marginBottom: 0 }}>
            <DateContainer>
              <DateText>{data.date} ({data.day})</DateText>
              <SmallPhoto
                src={`data.photo_path`}
                alt="식물 사진"
              />
            </DateContainer>

            <h3>🌱 센서 정보</h3>
            <SensorList>
              <SensorItem>📏 오늘 키: {data.sensor_data.height_today}</SensorItem>
              <SensorItem>📏 어제 키: {data.sensor_data.height_yesterday}</SensorItem>
              <SensorItem>💧 토양 습도: {data.sensor_data.soil_moisture}</SensorItem>
              <SensorItem>💡 조도: {data.sensor_data.light}</SensorItem>
              <SensorItem>🌡️ 온도: {data.sensor_data.temperature}℃</SensorItem>
              <SensorItem>💦 습도: {data.sensor_data.humidity}%</SensorItem>
              <SensorItem>🫁 CO₂: {data.sensor_data.co2}ppm</SensorItem>
            </SensorList>

            <DiaryText><b>일기:</b> {data.diary}</DiaryText>
          </DiaryCard>
        </PlantSpeech>
      )}
    </div>

  )
};

export default AutoDiarySection;
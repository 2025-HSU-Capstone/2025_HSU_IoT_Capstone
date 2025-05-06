import React, { useEffect, useState } from 'react';
import axios from 'axios';

const TimelapseViewer = () => {
  const [images, setImages] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [isReady, setIsReady] = useState(false);
  const [hasQueried, setHasQueried] = useState(false);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  // 📡 날짜 자동 설정
  const fetchDateRange = async () => {
    try {
      const res = await axios.get("http://localhost:8000/timelapse/date-range");
      const { start_date, end_date } = res.data;
      setStartDate(start_date);
      setEndDate(end_date);
      setIsReady(true);
    } catch (err) {
      console.error("날짜 범위 가져오기 실패", err);
    }
  };

  // 📸 이미지 요청
  const fetchImages = async () => {
    try {
      const res = await axios.get("http://localhost:8000/timelapse/images", {
        params: { start_date: startDate, end_date: endDate },
      });
      setImages(res.data.images);
      setHasQueried(true);
      setCurrentIndex(0);  // 시작 인덱스 초기화
      setIsPlaying(true);  // 재생 시작
    } catch (err) {
      console.error("이미지 불러오기 실패", err);
    }
  };

  // ▶️ 슬라이드 자동 재생 로직
  useEffect(() => {
    let timer = null;
    if (isPlaying && images.length > 0) {
      timer = setInterval(() => {
        setCurrentIndex((prev) => {
            if (prev + 1 < images.length) {
              return prev + 1;
            } else {
              setIsPlaying(false);  // 🔥 마지막 이미지면 재생 멈춤!
              return prev;
            }
          });
      }, 1000); // 1초 간격
    }
    return () => clearInterval(timer);
  }, [isPlaying, images]);

  useEffect(() => {
    fetchDateRange();
  }, []);

  return (
    <div style={{ marginTop: 40 }}>
      <h1 style={{
        fontSize: '2.25rem',
        fontWeight: 700,
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        marginBottom: '1rem'
      }}>
        📸 타임랩스 보기
      </h1>

      {isReady && (
        <div style={{
          marginBottom: 20,
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          flexWrap: 'wrap'
        }}>
          <label>시작 날짜:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            style={{
              padding: '8px',
              border: '1px solid #ccc',
              borderRadius: '8px'
            }}
          />

          <label>종료 날짜:</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            style={{
              padding: '8px',
              border: '1px solid #ccc',
              borderRadius: '8px'
            }}
          />

          <button
            onClick={fetchImages}
          >
            조회
          </button>
        </div>
      )}

      {/* 슬라이드 영역 */}
      {hasQueried && images.length > 0 && (
        <div style={{ textAlign: 'center' }}>
          <img
            src={`http://localhost:8000${images[currentIndex].path}`}
            alt={`타임랩스 ${images[currentIndex].date}`}
            style={{
              width: '300px',
              height: 'auto',
              borderRadius: '12px',
              boxShadow: '0 0 10px rgba(0,0,0,0.1)'
            }}
          />
          <div style={{ fontSize: '1rem', marginTop: '8px' }}>
            {images[currentIndex].date}
          </div>
        </div>
      )}

      {hasQueried && images.length === 0 && (
        <p style={{ marginTop: 20 }}>📭 해당 날짜 범위에 사진이 없습니다.</p>
      )}
    </div>
  );
};

export default TimelapseViewer;

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { PlantSpeech, ChatRight } from './styles/styledComponents';

const TimelapseViewer = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [isReady, setIsReady] = useState(false);

  const [videoUrl, setVideoUrl] = useState('');
  const [isVideoReady, setIsVideoReady] = useState(false);

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

  // 📹 타임랩스 영상 요청
  const fetchVideo = async () => {
    try {
      const res = await axios.get("http://localhost:8000/timelapse/video", {
        params: { start_date: startDate, end_date: endDate },
      });
      setVideoUrl(res.data.video_url);
      setIsVideoReady(true);
    } catch (err) {
      console.error("타임랩스 영상 불러오기 실패", err);
    }
  };

  useEffect(() => {
    fetchDateRange();
  }, []);

  return (
    <div style={{ marginTop: 40 }}>
      <PlantSpeech>
        날짜를 설정하면 자라는 모습을 영상으로 보여줄게!
      </PlantSpeech>

      {isReady && (
        <ChatRight>
          <label>시작 날짜:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
          <label style={{ marginLeft: '8px' }}>종료 날짜:</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
          <button onClick={fetchVideo} style={{ marginLeft: '8px' }}>
            영상 보기
          </button>
        </ChatRight>
      )}

      {isVideoReady && (
        <PlantSpeech>
          <div style={{ textAlign: 'center' }}>
            <video
              src={videoUrl}
              controls
              style={{
                width: '100%',
                maxWidth: '600px',
                borderRadius: '12px',
                boxShadow: '0 0 10px rgba(0,0,0,0.1)',
              }}
            />
          </div>
        </PlantSpeech>
      )}
    </div>
  );
};

export default TimelapseViewer;

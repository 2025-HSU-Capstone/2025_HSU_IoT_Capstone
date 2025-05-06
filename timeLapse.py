import sys
sys.stdout.reconfigure(encoding='utf-8')

import cv2
import os
from natsort import natsorted
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips

# 📁 이미지 폴더 경로
image_folder = './images'
output_video = 'timelapse.mp4'

# 📸 이미지 파일 목록 정렬
images = [img for img in os.listdir(image_folder) if img.endswith(('.jpg', '.png'))]
images = natsorted(images)  # 숫자 순 정렬

# 첫 이미지로 프레임 사이즈 설정
first_frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = first_frame.shape
size = (width, height)

# 🎞️ 비디오 객체 생성 (코덱: mp4v, fps: 10)
out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 10, size)

for img in images:
    frame = cv2.imread(os.path.join(image_folder, img))
    out.write(frame)

out.release()
print("✅ 타임랩스 영상 생성 완료:", output_video)

# 🎞️ 입력 파일 경로
video_path = "timelapse.mp4"
audio_path = "music.mp3"
output_path = "timelapse_with_music.mp4"

# 영상과 음악 불러오기
video = VideoFileClip(video_path)
audio = AudioFileClip(audio_path)

# 음악 반복: 영상 길이에 맞게 충분히 반복한 후 자르기
n_loops = int(video.duration // audio.duration) + 1
audio_looped = concatenate_audioclips([audio] * n_loops).subclipped(0, video.duration)

# (선택) 음악 볼륨 줄이기 – 필요 시 사용
# audio_looped = audio_looped.volumex(0.6)

# 오디오 붙이기
final_video = video.with_audio(audio_looped)

# 출력 저장
final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

print("✅ 음악 추가된 영상 저장 완료:", output_path)

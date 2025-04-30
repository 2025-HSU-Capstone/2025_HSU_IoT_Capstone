from ultralytics import YOLO
import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import numpy as np
import os

# === 1. 아루코 마커 생성 및 합성 ===

# (1) 마커 생성
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
marker_img = aruco.generateImageMarker(aruco_dict, id=0, sidePixels=100)
marker_img = cv2.cvtColor(marker_img, cv2.COLOR_GRAY2BGR)

# (2) 이미지 로드
image_path = "/Users/heohyeonjun/Desktop/IoT_Capstone/2025_HSU_IoT_Capstone/화분.jpg"
image = cv2.imread(image_path)
h, w, _ = image.shape

# (3) 마커 붙일 위치 계산 (중간 하단)
x_offset = w // 2 - 50  # 가운데
y_offset = h - 150      # 하단 100px 위

# (4) 마커 합성
image[y_offset:y_offset+100, x_offset:x_offset+100] = marker_img

# === 2. YOLO 모델 로드 ===
model = YOLO("/Users/heohyeonjun/Desktop/IoT_Capstone/2025_HSU_IoT_Capstone/runs/train/plant_pot_model2/weights/best.pt")

# === 3. 추론 수행 ===
results = model.predict(source=image, conf=0.3, save=False, show=False)

# === 4. 시각화 ===
for r in results:
    for box in r.boxes:
        cls_id = int(box.cls.item())
        conf = float(box.conf.item())
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        
        y1 = y1 + int(0.1 * (y2 - y1))
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        label = f"flowerpot {conf:.2f}"
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        # 순수 식물 길이 계산 (화분 상단부터 이미지 맨 위까지)
        plant_height_px = y1
        pixel_per_cm = 100 / 5  # 예시: 아루코 마커 100px = 5cm
        plant_height_cm = round(plant_height_px / pixel_per_cm, 2)

        print(f"🌿 순수 식물 높이: {plant_height_px}px ≈ {plant_height_cm}cm")

        # 시각화 (식물 높이 선)
        line_x = x2 + 20
        cv2.line(image, (line_x, 0), (line_x, y1), (0, 255, 0), 2)
        cv2.putText(image, f"{plant_height_cm} cm", (line_x + 10, y1 // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# === 5. 결과 출력 ===
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(8, 6))
plt.imshow(image_rgb)
plt.axis("off")
plt.title("Flowerpot Detection with ArUco")
plt.show()
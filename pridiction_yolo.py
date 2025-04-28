from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os

# 1. 학습된 모델 로드
model = YOLO("/Users/heohyeonjun/Desktop/IoT_Capstone/2025_HSU_IoT_Capstone/runs/train/plant_pot_model2/weights/best.pt")

# 2. 추론할 이미지 경로
image_path = "/Users/heohyeonjun/Desktop/IoT_Capstone/2025_HSU_IoT_Capstone/화분.jpg"
image_filename = os.path.basename(image_path)

# 3. 추론 수행
results = model.predict(source=image_path, conf=0.3, save=False, show=False)

# 4. 원본 이미지 불러오기
image = cv2.imread(image_path)

# 5. 바운딩박스 후처리 및 그리기
for r in results:
    for box in r.boxes:
        cls_id = int(box.cls.item())
        conf = float(box.conf.item())
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        # 상단 20% 잘라낸 조정된 y1
        adjusted_y1 = y1 + 0.2 * (y2 - y1)

        # 원래 YOLO 박스 (회색)
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (180, 180, 180), 2)

        # 조정된 박스 (파란색)
        cv2.rectangle(image, (int(x1), int(adjusted_y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        label = f"flowerpot adj {conf:.2f}"
        cv2.putText(image, label, (int(x1), int(adjusted_y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# 6. 결과 시각화
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(8, 6))
plt.imshow(image_rgb)
plt.axis("off")
plt.title("Adjusted Flowerpot Detection")
plt.show()

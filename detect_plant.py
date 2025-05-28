import os
import cv2
import json
from ultralytics import YOLO

# ✅ 기준 디렉토리 설정 (detect_plant.py가 위치한 폴더 기준)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ 경로 설정
IMAGE_PATH = os.path.join(SCRIPT_DIR, "screenshot.jpg")
MODEL_PATH = os.path.join(SCRIPT_DIR, "yolo_model", "best.pt")
SAVE_PATH = os.path.join(SCRIPT_DIR, "result_with_boxes.jpg")
HEIGHT_JSON_PATH = os.path.join(SCRIPT_DIR, "height.json")
PIXEL_TO_CM = 0.0552  # cm per pixel from ArUco calibration

# ✅ 1. Raspberry Pi 카메라로 실시간 사진 촬영 (libcamera-still 사용)
print("📸 Capturing image using Raspberry Pi Camera Module 3...")
capture_command = f"libcamera-still -o {IMAGE_PATH} --width 640 --height 480 --nopreview --timeout 1000"
exit_code = os.system(capture_command)

if exit_code != 0 or not os.path.exists(IMAGE_PATH):
    raise RuntimeError("❌ Failed to capture image with libcamera-still")

print(f"✅ Image saved to {IMAGE_PATH}")

# ✅ 2. YOLO 모델 로딩 및 이미지 분석
image = cv2.imread(IMAGE_PATH)
if image is None:
    raise FileNotFoundError(f"❌ Cannot load captured image: {IMAGE_PATH}")

print("🧠 Running YOLO inference...")
model = YOLO(MODEL_PATH)
results = model(image)

# ✅ 3. 식물 객체의 bounding box 탐지
plant_top_y, plant_bottom_y = None, None

for r in results:
    boxes = r.boxes
    for box in boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = model.names[cls_id]

        if label == "plant":
            plant_top_y = min(plant_top_y, y1) if plant_top_y is not None else y1
            plant_bottom_y = max(plant_bottom_y, y2) if plant_bottom_y is not None else y2

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# ✅ 4. 키 계산 및 height.json 저장
if plant_top_y is not None and plant_bottom_y is not None:
    height_px = plant_bottom_y - plant_top_y
    height_cm = height_px * PIXEL_TO_CM
    print(f"📏 Estimated plant height: {height_cm:.2f} cm")

    cv2.putText(image, f"Height: {height_cm:.2f} cm", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    with open(HEIGHT_JSON_PATH, "w") as f:
        json.dump({"height_cm": round(height_cm, 2)}, f)
    print(f"✅ Saved height_cm to {HEIGHT_JSON_PATH}")
else:
    print("⚠️ No plant detected.")
    if os.path.exists(HEIGHT_JSON_PATH):
        os.remove(HEIGHT_JSON_PATH)
        print("🧹 Removed old height.json")

# ✅ 5. 결과 이미지 저장
cv2.imwrite(SAVE_PATH, image)
print(f"🖼️ Result saved to {SAVE_PATH}")

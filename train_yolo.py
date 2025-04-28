import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

from ultralytics import YOLO

# 모델 로드 (pretrained yolov8n 사용)
model = YOLO("yolov8n.pt")

# 학습 실행
model.train(
    data="/Users/heohyeonjun/Desktop/IoT_Capstone/2025_HSU_IoT_Capstone/YOLOdataset/data.yaml",  # ← data.yaml 경로 (상대 or 절대)
    epochs=50,
    imgsz=640,
    batch=16,
    name="plant_pot_model",         # 결과가 저장될 디렉토리 이름
    project="runs/train",           # 결과 root 디렉토리
    device="mps"                        # GPU 사용 (없으면 CPU로 자동 fallback)
)


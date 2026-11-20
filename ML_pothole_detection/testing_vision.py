import cv2 as cv
from ml_engine import Ml_Engine
import numpy as np
# from gps_module import GPS

engine = Ml_Engine(
    model=r"C:\Users\Asus\Downloads\exp-6.onnx",
    conf_thresh=0.2,
    nms_thresh=0.2
)

# gps=GPS(port="", baudrate=9600)
# gps.read()

cap = cv.VideoCapture(r"C:\Users\Asus\Videos\Screen Recordings\Screen Recording 2026-11-16 134308.mp4")

while cap.isOpened():
    succes, frame = cap.read()
    
    # WAJIB pakai break supaya tidak lanjut ke engine.pred(None) saat video habis
    if not succes or frame is None:
        print("Video selesai atau gagal dibaca.")
        break

    Boxes = engine.pred(frame)
    if Boxes is not None:
        for box in Boxes:
            track_id, cls_name, x, y, w, h, confidence = [
                box[k] for k in ["track_id", "class_name", "x1", "y1", "w", "h", "confidence"]
            ]
            # Pastikan koordinat integer agar cv.rectangle tidak error
            x, y, w, h = int(x), int(y), int(w), int(h)
            
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(
                frame,
                f"{confidence:.2f}, track_id: {track_id}",
                (x, y - 10),
                cv.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2,
            )
            # location: dict[str, float] = gps.get_location()

    cv.imshow("frame", frame)

    # Gunakan waitKey(1) agar video jalan otomatis, tekan 'q' untuk berhenti
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv.destroyAllWindows()

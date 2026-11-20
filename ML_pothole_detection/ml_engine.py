#TODO:
"""
1. tentukan lokasi model (format onnyx masih plan)
2. membaca model menggunakan dnn
3. check device, optimalin pake gpu kalo ga ada handle pake cpu
4. baca arsitektur layer dari model
5. lakuin prediksi pake fungsi forward()
6. Biasanya hasil prediksi formatnya bakal ga enak 
[batch(biasanya 1 jadi ilangin aja),baris(x,y,w,h), kolom(value dari baris)]
7. ilangin batch pake np.sequeence, kemudian transpose supaya [kolom(value dari baris), baris(x,y,w,h,..)]
8. acces array hasil prediksi menggunakan for loop (utamanya akses barisnya)
9. tampung x,y,w,h didalam boxes, tampung confidence di conf, dan tampung conf id cls id
10. gunakan nmsboxes pada conf dan box
11. hasil dari indeces kita gunain buat olah boxes, cls_id, dan conf supaya bisa dijadiin satu
12. rencanya step 11 bakal dilakuin dan ditampung di detections format dict
13. hasil nmsBoxes diflatten 
14. selanjutnya akses boxes dan conf, dan cls_id
15. tampung 3 feature itu di detection dictionary
"""

import cv2 as cv
import numpy as np
import supervision as sv
import onnxruntime as ort
from trackers import ByteTrackTracker

class Ml_Engine:
    def __init__(self, model=None, conf_thresh=0.7, nms_thresh=0.4, track_activation: float = 0.25, minimum_consecutive_frames: int = 1):
        if model is None:
            raise ValueError("Model path must be defined")
        
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        self.session = ort.InferenceSession(model, providers=providers)
        
        self.input_name = self.session.get_inputs()[0].name
        self.input_type = self.session.get_inputs()[0].type
        self.output_names = [out.name for out in self.session.get_outputs()]
        
        self.conf_thresh = conf_thresh
        self.nms_thresh = nms_thresh
        self.tracker = ByteTrackTracker(
            track_activation_threshold=track_activation,
            minimum_consecutive_frames=minimum_consecutive_frames
        )

    def pred(self, frame) -> list[dict]:
        h_real, w_real, _ = frame.shape
        x_fact, y_fact = w_real / 640.0, h_real / 640.0
        
        blob = cv.dnn.blobFromImage(frame, scalefactor=1/255.0, size=(640, 640), swapRB=True, crop=False)
        if 'float16' in self.input_type:
            blob = blob.astype(np.float16)

        outputs = self.session.run(self.output_names, {self.input_name: blob})
        output = np.squeeze(outputs[0]).astype(np.float32)
        
        if output.shape[0] < output.shape[1]:
            output = output.T  # (8400, 5)

        scores = np.max(output[:, 4:], axis=1)
        mask = scores > self.conf_thresh
        valid_preds = output[mask]

        # Default deteksi kosong (tetap wajib masuk tracker.update agar state waktu tracker jalan)
        sv_detections = sv.Detections.empty()

        if len(valid_preds) > 0:
            valid_scores = scores[mask]
            valid_cls_ids = np.argmax(valid_preds[:, 4:], axis=1)

            cx, cy, w_img, h_img = valid_preds[:, 0], valid_preds[:, 1], valid_preds[:, 2], valid_preds[:, 3]
            
            # Clipping koordinat agar tidak keluar batas resolusi gambar
            x1 = np.clip((cx - 0.5 * w_img) * x_fact, 0, w_real)
            y1 = np.clip((cy - 0.5 * h_img) * y_fact, 0, h_real)
            x2 = np.clip((cx + 0.5 * w_img) * x_fact, 0, w_real)
            y2 = np.clip((cy + 0.5 * h_img) * y_fact, 0, h_real)
            width = x2 - x1
            height = y2 - y1

            # 1. Format [x1, y1, width, height] khusus untuk OpenCV NMSBoxes
            boxes_xywh = np.column_stack((x1, y1, width, height)).tolist()
            # 2. Format [x1, y1, x2, y2] khusus untuk Supervision & Output
            boxes_xyxy = np.column_stack((x1, y1, x2, y2)).astype(np.float32)

            indices = cv.dnn.NMSBoxes(boxes_xywh, valid_scores.tolist(), self.conf_thresh, self.nms_thresh)

            if len(indices) > 0:
                idx = indices.flatten()
                sv_detections = sv.Detections(
                    xyxy=boxes_xyxy[idx],
                    confidence=valid_scores[idx].astype(np.float32),
                    class_id=valid_cls_ids[idx].astype(int)
                )

        # Update tracker di setiap frame (baik ada deteksi maupun kosong)
        tracked = self.tracker.update(sv_detections)

        # Susun output akhir list[dict] lengkap dengan track_id
        detections = []
        if len(tracked) > 0:
            for i in range(len(tracked)):
                bx1, by1, bx2, by2 = tracked.xyxy[i].astype(int)
                track_id = int(tracked.tracker_id[i]) if tracked.tracker_id is not None else -1
                
                detections.append({
                    "track_id": track_id,
                    "class_id": int(tracked.class_id[i]),
                    "class_name": "pothole",
                    "confidence": round(float(tracked.confidence[i]), 2),
                    "x1": int(bx1),
                    "y1": int(by1),
                    "x2": int(bx2),
                    "y2": int(by2),
                    "w": int(bx2 - bx1),
                    "h": int(by2 - by1)
                })

        return detections
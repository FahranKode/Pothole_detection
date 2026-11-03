import cv2 as cv
import numpy as np

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

class Ml_Engine():
    def __init__(self, model=None, conf_thresh=0.7, nms_thresh=0.4):
        self.model=cv.dnn.readNetFromONNX(model) if model is not None else print("model path not defined")
        self.conf_thresh=conf_thresh
        self.nms_thresh=nms_thresh
    def pred(self,frame):
        h_real,w_real,_=frame.shape
        x_fact,y_fact=w_real/640,h_real/640
        
        # pastiin atur ulang karena kamera mempunya beberapa parameter yang berbeda contohnya resolusi
        blob = cv.dnn.blobFromImage(frame, scalefactor=1/255.0, size=(640, 640), swapRB=True, crop=False)
    
        self.model.setInput(blob)
        output_layers = self.model.getUnconnectedOutLayersNames()
        
        #forward layer
        pred=self.model.forward(output_layers) #[batch,baris(x,y,w,h,conf,...),kolom(nilai dari x,y,w,h,conf,...)]
        pred=np.squeeze(pred).T #expected [batch,baris,kolom,conf...] -> [baris,kolom,conf] -> T = [kolom,baris] 
        
        #prediction result
        boxes=[]
        conf=[]
        cls_id=[]
        
        for row in pred:
            if conf>self.conf_thresh: # -> bool
                cx,cy,w_img,h_img=row[0:4] # -> cx=koor_x,cy=koor_y,w=witdh,h=height 
                left = int((cx - 0.5 * w_img) * x_fact)
                top = int((cy - 0.5 * h_img) * y_fact)
                width = int(w_img * x_fact)
                height = int(h_img * y_fact)
        
                boxes.append([left,top,width,height]) # -> [left,top,width,height]
                conf.append(row[4]) # -> [conf]
                cls_id.append(row[4]) #[conf1, conf2, ....]
            indices=cv.dnn.NMSBoxes(boxes, conf, self.conf_threshold, self.nms_thresh) # ga numpuk
        
            detections = []
            if len(indices) > 0:
                for i in indices.flatten():
                    box = boxes[i]
                    x1 = max(0, box[0])
                    y1 = max(0, box[1])
                    x2 = min(w_img, box[0] + box[2])
                    y2 = min(h_img, box[1] + box[3])
                    detections.append({
                        "class_id": cls_id[i],
                        "class_name": "pothole",
                        "confidence": round(conf[i], 2),
                        "x1": float(x1),
                        "y1": float(y1),
                        "x2": float(x2),
                        "y2": float(y2)
                    }) # -> {dict}
            return detections

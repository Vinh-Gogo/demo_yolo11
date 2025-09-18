import cv2
from ultralytics import YOLO
from flask import Flask, Response

app = Flask(__name__)
path_model_trained = "./runs/detect/train10/weights/best.pt"
model = YOLO(path_model_trained)  # load model YOLOv11

def gen_frames():
    cap = cv2.VideoCapture(0)  # mở webcam
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # chạy YOLOv11 trên frame
            results = model(frame)
            annotated = results[0].plot()

            # mã hóa frame sang JPEG
            _, buffer = cv2.imencode('.jpg', annotated)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video')
def video():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host="0.0.0.0", port=5000)
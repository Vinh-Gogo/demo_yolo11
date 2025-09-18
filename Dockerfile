FROM ultralytics/ultralytics:latest

WORKDIR /app

# Copy file app
COPY app.py /app/

# Cài Flask + OpenCV
RUN pip install flask opencv-python

# Mở cổng Flask
EXPOSE 5000

CMD ["python", "app.py"]
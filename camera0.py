import cv2
import queue
import os
import threading
import time
from darknet.darknet import *
from register_python_csv.publish import run

frames = queue.Queue()


def receive(rtsp_cam, id_camera):
    cap = cv2.VideoCapture(rtsp_cam, cv2.CAP_FFMPEG)
    while True:
        conectado = False
        ret, frame = cap.read()
        if ret:
            conectado = True
            frame = cv2.resize(frame, (416, 416))
            try:
                frames.get_nowait()
            except queue.Empty:
                pass
            try:
                frames.put([frame, id_camera])
            except:
                pass

        if conectado == False:
            print("Falha na conexão com o RTSP: " + rtsp_cam)
            print("Tentativa de reconexão em 60 segundos ...")

            for categoria in class_names:
                if categoria != "Placa":
                    threading.Thread(target=mqtt, args=(
                        "-1", categoria, "contagem", id_camera, )).start()

            time.sleep(60)
            receive(rtsp_cam, id_camera)


def camera0(rtsp_cam, id_camera, model, line):
   ...

    while True:
        fluxo = time.time()
        frame = frames.get()

        if frame is None:
            break

        classes, scores, boxes = model.detect(frame[0], float(
            os.getenv("CONFIDENCE_THRESHOLD")), float(os.getenv("NMS_THRESHOLD")))

        for (classid, score, box) in zip(classes, scores, boxes):
            color = COLORS[int(classid) % len(COLORS)]
            label = str(class_names[classid])
   ...
        

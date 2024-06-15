'''
This file contains the functions for Flight control
'''
import cv2
import djitellopy
from djitellopy import *
from ultralytics import YOLO
import threading

model = YOLO("yolov8n.pt")

t = tello.Tello()
t.connect()  # connect to tello
print("connection established")

# video parameter
# t.set_video_resolution(t.RESOLUTION_720P)
# t.set_video_fps(t.FPS_30)
# t.set_video_direction(1)


t.streamon()
print("streaming on")

battery = [t.get_battery()]  # record starting battery volume


def video_stream(drone):
    while True:
        frame = drone.get_frame_read().frame
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow("f", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    drone.streamoff()


def drone_operation():
    while True:
        t.turn_motor_on()


operation_thread = threading.Thread(target=drone_operation)
streaming_thread = threading.Thread(target=video_stream, args=(t,))

operation_thread.start()
streaming_thread.start()

operation_thread.join()
streaming_thread.join()

battery.append(t.get_battery())  # record finish battery level
print("Drone start battery is {}, drone end battery is {}".format(battery[0], battery[1]))
t.end()

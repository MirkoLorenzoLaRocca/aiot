from email.mime import audio
import wave
from multiprocessing import Process, Event
from multiprocessing.connection import _ConnectionBase
import time
import csv
from collections import deque
import numpy as np
from pynput import keyboard

def is_stationary(current_data, previous_data, threshold):
    for i in range(len(current_data)):
        if abs(current_data[i] - previous_data[i]) > threshold:
            return False
    return True

class ITSGesture(Process):
    sensor_rx: _ConnectionBase
    audio_rx: _ConnectionBase

    def __init__(self, sensor_rx, audio_rx):
        Process.__init__(self)

        self.sensor_rx = sensor_rx
        self.audio_rx = audio_rx

        self.can_run = Event()

    def run(self, threshold=0.40):
        label = "in attesa"
        paused = False
        
        def on_press(key):
            nonlocal paused
            if key == keyboard.Key.space:
                paused = not paused
                if paused:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    with open("tactigon/registrazioni.csv", "a", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([timestamp, "Stop", "", "", "", "", "", ""])
                else:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    with open("tactigon/registrazioni.csv", "a", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([timestamp, "Start", "", "", "", "", "", ""])

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        while self.can_run.is_set():
            if not paused and self.sensor_rx.poll():
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                accX, accY, accZ, gyroX, gyroY, gyroZ = self.sensor_rx.recv()
                data = [accX, accY, accZ, gyroX, gyroY, gyroZ]
                magnitude = np.sqrt((accX)**2 + (accY)**2 + (accZ)**2)
                
                if magnitude > threshold:
                    label = "in movimento"
                else:
                    label = "fermo"

                print(f"accX:{accX:.2f} accY:{accY:.2f} accZ:{accZ:.2f} gyroX:{gyroX:.2f} gyroY:{gyroY:.2f} gyroZ:{gyroZ:.2f}, stato:{label}, magnitude:{magnitude:.2f}")

                with open("tactigon/registrazioni.csv", "a", newline='') as f:
                    writer = csv.writer(f)
                    if f.tell() == 0:
                        writer.writerow(["timestamp", "accX", "accY", "accZ", "gyroX", "gyroY", "gyroZ", "label"])

                    writer.writerow([timestamp, f"{accX:.2f}", f"{accY:.2f}", f"{accZ:.2f}", f"{gyroX:.2f}", f"{gyroY:.2f}", f"{gyroZ:.2f}", label])

        listener.stop()

    def stop(self):
        self.can_run.clear()
            # if self.audio_rx.poll():
            #     with wave.open("test.wav", "wb") as audio_file:
            #         audio_file.setnchannels(1)
            #         audio_file.setframerate(16000)
            #         audio_file.setsampwidth(2)

            #         while self.audio_rx.poll(1):
            #             audio_bytes = self.audio_rx.recv_bytes()
            #             audio_file.writeframes(audio_bytes)




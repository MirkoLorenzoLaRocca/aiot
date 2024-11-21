from collections import deque
import numpy as np
import torch
import joblib
from pynput import keyboard
from multiprocessing import Process, Event
from multiprocessing.connection import _ConnectionBase
import time
import csv
from .inferenza import LSTMModel
from sklearn.preprocessing import LabelEncoder
import joblib

class ITSGesture(Process):
    sensor_rx: _ConnectionBase
    audio_rx: _ConnectionBase

    def __init__(self, sensor_rx, audio_rx):
        Process.__init__(self)

        self.sensor_rx = sensor_rx
        self.audio_rx = audio_rx

        self.can_run = Event()
        self.buffer = deque(maxlen=20)  
        
        self.scaler = joblib.load("preprocessing/standard_scaler.pkl")
        self.input_size = 8
        self.hidden_size = 512
        self.num_layers = 3
        self.num_classes = 4
        self.dropout = 0.2
        self.device = "cpu"

        self.model = LSTMModel(
            self.input_size, self.hidden_size, self.num_layers, self.num_classes, self.dropout
        ).to(self.device)
        self.model.load_state_dict(torch.load("best_model2.pth", map_location=self.device))
        self.model.eval()

    def run(self, threshold=0.50):
        label = "in attesa"
        paused = False

        def on_press(key):
            nonlocal paused
            if key == keyboard.Key.space:
                paused = not paused
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                with open("tactigon/registrazioni.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    if paused:
                        writer.writerow([timestamp, "Stop", "", "", "", "", "", ""])
                    else:
                        writer.writerow([timestamp, "Start", "", "", "", "", "", ""])

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        while self.can_run.is_set():
            time.sleep(0.01)
            if not paused and self.sensor_rx.poll():
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                accX, accY, accZ, gyroX, gyroY, gyroZ = self.sensor_rx.recv()
                magnitude_acc = np.sqrt(accX**2 + accY**2 + accZ**2)
                magnitude_gyro = np.sqrt(gyroX**2 + gyroY**2 + gyroZ**2)
                label = "in movimento" if magnitude_gyro > threshold else "fermo"

                self.buffer.append([accX, accY, accZ, gyroX, gyroY, gyroZ, magnitude_acc, magnitude_gyro, label])

                if len(self.buffer) == 20 and label == "in movimento":
                    predicted_class = self.perform_inference(self.buffer)
                    print(f"Movimento: {predicted_class}")

                with open("tactigon/registrazioni.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    if f.tell() == 0:  
                        writer.writerow(["timestamp", "accX", "accY", "accZ", "gyroX", "gyroY", "gyroZ", "label"])
                    writer.writerow(
                        [timestamp, f"{accX:.2f}", f"{accY:.2f}", f"{accZ:.2f}", f"{gyroX:.2f}", f"{gyroY:.2f}", f"{gyroZ:.2f}", label]
                    )

                print(
                    # f"accX:{accX:.2f} accY:{accY:.2f} accZ:{accZ:.2f} "
                    # f"gyroX:{gyroX:.2f} gyroY:{gyroY:.2f} gyroZ:{gyroZ:.2f}, "
                    f"stato:{label}"
                )

        listener.stop()

    def stop(self):
        self.can_run.clear()

    def prepare_data_for_inference(self, buffer):
        data_array = np.array(buffer)

        features = data_array[:, :8]

        scaled_features = self.scaler.transform(features)
        return scaled_features

    def perform_inference(self, buffer):
        input_data = self.prepare_data_for_inference(buffer)

        input_tensor = torch.tensor(input_data, dtype=torch.float32).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(input_tensor)
            predicted_class = torch.argmax(output, dim=1).item()
        label_encoder = joblib.load("preprocessing/verso_encoder.pkl")
        predicted_label = label_encoder.inverse_transform([predicted_class])[0]

        return predicted_label
from multiprocessing import Pipe
import time
import random
from itsGesturelstm import ITSGesture 

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def generate_sensor_data():
    """
    Generates one row of synthetic sensor data.
    Each row contains accelerometer (accX, accY, accZ)
    and gyroscope (gyroX, gyroY, gyroZ) values.
    """
    accX = random.uniform(-1.0, 1.0)
    accY = random.uniform(-1.0, 1.0)
    accZ = random.uniform(-1.0, 1.0)
    gyroX = random.uniform(-0.5, 0.5)
    gyroY = random.uniform(-0.5, 0.5)
    gyroZ = random.uniform(-0.5, 0.5)
    return accX, accY, accZ, gyroX, gyroY, gyroZ


if __name__ == "__main__":
    sensor_rx, sensor_tx = Pipe()  
    audio_rx, audio_tx = Pipe()    

    # Instantiate the ITSGesture process
    gesture_process = ITSGesture(sensor_rx, audio_rx)

    # Start the ITSGesture process
    gesture_process.can_run.set()
    gesture_process.start()

    try:
        # Generate and send sensor data to the ITSGesture process in real-time
        for _ in range(200):  # Generate sensor data for ~20 seconds (200 samples at 0.1s intervals)
            sensor_data = generate_sensor_data()  # Generate a row of synthetic data
            sensor_tx.send(sensor_data)          # Send the data to the ITSGesture process
            time.sleep(0.1)                      # Wait 0.1 seconds before sending the next row

    finally:
        # Stop the ITSGesture process
        gesture_process.stop()
        gesture_process.join()

        print("ITSGesture process has stopped.")
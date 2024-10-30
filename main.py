import time
from customTskin import CustomTskin, Hand, OneFingerGesture

if __name__ == "__main__":
    # tskin = CustomTskin(....)
    with CustomTskin("C0:83:43:39:21:57", Hand.RIGHT) as tskin:
        while True:
            if not tskin.connected:
                print("Connecting...")
                time.sleep(0.1)
                continue

            touch = tskin.touch

            if touch and touch.one_finger == OneFingerGesture.SINGLE_TAP:
                print("ascolto.....")
                tskin.select_audio()
                time.sleep(10)
                tskin.select_sensors()
                print("ho finito")

            time.sleep(tskin.TICK)
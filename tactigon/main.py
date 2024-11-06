import time
from customTskin import CustomTskin, Hand, OneFingerGesture
import platform

os_name = platform.system()

if __name__ == "__main__":
    try:
        if os_name == "Darwin":
            with CustomTskin("72AA6234-0670-BF72-83AF-A08864FD3B36", Hand.RIGHT) as tskin:
                while True:
                    if not tskin.connected:
                        print("Connecting...")
                        time.sleep(0.1)
                        continue

                    touch = tskin.touch

                    # if touch and touch.one_finger == OneFingerGesture.SINGLE_TAP:
                    #     print("ascolto.....")
                    #     # tskin.select_audio()
                    #     time.sleep(10)
                    #     tskin.select_sensors()
                    #     print("ho finito")

                    time.sleep(tskin.TICK)
        else:
            with CustomTskin("C0:83:43:39:21:57", Hand.RIGHT) as tskin:
                while True:
                    if not tskin.connected:
                        print("Connecting...")
                        time.sleep(0.1)
                        continue

                    touch = tskin.touch

                    # if touch and touch.one_finger == OneFingerGesture.SINGLE_TAP:
                    #     print("ascolto.....")
                    #     # tskin.select_audio()
                    #     time.sleep(10)
                    #     tskin.select_sensors()
                    #     print("ho finito")

                    time.sleep(tskin.TICK)
    except KeyboardInterrupt:
        print("\nScript interrupted. Exiting gracefully...")
        
        
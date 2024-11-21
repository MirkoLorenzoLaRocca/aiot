import time
from customTskin import CustomTskin, Hand, OneFingerGesture
import platform
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
                           
os_name = platform.system()

if __name__ == "__main__":
    try:
        if os_name == "Darwin":
            with CustomTskin("6682F884-10E7-82A4-7945-0E4E7D405240", Hand.RIGHT) as tskin:
                while True:
                    if not tskin.connected:
                        print("Connecting...")
                        time.sleep(0.01)
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
            with CustomTskin("C0:83:3E:39:21:57 ", Hand.RIGHT) as tskin:
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
        
        
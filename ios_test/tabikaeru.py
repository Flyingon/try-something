import wda
import time
from appium import webdriver
import threading

c = wda.Client()

# class Client(wda.Client):
#     def home_duration(self):
#         return self.http.post('/wda/homescreen')



while True:
    print(c.status())
    s = c.session('jp.co.hit-point.tabikaeru')
    print(c.healthcheck())
    time.sleep(3)
    s.swipe_right()
    s.swipe_right()
    s.tap(286.4, 464.6)
    # t1 = threading.Thread(target=call_siri)
    # t2 = threading.Thread(target=s.tap, args=(219.3, 467.6))
    # t2.start()
    # t1.start()
    break
    # try:
    #     # time.sleep(0.2)
    #     print("Home")
    # except wda.WDAError:
    #     print("Home")


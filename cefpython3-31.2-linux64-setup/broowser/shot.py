from broowser import BrowserInitializer
import sys, time

bi = BrowserInitializer()
page = sys.argv[1]
bi.screenshoot(page, height=640, width=640)
time.sleep(2)
bi.screenshoot(page, height=640, width=640)


from broowser import BrowserInitializer
import sys, time

bi = BrowserInitializer()
page = sys.argv[1]
bi.screenshoot(page, height=3000, width=3000)
time.sleep(2)
bi.screenshoot(page, height=3000, width=3000)


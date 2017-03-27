from broowser import Broowser
import sys, time

try:
    b = Broowser("Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 Nokia5800d-1/60.0.003; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.1.33 Mobile Safari/533.4")
    page = sys.argv[1]
    b.screenshot(page)
    time.sleep(3)
    b.screenshot(page)
except BaseException as e:
    print(e)
    raise e


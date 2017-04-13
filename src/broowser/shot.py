from broowser import Broowser
import sys, time
import StringIO
import io
import Image

dom = StringIO.StringIO()
image = StringIO.StringIO()

nexus = "Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/KRT16H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.105 Mobile Safari/537.36"
nokia = "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 Nokia5800d-1/60.0.003; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.1.33 Mobile Safari/533.4"

try:
    b = Broowser(nexus, stringio=dom, io=image)
    page = sys.argv[1]
    b.screenshot(page)
    time.sleep(5)
    b.screenshot(page)
   # time.sleep(7)
    print("DOM " + dom.getvalue())
    png_image = Image.frombytes(
        "RGBA", (b.width, b.height), image.getvalue(), "raw", "RGBA", 0, 1
    )
    png_image.save("/home/mira/abc.png", "PNG")
    print("koncime")
except BaseException as e:
    print(e)
    raise e


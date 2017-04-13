from broowser import Broowser
import sys, time
import StringIO
import io
import Image

dom = StringIO.StringIO()
image = StringIO.StringIO()

try:
#    b = Broowser("Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 Nokia5800d-1/60.0.003; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.1.33 Mobile Safari/533.4")
    b = Broowser("""Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/KRT16H)
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.105 Mobile
            Safari/537.36 """, stringio=dom, io=image)
    page = sys.argv[1]
    b.screenshot(page)
    time.sleep(3)
    b.screenshot(page)
    print("stringio res {}".format(dom.getvalue()))
    # print("io res {} {}".format(type(image.getvalue()), image.getvalue()))
    real = Image.frombytes(
        "RGBA", (1080, 1920), image.getvalue(), "raw", "RGBA", 0, 1
    )
    real.save("/home/mira/jetu.png", "PNG")
    print("koncime")
    # image.save("/home/mira/mirecek.png", "PNG")
except BaseException as e:
    print(e)
    raise e


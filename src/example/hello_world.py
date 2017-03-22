# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v55.3+.

from cefpython3 import cefpython as cef
import platform
import sys

def get_switches():
   return {
    "enable-blink-features": 'CSSBoxShadow',
    }

def main():
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize({}, get_switches())

   #

    windowInfo = cef.WindowInfo()
    windowInfo.SetAsOffscreen(0)
    browserSettings = {
        "local_storage_disabled": True,
    }
    browser = cef.CreateBrowserSync(windowInfo, browserSettings,
            "http://localhost/transform.html")
    browser.SendFocusEvent(True)
   #

    #cef.CreateBrowserSync(url="http://localhost/box-shadow.html")
    cef.MessageLoop()
    cef.Shutdown()


def check_versions():
    print("[hello_world.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[hello_world.py] Python {ver} {arch}".format(
            ver=platform.python_version(), arch=platform.architecture()[0]))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"


if __name__ == '__main__':
    main()

from cefpython3 import cefpython

import threading, time
import os
import sys

from logging import getLogger
log = getLogger('mirecek')

settings = {
    "log_severity": cefpython.LOGSEVERITY_INFO, # LOGSEVERITY_VERBOSE
    #"log_file": cefpython.GetApplicationPath("debug.log"), # Set to "" to disable.
    "release_dcheck_enabled": True, # Enable only when debugging.
    # This directories must be set on Linux
    "locales_dir_path": cefpython.GetModuleDirectory()+"/locales",
    "resources_dir_path": cefpython.GetModuleDirectory(),
    #"multi_threaded_message_loop": False,
    #"remote_debugging_port": 8080,
    "browser_subprocess_path": "%s/%s" % (
        cefpython.GetModuleDirectory(), "subprocess")
}


class ClientHandler:
    """A client handler is required for the browser to do built in callbacks back into the application."""

    browser = None
    image = None
    width = None
    height = None
    screenshot_fpath = None

    def __init__(self, browser, width, height, screenshot_fpath):
        self.browser = browser
        self.width = width
        self.height = height
        self.screenshot_fpath = screenshot_fpath

    def OnPaint(self, browser, paintElementType, dirtyRects, buffer, width, height):
        print("\nOnPaint")
        self.height = height
        if paintElementType == cefpython.PET_POPUP:
            print("width=%s, height=%s" % (width, height))
        elif paintElementType == cefpython.PET_VIEW:
            self.image = buffer.GetString(mode="rgba", origin="top-left")
            print("\nOnPaint set self.image")
        else:
            print("\nOnPaint __error__")
            raise Exception("Unknown paintElementType: %s" % paintElementType)

    def GetViewRect(self, browser, rect):
        width = self.width
        height = self.height
        rect.append(0)
        rect.append(0)
        rect.append(width)
        rect.append(height)
        print("\nGetViewRect")
        return True

    def GetScreenPoint(self, browser, viewX, viewY, screenCoordinates):
        print("GetScreenPoint()")
        return False

    def OnLoadStart(self, browser, frame):
        print("\nOnLoadStart")
        pass

    def OnLoadEnd(self, browser, frame, httpStatusCode):
        print("HTTP status ", httpStatusCode)
        try:
            from PIL import Image
        except:
            print("PIL library not available, can't save image")
            return
        width = self.width
        height = self.height
        image = Image.frombytes("RGBA", (width, height), self.image, "raw", "RGBA", 0, 1)
        image.save(self.screenshot_fpath, "PNG")
        print("image saved")
        cefpython.QuitMessageLoop()

    def OnLoadError(self, browser, frame, errorCode, errorText, failedURL):
        print("load error", browser, frame, errorCode, errorText, failedURL)


class BindObject(object):

    def __init__(self, browser):
        self.browser = browser

    def method(self, json_obj):
        print(json_obj)


def set_js_bindings(browser):
    jsBindings = cefpython.JavascriptBindings(
            bindToFrames=True,
            bindToPopups=True
    )
    jsBindings.SetObject("window", BindObject(browser))
    browser.SetJavascriptBindings(jsBindings)

cefpython.g_debug = True
cefpython.Initialize(settings)

width=512
height=512
windowInfo = cefpython.WindowInfo()
windowInfo.SetAsOffscreen(0)
browserSettings = {}
browser = cefpython.CreateBrowserSync(windowInfo, browserSettings,
        navigateUrl="http://jakpsatweb.cz/")
#        navigateUrl="http://localhost/index.html")
#        navigateUrl="http://drb.mopa.cz/info")
#        navigateUrl="http:///home/mira/DIPLOMKA/broo-viewer/test_web/remote.html")
#        navigateUrl="http://kosire")
browser.SendFocusEvent(True)
#set_js_bindings(browser)
try:
    os.remove("screenshot.png")
except OSError:
    pass
browser.SetClientHandler(ClientHandler(browser, width, height, "screenshot.png"))
browser.WasResized()
cefpython.MessageLoop()
#cefpython.Shutdown()

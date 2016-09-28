from cefpython3 import cefpython

import threading, time
import os
import sys

settings = {
    "log_severity": cefpython.LOGSEVERITY_INFO, # LOGSEVERITY_VERBOSE
    #"log_file": GetApplicationPath("debug.log"), # Set to "" to disable.
    "release_dcheck_enabled": True, # Enable only when debugging.
    # This directories must be set on Linux
    "locales_dir_path": cefpython.GetModuleDirectory()+"/locales",
    "resources_dir_path": cefpython.GetModuleDirectory(),
    "multi_threaded_message_loop": False,
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
        self.height = height
        if paintElementType == cefpython.PET_POPUP:
            print("width=%s, height=%s" % (width, height))
        elif paintElementType == cefpython.PET_VIEW:
            browser.GetMainFrame().ExecuteJavascript('''document.body.style.background = "#ff00cc";''')
            self.image = buffer.GetString(mode="rgba", origin="top-left")
        else:
            raise Exception("Unknown paintElementType: %s" % paintElementType)

    def GetViewRect(self, browser, rect):
        width = self.width
        #height = self.height
        rect.append(0)
        rect.append(0)
        rect.append(width)
        rect.append(height)
        return True

    def GetScreenPoint(self, browser, viewX, viewY, screenCoordinates):
        print("GetScreenPoint()")
        return False

    def OnLoadEnd(self, browser, frame, httpStatusCode):
        try:
            from PIL import Image
        except:
            print("PIL library not available, can't save image")
            return
        width = self.width
        height = self.height
        image = Image.frombytes("RGBA", (width, height), self.image, "raw", "RGBA", 0, 1)
        image.save(self.screenshot_fpath, "PNG")
        cefpython.QuitMessageLoop()

    def OnLoadError(self, browser, frame, errorCode, errorText, failedURL):
        print("load error", browser, frame, errorCode, errorText, failedURL)

cefpython.g_debug = True
cefpython.Initialize(settings)

width=1024
height=1024
windowInfo = cefpython.WindowInfo()
windowInfo.SetAsOffscreen(0)
browserSettings = {}
browser = cefpython.CreateBrowserSync(windowInfo, browserSettings, navigateUrl="http://google.com")
browser.SendFocusEvent(True)
try:
    os.remove("screenshot.png")
except OSError:
    pass
browser.SetClientHandler(ClientHandler(browser, width, height, "screenshot.png"))
browser.WasResized()
cefpython.MessageLoop()
cefpython.Shutdown()

from cefpython3 import cefpython

import threading, time
import os
import sys
from PIL import Image
import datetime

import logging
logging.basicConfig()
log = logging.getLogger('mirecek')

class BrowserInitializer(object):
    def __init__(self, width=512, height=512, capabilities=None):
        cefpython.g_debug = True
        application_settings = {
            "log_severity": cefpython.LOGSEVERITY_INFO, # LOGSEVERITY_VERBOSE
            #"log_file": cefpython.GetApplicationPath("debug.log"), # Set to "" to disable.
            # "release_dcheck_enabled": True, # Enable only when debugging.
            # This directories must be set on Linux
            "locales_dir_path": cefpython.GetModuleDirectory()+"/locales",
            "resources_dir_path": cefpython.GetModuleDirectory(),
            "pack_loading_disabled": True,
            #"multi_threaded_message_loop": False,
            #"remote_debugging_port": 8080,
            "browser_subprocess_path": "%s/%s" % (
                cefpython.GetModuleDirectory(), "subprocess"),
            # nefunguje"disable_blink_features": "CSSIndependentTransformProperties",
        }
        cli_switches = {
            # "enable-blink-features": 'CSSMotionPath',
            #"enable-blink-features": "CSS3TextDecorations,CSSBackDropFilter",
        }
        cefpython.Initialize(application_settings, cli_switches)

        windowInfo = cefpython.WindowInfo()
        windowInfo.SetAsOffscreen(0)
        browserSettings = {
            "local_storage_disabled": True,
        }
        self.browser = cefpython.CreateBrowserSync(windowInfo, browserSettings,
                "http://localhost/transform.html")
        self.browser.SendFocusEvent(True)
        #set_js_bindings(browser)
        self.client_handler = ClientHandler(
                self.browser, width, height, "screenshot.png"
                )
        self.browser.SetClientHandler(self.client_handler)

        self.bind()

    def bind(self):
        jsBindings = cefpython.JavascriptBindings(
            bindToFrames=True, bindToPopups=True
        )
        jsBindings.SetObject("localStorage", False)
        jsBindings.SetObject("Neexistujici", False)
        # jsBindings.SetObject("python", BindObject(self.browser))
        self.browser.SetJavascriptBindings(jsBindings)
        self.browser.javascriptBindings.Rebind()

    def screenshoot(self, page, width=512, height=512):
        try:
            os.remove("screenshot.png")
        except OSError:
            pass

        self.client_handler.width = width
        self.client_handler.height = height
        self.browser.LoadUrl(page)
        self.browser.SendFocusEvent(True)
        self.browser.WasResized()
        cefpython.MessageLoop()

    def exit(self):
        cefpython.Shutdown()
        sys.exit(0)


class ClientHandler:
    """A client handler is required for the browser to do built in callbacks back into the application."""

    def __init__(self, browser, width, height, screenshot_fpath):
        self.browser = browser
        self.width = width
        self.height = height
        self.screenshot_fpath = screenshot_fpath

    def OnPaint(self, browser, paintElementType, dirtyRects, buffer, width, height):
        log.error("time OnPaint zavolano %s", datetime.datetime.now())
        if paintElementType == cefpython.PET_POPUP:
            pass
        elif paintElementType == cefpython.PET_VIEW:
            self_image = buffer.GetString(mode="rgba", origin="top-left")
            image = Image.frombytes(
                "RGBA", (self.width, self.height), self_image, "raw", "RGBA", 0, 1
            )
            image.save(self.screenshot_fpath, "PNG")
            cefpython.QuitMessageLoop()
        else:
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

#    def GetScreenPoint(self, browser, viewX, viewY, screenCoordinates):
#        print("GetScreenPoint()")
#        return False
#
    def OnLoadStart(self, browser, frame):
        print("LoadStart")
        frame.ExecuteJavascript("delete localStorage;");

    def OnLoadEnd(self, browser, frame, httpStatusCode):
        log.error("time OnLoadEnd zavolano %s", datetime.datetime.now())
        #cefpython.QuitMessageLoop()

#    def OnLoadError(self, browser, frame, errorCode, errorText, failedURL):
#        print("load error", browser, frame, errorCode, errorText, failedURL)


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
    jsBindings.SetObject("python", BindObject(browser))
    browser.SetJavascriptBindings(jsBindings)


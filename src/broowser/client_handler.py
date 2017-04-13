from cefpython3 import cefpython as cef
import threading, time
import os
import sys
from PIL import Image
import datetime

import logging
logging.basicConfig()


log = logging.getLogger(__name__)


class ClientHandler:
    """A client handler is required for the browser to do built in callbacks back into the application."""

    def __init__(self, browser, width, height, screenshot_fpath, io):
        self.browser = browser
        self.width = width
        self.height = height
        self.screenshot_fpath = screenshot_fpath
        self.io = io

    def OnPaint(
            self,
            browser=None,
            dirty_rects=None,
            paint_buffer=None,
            height=None,
            width=None,
            element_type=None, **kwargs):
        print("Paint")
        if element_type == cef.PET_POPUP:
            pass
        elif element_type == cef.PET_VIEW:
            self_image = paint_buffer.GetString(mode="rgba", origin="top-left")
#            image = Image.frombytes(
#                "RGBA", (self.width, self.height), self_image, "raw", "RGBA", 0, 1
#            )
            self.io.write(self_image)
#            image.save(self.screenshot_fpath, "PNG")
            cef.QuitMessageLoop()
        else:
            raise Exception("Unknown paintElementType: %s" % paintElementType)

    def GetViewRect(self, browser, rect_out, *args, **kwargs):
        rect_out.append(0)
        rect_out.append(0)
        rect_out.append(self.width)
        rect_out.append(self.height)
        return True

    def GetScreenPoint(self, browser, view_x, view_y, screen_coordinates_out):
        if screen_coordinates_out:
            return True
        return False

    def OnLoadStart(self, browser, frame):
        print("LoadStart")

    def OnLoadEnd(self, browser, frame, *args, **kwargs):
        print("LoadEnd")
        frame.ExecuteJavascript("python.move(window.document.getRootNode().documentElement.outerHTML)")
        # cef.QuitMessageLoop()


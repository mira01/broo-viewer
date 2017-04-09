# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v55.3+.

from cefpython3 import cefpython as cef
import platform
import sys, os

from client_handler import ClientHandler
from properties_fetcher import PropertiesFetcher

#check_versions()
sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error


def func():
    return "undefined"


class BindObject(object):

    def move(self, whatever):
        print(whatever)


class Broowser(object):

    def application_settings(self):
        return {"user_agent": "CUSTOM UA"}

    def cli_switches(self, user_agent):
        blink_switches = self.pf.get_blink_switches(self.capabilities)
        cli_switches = {"enable-blink-features": blink_switches}
        if not self.pf.get_localStorage(self.capabilities):
            cli_switches['disable-local-storage'] = ""
        return cli_switches

    def browser_settings(self):
        return {}


    def __init__(self, user_agent, display_dimensions=None):
        """
        if display_dimmensions tuple(width, height, dpi) is set
        it will overwrite respective values taken from broo
        """
        self.pf = PropertiesFetcher()
        self.capabilities = self.pf.load_capabilities(user_agent=user_agent)
        if not display_dimensions:
            display_dimensions = self.pf.get_display_dimensions(self.capabilities)
        self.width = int(display_dimensions[0])
        self.height = int(display_dimensions[1])

        print(self.width, self.height, type(self.width), type(self.height))

        cef.Initialize(
            self.application_settings(), self.cli_switches(user_agent)
        )
        windowInfo = cef.WindowInfo()
        windowInfo.SetAsOffscreen(0)

        self.browser = cef.CreateBrowserSync(windowInfo, self.browser_settings())
        self.client_handler = ClientHandler(self.browser, self.width, self.height,
            "screenshot.png"
        )
        self.browser.SetClientHandler(self.client_handler)

        # js binding
        jsBindings = cef.JavascriptBindings(
            bindToFrames=False, bindToPopups=False
        )
        jsBindings.SetObject("python", BindObject())
        self.browser.SetJavascriptBindings(jsBindings)
        self.browser.javascriptBindings.Rebind()
        # end jsbinding

        self.browser.SendFocusEvent(True)

    def screenshot(self, url):

        try:
            os.remove("screenshot.png")
        except OSError:
            pass

        self.client_handler.width = self.width
        self.client_handler.height = self.height
        self.browser.LoadUrl(url)
        self.browser.SendFocusEvent(True)
        self.browser.WasResized()
        cef.MessageLoop()

    def page_down(self):
        self.browser.SendMouseWheelEvent(x=0, y=0, deltaX=0, deltaY=self.height)
        cef.MessageLoop()

    def __del__(self):
        print("called shutdown")
        cef.Shutdown()

    #cef.CreateBrowserSync(url="http://localhost/box-shadow.html")

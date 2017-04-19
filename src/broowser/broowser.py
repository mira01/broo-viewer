from cefpython3 import cefpython as cef
import platform
import sys, os

from client_handler import ClientHandler
from properties_fetcher import PropertiesFetcher

sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error

def func():
    "function for js binding"
    return "undefined"


class BindObject(object):
    "object used to return js values to python"

    def __init__(self, stringio):
        self.stringio = stringio

    def move(self, whatever):
        self.stringio.write(whatever)


class Broowser(object):
    "main object responsible for instantiating cefpython browser obejct"

    def application_settings(self):
        "gets application setting as specified in cefpython Browser class"
        return {"user_agent": self.ua}

    def cli_switches(self, user_agent):
        """returns cli_switches for instantiating cefpython Browser object
        switches depends on capabilities of device specified in user-agent
        """
        blink_switches = self.pf.get_blink_switches(self.capabilities)
        cli_switches = {"enable-blink-features": blink_switches}
        if not self.pf.get_localStorage(self.capabilities):
            cli_switches['disable-local-storage'] = ""
        return cli_switches

    def browser_settings(self):
        "returns browser_settings as specified in cefpython Browser class"
        return {}


    def __init__(self, user_agent, display_dimensions=None, stringio=None,
            io=None):
        """
        if display_dimmensions tuple(width, height, dpi) is set
        it will overwrite respective values taken from broo
        """
        self.ua = user_agent
        self.pf = PropertiesFetcher()
        self.capabilities = self.pf.load_capabilities(user_agent=user_agent)
        if not display_dimensions:
            display_dimensions = self.pf.get_display_dimensions(self.capabilities)
        self.width = int(display_dimensions[0])
        self.height = int(display_dimensions[1])

        cef.Initialize(
            self.application_settings(), self.cli_switches(user_agent)
        )
        windowInfo = cef.WindowInfo()
        windowInfo.SetAsOffscreen(0)

        self.browser = cef.CreateBrowserSync(windowInfo, self.browser_settings())
        self.client_handler = ClientHandler(
                self.browser, self.width, self.height, io
        )
        self.browser.SetClientHandler(self.client_handler)

        # js binding
        jsBindings = cef.JavascriptBindings(
            bindToFrames=False, bindToPopups=False
        )
        jsBindings.SetObject("python", BindObject(stringio))
        self.browser.SetJavascriptBindings(jsBindings)
        self.browser.javascriptBindings.Rebind()
        # end jsbinding

        self.browser.SendFocusEvent(True)

    def screenshot(self, url):
        "takes screenshot of specified url"
        self.client_handler.width = self.width
        self.client_handler.height = self.height
        self.browser.LoadUrl(url)
        self.browser.SendFocusEvent(True)
        self.browser.WasResized()
        cef.MessageLoop()

    def page_down(self):
        "should scroll down the webpage"
        self.browser.SendMouseWheelEvent(x=0, y=0, deltaX=0, deltaY=self.height)
        cef.MessageLoop()

    def __del__(self):
        print("called shutdown")
        cef.Shutdown()

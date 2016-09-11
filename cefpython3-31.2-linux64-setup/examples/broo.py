# trying to implement my own Cef browser

# The official CEF Python binaries come with tcmalloc hook
# disabled. But if you've built custom binaries and kept tcmalloc
# hook enabled, then be aware that in such case it is required
# for the cefpython module to be the very first import in
# python scripts. See Issue 73 in the CEF Python Issue Tracker
# for more details.

import ctypes, os, sys
libcef_so = os.path.join(os.path.dirname(
						os.path.abspath(__file__)), 'libcef.so')
if os.path.exists(libcef_so):
	# Import local module
	types.CDLL(libcef_so, ctypes.RTLD_GLOBAL)
	if 0x02070000 <= sys.hexversion < 0x03000000:
		import cefpython_py27 as cefpython
	else:
		raise Exception("Unsupported python version: %s" % sys.version)
else:
	# Import from package
	from cefpython3 import cefpython


class CefBrowser(object):

	def __init__(self, start_url='http://www.google.com/', **kwargs):
		super(CefBrowser, self).__init__(**kwargs)
		self.start_url = start_url


	def _cef_mes(self, *kwargs):
		'''Get called every frame.
		'''
		cefpython.MessageLoopWork()

	def start_cef(self):
		#configure cef
		settings = {
			"debug": True, # cefpython debug messages in console and in log_file
			"log_severity": cefpython.LOGSEVERITY_VERBOSE,
			"log_file": "debug.log",
			"release_dcheck_enabled": True, # Enable only when debugging.
			# This directories must be set on Linux
			"locales_dir_path": cefpython.GetModuleDirectory()+"/locales",
			"resources_dir_path": cefpython.GetModuleDirectory(),
			"browser_subprocess_path": "%s/%s" % (cefpython.GetModuleDirectory(), "subprocess"),
			"remote_debugging_port": "9222",	
			#  "windowless_rendering_enabled": True,
		}
		switches = {
		# "proxy-server": "socks5://127.0.0.1:8888",
		# "enable-media-stream": "",
		}

		#start idle
		#!Clock.schedule_interval(self._cef_mes, 0)

		#init CEF
		cefpython.Initialize(settings, switches)

		#WindowInfo offscreen flag
		windowInfo = cefpython.WindowInfo()
		windowInfo.SetAsOffscreen(1)

		#Create Broswer and naviagte to empty page <= OnPaint won't get called yet
		browserSettings = {}
		# The render handler callbacks are not yet set, thus an
		# error report will be thrown in the console (when release
		# DCHECKS are enabled), however don't worry, it is harmless.
		# This is happening because calling GetViewRect will return
		# false. That's why it is initially navigating to "about:blank".
		# Later, a real url will be loaded using the LoadUrl() method
		# and the GetViewRect will be called again. This time the render
		# handler callbacks will be available, it will work fine from
		# this point.
		# --
		# Do not use "about:blank" as navigateUrl - this will cause
		# the GoBack() and GoForward() methods to not work.
		self.browser = cefpython.CreateBrowserSync(windowInfo, browserSettings,
						navigateUrl=self.start_url)

		#set focus
		self.browser.SendFocusEvent(True)

		self._client_handler = ClientHandler(self)
		self.browser.SetClientHandler(self._client_handler)
		#!self.set_js_bindings()

		#Call WasResized() => force cef to call GetViewRect() and OnPaint afterwards
		self.browser.WasResized()

		# The browserWidget instance is required in OnLoadingStateChange().
		self.browser.SetUserData("browserWidget", self)
		cefpython.MessageLoop()
		
		
		# Clock.schedule_once(self.change_url, 5)

	def change_url(self, *kwargs):
		# Doing a javascript redirect instead of Navigate()
		# solves the js bindings error. The url here need to
		# be preceded with "http://". Calling StopLoad()
		# might be a good idea before making the js navigation.

		self.browser.StopLoad()
		self.browser.GetMainFrame().ExecuteJavascript(
								"window.location='http://www.youtube.com/'")

		# Do not use Navigate() or GetMainFrame()->LoadURL(),
		# as it causes the js bindings to be removed. There is
		# a bug in CEF, that happens after a call to Navigate().
		# The OnBrowserDestroyed() callback is fired and causes
		# the js bindings to be removed. See this topic for more
		# details:
		# http://www.magpcss.org/ceforum/viewtopic.php?f=6&t=11009

		# OFF:
		# | self.browser.Navigate("http://www.youtube.com/")


class ClientHandler:

	def __init__(self, browserWidget):
		self.browserWidget = browserWidget


cb = CefBrowser()
cb.start_cef()
b = cb.browser		


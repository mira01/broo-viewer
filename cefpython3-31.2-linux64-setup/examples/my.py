from cefpython3 import cefpython
from pprint import pprint

windowInfo = cefpython.WindowInfo()
windowInfo.SetAsOffscreen(1)
windowInfo.SetTransparentPainting(True)

browserSettings = {}
url = "http://www.google.com"

b = cefpython.CreateBrowser(windowInfo,
							    browserSettings={},
								navigateUrl=url)
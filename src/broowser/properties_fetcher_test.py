import requests

KNOWN_CAPABILITIES = {
    "css.wordWrap": "CSSWordWrap",
    "css.wordBreak": "CSSWordBreak",
    "css.backgroundSize": "CSSBackgroundSize",
    "css.borderImage": "CSSBorderImage",
    "css.opacity": "CSSOpacity",
    "css.boxShadow": "CSSBoxShadow",
    "css.textShadow": "CSSTextShadow",
    "css.hyphens": "CSSHyphens",
}


class PropertiesFetcherTest(object):
    "clone of PropertiesFetcher. Used for testing purpose"

    def __init__(self, broo_address=None):
        self.broo_address = "http://drb.mopa.cz/info"

    def load_capabilities(self, user_agent=None):
        return {}

    def get_enabled_capabilities(self, capabilities=None):
        return [
            cp for cp, enabled in capabilities.iteritems()
            if enabled == "1" and cp in KNOWN_CAPABILITIES.iterkeys()
        ]

    def get_display_dimensions(self, capabilities=None):
        return (300, 300, 300)

    def get_blink_switches(self, capabilities=None):
        return ""

    def get_localStorage(self, capabilities=None):
        return False



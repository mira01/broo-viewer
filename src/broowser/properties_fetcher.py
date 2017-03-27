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


class PropertiesFetcher(object):

    def __init__(self, broo_address=None):
        self.broo_address = "http://drb.mopa.cz/info"



    def load_capabilities(self, user_agent=None):
        r = requests.get(
            self.broo_address, headers={'user-agent': user_agent}
        )
        return r.json()['capabilities']

    def get_enabled_capabilities(self, capabilities=None):
        return [
            cp for cp, enabled in capabilities.iteritems()
            if enabled == "1" and cp in KNOWN_CAPABILITIES.iterkeys()
        ]

    def get_display_dimensions(self, capabilities=None):
        return (
            capabilities.get('display.width'),
            capabilities.get('display.height'),
            capabilities.get('display.dpi'),
        )

    def get_blink_switches(self, capabilities=None):
        return ",".join(
            KNOWN_CAPABILITIES[cap] for cap in
            self.get_enabled_capabilities(capabilities)
        )




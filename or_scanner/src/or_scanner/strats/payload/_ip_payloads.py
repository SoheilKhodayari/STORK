from ._base import PayloadStrategy
from ._utils import nip_dash, nip_dot, ip4_oct, ip4_dec, ip4_hex, ip4_dotless_oct, ip4_dotless_dec, ip4_dotless_hex, ip6, ip6_mapped

class ToNipDotPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = nip_dot(target_url)
        return payload

class ToNipDashPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = nip_dash(target_url)
        return payload

class ToIP4OctPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = ip4_oct(target_url)
        return payload

class ToIP4DecPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = ip4_dec(target_url)
        return payload

class ToIP4HexPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = ip4_hex(target_url)
        return payload

class ToIP4DotlessOctPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = ip4_dotless_oct(target_url)
        return payload

class ToIP4DotlessDecPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = ip4_dotless_dec(target_url)
        return payload

class ToIP4DotlessHexPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = ip4_dotless_oct(target_url)
        return payload


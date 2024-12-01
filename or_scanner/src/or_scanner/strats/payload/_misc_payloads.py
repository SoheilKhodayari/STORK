from ._base import PayloadStrategy

class IdentityPayload(PayloadStrategy):

    def generate(self, url):
        target_url = super().generate(url)
        return target_url 

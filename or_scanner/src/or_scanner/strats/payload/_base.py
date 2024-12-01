from abc import ABC, abstractmethod
from ._utils import prepend_uuid_subdomain


class PayloadStrategy(ABC):

    def __init__(self, add_tracking=False, **kwargs):
        self.add_tracking = add_tracking

    @abstractmethod
    def generate(self, url):
        """
        Generate a payload for the redirect target verification_url.
        The original candidate_url is provided for dynamic payload generation.
        """
        if self.add_tracking:
            return prepend_uuid_subdomain(url)
        return url


    def get_name(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.get_name()

import requests
from abc import ABC, abstractmethod
from ..logging import get_logger


class BaseDriver(ABC):

    TIMEOUT_SECS = 30

    def __init__(self, backend_url, data):
        self.logger = get_logger(__name__)
        if not data:
            self.logger.warn("Instantiated driver with no data!")
        try:
            # Verify that the backend is reachable as integrity check
            requests.head(backend_url, verify=False)
        except Exception:
            error_msg = "Cannot reach backend. Aborting..."
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.backend_url = backend_url.rstrip("/")
        self.data = data
        
    @abstractmethod
    def _visit(self):
        # Visit candidate url and wait for element with id matching secret
        return False

    @abstractmethod
    def _oracle(self):
        # Open redirect oracle
        return False


    def execute(self):
        return self._visit()

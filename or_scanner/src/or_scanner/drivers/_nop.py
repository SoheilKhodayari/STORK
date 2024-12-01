from ._base import BaseDriver
from ..logging import get_logger

class NopDriver(BaseDriver):

    def __init__(self, backend_url, data):
        super().__init__(backend_url, data)
        self.logger = get_logger(__name__)

    def visit(self, candidate_url, secret):
        self.logger.info(f"Visiting: {candidate_url}")
        self.logger.info(f"Looking for: {secret}")

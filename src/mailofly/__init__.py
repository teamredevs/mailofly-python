"""Official Python client for the Mailofly REST API."""

from .client import Mailofly
from .errors import MailoflyError

__all__ = ["Mailofly", "MailoflyError"]
__version__ = "0.1.0"

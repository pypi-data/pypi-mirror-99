"""Encryption logic of Bosch thermostat."""
from bosch_thermostat_client.const.ivt import MAGIC_IVT

from .base_encryption import BaseEncryption


class IVTEncryption(BaseEncryption):
    """Encryption class."""

    magic = MAGIC_IVT

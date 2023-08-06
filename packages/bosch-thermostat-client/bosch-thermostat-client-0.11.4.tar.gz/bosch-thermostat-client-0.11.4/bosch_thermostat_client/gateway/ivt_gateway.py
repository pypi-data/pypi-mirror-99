"""Gateway module connecting to Bosch thermostat."""

import logging
import json
from .base_gateway import BaseGateway
from bosch_thermostat_client.const import (
    GATEWAY,
    MODELS,
    EMS,
    SYSTEM_BUS,
    VALUE,
    VALUES,
)
from bosch_thermostat_client.const.ivt import IVT, SYSTEM_INFO, CAN
from bosch_thermostat_client.connectors import connector_ivt_chooser
from bosch_thermostat_client.encryption import IVTEncryption as Encryption
from bosch_thermostat_client.exceptions import DeviceException


_LOGGER = logging.getLogger(__name__)


class IVTGateway(BaseGateway):
    """IVT Gateway"""

    device_type = IVT

    def __init__(
        self, session, session_type, host, access_token, access_key=None, password=None
    ):
        """IVT Gateway constructor

        Args:
            session (loop): loop or websession
            session_type (str): either HTTP or XMPP
            host (str): host IP or hostname for HTTP or serial number for XMPP
            access_key (str): access key to Bosch Gateway
            password (str, optional): Password to Bosch Gateway. Defaults to None.
        """
        self._access_token = access_token.replace("-", "")
        if password:
            access_key = self._access_token
        Connector = connector_ivt_chooser(session_type)
        self._connector = Connector(
            host=host,
            loop=session,
            access_key=self._access_token,
            encryption=Encryption(access_key, password),
        )
        super().__init__(host)

    async def _update_info(self, initial_db):
        """Update gateway info from Bosch device."""
        for name, uri in initial_db.items():
            try:
                response = await self._connector.get(uri)
                if VALUE in response:
                    self._data[GATEWAY][name] = response[VALUE]
                elif name == SYSTEM_INFO:
                    self._data[GATEWAY][SYSTEM_INFO] = response.get(VALUES, [])
            except DeviceException as err:
                _LOGGER.debug("Can't fetch data for update_info %s", err)
                pass

    async def get_device_model(self, _db):
        """Find device model."""
        system_bus = self._data[GATEWAY].get(SYSTEM_BUS)
        model_scheme = _db[MODELS]
        if system_bus == CAN:
            self._bus_type = CAN
            return model_scheme.get(CAN)
        self._bus_type = EMS
        system_info = self._data[GATEWAY].get(SYSTEM_INFO)
        attached_devices = {}
        if system_info:
            for info in system_info:
                _id = info.get("Id", -1)
                model = model_scheme.get(_id)
                if model is not None:
                    _LOGGER.debug("Found supported device %s with id %s", model, _id)
                    attached_devices[_id] = model
            if attached_devices:
                found_model = attached_devices[sorted(attached_devices.keys())[0]]
                _LOGGER.debug("Using model %s as database schema", found_model[VALUE])
                return found_model
        _LOGGER.error(
            "I cannot find supported device. Your devices: %s", json.dumps(system_info)
        )

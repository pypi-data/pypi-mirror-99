"""Helper functions."""

import re
import logging
from datetime import datetime, timedelta
from bosch_thermostat_client.const import (
    ID,
    NAME,
    PATH,
    RESULT,
    TYPE,
    REGULAR,
    URI,
    VALUE,
    MAX_VALUE,
    MIN_VALUE,
    UNITS,
    STATUS,
    TIMESTAMP,
    REFERENCES,
    RECORDINGS,
    WRITABLE,
    INTERVAL,
)
from bosch_thermostat_client.const.ivt import ALLOWED_VALUES, STATE

from .exceptions import DeviceException, EncryptionException

_LOGGER = logging.getLogger(__name__)

HTTP_REGEX = re.compile("http://\\d+\\.\\d+\\.\\d+\\.\\d+/", re.IGNORECASE)


def get_all_intervals():
    yesterday = datetime.today() - timedelta(days=1)
    ytt = yesterday.timetuple()
    yttiso = yesterday.isocalendar()
    return [
        f"{ytt[0]}-{ytt[1]}-{ytt[2]}",
        f"{ytt[0]}-{ytt[1]}",
        f"{ytt[0]}-W{yttiso[1]}",
    ]


async def crawl(url, _list, deep, get, exclude=()):
    """Crawl for Bosch API correct values."""
    try:
        resp = await get(url)
        if (REFERENCES not in resp or deep == 0) and ID in resp:
            if not resp[ID] in exclude:
                _list.append(resp)
        else:
            if REFERENCES in resp:
                for uri in resp[REFERENCES]:
                    if ID in uri and deep > 0:
                        await crawl(uri[ID], _list, deep - 1, get, exclude)
        return _list
    except DeviceException:
        return _list


async def deep_into(url, _list, get):
    """Test for getting references. Used for raw scan."""
    try:
        resp = await get(url)
        new_resp = resp
        if URI in new_resp:
            new_resp[URI] = remove_all_ip_occurs(resp[URI])
        if RECORDINGS in new_resp.get(ID, "") and REFERENCES not in new_resp:
            intervals = get_all_intervals()
            for ivs in intervals:
                try:
                    ivs_resp = await get(f"{url}?{INTERVAL}={ivs}")
                    _list.append(ivs_resp)
                except (DeviceException, EncryptionException):
                    pass
        if ID in new_resp and new_resp[ID] == "/gateway/uuid":
            new_resp[VALUE] = "-1"
            if ALLOWED_VALUES in new_resp:
                new_resp[ALLOWED_VALUES] = ["-1"]
        if "setpointProperty" in new_resp and URI in new_resp["setpointProperty"]:
            new_resp["setpointProperty"][URI] = remove_all_ip_occurs(
                new_resp["setpointProperty"][URI]
            )
        _list.append(resp)
        if REFERENCES in resp:
            for idx, val in enumerate(resp[REFERENCES]):
                val2 = val
                if URI in val2:
                    val2[URI] = remove_all_ip_occurs(val2[URI])
                new_resp[REFERENCES][idx] = val2
                await deep_into(val[ID], _list, get)
    except (DeviceException, EncryptionException):
        pass
    return _list


def remove_all_ip_occurs(data):
    """Change IP to THERMOSTAT string."""
    return HTTP_REGEX.sub("http://THERMOSTAT/", data)


class BoschEntities:
    """Main object to deriver sensors and circuits."""

    def __init__(self, get):
        """
        Initiazlie Bosch entities.

        :param dic requests: { GET: get function, SUBMIT: submit function}
        """
        self._items = []
        self._get = get

    async def retrieve_from_module(self, deep, path, exclude=()):
        """Retrieve all json objects with simple values."""
        return await crawl(path, [], deep, self._get, exclude)

    def get_items(self):
        """Get items."""
        return self._items


class BoschSingleEntity:
    """Object for single sensor/circuit. Don't use it directly."""

    def __init__(self, name, connector, attr_id, path=None):
        """Initialize single entity."""
        self._connector = connector
        self._main_data = {NAME: name, ID: attr_id, PATH: path}
        self._data = {}
        self._update_initialized = False
        self._state = False
        # self._interrupt = False
        self._extra_message = "Waiting to fetch data"

    # def interrupt(self):
    #     self._interrupt = True

    @property
    def connector(self):
        """Retrieve connector."""
        return self._connector

    def process_results(self, result, key=None, return_data=False):
        """Convert multi-level json object to one level object."""
        data = {} if return_data else self._data[key][RESULT]
        updated = False
        if result:
            for res_key in [
                VALUE,
                MIN_VALUE,
                MAX_VALUE,
                ALLOWED_VALUES,
                UNITS,
                STATUS,
                TIMESTAMP,
                REFERENCES,
                WRITABLE,
            ]:
                if res_key in result:
                    if res_key in data and result[res_key] == data[res_key]:
                        continue
                    data[res_key] = result[res_key]
                    self._update_initialized = True
                    updated = True
        if STATE in result:
            for state in result[STATE]:
                for key, item in state.items():
                    if key in data:
                        _LOGGER.error(
                            f"This key already exists! {key}, {data[key]}, {item}. Write to developer!"
                        )
                    data[STATE + "_" + key] = item
        return data if return_data else updated

    @property
    def state_message(self):
        """Get text state of device"""
        return self._extra_message

    @property
    def update_initialized(self):
        """Inform if we successfully invoked update at least one time."""
        return self._update_initialized

    def get_property(self, property_name):
        """Retrieve JSON with all properties: value, min, max, state etc."""
        return self._data.get(property_name, {}).get(RESULT, {})

    def get_value(self, property_name, default_value=None):
        """Retrieve only value from JSON."""
        ref = self.get_property(property_name)
        return ref.get(VALUE, default_value)

    @property
    def get_all_properties(self):
        return self._data.keys()

    @property
    def get_data(self):
        return self._data

    @property
    def attr_id(self):
        """Get ID of the entity."""
        return self._main_data[ID]

    @property
    def name(self):
        """Name of Bosch entity."""
        return self._main_data[NAME]

    @property
    def path(self):
        """Get path of Bosch API which entity is using for data."""
        return self._main_data[PATH]

    async def update(self):
        """Update info about Circuit asynchronously."""
        try:
            for key, item in self._data.items():
                if item[TYPE] == REGULAR:
                    result = await self._connector.get(item[URI])
                    self.process_results(result, key)
            self._state = True
        except DeviceException as err:
            _LOGGER.error(
                f"Can't update data for {self.name}. Trying uri: {item[URI]}. Error message: {err}"
            )
            self._state = False
            self._extra_message = f"Can't update data. Error: {err}"

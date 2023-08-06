"""Logic to converse schedule."""
import logging
from datetime import datetime

from bosch_thermostat_client.const import (
    MODE,
    SETPOINT,
    VALUE,
    SWITCHPROGRAM,
    DAYS_INT,
    CIRCUIT_TYPES,
    ID,
    MAX,
    MIN,
    MAX_VALUE,
    MIN_VALUE,
    ON,
    URI,
    ACTIVE_PROGRAM,
    SWITCHPROGRAM_MODE,
    LEVELS,
    ABSOLUTE,
    REFS,
    DEFAULT_MAX_HC_TEMP,
    DEFAULT_MIN_HC_TEMP,
)

from bosch_thermostat_client.const.ivt import (
    DAYOFWEEK,
    TIME,
    TEMP,
    SETPOINT_PROP,
    SWITCH_POINTS,
    CAN,
)
from .exceptions import DeviceException

_LOGGER = logging.getLogger(__name__)


def sort_switchpoints(dic):
    day = dic[DAYOFWEEK]
    return (DAYS_INT.index(day), dic[TIME])


class Schedule:
    """Scheduler logic."""

    def __init__(
        self,
        connector,
        circuit_type,
        circuit_name,
        current_time,
        bus_type,
        db,
        op_mode,
    ):
        """Initialize schedule handling of Bosch gateway."""
        self._connector = connector
        self._active_program = None
        self._circuit_type = CIRCUIT_TYPES[circuit_type]
        self._circuit_name = circuit_name
        self._setpoints_temp = {}
        self._switch_points = None
        self._active_setpoint = None
        self._active_program_uri = None
        self._time = None
        self._time_retrieve = current_time
        self._bus_type = bus_type
        self._db = db
        self._op_mode = op_mode
        self._switchprogram_mode = LEVELS
        self._schedule_found = False

    async def update_schedule(self, active_program):
        """Update schedule from Bosch gateway."""
        self._active_program = active_program
        self._active_program_uri = self._db[SWITCHPROGRAM].format(
            self._circuit_name, active_program
        )
        if SWITCHPROGRAM_MODE in self._db[REFS]:
            try:
                switch_program_result = await self._connector.get(
                    f"/{self._circuit_type}/{self._circuit_name}/{SWITCHPROGRAM_MODE}"
                )
                self._switchprogram_mode = switch_program_result.get(VALUE, LEVELS)
            except DeviceException:
                pass
        try:
            self._time = await self._time_retrieve()
            result = await self._connector.get(self._active_program_uri)
            await self._parse_schedule(
                result.get(SWITCH_POINTS), result.get(SETPOINT_PROP)
            )
            self._schedule_found = True
        except DeviceException:
            self._schedule_found = False
            _LOGGER.warning(
                "URI for Active Program %s doesn't exists. Maybe we can figure out how to work anyway",
                active_program,
            )
            pass

    async def update_schedule_test(self, result, time):
        """Test function to do. Update schedule from Bosch gateway."""
        self._time = time
        self._switch_points = result.get(SWITCH_POINTS)

    @property
    def setpoints(self):
        """Retrieve json setpoints."""
        return self._setpoints_temp

    @property
    def time(self):
        """Get current time of Gateway."""
        return self._time

    @property
    def active_program(self):
        """Get active program."""
        return self._active_program

    def cache_temp_for_mode(self, temp):
        """Save active program for cache."""
        active_setpoint = self._op_mode.current_mode
        if self._op_mode.is_auto:
            active_setpoint = self.get_temp_in_schedule()[MODE]
        if active_setpoint in self._setpoints_temp:
            self._setpoints_temp[active_setpoint][VALUE] = temp

    async def _get_setpoint_temp(self, setpoint_property, setpoint):
        """Download temp for setpoint."""
        try:
            uri = f"{setpoint_property[ID]}/{setpoint}"
            _LOGGER.debug("Getting setpoint for URI %s", uri)
            result = await self._connector.get(uri)
            if self._bus_type == CAN and result.get(VALUE, 0) == 1:
                uri = f"/{self._circuit_type}/{self._circuit_name}/currentSetpoint"
                result = await self._connector.get(uri)
        except DeviceException as err:
            _LOGGER.debug("Bug %s", err)
            if setpoint == ON and self._bus_type != CAN:
                setpoint = "high"
                result = await self._connector.get(
                    f"{setpoint_property[ID]}/{setpoint}"
                )
            raise DeviceException
        return {
            MODE: setpoint,
            VALUE: result.get(VALUE, 0),
            MAX: result.get(MAX_VALUE, 0),
            MIN: result.get(MIN_VALUE, 0),
            URI: uri,
        }

    async def _parse_schedule(self, switch_points, setpoint_property):
        """Convert Bosch schedule to dict format."""
        for switch in switch_points:
            setpoint = switch[SETPOINT]
            if (
                setpoint not in self._setpoints_temp
                and self._switchprogram_mode == LEVELS
            ):
                self._setpoints_temp[setpoint] = await self._get_setpoint_temp(
                    setpoint_property, setpoint
                )
        self._switch_points = switch_points

    def get_temp_for_current_mode(self):
        """This is working only in manual for RC35 where op_mode == setpoint."""
        cache = {}
        # self._mode_to_setpoint.get(self._active_program, {}).get()
        if self._op_mode.is_manual:
            return self._setpoints_temp.get(self._op_mode.current_mode, {}).get(
                VALUE, -1
            )
        if not self._schedule_found:
            return ACTIVE_PROGRAM
        if self.time:
            cache = self.get_temp_in_schedule()
        return cache.get(TEMP, 0)

    def get_max_temp_for_mode(self, extra_val=False):
        """Get max temp for mode in schedule."""
        return self.get_min_max_for_mode(MAX, extra_val)

    def get_min_temp_for_mode(self, extra_val=False):
        """Get min temp for mode in schedule."""
        val = self.get_min_max_for_mode(MIN, extra_val)
        return val

    def get_min_max_for_mode(self, min_max, extra_val=False):
        cache = {}
        extra_val = extra_val if extra_val else -1 if self._op_mode.is_manual else 0
        if self._op_mode.is_manual:
            return self._setpoints_temp.get(self._op_mode.current_mode, {}).get(
                min_max, extra_val
            )
        if not self._schedule_found:
            return ACTIVE_PROGRAM
        if self.time:
            cache = self.get_temp_in_schedule()
        if (
            min_max == MAX
            and cache.get(VALUE, 0) > cache.get(min_max, 0)
            or cache.get(VALUE, 0) < cache.get(MIN, 0)
        ):
            return extra_val
        return cache.get(min_max, extra_val)

    def get_setpoint_for_current_mode(self):
        """Get setpoints for mode."""
        cache = {}
        if self._op_mode.is_manual:
            return self._setpoints_temp.get(self._op_mode.current_mode, {}).get(
                MODE, -1
            )
        if not self._schedule_found:
            return ACTIVE_PROGRAM
        if self.time:
            cache = self.get_temp_in_schedule()
            if self._bus_type == CAN and cache.get(MODE) == ON:
                return "currentSetpoint"
        return cache.get(MODE)

    def get_uri_setpoint_for_current_mode(self):
        """Get setpoints for mode."""
        cache = {}
        if self._op_mode.is_manual:
            return self._setpoints_temp.get(self._op_mode.current_mode, {}).get(URI, -1)
        if not self._schedule_found:
            return ACTIVE_PROGRAM
        if self.time:
            cache = self.get_temp_in_schedule()
        return cache.get(URI)

    def get_temp_in_schedule(self):
        """Find temp in schedule for current date."""
        if self._time:
            bosch_date = datetime.strptime(self._time, "%Y-%m-%dT%H:%M:%S")
            day_of_week = DAYS_INT[bosch_date.weekday()]
            if self._switch_points:
                switch_points = self._switch_points.copy()
                current_setpoint = {
                    DAYOFWEEK: day_of_week,
                    SETPOINT: "",
                    TIME: self._get_minutes_since_midnight(bosch_date),
                }
                switch_points.append(current_setpoint)
                switch_points.sort(key=sort_switchpoints)
                _prev_setpoint = switch_points[
                    switch_points.index(current_setpoint) - 1
                ][SETPOINT]
                if self._switchprogram_mode == LEVELS:
                    return {
                        MODE: _prev_setpoint,
                        TEMP: self._setpoints_temp[_prev_setpoint][VALUE],
                        MAX: self._setpoints_temp[_prev_setpoint][MAX],
                        MIN: self._setpoints_temp[_prev_setpoint][MIN],
                        URI: self._setpoints_temp[_prev_setpoint][URI],
                    }
                elif self._switchprogram_mode == ABSOLUTE:
                    return {
                        MODE: ABSOLUTE,
                        TEMP: float(_prev_setpoint),
                        MAX: DEFAULT_MAX_HC_TEMP,
                        MIN: DEFAULT_MIN_HC_TEMP,
                        URI: None,
                    }
        return {}

    def _get_minutes_since_midnight(self, date):
        """Retrieve minutes since midnight."""
        return int(
            (
                date - date.replace(hour=0, minute=0, second=0, microsecond=0)
            ).total_seconds()
            / 60.0
        )

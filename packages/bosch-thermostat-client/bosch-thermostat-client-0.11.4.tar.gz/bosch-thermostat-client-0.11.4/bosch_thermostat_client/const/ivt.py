from . import USER_AGENT, CONTENT_TYPE, APP_JSON

MAGIC_IVT = bytearray.fromhex(
    "867845e97c4e29dce522b9a7d3a3e07b152bffadddbed7f5ffd842e9895ad1e4"
)
IVT = "IVT"
HTTP = "HTTP"


""" BOSCH SCHEME """

CONNECTION = "Connection"
TELEHEATER = "TeleHeater"
KEEP_ALIVE = "keep-alive"

HTTP_HEADER = {USER_AGENT: TELEHEATER, CONNECTION: KEEP_ALIVE, CONTENT_TYPE: APP_JSON}

CAN = "CAN"
NSC_ICOM_GATEWAY = "NSC_ICOM_GATEWAY"
RC300_RC200 = "RC300_RC200"


ALLOWED_VALUES = "allowedValues"

READ = "read"
WRITE = "write"
STATE = "state"

CURRENT_SETPOINT = "currentSetpoint"

DAYOFWEEK = "dayOfWeek"
TIME = "time"
TEMP = "temp"
SETPOINT_PROP = "setpointProperty"
SWITCH_POINTS = "switchPoints"
SYSTEM_INFO = "systemInfo"
# SYSTEM_BRAND = "brand"
# SYSTEM_TYPE = "systemType"
INVALID = "invalid"

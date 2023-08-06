import datetime
from enum import Enum

import dateutil.parser

from yalexs.bridge import BridgeDetail, BridgeStatus
from yalexs.device import Device, DeviceDetail
from yalexs.keypad import KeypadDetail

LOCKED_STATUS = ("locked", "kAugLockState_Locked", "kAugLockState_Locking")
UNLOCKED_STATUS = ("unlocked", "kAugLockState_Unlocked", "kAugLockState_Unlocking")
CLOSED_STATUS = ("closed", "kAugLockDoorState_Closed", "kAugDoorState_Closed")
OPEN_STATUS = ("open", "kAugLockDoorState_Open", "kAugDoorState_Open")

LOCK_STATUS_KEY = "status"
DOOR_STATE_KEY = "doorState"


class Lock(Device):
    def __init__(self, device_id, data):
        super().__init__(
            device_id,
            data["LockName"],
            data["HouseID"],
        )
        self._user_type = data["UserType"]

    @property
    def is_operable(self):
        return self._user_type == "superuser"

    def __repr__(self):
        return "Lock(id={}, name={}, house_id={})".format(
            self.device_id, self.device_name, self.house_id
        )


class LockDetail(DeviceDetail):
    def __init__(self, data):
        super().__init__(
            data["LockID"],
            data["LockName"],
            data["HouseID"],
            data["SerialNumber"],
            data["currentFirmwareVersion"],
            data.get("pubsubChannel"),
        )

        if "Bridge" in data:
            self._bridge = BridgeDetail(self.house_id, data["Bridge"])
        else:
            self._bridge = None

        self._doorsense = False
        self._lock_status = LockStatus.UNKNOWN
        self._door_state = LockDoorStatus.UNKNOWN
        self._lock_status_datetime = None
        self._door_state_datetime = None
        self._model = None

        if "LockStatus" in data:
            lock_status = data["LockStatus"]

            self._lock_status = determine_lock_status(lock_status.get(LOCK_STATUS_KEY))
            self._door_state = determine_door_state(lock_status.get(DOOR_STATE_KEY))

            if "dateTime" in lock_status:
                self._lock_status_datetime = dateutil.parser.parse(
                    lock_status["dateTime"]
                )
                self._door_state_datetime = self._lock_status_datetime

            if (
                DOOR_STATE_KEY in lock_status
                and self._door_state != LockDoorStatus.UNKNOWN
            ):
                self._doorsense = True

        if "keypad" in data:
            keypad_name = data["LockName"] + " Keypad"
            self._keypad_detail = KeypadDetail(
                self.house_id, keypad_name, data["keypad"]
            )
        else:
            self._keypad_detail = None

        self._battery_level = int(100 * data["battery"])

        if "skuNumber" in data:
            self._model = data["skuNumber"]
        self._data = data

    @property
    def model(self):
        return self._model

    @property
    def battery_level(self):
        return self._battery_level

    @property
    def keypad(self):
        return self._keypad_detail

    @property
    def bridge(self):
        return self._bridge

    @property
    def bridge_is_online(self):
        if self._bridge is None:
            return False

        # Old style bridge that does not report current status
        # This may have been updated but I do not have a Gen2
        # doorbell to test with yet.
        if self._bridge.status is None and self._bridge.operative:
            return True

        if (
            self._bridge.status is not None
            and self._bridge.status.current == BridgeStatus.ONLINE
        ):
            return True

        return False

    @property
    def doorsense(self):
        return self._doorsense

    @property
    def lock_status(self):
        return self._lock_status

    @lock_status.setter
    def lock_status(self, var):
        """Update the lock status (usually form the activity log)."""
        if var not in LockStatus:
            raise ValueError
        self._lock_status = var

    @property
    def lock_status_datetime(self):
        return self._lock_status_datetime

    @lock_status_datetime.setter
    def lock_status_datetime(self, var):
        """Update the lock status datetime (usually form the activity log)."""
        if not isinstance(var, datetime.date):
            raise ValueError
        self._lock_status_datetime = var

    @property
    def door_state(self):
        return self._door_state

    @door_state.setter
    def door_state(self, var):
        """Update the door state (usually form the activity log)."""
        if var not in LockDoorStatus:
            raise ValueError
        self._door_state = var
        if var != LockDoorStatus.UNKNOWN:
            self._doorsense = True

    @property
    def door_state_datetime(self):
        return self._door_state_datetime

    @door_state_datetime.setter
    def door_state_datetime(self, var):
        """Update the door state datetime (usually form the activity log)."""
        if not isinstance(var, datetime.date):
            raise ValueError
        self._door_state_datetime = var

    def set_online(self, state):
        """Called when the lock comes back online or goes offline."""
        if not self._bridge:
            return
        self._bridge.set_online(state)

    def get_user(self, user_id):
        """Lookup user data by id."""
        return self._data.get("users", {}).get(user_id)


class LockStatus(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    UNKNOWN = "unknown"


class LockDoorStatus(Enum):
    CLOSED = "closed"
    OPEN = "open"
    UNKNOWN = "unknown"


def determine_lock_status(status):
    if status in LOCKED_STATUS:
        return LockStatus.LOCKED
    if status in UNLOCKED_STATUS:
        return LockStatus.UNLOCKED
    return LockStatus.UNKNOWN


def determine_door_state(status):
    if status in CLOSED_STATUS:
        return LockDoorStatus.CLOSED
    if status in OPEN_STATUS:
        return LockDoorStatus.OPEN
    return LockDoorStatus.UNKNOWN


def door_state_to_string(door_status):
    """Returns the normalized value that determine_door_state represents."""
    if door_status == LockDoorStatus.OPEN:
        return "dooropen"
    if door_status == LockDoorStatus.CLOSED:
        return "doorclosed"
    raise ValueError

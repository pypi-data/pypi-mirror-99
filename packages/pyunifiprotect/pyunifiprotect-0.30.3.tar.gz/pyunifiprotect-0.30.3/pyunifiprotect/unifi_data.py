"""Unifi Protect Data."""
from collections import OrderedDict
import datetime
import enum
import logging
import struct
import time
import zlib

WS_HEADER_SIZE = 8
_LOGGER = logging.getLogger(__name__)

DEVICE_MODEL_CAMERA = "camera"
DEVICE_MODEL_LIGHT = "light"

EVENT_SMART_DETECT_ZONE = "smartDetectZone"
EVENT_MOTION = "motion"
EVENT_RING = "ring"
EVENT_DISCONNECT = "disconnect"
EVENT_PROVISION = "provision"

EVENT_LENGTH_PRECISION = 3

TYPE_MOTION_OFF = "off"
TYPE_RECORD_NEVER = "never"

PRIVACY_OFF = [[0, 0], [0, 0], [0, 0], [0, 0]]
PRIVACY_ON = [[0, 0], [1, 0], [1, 1], [0, 1]]
ZONE_NAME = "hass zone"

PROCESSED_EVENT_EMPTY = {
    "event_start": None,
    "event_score": 0,
    "event_thumbnail": None,
    "event_heatmap": None,
    "event_on": False,
    "event_ring_on": False,
    "event_type": None,
    "event_length": 0,
    "event_object": [],
}

MAX_SUPPORTED_CAMERAS = 256
MAX_EVENT_HISTORY_IN_STATE_MACHINE = MAX_SUPPORTED_CAMERAS * 2

LIVE_RING_FROM_WEBSOCKET = -1

CAMERA_KEYS = {
    "state",
    "recordingSettings",
    "ispSettings",
    "ledSettings",
    "upSince",
    "firmwareVersion",
    "featureFlags",
    "hdrMode",
    "videoMode",
    "micVolume",
    "channels",
    "name",
    "type",
    "mac",
    "host",
    "lastMotion",
    "lastRing",
    "isMotionDetected",
    "zoomPosition",
}

LIGHT_KEYS = {
    "isConnected",
    "name",
    "type",
    "upSince",
    "firmwareVersion",
    "mac",
    "host",
    "isPirMotionDetected",
    "lightDeviceSettings",
    "lightModeSettings",
    "firmwareVersion",
    "lastMotion",
    "isLedForceOn",
    "isLightOn",
}

SENSOR_KEYS = {
    "upSince",
    "firmwareVersion",
    "isMotionDetected",
    "isOpened",
    "motionDetectedAt",
    "openStatusChangedAt",
}


@enum.unique
class ProtectWSPayloadFormat(enum.Enum):
    """Websocket Payload formats."""

    JSON = 1
    UTF8String = 2
    NodeBuffer = 3


def decode_ws_frame(frame, position):
    """Decode a unifi updates websocket frame."""
    # The format of the frame is
    # b: packet_type
    # b: payload_format
    # b: deflated
    # b: unknown
    # i: payload_size
    _, payload_format, deflated, _, payload_size = struct.unpack(
        "!bbbbi", frame[position : position + WS_HEADER_SIZE]
    )
    position += WS_HEADER_SIZE
    frame = frame[position : position + payload_size]
    if deflated:
        frame = zlib.decompress(frame)
    position += payload_size
    return frame, ProtectWSPayloadFormat(payload_format), position


def process_light(server_id, light, include_events):
    """Process the light json."""

    # Get if Light is Online
    online = light["state"] == "CONNECTED"
    # Get if Light is On
    is_on = light["isLightOn"]
    # Get Firmware Version
    firmware_version = str(light["firmwareVersion"])
    # Get when the light came online
    upsince = (
        "Offline"
        if light["upSince"] is None
        else datetime.datetime.fromtimestamp(int(light["upSince"]) / 1000).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )
    # Get Light Mode Settings
    lightmodesettings = light.get("lightModeSettings")
    motion_mode = lightmodesettings.get("mode")
    motion_mode_enabled_at = lightmodesettings.get("enableAt")
    # Get Light Device Setting
    device_type = light["modelKey"]
    lightdevicesettings = light.get("lightDeviceSettings")
    brightness = lightdevicesettings.get("ledLevel")
    lux_sensitivity = lightdevicesettings.get("luxSensitivity")
    pir_duration = lightdevicesettings.get("pirDuration")
    pir_sensitivity = lightdevicesettings.get("pirSensitivity")
    status_light = lightdevicesettings.get("isIndicatorEnabled")

    light_update = {
        "name": str(light["name"]),
        "type": device_type,
        "model": str(light["type"]),
        "mac": str(light["mac"]),
        "ip_address": str(light["host"]),
        "firmware_version": firmware_version,
        "motion_mode": motion_mode,
        "motion_mode_enabled_at": motion_mode_enabled_at,
        "up_since": upsince,
        "online": online,
        "is_on": is_on,
        "brightness": brightness,
        "lux_sensitivity": lux_sensitivity,
        "pir_duration": pir_duration,
        "pir_sensitivity": pir_sensitivity,
        "status_light": status_light,
    }

    if server_id is not None:
        light_update["server_id"] = server_id

    if include_events:
        # Get the last time motion occured
        light_update["last_motion"] = (
            None
            if light["lastMotion"] is None
            else datetime.datetime.fromtimestamp(
                int(light["lastMotion"]) / 1000
            ).strftime("%Y-%m-%d %H:%M:%S")
        )
    return light_update


def process_sensor(server_id, sensor, include_events):
    """Process the sensor json."""

    device_type = sensor["modelKey"]
    # Get if Sensor is Online
    online = sensor["state"] == "CONNECTED"
    # Get Firmware Version
    firmware_version = str(sensor["firmwareVersion"])
    # Get when the Sensor came online
    upsince = (
        "Offline"
        if sensor["upSince"] is None
        else datetime.datetime.fromtimestamp(int(sensor["upSince"]) / 1000).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )
    # Get Sensor Status
    stats = sensor.get("stats")
    light_value = stats["light"]["value"]
    humidity_value = stats["humidity"]["value"]
    temperature_value = stats["temperature"]["value"]
    battery_status = sensor["batteryStatus"]["percentage"]

    # Get Sensor Mode Settings
    alarm_enabled = sensor["alarmSettings"]["isEnabled"]
    light_enabled = sensor["lightSettings"]["isEnabled"]
    motion_enabled = sensor["motionSettings"]["isEnabled"]
    temperature_enabled = sensor["temperatureSettings"]["isEnabled"]
    humidity_enabled = sensor["humiditySettings"]["isEnabled"]
    led_enabled = sensor["ledSettings"]["isEnabled"]

    sensor_update = {
        "name": str(sensor["name"]),
        "type": device_type,
        "model": str(sensor["type"]),
        "mac": str(sensor["mac"]),
        "ip_address": str(sensor["host"]),
        "firmware_version": firmware_version,
        "up_since": upsince,
        "online": online,
        "light_value": light_value,
        "humidity_value": humidity_value,
        "temperature_value": temperature_value,
        "battery_status": battery_status,
        "alarm_enabled": alarm_enabled,
        "light_enabled": light_enabled,
        "motion_enabled": motion_enabled,
        "temperature_enabled": temperature_enabled,
        "humidity_enabled": humidity_enabled,
        "led_enabled": led_enabled,
    }

    if server_id is not None:
        sensor_update["server_id"] = server_id

    if include_events:
        # Get the last time motion occured
        sensor_update["last_motion"] = (
            None
            if sensor["motionDetectedAt"] is None
            else datetime.datetime.fromtimestamp(
                int(sensor["motionDetectedAt"]) / 1000
            ).strftime("%Y-%m-%d %H:%M:%S")
        )

        # Get the last time open/close sensor changed
        sensor_update["last_openchange"] = (
            None
            if sensor["openStatusChangedAt"] is None
            else datetime.datetime.fromtimestamp(
                int(sensor["openStatusChangedAt"]) / 1000
            ).strftime("%Y-%m-%d %H:%M:%S")
        )

    return sensor_update


def process_camera(server_id, host, camera, include_events):
    """Process the camera json."""

    # If addtional keys are checked, update CAMERA_KEYS

    # Get if camera is online
    online = camera["state"] == "CONNECTED"
    # Get Recording Mode
    recording_mode = str(camera["recordingSettings"]["mode"])
    # Get Infrared Mode
    ir_mode = str(camera["ispSettings"]["irLedMode"])
    # Get Status Light Setting
    status_light = camera["ledSettings"]["isEnabled"]

    # Get when the camera came online
    upsince = (
        "Offline"
        if camera["upSince"] is None
        else datetime.datetime.fromtimestamp(int(camera["upSince"]) / 1000).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )
    # Check if Regular Camera or Doorbell
    device_type = (
        "camera" if "doorbell" not in str(camera["type"]).lower() else "doorbell"
    )
    # Get Firmware Version
    firmware_version = str(camera["firmwareVersion"])

    # Get High FPS Video Mode
    featureflags = camera.get("featureFlags")
    has_highfps = "highFps" in featureflags.get("videoModes", "")
    video_mode = camera.get("videoMode") or "default"
    # Get HDR Mode
    has_hdr = featureflags.get("hasHdr")
    hdr_mode = camera.get("hdrMode") or False
    # Doorbell Chime
    has_chime = featureflags.get("hasChime")
    chime_enabled = False if camera.get("chimeDuration") == 0 else True
    # Get Microphone Volume
    mic_volume = camera.get("micVolume") or 0
    # Get SmartDetect capabilities
    has_smartdetect = featureflags.get("hasSmartDetect")
    # Get if soroundings are Dark
    is_dark = camera.get("isDark") or False
    # Get Optical Zom capabilities
    has_opticalzoom = featureflags.get("canOpticalZoom")
    zoom_position = str(camera["ispSettings"]["zoomPosition"])
    # Wide Dynamic Range
    wdr = str(camera["ispSettings"]["wdr"])
    # Get Privacy Mode
    privacyzones = camera.get("privacyZones")
    privacy_on = False
    for row in privacyzones:
        if row["name"] == ZONE_NAME:
            privacy_on = row["points"] == PRIVACY_ON
            break

    # Add rtsp streaming url if enabled
    rtsp = None
    channels = camera["channels"]
    for channel in channels:
        if channel["isRtspEnabled"]:
            rtsp = f"rtsp://{host}:7447/{channel['rtspAlias']}"
            break

    camera_update = {
        "name": str(camera["name"]),
        "type": device_type,
        "model": str(camera["type"]),
        "mac": str(camera["mac"]),
        "ip_address": str(camera["host"]),
        "firmware_version": firmware_version,
        "recording_mode": recording_mode,
        "ir_mode": ir_mode,
        "status_light": status_light,
        "rtsp": rtsp,
        "up_since": upsince,
        "online": online,
        "has_highfps": has_highfps,
        "has_hdr": has_hdr,
        "video_mode": video_mode,
        "hdr_mode": hdr_mode,
        "mic_volume": mic_volume,
        "has_smartdetect": has_smartdetect,
        "is_dark": is_dark,
        "privacy_on": privacy_on,
        "has_opticalzoom": has_opticalzoom,
        "zoom_position": zoom_position,
        "wdr": wdr,
        "has_chime": has_chime,
        "chime_enabled": chime_enabled,
    }

    if server_id is not None:
        camera_update["server_id"] = server_id
    if include_events:
        # Get the last time motion occured
        camera_update["last_motion"] = (
            None
            if camera["lastMotion"] is None
            else datetime.datetime.fromtimestamp(
                int(camera["lastMotion"]) / 1000
            ).strftime("%Y-%m-%d %H:%M:%S")
        )
        # Get the last time doorbell was ringing
        camera_update["last_ring"] = (
            None
            if camera.get("lastRing") is None
            else datetime.datetime.fromtimestamp(
                int(camera["lastRing"]) / 1000
            ).strftime("%Y-%m-%d %H:%M:%S")
        )

    return camera_update


def event_from_ws_frames(state_machine, minimum_score, action_json, data_json):
    """Convert a websocket frame to internal format.

    Smart Detect Event Add:
    {'action': 'add', 'newUpdateId': '032615bb-910d-41bf-8710-b04959f24455', 'modelKey': 'event', 'id': '5fb0c89003085203870013d0'}
    {'type': 'smartDetectZone', 'start': 1605421197481, 'score': 98, 'smartDetectTypes': ['person'], 'smartDetectEvents': [], 'camera': '5f9f43f102f7d90387004da5', 'partition': None, 'id': '5fb0c89003085203870013d0', 'modelKey': 'event'}

    Smart Detect Event Update:
    {'action': 'update', 'newUpdateId': '84c74562-bb14-4426-8b92-84ae80d1fb4a', 'modelKey': 'event', 'id': '5fb0c92303b75203870013db'}
    {'end': 1605421366608, 'score': 52}

    Camera Motion Start (event):
    {'action': 'add', 'newUpdateId': '25b1142a-2d0d-4b85-b97e-401b03dd1f0b', 'modelKey': 'event', 'id': '5fb0c90603455203870013d7'}
    {'type': 'motion', 'start': 1605421315759, 'score': 0, 'smartDetectTypes': [], 'smartDetectEvents': [], 'camera': '5e539ed503617003870003ed', 'partition': None, 'id': '5fb0c90603455203870013d7', 'modelKey': 'event'}

    Camera Motion End (event):
    {'action': 'update', 'newUpdateId': 'aa1c159c-c575-443a-9e57-b63ed847549c', 'modelKey': 'event', 'id': '5fb0c90603455203870013d7'}
    {'end': 1605421330342, 'score': 46}

    Camera Ring (event)
    {'action': 'add', 'newUpdateId': 'da36377d-b947-4b05-ba11-c17b0d2703f9', 'modelKey': 'event', 'id': '5fb1964b03b352038700184d'}
    {'type': 'ring', 'start': 1605473867945, 'end': 1605473868945, 'score': 0, 'smartDetectTypes': [], 'smartDetectEvents': [], 'camera': '5f9f43f102f7d90387004da5', 'partition': None, 'id': '5fb1964b03b352038700184d', 'modelKey': 'event'}

    Light Motion (event)
    {'action': 'update', 'newUpdateId': '41fddb04-e79f-4726-945f-0de74294045e', 'modelKey': 'light', 'id': '5fec968501ce7d038700539b'}
    {'isPirMotionDetected': True, 'lastMotion': 1609579367419}
    """

    if action_json["modelKey"] != "event":
        raise ValueError("Model key must be event")

    action = action_json["action"]
    event_id = action_json["id"]

    if action == "add":
        device_id = (
            data_json.get("camera") or data_json.get("light") or data_json.get("sensor")
        )
        if device_id is None:
            return None, None
        state_machine.add(event_id, data_json)
        event = data_json
    elif action == "update":
        event = state_machine.update(event_id, data_json)
        if not event:
            return None, None
        device_id = event.get("camera") or event.get("light") or data_json.get("sensor")
    else:
        raise ValueError("The action must be add or update")

    _LOGGER.debug("Processing event: %s", event)
    processed_event = process_event(event, minimum_score, LIVE_RING_FROM_WEBSOCKET)

    return device_id, processed_event


def sensor_update_from_ws_frames(state_machine, action_json, data_json):
    """Convert a websocket frame to internal format."""

    if action_json["modelKey"] != "sensor":
        raise ValueError("Model key must be sensor")

    sensor_id = action_json["id"]

    if not state_machine.has_device(sensor_id):
        _LOGGER.debug("Skipping non-adopted sensor: %s", data_json)
        return None, None

    sensor = state_machine.update(sensor_id, data_json)

    if data_json.keys().isdisjoint(SENSOR_KEYS):
        _LOGGER.debug("Skipping sensor data: %s", data_json)
        return None, None

    _LOGGER.debug("Processing sensor: %s", sensor)
    processed_sensor = process_light(None, sensor, True)

    return sensor_id, processed_sensor


def light_update_from_ws_frames(state_machine, action_json, data_json):
    """Convert a websocket frame to internal format."""

    if action_json["modelKey"] != "light":
        raise ValueError("Model key must be light")

    light_id = action_json["id"]

    if not state_machine.has_device(light_id):
        _LOGGER.debug("Skipping non-adopted light: %s", data_json)
        return None, None

    light = state_machine.update(light_id, data_json)

    if data_json.keys().isdisjoint(LIGHT_KEYS):
        _LOGGER.debug("Skipping light data: %s", data_json)
        return None, None

    _LOGGER.debug("Processing light: %s", light)
    processed_light = process_light(None, light, True)

    return light_id, processed_light


def camera_update_from_ws_frames(state_machine, host, action_json, data_json):
    """Convert a websocket frame to internal format."""

    if action_json["modelKey"] != "camera":
        raise ValueError("Model key must be camera")

    camera_id = action_json["id"]

    if not state_machine.has_device(camera_id):
        _LOGGER.debug("Skipping non-adopted camera: %s", data_json)
        return None, None

    camera = state_machine.update(camera_id, data_json)

    if data_json.keys().isdisjoint(CAMERA_KEYS):
        _LOGGER.debug("Skipping camera data: %s", data_json)
        return None, None

    _LOGGER.debug("Processing camera: %s", camera)
    processed_camera = process_camera(None, host, camera, True)

    return camera_id, processed_camera


def camera_event_from_ws_frames(state_machine, action_json, data_json):
    """Create processed events from the camera model."""

    if "isMotionDetected" not in data_json and "lastMotion" not in data_json:
        return None

    camera_id = action_json["id"]
    start_time = None
    event_length = 0
    event_on = False

    last_motion = data_json.get("lastMotion")
    is_motion_detected = data_json.get("isMotionDetected")

    if is_motion_detected is None:
        start_time = state_machine.get_motion_detected_time(camera_id)
        event_on = start_time is not None
    else:
        if is_motion_detected:
            event_on = True
            start_time = last_motion
            state_machine.set_motion_detected_time(camera_id, start_time)
        else:
            start_time = state_machine.get_motion_detected_time(camera_id)
            state_machine.set_motion_detected_time(camera_id, None)
            if last_motion is None:
                last_motion = round(time.time() * 1000)

    if start_time is not None and last_motion is not None:
        event_length = round(
            (float(last_motion) - float(start_time)) / 1000, EVENT_LENGTH_PRECISION
        )

    return {
        "event_on": event_on,
        "event_type": "motion",
        "event_start": start_time,
        "event_length": event_length,
        "event_score": 0,
    }


def light_event_from_ws_frames(state_machine, action_json, data_json):
    """Create processed events from the light model."""

    if "isPirMotionDetected" not in data_json and "lastMotion" not in data_json:
        return None

    light_id = action_json["id"]
    start_time = None
    event_length = 0
    event_on = False
    _LOGGER.debug("Processed light event: %s", data_json)

    last_motion = data_json.get("lastMotion")
    is_motion_detected = data_json.get("isPirMotionDetected")

    if is_motion_detected is None:
        start_time = state_machine.get_motion_detected_time(light_id)
        event_on = start_time is not None
    else:
        if is_motion_detected:
            event_on = True
            start_time = last_motion
            state_machine.set_motion_detected_time(light_id, start_time)
        else:
            start_time = state_machine.get_motion_detected_time(light_id)
            state_machine.set_motion_detected_time(light_id, None)
            if last_motion is None:
                last_motion = round(time.time() * 1000)

    if start_time is not None and last_motion is not None:
        event_length = round(
            (float(last_motion) - float(start_time)) / 1000, EVENT_LENGTH_PRECISION
        )

    return {
        "event_on": event_on,
        "event_type": "motion",
        "event_start": start_time,
        "event_length": event_length,
        "event_score": 0,
    }


def sensor_event_from_ws_frames(state_machine, action_json, data_json):
    """Create processed events from the sensor model."""
    # TODO: Add the events that can occur (Motion and Door Open/Close)
    if "isPirMotionDetected" not in data_json and "lastMotion" not in data_json:
        return None

    light_id = action_json["id"]
    start_time = None
    event_length = 0
    event_on = False
    _LOGGER.debug("Processed light event: %s", data_json)

    last_motion = data_json.get("lastMotion")
    is_motion_detected = data_json.get("isPirMotionDetected")

    if is_motion_detected is None:
        start_time = state_machine.get_motion_detected_time(light_id)
        event_on = start_time is not None
    else:
        if is_motion_detected:
            event_on = True
            start_time = last_motion
            state_machine.set_motion_detected_time(light_id, start_time)
        else:
            start_time = state_machine.get_motion_detected_time(light_id)
            state_machine.set_motion_detected_time(light_id, None)
            if last_motion is None:
                last_motion = round(time.time() * 1000)

    if start_time is not None and last_motion is not None:
        event_length = round(
            (float(last_motion) - float(start_time)) / 1000, EVENT_LENGTH_PRECISION
        )

    return {
        "event_on": event_on,
        "event_type": "motion",
        "event_start": start_time,
        "event_length": event_length,
        "event_score": 0,
    }


def process_event(event, minimum_score, ring_interval):
    """Convert an event to our format."""
    start = event.get("start")
    end = event.get("end")
    event_type = event.get("type")
    score = event.get("score")

    event_length = 0
    start_time = None

    if start:
        start_time = _process_timestamp(start)
    if end:
        event_length = round(
            (float(end) / 1000) - (float(start) / 1000), EVENT_LENGTH_PRECISION
        )

    processed_event = {
        "event_on": False,
        "event_ring_on": False,
        "event_type": event_type,
        "event_start": start_time,
        "event_length": event_length,
        "event_score": score,
        "event_object": event.get("smartDetectTypes"),
    }

    if event_type in (EVENT_MOTION, EVENT_SMART_DETECT_ZONE):
        processed_event["last_motion"] = start_time
        if score is not None and int(score) >= minimum_score and not end:
            processed_event["event_on"] = True
    elif event_type == EVENT_RING:
        processed_event["last_ring"] = start_time
        if ring_interval == LIVE_RING_FROM_WEBSOCKET or not end:
            _LOGGER.debug("EVENT: DOORBELL IS RINGING")
            processed_event["event_ring_on"] = True
        elif start >= ring_interval and end >= ring_interval:
            _LOGGER.debug("EVENT: DOORBELL HAS RUNG IN LAST 3 SECONDS!")
            processed_event["event_ring_on"] = True
        else:
            _LOGGER.debug("EVENT: DOORBELL WAS NOT RUNG IN LAST 3 SECONDS")

    thumbail = event.get("thumbnail")
    if thumbail is not None:  # Only update if there is a new Motion Event
        processed_event["event_thumbnail"] = thumbail

    heatmap = event.get("heatmap")
    if heatmap is not None:  # Only update if there is a new Motion Event
        processed_event["event_heatmap"] = heatmap

    return processed_event


def _process_timestamp(time_stamp):
    return datetime.datetime.fromtimestamp(int(time_stamp) / 1000).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


class ProtectDeviceStateMachine:
    """A simple state machine for events."""

    def __init__(self):
        """Init the state machine."""
        self._devices = {}
        self._motion_detected_time = {}

    def has_device(self, device_id):
        """Check to see if a device id is in the state machine."""
        return device_id in self._devices

    def update(self, device_id, new_json):
        """Update an device in the state machine."""
        self._devices.setdefault(device_id, {}).update(new_json)
        return self._devices[device_id]

    def set_motion_detected_time(self, device_id, timestamp):
        """Set device motion start detected time."""
        self._motion_detected_time[device_id] = timestamp

    def get_motion_detected_time(self, device_id):
        """Get device motion start detected time."""
        return self._motion_detected_time.get(device_id)


class ProtectEventStateMachine:
    """A simple state machine for cameras."""

    def __init__(self):
        """Init the state machine."""
        self._events = FixSizeOrderedDict(max_size=MAX_EVENT_HISTORY_IN_STATE_MACHINE)

    def add(self, event_id, event_json):
        """Add an event to the state machine."""
        self._events[event_id] = event_json

    def update(self, event_id, new_event_json):
        """Update an event in the state machine and return the merged event."""
        event_json = self._events.get(event_id)
        if event_json is None:
            return None
        event_json.update(new_event_json)
        return event_json


class FixSizeOrderedDict(OrderedDict):
    """A fixed size ordered dict."""

    def __init__(self, *args, max_size=0, **kwargs):
        """Create the FixSizeOrderedDict."""
        self._max_size = max_size
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        """Set an update up to the max size."""
        OrderedDict.__setitem__(self, key, value)
        if self._max_size > 0:
            if len(self) > self._max_size:
                self.popitem(False)

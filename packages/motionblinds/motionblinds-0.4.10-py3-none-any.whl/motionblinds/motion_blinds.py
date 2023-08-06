"""
This module implements the interface to Motion Blinds.

:copyright: (c) 2020 starkillerOG.
:license: MIT, see LICENSE for more details.
"""


import logging
import socket
import json
import struct
import datetime
import platform
from enum import IntEnum
from Cryptodome.Cipher import AES
from threading import Thread

_LOGGER = logging.getLogger(__name__)

MULTICAST_ADDRESS = '238.0.0.18'
UDP_PORT_SEND = 32100
UDP_PORT_RECEIVE = 32101
SOCKET_BUFSIZE = 1024

DEVICE_TYPES_GATEWAY = ["02000001", "02000002"] # Gateway
DEVICE_TYPE_BLIND = "10000000"                  # Standard Blind
DEVICE_TYPE_TDBU = "10000001"                   # Top Down Bottom Up
DEVICE_TYPE_DR = "10000002"                     # Double Roller


class ParseException(Exception):
    """Exception wrapping any parse errors of a response send by a cover."""


class GatewayStatus(IntEnum):
    """Status of the gateway."""

    Working = 1
    Pairing = 2
    Updating = 3


class BlindType(IntEnum):
    """Blind type matching of the blind using the values provided by the motion-gateway."""

    Unknown = -1
    RollerBlind = 1
    VenetianBlind = 2
    RomanBlind = 3
    HoneycombBlind = 4
    ShangriLaBlind = 5
    RollerShutter = 6
    RollerGate = 7
    Awning = 8
    TopDownBottomUp = 9
    DayNightBlind = 10
    DimmingBlind = 11
    Curtain = 12
    CurtainLeft = 13
    CurtainRight = 14
    DoubleRoller = 17
    Switch = 43


class BlindStatus(IntEnum):
    """Status of the blind."""

    Unknown = -1
    Closing = 0
    Opening = 1
    Stopped = 2
    StatusQuery = 5


class LimitStatus(IntEnum):
    """Limit status of the blind."""

    Unknown = -1
    NoLimit = 0
    TopLimit = 1
    BottomLimit = 2
    Limits = 3
    Limit3 = 4

class MotionCommunication:
    """Communication class for Motion Gateways."""

    def _get_timestamp(self):
        """Get the current time and format according to required Message-ID (Timestamp)."""
        time = datetime.datetime.utcnow()
        time_str = time.strftime("%Y%m%d%H%M%S%f")[:-3]
        
        return time_str

    def _create_mcast_socket(self, interface):
            """Create and bind a socket for communication."""
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            if interface != 'any':
                if platform.system() != "Windows":
                    try:
                        sock.bind((MULTICAST_ADDRESS, UDP_PORT_RECEIVE))
                    except OSError:
                        sock.bind((interface, UDP_PORT_RECEIVE))
                else:
                    sock.bind((interface, UDP_PORT_RECEIVE))

                mreq = socket.inet_aton(MULTICAST_ADDRESS) + socket.inet_aton(interface)
            else:
                if platform.system() != "Windows":
                    try:
                        sock.bind((MULTICAST_ADDRESS, UDP_PORT_RECEIVE))
                    except OSError:
                        sock.bind(('', UDP_PORT_RECEIVE))
                else:
                    sock.bind(('', UDP_PORT_RECEIVE))
                mreq = struct.pack("=4sl", socket.inet_aton(MULTICAST_ADDRESS), socket.INADDR_ANY)

            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            return sock


class MotionDiscovery(MotionCommunication):
    """Multicast UDP discovery of Motion Gateways."""

    def __init__(self, interface='any', discovery_time=10.0):
        self._mcastsocket = None
        self._interface = interface
        self._discovery_time = discovery_time
        
        self._discovered_devices = {}

    def discover(self):
        self._mcastsocket = self._create_mcast_socket(self._interface)
        self._mcastsocket.settimeout(self._discovery_time)
        
        msg = {"msgType":"GetDeviceList", "msgID":self._get_timestamp()}
        
        self._mcastsocket.sendto(bytes(json.dumps(msg), 'utf-8'), (MULTICAST_ADDRESS, UDP_PORT_SEND))
        
        start_time = datetime.datetime.utcnow()
        while True:
            time_delta = datetime.datetime.utcnow() - start_time
            
            if time_delta.total_seconds() > self._discovery_time:
                break

            try:
                data, (ip, _) = self._mcastsocket.recvfrom(SOCKET_BUFSIZE)
                response = json.loads(data)
                
                # check msgType
                msgType = response.get("msgType")
                if msgType != "GetDeviceListAck":
                    if msgType != "Heartbeat":
                        _LOGGER.error(
                            "Response from discovery is not a GetDeviceListAck but '%s'.",
                            msgType,
                        )
                    continue
                
                # check device_type
                device_type = response.get("deviceType")
                if device_type not in DEVICE_TYPES_GATEWAY:
                    _LOGGER.error(
                        "DeviceType %s does not correspond to a gateway from a discovery response.",
                        device_type,
                    )
                    continue
                
                # add to discovered devices
                self._discovered_devices[ip] = response
            except socket.timeout:
                break
        
        self._mcastsocket.close()
        
        if self._discovered_devices == {}:
            _LOGGER.warning("No Motion gateways discovered after %.1f seconds.", self._discovery_time)
        
        return self._discovered_devices

    @property
    def discovered_devices(self):
        """Return the discovered devices."""
        return self._discovered_devices


class MotionMulticast(MotionCommunication):
    """Multicast UDP communication class for a MotionGateway."""

    def __init__(self, interface='any'):
        self._listening = False
        self._mcastsocket = None
        self._thread = None
        self._interface = interface

        self._registered_callbacks = {}

    def _listen_to_msg(self):
        """Listen loop for UDP multicast messages for the Motion Gateway."""
        while self._listening:
            if self._mcastsocket is None:
                continue
            try:
                data, (ip_add, _) = self._mcastsocket.recvfrom(SOCKET_BUFSIZE)
            except socket.timeout:
                continue
            try:
                message = json.loads(data)

                if ip_add not in self._registered_callbacks:
                    _LOGGER.info('Unknown motion gateway ip %s', ip_add)
                    continue

                if message.get("actionResult") is not None:
                    _LOGGER.error("Received actionResult: '%s', on multicast listener from ip '%s'",
                        message.get("actionResult"),
                        ip_add,
                    )

                callback = self._registered_callbacks[ip_add]
                callback(message)

            except Exception as err:
                _LOGGER.error("Cannot process multicast message: '%s'\n%s", data, err)
                continue

        _LOGGER.info('Listener stopped')

    def Register_motion_gateway(self, ip, callback):
        """Register a Motion Gateway to this Multicast listener."""
        if ip in self._registered_callbacks:
            _LOGGER.error("A callback for ip '%s' was already registed, overwriting previous callback", ip)
        self._registered_callbacks[ip] = callback

    def Start_listen(self):
        """Start listening."""
        if self._listening:
            _LOGGER.error('Multicast listener already started, not starting another one.')
            return

        self._listening = True

        if self._mcastsocket is None:
            _LOGGER.info('Creating multicast socket')
            self._mcastsocket = self._create_mcast_socket(self._interface)
            self._mcastsocket.settimeout(2.0)  # ensure you can exit the _listen_to_msg loop
        else:
            _LOGGER.error('Multicast socket was already created.')

        if self._thread is None:
            self._thread = Thread(target=self._listen_to_msg, args=())
            self._thread.daemon = True
            self._thread.start()
        else:
            _LOGGER.error('Multicast thread was already created.')
            self._thread.daemon = True
            self._thread.start()

    def Stop_listen(self):
        """Stop listening."""
        self._listening = False

        if self._thread is not None:
            self._thread.join()

        self._thread = None
        _LOGGER.info('Multicast thread stopped')

        if self._mcastsocket is not None:
            self._mcastsocket.close()
            self._mcastsocket = None


class MotionGateway(MotionCommunication):
    """Main class representing the Motion Gateway."""

    def __init__(
        self,
        ip: str = None,
        key: str = None,
        timeout: float = 3.0,
        mcast_timeout: float = 5.0,
        multicast: MotionMulticast = None,
    ):
        self._ip = ip
        self._key = key
        self._token = None

        self._access_token = None
        self._gateway_mac = None
        self._timeout = timeout
        self._mcast_timeout = mcast_timeout

        self._multicast = multicast
        self._registered_callbacks = {}

        self._device_list = {}
        self._device_type = None
        self._status = None
        self._available = False
        self._N_devices = None
        self._RSSI = None
        self._protocol_version = None

        if self._multicast is not None:
            self._multicast.Register_motion_gateway(ip, self._multicast_callback)


    def __repr__(self):
        return "<MotionGateway ip: %s, mac: %s, protocol: %s, N_devices: %s, status: %s, RSSI: %s dBm>" % (
            self._ip,
            self.mac,
            self.protocol,
            self.N_devices,
            self.status,
            self.RSSI,
        )

    def _get_access_token(self):
        """Calculate the AccessToken from the Key and Token."""
        if self._token is None:
            _LOGGER.error("Token not yet retrieved, use GetDeviceList to obtain it before using _get_access_token.")
            return None
        if self._key is None:
            _LOGGER.error("Key not specified, specify a key when creating the gateway class like MotionGateway(ip = '192.168.1.100', key = 'abcd1234-56ef-78') when using _get_access_token.")
            return None
        
        token_bytes = bytes(self._token, 'utf-8')
        key_bytes = bytes(self._key, 'utf-8')

        cipher = AES.new(key_bytes, AES.MODE_ECB)
        encrypted_bytes = cipher.encrypt(token_bytes)
        self._access_token = encrypted_bytes.hex().upper()
        
        return self._access_token

    def _send(self, message):
        """Send a command to the Motion Gateway."""
        attempt = 1
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(self._timeout)
                
                s.sendto(bytes(json.dumps(message), 'utf-8'), (self._ip, UDP_PORT_SEND))

                data, addr = s.recvfrom(SOCKET_BUFSIZE)
                
                s.close()
                break
            except socket.timeout:
                if attempt >= 3:
                    _LOGGER.error("Timeout of %.1f sec occurred on %i attempts while sending message '%s'", self._timeout, attempt, message)
                    s.close()
                    self._available = False
                    raise
                _LOGGER.debug("Timeout of %.1f sec occurred at %i attempts while sending message '%s', trying again...", self._timeout, attempt, message)
                s.close()
                attempt += 1
        
        response = json.loads(data)
        
        if response.get("actionResult") is not None:
            _LOGGER.error("Received actionResult: '%s', when sending message: '%s'",
                response.get("actionResult"),
                message
            )
        
        return response

    def _read_subdevice(self, mac, device_type):
        """Read the status of a subdevice."""
        msg = {"msgType": "ReadDevice", "mac": mac, "deviceType": device_type, "msgID": self._get_timestamp()}

        return self._send(msg)

    def _write_subdevice(self, mac, device_type, data):
        """Write a command to a subdevice."""
        msg = {"msgType": "WriteDevice", "mac": mac, "deviceType": device_type, "AccessToken": self.access_token, "msgID": self._get_timestamp(), "data": data}

        return self._send(msg)

    def _parse_update_response(self, response):
        """Parse the response to a update of the gateway"""

        # check device_type
        device_type = response.get("deviceType")
        if device_type not in DEVICE_TYPES_GATEWAY:
            _LOGGER.warning(
                "DeviceType %s does not correspond to a gateway in parse update function.",
                device_type,
            )
        
        # update variables
        self._gateway_mac = response["mac"]
        self._device_type = device_type
        self._status = GatewayStatus(response["data"]["currentState"])
        self._N_devices = response["data"]["numberOfDevices"]
        self._RSSI = response["data"]["RSSI"]
        self._available = True

    def _parse_device_list_response(self, response):
        """Parse the response to a device list update of the gateway"""

        # check device_type
        device_type = response.get("deviceType")
        if device_type not in DEVICE_TYPES_GATEWAY:
            _LOGGER.warning(
                "DeviceType %s does not correspond to a gateway in GetDeviceList function.",
                device_type,
            )
        
        # update variables
        self._gateway_mac = response["mac"]
        self._device_type = device_type
        self._protocol_version = response["ProtocolVersion"]
        self._token = response["token"]
        self._available = True
        
        # calculate the acces token
        self._get_access_token()
        
        # add the discovered blinds to the device list.
        for blind in response["data"]:
            blind_type = blind["deviceType"]
            if blind_type not in DEVICE_TYPES_GATEWAY:
                blind_mac = blind["mac"]
                if blind_type in [DEVICE_TYPE_BLIND]:
                    self._device_list[blind_mac] = MotionBlind(gateway = self, mac = blind_mac, device_type = blind_type)
                elif blind_type in [DEVICE_TYPE_DR]:
                    self._device_list[blind_mac] = MotionBlind(gateway = self, mac = blind_mac, device_type = blind_type, max_angle = 90)
                elif blind_type in [DEVICE_TYPE_TDBU]:
                    self._device_list[blind_mac] = MotionTopDownBottomUp(gateway = self, mac = blind_mac, device_type = blind_type)
                else:
                    _LOGGER.warning(
                        "Device with mac '%s' has DeviceType '%s' that does not correspond to a gateway or known blind.",
                        blind_mac,
                        blind_type,
                    )

    def _multicast_callback(self, message):
        """Process a multicast push message to update data."""
        msgType = message.get("msgType")
        if msgType == "Report":
            mac = message.get("mac")
            if mac not in self.device_list:
                _LOGGER.warning("Multicast push with mac '%s' not in device_list, message: '%s'", mac, message)
                return
            self.device_list[mac]._multicast_callback(message)
        elif msgType == "Heartbeat":
            mac = message.get("mac")
            if mac != self._gateway_mac:
                _LOGGER.warning("Multicast Heartbeat with mac '%s' does not agree with gateway mac '%s', message: '%s'", mac, self._gateway_mac, message)
                return
            self._parse_update_response(message)
            for callback in self._registered_callbacks.values():
                callback()
        elif msgType == "GetDeviceListAck":
            if mac != self._gateway_mac:
                _LOGGER.warning("Multicast GetDeviceListAck with mac '%s' does not agree with gateway mac '%s', message: '%s'", mac, self._gateway_mac, message)
                return
            self._parse_device_list_response(message)
            for callback in self._registered_callbacks.values():
                callback()
        else:
            _LOGGER.warning("Unknown msgType '%s' received from multicast push with message: '%s'", msgType, message)
            return

    def GetDeviceList(self):
        """Get the device list from the Motion Gateway."""
        msg = {"msgType":"GetDeviceList", "msgID":self._get_timestamp()}

        try:
            response = self._send(msg)
        except socket.timeout:
            for blind in self.device_list.values():
                blind._available = False
            raise
        
        # check msgType
        msgType = response.get("msgType")
        if msgType != "GetDeviceListAck":
            _LOGGER.error(
                "Response to GetDeviceList is not a GetDeviceListAck but '%s'.",
                msgType,
            )
            return
        
        # parse response
        self._parse_device_list_response(response)

        return self._device_list

    def Update(self):
        """Get the status of the Motion Gateway."""
        if self._gateway_mac is None or self._device_type is None:
            _LOGGER.debug("gateway mac or device_type not yet retrieved, first executing GetDeviceList to obtain it before continuing with Update.")
            self.GetDeviceList()
        
        msg = {"msgType":"ReadDevice", "mac": self.mac, "deviceType": self.device_type, "msgID":self._get_timestamp()}

        try:
            response = self._send(msg)
        except socket.timeout:
            for blind in self.device_list.values():
                blind._available = False
            raise
        
        # check msgType
        msgType = response.get("msgType")
        if msgType != "ReadDeviceAck":
            _LOGGER.error(
                "Response to Update is not a ReadDeviceAck but '%s'.",
                msgType,
            )
            return

        # parse response
        self._parse_update_response(response)

    def Register_callback(self, id, callback):
        """Register a external callback function for updates of the gateway."""
        if id in self._registered_callbacks:
            _LOGGER.error("A callback with id '%s' was already registed, overwriting previous callback", id)
        self._registered_callbacks[id] = callback

    def Remove_callback(self, id):
        """Remove a external callback using its id."""
        self._registered_callbacks.pop(id)

    def Clear_callbacks(self):
        """Remove all external registered callbacks for updates of the gateway."""
        self._registered_callbacks.clear()

    @property
    def available(self):
        """Return if the blind is available."""
        return self._available

    @property
    def status(self):
        """Return gateway status: from GatewayStatus enum."""
        if self._status is not None:
            return self._status.name

        return self._status

    @property
    def N_devices(self):
        """Return the number of connected child devices."""
        return self._N_devices

    @property
    def RSSI(self):
        """Return the Wi-Fi connection strength of the gateway in dBm."""
        return self._RSSI

    @property
    def token(self):
        """Return the Token."""
        return self._token

    @property
    def access_token(self):
        """Return the AccessToken."""
        if self._access_token is None:
            if self._token is None:
                _LOGGER.error("Token not yet retrieved, use GetDeviceList to obtain it before using the access_token.")
                return None
            if self._key is None:
                _LOGGER.error("Key not specified, specify a key when creating the gateway class like MotionGateway(ip = '192.168.1.100', key = 'abcd1234-56ef-78') when using the access_token.")
                return None
            # calculate the acces token
            self._get_access_token()
        
        return self._access_token

    @property
    def mac(self):
        """Return the mac address of the gateway."""
        if self._gateway_mac is None:
            _LOGGER.error("gateway mac not yet retrieved, use GetDeviceList to obtain it before using the mac.")
            return None
        
        return self._gateway_mac

    @property
    def device_type(self):
        """Return the device type of the gateway."""
        if self._device_type is None:
            _LOGGER.error("gateway device_type not yet retrieved, use GetDeviceList to obtain it before using the device_type.")
            return None

        return self._device_type

    @property
    def protocol(self):
        """Return the protocol version of the gateway."""
        return self._protocol_version

    @property
    def device_list(self):
        """
        Return a dict containing all blinds connected to the gateway.
        
        The keys in the dict are the mac adresses of the blinds.
        """
        return self._device_list

class MotionBlind:
    """Sub class representing a blind connected to the Motion Gateway."""

    QUERY_DATA = {"operation": 5}

    def __init__(
        self,
        gateway: MotionGateway = None,
        mac: str = None,
        device_type: str = None,
        max_angle: int = 180,
    ):
        self._gateway = gateway
        self._mac = mac
        self._device_type = device_type
        self._blind_type = None
        self._max_angle = max_angle
        
        self._registered_callbacks = {}
        self._last_status_report = datetime.datetime.utcnow()
        
        self._status = None
        self._available = False
        self._limit_status = None
        self._position = None
        self._angle = None
        self._battery_voltage = None
        self._battery_level = None
        self._RSSI = None

    def __repr__(self):
        return "<MotionBlind mac: %s, type: %s, status: %s, position: %s %%, angle: %s, limit: %s, battery: %s %%, %s V, RSSI: %s dBm>" % (
            self.mac,
            self.blind_type,
            self.status,
            self.position,
            self.angle,
            self.limit_status,
            self.battery_level,
            self.battery_voltage,
            self.RSSI,
        )

    def _write(self, data):
        """Write a command to control the blind."""
        
        response = self._gateway._write_subdevice(self.mac, self._device_type, data)
        
        # check msgType
        msgType = response.get("msgType")
        if msgType != "WriteDeviceAck":
            _LOGGER.error(
                "Response to Write is not a WriteDeviceAck but '%s'.",
                msgType,
            )

        return response

    def _wait_on_mcast_report(self, mcast_socket):
        """Wait untill a status report is received from the multicast socket"""
        while True:
            try:
                mcast_data, (ip, _) = mcast_socket.recvfrom(SOCKET_BUFSIZE)
                mcast_response = json.loads(mcast_data)

                # check ip
                if ip != self._gateway._ip:
                    _LOGGER.debug("Received multicast push from a diffrent gateway with ip '%s', in Update function",
                        ip
                    )
                    continue

                # check mac
                if mcast_response.get("mac") != self.mac:
                    _LOGGER.debug("Received multicast push regarding a diffrent blind with mac '%s', in Update function",
                        mcast_response.get("mac")
                    )
                    continue

                # check actionResult
                if mcast_response.get("actionResult") is not None:
                    _LOGGER.error("Received actionResult: '%s' from multicast push within Update function",
                        mcast_response.get("actionResult")
                    )
                    continue

                # check msgType
                msgType = mcast_response.get("msgType")
                if msgType != "Report":
                    _LOGGER.debug(
                        "Response to update on multicast is not a Report but '%s'.",
                        msgType,
                    )
                    continue

                # done
                mcast_socket.close()
                return mcast_response
            except socket.timeout:
                mcast_socket.close()
                raise

    def _calculate_battery_level(self, voltage):
        if voltage > 0.0 and voltage <= 9.4:
            # 2 cel battery pack (8.4V)
            return round((voltage-6.2)*100/(8.4-6.2), 0)

        if voltage > 9.4 and voltage <= 13.6:
            # 3 cel battery pack (12.6V)
            return round((voltage-10.4)*100/(12.6-10.4), 0)

        if voltage > 13.6:
            # 4 cel battery pack (16.8V)
            return round((voltage-14.6)*100/(16.8-14.6), 0)

        return 0.0

    def _parse_response_common(self, response):
        """Parse the common part of a response form the blind."""

        # check device_type
        device_type = response.get("deviceType")
        if device_type not in [DEVICE_TYPE_BLIND, DEVICE_TYPE_TDBU, DEVICE_TYPE_DR]:
            _LOGGER.warning(
                "Device with mac '%s' has DeviceType '%s' that does not correspond to a known blind in Update function.",
                self.mac,
                device_type,
            )
        
        # update variables
        self._mac = response["mac"]
        self._device_type = response["deviceType"]
        try:
            self._blind_type = BlindType(response["data"]["type"])
        except ValueError:
            if self._blind_type != BlindType.Unknown:
                _LOGGER.error(
                    "Device with mac '%s' has blind_type '%s' that is not yet known, please submit an issue at https://github.com/starkillerOG/motion-blinds/issues.",
                    self.mac,
                    response["data"]["type"],
                )
            self._blind_type = BlindType.Unknown

        # Check max angle
        if self._blind_type in [BlindType.ShangriLaBlind]:
            self._max_angle = 90

        self._RSSI = response["data"]["RSSI"]
        self._available = True

    def _parse_response(self, response):
        """Parse a response form the blind."""
        try:
            # handle the part that is common among all blinds
            self._parse_response_common(response)
            
            # handle specific properties
            try:
                self._status = BlindStatus(response["data"]["operation"])
            except ValueError:
                if self._status != BlindStatus.Unknown:
                    _LOGGER.error(
                        "Device with mac '%s' has status '%s' that is not yet known, please submit an issue at https://github.com/starkillerOG/motion-blinds/issues.",
                        self.mac,
                        response["data"]["operation"],
                    )
                self._status = BlindStatus.Unknown
            try:
                self._limit_status = LimitStatus(response["data"]["currentState"])
            except ValueError:
                if self._limit_status != LimitStatus.Unknown:
                    _LOGGER.error(
                        "Device with mac '%s' has limit_status '%s' that is not yet known, please submit an issue at https://github.com/starkillerOG/motion-blinds/issues.",
                        self.mac,
                        response["data"]["currentState"],
                    )
                self._status = LimitStatus.Unknown
            self._position = response["data"]["currentPosition"]
            self._angle = response["data"]["currentAngle"]*(180.0/self._max_angle)
            self._battery_voltage = response["data"]["batteryLevel"]/100.0

            self._battery_level = self._calculate_battery_level(self._battery_voltage)
        except KeyError as ex:
            _LOGGER.error(
                "Device with mac '%s' send an response with unexpected data, please submit an issue at https://github.com/starkillerOG/motion-blinds/issues. Response: '%s', Exception: '%s'",
                self.mac,
                response,
                ex,
            )
            raise ParseException("Got an exception while parsing response") from ex

    def _multicast_callback(self, message):
        """Process a multicast push message to update data."""
        self._parse_response(message)

        if message.get("msgType") == "Report":
            self._last_status_report = datetime.datetime.utcnow()

        for callback in self._registered_callbacks.values():
            callback()

    def Update_from_cache(self):
        """
        Get the status of the blind from the cache of the Motion Gateway

        No 433MHz radio communication with the blind takes place.
        """
        response = self._gateway._read_subdevice(self.mac, self._device_type)
        
        # check msgType
        msgType = response.get("msgType")
        if msgType != "ReadDeviceAck":
            _LOGGER.error(
                "Response to Update is not a ReadDeviceAck but '%s'.",
                msgType,
            )
            return
        
        self._parse_response(response)

    def Update(self):
        """
        Get the status of the blind from the blind through the Motion Gateway

        This will send a query to the blind to retrieve its status.
        The Gateway will imediatly respond with the status of the blind from cache (old status).
        As soon as the blind responds over 433MHz radio, a multicast push will be sent out by the gateway with the new status.
        """
        attempt = 1
        while True:
            if self._gateway._multicast is None:
                mcast = self._gateway._create_mcast_socket('any')
                mcast.settimeout(self._gateway._mcast_timeout)
            else:
                start = datetime.datetime.utcnow()
            
            # send update request
            response = self._write(self.QUERY_DATA)
            
            # parse status from cache
            self._parse_response(response)
            
            # wait on multicast push for new status
            try:
                if self._gateway._multicast is None:
                    mcast_response = self._wait_on_mcast_report(mcast)

                    self._parse_response(mcast_response)
                    break;
                else:
                    while True:
                        time_diff = self._last_status_report - start
                        if time_diff.total_seconds() > 0:
                            break
                        time_past = datetime.datetime.utcnow() - start
                        if time_past.total_seconds() > self._gateway._mcast_timeout:
                            raise socket.timeout
                    break
            except socket.timeout:
                if attempt >= 5:
                    _LOGGER.error("Timeout of %.1f sec occurred on %i attempts while waiting on multicast push from update request, communication between gateway and blind might be bad.", self._gateway._mcast_timeout, attempt)
                    self._available = False
                    raise
                _LOGGER.debug("Timeout of %.1f sec occurred at %i attempts while waiting on multicast push from update request, trying again...", self._gateway._mcast_timeout, attempt)
                attempt += 1

    def Stop(self):
        """Stop the motion of the blind."""
        data = {"operation": 2}

        response = self._write(data)
        
        self._parse_response(response)

    def Open(self):
        """Open the blind/move the blind up."""
        data = {"operation": 1}

        response = self._write(data)
        
        self._parse_response(response)

    def Close(self):
        """Close the blind/move the blind down."""
        data = {"operation": 0}

        response = self._write(data)
        
        self._parse_response(response)

    def Set_position(self, position):
        """
        Set the position of the blind.
        
        position is in %, so 0-100
        0 = open
        100 = closed
        """
        data = {"targetPosition": position}

        response = self._write(data)
        
        self._parse_response(response)

    def Set_angle(self, angle):
        """
        Set the angle/rotation of the blind.
        
        angle is in degrees, so 0-180
        """
        target_angle = round(angle*self._max_angle/180.0, 0)
        
        data = {"targetAngle": target_angle}

        response = self._write(data)
        
        self._parse_response(response)

    def Register_callback(self, id, callback):
        """Register a external callback function for updates of this blind."""
        if id in self._registered_callbacks:
            _LOGGER.error("A callback with id '%s' was already registed, overwriting previous callback", id)
        self._registered_callbacks[id] = callback

    def Remove_callback(self, id):
        """Remove a external callback using its id."""
        self._registered_callbacks.pop(id)

    def Clear_callbacks(self):
        """Remove all external registered callbacks for updates of this blind."""
        self._registered_callbacks.clear()

    @property
    def device_type(self):
        """Return the device type of the blind."""
        if self._device_type is None:
            _LOGGER.error("blind device_type not yet retrieved, use Update to obtain it before using the device_type.")
            return None

        return self._device_type

    @property
    def blind_type(self):
        """Return the type of the blind from BlindType enum."""
        if self._blind_type is not None:
            return self._blind_type.name

        return self._blind_type

    @property
    def type(self):
        """Return the type of the blind as a BlindType enum."""
        return self._blind_type

    @property
    def mac(self):
        """Return the mac address of the blind."""
        return self._mac

    @property
    def available(self):
        """Return if the blind is available."""
        return self._available

    @property
    def status(self):
        """Return the current status of the blind from BlindStatus enum."""
        if self._status is not None:
            return self._status.name

        return self._status

    @property
    def limit_status(self):
        """Return the current status of the limit detection of the blind from LimitStatus enum."""
        if self._limit_status is not None:
            return self._limit_status.name

        return self._limit_status

    @property
    def position(self):
        """Return the current position of the blind in % (0-100)."""
        return self._position

    @property
    def angle(self):
        """Return the current angle of the blind 0-180."""
        return self._angle

    @property
    def battery_voltage(self):
        """Return the current battery voltage of the blind in V."""
        return self._battery_voltage

    @property
    def battery_level(self):
        """Return the current battery level of the blind in %."""
        return self._battery_level

    @property
    def RSSI(self):
        """Return the radio connection strength of the blind to the gateway in dBm."""
        return self._RSSI

class MotionTopDownBottomUp(MotionBlind):
    """Sub class representing a Top Down Bottom Up blind connected to the Motion Gateway."""

    QUERY_DATA = {"operation_T": 5, "operation_B": 5}

    def __repr__(self):
        return "<MotionBlind mac: %s, type: %s, status: %s, position: %s %%, scaled_position: %s %%, width: %s %%, limit: %s, battery: %s %%, %s V, RSSI: %s dBm>" % (
            self.mac,
            self.blind_type,
            self.status,
            self.position,
            self.scaled_position,
            self.width,
            self.limit_status,
            self.battery_level,
            self.battery_voltage,
            self.RSSI,
        )

    def _parse_response(self, response):
        """Parse a response form the blind."""
        try:
            # handle the part that is common among all blinds
            self._parse_response_common(response)
            
            # handle specific properties
            self._status = {"T": BlindStatus(response["data"]["operation_T"]), "B": BlindStatus(response["data"]["operation_B"])}
            self._limit_status = {"T": LimitStatus(response["data"]["currentState_T"]), "B": LimitStatus(response["data"]["currentState_B"])}
            pos_T = response["data"]["currentPosition_T"]
            pos_B = response["data"]["currentPosition_B"]
            pos_C = (pos_T + pos_B)/2.0
            self._position = {"T": pos_T, "B": pos_B, "C": pos_C}
            self._angle = None
            self._battery_voltage = {"T": response["data"]["batteryLevel_T"]/100.0, "B": response["data"]["batteryLevel_B"]/100.0}

            self._battery_level = {"T": self._calculate_battery_level(self._battery_voltage["T"]), "B": self._calculate_battery_level(self._battery_voltage["B"])}
        except KeyError as ex:
            _LOGGER.error(
                "Device with mac '%s' send an response with unexpected data, please submit an issue at https://github.com/starkillerOG/motion-blinds/issues. Response: '%s', Exception: '%s'",
                self.mac,
                response,
                ex,
            )
            raise ParseException("Got an exception while parsing response") from ex

    def Stop(self, motor: str = "B"):
        """Stop the motion of the blind."""
        if motor == "B":
            data = {"operation_B": 2}
        elif motor == "T":
            data = {"operation_T": 2}
        elif motor == "C":
            data = {"operation_B": 2, "operation_T": 2}
        else:
            _LOGGER.error('Please specify which motor to control "T" (top), "B" (bottom) or "C" (combined)')
            return

        response = self._write(data)
        
        self._parse_response(response)

    def Open(self, motor: str = "B"):
        """Open the blind/move the blind up."""
        if motor == "B":
            data = {"operation_B": 1}
        elif motor == "T":
            data = {"operation_T": 1}
        elif motor == "C":
            data = {"operation_B": 1, "operation_T": 1}
        else:
            _LOGGER.error('Please specify which motor to control "T" (top), "B" (bottom) or "C" (combined)')
            return

        response = self._write(data)
        
        self._parse_response(response)

    def Close(self, motor: str = "B"):
        """Close the blind/move the blind down."""
        if motor == "B":
            data = {"operation_B": 0}
        elif motor == "T":
            data = {"operation_T": 0}
        elif motor == "C":
            data = {"operation_B": 0, "operation_T": 1}
        else:
            _LOGGER.error('Please specify which motor to control "T" (top), "B" (bottom) or "C" (combined)')
            return

        response = self._write(data)
        
        self._parse_response(response)

    def Set_position(self, position, motor: str = "B", width: int = None):
        """
        Set the position of the blind.
        
        position is in %, so 0-100
        0 = open
        100 = closed
        """
        if width is None:
            width = self.width

        if motor == "B":
            if position >= self._position["T"]:
                data = {"targetPosition_B": position}
            else:
                _LOGGER.error('Error setting position, the bottom of the TDBU blind can not go above the top of the TDBU blind')
                return
        elif motor == "T":
            if position <= self._position["B"]: 
                data = {"targetPosition_T": position}
            else:
                _LOGGER.error('Error setting position, the top of the TDBU blind can not go below the bottom of the TDBU blind')
                return
        elif motor == "C":
            if position >= width/2.0 and position <= (100 - width/2.0): 
                data = {"targetPosition_T": position-width/2.0, "targetPosition_B": position+width/2.0}
            else:
                _LOGGER.error('Error setting position, the combined TDBU blind cannot reach position %.1f, because including the width of %.1f, it would exceed its limits', position, width)
                return
        else:
            _LOGGER.error('Please specify which motor to control "T" (top), "B" (bottom) or "C" (combined)')
            return

        response = self._write(data)
        
        self._parse_response(response)

    def Set_scaled_position(self, scaled_position, motor: str = "B"):
        """
        Set the scaled position of the blind.
        
        scaled_position is in %, so 0-100
        for top blind:
            0 = open
            100 = at position of bottom blind
        for bottom blind:
            0 = at position of the top blind
            100 = closed
        """
        if motor == "B":
            pos_bottom = self._position["T"] + (100.0 - self._position["T"])*scaled_position/100.0
            return self.Set_position(pos_bottom, motor)
        elif motor == "T":
            pos_top = scaled_position*self._position["B"]/100.0
            return self.Set_position(pos_top, motor)
        elif motor == "C":
            pos_combined = self.width/2.0 + scaled_position*(100.0 - self.width)/100.0
            return self.Set_position(pos_combined, motor)
        else:
            _LOGGER.error('Please specify which motor to control "T" (top) or "B" (bottom)')
            return

    def Set_angle(self, angle, motor: str = "B"):
        """
        Set the angle/rotation of the blind.
        
        angle is in degrees, so 0-180
        """
        target_angle = round(angle*self._max_angle/180.0, 0)

        if motor == "B":
            data = {"targetAngle_B": target_angle}
        elif motor == "T":
            data = {"targetAngle_T": target_angle}
        elif motor == "C":
            data = {"targetAngle_B": target_angle, "targetAngle_T": target_angle}
        else:
            _LOGGER.error('Please specify which motor to control "T" (top), "B" (bottom) or "C" (combined)')
            return

        response = self._write(data)
        
        self._parse_response(response)

    @property
    def scaled_position(self):
        """
        Return the current scaled position of the blind in % (0-100).

        For the Top this is the position from the top to the bottom blind
        For the Bottom this is the postion from the top blind to the bottom
        """
        if self._position["B"] > 0:
            pos_top = round(self._position["T"]*100.0/self._position["B"], 1)
        else:
            pos_top = 0

        if self._position["T"] < 100:
            pos_bottom = round((self._position["B"] - self._position["T"])*100.0/(100.0 - self._position["T"]), 1)
        else:
            pos_bottom = 100

        if self.width < 100:
            pos_combined = round((self._position["C"] - self.width/2.0)*100.0/(100.0 - self.width), 1)
        else:
            pos_combined = 100

        return {"T": pos_top, "B": pos_bottom, "C": pos_combined}

    @property
    def width(self):
        """Return the current width of the closed surface in % (0-100)."""
        return self._position["B"] - self._position["T"]

    @property
    def status(self):
        """Return the current status of the blind from BlindStatus enum."""
        if self._status is not None:
            return {"T": self._status["T"].name, "B": self._status["B"].name}

        return self._status

    @property
    def limit_status(self):
        """Return the current status of the limit detection of the blind from LimitStatus enum."""
        if self._limit_status is not None:
            return {"T": self._limit_status["T"].name, "B": self._limit_status["B"].name}

        return self._limit_status


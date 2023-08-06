#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""Evohome RF - RAMSES-II compatble Packet processor.

Operates at the pkt layer of: app - msg - pkt - h/w
"""

import asyncio
import logging
import os
import re
from datetime import datetime as dt
from datetime import timedelta as td
from multiprocessing import Process
from queue import Queue
from string import printable
from threading import Lock, Thread
from types import SimpleNamespace
from typing import ByteString, Callable, Optional, Tuple

from serial import serial_for_url  # Serial, SerialException, serial_for_url
from serial_asyncio import SerialTransport as SerialTransportAsync

from .command import Command, Priority
from .const import DTM_LONG_REGEX, HGI_DEV_ADDR, __dev_mode__
from .helpers import dt_str
from .packet import _PKT_LOGGER, Packet
from .protocol import create_protocol_factory
from .schema import (
    ALLOW_LIST,
    BLOCK_LIST,
    DISABLE_SENDING,
    ENFORCE_ALLOWLIST,
    ENFORCE_BLOCKLIST,
    EVOFW_FLAG,
    SERIAL_CONFIG,
    SERIAL_CONFIG_SCHEMA,
)
from .version import __version__

DEV_MODE = __dev_mode__ and False

ERR_MSG_REGEX = re.compile(r"^([0-9A-F]{2}\.)+$")

POLLER_TASK = "poller_task"

DEFAULT_SERIAL_CONFIG = SERIAL_CONFIG_SCHEMA(dict())

Pause = SimpleNamespace(
    NONE=td(seconds=0),
    MINIMUM=td(seconds=0.01),
    SHORT=td(seconds=0.05),
    DEFAULT=td(seconds=0.15),
    LONG=td(seconds=0.5),
)

INIT_QOS = {"priority": Priority.HIGHEST, "retries": 24, "disable_backoff": True}
INIT_CMD = Command._puzzle(message=f"v{__version__}", **INIT_QOS)

# tx (from sent to gwy, to get back from gwy) seems to takes approx. 0.025s
QOS_TX_TIMEOUT = td(seconds=0.05)  # 0.20 OK, but too high?
QOS_TX_RETRIES = 2

QOS_RX_TIMEOUT = td(seconds=0.50)  # 0.20 seems OK, 0.10 too low sometimes
QOS_MAX_BACKOFF = 3  # 4 = 16x, is too many?

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.WARNING)  # INFO may have too much detail
if DEV_MODE:  # or True:
    _LOGGER.setLevel(logging.DEBUG)  # should be INFO


class SerTransportDict(asyncio.Transport):
    """Interface for a packet transport using a file - Experimental."""

    def __init__(self, loop, protocol, packet_dict, extra=None):
        _LOGGER.info("SerTransDict.__init__(%s) *** dict version ***")

        self._loop = loop

        self._protocol = protocol
        self._pkt_dict = packet_dict
        self._extra = {} if extra is None else extra

        self._start()

    def _start(self):
        async def _polling_loop():
            if DEV_MODE:
                _LOGGER.debug("SerTransDict._polling_loop() BEGUN")
            self._protocol.pause_writing()
            self._protocol.connection_made(self)

            for dtm, pkt in self._pkt_dict:
                self._protocol.data_received(f"{dtm} {pkt}")
                await asyncio.sleep(0)

            if DEV_MODE:
                _LOGGER.debug("SerTransDict._polling_loop() ENDED")
            self._protocol.connection_lost(exc=None)

        if DEV_MODE:
            _LOGGER.debug("SerTransDict._start() STARTING loop")
        self._extra[POLLER_TASK] = self._loop.create_task(_polling_loop())

    def write(self, cmd):
        """Write some data bytes to the transport."""
        _LOGGER.debug("SerTransDict.write(%s)", cmd)

        raise NotImplementedError


class SerTransportFile(asyncio.Transport):
    """Interface for a packet transport using a file - Experimental."""

    def __init__(self, loop, protocol, packet_log, extra=None):
        _LOGGER.info("SerTransFile.__init__(%s) *** log file version ***", packet_log)

        self._loop = loop

        self._protocol = protocol
        self._pkt_fp = packet_log
        self._extra = {} if extra is None else extra

        self._start()

    def _start(self):
        async def _polling_loop():
            if DEV_MODE:
                _LOGGER.debug("SerTransFile._polling_loop() BEGUN")
            self._protocol.pause_writing()
            self._protocol.connection_made(self)

            for dtm_pkt_line in self._pkt_fp:
                self._protocol.data_received(dtm_pkt_line.strip())
                # await asyncio.sleep(0)

            if DEV_MODE:
                _LOGGER.debug("SerTransFile._polling_loop() ENDED")
            self._protocol.connection_lost(exc=None)

        if DEV_MODE:
            _LOGGER.debug("SerTransFile._start() STARTING loop")
        self._extra[POLLER_TASK] = self._loop.create_task(_polling_loop())

    def write(self, cmd):
        """Write some data bytes to the transport."""
        _LOGGER.debug("SerTransFile.write(%s)", cmd)

        raise NotImplementedError


class SerTransportPoller(asyncio.Transport):
    """Interface for a packet transport using polling."""

    MAX_BUFFER_SIZE = 500

    def __init__(self, loop, protocol, ser_instance, extra=None):
        _LOGGER.info("SerTransPoll.__init__(%s) *** Polling version ***", ser_instance)

        self._loop = loop
        self._protocol = protocol
        self.serial = ser_instance
        self._extra = {} if extra is None else extra

        self._is_closing = None
        self._write_queue = None

        self._start()

    def _start(self):
        async def _polling_loop():
            if DEV_MODE:
                _LOGGER.debug("SerTransPoll._polling_loop() BEGUN")
            self._protocol.connection_made(self)

            while self.serial.is_open:
                await asyncio.sleep(0.001)

                if self.serial.in_waiting:
                    self._protocol.data_received(
                        self.serial.read(self.serial.in_waiting)
                    )  # NOTE: cant use readline(), as it blocks until a newline
                    continue

                if hasattr(self.serial, "out_waiting") and self.serial.out_waiting:
                    continue

                if not self._write_queue.empty():
                    self.serial.write(self._write_queue.get())
                    self._write_queue.task_done()

            if DEV_MODE:
                _LOGGER.error("SerTransPoll._polling_loop() ENDED")
            self._protocol.connection_lost()

        if DEV_MODE:
            _LOGGER.debug("SerTransPoll._start() STARTING loop")
        self._write_queue = Queue(maxsize=self.MAX_BUFFER_SIZE)

        self._extra[POLLER_TASK] = self._loop.create_task(_polling_loop())

    def write(self, cmd):
        """Write some data bytes to the transport.

        This does not block; it buffers the data and arranges for it to be sent out
        asynchronously.
        """
        # _LOGGER.debug("SerTransPoll.write(%s)", cmd)

        self._write_queue.put_nowait(cmd)


class SerTransportProcess(Process):  # TODO: WIP
    """Interface for a packet transport using a process - WIP."""

    def __init__(self, loop, protocol, ser_port, extra=None):
        _LOGGER.info("SerTransProc.__init__() *** Process version ***", ser_port)

        self._loop = loop

        self._protocol = protocol
        self._ser_port = ser_port
        self._extra = {} if extra is None else extra

        self.serial = None
        self._is_closing = None
        self._poller = None
        self._write_queue = None

        self._start()

    def _start(self):
        def _polling_loop(self):
            if DEV_MODE:
                _LOGGER.error("WinTransport._polling_loop() BEGUN")

            # asyncio.set_event_loop(self._loop)
            asyncio.get_running_loop()  # TODO: this fails

            self._protocol.connection_made(self)

            while self.serial.is_open:
                if self.serial.in_waiting:
                    self._protocol.data_received(
                        # self.serial.readline()
                        self.serial.read()
                        # self.serial.read(self.serial.in_waiting)
                    )
                    # time.sleep(0.005)
                    continue

                if self.serial.out_waiting:
                    # time.sleep(0.005)
                    continue

                if not self._write_queue.empty():
                    cmd = self._write_queue.get()
                    self.serial.write(bytearray(f"{cmd}\r\n".encode("ascii")))
                    self._write_queue.task_done()
                    # time.sleep(0.005)
                    continue

                # print("sleep")
                # time.sleep(0.005)

            if DEV_MODE:
                _LOGGER.debug("SerTransProc._polling_loop() ENDED")
            self._protocol.connection_lost(exc=None)

        if DEV_MODE:
            _LOGGER.debug("SerTransProc._start() STARTING loop")
        self._write_queue = Queue(maxsize=200)

        self.serial = serial_for_url(self._ser_port[0], **self._ser_port[1])
        self.serial.timeout = 0

        self._poller = Thread(target=self._polling_loop, daemon=True)
        self._poller.start()

        self._protocol.connection_made(self)

    def write(self, cmd):
        """Write some data bytes to the transport.

        This does not block; it buffers the data and arranges for it to be sent out
        asynchronously.
        """
        # _LOGGER.debug("SerTransProc.write(%s)", cmd)

        self._write_queue.put_nowait(cmd)


class PacketProtocolBase(asyncio.Protocol):
    """Interface for a packet protocol (no Qos).

    ex transport: self.data_received(bytes) -> self._callback(pkt)
    to transport: self.send_data(cmd)       -> self._transport.write(bytes)
    """

    def __init__(self, gwy, pkt_handler: Callable) -> None:
        self._loop = gwy._loop

        self._gwy = gwy
        self._callback = pkt_handler  # Could be None

        self._transport = None
        self._pause_writing = True
        self._recv_buffer = bytes()

        self._sequence_no = 0

        # TODO: this is a little messy - the gwy.config[...] are mutex...
        self._include = list(gwy._include) if gwy.config[ENFORCE_ALLOWLIST] else []
        self._exclude = list(gwy._exclude) if gwy.config[ENFORCE_BLOCKLIST] else []

        if self._include:
            _LOGGER.info("Using an %s: %s", ALLOW_LIST, self._include)
        elif self._exclude:
            _LOGGER.info("Using an %s: %s", BLOCK_LIST, self._exclude)
        else:
            _LOGGER.warning("Not Using an device filter (an allow_list is recommended)")

        self._has_initialized = None
        if not self._gwy.config[DISABLE_SENDING]:
            self._loop.create_task(self.send_data(INIT_CMD))  # HACK: port wakeup

    def connection_made(self, transport: asyncio.Transport) -> None:
        """Called when a connection is made."""
        _LOGGER.debug("PktProtocol.connection_made(%s)", transport)

        self._transport = transport
        # self._transport.serial.rts = False

        _PKT_LOGGER.warning(
            "# evohome_rf %s", __version__, extra=self._extra(dt_str(), "")
        )

        self._loop.create_task(
            self._send_data(bytes("!V\r\n".encode("ascii")), ignore_pause=False)
        )  # Used to see if using a evofw3 rather than a HGI80
        self._pause_writing = False  # TODO: needs work

    @staticmethod
    def is_wanted(pkt, include_list, exclude_list) -> bool:
        """Parse the packet, return True if the packet is not to be filtered out."""
        if " 18:" in str(pkt):  # NOTE: " 18:", leading space is required
            return True
        if include_list:
            return any(device in str(pkt) for device in include_list)
        if exclude_list:
            return not any(device in str(pkt) for device in exclude_list)
        return True

    @staticmethod
    def _normalise(pkt_line: str) -> str:
        """Perform any firmware-level hacks, as required.

        Ensure an evofw3 provides the exact same output as a HGI80.
        """

        # bug fixed in evofw3 v0.6.x...
        # 095  I --- 18:013393 18:000730 --:------ 0001 005 00FFFF0200 # HGI80
        # 000  I --- 18:140805 18:140805 --:------ 0001 005 00FFFF0200 # evofw3
        if pkt_line[10:14] == " 18:" and pkt_line[11:20] == pkt_line[21:30]:
            pkt_line = pkt_line[:21] + HGI_DEV_ADDR.id + pkt_line[30:]
            if DEV_MODE:  # TODO: should be _LOGGER.debug
                _LOGGER.warning("evofw3 packet line has been normalised (0x00)")

        # non-RAMSES-II packets...
        elif (
            pkt_line[10:14] in (" 08:", " 31:") and pkt_line[-16:] == "* Checksum error"
        ):
            pkt_line = pkt_line[:-17] + " # Checksum error (ignored)"
            if DEV_MODE:  # TODO: should be _LOGGER.debug
                _LOGGER.warning("Packet line has been normalised (0x01)")

        # bug fixed in evofw3 v0.6.x...
        elif pkt_line.startswith("!C"):
            pkt_line = "# " + pkt_line
            if DEV_MODE:  # TODO: should be _LOGGER.debug
                _LOGGER.warning("Packet line has been normalised (0x02)")

        # old packet logs
        elif ERR_MSG_REGEX.match(pkt_line):
            pkt_line = "# " + pkt_line
            if DEV_MODE:  # TODO: should be _LOGGER.debug
                _LOGGER.warning("Packet line has been normalised (0x03)")

        return pkt_line

    def _data_received(  # sans QoS
        self, pkt_dtm: str, pkt_str: Optional[str], pkt_raw: Optional[ByteString] = None
    ) -> None:
        """Called when some normalised data is received (no QoS)."""
        _LOGGER.info("PktProtocol.data_rcvd(%s)", pkt_raw)

        pkt = Packet(pkt_dtm, pkt_str, raw_pkt_line=pkt_raw)
        if not pkt.is_valid:
            return
        elif self._has_initialized is None:
            self._has_initialized = True

        if self._callback and self.is_wanted(pkt, self._include, self._exclude):
            self._callback(pkt)  # only wanted PKTs up to the MSG transport's handler

    def data_received(self, data: ByteString) -> None:
        """Called when some data (raw packet fragment) is received."""
        if DEV_MODE:
            _LOGGER.debug("PktProtocol.data_rcvd(%s)", data)

        def create_pkt(pkt_raw: ByteString) -> Tuple:
            dtm_str = dt_str()  # done here & now for most-accurate timestamp

            try:
                pkt_str = "".join(
                    c
                    for c in pkt_raw.decode("ascii", errors="strict").strip()
                    if c in printable
                )
            except UnicodeDecodeError:
                _PKT_LOGGER.warning(
                    "%s < Bad pkt", pkt_raw, extra=self._extra(dtm_str, pkt_raw)
                )
                return dtm_str, None, pkt_raw

            if (  # "# evofw3" in pkt_str
                "# evofw3" in pkt_str
                and self._gwy.config[EVOFW_FLAG]
                and self._gwy.config[EVOFW_FLAG] != "!V"
            ):
                flag = self._gwy.config[EVOFW_FLAG]
                data = bytes(f"{flag}\r\n".encode("ascii"))
                self._loop.create_task(self._send_data(data, ignore_pause=True))

            if DEV_MODE:  # TODO: deleteme
                _LOGGER.debug("Rx: %s", pkt_raw, extra=self._extra(dtm_str, pkt_raw))

            return dtm_str, self._normalise(pkt_str), pkt_raw

        self._recv_buffer += data
        if b"\r\n" in self._recv_buffer:
            lines = self._recv_buffer.split(b"\r\n")
            self._recv_buffer = lines[-1]

            for line in lines[:-1]:
                pkt_dtm, pkt_str, pkt_raw = create_pkt(line)
                if pkt_str:
                    self._data_received(pkt_dtm, pkt_str, pkt_raw)

    async def _send_data(self, data: ByteString, ignore_pause=False) -> None:
        """Send a bytearray to the transport (serial) interface.

        The _pause_writing flag can be ignored, is useful for sending traceflags.
        """

        if not ignore_pause:
            while self._pause_writing:
                await asyncio.sleep(0.005)
        while (
            self._transport is None
            or self._transport.serial is None  # Shouldn't be required, but is!
            or (
                hasattr(self._transport.serial, "out_waiting")
                and self._transport.serial.out_waiting
            )
        ):
            await asyncio.sleep(0.005)
        if DEV_MODE:  # TODO: deleteme
            _LOGGER.debug("Tx:     %s", data, extra=self._extra(dt_str(), data))

        self._transport.write(data)
        # 0.2: can still exceed with back-to-back restarts
        # await asyncio.sleep(0.2)  # TODO: RF Duty cycle, make configurable?

    async def send_data(self, cmd: Command) -> None:
        """Called when some data is to be sent (not a callback)."""
        _LOGGER.info("PktProtocol.send_data(%s)", cmd)

        if self._gwy.config[DISABLE_SENDING]:
            raise RuntimeError("Sending is disabled")

        if not cmd.is_valid:
            _LOGGER.warning(
                "PktProtocol.send_data(%s): invalid command: %s", cmd.tx_header, cmd
            )
            return

        self._sequence_no = (self._sequence_no + 1) % 256
        if False and self._qos_cmd.seqn == "---":
            self._qos_cmd.seqn = f"{self._sequence_no:03d}"

        if cmd.from_addr.type != "18":
            _LOGGER.warning("PktProtocol.send_data(%s): IMPERSONATING!", cmd.tx_header)
            kmd = Command._puzzle("02", cmd.tx_header)
            await self._send_data(bytes(f"{kmd}\r\n".encode("ascii")))

        # self._loop.create_task(
        #     self._send_data(bytes(f"{cmd}\r\n".encode("ascii")))
        # )
        await self._send_data(bytes(f"{cmd}\r\n".encode("ascii")))

    def connection_lost(self, exc: Optional[Exception]) -> None:
        """Called when the connection is lost or closed."""
        _LOGGER.debug("PktProtocol.connection_lost(%s)", exc)

        if exc is not None:
            pass

    def pause_writing(self) -> None:
        """Called when the transport's buffer goes over the high-water mark."""
        _LOGGER.warning("PktProtocol.pause_writing()")
        # self._transport.get_write_buffer_size()

        self._pause_writing = True

    def resume_writing(self) -> None:
        """Called when the transport's buffer drains below the low-water mark."""
        _LOGGER.warning("PktProtocol.resume_writing()")
        # self._transport.get_write_buffer_size()

        self._pause_writing = False

    @staticmethod
    def _extra(dtm, pkt=None) -> dict:  # HACK: untidy: needs sorting, eventually
        """Create the dict required for logging"""
        _date, _time = dtm[:26].split("T")
        return {
            "date": _date,
            "time": _time,
            "_packet": str(pkt) + " " if pkt else "",
            "error_text": "",
            "comment": "",
        }


class PacketProtocol(PacketProtocolBase):
    """Interface for a packet protocol (without QoS)."""

    def __init__(self, gwy, pkt_handler: Callable) -> None:
        _LOGGER.info(
            "PktProtocol.__init__(gwy, %s) *** Std version ***",
            pkt_handler.__name__ if pkt_handler else None,
        )
        super().__init__(gwy, pkt_handler)


class PacketProtocolFile(PacketProtocolBase):
    """Interface for a packet protocol (for packet log)."""

    def __init__(self, gwy, pkt_handler: Callable) -> None:
        _LOGGER.info(
            "PacketProtocolFile.__init__(gwy, %s) *** Log version ***",
            pkt_handler.__name__ if pkt_handler else None,
        )
        super().__init__(gwy, pkt_handler)

    def connection_made(self, transport: asyncio.Transport) -> None:
        """Called when a connection is made."""
        _LOGGER.debug("PacketProtocolFile.connection_made(%s)", transport)

        self._transport = transport

        _PKT_LOGGER.warning(
            "# evohome_rf %s", __version__, extra=self._extra(dt_str(), "")
        )

    def data_received(self, data: str) -> None:
        """Called when some data is received."""
        _LOGGER.debug("PktProtocolFile.data_rcvd(%s)", data)

        pkt_dtm, pkt_str = data[:26], data[27:]

        try:
            assert DTM_LONG_REGEX.match(pkt_dtm)
            dt.fromisoformat(pkt_dtm)

        except (AssertionError, TypeError, ValueError):
            if data != "" and pkt_dtm.strip()[:1] != "#":
                _PKT_LOGGER.debug(
                    "%s < Packet line has an invalid timestamp (ignoring)",
                    data,  # TODO: None?
                    extra=self._extra(dt_str(), data),
                )

        else:
            self._data_received(pkt_dtm, self._normalise(pkt_str), None)


class PacketProtocolQos(PacketProtocolBase):
    """Interface for a packet protocol (includes QoS)."""

    def __init__(self, gwy, pkt_handler: Callable) -> None:
        _LOGGER.info(
            "PktProtocol.__init__(gwy, %s) *** Qos version ***",
            pkt_handler.__name__ if pkt_handler else None,
        )
        super().__init__(gwy, pkt_handler)

        self._qos_lock = Lock()
        self._qos_cmd = None
        self._tx_hdr = None
        self._rx_hdr = None
        self._tx_retries = None
        self._tx_retry_limit = None

        self._backoff = 0
        self._timeout_full = None
        self._timeout_half = None

    def _timeouts(self, dtm: dt) -> Tuple[dt, dt]:
        """Update self._timeout_full, self._timeout_half"""
        if self._qos_cmd:
            if self._tx_hdr:
                timeout = QOS_TX_TIMEOUT
            else:
                timeout = self._qos_cmd.qos.get("timeout", QOS_RX_TIMEOUT)
            self._timeout_full = dtm + timeout * 2 ** self._backoff
            self._timeout_half = dtm + timeout * 2 ** (self._backoff - 1)

            _LOGGER.debug(
                "backoff=%s, timeout=%s, timeout_full=%s",
                self._backoff,
                timeout,
                self._timeout_full,
            )

        # if self._timeout_half >= dtm:
        #     self._backoff = max(self._backoff - 1, 0)
        # if self._timeout_full >= dtm:
        #     self._backoff = min(self._backoff + 1, QOS_MAX_BACKOFF)

    def _data_received(  # with Qos
        self, pkt_dtm: str, pkt_str: Optional[str], pkt_raw: Optional[ByteString] = None
    ) -> None:
        """Called when some data is received. Adjust backoff as required."""
        _LOGGER.info("PktProtocolQos.data_rcvd(%s)", pkt_raw)

        def _logger_rcvd(logger, msg: str) -> None:
            if self._qos_cmd is None:
                wanted = None
            elif self._tx_hdr:
                wanted = self._tx_hdr
            else:
                wanted = self._rx_hdr

            logger(
                "PktProtocolQos.data_rcvd(%s): boff=%s, want=%s, tout=%s: %s",
                pkt._header,
                self._backoff,
                wanted,
                self._timeout_full,
                msg,
            )

        pkt = Packet(pkt_dtm, pkt_str, raw_pkt_line=pkt_raw)
        if not pkt.is_valid:
            return
        elif self._has_initialized is None:
            self._has_initialized = True

        if self._qos_cmd:
            _logger_rcvd(_LOGGER.debug, "CHECKING")

            # NOTE: is the Tx pkt, and no response is expected
            if pkt._header == self._tx_hdr and self._rx_hdr is None:
                msg = "matched the Tx pkt (not wanting a Rx pkt) - now done"
                self._qos_lock.acquire()
                self._qos_cmd = None
                self._qos_lock.release()

            # NOTE: is the Tx pkt, and a response *is* expected
            elif pkt._header == self._tx_hdr:
                # assert str(pkt)[4:] == str(self._qos_cmd), "Packets dont match"
                msg = "matched the Tx pkt (now wanting a Rx pkt)"
                self._tx_hdr = None

            # NOTE: is the Tx pkt, but is a *duplicate* - we've already seen it!
            elif pkt._header == self._qos_cmd.tx_header:
                # assert str(pkt) == str(self._qos_cmd), "Packets dont match"
                msg = "duplicated Tx pkt (still wanting the Rx pkt)"
                self._timeouts(dt.now())  # TODO: increase backoff?

            # NOTE: is the Rx pkt, and is a non-Null (expected) response
            elif pkt._header == self._rx_hdr:
                msg = "matched the Rx pkt - now done"
                self._qos_lock.acquire()
                self._qos_cmd = None
                self._qos_lock.release()

            # TODO: is the Rx pkt, but is a Null response
            # elif pkt._header == self._qos_cmd.null_header:
            #     msg = "matched a NULL Rx pkt - now done"
            #     self._qos_lock.acquire()
            #     self._qos_cmd = None
            #     self._qos_lock.release()

            # NOTE: is not the expected pkt, but another pkt
            else:
                msg = (
                    "unmatched pkt (still wanting a "
                    + ("Tx" if self._tx_hdr else "Rx")
                    + " pkt)"
                )

            self._timeouts(dt.now())
            _logger_rcvd(_LOGGER.debug, f"CHECKED - {msg}")

        else:  # no outstanding cmd - ?throttle down the backoff
            # self._timeouts(dt.now())
            _logger_rcvd(_LOGGER.debug, "XXXXXXX - ")

        if self._callback and self.is_wanted(pkt, self._include, self._exclude):
            self._callback(pkt)  # only wanted PKTs up to the MSG transport's handler

    async def send_data(self, cmd: Command) -> None:
        """Called when some data is to be sent (not a callback)."""
        _LOGGER.info("PktProtocolQos.send_data(%s)", cmd)

        def _logger_send(logger, msg: str) -> None:
            logger(
                "PktProtocolQos.send_data(%s): boff=%s, want=%s, tout=%s: %s",
                cmd.tx_header,
                self._backoff,
                self._tx_hdr if self._tx_hdr else self._rx_hdr,
                self._timeout_full,
                msg,
            )

        if self._gwy.config[DISABLE_SENDING]:
            raise RuntimeError("Sending is disabled")

        if not cmd.is_valid:
            _LOGGER.warning(
                "PktProtocolQos.send_data(%s): invalid command: %s", cmd.tx_header, cmd
            )
            return

        while self._qos_cmd is not None:
            await asyncio.sleep(0.005)

        self._qos_lock.acquire()
        self._qos_cmd = cmd
        self._qos_lock.release()
        self._tx_hdr = cmd.tx_header
        self._rx_hdr = cmd.rx_header  # Could be None
        self._tx_retries = 0
        self._tx_retry_limit = cmd.qos.get("retries", QOS_TX_RETRIES)

        self._sequence_no = (self._sequence_no + 1) % 256
        if False and self._qos_cmd.seqn == "---":
            self._qos_cmd.seqn = f"{self._sequence_no:03d}"

        if cmd.from_addr.type != "18":
            _LOGGER.warning(
                "PacketProtocolQos.send_data(%s): IMPERSONATING!", cmd.tx_header
            )
            kmd = Command._puzzle("02", cmd.tx_header)
            await self._send_data(bytes(f"{kmd}\r\n".encode("ascii")))

        self._timeouts(dt.now())
        await self._send_data(bytes(f"{cmd}\r\n".encode("ascii")))

        while self._qos_cmd is not None:  # until sent (may need re-transmit) or expired
            await asyncio.sleep(0.005)
            if self._timeout_full > dt.now():
                await asyncio.sleep(0.02)
                # await self._send_data(bytes("\r\n".encode("ascii")))

            elif self._qos_cmd is None:  # can be set to None by data_received
                continue

            elif self._tx_retries < self._tx_retry_limit:
                self._tx_hdr = cmd.tx_header
                self._tx_retries += 1
                if not self._qos_cmd.qos.get("disable_backoff", False):
                    self._backoff = min(self._backoff + 1, QOS_MAX_BACKOFF)
                self._timeouts(dt.now())
                await self._send_data(bytes(f"{cmd}\r\n".encode("ascii")))
                _logger_send(
                    _LOGGER.warning,
                    f"RE-SENT ({self._tx_retries}/{self._tx_retry_limit})",
                )  # TODO: should be info/debug

            else:
                if self._qos_cmd.code != "7FFF":  # HACK: why expired when shouldn't
                    _logger_send(_LOGGER.error, "EXPIRED")
                self._qos_lock.acquire()
                self._qos_cmd = None
                self._qos_lock.release()
                self._backoff = 0  # TODO: need a better system
                break

        else:
            if self._timeout_half >= dt.now():
                self._backoff = max(self._backoff - 1, 0)
            _logger_send(_LOGGER.debug, "SENT OK")


def create_pkt_stack(
    gwy, msg_handler, protocol_factory=None, serial_port=None, packet_log=None
) -> Tuple[asyncio.Protocol, asyncio.Transport]:
    """Utility function to provide a transport to the internal protocol.

    The architecture is: app (client) -> msg -> pkt -> ser (HW interface).

    The msg/pkt interface is via:
     - PktProtocol.data_received           to (msg_handler)  MsgTransport._pkt_receiver
     - MsgTransport.write (pkt_dispatcher) to (pkt_protocol) PktProtocol.send_data
    """

    def _protocol_factory():
        if packet_log:
            return create_protocol_factory(PacketProtocolFile, gwy, msg_handler)()
        elif gwy.config[DISABLE_SENDING]:
            return create_protocol_factory(PacketProtocol, gwy, msg_handler)()
        else:
            return create_protocol_factory(PacketProtocolQos, gwy, msg_handler)()

    assert (serial_port is not None and packet_log is None) or (
        serial_port is None and packet_log is not None
    ), "port / file are not mutually exclusive"

    pkt_protocol = protocol_factory() if protocol_factory else _protocol_factory()

    if packet_log:
        pkt_transport = SerTransportFile(gwy._loop, pkt_protocol, packet_log)
        return (pkt_protocol, pkt_transport)

    serial_config = DEFAULT_SERIAL_CONFIG
    serial_config.update(gwy.config[SERIAL_CONFIG])

    ser_instance = serial_for_url(serial_port, **serial_config)
    if os.name == "posix":  # or use: NotImplementedError
        try:
            ser_instance.set_low_latency_mode(True)  # only for FTDI?
        except (AttributeError, ValueError):  # AttributeError shouldn't be needed
            pass

    if any(
        (
            serial_port.startswith("rfc2217:"),
            serial_port.startswith("socket:"),
            os.name == "nt",
        )
    ):
        pkt_transport = SerTransportPoller(gwy._loop, pkt_protocol, ser_instance)
    else:
        pkt_transport = SerialTransportAsync(gwy._loop, pkt_protocol, ser_instance)

    return (pkt_protocol, pkt_transport)

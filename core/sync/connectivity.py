"""
Connectivity Manager for IELTS by GAMA.
Manages network status (OFFLINE, ONLINE, ONLINE_LIMITED, SYNCING),
ensures user always knows data transmission status, and supports manual offline lock.
"""

import enum
import socket
import threading
import time
from typing import Callable, List, Optional


class ConnectivityState(str, enum.Enum):
    OFFLINE = "OFFLINE"
    ONLINE = "ONLINE"
    ONLINE_LIMITED = "ONLINE_LIMITED"
    SYNCING = "SYNCING"


class ConnectivityManager:
    """Singleton connectivity supervisor."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConnectivityManager, cls).__new__(cls)
                cls._instance._init()
            return cls._instance

    def _init(self):
        self._state = ConnectivityState.OFFLINE
        self._forced_offline = False
        self._listeners: List[Callable[[ConnectivityState], None]] = []
        self._probe_hosts = [("8.8.8.8", 53), ("1.1.1.1", 53)]
        self._state_lock = threading.RLock()
        self.check_connection()

    @property
    def state(self) -> ConnectivityState:
        with self._state_lock:
            if self._forced_offline:
                return ConnectivityState.OFFLINE
            return self._state

    @property
    def is_online(self) -> bool:
        return self.state in [ConnectivityState.ONLINE, ConnectivityState.SYNCING]

    @property
    def is_forced_offline(self) -> bool:
        return self._forced_offline

    def set_forced_offline(self, enabled: bool):
        """Allows user to enforce 100% offline mode regardless of physical network."""
        with self._state_lock:
            self._forced_offline = enabled
            self._notify_listeners()

    def set_state(self, new_state: ConnectivityState):
        with self._state_lock:
            if self._state != new_state:
                self._state = new_state
                self._notify_listeners()

    def add_listener(self, listener: Callable[[ConnectivityState], None]):
        with self._state_lock:
            if listener not in self._listeners:
                self._listeners.append(listener)

    def remove_listener(self, listener: Callable[[ConnectivityState], None]):
        with self._state_lock:
            if listener in self._listeners:
                self._listeners.remove(listener)

    def _notify_listeners(self):
        current = self.state
        for cb in list(self._listeners):
            try:
                cb(current)
            except Exception:
                pass

    def check_connection(self) -> ConnectivityState:
        """Actively probes internet connection."""
        if self._forced_offline:
            return ConnectivityState.OFFLINE
        connected = False
        for host, port in self._probe_hosts:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.5)
                sock.connect((host, port))
                sock.close()
                connected = True
                break
            except (socket.timeout, OSError):
                continue

        with self._state_lock:
            old = self._state
            self._state = ConnectivityState.ONLINE if connected else ConnectivityState.OFFLINE
            if old != self._state:
                self._notify_listeners()
            return self.state

    def get_ui_indicator(self) -> str:
        """Returns prompt-specified indicator text."""
        s = self.state
        if s == ConnectivityState.ONLINE:
            return "● ONLINE"
        elif s == ConnectivityState.SYNCING:
            return "● SYNCING"
        elif s == ConnectivityState.ONLINE_LIMITED:
            return "● ONLINE (LIMITED)"
        else:
            return "● OFFLINE"

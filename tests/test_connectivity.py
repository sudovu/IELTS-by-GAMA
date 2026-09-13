"""
Unit tests for ConnectivityManager and sync states.
"""

import unittest
from core.sync.connectivity import ConnectivityManager, ConnectivityState


class TestConnectivity(unittest.TestCase):
    def setUp(self):
        self.mgr = ConnectivityManager()
        self.mgr.set_forced_offline(False)

    def test_forced_offline_toggle(self):
        self.mgr.set_forced_offline(True)
        self.assertEqual(self.mgr.state, ConnectivityState.OFFLINE)
        self.assertFalse(self.mgr.is_online)
        self.assertEqual(self.mgr.get_ui_indicator(), "● OFFLINE")

        self.mgr.set_forced_offline(False)
        # Indicator reflects actual state
        indicator = self.mgr.get_ui_indicator()
        self.assertTrue(indicator.startswith("● "))

    def test_listener_notifications(self):
        events = []
        def listener(state):
            events.append(state)

        self.mgr.add_listener(listener)
        self.mgr.set_forced_offline(True)
        self.assertIn(ConnectivityState.OFFLINE, events)

        self.mgr.remove_listener(listener)
        self.mgr.set_forced_offline(False)


if __name__ == "__main__":
    unittest.main()

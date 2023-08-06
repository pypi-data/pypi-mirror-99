# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading
import time
from contrast.agent import scope
from contrast.utils.decorators import fail_safely
from contrast.utils.timer import Timer

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


class Heartbeat(threading.Thread):
    def __init__(self, settings):
        super(Heartbeat, self).__init__()
        self.daemon = True
        self.settings = settings
        self.stopped = False

        self.heartbeat_interval_ms = self.settings.config.get(
            "agent.polling.app_activity_ms", 30000
        )
        self.heartbeat_interval_sec = self.heartbeat_interval_ms / 1000

        # Agent should not ping too frequently
        if self.heartbeat_interval_ms < 10000:
            self.heartbeat_interval_ms = 10000
            self.heartbeat_interval_sec = 10

    def get_sleep_time(self):
        return self.heartbeat_interval_sec

    def run(self):
        # Ensure the heartbeat thread runs in scope because it is initialized
        # before our thread.start patch is applied.
        with scope.contrast_scope():
            logger.debug("Establishing heartbeat")

            while not self.stopped and self.settings.is_agent_config_enabled():
                self.send_heartbeat()
                time.sleep(self.get_sleep_time())

    @fail_safely("Error sending a heartbeat message")
    def send_heartbeat(self):
        from contrast.agent import service_client

        heartbeat_interval_ms = self.heartbeat_interval_ms

        # only send after we have not updated after the last interval time set in the config
        if (
            self.settings.last_update is not None
            and (Timer.now_ms() - self.settings.last_update) > heartbeat_interval_ms
        ):
            service_client.send_heartbeat_message()

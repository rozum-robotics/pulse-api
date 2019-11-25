import asyncio
import logging

from aiopdhttp.api import RobotApi
from pulseapi import RobotPulse, MotionStatus

class AioRobotPulse(RobotPulse):
    
    def __init__(self, host=None, logger=None):
        self._api = RobotApi()
        if host is not None:
            host = "http://" + host
            self._api.api_client.configuration.host = host
        if logger is None:
            logger = logging.getLogger("pulseapi")
            logger.addHandler(logging.NullHandler())
        self.logger = logger
        self.host = self._api.api_client.configuration.host
    
    async def __aenter__(self):
        return self
    
    async def stop(self, asking_interval=0.1):
        self.logger.debug(str(asking_interval))
        while await self.status_motion() != MotionStatus.IDLE:
            await asyncio.sleep(asking_interval)
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._api.api_client.rest_client.pool_manager.close()

from enum import Enum
from typing import Union
from collections import deque
from typing import Deque, Union
from ._job_handler import JobHandler
from ._job_cache import JobCache

class Inherit(Enum):
    INHERIT = ''

class ConfigEntry:
    def __init__(self, use_container: bool, job_handler: Union[JobHandler, None], job_cache: Union[JobCache, None]):
        self._use_container = use_container
        self._job_handler = job_handler
        self._job_cache = job_cache
    @property
    def use_container(self):
        return self._use_container
    @property
    def job_handler(self):
        return self._job_handler
    @property
    def job_cache(self):
        return self._job_cache

class UseConfig:
    def __init__(self, config: ConfigEntry):
        self._config = config
    def __enter__(self):
        Config.config_stack.append(self._config)
    def __exit__(self, exc_type, exc_val, exc_tb):
        Config.config_stack.pop()

class Config:
    config_stack: Deque[ConfigEntry] = deque()

    def __init__(self,
        use_container: Union[bool, Inherit]=Inherit.INHERIT,
        job_handler: Union[JobHandler, None, Inherit]=Inherit.INHERIT,
        job_cache: Union[JobCache, None, Inherit]=Inherit.INHERIT
    ):
        old_config = Config.config_stack[-1] # throws if no default set
        self.new_config = ConfigEntry(
            use_container=use_container if not isinstance(use_container, Inherit) else old_config.use_container,
            job_handler=job_handler if not isinstance(job_handler, Inherit) else old_config.job_handler,
            job_cache=job_cache if not isinstance(job_cache, Inherit) else old_config.job_cache
        )

    @staticmethod
    def get_current_config() -> ConfigEntry:
        return Config.config_stack[-1]
    
    @staticmethod
    def get_default_config() -> ConfigEntry:
        return ConfigEntry(
            use_container=False,
            job_handler=None,
            job_cache=None
        )

    def __enter__(self):
        Config.config_stack.append(self.new_config)
    def __exit__(self, exc_type, exc_val, exc_tb):
        Config.config_stack.pop()

Config.config_stack.append(Config.get_default_config())
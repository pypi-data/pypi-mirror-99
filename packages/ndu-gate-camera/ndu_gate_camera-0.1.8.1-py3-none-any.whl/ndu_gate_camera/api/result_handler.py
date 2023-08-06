from abc import ABC, abstractmethod

import logging

log = logging.getLogger("result")


class ResultHandler(ABC):

    @abstractmethod
    def save_result(self, result, device=None, runner_name=None, data_type='telemetry'):
        pass

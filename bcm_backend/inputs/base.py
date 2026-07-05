from abc import ABC, abstractmethod

class TelemetryInput(ABC):
    @abstractmethod
    def frames(self):
        """
        Yield raw CAN frames one by one
        """
        pass
from abc import ABC, abstractmethod
import logging

from ROAR.roar_autonomous_system.utilities_module.vehicle_models import (
    Vehicle,
    VehicleControl,
)
from ROAR.roar_autonomous_system.utilities_module.data_structures_models import Transform


class Controller(ABC):
    def __init__(self, agent):
        self.agent = agent

    @abstractmethod
    def run_step(self, next_waypoint: Transform, **kwargs) \
            -> VehicleControl:
        """
        Abstract function for run step

        Args:
            next_waypoint: next waypoint
            **kwargs:

        Returns:
            VehicleControl
        """
        return VehicleControl()

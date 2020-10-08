from ROAR.roar_autonomous_system.agent_module.agent import Agent
from ROAR.roar_autonomous_system.utilities_module.data_structures_models import SensorsData
from ROAR.roar_autonomous_system.utilities_module.vehicle_models import Vehicle, VehicleControl
from ROAR.roar_autonomous_system.configurations.agent_settings import AgentConfig
import numpy as np
import random
import cv2


class ForwardOnlyAgent(Agent):
    def __init__(self, vehicle: Vehicle, agent_settings: AgentConfig):
        super().__init__(vehicle, agent_settings)

    def run_step(self, sensors_data: SensorsData, vehicle: Vehicle) -> VehicleControl:
        super().run_step(sensors_data=sensors_data, vehicle=vehicle)
        control = VehicleControl(throttle=0.4, steering=0)
        if sensors_data.front_rgb is not None and sensors_data.front_rgb.data is not None:
            cv2.imshow("rgb", self.front_rgb_camera.data)
            cv2.waitKey(1)
        return control

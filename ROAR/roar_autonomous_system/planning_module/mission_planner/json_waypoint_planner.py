from ROAR.roar_autonomous_system.planning_module.mission_planner.mission_planner import MissionPlanner
from ROAR.roar_autonomous_system.utilities_module.data_structures_models import Transform, Location
from typing import List
from pathlib import Path
from ROAR.roar_autonomous_system.utilities_module.data_structures_models import MapEntry
import json
import numpy as np
from ROAR.roar_autonomous_system.agent_module.agent import Agent
from collections import deque


class JSONWaypointPlanner(MissionPlanner):
    def __init__(self, agent: Agent):
        super().__init__(agent=agent)
        self.file_path: Path = Path(self.agent.agent_settings.json_waypoint_file_path)
        self.mission_plan: deque = self.run_step()
        # print(self._read_data_file())

    def run_step(self) -> deque:
        result = deque()
        map_entries = self._read_data_file()
        for m in map_entries:
            result.append(self._map_entry_to_transform(map_entry=m))
        return result

    def _read_data_file(self):
        raw = json.load(fp=self.file_path.open('r'))
        result = [MapEntry.parse_obj(i) for i in raw]
        return result

    def _map_entry_to_transform(self, map_entry: MapEntry):
        mid_point = (np.array(map_entry.point_a) + np.array(map_entry.point_b)) / 2
        return Transform(
            location=Location(x=mid_point[0], y=mid_point[1], z=mid_point[2])
        )

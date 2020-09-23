from ROAR.roar_autonomous_system.perception_module.detector import Detector
import logging
import open3d as o3d
import numpy as np
import cv2
import time
from typing import Optional
from ROAR.roar_autonomous_system.perception_module.point_cloud_detector import PointCloudDetector
from ROAR.roar_autonomous_system.utilities_module.data_structures_models import Transform, Location, Rotation


class GroundPlanePointCloudDetector(PointCloudDetector):
    def __init__(self,
                 max_ground_height_relative_to_vehcile=5,
                 knn=200,
                 std_ratio=2,
                 nb_neighbors=10,
                 ground_tilt_threshhold=0.05,
                 **kwargs):
        """

        Args:
            max_ground_height_relative_to_vehicle: anything above this height will be chucked away since it will be probaly ceiling
            knn: when finding reference points for ground detection, this is the number of points in front of the vehicle the algorithm will serach for
            std_ratio: this is the ratio that determines whether a point is an outlier. it is used in conjunction with nb_neighbor
            nb_neighbors: how many neighbors are around this point for it to be classified as "within" main frame
            ground_tilt_threshhold: variable to help compensate for slopes on the ground
            **kwargs:
        """
        super().__init__(**kwargs)
        self.logger = logging.getLogger("Point Cloud Detector")

        self.max_ground_height_relative_to_vehcile = max_ground_height_relative_to_vehcile
        self.knn = knn
        self.std_ratio = std_ratio
        self.nb_neighbors = nb_neighbors
        self.ground_tilt_threshold = ground_tilt_threshhold
        self.counter = 0
        self.reference_normal = None

    def run_step(self) -> np.ndarray:
        points_3d = self.calculate_world_cords()  # (Nx3)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points_3d)  # - np.mean(points_3d, axis=0))
        pcd.estimate_normals()
        normals = np.asarray(pcd.normals)
        if self.reference_normal is None:
            pcd_tree = o3d.geometry.KDTreeFlann(pcd)  # build KD tree for fast computation
            [k, idx, _] = pcd_tree.search_knn_vector_3d(self.agent.vehicle.transform.location.to_array(), knn=self.knn)  # find points around me
            points_near_me = np.asarray(pcd.points)[idx, :]  # 200 x 3
            u, s, vh = np.linalg.svd(points_near_me, full_matrices=False)  # use svd to find normals of points
            self.reference_normal = vh[2, :]
        norm_flat = np.abs(normals @ self.reference_normal)
        planes = points_3d[norm_flat > 1-self.ground_tilt_threshold]
        ground = planes[planes[:, 2] < self.agent.vehicle.transform.location.z +
                        self.max_ground_height_relative_to_vehcile]
        # pcd.points = o3d.utility.Vector3dVector(ground)  # - np.mean(planes, axis=0))

        # pcd, ids = pcd.remove_statistical_outlier(nb_neighbors=self.nb_neighbors, std_ratio=self.std_ratio)

        # self.pcd.points = o3d.utility.Vector3dVector(np.asarray(pcd.points) - np.mean(np.asarray(pcd.points), axis=0))
        # if self.counter == 0:
        #     self.vis.create_window(window_name="Open3d", width=400, height=400)
        #     self.vis.add_geometry(self.pcd)
        #     render_option: o3d.visualization.RenderOption = self.vis.get_render_option()
        #     render_option.show_coordinate_frame = True
        # else:
        #     self.vis.update_geometry(self.pcd)
        #     render_option: o3d.visualization.RenderOption = self.vis.get_render_option()
        #     render_option.show_coordinate_frame = True
        #     self.vis.poll_events()
        #     self.vis.update_renderer()
        self.counter += 1
        # return np.asarray(pcd.points)
        return ground

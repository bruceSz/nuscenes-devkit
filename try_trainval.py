import os.path as osp
import numpy as np
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud, RadarPointCloud, Box
from nuscenes.utils.geometry_utils import view_points, transform_matrix
import matplotlib.pyplot as plt

#nusc = NuScenes(version='v1.0-mini', dataroot='/media/aicore/Daten/aicore 2TB/nuScenes/v1.0-mini', verbose=True)
nusc = NuScenes(version='v1.0-trainval', dataroot='/media/aicore/Daten/aicore 2TB/nuScenes/v1.0-trainval', verbose=True)

file = nusc.sample_data[10]['filename']
print(file)
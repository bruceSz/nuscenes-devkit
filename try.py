import os.path as osp
import numpy as np
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud, RadarPointCloud, Box
from nuscenes.utils.geometry_utils import view_points, transform_matrix
import matplotlib.pyplot as plt

nusc = NuScenes(version='v1.0-mini', dataroot='/media/aicore/Daten/aicore 2TB/nuScenes/v1.0-mini', verbose=True)

my_sample = nusc.get('sample', 'cd9964f8c3d34383b16e9c2997de1ed0')
#nusc.render_sample(my_sample['token'])

sample_record = nusc.get('sample', my_sample['token'])
#nusc.list_sample(my_sample['token'])
for sd_token in sample_record['data'].values():
    sd_record = nusc.get('sample_data', sd_token)
    if sd_record['sensor_modality'] == 'lidar':
        pcl_path = osp.join(nusc.dataroot, sd_record['filename'])
        pc = LidarPointCloud.from_file(pcl_path)
        view = np.eye(4)
        print(pc.points.shape)
        count = 0
        points_in_horizion = np.transpose(view_points(pc.points[:3, :], view, normalize=True))
        for point in points_in_horizion:
            if np.sum(np.square(point[0:1])) > 2500:
                count += 1

        print(count, len(points_in_horizion))
        count = 0
        points = np.transpose(pc.points[:3, :])
        for point in points:
            if point[2] > 10:
                print(point)
                count += 1
            if np.sum(np.square(point[0:1])) < 1 and point[2] < 0.3:
                print(point)
        print(count, len(points))
        print(pc.points[3, :])

        fig, axes = plt.subplots(1, 2, figsize=(18, 9))
        pc.render_height(axes[0], view=view)



print('annotations')
for sa_token in sample_record['anns']:
    sa_record = nusc.get('sample_annotation', sa_token)
    print(sa_record['rotation'])



my_scene_token = nusc.field2token('scene', 'name', 'scene-0061')[0]
nusc.render_scene(my_scene_token)

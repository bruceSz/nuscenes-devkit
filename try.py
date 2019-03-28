import os.path as osp
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud, RadarPointCloud, Box

nusc = NuScenes(version='v1.0-mini', dataroot='./data', verbose=True)
my_sample = nusc.get('sample', 'cd9964f8c3d34383b16e9c2997de1ed0')
#nusc.render_sample(my_sample['token'])

sample_record = nusc.get('sample', my_sample['token'])
#nusc.list_sample(my_sample['token'])
for sd_token in sample_record['data'].values():
    sd_record = nusc.get('sample_data', sd_token)
    if sd_record['sensor_modality'] == 'lidar':
        pcl_path = osp.join(nusc.dataroot, sd_record['filename'])
        pc = LidarPointCloud.from_file(pcl_path)
        print(pc)

print('annotations')
for sa_token in sample_record['anns']:
    sa_record = nusc.get('sample_annotation', sa_token)
    print(sa_record)


my_scene_token = nusc.field2token('scene', 'name', 'scene-0061')[0]
#nusc.render_scene(my_scene_token)

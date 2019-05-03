from nuscenes.nuscenes import NuScenes
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from typing import Tuple, List
import sklearn.metrics
from PIL import Image
from nuscenes.utils.geometry_utils import view_points, box_in_image, BoxVisibility
print(BoxVisibility.ANY)
import os, sys, glob, gc
import subprocess
nusc = NuScenes(version='v1.0-trainval', dataroot='/media/aicore/Daten/aicore2TB/nuScenes/v1.0-trainval', verbose=True)


def render_sample(token: str,
                  index: int,
                  description: str,
                  mode: bool,
                  box_vis_level: BoxVisibility = BoxVisibility.ANY,
                  nsweeps: int = 1,
                  out_path: str = None) -> None:
    """
    Render all LIDAR and camera sample_data in sample along with annotations.
    :param token: Sample token.
    :param box_vis_level: If sample_data is an image, this sets required visibility for boxes.
    :param nsweeps: Number of sweeps for lidar and radar.
    """
    record = nusc.get('sample', token)

    # Separate RADAR from LIDAR and vision.
    radar_data = {}
    nonradar_data = {}
    for channel, token in record['data'].items():
        sd_record = nusc.get('sample_data', token)
        sensor_modality = sd_record['sensor_modality']
        if sensor_modality in ['lidar', 'camera']:
            nonradar_data[channel] = token
        else:
            radar_data[channel] = token

    # Create plots.
    n = 2 + len(nonradar_data)
    cols = 3
    fig, axes = plt.subplots(int(np.ceil(n / cols)), cols, figsize=(24, 16))

    ax = axes[0, 0]

    ax.text(0, 1, str(index), fontsize=20,
            verticalalignment="top", horizontalalignment="left",
            bbox=dict(boxstyle="square", ec=(1., 0.5, 0.5), fc=(1., 0.8, 0.8), )
            )
    if mode:
        ax.text(0, 0.9, description, fontsize=20,
                verticalalignment="top", horizontalalignment="left"
                )
    ax.axis('off')
    # render_egoposes_on_map(map_poses, close_poses, ax: Axes, title, mask)

    # Plot radar into a single subplot.
    ax = axes[0, 1]
    for i, (_, sd_token) in enumerate(radar_data.items()):
        nusc.render_sample_data(sd_token, with_anns=(i == 0) and mode, box_vis_level=box_vis_level, ax=ax,
                                nsweeps=nsweeps)
    ax.set_title('Fused RADARs')

    name_list = ['LIDAR_TOP', 'CAM_FRONT_LEFT', 'CAM_FRONT', 'CAM_FRONT_RIGHT', 'CAM_BACK_LEFT', 'CAM_BACK',
                 'CAM_BACK_RIGHT']
    output_list = [nonradar_data[key] for key in name_list if key in nonradar_data]

    # Plot camera and lidar in separate subplots.
    for sd_token, ax in zip(output_list, axes.flatten()[2:]):
        nusc.render_sample_data(sd_token, with_anns=mode, box_vis_level=box_vis_level, ax=ax, nsweeps=nsweeps)

    axes.flatten()[-1].axis('off')
    plt.tight_layout()
    fig.subplots_adjust(wspace=0, hspace=0)

    if out_path != None:
        fig.savefig(out_path)  # save the figure to file
        plt.close(fig)  # close the figure

dir_label = '/media/aicore/Daten/aicore2TB/nuScenes/scenerio/scenes_label/temp'
dir_no_label = '/media/aicore/Daten/aicore2TB/nuScenes/scenerio/scenes/temp'

def make_video(scene_name, label):
    if label:
        os.chdir(dir_label)
        file_name = 'scenes_label'
    else:
        os.chdir(dir_no_label)
        file_name = 'scenes'
    subprocess.call([
        'ffmpeg', '-framerate', '1', '-i', 'sample%02d.png',
        '-r', '1', '-crf', '15', '-b', '10M',
        '-pix_fmt', 'yuv420p',
        '/media/aicore/Daten/aicore2TB/nuScenes/scenerio/%s/%s.mp4'%(file_name, scene_name)])
    for file_name in glob.glob("*.png"):
        os.remove(file_name)


# scene_rec = nusc.get('scene', scene_token)

for scene_rec in nusc.scene:
    dsc = scene_rec['description']

    first_sample_token = scene_rec['first_sample_token']
    last_sample_token = scene_rec['last_sample_token']

    current_sample_token = first_sample_token

    # map_poses, close_poses, mask, title = render_egoposes_on_map_init(record['scene_token'])

    count = 0
    while current_sample_token != last_sample_token:
        current_sample = nusc.get('sample', current_sample_token)
        # nusc.render_sample_data(current_sample['data']['LIDAR_TOP'], with_anns=True)
        render_sample(current_sample_token, count, dsc, True, out_path=dir_label + '/sample%02d.png' % count)
        render_sample(current_sample_token, count, dsc, False, out_path=dir_no_label + '/sample%02d.png' % count)

        count += 1
        current_sample_token = current_sample['next']

    make_video(scene_rec['name'], True)
    make_video(scene_rec['name'], False)
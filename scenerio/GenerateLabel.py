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
import csv

nusc = NuScenes(version='v1.0-trainval', dataroot='/media/aicore/Daten/aicore2TB/nuScenes/v1.0-trainval', verbose=True)


def get_color(category_name: str) -> Tuple[int, int, int]:
    """ Provides the default colors based on the category names. """
    if category_name in ['vehicle.bicycle', 'vehicle.motorcycle']:
        return 255, 61, 99  # Red
    elif 'vehicle' in category_name:
        return 255, 158, 0  # Orange
    elif 'human.pedestrian' in category_name:
        return 0, 0, 230  # Blue
    elif 'cone' in category_name or 'barrier' in category_name:
        return 0, 0, 0  # Black
    else:
        return 255, 0, 255  # Magenta


def render_sample_labelonly(sample_token: str,
                            with_anns: bool = True,
                            box_vis_level: BoxVisibility = BoxVisibility.ANY,
                            axes_limit: float = 50,
                            ax: Axes = None,
                            out_path: str = None) -> None:
    """
    Render sample data onto axis.
    :param sample_data_token: Sample_data token.
    :param with_anns: Whether to draw annotations.
    :param box_vis_level: If sample_data is an image, this sets required visibility for boxes.
    :param axes_limit: Axes limit for lidar and radar (measured in meters).
    :param ax: Axes onto which to render.
    :param nsweeps: Number of sweeps for lidar and radar.
    """

    # Get sensor modality.  should be 'LIDAR_TOP'
    lidar_sd_record = nusc.get('sample_data', sample_token['data']['LIDAR_TOP'])

    # Get boxes in lidar frame.
    _, boxes, _ = nusc.get_sample_data(sample_token['data']['LIDAR_TOP'], box_vis_level=box_vis_level)
    # _, boxes, camera_intrinsic = nusc.get_sample_data(sample_token['data']['CAM_FRONT'], box_vis_level=box_vis_level)
    # Note that the boxes are transformed into the current sensor's coordinate frame.

    # Init axes.
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(9, 9))

    # Show ego vehicle.
    ax.plot(0, 0, 'x', color='red')

    # Show boxes.
    if with_anns:
        for box in boxes:
            c = np.array(get_color(box.name)) / 255.0
            box.render(ax, view=np.eye(4), normalize=False, colors=(c, c, c), linewidth=1)
            # box.render(ax, view=camera_intrinsic, normalize=True, colors=(c, c, c))

    # Limit visible range.
    ax.set_xlim(-axes_limit, axes_limit)
    ax.set_ylim(-axes_limit, axes_limit)

    ax.axis('off')
    plt.tight_layout()
    ax.set_title('TOP')
    ax.set_aspect('equal')
    if out_path != None:
        fig.savefig(out_path)  # save the figure to file
        plt.close(fig)  # close the figure

path = '/media/aicore/Daten/aicore2TB/nuScenes/scenerio/pic'

num_scene = 0
for scene_rec in nusc.scene:
    num_scene += 1
    os.mkdir(os.path.join(path, '%03d'%num_scene))
    scene_name = scene_rec['name']
    first_sample_token = scene_rec['first_sample_token']
    last_sample_token = scene_rec['last_sample_token']
    sample_token = first_sample_token
    count = 0
    while sample_token != last_sample_token:
        sample = nusc.get('sample', sample_token)
        count+=1
        render_sample_labelonly(sample, out_path=path + '/%03d/sample%02d.png' % (num_scene, count))
        sample_token = sample['next']
    # cmd = ['ffmpeg', '-framerate', '1', '-i', path+'/temp/sample%02d.png',
    #     '-r', '1', '-crf', '15', '-b', '10M',
    #     '-pix_fmt', 'yuv420p',
    #     path+'/%s.mp4'%scene_name]
    # subprocess.call(' '.join(cmd), shell=True)
    # for file_name in glob.glob(path+"/temp/*.png"):
    #     os.remove(file_name)

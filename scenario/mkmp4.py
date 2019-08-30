
from nuscenes.utils.geometry_utils import view_points, box_in_image, BoxVisibility
print(BoxVisibility.ANY)
import os, sys, glob, gc
import subprocess


dir_label = '/media/aicore/Daten/aicore2TB/nuScenes/scenerio/scenes_label/temp'
dir_no_label = '/media/aicore/Daten/aicore2TB/nuScenes/scenerio/scenes/temp'

def make_video(scene_name, label):
    if label:
        #os.chdir(dir_label)
        d = dir_label
        file_name = 'scenes_label'
    else:
        #os.chdir(dir_no_label)
        d = dir_no_label
        file_name = 'scenes'
    cmd = ['ffmpeg', '-framerate', '1', '-i', d+'/sample%02d.png',
        '-r', '1', '-crf', '15', '-b', '10M',
        '-pix_fmt', 'yuv420p',
        '/media/aicore/Daten/aicore2TB/nuScenes/scenerio/%s/%s.mp4'%(file_name, scene_name)]
    print(' '.join(cmd))

    subprocess.call(' '.join(cmd), shell=True)
    for file_name in glob.glob("*.png"):
        os.remove(file_name)


make_video('test', True)
make_video('test', False)
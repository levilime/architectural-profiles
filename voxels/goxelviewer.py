import numpy as np
from pyvox.models import Vox
from pyvox.writer import VoxWriter
from subprocess import call

from voxels.magicavoxwrapper import export


def visualize_voxel(array, filename="temp.vox"):
    export(array, filename)
    open_voxel("goxel.exe", filename)


def open_voxel(program_path, voxel_path):
    call([program_path, voxel_path])




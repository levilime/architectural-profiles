import numpy as np
from pyvox.models import Vox
from pyvox.parser import VoxParser
from pyvox.writer import VoxWriter
from subprocess import call, check_output


def visualize_voxel(array, filename="temp.vox"):
    export(array, filename)
    open_voxel("MagicaVoxel-0.99.1-alpha-mac/MagicaVoxel.app", filename)


# array: (x,z,y)
def export(array, filename):
    M = np.copy(array)
    # M = np.rot90(M, 2, (0,1))
    vox = Vox.from_dense(M)
    VoxWriter(filename, vox).write()


def import_voxel(path):
    return Vox.to_dense(VoxParser(path).parse())


def open_voxel(magica_program_path, voxel_path):
    call([magica_program_path, voxel_path])




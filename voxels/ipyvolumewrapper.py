import numpy as np
import ipyvolume as ipv
from itertools import product


def color_converter(num):
    return 0.9, 0.9, 0.9


def is_empty(num):
    return not (num == 252 or num == 17 or num == 246)


def corners_of_viewbox(array):
    max_shape = int(np.max(array.shape))
    return list(product(*[[0, max_shape]] * 3))


def visualize_voxel(array, width=500, height=400):
    fig = ipv.figure(width=width, height=height)
    ipv.pylab.style.box_off()
    ipv.pylab.style.axes_off()
    ipv.style.use('nobox')
    fig.scatter = get_view_object(array)
    return ipv.gcc()


def get_view_object(array):
    array = np.rot90(array, 2, (1, 2))
    it = np.nditer(array, flags=['multi_index'])
    # go over all boxes
    x = []
    y = []
    z = []
    color = []
    while not it.finished:
        index = it.multi_index

        current_color = array[index]
        if not current_color or is_empty(current_color):
            it.iternext()
            continue
        x.append(index[0])
        y.append(index[1])
        z.append(index[2])
        color.append(color_converter(current_color))
        it.iternext()

    def convert_array(d):
        return np.asarray(d).astype(float)

    # add corners of viewbox because otherwise the scene is not uniformly scaled
    corners = corners_of_viewbox(array)
    x = x + list(map(lambda x: x[0], corners))
    y = y + list(map(lambda x: x[1], corners))
    z = z + list(map(lambda x: x[2], corners))
    color = color + [[1, 1, 1]] * len(corners)

    relative_size = int(np.max(array.shape) / 2)
    size_of_boxes = int(100 / np.max(array.shape))

    view_obj = ipv.scatter(convert_array(x), convert_array(y), convert_array(z),
                           size=size_of_boxes,
                           color=color,
                           marker="box")
    return view_obj


def create_temporary_images():
    import ipywidgets
    from IPython.display import display
    from ipyvolume.pylab import gcf, view, savefig
    import os

    def _change_azimuth_angle(fig, frame, fraction):
        with fig:
            view(azimuth=fraction * 360)

    fps = 20
    frames = 10
    endpoint = False
    function = _change_azimuth_angle
    import tempfile
    tempdir = tempfile.mkdtemp()
    print(tempdir)
    output = ipywidgets.Output()
    display(output)
    fig = gcf()
    for i in range(frames):
        with output:
            fraction = i / (frames - 1. if endpoint else frames)
            function(fig, i, fraction)
            frame_filename = os.path.join(tempdir, "frame-%05d.png" % i)
            savefig(frame_filename, output_widget=output)
    return tempdir


def create_movie(filename="temp.gif"):
    import imageio
    import os
    tempdir = create_temporary_images()
    images = []
    image_locations = [os.path.join(tempdir, file) for file in os.listdir(tempdir)]
    print(tempdir)
    print(image_locations)
    for filename in image_locations:
        images.append(imageio.imread(filename))

    imageio.mimsave(filename, images)


def create_movie_from_image_dir(tempdir, output_filename="temp.gif"):
    import imageio
    import os
    images = []
    image_locations = [os.path.join(tempdir, file) for file in os.listdir(tempdir)]
    for filename in image_locations:
        images.append(imageio.imread(filename))
    imageio.mimsave(output_filename, images)

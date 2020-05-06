import os
from PIL import Image
from functools import reduce
import numpy as np
import random

from solving.util import compare_textures

class Texture:

    def __init__(self, name, img, transformation):
        self.img = img
        # FIXME hardcoded right now, take dimensions from img
        self.block_size = {"x": 16,"y": 16}
        self.transformation = transformation
        # convention: x, -x, y, -y, z, -z
        # only the 2d case right now
        # x = right, -x = left, y = up, -y = down
        self.constraints = {"x": {}, "-x": {}, "y": {}, "-y": {}}

        arr = np.asarray(self.transformed_image())
        # FIXME can replace arr.shape[0]-1 by -1
        self.edges = {"x": arr[:,arr.shape[0]-1],"-x": arr[:,0],"y": arr[0], "-y": arr[arr.shape[1]-1]}
        self.id = name + "A" + reduce(lambda agg, key: agg + key + str(transformation[key]), transformation.keys(), '')

    def add_constraint(self, edge, texture):
        self.constraints[edge][texture.id] = texture

    def transformed_image(self):
        copy_image = self.img.copy()
        if 'rotation' in self.transformation:
            copy_image = copy_image.rotate(self.transformation['rotation'])
        if 'hflip' in self.transformation and self.transformation['hflip'] == 1:
            copy_image = copy_image.transpose(Image.FLIP_LEFT_RIGHT)
        return copy_image

    def show(self):
        return self.transformed_image()

    def show_with_constraints(self):
        biggest_constraint_list_len = 0
        for dimension in self.constraints:
            for constraint_dim in self.constraints[dimension]:
                if biggest_constraint_list_len < len(constraint_dim):
                    biggest_constraint_list_len = len(constraint_dim)
        amount_blockspace_per_item = 3
        img = Image.new('RGB', (self.block_size['x'] * amount_blockspace_per_item  * len(self.constraints),
                                self.block_size['y'] * amount_blockspace_per_item  * biggest_constraint_list_len), color=(255, 255, 255))
        y_count = 0
        x_count = 0
        b_x  = self.block_size['x'] * amount_blockspace_per_item
        b_y = self.block_size['y'] * amount_blockspace_per_item
        for dimension in self.constraints:
            for constraint_dim in self.constraints[dimension]:
                xx = x_count * amount_blockspace_per_item * self.block_size["x"] + self.block_size["x"]
                yy = y_count * amount_blockspace_per_item * self.block_size["y"]  + self.block_size["y"]
                placement = (xx, yy, xx + self.block_size["x"], yy + self.block_size["y"])
                # reference image
                img.paste(
                    Image.new('RGB', (b_x,
                                      b_y),
                              color=tuple(map(lambda x: random.randint(0, 255), range(0, 3)))),
                    (x_count * b_x, y_count * b_y, x_count * b_x + b_x, y_count * b_y + b_y)
                )
                img.paste(
                    self.show(), placement
                )
                constraint_map = {
                    "x": (self.block_size["x"], 0, self.block_size["x"], 0),
                    "-x": (-self.block_size["x"], 0, - self.block_size["x"], 0),
                    "-y": (0, self.block_size["y"], 0, self.block_size["y"]),
                    "y": (0 ,  - self.block_size["y"], 0, -self.block_size["y"])
                }
                proper_constraint = constraint_map[dimension]
                # constraint
                img.paste(
                    self.constraints[dimension][constraint_dim].show(), tuple(map(lambda t: t[0] + t[1], list(zip(placement, proper_constraint))))
                )
                x_count = x_count + 1
            x_count = 0
            y_count = y_count + 1
        img.show()
        return img


class ConstraintsFromPixels:

    def __init__(self, folder):
        default_transform = {'rotation': 0}
        texture_folder = os.path.join(folder, 'imgs')
        textures = list(map(lambda file: (file.split('.')[0], Image.open(os.path.join(texture_folder, file))), os.listdir(texture_folder)))
        # create map
        texture_map = {}
        for texture in textures:
            texture_map[texture[0]] = texture[1]
        instructions = self.read_instructions(os.path.join(folder, 'instruction.txt'))
        aggregated_textures = [
            {"key": key, "img": texture_map[key],
                    "instructions": instructions[key] if key in instructions else [default_transform]}
            for key in texture_map.keys()]
        textures = []
        for agg_texture in aggregated_textures:
            for instruction in agg_texture['instructions']:
                textures.append(Texture(agg_texture['key'], agg_texture['img'], instruction))

        # add constraint for every texture
        for texture_subject in textures:
            for texture_sample in textures:
                d = compare_textures(texture_subject, texture_sample)
                for dim in d.keys():
                    if d[dim]:
                        texture_subject.add_constraint(dim, texture_sample)
        self.realized_textures = textures

    def get_textures(self):
        return self.realized_textures

    def read_instructions(self, path):
        instructions = {}
        file = open(path, "r")
        for line in file:
            splitted_line = line.split(":")
            element = splitted_line[0]
            rules = splitted_line[1].replace('\n','').split(',')
            transformations = []
            # these rules are for the 2D case
            for rule in rules:
                new_transforms = []
                if rule == "rotation":
                    for i in range(0,4):
                        new_transforms.append({"rotation": i * 90})

                if rule == "flip":
                    for i in range(0,2):
                        new_transforms.append({"hflip": i})
                if not transformations:
                    transformations = new_transforms
                else:
                    aggregated_transforms = []
                    for existing_transform in transformations:
                        for new_transform in new_transforms:
                            aggregated_transform = dict(existing_transform)
                            aggregated_transform[list(new_transform.keys())[0]] = list(new_transform.values())[0]
                            aggregated_transforms.append(aggregated_transform)

                    transformations = aggregated_transforms
            instructions[element] = transformations
        return instructions


# c = ConstraintsFromPixels('../imgs/simplestplan')
# for texture in c.realized_textures:
#     texture.show_with_constraints()

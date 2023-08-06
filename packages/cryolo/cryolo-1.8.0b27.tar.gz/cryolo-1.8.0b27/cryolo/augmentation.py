"""
Author: Thorsten Wagner (thorsten.wagner@mpi-dortmund.mpg.de)
"""
#
# COPYRIGHT
# All contributions by Thorsten Wagner:
# Copyright (c) 2017 - 2019, Thorsten Wagner.
# All rights reserved.
#
# ---------------------------------------------------------------------------
#         Do not reproduce or redistribute, in whole or in part.
#      Use of this code is permitted only under licence from Max Planck Society.
#            Contact us at thorsten.wagner@mpi-dortmund.mpg.de
# ---------------------------------------------------------------------------
#

import random
import numpy as np
from scipy import ndimage
from abc import ABC, abstractmethod
import copy

class AugmentationMethod(ABC):

    @abstractmethod
    def transform_image(self, image : np.array) -> np.array:
        pass

    @abstractmethod
    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        pass


class Rot90Augmentation(AugmentationMethod):

    def __init__(self, num_rotations : float):
        self.num_rotations = num_rotations

    def transform_image(self, image : np.array) -> np.array:

        if np.squeeze(image).shape[0] != np.squeeze(image).shape[1] and self.num_rotations % 2 != 0:
            raise ValueError("Rotational data augmentations failed. For non-square images the number of rotations needs even.")

        image = np.rot90(image, k=self.num_rotations, axes=(1, 0))
        return image

    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        object_coords_cpy = copy.deepcopy(object_coords)
        for obj in object_coords_cpy:
            hcenter = float(image_dims[1]) / 2
            wcenter = float(image_dims[0]) / 2

            for i in range(self.num_rotations):
                obj["xmin"] = obj["xmin"] - wcenter
                obj["xmax"] = obj["xmax"] - wcenter
                obj["ymin"] = obj["ymin"] - hcenter
                obj["ymax"] = obj["ymax"] - hcenter

                help = obj["xmin"]
                obj["xmin"] = -1 * obj["ymin"]
                obj["ymin"] = help

                help = obj["xmax"]
                obj["xmax"] = -1 * obj["ymax"]
                obj["ymax"] = help

                obj["xmin"] = obj["xmin"] + wcenter
                obj["xmax"] = obj["xmax"] + wcenter
                obj["ymin"] = obj["ymin"] + hcenter
                obj["ymax"] = obj["ymax"] + hcenter

                # Swap xmin and xmax
                help = obj["xmax"]
                obj["xmax"] = obj["xmin"]
                obj["xmin"] = help

                if "angle" in obj:
                    obj["angle"] = obj["angle"] + np.pi / 2
                    if obj["angle"] > np.pi:
                        obj["angle"] = obj["angle"] - np.pi

        return object_coords_cpy

class CustomRotationAugmentation(AugmentationMethod):

    def __init__(self, rotation_angle_rad : float):
        self.rotation_in_rad = rotation_angle_rad

    def transform_image(self, image : np.array) -> np.array:
        return ndimage.rotate(image, np.rad2deg(self.rotation_in_rad), reshape=False, mode='reflect', order=1)

    def transform_coords(self, object_coords : list, image_dims: list) -> list:
        hcenter = float(image_dims[1]) / 2
        wcenter = float(image_dims[0]) / 2
        object_coords_cpy = copy.deepcopy(object_coords)
        for obj in object_coords_cpy:
            # 1. calculate center coordinate of object
            rotational_center_x = wcenter
            rotational_center_y = hcenter
            center_x = obj["xmin"] + (obj["xmax"] - obj["xmin"]) / 2 - rotational_center_x
            center_y = obj["ymin"] + (obj["ymax"] - obj["ymin"]) / 2 - rotational_center_y

            # 2. rotate center point
            c, s = np.cos(-1*self.rotation_in_rad), np.sin(-1*self.rotation_in_rad)
            R = np.array(((c, -s), (s, c)))
            rot_point = R @ np.array([center_x, center_y])
            rot_point[0] = rot_point[0] + rotational_center_x
            rot_point[1] = rot_point[1] + rotational_center_y

            # 4. calculate new xmin/max
            boxw = obj["xmax"] - obj["xmin"]
            boxh = obj["ymax"] - obj["ymin"]
            obj["xmin"] = rot_point[0] - boxw / 2
            obj["xmax"] = rot_point[0] + boxw / 2
            obj["ymin"] = rot_point[1] - boxh / 2
            obj["ymax"] = rot_point[1] + boxh / 2

            # 3. update angle by adding rotation range c
            if "angle" in obj:
                obj["angle"] = obj["angle"] - self.rotation_in_rad
                while obj["angle"] < 0:
                    obj["angle"] = obj["angle"] + np.pi
        return object_coords_cpy

class FlipAugmentation(AugmentationMethod):

    FLIP_BOTH = 1
    FLIP_HORIZONTAL = 2
    FLIP_VERTICAL = 3

    def __init__(self, flipping_mode):
        if flipping_mode not in [0,1,2,3]:
            raise ValueError("Flipping mode is not supported")
        self.flipping_mode = flipping_mode


    def transform_image(self, image: np.array) -> np.array:

        if self.flipping_mode == self.FLIP_VERTICAL:
            image = np.flip(image, 1)
        if self.flipping_mode == self.FLIP_HORIZONTAL:
            image = np.flip(image, 0)
        if self.flipping_mode == self.FLIP_BOTH:
            image = np.flip(np.flip(image, 0), 1)

        return image

    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        '''

        :param object_coords:
        :param image_dims: list of image width and image height
        :return:
        '''

        object_coords_cpy = copy.deepcopy(object_coords)
        for obj in object_coords_cpy:
            if self.flipping_mode == self.FLIP_VERTICAL or self.flipping_mode == self.FLIP_BOTH:
                xmin = obj["xmin"]
                obj["xmin"] = image_dims[0] - obj["xmax"]
                obj["xmax"] = image_dims[0] - xmin

            if self.flipping_mode == self.FLIP_HORIZONTAL or self.flipping_mode == self.FLIP_BOTH:
                ymin = obj["ymin"]
                obj["ymin"] = image_dims[1] - obj["ymax"]
                obj["ymax"] = image_dims[1] - ymin

            if "angle" in obj and (self.flipping_mode in [self.FLIP_HORIZONTAL, self.FLIP_VERTICAL]):
                # in case of flip_both the direction doesnt change...
                obj["angle"] = np.pi - obj["angle"]

        return object_coords_cpy

class Augmentation:
    """
    Class for doing data augmentation
    """

    def __init__(self, is_grey=False):
        self.is_grey = is_grey

    def image_augmentation(self, image):
        """
        Applies random selection of data augmentations
        :param image:  Input image
        :return: Augmented image
        """
        augmentations = [
            self.additive_gauss_noise,
            self.add,
            self.contrast_normalization,
            self.multiply,
            self.dropout,
        ]

        num_augs = np.random.randint(0, np.minimum(6, len(augmentations)))
        if num_augs > 0:

            if np.random.rand() > 0.5:
                augmentations.append(self.gauss_blur)
            else:
                augmentations.append(self.avg_blur)

            selected_augs = random.sample(augmentations, num_augs)
            image = image.astype(np.float32, copy=False)
            for sel_aug in selected_augs:
                image = sel_aug(image)
            #   print "Mean after", sel_aug, " sum: ", np.mean(image)
            if self.is_grey:
                min_img = np.min(image)
                max_img = np.max(image)
                image = ((image - min_img) / (max_img - min_img)) * 255
                #    image = np.clip(image, 0, 255)
                image = image.astype(np.uint8, copy=False)

        return image

    def gauss_blur(self, image, sigma_range=(0, 3)):
        """
        Applys gaussian blurring with random sigma
        :param image: Input image
        :param sigma_range:  Range for random sigma
        :return: Blurred image
        """
        rand_sigma = sigma_range[0] + np.random.rand() * (
            sigma_range[1] - sigma_range[0]
        )
        result = ndimage.gaussian_filter(
            image, sigma=rand_sigma, mode="nearest", output=image
        )

        if not np.issubdtype(image.dtype, np.float32):
            result = result.astype(np.float32, copy=False)
        return result

    def avg_blur(self, image, kernel_size=(2, 7)):
        """
        Applys average blurring with random kernel size
        :param image: Input image (numpy array)
        :param kernel_size: Range for random kernel size
        :return: Blurred image
        """
        rang_kernel_size = np.random.randint(kernel_size[0], kernel_size[1])
        image = ndimage.uniform_filter(
            image, size=rang_kernel_size, mode="nearest", output=image
        )
        return image

    def additive_gauss_noise(self, image, max_sigma_range_factor=0.05):
        """
        Add random gaussian noise to image
        :param image: Input image
        :param max_sigma_range_factor: Range for max_sigma_range. The standard deviation of the noise is
        choosen randomly depending on the standard deviation of the image.
        The choosen standard deviation for noise is between: 0 and  max_sigma_factor*6*np.std(image)
        :return:
        """

        width = 2 * 3 * np.std(image)
        max_sigma = width * max_sigma_range_factor
        rand_sigma = np.random.rand() * max_sigma
        noise = np.random.randn(image.shape[0], image.shape[1])

        # image = noise*rand_sigma + image

        np.multiply(noise, rand_sigma, out=noise)
        np.add(image, noise, out=image)

        if not np.issubdtype(image.dtype, np.float32):
            image = image.astype(np.float32, copy=False)

        return image

    def contrast_normalization(self, image, alpha_range=(0.5, 2.0)):
        """
        Spread or squeeze the pixel values.
        :param image: Input image
        :param alpha_range: Range for alpha. Alpha controlls the normalization.
        :return: Modified image
        """
        rand_multiplyer = alpha_range[0] + np.random.rand() * (
            alpha_range[1] - alpha_range[0]
        )
        middle = np.median(image)
        np.subtract(image, middle, out=image)
        np.multiply(rand_multiplyer, image, out=image)
        np.add(middle, image, out=image)

        return image

    def dropout(self, image, ratio=(0.01, 0.1)):
        """
        Set a random selection of pixels to the mean of the image
        :param image: Input image
        :param ratio: Range for random ratio
        :return: Modified image
        """
        if isinstance(ratio, float):
            rand_ratio = ratio
        else:
            rand_ratio = ratio[0] + np.random.rand() * (ratio[1] - ratio[0])
        mean_val = np.mean(image)
        drop = np.random.binomial(
            n=1, p=1 - rand_ratio, size=(image.shape[0], image.shape[1])
        )
        image[drop == 0] = mean_val

        return image

    def add(self, image, scale=0.05):
        """
        Adds a random constant to the image
        :param image: Input image
        :param scale: Scale for random constant. The random constant
        will be between 0 and scale*6*std(image)
        :return: Modified image
        """
        width = 2 * 3 * np.std(image)
        width_rand = scale * width
        rand_constant = (np.random.rand() * width_rand) - width_rand / 2
        np.add(image, rand_constant, out=image)

        return image

    def multiply(self, image, mult_range=(0.5, 1.5)):
        """
        Multipy the input image by a random float.
        :param image: Input image
        :param mult_range: Range for random multiplier
        :return: multiplied image
        """

        rand_multiplyer = mult_range[0] + np.random.rand() * (
            mult_range[1] - mult_range[0]
        )
        np.multiply(image, rand_multiplyer, out=image)
        return image

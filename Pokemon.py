import os
from os.path import join
import imageio
import numpy as np

class Pokemon:

    def __init__(self, name, number, type1, type2, page):
        # String
        self.name = name
        # String
        self.number = number
        # String
        self.type1 = type1
        # String or None
        self.type2 = type2
        # String representing pokemon's page that we scraped it's img from
        self.page = page
        # Numpy array to be loaded explicitly
        self.img = None

    def __repr__(self):
        repr = '{}: {}'.format(self.number, self.name)
        return repr
    
    def load_pic(self, folder):
        name = join(folder, self.name + ".png")
        try:
            img = imageio.imread(name)
            self.img = img
            return True
        except ValueError:
            print(self.name + " could not load its png pic")
            return False
    
    def make_data(self):
        """Turns Pokemon into tuple about itself"""
        if not self.img:
            raise ValueError("Need to load img first")

        type_tuple = (self.type1.lower(), self.type2.lower() if self.type2 else "None")
        return (self.name.lower, type_tuple, self.img)
    
    @classmethod
    def pad_data(self, img, max_w, max_h, white=255):
        """Zero pads an image to max_w and max_h with `white` values.  Tries to keep the img in the center of the padding."""
        offset = 0.1 # Found by testing :P
        pad = (max_w - img.shape[0], max_h - img.shape[1])
        # Breaks ties by taking lesser amount on left side of pad
        pad_width = [(p // 2, round(p / 2 + offset)) for p in pad] + [(0, 0)]
        new_img = np.pad(img, pad_width=tuple(pad_width), mode='constant', constant_values=white)

        # For debugging
        if new_img.shape != (max_w, max_h, 3):
            print(img.shape)
        return new_img

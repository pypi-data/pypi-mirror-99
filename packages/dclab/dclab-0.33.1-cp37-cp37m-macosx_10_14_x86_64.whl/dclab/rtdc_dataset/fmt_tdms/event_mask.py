"""Class for on-the-fly conversion of contours to masks"""

import numpy as np
import scipy.ndimage as ndi


class MaskColumn(object):
    def __init__(self, rtdc_dataset):
        """Computes mask from contour data"""
        self.contour = rtdc_dataset["contour"]
        self.image = rtdc_dataset["image"]
        self.identifier = self.contour.identifier
        self.config = rtdc_dataset.config
        self._shape = None

    def __getitem__(self, idx):
        mask = np.zeros(self._img_shape, dtype=bool)
        conti = self.contour[idx]
        mask[conti[:, 1], conti[:, 0]] = True
        ndi.morphology.binary_fill_holes(mask, output=mask)
        return mask

    def __len__(self):
        if self._img_shape != (0, 0):
            lc = len(self.contour)
        else:
            lc = 0
        return lc

    @property
    def _img_shape(self):
        if self._shape is None:
            cfgim = self.config["imaging"]
            if self.image:
                # get shape from image column
                self._shape = self.image.shape
            elif "roi size x" in cfgim and "roi size y" in cfgim:
                # get shape from config (this is less reliable than getting
                # the shape from the image; there were measurements with
                # wrong config keys)
                self._shape = (cfgim["roi size y"], cfgim["roi size x"])
            else:
                # no shape available
                self._shape = (0, 0)
        return self._shape

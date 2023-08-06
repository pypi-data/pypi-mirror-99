import imageio
import numpy as np
from skimage import img_as_ubyte


class GifWriter:
    def __init__(self, path, fps=30):
        self.images = []
        self.path = path
        self.fps = fps

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        imageio.mimsave(self.path, self.images, fps=self.fps)

    def record(self, obj: np.ndarray) -> None:
        objc = obj.copy()
        objc[:] = obj[:]
        objc = (objc - objc.min()) / (objc.max() - objc.min())
        objc = objc.astype(np.float32)
        objc = img_as_ubyte(objc)
        self.images.append(objc)
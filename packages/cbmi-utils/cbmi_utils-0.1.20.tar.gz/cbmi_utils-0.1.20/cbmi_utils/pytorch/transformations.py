import torchvision.transforms.functional as functional
import random
from typing import Sequence


# from: https://github.com/pytorch/vision/issues/566#issuecomment-535854734
class RotateTransform:
    def __init__(self, angles: Sequence[int]):
        self.angles = angles

    def __call__(self, x):
        angle = random.choice(self.angles)
        return functional.rotate(x, angle)

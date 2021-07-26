# AUTOGENERATED! DO NOT EDIT! File to edit: 00_attractor.ipynb (unless otherwise specified).

__all__ = ['Attractor', 'rotation_matrix', 'rotate', 'RouletteCurve']
# Cell

# %matplotlib widget
import IPython
# IPython.get_ipython().run_line_magic('matplotlib', 'widget')
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import numba as nb
import math
import random
import time
from scipy import signal, misc

# Cell

class Attractor:
    def __init__(self):
        pass

@nb.njit
def rotation_matrix(a):
    sin = np.sin(a)
    cos = np.cos(a)
    R = [
        [cos, -sin],
        [sin, cos]
    ]
    return np.array(R)

@nb.njit
def rotate(a, b, t):
#         if type(t) in [int, float]:
#         if isinstance(t, (int, float)):
    t = rotation_matrix(t)

#         return (rMatrix @ (a - b)) + b
    return (t @ (a - b)) + b

# Cell

@nb.njit
def simulate_accelerated(speeds, pivots, center, angles, start, points, steps=100, clip=True):
#     todo: reuse code
    rMatrices = []
    for s in speeds:
        rMatrices.append(rotation_matrix(s))
    num_pivots = len(pivots)
    for s in range(steps):
        for l in list(range(num_pivots)):
            rMatrix = rMatrices[l]
            offsets = center if l == 0 else pivots[l-1]
            angles[l:] += speeds[l]
            if clip:
                angles[l:] %= 2 * math.pi
        prev = rotate(start[0], center, angles[0])
        for p in range(1, num_pivots):
            pivots[p] = rotate(start[p], center, angles[p]) + prev
            prev = pivots[p]
#         if self.live_rendering:
#             self.draw_point(self.pivots[-1].copy(), 'pixel')
#         else:
        points = np.append(points, np.expand_dims(pivots[-1], axis=0), axis=0)
    return points
# dynamic wrappers for Numba functions

# Cell

# @nb.jit
class RouletteCurve(Attractor):
    def __init__(self, center=[0, 0], num_sections=4, lengths=None, speeds=None, random_distribution='uniform'):
        """
        Create a new `RouletteCurve` object. This subclasses `Attractor` and describes a process where one or more line segments, connected end-to-end, rotate continuously about their pivots/endpoints. The length of each line segment and the speed at which it rotates are adjustable parameters.
        """
        super().__init__()
        self.random_distribution = getattr(np.random, random_distribution)
        self.rd = self.random_distribution
        self.center = np.array(center)
        self.rank = self.center.size
#         use rank?
        if lengths is None:
            lengths = np.random.uniform(0, 1, num_sections)
        if speeds is None:
            speeds = np.random.normal(0, 1, num_sections)
        self.lengths = RouletteCurve.randomize_list(lengths).astype(float)
        self.speeds = RouletteCurve.randomize_list(speeds).astype(float)
#         self.angles = np.random.normal(0, 2*math.pi, num_sections).astype(float)
        self.angles = np.zeros(num_sections, dtype=float)
        self.angles_ = []
        self.start = center + np.array([[0, sum(self.lengths[:i])] for i in range(1, len(self.lengths)+1)])
        self.start = self.start.astype(float)
        self.pivots = self.start.copy()
        self.pivots_ = []
        self.points = []
        self.canvas = np.zeros([100, 100])
        self.position = 0

        self.zoom = 10
        self.offset = 0
        self.N = 0
        self.live_rendering = False

#         See colormaps by category at https://matplotlib.org/stable/tutorials/colors/colormaps.html; used here are the "sequential" cmaps and a few others
        self.cmaps = ['inferno', 'plasma', 'rainbow', 'hot', 'cool', 'autumn', 'winter', 'summer'] + [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

    def clear(self):
        """
        Remove all generated points from this `Attractor`
        """
        self.points = np.zeros([1, 2])
        return self

    @nb.jit(forceobj=True)
    def simulate(self, steps=1, clip=True):
    def get_state(self):
        """
        Internal/helper function; gets current values of this instance's speeds, pivots, angles, etc. as a dictionary (mainly for use in typed functions like simulate_accelerated)
        """
        return dict(
            speeds=self.speeds,
            pivots=self.pivots,
            center=self.center,
            angles=self.angles,
            start=self.start,
            points=self.points
        )
        rMatrices = []
        for s in self.speeds:
#             theta = 1 * self.speeds[l]
            rMatrices.append(rotation_matrix(s))

        for s in range(steps):
            last = self.pivots.copy()
#             for l in list(range(len(self.pivots)))[::-1]:
            gamma = 0
            num_pivots = len(self.pivots)
            for l in list(range(num_pivots)):
#             theta = 1 * self.speeds
                rMatrix = rMatrices[l]
#                 rMatrix = np.array(rMatrix)#.swapaxes(0,2)
                offsets = self.center if l == 0 else last[l-1]#.copy() #?
#                 for f in list(range(l, num_pivots)):
    #                 print(s, rMatrix)
        #             print(self.pivots[:-1].shape)
    #                 offsets = np.concatenate([self.center[np.newaxis,...], self.pivots[:-1]], axis=0)
    #                 offsets=np.array(0)
    #                 len(self.pivots)-1
    #                 print(offsets)
        #             print(offsets.shape, rMatrix.shape, self.pivots.shape)
    #                 self.pivots[l] = (last[l] - offsets) @ rMatrix + offsets

    #                 func of t?
    #                 delta = (last[l] - offsets) @ rMatrix + offsets
#                     delta = (rMatrix @ (self.pivots[f] - offsets)) + offsets# + gamma
    #                 print(delta)
#                     gamma += delta
#                     self.pivots[f] = delta

                self.angles[l:] += self.speeds[l]
                if clip:
                    self.angles[l:] %= 2 * math.pi
                self.angles_.append(self.angles.copy())

    #             self.points.append(np.clip(self.pivots[-1], 0, np.array(self.canvas.shape)))
#     sequencemethod

            prev = rotate(self.start[0], self.center, self.angles[0])
            for p in range(1, num_pivots):
#                 print(p, prev)
                self.pivots[p] = rotate(self.start[p], self.center, self.angles[p]) + prev
                prev = self.pivots[p]
            self.pivots_.append(self.pivots.copy())
            self.points.append(self.pivots[-1].copy())
        return self

#     @nb.jit(forceobj=True)
    def render(self, recenter=True, zoom=None, mode='dist'):
        cshape = np.array(self.canvas.shape)
        self.offset = cshape / 2
        if not self.live_rendering:# and (self.points):
            if zoom is None:
                zoom = np.min(cshape / np.max(np.abs(self.points), axis=0)) * 0.5
            self.zoom = zoom
#         for p in self.points.copy():
        if mode == 'dist':
#             grid = np.stack(np.meshgrid([np.arange(5.)]*2))
            grid = np.mgrid[0:5, 0:5]
            brush = 1 / np.linalg.norm(grid - 2.5, axis=0)
            print(brush)
        for i, p in enumerate(map(np.copy, self.points)):
#             for j, p in enumerate(px):
            p = p.astype(float)
            p *= zoom
            if recenter:
                p += offset
            p = np.clip(p, 0, np.array(self.canvas.shape)-1)
            w, h = self.canvas.shape
            x, y = p.astype(int)
            if mode == 'pixel':
                self.canvas[x, y] += 1
            elif mode == 'dist':
                x, y = np.clip(x, 5, w-6), np.clip(y, 5, h-6)
                self.canvas[x-2:x+3, y-2:y+3] += brush
#                 self.canvas[x, y] = j+1
#         plt.style.use('fivethirtyeight')
        plt.style.use('classic')
        P = plt.imshow(np.flip(self.canvas.T, axis=0), interpolation='none')
        plt.grid('off')
        return P
#         return self

    @staticmethod
    def randomize_list(L):
        return np.array([self.rd(*x) if type(x) in [list, tuple] else x for x in L])
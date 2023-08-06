"""Ground projection axis module."""

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.axes import Axes
from matplotlib.axis import XAxis, YAxis
from matplotlib.patches import PathPatch
from matplotlib.collections import LineCollection
from matplotlib.ticker import NullLocator, FixedLocator

from .transform import ProjTransform
from .ticks import lon_e_ticks, lat_ticks, km_ticks, km_s_ticks, deg_ticks, hr_ticks


PROPS = {
    'alt': ('Altitude', km_ticks),
    'dist': ('Distance', km_ticks),
    'local_time': ('Local time', hr_ticks),
    'inc': ('Incidence angle', deg_ticks),
    'emi': ('Emission angle', deg_ticks),
    'phase': ('Phase angle', deg_ticks),
    'solar_zenith_angle': ('Solar zenith angle', deg_ticks),
    'solar_longitude': ('Seasonal solar longitude', deg_ticks),
    'true_anomaly': ('True anomaly angle', deg_ticks),
    'groundtrack_velocity': ('Groundtrack velocity', km_s_ticks),
}


class ProjAxes(Axes):
    """An abstract base class for geographic projections."""

    def __init__(self, *args, proj='equi', bg=None, bg_extent=False, **kwargs):
        self.proj = proj
        self.bg = bg
        self.bg_extent = bg_extent

        super().__init__(*args, **kwargs)

    def _init_axis(self):
        self.xaxis = XAxis(self)
        self.yaxis = YAxis(self)
        self._update_transScale()

    def cla(self):
        """Clear axes."""
        Axes.cla(self)
        self.set_aspect(1)

        self.xaxis.set_minor_locator(NullLocator())
        self.yaxis.set_minor_locator(NullLocator())

        self.set_longitude_grid(30)
        self.set_latitude_grid(30)

        self.set_background()
        self.grid(lw=.5, color='k')

        Axes.set_xlim(self, *self.proj.extent[:2])
        Axes.set_ylim(self, *self.proj.extent[2:])

    def _get_core_transform(self):
        return ProjTransform(self.proj)

    def plot(self, *args, scalex=True, scaley=True, data=None, **kwargs):
        """Generic plot function with projection."""
        if hasattr(args[0], 'lonlat'):
            traj = args[0]

            if len(args) > 1 and isinstance(args[1], str):
                attr = args[1].lower().replace(' ', '_')
                if hasattr(traj, attr):
                    values = getattr(traj, attr)

                    x, y, data = self.proj.xy_plot(*traj.lonlat, values=values)

                    label, fmt = PROPS.get(attr, (None, None))
                    kwargs = {'label': label, 'fmt': fmt, **kwargs}

                    return self.plot_colorline(x, y, data, **kwargs)

            x, y = self.proj.xy_plot(*traj.lonlat)
            args = args[1:]

        elif len(args[0]) == 2 and isinstance(args[0], tuple) and np.ndim(args[0]) == 2:
            x, y = self.proj.xy_plot(*args[0])
            args = args[1:]

        elif len(args) > 2 and '.' not in args[2] and 'o' not in args[2]:
            x, y = self.proj.xy_plot(*args[:2])
            args = args[2:]

        else:
            x, y = self.proj.xy(*args[:2])
            args = args[2:]

        return super().plot(x, y, *args,
                            scalex=scalex, scaley=scaley, data=data, **kwargs)

    def plot_colorline(self, x, y, data, cmap='turbo_r', vmin=None, vmax=None,
                       linewidth=1.5, label=None, fmt=None, orientation='horizontal'):
        """Plot a colored line."""
        points = np.transpose([x, y]).reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        data = np.array(data)
        values = .5 * (data[1:] + data[:-1])

        if vmin is None:
            vmin = np.nanmin(data)
        if vmax is None:
            vmax = np.nanmax(data)

        norm = plt.Normalize(vmin, vmax)

        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(values)
        lc.set_linewidth(linewidth)

        line = super(Axes, self).add_collection(lc)  # pylint: disable=bad-super-call

        # Colorbar extend is based on the data range
        cmin = np.nanmin(data) < vmin
        cmax = np.nanmax(data) > vmax

        extend = 'both' if cmin and cmax else 'min' \
            if cmin else 'max' if cmax else 'neither'

        return plt.colorbar(
            line, ax=self,
            extend=extend,
            shrink=.6,
            aspect=40,
            pad=0.05,
            orientation=orientation,
            format=fmt,
            label=label,
        )

    def add_path(self, path, *args, **kwargs):
        """Draw path."""
        self.add_patch(PathPatch(path, *args, **kwargs))

    def add_patch(self, p):
        """Draw patch."""
        super().add_patch(self.proj.xy_patch(p))

    def add_collection(self, collection, autolim=True):
        """Draw patches collection."""
        super().add_collection(self.proj.xy_collection(collection), autolim=autolim)

    def set_longitude_grid(self, degrees):
        """Set the number of degrees between each longitude grid."""
        grid = np.linspace(0, 360, int(360 / degrees) + 1).astype(int)
        self.xaxis.set_major_locator(FixedLocator(grid))
        self.xaxis.set_major_formatter(lon_e_ticks)

    def set_latitude_grid(self, degrees):
        """Set the number of degrees between each longitude grid."""
        grid = np.linspace(-90, 90, int(180 / degrees) + 1).astype(int)
        self.yaxis.set_major_locator(FixedLocator(grid))
        self.yaxis.set_major_formatter(lat_ticks)

    def set_background(self):
        """Set image basemap background."""
        if self.bg:
            im = plt.imread(self.bg)
            self.imshow(im, extent=self.bg_extent, cmap='gray')

    # def imshow(self, X, extent=None, **kwargs):
    #     """Display data as an image.

    #     Parameters
    #     ----------
    #     X : array-like or PIL image
    #         The image data. Supported array shapes are:

    #         - (M, N): an image with scalar data. The values are mapped to
    #           colors using normalization and a colormap. See parameters *norm*,
    #           *cmap*, *vmin*, *vmax*.
    #         - (M, N, 3): an image with RGB values (0-1 float or 0-255 int).
    #         - (M, N, 4): an image with RGBA values (0-1 float or 0-255 int),
    #           i.e. including transparency.

    #         The first two dimensions (M, N) define the rows and columns of
    #         the image.

    #         Out-of-range RGB(A) values are clipped.

    #     extent: floats (left, right, bottom, top), optional
    #         The bounding box in data coordinates that the image will fill.
    #         The image is stretched individually along x and y to fill the box.

    #     **kwargs: matplotlib.Axes.imshow
    #         Axes optional properties

    #     Raises
    #     ------
    #     ValueError:
    #         If the image dimensions are invalid (2D and 3D array only).

    #     """
    #     if np.ndim(X) == 2:
    #         h, w = np.shape(X)
    #     elif np.ndim(X) == 3:
    #         h, w, _ = np.shape(X)
    #     else:
    #         raise ValueError(f'Image invalid dimensions: `{np.ndim(X)}`')

    #     return super().imshow(X, extent=extent, **kwargs)

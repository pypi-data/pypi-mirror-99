"""Trajectory calculation module."""

import numpy as np

from .mask_traj import MaskedTrajectory

from ..math.vectors import angle, norm, ell_norm
from ..misc import cached_property, logger
from ..spice import SPICEPool, SPICERef, et, utc
from ..spice.toolbox import (
    illum_angles, groundtrack_velocity, local_time, obs_state,
    rlonlat, solar_longitude, sub_obs_pt, sun_pos, true_anomaly
)


log_traj, debug_trajectory = logger('Trajectory')


class Trajectory:  # pylint: disable=too-many-public-methods
    """Trajectory calculation object.

    Parameters
    ----------
    kernels: str or tuple
        List of kernels to be loaded in the SPICE pool.

    observer: str or spice.SPICERef
        Observer SPICE reference.

    observer: str or spice.SPICERef
        Target SPICE reference.

    ets: float or str or list
        Ephemeris time(s).

    abcorr: str, optional
        Aberration corrections to be applied when computing
        the target's position and orientation.
        Only the SPICE keys are accepted.

    """

    def __init__(self, kernels, observer, target, ets, abcorr='NONE'):
        self.kernels = kernels

        # Init SPICE references
        self.observer = observer if isinstance(observer, SPICERef) else SPICERef(observer)
        self.target = target if isinstance(target, SPICERef) else SPICERef(target)

        # Init ephemeris times
        self.ets = ets

        # Optional parameters
        self.abcorr = abcorr

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}> '
            f'Observer: {self.observer} | '
            f'Target: {self.target}'
            f'\n - Start time: {self.start}'
            f'\n - Stop time: {self.stop}'
            f'\n - Nb of pts: {len(self)}'
        )

    def __len__(self):
        return len(self.ets)

    def __and__(self, other):
        """And ``&`` operator."""
        return self.mask(self.intersect(other))

    def __xor__(self, other):
        """Hat ``^`` operator."""
        return self.mask(self.intersect(other, outside=True))

    @property
    def kernels(self):
        """Get the list of kernels to used."""
        return self.__kernels

    @kernels.setter
    def kernels(self, kernels):
        """List of kernels setter.

        Note
        ----
        SPICE pool content is checked to see if
        all the kernels are correctly loaded.
        If it's not the case, the pool will
        be purge and refilled.

        """
        self.__kernels = kernels

        if SPICEPool != kernels:
            log_traj.info('Load the kernels to the pool.')
            SPICEPool.add(kernels, purge=True)

    @property
    def ets(self):
        """Ephemeris times."""
        return self.__ets

    @ets.setter
    def ets(self, ets):
        """Ephemeris times setter."""
        log_traj.debug('Init ephemeris time.')

        if isinstance(ets, str):
            self.__ets = np.array([et(ets)])
        elif isinstance(ets, (int, float)):
            self.__ets = np.array([ets])
        elif isinstance(ets, (tuple, list, np.ndarray)):
            self.__ets = np.array(sorted([
                et(t) if isinstance(t, str) else t for t in ets]))
        else:
            raise ValueError('Invalid input Ephemeris Time(s).')

    @cached_property
    def utc(self):
        """UTC times."""
        log_traj.info('Compute UTC times.')
        return utc(self.ets)

    @property
    def start(self):
        """UTC start time."""
        return utc(self.ets[0])

    @property
    def stop(self):
        """UTC stop time."""
        return utc(self.ets[-1])

    @property
    def abcorr(self):
        """SPICE aberration correction."""
        return self.__abcorr

    @abcorr.setter
    def abcorr(self, key):
        """SPICE aberration correction setter."""
        if key.replace(' ', '').upper() not in [
            'NONE', 'LT', 'LT+S', 'CN', 'CN+S',
            'XLT', 'XLT+S', 'XCN', 'XCN+S',
        ]:
            raise KeyError(f'Invalid aberration correction key:`{key}`')
        self.__abcorr = key.upper()

    @cached_property
    def sub_obs_pts(self):
        """Sub-observer position vector.

        Returns
        -------
        np.ndarray
            Observer XYZ coordinates in the target body fixed frame
            (expressed in km).

        Note
        ----
        Currently the intersection method is fixed internally
        as ``method='NEAR POINT/ELLIPSOID'``.

        See Also
        --------
        Trajectory.lonlat
        Trajectory.rlonlat
        Trajectory.lon_e
        Trajectory.lat
        Trajectory.local_time
        Trajectory.illum_angles
        Trajectory.solar_zenith_angle

        """
        log_traj.info('Compute sub-observer points.')
        res = sub_obs_pt(
            self.ets,
            self.observer,
            self.target,
            abcorr=self.abcorr,
            method='NEAR POINT/ELLIPSOID')

        log_traj.debug('Result: %r', res)
        return res

    @cached_property(parent='sub_obs_pts')
    def sub_obs_rlonlat(self):
        """Sub-observer coordinates.

        Returns
        -------
        np.ndarray
            Sub-observer planetocentric coordinates:
            radii, east longitudes and longitudes.

        Note
        ----
        Currently the intersection method is fixed internally
        as ``method='NEAR POINT/ELLIPSOID'``.

        See Also
        --------
        Trajectory.sub_obs_pts
        Trajectory.lon_e
        Trajectory.lat

        """
        log_traj.debug('Compute sub-observer point in planetocentric coordinates.')
        return rlonlat(self.sub_obs_pts)

    @property
    def sub_obs_lon_e(self):
        """Sub-observer east longitude (degree)."""
        return self.sub_obs_rlonlat[1]

    @property
    def sub_obs_lat(self):
        """Sub-observer latitude (degree)."""
        return self.sub_obs_rlonlat[2]

    @property
    def lonlat(self):
        """Sub-observer ground track (degree)."""
        return self.sub_obs_rlonlat[1:]

    @cached_property(parent='sub_obs_rlonlat')
    def local_time(self):
        """Sub-observer local time (decimal hours).

        See Also
        --------
        Trajectory.sub_obs_rlonlat

        """
        log_traj.info('Compute sub-observer local time.')
        return local_time(self.ets, self.sub_obs_lon_e, self.target)

    @cached_property(parent='sub_obs_pts')
    def illum_angles(self):
        """Sub-observer illumination angles (degree).

        Incidence, emission and phase angles.

        See Also
        --------
        Trajectory.inc
        Trajectory.emi
        Trajectory.phase
        Trajectory.sub_obs_pts

        """
        log_traj.info('Compute sub-observer illumination geometry.')
        return illum_angles(
            self.ets,
            self.observer,
            self.target,
            self.sub_obs_pts,
            abcorr=self.abcorr,
            method='ELLIPSOID',
        )

    @property
    def inc(self):
        """Sub-observer incidence angle (degree)."""
        return self.illum_angles[0]

    @property
    def emi(self):
        """Sub-observer emission angle (degree)."""
        return self.illum_angles[1]

    @property
    def phase(self):
        """Sub-observer phase angle (degree)."""
        return self.illum_angles[2]

    @cached_property(parent='illum_angles')
    def day(self):
        """Day side.

        Mask on sub-observer incidence lower than 90°.

        """
        return self.inc <= 90  # pylint: disable=comparison-with-callable

    @property
    def night(self):
        """Night side.

        Mask on sub-observer incidence larger than 90°.

        """
        return ~self.day  # pylint: disable=invalid-unary-operand-type

    @cached_property
    def obs_state(self):
        """Spacecraft position and velocity in the target body fixed frame (km and km/s).

        See Also
        --------
        Trajectory.obs_pos
        Trajectory.alt

        """
        log_traj.info('Compute spacecraft position and velocity in the target frame.')
        res = obs_state(
            self.ets,
            self.observer,
            self.target,
            abcorr=self.abcorr)

        log_traj.debug('Result: %r', res)
        return res

    @property
    def obs_pos(self):
        """Observer position in the target body fixed frame (km).

        See Also
        --------
        Trajectory.dist
        Trajectory.alt

        """
        return self.obs_state[:3]

    @property
    def obs_velocity(self):
        """Observer velocity vector in the target body fixed frame (km/s).

        See Also
        --------
        Trajectory.obs_speed

        """
        return self.obs_state[3:]

    @cached_property(parent=('obs_state'))
    def obs_speed(self):
        """Observer speed in the target body fixed frame (km/s).

        See Also
        --------
        Trajectory.obs_velocity

        """
        return norm(self.obs_velocity.T)

    @cached_property(parent='obs_state')
    def dist(self):
        """Spacecraft distance to the target (km).

        This distance is computed to the center of the targeted body.

        See Also
        --------
        Trajectory.obs_pos
        Trajectory.alt

        """
        log_traj.debug('Compute observer distance in the target frame.')
        return norm(self.obs_pos.T)

    @cached_property(parent=('sub_obs_pts', 'obs_state'))
    def alt(self):
        """Spacecraft altitude to the sub-observer point (km).

        The intersect on the surface is computed on the reference
        ellipsoide.

        See Also
        --------
        Trajectory.sub_obs_pts
        Trajectory.obs_pos
        Trajectory.dist

        """
        log_traj.debug('Compute observer distance in the target frame.')
        return norm(self.obs_pos.T - self.sub_obs_pts.T)

    @cached_property(parent='obs_state')
    def groundtrack_velocity(self):
        """Compute the groundtrack velocity (km/s).

        It correspond to the motion speed of the sub-observer point
        on the surface.

        See Also
        --------
        Trajectory.obs_state
        Trajectory.obs_pos
        Trajectory.obs_velocity

        """
        log_traj.info('Compute ground track velocity.')
        res = groundtrack_velocity(self.target, self.obs_state)

        log_traj.debug('Result: %r', res)
        return res

    @cached_property
    def sun_pos(self):
        """Sun position in the target body fixed frame (km).

        Note
        ----
        Currently the intersection method is fixed on a sphere
        and the input time at the target center is not corrected
        from light travel.

        See Also
        --------
        Trajectory.sun_rlonlat
        Trajectory.sun_lon_e
        Trajectory.sun_lat
        Trajectory.sun_lonlat
        Trajectory.solar_zenith_angle

        """
        log_traj.info('Compute Sun coordinates in the target frame.')
        res = sun_pos(
            self.ets,
            self.target,
            abcorr=self.abcorr)

        log_traj.debug('Result: %r', res)
        return res

    @cached_property(parent='sun_pos')
    def sun_rlonlat(self):
        """Sub-solar coordinates.

        Returns
        -------
        np.ndarray
            Sub-solar planetocentric coordinates:
            radii, east longitudes and longitudes.

        See Also
        --------
        Trajectory.sun_pos
        Trajectory.sun_lon_e
        Trajectory.sun_lat
        Trajectory.sun_lonlat

        """
        log_traj.debug('Compute sub-solar point in planetocentric coordinates.')
        return rlonlat(self.sun_pos)

    @property
    def sun_lon_e(self):
        """Sub-solar point east longitude (degree)."""
        return self.sun_rlonlat[1]

    @property
    def sun_lat(self):
        """Sub-solar point latitude (degree)."""
        return self.sun_rlonlat[2]

    @property
    def sun_lonlat(self):
        """Sub-solar point ground track (degree)."""
        return self.sun_rlonlat[1:]

    @property
    def ss(self):
        """Alias on the sub-solar point groundtrack (degree)."""
        return self.sun_lonlat

    @cached_property(parent=('sub_obs_pts'))
    def ell_norm(self):
        """Sub-observer local normal.

        Unitary vector pointing upward from the surface of the ellipsoid.

        See Also
        --------
        Trajectory.sub_obs_pts

        """
        log_traj.debug('Compute sub-observer local normal.')
        res = ell_norm(self.sub_obs_pts.T, self.target.radii).T

        log_traj.debug('Result: %r', res)
        return res

    @cached_property(parent=('sub_obs_pts', 'sun_pos', 'ell_norm'))
    def solar_zenith_angle(self):
        """Sub-observer solar zenith angle (degree).

        The angle is computed from the local normal
        on the ellipsoid. If the targeted body is a sphere,
        this value much be equal to the incidence angle.

        See Also
        --------
        Trajectory.sun_pos
        Trajectory.sub_obs_pts
        Trajectory.ell_norm

        """
        log_traj.debug('Compute sub-observer solar zenith angle.')
        res = angle(self.sun_pos.T - self.sub_obs_pts.T,
                    self.ell_norm.T)  # pylint: disable=no-member

        log_traj.debug('Result: %r', res)
        return res

    @cached_property
    def solar_longitude(self):
        """Target seasonal solar longitude (degrees).

        Warning
        -------
        The seasonal solar longitude is computed on the main parent body
        for the moons (`spiceypy.lspcn` on the moon will not return
        the correct expected value).

        """
        log_traj.info('Compute the target seasonal solar longitude.')
        res = solar_longitude(
            self.ets,
            self.target,
            abcorr=self.abcorr)

        log_traj.debug('Result: %r', res)
        return res

    @property
    def inertial_frame(self):
        """Target parent inertial frame."""
        return 'JUICE_JUPITER_IF_J2000' \
            if self.target.parent == 'JUPITER' and self.observer == 'JUICE' else \
            'ECLIPJ2000'

    @cached_property
    def true_anomaly(self):
        """Target orbital true anomaly (degree)."""
        log_traj.debug('Compute true anomaly angle.')

        res = true_anomaly(
            self.ets,
            self.target,
            abcorr=self.abcorr,
            frame=self.inertial_frame)

        log_traj.debug('Result: %r', res)
        return res

    def mask(self, cond):
        """Create a masked trajectory."""
        return MaskedTrajectory(self, cond)

    def where(self, cond):
        """Create a masked trajectory only where the condition is valid."""
        return self.mask(~cond)

    def intersect(self, obj, outside=False):
        """Intersection mask between the trajectory and an object.

        Parameters
        ----------
        obj: any
            ROI-like object to intersect the trajectory.
        outside: bool, optional
            Return the invert of the intersection (default: `False`).

        Returns
        -------
        MaskedTrajectory
            Mask to apply on the trajectory.

        Raises
        ------
        AttributeError
            If the comparison object doest have a :py:func:`constains`
            test function.

        """
        if not hasattr(obj, 'contains'):
            raise AttributeError(f'Undefined `contains` intersection in {obj}.')

        cond = obj.contains(self.lonlat)
        return cond if outside else ~cond

# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This module implements the DAOStarFinder class.
"""

import warnings

from astropy.table import Table
from astropy.utils import lazyproperty
import numpy as np

from .base import StarFinderBase
from ._utils import _StarCutout, _StarFinderKernel, _find_stars
from ..utils.exceptions import NoDetectionsWarning

__all__ = ['DAOStarFinder']


class DAOStarFinder(StarFinderBase):
    """
    Detect stars in an image using the DAOFIND (`Stetson 1987
    <https://ui.adsabs.harvard.edu/abs/1987PASP...99..191S/abstract>`_)
    algorithm.

    DAOFIND (`Stetson 1987; PASP 99, 191
    <https://ui.adsabs.harvard.edu/abs/1987PASP...99..191S/abstract>`_)
    searches images for local density maxima that have a peak amplitude
    greater than ``threshold`` (approximately; ``threshold`` is applied
    to a convolved image) and have a size and shape similar to the
    defined 2D Gaussian kernel.  The Gaussian kernel is defined by the
    ``fwhm``, ``ratio``, ``theta``, and ``sigma_radius`` input
    parameters.

    ``DAOStarFinder`` finds the object centroid by fitting the marginal x
    and y 1D distributions of the Gaussian kernel to the marginal x and
    y distributions of the input (unconvolved) ``data`` image.

    ``DAOStarFinder`` calculates the object roundness using two methods. The
    ``roundlo`` and ``roundhi`` bounds are applied to both measures of
    roundness.  The first method (``roundness1``; called ``SROUND`` in
    `DAOFIND`_) is based on the source symmetry and is the ratio of a
    measure of the object's bilateral (2-fold) to four-fold symmetry.
    The second roundness statistic (``roundness2``; called ``GROUND`` in
    `DAOFIND`_) measures the ratio of the difference in the height of
    the best fitting Gaussian function in x minus the best fitting
    Gaussian function in y, divided by the average of the best fitting
    Gaussian functions in x and y.  A circular source will have a zero
    roundness.  A source extended in x or y will have a negative or
    positive roundness, respectively.

    The sharpness statistic measures the ratio of the difference between
    the height of the central pixel and the mean of the surrounding
    non-bad pixels in the convolved image, to the height of the best
    fitting Gaussian function at that point.

    Parameters
    ----------
    threshold : float
        The absolute image value above which to select sources.

    fwhm : float
        The full-width half-maximum (FWHM) of the major axis of the
        Gaussian kernel in units of pixels.

    ratio : float, optional
        The ratio of the minor to major axis standard deviations of the
        Gaussian kernel.  ``ratio`` must be strictly positive and less
        than or equal to 1.0.  The default is 1.0 (i.e., a circular
        Gaussian kernel).

    theta : float, optional
        The position angle (in degrees) of the major axis of the
        Gaussian kernel measured counter-clockwise from the positive x
        axis.

    sigma_radius : float, optional
        The truncation radius of the Gaussian kernel in units of sigma
        (standard deviation) [``1 sigma = FWHM /
        (2.0*sqrt(2.0*log(2.0)))``].

    sharplo : float, optional
        The lower bound on sharpness for object detection.

    sharphi : float, optional
        The upper bound on sharpness for object detection.

    roundlo : float, optional
        The lower bound on roundness for object detection.

    roundhi : float, optional
        The upper bound on roundness for object detection.

    sky : float, optional
        The background sky level of the image.  Setting ``sky`` affects
        only the output values of the object ``peak``, ``flux``, and
        ``mag`` values.  The default is 0.0, which should be used to
        replicate the results from `DAOFIND`_.

    exclude_border : bool, optional
        Set to `True` to exclude sources found within half the size of
        the convolution kernel from the image borders.  The default is
        `False`, which is the mode used by `DAOFIND`_.

    brightest : int, None, optional
        Number of brightest objects to keep after sorting the full object list.
        If ``brightest`` is set to `None`, all objects will be selected.

    peakmax : float, None, optional
        Maximum peak pixel value in an object. Only objects whose peak pixel
        values are *strictly smaller* than ``peakmax`` will be selected.
        This may be used to exclude saturated sources. By default, when
        ``peakmax`` is set to `None`, all objects will be selected.

        .. warning::
            `DAOStarFinder` automatically excludes objects whose peak
            pixel values are negative. Therefore, setting ``peakmax`` to a
            non-positive value would result in exclusion of all objects.

    See Also
    --------
    IRAFStarFinder

    Notes
    -----
    For the convolution step, this routine sets pixels beyond the image
    borders to 0.0.  The equivalent parameters in `DAOFIND`_ are
    ``boundary='constant'`` and ``constant=0.0``.

    The main differences between `~photutils.detection.DAOStarFinder`
    and `~photutils.detection.IRAFStarFinder` are:

    * `~photutils.detection.IRAFStarFinder` always uses a 2D
      circular Gaussian kernel, while
      `~photutils.detection.DAOStarFinder` can use an elliptical
      Gaussian kernel.

    * `~photutils.detection.IRAFStarFinder` calculates the objects'
      centroid, roundness, and sharpness using image moments.

    References
    ----------
    .. [1] Stetson, P. 1987; PASP 99, 191
           (https://ui.adsabs.harvard.edu/abs/1987PASP...99..191S/abstract)
    .. [2] https://iraf.net/irafhelp.php?val=daofind

    .. _DAOFIND: https://iraf.net/irafhelp.php?val=daofind
    """

    def __init__(self, threshold, fwhm, ratio=1.0, theta=0.0,
                 sigma_radius=1.5, sharplo=0.2, sharphi=1.0, roundlo=-1.0,
                 roundhi=1.0, sky=0.0, exclude_border=False,
                 brightest=None, peakmax=None):

        if not np.isscalar(threshold):
            raise TypeError('threshold must be a scalar value.')
        self.threshold = threshold

        if not np.isscalar(fwhm):
            raise TypeError('fwhm must be a scalar value.')
        self.fwhm = fwhm

        self.ratio = ratio
        self.theta = theta
        self.sigma_radius = sigma_radius
        self.sharplo = sharplo
        self.sharphi = sharphi
        self.roundlo = roundlo
        self.roundhi = roundhi
        self.sky = sky
        self.exclude_border = exclude_border

        self.kernel = _StarFinderKernel(self.fwhm, self.ratio, self.theta,
                                        self.sigma_radius)
        self.threshold_eff = self.threshold * self.kernel.relerr
        self.brightest = brightest
        self.peakmax = peakmax
        self._star_cutouts = None

    def find_stars(self, data, mask=None):
        """
        Find stars in an astronomical image.

        Parameters
        ----------
        data : 2D array_like
            The 2D image array.

        mask : 2D bool array, optional
            A boolean mask with the same shape as ``data``, where a
            `True` value indicates the corresponding element of ``data``
            is masked.  Masked pixels are ignored when searching for
            stars.

        Returns
        -------
        table : `~astropy.table.Table` or `None`
            A table of found stars with the following parameters:

            * ``id``: unique object identification number.
            * ``xcentroid, ycentroid``: object centroid.
            * ``sharpness``: object sharpness.
            * ``roundness1``: object roundness based on symmetry.
            * ``roundness2``: object roundness based on marginal Gaussian
              fits.
            * ``npix``: the total number of pixels in the Gaussian kernel
              array.
            * ``sky``: the input ``sky`` parameter.
            * ``peak``: the peak, sky-subtracted, pixel value of the object.
            * ``flux``: the object flux calculated as the peak density in
              the convolved image divided by the detection threshold.  This
              derivation matches that of `DAOFIND`_ if ``sky`` is 0.0.
            * ``mag``: the object instrumental magnitude calculated as
              ``-2.5 * log10(flux)``.  The derivation matches that of
              `DAOFIND`_ if ``sky`` is 0.0.

            `None` is returned if no stars are found.

        """

        star_cutouts = _find_stars(data, self.kernel, self.threshold_eff,
                                   mask=mask,
                                   exclude_border=self.exclude_border)

        if star_cutouts is None:
            warnings.warn('No sources were found.', NoDetectionsWarning)
            return None

        self._star_cutouts = star_cutouts

        star_props = []
        for star_cutout in star_cutouts:
            props = _DAOFindProperties(star_cutout, self.kernel, self.sky)

            if np.isnan(props.dx_hx).any() or np.isnan(props.dy_hy).any():
                continue

            if (props.sharpness <= self.sharplo
                    or props.sharpness >= self.sharphi):
                continue

            if (props.roundness1 <= self.roundlo
                    or props.roundness1 >= self.roundhi):
                continue

            if (props.roundness2 <= self.roundlo
                    or props.roundness2 >= self.roundhi):
                continue

            if self.peakmax is not None and props.peak >= self.peakmax:
                continue

            star_props.append(props)

        nstars = len(star_props)
        if nstars == 0:
            warnings.warn('Sources were found, but none pass the sharpness '
                          'and roundness criteria.', NoDetectionsWarning)
            return None

        if self.brightest is not None:
            fluxes = [props.flux for props in star_props]
            idx = sorted(np.argsort(fluxes)[-self.brightest:].tolist())
            star_props = [star_props[k] for k in idx]
            nstars = len(star_props)

        table = Table()
        table['id'] = np.arange(nstars) + 1
        columns = ('xcentroid', 'ycentroid', 'sharpness', 'roundness1',
                   'roundness2', 'npix', 'sky', 'peak', 'flux', 'mag')
        for column in columns:
            table[column] = [getattr(props, column) for props in star_props]

        return table


class _DAOFindProperties:
    """
    Class to calculate the properties of each detected star, as defined
    by `DAOFIND`_.

    Parameters
    ----------
    star_cutout : `_StarCutout`
        A `_StarCutout` object containing the image cutout for the star.

    kernel : `_StarFinderKernel`
        The convolution kernel.  The shape of the kernel must match that
        of the input ``star_cutout``.

    sky : float, optional
        The local sky level around the source.  ``sky`` is used only to
        calculate the source peak value, flux, and magnitude.  The
        default is 0.

    .. _DAOFIND: https://iraf.net/irafhelp.php?val=daofind
    """

    def __init__(self, star_cutout, kernel, sky=0.):
        if not isinstance(star_cutout, _StarCutout):
            raise ValueError('data must be an _StarCutout object')

        if star_cutout.data.shape != kernel.shape:
            raise ValueError('cutout and kernel must have the same shape')

        self.cutout = star_cutout
        self.kernel = kernel
        self.sky = sky  # DAOFIND has no sky input -> same as sky=0.

        self.data = star_cutout.data
        self.data_masked = star_cutout.data_masked
        self.npixels = star_cutout.npixels  # unmasked pixels
        self.nx = star_cutout.nx
        self.ny = star_cutout.ny
        self.xcenter = star_cutout.cutout_xcenter
        self.ycenter = star_cutout.cutout_ycenter

    @lazyproperty
    def data_peak(self):
        return self.data[self.ycenter, self.xcenter]

    @lazyproperty
    def conv_peak(self):
        return self.cutout.convdata[self.ycenter, self.xcenter]

    @lazyproperty
    def roundness1(self):
        # set the central (peak) pixel to zero
        cutout_conv = self.cutout.convdata.copy()
        cutout_conv[self.ycenter, self.xcenter] = 0.0  # for sum4

        # calculate the four roundness quadrants.
        # the cutout size always matches the kernel size, which have odd
        # dimensions.
        # quad1 = bottom right
        # quad2 = bottom left
        # quad3 = top left
        # quad4 = top right
        # 3 3 4 4 4
        # 3 3 4 4 4
        # 3 3 x 1 1
        # 2 2 2 1 1
        # 2 2 2 1 1
        quad1 = cutout_conv[0:self.ycenter + 1, self.xcenter + 1:]
        quad2 = cutout_conv[0:self.ycenter, 0:self.xcenter + 1]
        quad3 = cutout_conv[self.ycenter:, 0:self.xcenter]
        quad4 = cutout_conv[self.ycenter + 1:, self.xcenter:]

        sum2 = -quad1.sum() + quad2.sum() - quad3.sum() + quad4.sum()
        if sum2 == 0:
            return 0.

        sum4 = np.abs(cutout_conv).sum()
        if sum4 <= 0:
            return None

        return 2.0 * sum2 / sum4

    @lazyproperty
    def sharpness(self):
        npixels = self.npixels - 1  # exclude the peak pixel
        data_mean = (np.sum(self.data_masked) - self.data_peak) / npixels

        return (self.data_peak - data_mean) / self.conv_peak

    def daofind_marginal_fit(self, axis=0):
        """
        Fit 1D Gaussians, defined from the marginal x/y kernel
        distributions, to the marginal x/y distributions of the original
        (unconvolved) image.

        These fits are used calculate the star centroid and roundness
        ("GROUND") properties.

        Parameters
        ----------
        axis : {0, 1}, optional
            The axis for which the marginal fit is performed:

            * 0: for the x axis
            * 1: for the y axis

        Returns
        -------
        dx : float
            The fractional shift in x or y (depending on ``axis`` value)
            of the image centroid relative to the maximum pixel.

        hx : float
            The height of the best-fitting Gaussian to the marginal x or
            y (depending on ``axis`` value) distribution of the
            unconvolved source data.
        """

        # define triangular weighting functions along each axis, peaked
        # in the middle and equal to one at the edge
        x = self.xcenter - np.abs(np.arange(self.nx) - self.xcenter) + 1
        y = self.ycenter - np.abs(np.arange(self.ny) - self.ycenter) + 1
        xwt, ywt = np.meshgrid(x, y)

        if axis == 0:  # marginal distributions along x axis
            wt = xwt[0]  # 1D
            wts = ywt  # 2D
            size = self.nx
            center = self.xcenter
            sigma = self.kernel.xsigma
            dxx = center - np.arange(size)
        elif axis == 1:  # marginal distributions along y axis
            wt = np.transpose(ywt)[0]  # 1D
            wts = xwt  # 2D
            size = self.ny
            center = self.ycenter
            sigma = self.kernel.ysigma
            dxx = np.arange(size) - center

        # compute marginal sums for given axis
        wt_sum = np.sum(wt)
        dx = center - np.arange(size)

        # weighted marginal sums
        kern_sum_1d = np.sum(self.kernel.gaussian_kernel_unmasked * wts,
                             axis=axis)
        kern_sum = np.sum(kern_sum_1d * wt)
        kern2_sum = np.sum(kern_sum_1d**2 * wt)

        dkern_dx = kern_sum_1d * dx
        dkern_dx_sum = np.sum(dkern_dx * wt)
        dkern_dx2_sum = np.sum(dkern_dx**2 * wt)
        kern_dkern_dx_sum = np.sum(kern_sum_1d * dkern_dx * wt)

        data_sum_1d = np.sum(self.data * wts, axis=axis)
        data_sum = np.sum(data_sum_1d * wt)
        data_kern_sum = np.sum(data_sum_1d * kern_sum_1d * wt)
        data_dkern_dx_sum = np.sum(data_sum_1d * dkern_dx * wt)
        data_dx_sum = np.sum(data_sum_1d * dxx * wt)

        # perform linear least-squares fit (where data = sky + hx*kernel)
        # to find the amplitude (hx)
        # reject the star if the fit amplitude is not positive
        hx_numer = data_kern_sum - (data_sum * kern_sum) / wt_sum
        if hx_numer <= 0.:
            return np.nan, np.nan

        hx_denom = kern2_sum - (kern_sum**2 / wt_sum)
        if hx_denom <= 0.:
            return np.nan, np.nan

        # compute fit amplitude
        hx = hx_numer / hx_denom
        # sky = (data_sum - (hx * kern_sum)) / wt_sum

        # compute centroid shift
        dx = ((kern_dkern_dx_sum
               - (data_dkern_dx_sum - dkern_dx_sum * data_sum))
              / (hx * dkern_dx2_sum / sigma**2))

        hsize = size / 2.
        if abs(dx) > hsize:
            if data_sum == 0.:
                dx = 0.0
            else:
                dx = data_dx_sum / data_sum
                if abs(dx) > hsize:
                    dx = 0.0

        return dx, hx

    @lazyproperty
    def dx_hx(self):
        return self.daofind_marginal_fit(axis=0)

    @lazyproperty
    def dy_hy(self):
        return self.daofind_marginal_fit(axis=1)

    @lazyproperty
    def dx(self):
        return self.dx_hx[0]

    @lazyproperty
    def dy(self):
        return self.dy_hy[0]

    @lazyproperty
    def xcentroid(self):
        return self.cutout.xpeak + self.dx

    @lazyproperty
    def ycentroid(self):
        return self.cutout.ypeak + self.dy

    @lazyproperty
    def hx(self):
        return self.dx_hx[1]

    @lazyproperty
    def hy(self):
        return self.dy_hy[1]

    @lazyproperty
    def roundness2(self):
        """
        The star roundness.

        This roundness parameter represents the ratio of the difference
        in the height of the best fitting Gaussian function in x minus
        the best fitting Gaussian function in y, divided by the average
        of the best fitting Gaussian functions in x and y.  A circular
        source will have a zero roundness.  A source extended in x or y
        will have a negative or positive roundness, respectively.
        """

        if np.isnan(self.hx) or np.isnan(self.hy):
            return np.nan
        else:
            return 2.0 * (self.hx - self.hy) / (self.hx + self.hy)

    @lazyproperty
    def peak(self):
        return self.data_peak - self.sky

    @lazyproperty
    def npix(self):
        """
        The total number of pixels in the rectangular cutout image.
        """

        return self.data.size

    @lazyproperty
    def flux(self):
        return ((self.conv_peak / self.cutout.threshold_eff)
                - (self.sky * self.npix))

    @lazyproperty
    def mag(self):
        if self.flux <= 0:
            return np.nan
        else:
            return -2.5 * np.log10(self.flux)

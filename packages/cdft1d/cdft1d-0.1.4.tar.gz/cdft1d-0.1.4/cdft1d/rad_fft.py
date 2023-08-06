#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module provides collection
of FFT routines for treatment of
spherically symmetric functions
"""

import math

import numpy as np
from math import pi
from scipy.fftpack import dst


def fft_rgrid_iv(dr, ntot):
    r"""
    Generates midpoint based (type=4) grid in real space as

    .. math::
        \begin{equation}
        r(i)=dr(i-0.5), \quad i=1,\ldots,ntot
        \end{equation}
    Args:
        dr: grid spacing in real space
        ntot: number of grid points

    Returns:
        :math:`r(i)` - 1D numpy array of grid points in real space

    """

    rg = np.arange(1, ntot + 1, 1,dtype=np.double)
    rg = dr * (rg - 0.5)
    return rg


def fft_kgrid_spacing(dr, ntot):
    """
    Compute spacing of reciprocal (k) grid

    Args:
        dr: grid spacing in real space
        ntot: number of grid points


    Returns:
        Spacing of reciprocal (k) grid

    """
    return pi / (dr * ntot)


def fft_kgrid_iv(dr, ntot):

    r"""
    Generates midpoint based (type=4) grid in reciprocal space as

    .. math::
        k(i)=\frac{\pi}{dr \cdot ntot}(i-0.5), \quad i=1,\ldots,ntot

    Args:
        dr: grid spacing in real space
        ntot: number of grid points

    Returns:
        :math:`k(i)` - 1D numpy array of grid points in reciprocal k-space

    """

    _dk = fft_kgrid_spacing(dr, ntot)

    _rg = np.arange(1, ntot + 1, 1,dtype=np.double)
    _rg = _dk*(_rg-0.5)
    return _rg


def fft_kgrid_to_rgrid(kgrid):

    ntot = len(kgrid)
    dk = kgrid[1]-kgrid[0]
    dr = pi/(ntot*dk)

    # return (dr/dk) * kgrid
    return fft_rgrid_iv(dr, ntot)

def dst_iv(fi, delta_grid=1.0):

    r"""
    Performs type 4 Discrete Sine Transform (DST-IV) [#dst]_
    from real to reciprocal space.

    .. math::
        f(k_i)= \Delta_g \cdot \sum_{i=1}^{N} f(r_i) \sin(k_i r_i)


    Args:
        fi: function as an array over the grid
        delta_grid: grid spacing ( :math:`L/N`  )


    Returns:

    Notes:
        - Type 4 definition of DST is used as defined
          in `Scipy <https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.dst.html>`_.

        - Optional grid spacing allows to evaluate

          .. math::
            f(k)=\int_0^{L}  f(r)\sin(kr) dr \approx
            \frac{L}{N}\sum_{i=1}^{N} f(r_i) \sin(kr_i)


    """

    N = len(fi)
    fk = dst(fi, type=4, norm='ortho')

    fk = fk * delta_grid * math.sqrt(N / 2.0)

    return fk


def bst_forward(rg, kg, fr):
    r"""
    Performs forward Bessel transform defined as

    .. math::
        f(k_i)=\frac{4\pi}{k_i}\int_0^{L}  f(r)\sin(k_i r) dr \approx
        \frac{4\pi }{k_i} \Delta r \sum_{j=1}^{N} f(r_j) \sin(k_ir_j)
    where :math:`\Delta r = L/N`

    Args:
        dr: grid spacing :math:`\Delta r = L/N`
        rg: real space grid :math:`\{r_i, i=1,\ldots , N\}`
        kg: kspace space grid :math:`\{k_i, i=1,\ldots , N\}`
        fr: function as an array over the grid :math:`\{f(r_i), i=1,\ldots , N\}`

    Returns:

    """

    dr = rg[1]-rg[0]
    fk = dst_iv(rg * fr, delta_grid=dr)
    fk = (fk/kg)*4.0*math.pi

    return fk


def bst_inverse(rg, kg, fk):
    """

    Args:
        dr:
        rg:
        kg:
        fr:

    Returns:

    """

    dk = kg[1] - kg[0]
    fr = dst_iv(kg * fk, delta_grid=dk)
    fr = fr/(rg*2.0*math.pi**2)

    return fr


class RadFFT:
    """
    Provides FFT operations for spherically symmetric functions

    Args:
        dr:    grid spacing
        ntot:  number of grid points

    """

    def __init__(self, dr, ntot):

        self.dr = dr
        self.ntot = ntot

        self.rgrid = fft_rgrid_iv(dr, ntot)

        self.dk = fft_kgrid_spacing(dr, ntot)
        self.kgrid = fft_kgrid_iv(dr, ntot)

    def to_kspace(self, fr):
        """
        Generates k-space representation

        Args:
            fr: function on a radial grid

        Returns:
            k-space representation of fr

        """
        fk = bst_forward(self.rgrid, self.kgrid, fr)
        return fk

    def to_rspace(self, fk):
        """
        Generates r-space representation

        Args:
            fk: function on a reciprocal grid

        Returns:
            r-space representation of fr

        """
        fr = bst_inverse(self.rgrid, self.kgrid, fk)
        return fr


def fft_pair(rg, kg, a=1.0):
    pi = math.pi

    fr = np.exp(-a * rg ** 2)

    fk = math.sqrt(pi / a) ** 3 * np.exp(-kg ** 2 / (4.0 * a))

    return fr, fk

if __name__ == '__main__':
    dr = 0.01
    ntot = 8192
    rg = fft_rgrid_iv(dr, ntot)
    kg = fft_kgrid_iv(dr, ntot)
    fr0, fk0 = fft_pair(rg,kg)

    ifft = RadFFT(dr, ntot)

    fr = ifft.to_rspace(fk0)/math.sqrt(2*ntot)

    fk = ifft.to_kspace(fr)/math.sqrt(2*ntot)
    print(fk[0],fk0[0],fk[0]/fk0[0])
    pass
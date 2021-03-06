#!/usr/bin/env python
u"""
fourier_legendre.py
Original IDL code gen_plms.pro written by Sean Swenson
Adapted by Tyler Sutterley (09/2021)

Computes Fourier coefficients of the associated Legendre functions

CALLING SEQUENCE:
    plm = fourier_legendre(lmax,mmax)

INPUTS:
    lmax: maximum spherical harmonic degree
    mmax: maximum spherical harmonic order

OUTPUTS:
    plm: Fourier coefficients

PYTHON DEPENDENCIES:
    numpy: Scientific Computing Tools For Python (https://numpy.org)

UPDATE HISTORY:
    Updated 09/2021: cleaned up program for public release
    Updated 07/2020: added function docstrings
    Updated 06/2019: using Python3 compatible division
    Written 04/2013
"""
from __future__ import division
import numpy as np

def fourier_legendre(lmax,mmax):
    """
    Computes Fourier coefficients of the associated Legendre functions

    Arguments
    ---------
    lmax: Upper bound of Spherical Harmonic Degrees
    mmax: Upper bound of Spherical Harmonic Orders

    Returns
    -------
    plms: Fourier coefficients
    """

    #-- allocate for output fourier coefficients
    plm = np.zeros((lmax+1,lmax+1,lmax+1))
    l_even = np.arange(0,lmax+1,2)
    l_odd = np.arange(1,lmax,2)
    m_even = np.arange(0,mmax+1,2)
    m_odd = np.arange(1,mmax,2)

    #-- First compute m=0, m=1 terms
    #-- Compute m = 0, l = even terms
    plm[l_even,0,0] = 1.0
    p1 = (l_even*(l_even+1.0))*plm[l_even,0,0]
    plm[l_even,0,2] = p1 / (l_even*(l_even+1.0)-2.0)
    for j in range(2,lmax,2):#-- equivalent to 2:lmax-2
        p1 = 2.0*(l_even*(l_even+1.0)-j**2.0)*plm[l_even,0,j]
        p2 = ((j-2.0)*(j-1.0)-l_even*(l_even+1.0))*plm[l_even,0,j-2]
        dfactor = (l_even*(l_even+1.0)-(j+2.0)*(j+1.0))
        plm[l_even,0,j+2] = (p1 + p2) / dfactor


    #-- Special case for j = 0 fourier coefficient
    plm[l_even,0,0] = plm[l_even,0,0]/2.0
    #-- Normalize overall sum to 2 for m == 0
    norm = np.zeros((len(l_even)))
    for j in range(0,lmax+2,2):#-- equivalent to 0:lmax
        ptemp = np.squeeze(plm[l_even[:, np.newaxis],0,m_even])
        dtemp = 1.0/(1.0-j-m_even) + 1.0/(1.0+j-m_even) + \
            1.0/(1.0-j+m_even) + 1.0/(1.0+j+m_even)
        norm[l_even//2] = norm[l_even//2] + plm[l_even,0,j] * \
            np.dot(ptemp, dtemp)/2.0
    #-- normalize plms
    norm = np.sqrt(norm/2.0)
    for l in range(0,lmax+2,2):#-- equivalent to 0:lmax
        plm[l,0,:] = plm[l,0,:]/norm[l//2]


    #-- Compute m = 0, l = odd terms
    plm[l_odd,0,1] = 1.0
    p1 = (2.0-l_odd*(l_odd+1.0))*plm[l_odd,0,1]
    plm[l_odd,0,3] = p1 / (6.0-l_odd*(l_odd+1.0))
    for j in range(3,lmax-1,2):#-- equivalent to 3:lmax-3
        p1 = 2.0*(l_odd*(l_odd+1.0)-j**2.0)*plm[l_odd,0,j]
        p2 = ((j-2.0)*(j-1.0)-l_odd*(l_odd+1.0))*plm[l_odd,0,j-2]
        dfactor = (l_odd*(l_odd+1.0)-(j+2.0)*(j+1.0))
        plm[l_odd,0,j+2] = (p1 + p2) / dfactor

    #-- Normalize overall sum to 2 for m == 0
    norm = np.zeros((len(l_odd)))
    for j in range(1,lmax+1,2):#-- equivalent to 1:lmax-1
        ptemp = np.squeeze(plm[l_odd[:, np.newaxis],0,m_odd])
        dtemp = 1.0/(1.0-j-m_odd) + 1.0/(1.0+j-m_odd) + \
            1.0/(1.0-j+m_odd) + 1.0/(1.0+j+m_odd)
        norm[(l_odd-1)//2] = norm[(l_odd-1)//2] + plm[l_odd,0,j] * \
            np.dot(ptemp, dtemp)/2.0
    #-- normalize plms
    norm = np.sqrt(norm/2.0)
    for l in range(1,lmax+1,2):#-- equivalent to 1:lmax-1
        plm[l,0,:] = plm[l,0,:]/norm[(l-1)//2]


    #-- Compute m = 1, l = even terms
    plm[l_even,1,0] = 0.0
    plm[l_even,1,2] = 1.0
    for j in range(2,lmax,2):#-- equivalent to 2:lmax-2
        p1 = 2.0*(l_even*(l_even+1)-j**2.0-2.0)*plm[l_even,1,j]
        p2 = ((j-2.0)*(j-1.0)-l_even*(l_even+1))*plm[l_even,1,j-2]
        dfactor = (l_even*(l_even+1.0)-(j+2.0)*(j+1.0))
        plm[l_even,1,j+2] = (p1 + p2) / dfactor

    #-- Normalize overall sum to 4 for m == 1
    #-- different norm than that of the cosine series
    norm = np.zeros((len(l_even)))
    for j in range(0,lmax+2,2):#-- equivalent to 0:lmax
        ptemp = np.squeeze(plm[l_even[:, np.newaxis],1,m_even])
        dtemp = -1.0/(1.0-j-m_even) + 1.0/(1+j-m_even) + \
            1.0/(1.0-j+m_even) - 1.0/(1+j+m_even)
        norm[l_even//2] = norm[l_even//2] + plm[l_even,1,j] * \
            np.dot(ptemp, dtemp)/2.0
    #-- normalize plms
    norm = np.sqrt(norm/4.0)
    for l in range(0,lmax+2,2):#-- equivalent to 0:lmax
        plm[l,1,:] = plm[l,1,:]/norm[l//2]

    #-- Compute m = 1, l = odd terms
    plm[l_odd,1,1] = 1.0
    plm[l_odd,1,3] = 3.0*(l_odd*(l_odd+1)-2)*plm[l_odd,1,1]/(l_odd*(l_odd+1)-6)
    for j in range(3,lmax-1,2):#-- equivalent to 3:lmax-3
        p1 = 2.0*(l_odd*(l_odd+1.0)-j**2.0-2.0)*plm[l_odd,1,j]
        p2 = ((j-2.0)*(j-1.0)-l_odd*(l_odd+1.0))*plm[l_odd,1,j-2]
        dfactor = (l_odd*(l_odd+1.0)-(j+2.0)*(j+1.0))
        plm[l_odd,1,j+2] = (p1 + p2) / dfactor

    #-- Normalize overall sum to 4 for m == 1
    norm = np.zeros((len(l_odd)))
    for j in range(1,lmax+1,2):#-- equivalent to 1:lmax-1
        ptemp = np.squeeze(plm[l_odd[:, np.newaxis],1,m_odd])
        dtemp = -1.0/(1.0-j-m_odd) + 1.0/(1.0+j-m_odd) + \
            1.0/(1.0-j+m_odd) - 1.0/(1.0+j+m_odd)
        norm[(l_odd-1)//2] = norm[(l_odd-1)//2] + plm[l_odd,1,j] * \
            np.dot(ptemp, dtemp)/2.0
    #-- normalize plms
    norm = np.sqrt(norm/4.0)
    for l in range(1,lmax+1,2):#-- equivalent to 1:lmax-1
        plm[l,1,:] = plm[l,1,:]/norm[(l-1)//2]


    #-- Compute coefficients for m > 0
    #-- m = 0 terms on rhs have different normalization
    m = 0
    #-- m = 0, l = even terms
    for l in range(m,lmax-1):#-- equivalent to m:lmax-2
        p1 = np.sqrt((l+m+2.0)*(l+m+1.0)/(2.0*l+1.0))*plm[l,m,m_even]
        p2 = np.sqrt((l-m+1.0)*(l-m+2.0)/(2.0*l+5.0))*plm[l+2,m,m_even]
        p3 = np.sqrt((l-m)*(l-m-1.0)/(2.0*l+1.0)/2.0)*plm[l,m+2,m_even]
        dfactor = np.sqrt((l+m+4.0)*(l+m+3.0)/(2.0*l+5.0)/2.0)
        plm[l+2,m+2,m_even] = (p1 - p2 + p3) / dfactor

    #-- m = 0, l = odd terms
    for l in range(m+1,lmax-1):#-- equivalent to m+1:lmax-2
        p1 = np.sqrt((l+m+2.0)*(l+m+1.0)/(2.0*l+1.0))*plm[l,m,m_odd]
        p2 = np.sqrt((l-m+1.0)*(l-m+2.0)/(2.0*l+5.0))*plm[l+2,m,m_odd]
        p3 = np.sqrt((l-m)*(l-m-1.0)/(2.0*l+1.0)/2.0)*plm[l,m+2,m_odd]
        dfactor = np.sqrt((l+m+4.0)*(l+m+3.0)/(2.0*l+5.0)/2.0)
        plm[l+2,m+2,m_odd] = (p1 - p2 + p3) / dfactor

    #-- m = even terms
    for m in range(2,lmax,2):#-- equivalent to 2:lmax-2
        #-- m = even, > 2, l = even terms
        for l in range(m,lmax,2):#-- equivalent to m:lmax-2
            p1 = np.sqrt((l+m+2.0)*(l+m+1.0)/(2.0*l+1.0))*plm[l,m,m_even]
            p2 = np.sqrt((l-m+1.0)*(l-m+2.0)/(2.0*l+5.0))*plm[l+2,m,m_even]
            p3 = np.sqrt((l-m)*(l-m-1.0)/(2.0*l+1.0))*plm[l,m+2,m_even]
            dfactor = np.sqrt((l+m+4.0)*(l+m+3.0)/(2.0*l+5.0))
            plm[l+2,m+2,m_even] = (p1 - p2 + p3) / dfactor

        #-- m = even, > 2, l = odd terms
        for l in range(m+1,lmax-1,2):
            p1 = np.sqrt((l+m+2.0)*(l+m+1.0)/(2.0*l+1.0))*plm[l,m,m_odd]
            p2 = np.sqrt((l-m+1.0)*(l-m+2.0)/(2.0*l+5.0))*plm[l+2,m,m_odd]
            p3 = np.sqrt((l-m)*(l-m-1.0)/(2.0*l+1.0))*plm[l,m+2,m_odd]
            dfactor = np.sqrt((l+m+4.0)*(l+m+3.0)/(2.0*l+5.0))
            plm[l+2,m+2,m_odd] = (p1 - p2 + p3) / dfactor

    #-- m = odd terms
    for m in range(1,lmax-1,2):#-- equivalent to 1:lmax-3
        #-- m = odd, > 1, l = even terms
        for l in range(m+1,lmax-1,2):#-- equivalent to m+1,lmax-2
            p1 = np.sqrt((l+m+2.0)*(l+m+1.0)/(2.0*l+1.0))*plm[l,m,m_even]
            p2 = np.sqrt((l-m+1.0)*(l-m+2.0)/(2.0*l+5.0))*plm[l+2,m,m_even]
            p3 = np.sqrt((l-m)*(l-m-1.0)/(2.0*l+1.0))*plm[l,m+2,m_even]
            dfactor = np.sqrt((l+m+4.0)*(l+m+3.0)/(2.0*l+5.0))
            plm[l+2,m+2,m_even] = (p1 - p2 + p3) / dfactor

        #-- m = odd, > 1, l = odd terms
        for l in range(m,lmax-1,2):#-- equivalent to m:lmax-2
            p1 = np.sqrt((l+m+2.0)*(l+m+1.0)/(2.0*l+1.0))*plm[l,m,m_odd]
            p2 = np.sqrt((l-m+1.0)*(l-m+2.0)/(2.0*l+5.0))*plm[l+2,m,m_odd]
            p3 = np.sqrt((l-m)*(l-m-1.0)/(2.0*l+1.0))*plm[l,m+2,m_odd]
            dfactor = np.sqrt((l+m+4.0)*(l+m+3.0)/(2.0*l+5.0))
            plm[l+2,m+2,m_odd] = (p1 - p2 + p3) / dfactor

    #-- return the fourier coefficients
    return plm

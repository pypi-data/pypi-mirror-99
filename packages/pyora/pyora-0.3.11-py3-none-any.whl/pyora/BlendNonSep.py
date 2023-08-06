import numpy as np


"""
Implementation of the non-separable blending modes as described in 

https://www.w3.org/TR/compositing-1/#blendingnonseparable

"""


"""
four non-separable utility functions as described on the aforementioned page

Lum(C) = 0.3 x Cred + 0.59 x Cgreen + 0.11 x Cblue
    
    ClipColor(C)
        L = Lum(C)
        n = min(Cred, Cgreen, Cblue)
        x = max(Cred, Cgreen, Cblue)
        if(n < 0)
            C = L + (((C - L) * L) / (L - n))
                      
        if(x > 1)
            C = L + (((C - L) * (1 - L)) / (x - L))
        
        return C
    
    SetLum(C, l)
        d = l - Lum(C)
        Cred = Cred + d
        Cgreen = Cgreen + d
        Cblue = Cblue + d
        return ClipColor(C)
        
    Sat(C) = max(Cred, Cgreen, Cblue) - min(Cred, Cgreen, Cblue)

"""

def _lum(_c):
    """

    :param c: x by x by 3 matrix of rgb color components of pixels
    :return: x by x by 3 matrix of luminosity of pixels
    """

    return (_c[:, :, 0] * 0.299) + (_c[:, :, 1] * 0.587) + (_c[:, :, 2] * 0.114)

def _setLum(c_orig, l):
    _c = c_orig.copy()
    _l = _lum(_c)
    d = l - _l
    _c[:, :, 0] += d
    _c[:, :, 1] += d
    _c[:, :, 2] += d
    _l = _lum(_c)

    _n = np.min(_c, axis=2)
    _x = np.max(_c, axis=2)

    for i in range(_c.shape[0]):
        for j in range(_c.shape[1]):
            c = _c[i][j]
            l = _l[i, j]
            n = _n[i, j]
            x = _x[i, j]

            if n < 0:
                _c[i][j] = l + (((c - l) * l) / (l - n))

            if x > 1:
                _c[i][j] = l + (((c - l) * (1 - l)) / (x - l))

    return _c

def _sat(_c):
    """

    :param c: x by x by 3 matrix of rgb color components of pixels
    :return: int of saturation of pixels
    """
    return np.max(_c, axis=2) - np.min(_c, axis=2)

# def _setSatKern(c):
#     max_i = np.argmax(c)
#     min_i = np.argmin(c)
#     if max_i != 2 and min_i != 2:
#         mid_i = 2
#     elif max_i != 1 and min_i != 1:
#         mid_i = 1
#     else:
#         mid_i = 0
#
#     if c[max_i] > c[min_i]:
#         c[mid_i] = (((c[mid_i] - c[min_i]) * s) / (c[max_i] - c[min_i]))
#         c[max_i] = s
#     else:
#         c[mid_i] = 0
#         c[max_i] = 0
#     c[min_i] = 0
#     return c

#setSatKern = np.vectorize(_setSatKern)

def _setSat(c_orig, s):
    """
    Set a new saturation value for the matrix of color

    The current implementation cannot be vectorized in an efficient manner, so it is very slow,
    O(m*n) at least. This might be able to be improved with openCL if that is the direction that the lib takes.
    :param c: x by x by 3 matrix of rgb color components of pixels
    :param s: int of the new saturation value for the matrix
    :return: x by x by 3 matrix of luminosity of pixels
    """
    _c = c_orig.copy()


    for i in range(_c.shape[0]):
        for j in range(_c.shape[1]):
            c = _c[i][j]

            min_i = 0
            mid_i = 1
            max_i = 2

            if c[mid_i] < c[min_i]:
                min_i, mid_i = mid_i, min_i
            if c[max_i] < c[mid_i]:
                mid_i, max_i = max_i, mid_i
            if c[mid_i] < c[min_i]:
                min_i, mid_i = mid_i, min_i
            if c[max_i] - c[min_i] > 0.0:
                _c[i][j][mid_i] = (((c[mid_i] - c[min_i]) * s[i, j]) / (c[max_i] - c[min_i]))
                _c[i][j][max_i] = s[i, j]
            else:
                _c[i][j][mid_i] = 0
                _c[i][j][max_i] = 0
            _c[i][j][min_i] = 0

    return _c


import math

#
# def _general_blend(source, destination, offsets, blend_func):
#     """
#     This function is slightly different than the one in the blend module, because the inside functions do not use the
#     alpha channel.
#     """
#
#     source = reshape_dest(source, destination, offsets)
#
#     destination_norm = destination / 255.0
#     source_norm = source / 255.0
#
#     Cb = destination_norm[:, :, :3]
#     Cs = source_norm[:, :, :3]
#
#     comp = blend_func(Cs, Cb)
#
#     # new algo, we apply the blend_func everywhere, except where dest does not exist, at all
#     # (where it does not exist, we just put src)
#     idxs = destination_norm[:, :, 3] == 0
#
#     ratio_rs = np.reshape(np.repeat(idxs, 3), [comp.shape[0], comp.shape[1], comp.shape[2]])
#     img_out = comp + (source_norm[:, :, :3] * ratio_rs)
#     img_out = np.nan_to_num(np.dstack((img_out, source_norm[:, :, 3])))  # add alpha channel and replace nans
#
#     return img_out * 255.0

# def _colourCompositingFormula(_as, ab, ar, Cs, Cb, Bbs):
#     return (1 - (_as / ar)) * Cb + (_as / ar) * math.floor((1 - ab) * Cs + ab * Bbs)


def hue(lower_rgb, upper_rgb):
    """

    Creates a color with the hue of the lower_rgb color and the saturation and luminosity of the backdrop color.

    """
    return _setLum(_setSat(upper_rgb, _sat(lower_rgb)), _lum(lower_rgb))

def saturation(lower_rgb, upper_rgb):
    """

    Creates a color with the saturation of the lower_rgb color and the hue and luminosity of the backdrop color.

    """
    return _setLum(_setSat(lower_rgb, _sat(upper_rgb)), _lum(lower_rgb))

def color(lower_rgb, upper_rgb):
    """

    Creates a color with the hue and saturation of the lower_rgb color and the luminosity of the backdrop color.

    """
    return _setLum(upper_rgb, _lum(lower_rgb))

def luminosity(lower_rgb, upper_rgb):
    """

    Creates a color with the luminosity of the lower_rgb color and the hue and saturation of the backdrop color.

    """
    return _setLum(lower_rgb, _lum(upper_rgb))

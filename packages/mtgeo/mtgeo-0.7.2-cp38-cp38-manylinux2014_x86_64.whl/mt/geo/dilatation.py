import numpy as _np

import mt.base.casting as _bc
from mt.base.deprecated import deprecated_func

from .transformation import register_transform, register_transformable
from .point_list import PointList
from .moments import Moments
from .affine_transformation import Aff


__all__ = ['dlt', 'Dlt', 'scale2d', 'flipx2d', 'flipy2d']


class Dlt(Aff):
    '''Dilatation (scaling and translation) in n-dim space. Here, scaling is per dimension, not uniform scaling.

    Examples
    --------
    >>> import numpy as _np
    >>> from mt.geo.dilatation import Dlt
    >>> a = Dlt(offset=_np.array([1,2]), scale=_np.array([3,4]))
    >>> ~a
    Dlt(offset=[-0.33333333 -0.5       ], scale=[0.33333333 0.25      ])
    >>> a*~a
    Dlt(offset=[0. 0.], scale=[1. 1.])
    >>> a/a
    Dlt(offset=[0. 0.], scale=[1. 1.])
    >>> a%a
    Dlt(offset=[0. 0.], scale=[1. 1.])
    >>> b = _mg.Dlt(offset=_np.array([1,0.5]), scale=_np.array([1/3,0.25]))
    >>> a*b
    Dlt(offset=[4. 4.], scale=[1. 1.])
    >>> b*a
    Dlt(offset=[1.33333333 1.        ], scale=[1. 1.])
    >>> a/b
    Dlt(offset=[-8. -6.], scale=[ 9. 16.])
    >>> b/a
    Dlt(offset=[0.88888889 0.375     ], scale=[0.11111111 0.0625    ])
    >>> a << _np.ones(2)
    array([4., 6.])
    '''

    # ----- base adaptation -----

    @property
    def dim(self):
        return self.bias_dim

    @property
    def bias(self):
        return self.__offset
    bias.__doc__ = Aff.bias.__doc__

    @bias.setter
    def bias(self, bias):
        if len(bias.shape) != 1:
            raise ValueError("Bias is not a vector, shape {}.".format(bias.shape))
        self.__offset = bias

    @property
    def bias_dim(self):
        return self.__offset.shape[0]
    bias_dim.__doc__ = Aff.bias_dim.__doc__

    @property
    def weight(self):
        return _np.diag(self.scale)
    weight.__doc__ = Aff.weight.__doc__

    @weight.setter
    def weight(self, weight):
        raise TypeError("Weight matrix is read-only.")

    @property
    def weight_shape(self):
        dim = self.scale_dim
        return (dim,dim)
    weight_shape.__doc__ = Aff.weight_shape.__doc__

    # ----- data encapsulation -----

    @property
    def offset(self):
        '''The offset/bias part of the dilated isometry.'''
        return self.__offset

    @offset.setter
    def offset(self, offset):
        if len(offset.shape) != 1:
            raise ValueError("Offset is not a vector, shape {}.".format(offset.shape))
        self.__offset = offset

    @property
    def scale(self):
        '''The scale component/scalar of the dilated isometry.'''
        return self.__scale

    @scale.setter
    def scale(self, scale):
        if len(scale.shape) != 1:
            raise ValueError("Scale is not a vector, shape {}.".format(scale.shape))
        self.__scale = scale

    @property
    def scale_dim(self):
        return self.__scale.shape[0]

    # ----- methods -----

    def __init__(self, offset=_np.zeros(3), scale=_np.ones(3), check_shapes=True):
        self.offset = offset
        self.scale = scale
        if check_shapes:
            _ = self.dim # just to check the shapes

    def __repr__(self):
        return "Dlt(offset={}, scale={})".format(self.offset, self.scale)

    def multiply(self, other):
        if not isinstance(other, dlt):
            return super(Dlt, self).multiply(other)
        return Dlt(self << other.offset, self.scale*other.scale)
    multiply.__doc__ = Aff.multiply.__doc__

    def invert(self):
        return Dlt(-self.offset/self.scale, 1/self.scale)
    invert.__doc__ = Aff.invert.__doc__


class dlt(Dlt):

    __doc__ = Dlt.__doc__

    @deprecated_func("0.4.2", suggested_func='mt.geo.dilatation.Dlt.__init__', removed_version="0.6.0")
    def __init__(self, *args, **kwargs):
        super(dlt, self).__init__(*args, **kwargs)


# ----- casting -----


_bc.register_cast(Dlt, Aff, lambda x: Aff(weight=x.weight, bias=x.bias, check_shapes=False))
_bc.register_cast(Aff, Dlt, lambda x: Dlt(offset=x.bias, scale=_np.diagonal(x.weight)))
_bc.register_castable(Aff, Dlt, lambda x: _np.count_nonzero(x.weight - _np.diag(np._diagonal(x.weight))) > 0)


# ----- transform functions -----


def transform_Dlt_on_Moments(dlt_tfm, moments):
    '''Transform the Moments using an affine transformation.

    Parameters
    ----------
    dlt_tfm : Dlt
        general dilatation
    moments : Moments
        general moments

    Returns
    -------
    Moments
        affined-transformed moments
    '''
    a = dlt_tfm.scale
    A = _np.diag(a)
    old_m0 = moments.m0
    old_mean = moments.mean
    old_cov = moments.cov
    new_mean = a*old_mean + dlt_tfm.offset
    new_cov = A @ old_cov @ A.T
    new_m0 = old_m0*abs(_np.prod(a))
    new_m1 = new_m0*new_mean
    new_m2 = new_m0*(_np.outer(new_mean, new_mean) + new_cov)
    return Moments(new_m0, new_m1, new_m2)
register_transform(Dlt, Moments, transform_Dlt_on_Moments)


def transform_Dlt_on_ndarray(dlt_tfm, point_array):
    '''Transform an array of points using a dilatation.

    Parameters
    ----------
    dlt_tfm : Dlt
        general dilatation
    point_array : numpy.ndarray with last dimension having the same length as the dimensionality of the transformation
        a point array

    Returns
    -------
    numpy.ndarray
        affine-transformed point array
    '''
    return point_array * dlt_tfm.scale + dlt_tfm.offset
register_transform(Dlt, _np.ndarray, transform_Dlt_on_ndarray)
register_transformable(Dlt, _np.ndarray, lambda x, y: x.ndim == y.shape[-1])


def transform_Dlt_on_PointList(dlt_tfm, point_list):
    '''Transform a point list using an affine transformation.

    Parameters
    ----------
    dlt_tfm : Dlt
        general dilatation
    point_list : PointList
        a point list

    Returns
    -------
    PointList
        affine-transformed point list
    '''
    return PointList(point_list.points * aff_tfm.scale + aff_tfm.offset, check=False)
register_transform(Dlt, PointList, transform_Dlt_on_PointList)


# ----- useful 2D transformations -----


@deprecated_func("0.3.5", suggested_func="mt.geo.dilatation.scale2d", removed_version="0.5.0")
def scale2d(scale_x=1, scale_y=None):
    '''Returns the scaling.'''
    if scale_y is None:
        scale_y = scale_x
    return Dlt(offset=_np.zeros(2), scale=_np.array([scale_x,scale_y]))

@deprecated_func("0.3.5", suggested_func=["mt.geo.dilatation.flipx2d", "mt.geo.affine2d.flipLR2d"], removed_version="0.5.0")
def flipx2d(width):
    '''Returns the transformation representing the horizontal flip of an image.'''
    return Dlt(offset=_np.array([width,0]), scale=_np.array([-1,1]))

@deprecated_func("0.3.5", suggested_func=["mt.geo.dilatation.flipy2d", "mt.geo.affine2d.flipUD2d"], removed_version="0.5.0")
def flipy2d(height):
    '''Returns the transformation representing the vertical flip of an image.'''
    return Dlt(offset=_np.array([0,height]), scale=_np.array([1,-1]))

